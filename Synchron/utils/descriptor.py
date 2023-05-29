class Descriptor:
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value


class Name(Descriptor):
    pass


class Email(Descriptor):
    pass


class ID(Descriptor):
    def __get__(self, instance, owner):
        if self.value is None:
            self.value = str(uuid1())

        return self.value


class Password(Descriptor):
    def __set__(self, instance, value):
        if value:
            value = value.encode("utf-8")
            hash = bcrypt.hashpw(value, bcrypt.gensalt())
            self.value = hash.decode("utf-8")
            instance._hashed_password = self.value
