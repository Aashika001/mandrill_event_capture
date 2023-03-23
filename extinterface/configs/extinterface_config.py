from extinterface.clients.mandrill import MandrillEventAdapter

WEBHOOK_EVENT_TYPE = ['send', 'deferral', 'hard_bounce', 'soft_bounce', 'delivered', 'open', 'click', 'spam', 'unsub',
                      'reject']

COMM_PROVIDER_MAP = {'MANDRILL': MandrillEventAdapter}

SCHEMA = {
    "message_event_data": {
        "type": "object",
        "properties": {
            "ts": {"type": "integer"},
            "event": {"type": "string", "enum": WEBHOOK_EVENT_TYPE},
            "_id": {"type": "string"},
            "msg": {"type": "object",
                    "properties": {
                        "_id": {"type": "string"},
                        "ts": {"type": "integer"},
                        "email": {"type": "string"},
                        "sender": {"type": "string"},
                        "subject": {"type": "string"},
                        "smtp_events": {"type": "object"},
                        "opens": {"type": "array",
                                  "items": {"type": "object",
                                  "properties": {
                                      "ts": {"type": "integer"},
                                      "ip": {"type": "string"},
                                      "location": {"type": "string"},
                                      "ua": {"type": "string"},
                                  },
                                  "required": ["ts"]}
                                  },
                        "clicks": {"type": "array",
                                   "items": {"type": "object",
                                  "properties": {
                                      "ts": {"type": "integer"},
                                      "url": {"type": "string"},
                                  },
                                   "required": ["ts"]}},
                        "state": {"type": "string"}

                    },
                    "required": ["_id", "ts"]},
            "url": {"type": "string"},
            "ip": {"type": "string"},
            "user_agent": {"type": "string"},
            "location": {"type": "object",
                         "properties": {
                             "country_short": {"type": "string"},
                             "country_long": {"type": "string"},
                             "region": {"type": "string"},
                             "city": {"type": "string"},
                             "postal_code": {"type": "string"},

                         }},
            "user_agent_parsed": {"type": "object",
                                  "properties": {
                                      "mobile": {"type": "boolean"},
                                      "os_company": {"type": "string"},
                                      "os_name": {"type": "string"},
                                  }},
        },
        "required": ["ts", "event", "_id"]
    }
}
