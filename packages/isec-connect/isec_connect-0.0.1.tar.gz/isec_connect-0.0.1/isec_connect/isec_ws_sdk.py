from requests import api
import socketio
import json
import requests
import time
from datetime import datetime
from hashlib import sha256

class SocketEventIsec(socketio.ClientNamespace):
    def __init__(self, namespace, isec_instance):
        super().__init__(namespace)
        self.isec = isec_instance
        self.hostname = 'https://uatstreams.icicidirect.com'
        self.sio = socketio.Client()

    def connect(self):
        auth = {"user": self.isec.user_id, "token": self.isec.session_key}
        # print(auth)
        self.sio.connect(self.hostname, auth=auth)
        # print("connected with sid")
        # print(self.sio.sid)

    def on_disconnect(self):
        pass
    
    def on_message(self, data):
        self.isec.on_ticks(data)
    
    def watch(self, data):
        print("watching stock")
        print(data)
        self.sio.emit('join', data)
        self.sio.on('stock',self.on_message)
    
    def unwatch(self, data):
        print("unsubscribed:"+str(data))
        self.sio.emit("leave", data)
        
class IsecConnect():

    def __init__(self, api_key): #needed for hashing json data
        self.user_id = None
        self.api_key = api_key
        self.session_key = None
        self.secret_key = None    
        self.sio_handler = None
        self.on_ticks = None
                 
    def ws_connect(self):
        if not self.sio_handler:
            self.sio_handler = SocketEventIsec("/", self)
            self.sio_handler.connect()
                 
    def subscribe_stock(self, stock_names):
        if self.sio_handler:
            self.sio_handler.watch(stock_names)
    
    def unsubscribe_stock(self, stock_names):
        if self.sio_handler:
            self.sio_handler.unwatch(stock_names)
        # raise SioHandlerNot
    
    def test_api(self, json_data,url,api_name):
        current_date = datetime.now()
        current_timestamp = current_date.strftime("%d-%b-%Y %H:%M:%S")
        
        hashedWord = sha256((current_timestamp+json.dumps(json_data)+self.secret_key).encode("utf-8")).hexdigest()
        req_body = {
            "AppKey": self.api_key,
            "time_stamp" : current_timestamp,
            "JSONPostData" : json.dumps(json_data),
            "Checksum" : hashedWord
        }
        # print("------REQUEST FOR "+api_name+" --------")
        # print(req_body)
        # print("---------------------------------------")
        result = requests.post(url = url, data = json.dumps(req_body) , headers={"Content-Type": "application/json"})
        # print("----------RESPONSE--------------")
        # print(result.text)
        # print("--------------------------------")
        self.session_key = result.json()['Success']['session_token']
        self.user_id = result.json()['Success']['idirect_userid']
    
    def generate_session(self, api_secret, session_token):
        self.session_key = session_token
        self.secret_key = api_secret
        url = "http://103.87.40.246/customer/customerdetails"
        json_data = {
                # "UserID" : self.user_id,
                "API_Session" : self.session_key,
                "AppKey": self.api_key
        }
        self.test_api(json_data,url,'cust_details')
    