
#from dotenv import load
#from dotenv import load_dotenv
#from dotenv import Dotenv
import os
import requests
import xmlrpc.client
import json

#Response
from .return_handling import ReturnHandling

#Auth
from requests.auth import HTTPBasicAuth #For CouchDB


class DBHelper():
    
    #Flask App Builder
    fab_access_token = ""
    fab_refresh_token = ""
    fab_username = ""
    fab_passowrd = ""

    #General
    db_type = "FAB"
        
    #Odoo
    db_name = ""
    odoo_server_url = ""
    odoo_server_ip = ""
    odoo_server_port= ""
    odoo_access_token = ""

    #FAB
    fab_server_url = ""
    fab_server_ip = ""
    fab_server_port= ""

    def __init__(self):
        self.url = self.odoo_server_url + ":" + self.odoo_server_port        
        self.fab_url = self.fab_server_url + ":" + self.fab_server_port

    def login(self, username, password):        
        self.username = username
        self.password = password
        self.uid = self.common.authenticate(self.db_name, username, password, {})
        return self.uid

    def db_login(self, username, password):
        pass

    def auth(self):
        response = requests.get('http://pos-dev.server007.weha-id.com/api/auth/token?db='+ self.db_name + '&login=' + self.login + '&password=' + self.password)
        print(response.status_code)
        if str(response.status_code) != '200':
            print("Http 401")
            return True, "Error Authentication" , False
        
        response_json = response.json()
        print(response_json)
        return False, "Authenctication Successfully", response_json

    # General CRUD for All Connection Type
    def search(self, data):
        if self.db_type == "FAB":
            if data['type'] == "GET":
                endpoint = data['endpoint']
                if 'id' in data.keys():
                    #Search By ID
                    id = data['id']
                else:
                    #Search By Query
                    filters = data['filters']
                columns = data['columns']

            if data['type'] == "POST":
                pass
            if data['type'] == "PUT":
                pass
            if data['type'] == "PATCH":
                pass
            if data['type'] == "DELETE":
                pass
                
    def create(self, data):
        pass

    def write(self, data):
        pass
    
    def delete(self, data):
        pass

    # CouchDB CRUD
    def _couchdb_get(self, endpoint, auth, headers={}, form_data={}):
        response = requests.get(endpoint, auth=auth)
        print(response.text)
        if response.status_code == 200:
            return ReturnHandling(False, "", response.json())
        if response.status_code == 401:
            return ReturnHandling(True, "Record Not Found", response.json())
        else:
            return ReturnHandling(True, "Error", response.json()) 

    def _couchdb_post(self, endpoint, auth, headers={}, form_data={}):
        response = requests.post(endpoint, auth=auth, headers=headers, data=json.dumps(form_data))
        print(response.text)
        if response.status_code == 200:
            return ReturnHandling(False, "", response.json())
        if response.status_code == 201:
            return ReturnHandling(False, "", response.json())
        else:
            return ReturnHandling(True, "", response.json()) 

    def _couchdb_put(self, endpoint, auth, headers={}, form_data={}):
        response = requests.put(endpoint, auth=auth, headers=headers, data=json.dumps(form_data))
        print(response.text)
        if response.status_code == 200:
            return ReturnHandling(False, "", response.json())
        if response.status_code == 201:
            return ReturnHandling(False, "", response.json())
        else:
            return ReturnHandling(True, "", response.json()) 

    def _couchdb_delete(self, endpoint, auth, headers={}, form_data={}):
        response = requests.delete(endpoint, auth=auth, headers=headers)
        print(response.text)
        if response.status_code == 200:
            return ReturnHandling(False, "", response.json())
        else:
            return ReturnHandling(True, "", response.json()) 

    # Custom API CRUD
    def api_get(self, endpoint, headers={}, form_data={}):
        err, message, auth = self.auth()
        if not err:
            headers.update({'access-token': auth['access_token']})
            response = requests.get(self.odoo_server_url + endpoint, headers=headers, data=form_data)
            print(response.text)
            if str(response.status_code) != '200':
                print("Http 401")
                return False, "Error", []
            
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                return True, response_json['message'], []
            else:
                datas = response_json['data']
                return False, '', datas
        else:
            return err, message, []

    def api_post(self, endpoint, headers={}, form_data={}):
        response = requests.post(self.odoo_server_url + endpoint, headers=headers, data=form_data)
        
        if str(response.status_code) != '200':
            print("Http 401")
            return ReturnHandling(False, "Error HTTP", [])
            
        response_json  = response.json()
        print("API POST")
        print(response_json)
        return ReturnHandling(response_json['err'], response_json['message'], response_json['data'])

    def api_put(self, endpoint, headers={}, form_data={}):
        pass 

    def api_delete(self, endpoint, headers={}, form_data={}):
        pass 

    # FAB CRUD
    def fab_login(self, login, password):
        headers = {
            'Content-Type': 'application/json'
        }
        endpoint = "/api/v1/security/login"
        url = self.fab_server_url + ":"  + self.fab_server_port + endpoint
        payload = {
            'username': login, 
            'password': password,
            'provider': 'db',
            'refresh': True
        }
        data=json.dumps(payload)
        try:
            response = requests.post(url, headers=headers, data=data)
            response_json  = response.json()
            print(response_json)
            if response.status_code == 200:
                return ReturnHandling(False, response.status_code, "Login Successfully", response_json)
            else:
                return ReturnHandling(True, response.status_code,  "Error : " + str(response.status_code) + " - " + response_json['message'], [])
        except requests.ConnectionError as err:
            print(err)
            return ReturnHandling(True,0, "Connection Error", [])

    def fab_refresh_token(self):
        headers = {} 
        headers.update({'Authorization': "Bearer " + self.fab_refresh_token})
        url = "http://localhost:5000/api/v1/security/refresh"
        payload = {}
        data=json.dumps(payload)
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
        except requests.Connection as err:
            return ReturnHandling(True, 0, "Connection Error", [])
        
    def fab_get(self, endpoint, headers={}, id=None):
        headers.update({'Authorization': "Bearer " +  self.controller.fab_access_token})
        headers.update({'Content-Type': 'application/json'})
        try:
            if id:
                endpoint = self.fab_server_url + ":"  + self.fab_server_port  + endpoint + "/" + str(id)
            else:
                endpoint = self.fab_server_url + ":"  + self.fab_server_port + endpoint
            print(endpoint)
            response = requests.get(endpoint, headers=headers)    
            if id:        
                if response.status_code != 200:
                    print(response.status_code)
                    print(response.text)
                    return ReturnHandling(True, response.status_code, "Error : " + str(response.status_code) + " - " + response.text, [])
            else:
                if response.status_code not in (200,201):
                    print(response.status_code)
                    print(response.text)
                    return ReturnHandling(True, response.status_code, "Error : " + str(response.status_code) + " - " + response.text, [])

            #Return Only Data
            response_json = response.json()
            result = response_json['result']
            if id:
                result.update({'id': response_json['id']})
            return ReturnHandling(False, response.status_code, '', result)
        except requests.ConnectionError as err:
            return ReturnHandling(True, 0, err, [])

    def fab_gets(self, endpoint, headers={}, form_data={}, multiple=True):
        print("FAB GETS")
        headers.update({'Authorization': "Bearer " +   self.controller.fab_access_token})
        headers.update({'Content-Type': 'application/json'})
        try:
            response = requests.get(self.fab_server_url + ":"  + self.fab_server_port + endpoint, headers=headers)
            response_json  = response.json()
            print(response_json)
            
            if response.status_code != 200:
                print(response.status_code)
                return ReturnHandling(True, response.status_code, "Error : " + str(response.status_code), [])

            datas=[]
            if response_json['count'] == 0:
                return ReturnHandling(True, response.status_code ,'Data not found', [])
            else:
                #Return Only Data
                for i in range(response_json['count']):
                    data = response_json['result'][i]
                    data.update({'id': response_json['ids'][i]})
                    datas.append(data)
            print(datas)
            return ReturnHandling(False, response.status_code,  '', datas)

        except requests.ConnectionError as err:
            return ReturnHandling(True,0,  err, [])

    def fab_post(self, endpoint, headers={}, form_data={}):
        headers.update({'Authorization': "Bearer " +   self.controller.fab_access_token})
        headers.update({'Content-Type': 'application/json'})
        try:
            response = requests.post(self.fab_server_url + ":"  + self.fab_server_port + endpoint, headers=headers, data=json.dumps(form_data))
            response_json  = response.json()
            if str(response.status_code) != '201':
                print("Http 401")
                print(response_json)
                return ReturnHandling(True, "Error : " + str(response.status_code) + " - " + str(response_json['message']) , [])
                
            result =  response_json['result']
            result.update({'id': response_json['id']})
            return ReturnHandling(False, response.status_code, 'Create Succesfully' , result)
        except requests.ConnectionError as err:
            return ReturnHandling(True, 0, err, [])

    def fab_put(self, endpoint, headers={}, id=None, form_data={}):
        headers.update({'Authorization': "Bearer " +  self.controller.fab_access_token})
        headers.update({'Content-Type': 'application/json'})
        try:
            print(form_data)
            response = requests.put(self.fab_server_url + ":"  + self.fab_server_port + endpoint + "/" + str(id), headers=headers, data=json.dumps(form_data))            
            if response.status_code != 200:
                print(response.status_code)
                print(response.text)    
                return ReturnHandling(True, response.status_code, "Error : " + str(response.status_code) + " - " + response.text, [])
            
            #Return Only Data
            response_json = response.json()
            result = response_json['result']
            result.update({'id': id})
            return ReturnHandling(False, response.status_code,'', result)
        except requests.ConnectionError as err:
            return ReturnHandling(True, 0, err, [])

    def fab_delete(self, endpoint, headers={}, id=None):
        headers.update({'Authorization': "Bearer " +   self.controller.fab_access_token})
        headers.update({'Content-Type': 'application/json'})
        try:
            response = requests.delete(self.fab_server_url + ":"  + self.fab_server_port + endpoint + "/" + str(id), headers=headers)
            response_json  = response.json()
            if response.status_code != 200:
                return ReturnHandling(True, response.status_code, "Error : " + str(response.status_code) + " - " + response_json['message'] , [])
            return ReturnHandling(False, response.status_code, response_json['message'] , [])
        except requests.ConnectionError as err:
            return ReturnHandling(True, 0, err, [])

    # ODOO CRUD
    def odoo_get(self, endpoint, headers={}, form_data={}):
        err, message, auth = self.auth()
        if not err:
            headers.update({'access-token': auth['access_token']})
            response = requests.get(self.odoo_server_url + endpoint, headers=headers, data=form_data)
            print(response.text)
            if str(response.status_code) != '200':
                print("Http 401")
                return False, "Error", []
            
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                return True, response_json['message'], []
            else:
                datas = response_json['data']
                return False, '', datas
        else:
            return err, message, []

    def odoo_post(self, endpoint, headers={}, form_data={}):
        response = requests.post(self.odoo_server_url + endpoint, headers=headers, data=form_data)
        
        if str(response.status_code) != '200':
            print("Http 401")
            return ReturnHandling(False, "Error HTTP", [])
            
        response_json  = response.json()
        print("API POST")
        print(response_json)
        return ReturnHandling(response_json['err'], response_json['message'], response_json['data'])

    def odoo_put(self, endpoint, headers={}, form_data={}):
        pass 
    
    def odoo_delete(self, endpoint, headers={}, form_data={}):
        pass 
