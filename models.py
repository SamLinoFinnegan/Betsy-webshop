from peewee import *
import os

betsy_db = SqliteDatabase(os.path.join(os.getcwd(), os.path.basename("my_database.db")))
betsy_db.connect()

class BaseModel(Model):
    
    class Meta:
        database = betsy_db

class Tag(BaseModel):
    name = CharField(unique=True)
    

class User(BaseModel):
    name = CharField(unique=True)
    address = CharField()
    billing = CharField()
    password = CharField()

class Product(BaseModel):
    name = CharField(index=True)
    description = TextField()
    price = DecimalField(auto_round=False, decimal_places=2)
    quant = IntegerField()
    tag = ManyToManyField(Tag, backref="product")
    user = ForeignKeyField(User)
    
class Transaction(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quant = IntegerField()


ProductTag = Product.tag.get_through_model()

