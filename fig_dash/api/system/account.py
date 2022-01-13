#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3
# import dataclasses
from enum import Enum
from typing import Union
from dataclasses import dataclass
# from sqlite3.dbapi2 import OperationalError
from fig_dash.api.system.database import FigDashAppDatabase, FigDashAppPassword, FigDatabaseModel


DEFAULT_USERDATA_PATH = os.path.expanduser("~/.fig_dash/accounts.db")
# possible gender identites.
class FigDashUserGender(Enum):
    Male = 0
    Female = 1
    TransMale = 2
    TransFemale = 3
    NonBinary = 4
    Other = 5

# email id.
class FigDashUserEmail:
    pass

# phone number.
class FigDashPhoneNumber:
    pass
# data associated with a fig-dash user.

@dataclass(frozen=True)
class FigDashUser(FigDatabaseModel):
    '''the user profile of a fig-user.'''
    username: str
    email: FigDashUserEmail
    password: str
    firstname: str="John"
    lastname: str="Doe"
    age: int=18
    gender: FigDashUserGender=FigDashUserGender.Male
    address: Union[str, None]=None
    phonenumber: Union[FigDashPhoneNumber, None]=None
    image: Union[str, None]=None

    def __str__(self):
        return f'''
        {self.username} ({self.firstname} {self.lastname})
        email: {self.email}
        age: {self.age}
        gender: {self.gender}
        address: {self.address}
        phonenumber: {self.phonenumber}
        '''
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
