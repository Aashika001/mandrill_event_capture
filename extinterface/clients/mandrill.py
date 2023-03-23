from extinterface.utils.extinterface_utils import generate_signature
from extinterface.clients.email_provider import EmailProvider
from extinterface.configs.client_config import MANDRILL_CLIENT_DATA
from extinterface.dao.extinterface_dao import ExtInterfaceDAO


class MandrillEventAdapter(EmailProvider):
    """
    This class handle events from Mandrill
    """

    def __int__(self):
        super(MandrillEventAdapter, self).__init__()
        self.__hmac_secret_key = MANDRILL_CLIENT_DATA['HMAC_KEY']
        self.__webhook_url = MANDRILL_CLIENT_DATA['WEBHOOK_URL']
        self.__hmac_signature = None

    def process_request(self, request):
        """
        This method processes webhook event request
        It validates webhook data by authenticating the signature
        If valid, saves event data in db and returns response
        Else raises exception
        :param request:
        :return: response
        """
        try:
            self.validate_webhook_data(request)

            # Save the validated event data to db
            webhook_event_id = ExtInterfaceDAO().create_event_data(request)

            response = dict(timestamp=request['ts'], event=request['event'], webhook_event_id=webhook_event_id)
            return response
        except Exception as ex:
            print("Exception in MandrillEventAdapter:process_request : ", str(ex))
            raise ex

    def validate_webhook_data(self, request_data):
        """
        Fetches the signature sent in the request
        Builds the signature and compares both the values
        If they do not match, raises an exception
        Else return True
        :param request_data:
        :return:
        """

        signature = request_data['webhook_signature']
        self.__build_hmac_signature()

        if self.__hmac_signature != signature:
            print("Signature not matching")
            raise Exception("Webhook data not authenticated")

        return True

    def __build_hmac_signature(self):
        """
        This method builds the base64 encoded HMAC-SHA1  signature with the webhook url
        :return:
        """
        sign_data = MANDRILL_CLIENT_DATA['WEBHOOK_URL']
        self.__hmac_signature = generate_signature(MANDRILL_CLIENT_DATA['HMAC_KEY'], sign_data)
        print("generated sign:", str(self.__hmac_signature))
