from extinterface.configs.extinterface_config import COMM_PROVIDER_MAP


class ExtInterfaceManager(object):
    def __int__(self):
        self.comm_provider_obj = None

    def process_comm_event_webhook(self, request_data):
        """
        This method handles webhook event request by using appropriate comm provider method
        :param request_data:
        :return:
        """
        comm_provider = request_data['comm_provider']
        self.comm_provider_obj = COMM_PROVIDER_MAP[comm_provider]()
        response = self.comm_provider_obj.process_request(request_data)

        return response
