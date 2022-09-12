from unicodedata import category
from urllib import response
import boto3
import datetime

from boto3.dynamodb.conditions import Key, Attr

class Accounting:

    def __init__(self):
        self.db = boto3.resource("dynamodb")

    def AddOutcome(self, user, date, term, price):
        dateStr = date.strftime("%Y/%m/%d %X")
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")

        table = self.db.Table("money_outcome")
        table.put_item(
            Item = {
                "user" : user,
                "date" : dateStr,
                "year" : year,
                "month" : month,
                "day" : day,
                "term" : term,
                "price" : price
            }
        )
        return "已存入"

    def PrintSummary(self, user, type, value):

        attribute = ""
        if type == "週結算":
            table = self.db.Table("money_week")
            attribute = "week"

        elif type == "月結算":
            table = self.db.Table("money_month")
            attribute = "month"

        elif type == "年結算":
            table = self.db.Table("money_year")
            attribute = "year"

        response = table.scan(
            FilterExpression = Attr("user").eq(user) & Attr("period").eq(value)
        )
        query = response["Items"]

        if query:
            outcome = 0
            for payment in query:
                outcome += payment["price"]
        
        else:

            table = self.db.Table("money_outcome")

            if attribute != "week":
                response = table.scan(
                    FilterExpression = Attr("user").eq(user) & Attr(attribute).eq(value)
                )

            else:
                upper = int(value) * 7
                lower = upper - 6
                if int(value) == 4:
                    upper = 31

                response = table.scan(
                    FilterExpression = Attr("user").eq(user) & Attr("day").gte(str(lower).zfill(2)) & Attr("day").lte(str(upper).zfill(2))
                )
            
            query = response["Items"]
            category = {}
            outcome = 0
            for payment in query:
                price = payment["price"]

                if "total" not in category:
                    category["total"] = 0
                category["total"] += price

                term = payment["term"]
                if term not in category:
                    category[term] = 0
                category[term] += price

        info = ""
        for k, v in category.items():
            if k == "total":
                info += value + ' ' + type + "，總支出為 " + str(v) + " 元"
            else:
                info += "\n" + k + "支出為 " + str(v) + " 元"

        return info

    def DeletePayment(self, tableName, partition, sort):
        table = self.db.Table(tableName)
        keyList = table.key_schema
        table.delete_item(
            Key = { keyList[0]["AttributeName"] : partition, keyList[1]["AttributeName"] : sort}
        )

    def Summary(self, user, type):

        if type == "週結算":
            table = self.db.Table("money_outcome")
            period = datetime.date.today().day // 7
            upper =  period * 7
            lower = upper - 6
            if period == 4:
                upper = 31

            response = table.scan(
                FilterExpression = Attr("user").eq(user) & Attr("day").gte(str(lower).zfill(2)) & Attr("day").lte(str(upper).zfill(2))
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

                table = self.db.Table("money_week")
                for k, v in category.items():
                    table.put_item(
                        Item = {
                            "user" : user,
                            "period" : str(period),
                            "term" : k,
                            "price" : v
                        }
                    )

        else:
            if type == "月結算":
                tableName = "money_week"
                period = 4
                
            elif type == "年結算":
                tableName = "money_month"
                period = 12

            table = self.db.Table(tableName)

            response = table.scan(
                FilterExpression = Attr("user").eq(user) & Attr("period").eq(str(period))
            )
            query = response["Items"]

            if query :
                category = {}
                for payment in query:
                    term = payment["term"]
                    if term not in category:
                        category[term] = 0

                    category[term] += payment["price"]
                    self.DeletePayment(table.table_name, user, payment["period"])

                table = None
                if type == "月結算":
                    table = self.db.Table("money_month")
                    value = str(datetime.date.today().month - 1)

                elif type == "年結算":
                    table = self.db.Table("money_year")
                    value = str(datetime.date.today().year - 1)

                for k, v in category.items():
                    table.put_item(
                        Item = {
                            "user" : user,
                            "period" : value,
                            "term" : k,
                            "price" : v
                        }
                    )
        

