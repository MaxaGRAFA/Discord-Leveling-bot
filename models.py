from peewee import *

db = SqliteDatabase('database.db')

class BaseModel(Model):
    id = IntegerField()
    guild_id = IntegerField()

    class Meta():
        database = db
        primary_key=CompositeKey('id','guild_id')

class User(BaseModel):
    name = CharField()
    exp = IntegerField()
    level = IntegerField()
    

    class Meta:
        db_table = 'users'

class Channel(BaseModel):
    
    name = CharField()

    class Meta():
        db_table = 'channels'

