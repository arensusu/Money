import boto3

from boto3.dynamodb.conditions import Attr

TABLE_ATTRIBUTE = {
    "money_outcome": ["user", "date", "year", "month", "day", "term", "price"]
}

class DBMethod:

    def __init__(self):
        self.__db = boto3.resource("dynamodb")

    def __del__(self):
        self.__db.meta.client.close()

    @property
    def db(self):
        return self.__db

    def check_table_existed(self, table_name: str) -> bool:
        table_list = self.__db.meta.client.list_tables()["TableNames"]

        if table_name in table_list:
            return True
        else:
            return False

    def key_schema(self, table_name: str):
        return [key["AttributeName"] for key in self.__db.Table(table_name).key_schema]

    def insert(self, table_name: str, attr: dict):
        try:
            self.__db.Table(table_name).put_item(Item = attr)
        except Exception as error:
            return error
        else:
            return None

    def update(self, table_name: str, attr: dict) -> str:
        pass

    def query(self, table_name: str, attr: dict):
        expression = Attr("user").eq(attr.pop("user"))
        while len(attr) != 0:
            k, v = attr.popitem()
            expression = expression & Attr(k).eq(v)

        try:
            self.__db.Table(table_name).scan(FilterExpression = expression)
        except Exception as error:
            return error
        else:
            return None
        

    def delete(self, table_name: str, keys: dict) -> str:
        try:
            self.__db.Table(table_name).delete_item(Key = keys)
        except Exception as error:
            return error
        else:
            return None

class Table:

    def __init__(self):
        self.__db_method = DBMethod()    

    def insert(self, table_name: str, attr: dict) -> str:

        if not self.__db_method.check_table_existed(table_name):
            return "Error: Table not found"

        for attribute in TABLE_ATTRIBUTE[table_name]:
            if attribute not in attr:
                print(f"Attribute {attribute} is lost")
                return "Error: Lost"

        if len(attr) > len(TABLE_ATTRIBUTE[table_name]):
            print("Dummy attribute")
            return "Error: Dummy"
        
        error = self.__db_method.insert(table_name, attr)
        if error:
            print(error)
            return "Error: Insertion failed"
        else:
            return f"已存入({attr['user']})"

    def update(self, table_name: str, attr: dict) -> str:
        pass

    def query(self, table_name: str, attr: dict) -> str:
        if not self.__db_method.check_table_existed(table_name):
            return "Error: Table not found"

        for attribute, _ in attr.items():
            if attribute not in TABLE_ATTRIBUTE[table_name]:
                print(f"Dummy Attribute")
                return "Error: Dummy"
        
        error = self.__db_method.query(table_name, attr)
        if error:
            print(error)
            return "Error: Query failed"
        else:
            return "Query completed"

    def delete(self, table_name: str, attr: dict) -> str:
        
        if not self.__db_method.check_table_existed(table_name):
            return "Error: Table not found"
        else:
            keyList = self.__db_method.key_schema(table_name)

        for key in keyList:
            if key not in attr:
                return "Error: Lost"

        if len(attr) > len(keyList):
            return "Error: Dummy"

        error = self.__db_method.delete(table_name, attr)
        if error:
            print(error)
            return "Error: Delete failed"
        else:
            return "Delete completed"