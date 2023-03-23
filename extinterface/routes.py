import json
from flask_restful import abort
from flask import Flask, request, render_template
from flask.views import MethodView
from flask_cors import cross_origin
from flask_socketio import SocketIO
from jsonschema import validate

from extinterface.configs.extinterface_config import SCHEMA
from extinterface_manager import ExtInterfaceManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


class MandrillEventWebhook(MethodView):
    """
    This class handles Mandrill event webhook requests
    """

    @cross_origin()
    def head(self):
        """
        This method handles HEAD request from Mandrill app
        It is used to test connectivity

        :URLPattern: http:head: /extinterface/mandrill/webhook/

        :return: SUCCESS OK string response
        """
        return "SUCCESS OK"

    @cross_origin()
    def post(self):
        """This method receives POST request from Mandrill and returns response

            :URLPattern: http:post:: /extinterface/mandrill/webhook/

            :Pseudocode: - validate the request
                         - process request further to authenticate signature and save to db
                         - post event notification to UI
                         - return response
        """
        try:
            webhook_data = request.form
            if 'mandrill_events' not in webhook_data:
                raise Exception('Invalid request')

            webhook_event_list = json.loads(webhook_data.get('mandrill_events'))

            for webhook_data in webhook_event_list:
                validate(instance=webhook_data, schema=SCHEMA["message_event_data"])

                webhook_data['webhook_signature'] = request.headers.get('X-Mandrill-Signature')
                webhook_data['comm_provider'] = 'MANDRILL'

                ext_mngr_obj = ExtInterfaceManager()
                response = ext_mngr_obj.process_comm_event_webhook(webhook_data)

                socketio.emit('event_notification', response, namespace='/')

            return "Completed"

        except ValueError as ex:
            print("ValueError in MandrillEventWebhook:post :", str(ex))
            abort(400, message=str(ex))
        except Exception as ex:
            print("Exception in MandrillEventWebhook:post :", str(ex))
            abort(500, message=str(ex))


app.add_url_rule('/extinterface/mandrill/webhook/', view_func=MandrillEventWebhook.as_view('mandrill_event_webhook'),
                 methods=['POST', 'HEAD'])


@app.route('/')
@cross_origin()
def index():
    """
    This method renders the simple mandrill event log UI page
    :return:
    """
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, port=5005, allow_unsafe_werkzeug=True, debug=True)
