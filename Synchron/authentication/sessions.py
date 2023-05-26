import datetime
from utils import cursor
from uuid import uuid1
from django.http import JsonResponse


class Session:
    __table_name__ = "sessions"
    __fields_str__ = "user_id,cookie,valid_till"
    __fields__ = tuple(__fields_str__.split(","))
    user_id: str
    cookie: str
    valid_till: str

    def __init__(self, id):
        self.user_id = id
        self.valid_till = datetime.datetime.now() + datetime.timedelta(hours=24)
        self.valid_till = self.valid_till.strftime("%Y-%m-%d %H:%M:%S")
        self.cookie = str(uuid1())
        query = f"""
            INSERT INTO {self.__table_name__}({self.__fields_str__})
            VALUES('{self.user_id}','{self.cookie}','{self.valid_till}')
        """
        cursor.execute(query)

    @classmethod
    def validate(cls, user_id, cookie):
        query = f"""SELECT {cls.__fields_str__}
                    FROM {cls.__table_name__} 
                    WHERE user_id='{user_id}' AND cookie='{cookie}'
                """
        cursor.execute(query)
        res = cursor.fetchall()[0]
        if res[-1] > datetime.datetime.now():
            return True
        else:
            return False

    def set_cookie_response(self):
        response = JsonResponse({"msg": "Login Successful"}, status=200)
        age = datetime.datetime.strptime(
            self.valid_till, "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        response.set_cookie("user_id", value=self.user_id, max_age=age)
        response.set_cookie("session", value=self.cookie, max_age=age)
        return response

    @classmethod
    def delete_cookie_response(cls, user_id, session):
        query = f"""DELETE FROM {cls.__table_name__} 
                    WHERE user_id='{user_id}' AND cookie='{session}'
                """
        try:
            cursor.execute(query)
        except:
            pass

        response = JsonResponse({"msg": "Clearing Cookies"}, status=200)
        response.delete_cookie("user_id")
        response.delete_cookie("session")
        return response