import bcrypt
from utils import cursor
from utils.descriptor import Name, Email, Password, ID


class User:
    __table_name__ = "users"
    __fields_str__ = "id,fname,lname,email,password,role"
    __fields__ = tuple(__fields_str__.split(","))
    fname: str = Name()
    lname: str = Name()
    email: str = Email()
    password: str = Password()
    role: str
    id: str = ID()

    def __init__(
        self,
        fname: str,
        lname: str,
        email: str,
        role: str,
        id: str = None,
        password: str = None,
    ) -> None:
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.role = role

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            (self._hashed_password).encode("utf-8"),
        )

    def insert(self):
        query = f"""
            INSERT INTO {self.__table_name__}({self.__fields_str__})
            VALUES('{self.id}','{self.fname}','{self.lname}','{self.email}','{self.password}','{self.role}')
        """
        cursor.execute(query)

    def update_password(self, password):
        self.password = password
        query = f"""
                    UPDATE {self.__table_name__}
                    SET password='{self.password}'
                    WHERE id='{self.id}'
                """
        cursor.execute(query)

    def delete(self):
        query = f"""
            DELETE FROM {self.__table_name__} 
            WHERE id={self.id}
        """
        cursor.execute(query)

    @classmethod
    def get_by_id(cls, id):
        query = f"""SELECT {cls.__fields_str__} 
                    FROM {cls.__table_name__} 
                    WHERE id='{id}'
                """
        cursor.execute(query)
        return cls.__get_user()

    @classmethod
    def get_by_email(cls, email):
        query = f"""SELECT {cls.__fields_str__}
                    FROM {cls.__table_name__} 
                    WHERE email='{email}'
                """

        cursor.execute(query)
        return cls.__get_user()

    @classmethod
    def __get_user(cls):
        res = cursor.fetchone()
        if res:
            res = {key: value for key, value in zip(cls.__fields__, res)}
            password = res.pop("password")
            user = User(**res)
            user._hashed_password = password
            return user
        else:
            return None
