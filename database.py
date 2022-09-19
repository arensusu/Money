
import boto3
import datetime

from boto3.dynamodb.conditions import Key, Attr

from table_method import *

class Accounting:
    """Interactives with AWS DynamoDB.

    Attributes:
        __db: A resouce service of DynamoDB.
    
    """

    def __init__(self):
        """Connects to AWS DynamoDB."""
        self.__table = Table()

    def AddOutcome(self, user: str, date: str, term: str, price: int) -> str:
        dateStr = date.strftime("%Y/%m/%d %X")
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")

        attr = {
                "user" : user,
                "date" : dateStr,
                "year" : year,
                "month" : month,
                "day" : day,
                "term" : term,
                "price" : price
        }
        return self.__table.insert("money_outcome", attr)

    def PrintSummary(self, user, type, value):

        table = self.__db.Table("money_outcome")
        if type == "週結算":

            upper = int(value) * 7
            lower = upper - 6
            if int(value) == 4:
                upper = 31

            response = table.scan(
                FilterExpression = Attr("user").eq(user) & Attr("day").gte(str(lower).zfill(2)) & Attr("day").lte(str(upper).zfill(2))
            )

        elif type == "月結算":
            response = table.scan(
                FilterExpression = Attr("user").eq(user) & Attr("month").eq(value.zfill(2))
            )

        elif type == "年結算":
            response = table.scan(
                FilterExpression = Attr("user").eq(user) & Attr("year").eq(value.zfill(4))
            )
        query = response["Items"]

        if query:
            category = {}
            for payment in query:
                price = payment["price"]

                if "total" not in category:
                    category["total"] = 0
                category["total"] += price

                term = payment["term"]
                if term not in category:
                    category[term] = 0
                category[term] += price

            info = user + " "
            for k, v in category.items():
                if k == "total":
                    info += value + ' ' + type + "，總支出為 " + str(v) + " 元"
                else:
                    info += "\n" + k + " " + str(v) + " 元"

            return info

        else:
            return "沒有紀錄"

    def DeletePayment(self, tableName, partition, sort):
        table = self.__db.Table(tableName)
        keyList = table.key_schema
        table.delete_item(
            Key = { keyList[0]["AttributeName"] : partition, keyList[1]["AttributeName"] : sort}
        )

    def Summary(self, user, type):

        if type == "月結算":
            table = self.__db.Table("money_outcome")

            thisMonth = datetime.date.today().strftime("%m")
            response = table.scan(
                FilterExpression = Attr("user").eq(user) & Attr("month").ne(thisMonth)
            )
            query = response["Items"]

            if query :
                category = {}
                for payment in query:
                    term = payment["term"]
                    if term not in category:
                        category[term] = 0

                    category[term] += payment["price"]
                    self.DeletePayment(table.table_name, user, payment["date"])

                table = self.__db.Table("money_month")
                prevMonth = str(int(thisMonth) - 1).zfill(2)

                id = 0
                for k, v in category.items():
                    table.put_item(
                        Item = {
                            "period" : prevMonth,
                            "id" : id,
                            "term" : k,
                            "user" : user,
                            "price" : v
                        }
                    )
                    id += 1

            
        elif type == "年結算":
            table = self.__db.Table("money_month")

            thisYear = datetime.date.today().strftime("%Y")
            response = table.scan(
                FilterExpression = Attr("user").eq(user)
            )
            query = response["Items"]

            if query :
                category = {}
                for payment in query:
                    term = payment["term"]
                    if term not in category:
                        category[term] = 0

                    category[term] += payment["price"]
                    self.DeletePayment(table.table_name, payment["period"], term)

                table = self.__db.Table("money_year")
                prevYear = str(int(thisYear) - 1).zfill(2)

                id = 0
                for k, v in category.items():
                    table.put_item(
                        Item = {
                            "period" : prevYear,
                            "id" : id,
                            "term" : k,
                            "user" : user,
                            "price" : v
                        }
                    )

                    id += 1

        
        

