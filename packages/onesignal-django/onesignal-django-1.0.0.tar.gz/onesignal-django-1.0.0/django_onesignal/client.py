from typing import List
import requests
import json
import datetime

class OnesignalClient():
#Set the Onesignal app_id

    def set_app_id(self, app_id: str,auth_user_key:str=None):
        self.app_id = app_id
        if auth_user_key:
            self.auth_user_key = auth_user_key


    #Create a message with title content and id/ids of target device/devices
    def create_message(self, title: str, cont:str, ids: List[str]):
        self.payload ={
                        "app_id": self.app_id ,           
                        "include_player_ids":ids ,
                        "headings": {"en": title},
                        "contents": {"en": cont}}

    #Create a message and send at specific time (Greenwich time)
    def create_future_message(self, title: str, cont:str, ids: List[str], date: str):
        self.payload = {
                        "app_id": self.app_id ,           
                        "include_player_ids":ids ,
                        "headings": {"en": title},
                        "contents": {"en": cont},              
                        "send_after": date.strftime("%Y-%m-%d %H:%M:%S")+" GMT+000",
                        }  
                        
    #Based on documentation check if requires_auth_user_key is needed for the type of notification
    async def send_message(self, requires_auth_user_key:bool=False):
        url="https://onesignal.com/api/v1/notifications"
        if requires_auth_user_key:
            header = {
                        "Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Basic "+ self.auth_user_key
                     }
        else:
            header = {"Content-Type": "application/json; charset=utf-8"}

        return requests.post(url, headers=header, data=json.dumps(self.payload))


                            