from ..client.Client import Client
from .. import settings
from ..database.Database import Database
from ..encoder.Encoder import Encoder
from ..decoder.Decoder import Decoder
from ..httpclient.HttpClient import HttpClient
import logging
logger = logging.getLogger(settings.LOGGER_NAME)

######################
#WIP
######################

class Proxy(object):
    """
    proxy that takes client requests and sends them to konami servers
    TODO: reuse session to prevent logging in every time
    """
    def __init__(self, *args, **kwargs):
        # super(Proxy, self).__init__(is_proxy=1)
        pass

    def send_data(self, encrypted_request):
        """
        accepts encoded request
        """
        decoder = Decoder()
        data = decoder.decode(encrypted_request)
        if data['session_crypto']:
            # requires login
            logger.info("Got a command for proxying: {}, session: {}".format(data['data']['msgid'], data['session_key']))
            result = self.send_data_with_auth(data)
        else:
            logger.info("Got a command for proxying: {}".format(data['data']['msgid']))
            httpclient = HttpClient()
            result = httpclient.send(encrypted_request, '/tppstm/main').text
            logger.debug("Response from proxy server: {}".format(decoder.decode(result)))
        return result

    def send_data_with_auth(self, data):
        # at this point client sends data with session_crypto = True.
        # Since client is supposed to log in through our server, his creds
        # should be in our database. In this case we create a client instance
        # with his credentials, send data to konami, get the response, replace
        # session id and return the result to client.
        # Use it with care
        db = Database()
        try:
            db.connect()
        except Exception as e:
            # cannot conect for whatever reason
            logger.info('Cannot connect to database, trying local config')
        else:
            player = db.player_find_by_session_id(data['session_key'], True)
            if player:
                logger.info('Using login-pass from db for session: {}'.format(data['session_key']))
                login = player['steam_id']
                password = player['magic_hash']
            else:
                logger.info('Using login-pass from settings for session: {}'.format(data['session_key']))
                login = settings.STEAM_ID
                password = settings.MAGIC_HASH

        if login and password:
            client = Client()
            result = client.login(login, password)
            # result = client.proxy_command(data)
        else:
            logger.info('No login or password found for {}, session: {}'.format(data['data']['msgid'], data['session_key']))
            result = None

        return result



    # def send_full_command(self, command, command_name):
    #     # just take whole command and send it to konami
    #     # this function will work only for CMDs before authentication
    #     httpclient = HttpClient()
    #     response = None
    #     command_found = False
    #     for url in server_urls:
    #         if command_name in server_urls[url]:
    #             command_found = True
    #             response = httpclient.send(command, url)
    #             logger.info("Proxying command {}, url {}, status {}".format(str(command_name), str(url), str(response.status_code)))
    #     else:
    #         if not command_found:
    #             logger.info("Proxifying command {} failed, command not found in client_commands!".format(str(command_name)))
    #     if response:
    #         response = response.text
    #     return response

    # def send_full_command_with_auth(self, command, command_name, crypto_key=None):
    #     self._client = Client()
    #     if crypto_key:
    #         self._client.__encoder__.__init_session_blowfish__(
    #             bytearray(
    #                 base64.decodestring(crypto_key.encode())
    #             )
    #         )

    #     logger.info("Got a command for proxying: {}".format(str(command)))
    #     orig_session_key = command['session_key']

    #     player = self._db.player_find_by_session_id(orig_session_key, True)
    #     response = None
    #     if player:
    #         self._client.login(steam_id = player['steam_id'], magic_hash=player['magic_hash'])
    #         command['session_key'] = self._client.__session_key__
    #         response = self._client.send_command(command_name, options = command['data'])
    #         logger.info("Proxying command {},  response:\n {}".format(str(command_name), str(response)))
    #         response['session_key'] = orig_session_key
    #     else:
    #         logger.info("Cannot find player during proxy procedure")
    #     return response