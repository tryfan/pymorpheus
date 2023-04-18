"""
Python module for interacting with the Morpheus API

"""

import requests
import urllib3
import logging
import json

logger = logging.getLogger(__name__)

name = "MorpheusClient"


class MorpheusClientException(Exception):
    """ Base Exception Class """


class MethodTypeError(MorpheusClientException):
    """ Exception for bad HTTP request type """
    pass


class MorpheusClient:

    def __init__(self, morpheus_url, **kwargs):
        """
        The main Morpheus class

        :param morpheus_url: Morpheus URL
        :type morpheus_url: str
        :key username: Morpheus username
        :key password: Morpheus password
        :key token: Morpheus token
        :key client_id: Morpheus client_id, defaults to 'morph-cli'
        :return: __init__ should return None
        :rtype: None
        """

        # Required args
        self.morpheus_url = morpheus_url
        self.morpheus_api = morpheus_url + "/api"

        # Optional args
        optargs = {
            'username': "",
            'password': "",
            'token': "",
            'client_id': "morph-cli",
            'sslverify': True
        }

        # Assign optional args
        for arg in optargs.keys():
            if arg in kwargs:
                optargs[arg] = kwargs[arg]

        self.morpheus_client_id = optargs['client_id']
        self.sslverify = optargs['sslverify']

        oauth_path = "/oauth/token?grant_type=password&scope=write&client_id=%s" % self.morpheus_client_id
        oauth_url = self.morpheus_url + oauth_path

        if not optargs['sslverify']:
            urllib3.disable_warnings()

        if len(optargs['token']) > 0:
            authmethod = "token"
        else:
            authmethod = "login"

        if authmethod == "login":
            try:
                r = requests.post(oauth_url,
                                  data={'username': optargs['username'],
                                        'password': optargs['password']},
                                  verify=optargs['sslverify'])
                self.token = r.json()['access_token']
                self.headers = {'Authorization': "BEARER %s" % self.token,
                                "Content-Type": "application/json"}
            except requests.exceptions.SSLError:
                raise requests.exceptions.SSLError

        elif authmethod == "token":
            self.token = optargs['token']
            self.headers = {'Authorization': "BEARER %s" % self.token,
                            "Content-Type": "application/json"}

    def get_token(self):
        """
        Return API token

        :return: API Token
        :rtype: str
        """
        return self.token

    def _send_call(self, method, path, **kwargs):
        print('Calling method: %r to %r with %r' % (method, path, kwargs))

        url = ""
        method = method.lower()

        if method not in dir(requests.api):
            print("bad method type: %s" % method)
            raise MethodTypeError

        try:
            if not path.startswith("/"):
                path = "/" + path

            options = ""

            if "options" in kwargs:
                for tup in kwargs['options']:
                    options += tup[0] + "=" + tup[1] + "&"

            json_string = ""

            if "jsonpayload" in kwargs:
                try:
                    json_string = json.loads(kwargs['jsonpayload'])
                except ValueError as e:
                    print("Invalid JSON string passed:")
                    print(kwargs['jsonpayload'])
                    print(e)

            url = self.morpheus_api + path + "?" + options
            print(url)

            r = getattr(requests, method)(url,
                                          headers=self.headers,
                                          verify=self.sslverify,
                                          json=json_string)
            
            if r.status_code != 200:
                print(r.text)
                raise requests.HTTPError(r)

            return r.json()

        except requests.ConnectionError as cerr:
            print("Connection Error: ", cerr)
            print(url)
        except requests.HTTPError as herr:
            print("Bad status code returned: ", herr)
            print(url)
        except requests.Timeout as terr:
            print("Timeout: ", terr)
            print(url)
        except requests.exceptions.RequestException as err:
            print("Requests: Something went wrong: ", err)
            print(url)

    def call(self, method, path, **kwargs):
        """
        Calls an API path

        :param method: URL request method
        :type method: str
        :param path: API path
        :type path: str
        :key options: Key, value options
        :key jsonpayload: JSON data payload
        :return: JSON result
        :rtype: dict
        """

        result = self._send_call(method, path, **kwargs)
        return result
