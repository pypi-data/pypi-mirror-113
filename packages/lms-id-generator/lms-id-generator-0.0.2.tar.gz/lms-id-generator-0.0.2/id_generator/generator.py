import os

from peewee import Model, BigIntegerField, CharField, Proxy, DoesNotExist
from playhouse.db_url import connect

database = Proxy()


def init(db_url=None):
    global database
    database.initialize(init_db(db_url))
    database.create_tables([Ids])


def generate_id(target="default", increment=1, id_start=1):
    with database.atomic():
        try:
            id_ = Ids.select().where(Ids.target == target).get()
            query = Ids.update({Ids.next_id: Ids.next_id + increment}).where(
                Ids.id == id_.id, Ids.next_id == id_.next_id
            )
            if query.execute() > 0:
                return id_.next_id
            raise ConflictException("Conflict occurred, please try again later.")
        except DoesNotExist:
            id_ = Ids(target=target, id_start=id_start, next_id=id_start + increment)
            id_.save()
            return id_start


def init_db(db_url):
    db_url = db_url if db_url else os.environ.get("DATABASE")
    if not db_url:
        raise ValueError(f"No valid database url specified for id generator, {db_url}")
    return connect(db_url)


class ConflictException(Exception):
    pass


class Ids(Model):
    class Meta:
        database = database

    next_id = BigIntegerField()
    target = CharField(unique=True)
    id_start = BigIntegerField(default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = kwargs.get("target", "default")
        self.id_start = kwargs.get("id_start", 1)
        self.next_id = kwargs.get("next_id", self.id_start)
