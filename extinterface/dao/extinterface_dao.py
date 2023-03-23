import mysql.connector
import json
from datetime import datetime


class ExtInterfaceDAO(object):
    def __init__(self):

        self.conn = mysql.connector.connect(host='192.168.56.102',
                                            user='root',
                                            passwd='Global!23',
                                            db='workgen',
                                            port='3306',
                                            autocommit=False)
        self.cursor = self.conn.cursor(dictionary=True)

    def create_event_data(self, event_data):
        """
        This methos creates a record in webhook_event_data, to save the webhook data
        :param event_data: request dict
        :return: webhook_event_id
        """
        try:
            create_event_query = "insert into webhook_event_data (webhook_event_id, comm_provider, msg_id, " \
                                 "event_data, created_by, created_datetime," \
                                 "modified_by, modified_datetime) values (NULL, %s, %s, %s, %s, %s, NULL, NULL)"
            args = (
                event_data['comm_provider'],
                event_data['_id'],
                json.dumps(event_data),
                'extinterface',
                datetime.now(),
            )
            self.cursor.execute(create_event_query, args)
            webhook_event_id = self.cursor.lastrowid
            print("saved event data with webhook_event_id :", webhook_event_id)

            if not webhook_event_id:
                print('DB Error: Unable to create event data record')
                raise Exception('DB Error: Unable to create event data record')

            self.conn.commit()
            return webhook_event_id
        except Exception as exp:
            print("Exception in ExtInterfaceDAO:create_event_data :", str(exp))
            raise
        finally:
            self.cursor.close()
