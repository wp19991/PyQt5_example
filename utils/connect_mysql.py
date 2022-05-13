from peewee import _ConnectionState, Model, DateTimeField, IntegerField
from contextvars import ContextVar
from playhouse.pool import PooledMySQLDatabase

from config.config import settings

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = PooledMySQLDatabase(
    settings.MYSQL_DATABASE,
    max_connections=8,
    stale_timeout=300,
    user=settings.MYSQL_USERNAME,
    host=settings.MYSQL_HOST,
    password=settings.MYSQL_PASSWORD,
    port=settings.MYSQL_PORT
)

db._state = PeeweeConnectionState()


class BaseModel(Model):
    id = IntegerField()
    gmt_created = DateTimeField()
    gmt_modified = DateTimeField()

    class Meta:
        database = db
