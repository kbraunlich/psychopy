############
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#############

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:03:17 2017

@author: bill.king
"""

import os
import json
import threading
import datetime
from sys import platform
# from psychopy import logging
import websocket
import ssl
import time
from pathlib import Path
import logging
# Set up logging for websockets library
logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)

MS_SEC_THRESHOLD = 1E+10


if platform == "linux" or platform == "linux2":
    raise NotImplementedError('Linux not yet supported')


class CortexApiException(Exception):
    pass

class CortexTimingException(Exception):
    pass

class CortexNoHeadsetException(Exception):
    pass


class Cortex(object):
    CORTEX_URL = "wss://localhost:6868"

    VERSION = 'debug'

    def __init__(self, client_id_file=None):
        home = str(Path.home())
        if client_id_file is None:
            client_id_file = ".emotiv_creds"
        file_path = os.path.join(home, client_id_file)
        self.parse_client_id_file(file_path)
        self.id_sequence = 0
        self.session_id = None
        self.marker_id = None
        self.waiting_for_id = None
        self.websocket = None
        logger.debug("Connection initializing")
        self.init_connection()
        logger.debug("Connection initialized")

        self.get_user_login()
        self.get_cortex_info()
        self.has_access_right()
        self.request_access()
        self.authorize()
        self.get_license_info()
        self.query_headsets()
        if len(self.headsets) > 0:
            if len(self.headsets) > 1:
                logger.warning("Currently Psychopy only supports a single headset")
                logger.warning("Connecting to the first headset found")
            time_str = datetime.datetime.now().isoformat()
            self.create_session(activate=True,
                              headset_id=self.headsets[0])
            self.create_record(title="Psychopy record {}".format(time_str))
        else:
            logger.error("Not able to find a connected headset")
            raise CortexNoHeadsetException("Unable to find Emotiv headset")
        self.running = False
        self.listen_ws = self.start_listening()

    def send_command(self, method, auth=True, **kwargs):
        self.send_wait_command(method, auth, wait=False, **kwargs)

    def send_wait_command(self, method, auth=True, callback=None,
                          wait=True, **kwargs):
        '''
        Send a command to cortex.

        Parameters:
            method: the cortex method to call as a string
            auth: boolean to indicate whether or not authentication is
                required for this method (may generate an additional call to
                authorize())
            callback: function to be called with the response data; defaults
                to returning the response data
            wait: flag whether to get response or send and forget
            **kwargs: all other keyword arguments become parameters in the
                request to cortex.
        Returns: response as dictionary if wait is True
        '''
        if not self.websocket:
            self.init_connection()
        if auth and not self.auth_token:
            self.authorize()
        msg = self.gen_request(method, auth, **kwargs)
        if method == 'injectMarker':
            self.waiting_for_id = self.id_sequence
        self.websocket.send(msg)
        if wait:
            logger.debug("data sent; awaiting response")
            resp = self.websocket.recv()
            if 'error' in resp:
                logger.warning(f"Got error in {method} with params {kwargs}:\n{resp}")
                raise CortexApiException(resp)
            resp = json.loads(resp)
            if callback:
                callback(resp)
            return resp
        return None

    def init_connection(self):
        """ Open a websocket and connect to cortex.  """
        self.websocket = websocket.WebSocket(sslopt=
                                             {"cert_reqs": ssl.CERT_NONE})
        self.websocket.connect(self.CORTEX_URL, timeout=60)
        print(self.websocket)

    def ws_listen(self):
        self.running = True
        while self.running:
            try:
                result = json.loads(self.websocket.recv())
                # if inject marker response save marker_id
                result_id = result.get("id", False)
                if result_id and self.waiting_for_id == result['id']:
                    marker_id = (result.get("result", {})
                                 .get("marker", {})
                                 .get("uuid", {}))
                    if marker_id:
                        self.marker_id = marker_id
                logger.debug('received:\n{}'.format(result))
            except Exception as e:
                import traceback
                logger.error(traceback.format_exc())
                logger.error("maybe the websocket was closed" + str(e))
        logger.debug("Finished listening")

    def to_epoch(self, dt=None):
        '''
        Convert a python datetime to a unix epoch time.

        Parameters:
            dt: input time; defaults to datetime.now()
        '''
        if not dt:
            dt = datetime.datetime.now()
            return int(dt.timestamp() * 1000)
        if isinstance(dt, datetime.datetime):
            if dt.tzinfo:
                return int(dt.timestamp() * 1000)
            else:
                raise CortexTimingException("datetime without timezone will not convert correctly")
        if isinstance(dt, int):
            if dt > MS_SEC_THRESHOLD:
                return dt
        return dt * 1000

    def parse_client_id_file(self, client_id_file_path):
        '''
        Parse a client_id file for client_id and client secret.

        Parameter:
            client_id_file_path: absolute or relative path to a client_id file

        We expect the client_id file to have the format:
        ```
        # optional comments start with hash
        client_id Jj2RihpwD6U3827GZ7J104URd1O9c0ZqBZut9E0y
        client_secret abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN
        ```
        '''
        self.client_id = None
        self.client_secret = None
        if not os.path.exists(client_id_file_path):
            raise OSError("no such file: {} Please add Cortex app credentials into '.emotiv_creds' file in home directory".format(client_id_file_path))
        with open(client_id_file_path, 'r') as client_id_file:
            for line in client_id_file:
                if line.startswith('#'):
                    continue
                (key, val) = line.split(' ')
                if key == 'client_id':
                    self.client_id = val.strip()
                elif key == 'client_secret':
                    self.client_secret = val.strip()
                else:
                    raise ValueError(
                        f'Found invalid key "{key}" while parsing '
                        f'client_id file {client_id_file_path}')

        if not self.client_id or not self.client_secret:
            raise ValueError(
                f"Did not find expected keys in client_id file "
                f"{client_id_file_path}")

    def gen_request(self, method, auth, **kwargs):
        '''
        Generate a JSON request formatted for Cortex.

        Parameters:
            method: method name as a string
            auth: boolean indicating whether or not authentication is required
                for this method (may generate an additional call to
                authorize())
            **kwargs: all other keyword arguments become parameters in the
                request.
        '''
        self.id_sequence += 1
        params = {key: value for (key, value) in kwargs.items()}
        if auth and self.auth_token:
            params['cortexToken'] = self.auth_token
        request = json.dumps(
            {'jsonrpc': "2.0",
             'method': method,
             'params': params,
             'id': self.id_sequence
             })
        logger.debug(f"Sending request:\n{request}")
        return request

    def authorize(self, license_id=None, debit=1):
        '''
        Generate an authorization token, required for most actions.
        Requires a valid license file, that the user be logged in via
        the Emotiv App, and that the user has granted access to this app.

        Optionally, a license_id can be specified to allow sharing a
        device-locked license across multiple users.

        Parameters:
            license_id (optional): a specific license to be used with the app.
                Can specify another user's license.
            debit (optional): number of sessions to debit from the license
        '''
        params = {'clientId': self.client_id,
                  'clientSecret': self.client_secret}
        if license_id:
            params['license_id'] = license_id
        if debit:
            params['debit'] = debit

        resp = self.send_wait_command('authorize', auth=False, **params)
        logger.debug(f"{__name__} resp:\n{resp}")
        self.auth_token = resp['result']['cortexToken']

    # def authorize(self, license_id=None, debit=1):
    #     self.body['method'] = 'authorize'
    #     self.body['auth'] = False
    #     self.body['params'] = {
    #         "clientId": self.client_id,
    #         "clientSecret": self.client_secret,
    #         "debit": 1
    #     }
    #     if license_id:
    #         self.body['params']['license_id'] = license_id
    #     while True:
    #         logging.debug("Authorizing!!!")
    #         self.send()
    #         result = json.loads(self.websocket.recv())
    #         internal_result = result.get('result', None)
    #         if internal_result is not None:
    #             auth = internal_result.get("cortexToken", None)
    #             if auth is not None:
    #                 break
    #     return auth

    # def send(self):
    #     s = json.dumps(self.body)
    #     logging.debug('sending:\n{}'.format(s))
    #     self.websocket.send(s)

    # I dont want to have to show the terms so
    # I should not accept the terms here
    # def accept_eula(self):
    #     self.body['method'] = "acceptLicense"
    #     self.body['params'] = {
    #         "_auth": self.auth
    #     }
    #     self.send()
    #     result = json.loads(self.websocket.recv())
    #     logging.debug('result', result)
    #     self.auth = result['result']['_auth']
    #     return result

    ##
    # Here down are cortex specific commands
    # Each of them is documented thoroughly in the API documentation:
    # https://emotiv.gitbook.io/cortex-api
    ##
    def inspectApi(self):
        ''' Return a list of available cortex methods '''
        resp = self.send_wait_command('inspectApi', auth=False)
        logger.debug(f"InspectApi resp:\n{resp}")


    def get_cortex_info(self):
        resp = self.send_wait_command('getCortexInfo', auth=False)
        logger.debug(f"{__name__} resp:\n{resp}")

    def flush_websocket(self):
        self.send_command('getCortexInfo', auth=False)

    def get_license_info(self):
        resp = self.send_wait_command('getLicenseInfo')
        logger.debug(f"{__name__} resp:\n{resp}")

    def query_headsets(self):
        resp = self.send_wait_command('queryHeadsets', auth=False)
        self.headsets = [h['id'] for h in resp['result']]
        logger.debug(f"{__name__} found headsets {self.headsets}")
        logger.debug(f"{__name__} resp:\n{resp}")

    def get_user_login(self):
        resp = self.send_wait_command('getUserLogin', auth=False,
                                      callback=self.get_user_login_cb)

    def get_user_login_cb(self, resp):
        ''' Example of using the callback functionality of send_command '''
        resp = resp['result'][0]
        if 'loggedInOSUId' not in resp:
            logger.debug(resp)
            raise CortexApiException(
                f"No user logged in! Please log in with the Emotiv App")
        if (resp['currentOSUId'] != resp['loggedInOSUId']):
            logger.debug(resp)
            raise CortexApiException(
                f"Cortex is already in use by {resp.loggedInOSUsername}")
        logger.debug(f"{__name__} resp:\n{resp}")

    def has_access_right(self):
        params = {'clientId': self.client_id,
                  'clientSecret': self.client_secret}
        resp = self.send_wait_command('requestAccess', auth=False, **params)
        logger.debug(f"{__name__} resp:\n{resp}")

    def request_access(self):
        params = {'clientId': self.client_id,
                  'clientSecret': self.client_secret}
        resp = self.send_wait_command('requestAccess', auth=False, **params)
        logger.debug(f"{__name__} resp:\n{resp}")

    def control_device(self, command, headset_id=None,
                       flex_mapping=None):
        if not headset_id:
            headset_id = self.headsets[0]
        params = {'headset': headset_id,
                  'command': command}
        if flex_mapping:
            params['mappings'] = flex_mapping
        resp = self.send_wait_command('controlDevice', **params)
        logger.debug(f"{__name__} resp:\n{resp}")

    def create_session(self, activate, headset_id=None):
        status = 'active' if activate else 'open'
        if not headset_id:
            headset_id = self.headsets[0]
        params = {'cortexToken': self.auth_token,
                  'headset': headset_id,
                  'status': status}
        resp = self.send_wait_command('createSession', **params)
        self.session_id = resp['result']['id']
        logger.debug(f"{__name__} resp:\n{resp}")

    def create_record(self, title=None):
        if not title:
            time_str = datetime.datetime.now().isoformat()
            title = f'Psychopy recording ' + time_str
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id,
                  'title': title}
        resp = self.send_wait_command('createRecord', **params)
        logger.debug(f"{__name__} resp:\n{resp}")
        return resp

    def stop_record(self):
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id}
        resp = self.send_wait_command('stopRecord', **params)
        logger.debug(f"{__name__} resp:\n{resp}")
        return resp

    def close_session(self):
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id,
                  'status': 'close'}
        resp = self.send_wait_command('updateSession', **params)
        logger.debug(f"{__name__} resp:\n{resp}")
        self.disconnect()

    def inject_marker(self, label='', value=0, port='psychopy',
                      dt=None):
        ms_time = self.to_epoch(dt)
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id,
                  'label': label,
                  'value': value,
                  'port': port,
                  'time': ms_time}
        self.send_command('injectMarker', **params)

    def update_marker(self, dt=None):
        ms_time = self.to_epoch(dt)
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id,
                  'markerId': self.marker_id,
                  'time': ms_time}
        self.send_command('updateMarker', **params)

    def start_listening(self):
        self.running = True
        listen_ws = threading.Thread(target=self.ws_listen)
        listen_ws.start()
        return listen_ws

    def stop_listening(self):
        self.running = False
        self.flush_websocket()  #

    def disconnect(self):
        self.stop_listening()
        time.sleep(2)
        self.websocket.close()


if __name__ == "__main__":
    cortex = Cortex()
    print("sending marker")
    cortex.inject_marker(label="test_marker", value=4, port="psychpy")
    time.sleep(10)
    print("sending stop")
    cortex.update_marker()
    print("finished")
    print(cortex.session_id)
