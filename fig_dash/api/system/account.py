#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import sqlite3
import requests
# import dataclasses
from typing import Union
from dataclasses import dataclass
# from sqlite3.dbapi2 import OperationalError
from fig_dash.assets import FigD
from fig_dash.api.system.database import FigDashAddressData, FigDashAppDatabase, FigDashPassword, FigDatabaseModel, FigDashMailData, FigDashImageData, FigDashAddressData, FigDashPhoneNumberData, FigDashGenderData


def quick_geo_locator():
    '''hacky way to get location tuple'''
    data_js_ext_url = "https://datajsext.com/ExtService.svc/getextparams"
    # json response.
    response = requests.get(data_js_ext_url).text
    try:
        all_data = json.loads(response)
        city = all_data['city']['en']
        subdiv = all_data['subdiv'][0]['en']
        country = all_data['cnames']['en']

        return (city, subdiv, country)
    
    except KeyError as e:
        print(e)
        
        return ("", "", "")

DEFAULT_USERDATA_PATH = os.path.expanduser("~/.fig_dash/accounts.db")
# data associated with a fig-dash user.
@dataclass
class FigDashUser(FigDatabaseModel):
    '''the user profile of a fig-user.'''
    username: str
    email: FigDashMailData
    password: FigDashPassword
    firstname: Union[str, None]=None
    lastname: Union[str, None]=None
    age: int=18
    gender: FigDashGenderData=FigDashGenderData.Male
    address: Union[FigDashAddressData, None]=None
    phonenumber: Union[FigDashPhoneNumberData, None]=None
    profile_picture: Union[FigDashImageData, None]=None

    def init(self, mode="partial"):
        self.setPrimaryKey("username")
        self.setFieldKeywords("username", "NOT NULL", "UNIQUE")
        self.setFieldKeywords("email", "NOT NULL")
        self.setFieldKeywords("password", "NOT NULL")
        if self.firstname is None:
            if self.gender == FigDashGenderData.Male:
                self.firstname = "John"
            elif self.gender == FigDashGenderData.Female:
                self.firstname = "Jane"
            elif self.gender == FigDashGenderData.TransMale:
                self.firstname = "Michael"
            elif self.gender == FigDashGenderData.TransFemale:
                self.firstname = "Christine"
            elif self.gender in [FigDashGenderData.NonBinary, FigDashGenderData.Other]:
                self.firstname = "Morgan"
        if self.lastname is None:
            if self.gender in [FigDashGenderData.Female, FigDashGenderData.Male, FigDashGenderData.NonBinary, FigDashGenderData.Other]:
                self.lastname = "Doe"
            elif self.gender == FigDashGenderData.TransMale:
                self.lastname = "Dillon"
            elif self.gender == FigDashGenderData.TransFemale:
                self.lastname = "Jorgensen"
        self.profile_picture = FigD.icon("navbar/account.png") 
        if mode == "full":
            loc_tuple = quick_geo_locator()
            location = ", ".join(loc_tuple)
            # get address using ip geo location data.
            self.address = FigDashAddressData.fromString(location) 
            # this: (https://projectricochet.com/blog/most-common-phone-number)
            self.phonenumber = FigDashPhoneNumberData.fromString("2147483648") 

    def __str__(self):
        return f'''{self.username} ({self.firstname} {self.lastname})
✉ email: {self.email}
📅 age: {self.age}
⚥ gender: {self.gender}
⌖ address: {self.address}
☎ phonenumber: {self.phonenumber}'''
# all data associated with a Fig Account.
class FigDashAccount:
    '''fig-dash account manager.'''
    def __init__(self, db_path=DEFAULT_USERDATA_PATH):
        '''
        initialize the user profile of a fig-dash user using the database path
        '''
        super(FigDashAppDatabase, self).__init__(
            db_path=db_path,
            table_names={
                "user": "FigDashUserData",
                "passwords": "FigDashUserPasswords"
            },
            table_fields={
                "user": {
                    "username": "text",
                    "password": "text",
                    "email": "text",
                    "firstanme": "text",
                    "lastanme": "text",
                    "age": "integer",
                    "gender": "text",
                    "address": "text",
                    "phonenumber": "text",
                    "image": "text",
                }
            },
        )
        # self.path = db_path
        # # ensure that the TABLE FigDashUserData exits.
        # try: 
        #     # open a connection to the fig_account_data database.
        #     connection = sqlite3.connect(db_path) 
        #     cursor = connection.cursor()
        #     # create the userdata table.
        #     cursor.execute('''CREATE TABLE FigDashUserData (username text, email text, password text, firstname text, lastname text, age integer, gender text, address text, phonenumber text, image text)''')
        #     # save the changes.
        #     connection.commit()
        #     # close the database. 
        #     connection.close() 
        #     print("created TABLE FigDashUserData")
        # except sqlite3.OperationalError:
        #     print("FigDashUserData already exists!")

    # def create(self, username: str, 
    #            email: str, password: str, 
    #            **data):
    #     '''create account.'''
    #     con = sqlite3.connect(self.db_path)
    #     password = FigDashUserPassword(password)
    #     user = FigDashUser(
    #         username=username,
    #         email=email,
    #         password=password.toObjectStr(),
    #         **data
    #     )
    #     print(f"Created New User: {user}")
    #     con.close()

    # def login(self, username: str, password: str):
    #     '''authenticate the user.'''
        # print("logging in with password")
