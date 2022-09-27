import os

def populate_test_database():
    from models import User ,Product, Transaction, Tag,  ProductTag,  betsy_db

    betsy_db.create_tables([User, Product, Transaction, Tag, ProductTag])

    clothes = Tag.create(name="clothes")
    shoes = Tag.create(name="shoes")
    shirts = Tag.create(name="shirts")
    pants = Tag.create(name="pants")
    accessories = Tag.create(name="accessories")
    furniture = Tag.create(name="furniture")


    john = User.create(name="john", address="Yellow brick road 123", billing="cc4344-3432-1123-000",password="xxxxxxxxxxxx")
    mark = User.create(name="mark", address="Brown brick road 123", billing="cc4344-3432-1123-000",password="xxxxxxxxxxxx")
    tom = User.create(name="tom", address="White brick road 123", billing="cc4344-3432-1123-000",password="xxxxxxxxxxxx")
    bob = User.create(name="bob", address="Blue brick road 123", billing="cc4344-3432-1123-000",password="xxxxxxxxxxxx")
    fred = User.create(name="fred", address="Orange brick road 123", billing="cc4344-3432-1123-000",password="xxxxxxxxxxxx")



    shirt = Product.create(name="white shirt", description="Its a nice WHITE shirt", price=10.53, quant=3,user=john)
    jeans = Product.create(name="large jeans", description="Its a nice shirt", price=10.50, quant=3,user=mark)
    jacket = Product.create(name="leather jacket", description="Its a nice shirt", price=10.50, quant=3,user=tom)
    shorts = Product.create(name="shorts", description="Its a nice shirt", price=10.52, quant=3,user=bob)
    shirt_b = Product.create(name="old blue shirt", description="Its a crapy BLUE shirt", price=3.54, quant=3,user=john)
    shoes_o = Product.create(name="old shoes", description="These shoes belonged to my grandfather", price=23.54, quant=3,user=fred)
    flip = Product.create(name="flip-Flops", description="Havaianas", price=3.54340, quant=3,user=fred)
    tv = Product.create(name="television", description="Its a big TV", price=66.00 , quant=1, user=bob)



    shirt.tag.add([shirts, clothes])
    jeans.tag.add([pants, clothes])
    jacket.tag.add(clothes)
    shorts.tag.add(clothes)
    shirt_b.tag.add([shirts, clothes])
    shoes_o.tag.add(shoes)
    flip.tag.add(shoes)
    tv.tag.add(accessories)


if not os.path.isfile(os.path.join(os.getcwd(), os.path.basename("my_database.db"))):
    populate_test_database()
 