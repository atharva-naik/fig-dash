import os
import uuid
import string
import hashlib
import sqlite3
import dataclasses
from dataclasses import dataclass


@dataclass(frozen=True)
class FigDatabaseModel:
    '''A database model class.'''
    def toSqlRecord(self):
        '''convert an instance of the data class to a column list for INSERT query execution in an SQlite3 database.'''
        SQLRecord = "("
        for field in dataclasses.fields(self):
            field_name = field.name
            field_type = field.type
            field_value = getattr(self, field_name)
            if field_type in [int, float]:
                SQLRecord += f"{field_value}, "
            else: 
                SQLRecord += f"'{field_value}', "
        SQLRecord = SQLRecord.strip(",")
        SQLRecord += ")"

        return SQLRecord

    def getSqlHeader(self, type_="SQLITE3"): 
        '''convert the class definition to column list of field names and types for CREATE TABLE query execution in an SQlite3 database.'''
        SQLHeader = "("
        dtype_map: dict={
            "str": "REAL",
            "int": "INTEGER",
            "double": "REAL",
            "float": "REAL",
        }
        for field in dataclasses.fields(self):
            field_name = field.name
            field_type = self.dtype_map[field.type]
            SQLHeader += f"{field_name} {field_type}, "         
        SQLHeader = SQLHeader.strip(",")
        SQLHeader += ")"

        return SQLHeader

# app password model.
class FigDashAppPassword:
    def __init__(self, raw_str: str=""):
        '''initialize password from unsalted and unhashed string'''
        self.salt = uuid.uuid4().hex
        self._password = self.hash_and_salt(raw_str, self.salt)

    def validate(self, password: str):
        '''validate the password: ensure that all available rules apply.'''
        for rule in self:
            if rule(password) == False: 
                return False
        
        return True

    def __iter__(self):
        for attr in dir(self):
            if attr.endswith("_rule"):
                yield getattr(self, attr)

    def uppercase_rule(self, password: str):
        '''rule: at least one uppercase character'''
        for char in string.ascii_uppercase:
            if char in password:
                return True
        
        return False

    def lowercase_rule(self, password: str):
        '''rule: at least one lowercase character'''
        for char in string.ascii_lowercase:
            if char in password:
                return True
        
        return False

    def length_rule(self, password: str):
        '''rule: minimum length of 12 characters.'''
        if len(password)<12: return False
        else: return True

    def non_alphanumeric_rule(self, password: str):
        '''rule: at least one non alphanumeric character should be present.'''
        for char in password:
            if not(char.isalpha() or char.isdigit()):
                return True

        return False

    def number_rule(self, password: str):
        '''rule: at least one number should be present.'''
        for char in string.digits:
            if char in password:
                return True
        
        return False

    def __str__(self):
        return f'''salt: {self.salt}
password: {self._password}'''

    def __repr__(self):
        objectStr = self.toObjectStr()
        return f"FigDashUserPassword.fromObjectStr('{objectStr}')"

    def check(self, raw_str: str):
        _password = self.hash_and_salt(raw_str, self.salt)
        return _password == self._password

    def hash_and_salt(self, raw_str: str, salt: str):
        return hashlib.sha512(
            salt.encode("utf-8")+
            raw_str.encode("utf-8")
        ).hexdigest()

    def toObjectStr(self):
        '''get serialized object string.'''
        return self._password+self.salt

    @classmethod
    def fromObjectStr(cls, objectStr: str):
        obj = cls()
        obj._password = objectStr[:128]
        obj.salt = objectStr[-32:]
        
        return obj

# all data associated with a Fig Application.
class FigDashAppDatabase:
    '''fig-dash application database template.'''
    def __init__(self, db_path: str, table_names: dict, 
                 table_fields: dict, table_keys: dict):
        '''
        initialize the user's account details.
        for the fig accounts it has the username, email, password hash etc.
        for the email account it has the email id and password.
        '''
        self.path = db_path
        self.table_keys = table_keys
        self.table_names = table_names
        self.table_fields = table_fields
        try: 
            # open a connection to the database.
            connection = sqlite3.connect(db_path) 
            cursor = connection.cursor()
            # create the user data table.
            user_table = table_names["user"]
            user_fields = table_fields["user"]
            user_primary_key = table_keys["user"]
            creation_query = f"CREATE TABLE {user_table} ("
            # construct the table creation query.
            for field, dtype in user_fields.items():
                column = f"{field} {dtype}"
                if user_primary_key == field:
                    column += "PRIMARY KEY, "
                else: column += ", "
                creation_query += column
            creation_query = creation_query.strip(",") + ")"
            print(f"executed query: {creation_query}")
            # execute the table creation query.
            cursor.execute(creation_query)
            # save the changes.
            # connection.commit()
            # close connection to the database. 
            connection.close() 
            print(f"created TABLE {user_table}")
        except sqlite3.OperationalError:
            print(f"OperationalError: {user_table} table already exists")

    def create_user(self, user_model, 
                    password: str, **data):
        '''create user account.'''
        connection = sqlite3.connect(self.path)
        password = FigDashAppPassword(password)
        user_primary_key = self.table_keys["user"]
        user_field_value = data["user"]
        user = user_model(password=password.toObjectStr(), **data)
        print(f"CREATE USER({user_primary_key}={user_field_value}, password={password})")
        connection.close()

    def create_record(self):
        pass

    def login(self, password: str, **user_field):
        '''authenticate the user.'''
        user_table = self.table_names["user"]
        user_field_name = list(user_field.keys())[0]
        user_field_value = list(user_field.values())[0]
        user_find_query = f"SELECT * FROM {user_table} WHERE {user_field_name} = {user_field_value}"
        
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(user_find_query)
        results = cursor.fetchall()
        
        if len(results) == 0:
            print(f"USER({user_field_name}={user_field_value}) not found")
        else:
            pass
        print(f"LOGIN {user_field}")

# SELECT DISTINCT column_list
# FROM table_list
#   JOIN table ON join_condition
# WHERE row_filter
# ORDER BY column
# LIMIT count OFFSET offset
# GROUP BY column
# HAVING group_filter;