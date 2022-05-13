import datetime
import hashlib

from peewee import CharField, IntegerField, BooleanField, DateTimeField

from utils.connect_mysql import BaseModel


class User(BaseModel):
    """
    用户信息表
    """
    user_name = CharField()
    is_valid = BooleanField()
    phone_number = CharField()
    email_address = CharField()
    encoded_password = CharField()
    type = IntegerField()
    brief = CharField()

    class Meta:
        table_name = 't_user'

    @classmethod
    def user_create(cls, user_name: str, password: str):
        md5_password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        user = User.create(user_name=user_name, encoded_password=md5_password)
        user.encoded_password = None
        return user

    @classmethod
    def user_delete(cls, user_id: int):
        res = User.delete().where(User.id == user_id).execute()
        if res == 0:
            return False
        else:
            return True

    @classmethod
    def user_update(cls, user_id: int,
                    name: str, phone: str, email: str, password: str):
        try:
            u = User.get(User.id == user_id)
            if u is None:
                return False
            if name != "":
                u.user_name = name
            if phone != "":
                u.phone_number = phone
            if email != "":
                u.email_address = email
            if password != "":
                encoded_password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
                u.encoded_password = encoded_password
            # print(str(datetime.datetime.now()))
            u.gmt_modified = datetime.datetime.now()
            res = u.save()
            if res == 0:
                # 和之前一样，修改失败
                return False
            else:
                return True
        except:
            # 有重复的名称
            return False

    @classmethod
    def get_user_datas(cls):
        datas = User.select().where(1 == 1)
        return datas

    @classmethod
    def select_from_user_name_and_password(cls, user_name: str, password: str):
        try:
            md5_password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
            info = User.select().where(User.user_name == user_name)[0]
            if info.encoded_password == md5_password:
                return info
            else:
                return None
        except:
            return None

    @classmethod
    def select_from_user_id(cls, user_id: int):
        info = User.get(User.id == user_id)
        return info
