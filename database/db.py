# This module contains models of your DB
import datetime

from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase
from config import Config


__sp = r"-\|/-\|/"  # this thingie used as spinner

# You can choose other types of DB, supported by peewee
db_handle = SqliteQueueDatabase(Config.DB_FILENAME,
                                use_gevent=False,
                                autostart=True,
                                queue_max_size=128,
                                )


def stop_db() -> bool:
    try:
        db_handle.commit()
        db_handle.stop()
        x = 0
        while not db_handle.is_stopped():
            print("Closing database...", __sp[x % 8], end="\r")
            x += 1
            continue
        print("Closing database... ok")
    except InternalError as e:
        print(e)
        return False
    return True


class BaseModel(Model):
    class Meta:
        database = db_handle


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    tg_user_id = IntegerField(null=False)
    tg_first_name = CharField(null=False)
    tg_last_name = CharField(null=False)
    tg_username = CharField(null=False)

    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "users"
        order_by = ("created_at",)


MODELS = [User]  # Add your user models, to simplify generation of tables
