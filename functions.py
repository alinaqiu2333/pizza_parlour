from Objects import Pizza,Drink,Order,Topping


def create_obj(object_type: str):
    if object_type == "pizza":
        return Pizza()
    elif object_type == "drink":
        return Drink()
    elif object_type == "order":
        return Order()
    elif object_type == "topping":
        return Topping()



