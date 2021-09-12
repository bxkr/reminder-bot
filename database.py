import json
from constants import *


class Data:
    def __init__(self, chat):
        self.__dict__['_chat'] = str(chat)
        self.__dict__['_time'] = DEFAULT_TIME
        self.__dict__['_message'] = DEFAULT_MESSAGE
        self.__dict__['_days'] = [True] * 7
        db = open(DATABASE, 'r')
        dict_f = json.loads(db.read())
        db.close()
        db = open(DATABASE, 'w')
        if str(chat) not in dict_f:
            dict_f[self.__dict__['_chat']] = {
                'message': self.__dict__['_message'],
                'time': self.__dict__['_time'],
                'days': self.__dict__['_days']
            }
        result = json.dumps(dict_f, indent=4)
        db.write(result)
        db.close()

    def __getattr__(self, item):
        with open(DATABASE, 'r') as db:
            dict_f = json.loads(db.read())
            return dict_f[self._chat][str(item)]

    def __setattr__(self, key, value):
        db = open(DATABASE, 'r+')
        dict_f = json.loads(db.read())
        db.close()
        dict_f[self._chat][key] = value
        db = open(DATABASE, 'w')
        db.write(json.dumps(dict_f, indent=4))
        db.close()
