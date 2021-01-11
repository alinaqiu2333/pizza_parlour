from flask import Flask, Response, request, jsonify
from functions import create_obj
from Objects import *

# rename
app = Flask("assignment-2-24-alinaqiu2333-skrpaowang")
# saves the pizza and orders by dict, key is their id number, value is the corresponding class.
all_pizza = {}
all_order = {}
# init the id number
curr_pizza_id = 1000
curr_order_id = 6000


# welcome
@app.route('/full_menu', methods=['GET'])
def welcome_pizza():
    """
    curl http://127.0.0.1:5000/full_menu
    :return:
    """
    menu_str = "Welcome to Pizza Planet! ^ ^\n\n"
    pizzas = "Here are the prices of pizzas:\n"
    for i in pizza_size_to_price:
        pizzas += i + " size pizza $" + str(pizza_size_to_price[i]) + "\n"
    pizzas += "\nHere are the types of pizzas: \n"
    for i in pizza_type_to_toppings:
        pizzas += i + " type pizza includes toppings: " + str(pizza_type_to_toppings[i]) + "\n"
    drinks = "\nHere are the prices of drinks: \n"
    for i in drink_name_to_price:
        drinks += i + " $" + str(drink_name_to_price[i]) + "\n"
    toppings = "\nHere are the prices of toppings: \n"
    for i in topping_type_to_price:
        toppings += i + " $" + str(topping_type_to_price[i]) + "\n"
    menu_str += pizzas + drinks + toppings
    return menu_str


@app.route('/get_item_prices', methods=["GET"])
def get_item_prices():
    """
    # successful ones
    curl -X GET -H "Content-Type: application/json" \
   -d '{"item_type":"pizza", "size": "6inch", "type": "pepperoni"}' \
      http://127.0.0.1:5000/get_item_prices
   curl -X GET -H "Content-Type: application/json" \
   -d '{"item_type":"topping", "name": "pepperoni"}' \
      http://127.0.0.1:5000/get_item_prices
   curl -X GET -H "Content-Type: application/json" \
   -d '{"item_type":"drink", "name": "Coke"}' \
      http://127.0.0.1:5000/get_item_prices
   # error messages:
   curl -X GET -H "Content-Type: application/json" \
   -d '{"item_type":"pizza", "name": "Coke"}' \
      http://127.0.0.1:5000/get_item_prices
    """
    item = request.get_json()
    if item is None:
        return Response("Item not received\n", status=405)
    if "item_type" not in item or item["item_type"] not in ["pizza", "drink", "topping"] \
            or len(item) == 1 or len(item) > 3:
        return Response("Invalid .json file\n", status=400)
    # valid json with item_type attribute which is either pizza, drink, or toppings
    if item["item_type"] == "pizza":
        if "size" not in item or item["size"] not in pizza_size_to_price:
            return Response("Pizza info missing to get price\n",status=400)
        if "type" not in item or item["type"] not in pizza_type_to_description:
            return Response(str(pizza_size_to_price[item["size"]]), status=200)
        # .json file contains a valid pizza where it includes type and size
        pizza = create_obj("pizza")
        pizza.set_pizza_type_description(item["type"])
        pizza.set_pizza_size(item["size"])
        topping = create_obj("topping")
        topping.set_toppings(pizza_type_to_toppings[item["type"]])
        pizza.set_pizza_toppings(topping)
        pizza.set_pizza_price()
        total = pizza.get_price()
        return Response(str(total), status=200)
    elif item["item_type"] == "drink":
        total = drink_name_to_price[item["name"]]
        return Response(str(total), status=200)
    elif item["item_type"] == "topping":
        total = topping_type_to_price[item["name"]]
        return Response(str(total), status=200)


@app.route('/change_item_prices', methods=["POST"])
def change_item_prices():
    """
    curl -X POST -H "Content-Type: application/json" \
   -d '{"pizza_size": "6inch", "price": 9.99 }' \
      http://127.0.0.1:5000/change_item_prices
   curl -X POST -H "Content-Type: application/json" \
   -d '{"drink_name": "Coke", "price": 3 }' \
      http://127.0.0.1:5000/change_item_prices
   curl -X POST -H "Content-Type: application/json" \
   -d '{"topping_name": "olive", "price": 0.5 }' \
      http://127.0.0.1:5000/change_item_prices """
    item = request.get_json()
    if item is None:
        return Response("Item not received\n", status=405)
    elif "price" not in item or len(item) != 2:
        return Response("Invalid .json file\n", status=400)
    elif "pizza_size" in item and item["pizza_size"] in pizza_size_to_price:
        pizza_size_to_price[item["pizza_size"]] = item["price"]
        return Response("Pizza price is successfully changed\n",status=200)
    elif "drink_name" in item:
        drink_name_to_price[item["drink_name"]] = item["price"]
        return Response("Drink price is successfully changed\n",status=200)
    elif "topping_name" in item:
        topping_type_to_price[item["topping_name"]] = item["price"]
        return Response("Topping price is successfully changed\n",status=200)
    else:
        return Response("Can't access the item you are trying to change price\n", status=400)


@app.route('/order_total', methods=['GET'])
def order_total():
    """
    curl -X GET -H "Content-Type: application/json" \
   -d '{"order_id": 6000}' \
    http://127.0.0.1:5000/order_total
    """
    find_ord = request.get_json()
    if find_ord is None:
        return Response("order not received\n", status=405)
    elif "order_id" not in find_ord or find_ord["order_id"] not in all_order:
        return Response("order not found\n", status=400)
    else:
        total = all_order[find_ord["order_id"]].get_total_price()
        return Response(str(total))


@app.route('/new_order', methods=['GET'])
def new_order():
    """
    curl http://127.0.0.1:5000/new_order
    """
    # create a new order class based on the curr order id
    global curr_order_id
    order = create_obj('order')
    # add this order into dict, where key is its order_id
    all_order[curr_order_id] = order
    order.set_order_id(curr_order_id)
    curr_order_id += 1
    return Response(str(order.id))


# add a new pizza
@app.route('/new_pizza', methods=['POST'])
def new_pizza():
    # we add any pizza into an existing order, therefore we need the order number
    """
    pizza successfully created:
    curl -X POST -H "Content-Type: application/json" \
      -d '{"order_id":6000, "type": "pepperoni", "size": "6inch"}' \
      http://127.0.0.1:5000/new_pizza

    .json missing type factor:
    curl -X POST -H "Content-Type: application/json" \
      -d '{"order_id":6000, "size": "6inch"}' \
      http://127.0.0.1:5000/new_pizza

    .json with wrong pizza size
    curl -X POST -H "Content-Type: application/json" \
      -d '{"order_id":6000, "type": "pepperoni", "size": "7inch"}' \
      http://127.0.0.1:5000/new_pizza
    """
    # check if such order exists:
    find_ord = request.get_json()
    if find_ord is None:
        return Response("Order not received\n", status=400)
    if len(find_ord) != 3:
        return Response(".json file invalid\n", status=400)
    if find_ord["order_id"] not in all_order:
        return Response("Order does not exist\n", status=400)
    if find_ord["type"] not in pizza_type_to_description:
        return Response("Type not found\n", status=400)
    if find_ord["size"] not in pizza_size_to_price:
        return Response("Size invalid\n", status=400)
    # then we have a .json strictly follows the input format; ready to create pizza
    temp_order_id = find_ord["order_id"]
    global curr_pizza_id
    pizza = create_obj("pizza")
    # add this pizza into pizza dict, where the key is its id, and value is the object
    all_pizza[curr_pizza_id] = pizza
    # pizza need its id, type, toppings, size, and price.
    pizza.set_pizza_id(curr_pizza_id)
    pizza.set_pizza_type_description(find_ord["type"])
    pizza.set_pizza_size(find_ord["size"])
    topping = create_obj("topping")
    topping.set_toppings(pizza_type_to_toppings[find_ord["type"]])
    pizza.set_pizza_toppings(topping)
    pizza.set_pizza_price()
    # now add this pizza to current order
    all_order[temp_order_id].add_pizza(pizza)
    # add it to all_pizza to keep track of this certain pizza
    all_pizza[curr_pizza_id] = pizza
    curr_pizza_id += 1
    return Response(str(pizza.id), status=200)


@app.route('/add_drink', methods=['POST'])
def new_drink():
    """
    curl -X POST -H "Content-Type: application/json" \
      -d '{"order_id":6000, "name": "Coke"}' \
      http://127.0.0.1:5000/add_drink
    """
    find_drink = request.get_json()
    if find_drink is None:
        return Response("Drink not received\n", status=400)
    if len(find_drink) != 2:
        return Response(".json file invalid\n", status=400)
    if find_drink["order_id"] not in all_order:
        return Response("Order does not exist\n", status=400)
    if find_drink["name"] not in drink_name_to_price:
        return Response("Drink name invalid\n", status=400)
    drink = create_obj("drink")
    drink.set_name_price(find_drink["name"])
    temp_order_id = find_drink["order_id"]
    all_order[temp_order_id].add_drink(drink)
    return Response("Drink successfully added to order\n", status=200)


@app.route('/remove_drink', methods=['POST', 'DELETE'])
def remove_drink():
    """
    curl -X DELETE -H "Content-Type: application/json" \
      -d '{"order_id": 6000, "name": "Coke"}' \
      http://127.0.0.1:5000/remove_drink
    """
    if request.json is None:
        return Response("Drink not received\n", status=405)
    elif "order_id" not in request.json or request.json["order_id"] is None:
        return Response("Order ID is invalid\n", status=400)
    elif len(request.json) != 2:
        return Response(".json file invalid\n", status=400)
    order_id = int(request.json["order_id"])
    name = request.json["name"]
    if order_id not in all_order:
        return Response("Order ID is incorrect\n", status=400)
    elif name not in drink_name_to_price:
        return Response("Drink not found in order\n", status=400)
    all_order[order_id].delete_drink(name)
    return Response("Your drink is deleted\n", status=200)


@app.route('/remove_pizza', methods=['POST', 'DELETE'])
def remove_pizza():
    """
    curl -X DELETE -H "Content-Type: application/json" \
      -d '{"pizza_id": 1000}' \
      http://127.0.0.1:5000/remove_pizza
    """
    if request.json is None:
        return Response("Pizza not received\n", status=405)
    elif "pizza_id" not in request.json or request.json["pizza_id"] is None:
        return Response("Pizza ID is invalid\n", status=400)
    pizza_id = int(request.json["pizza_id"])
    if pizza_id not in all_pizza:
        return Response("Pizza ID is incorrect\n", status=400)
    else:
        # delete pizza in corresponding order
        for order in all_order.values():
            if all_pizza[pizza_id] in order.pizzas:
                order.delete_pizza(pizza_id)
        # remove pizza in dict
        all_pizza.pop(pizza_id)
        return Response("Your Pizza is deleted\n", status=200)


@app.route('/add_toppings', methods=['POST'])
def new_topping():
    """
    curl -X POST -H "Content-Type: application/json" \
      -d '{"pizza_id":1000, "extra_toppings": ["pepperoni", "mushrooms"]}' \
      http://127.0.0.1:5000/add_toppings
    :return:
    """
    find_topping = request.get_json()
    if find_topping is None:
        return Response("topping not received\n", status=400)
    if len(find_topping) != 2:
        return Response(".json file invalid\n", status=400)
    if find_topping["pizza_id"] not in all_pizza:
        return Response("Pizza does not exist\n", status=400)
    for topping in find_topping["extra_toppings"]:
        if topping not in topping_type_to_price:
            return Response("Topping name invalid\n", status=400)
    temp_pizza_id = find_topping["pizza_id"]
    all_pizza[temp_pizza_id].toppings.add_toppings(find_topping["extra_toppings"])
    return Response("Toppings successfully added to pizza with respond to ID\n", status=200)


@app.route('/remove_toppings', methods=['POST', 'DELETE'])
def remove_toppings():
    """
    curl -X DELETE -H "Content-Type: application/json" \
      -d '{"pizza_id": 1000, "removed_toppings": "pepperoni"}'\
    http://127.0.0.1:5000/remove_toppings
    """
    find_topping = request.get_json()
    if find_topping is None:
        return Response("Topping not received\n", status=405)
    if len(find_topping) != 2:
        return Response(".json file invalid\n", status=400)
    if find_topping["pizza_id"] not in all_pizza:
        return Response("Pizza does not exist\n", status=400)
    pizza_id = find_topping["pizza_id"]
    to_be_removed = find_topping["removed_toppings"]
    if to_be_removed not in topping_type_to_price:
        return Response("Topping name invalid\n", status=400)
    if to_be_removed not in all_pizza[pizza_id].toppings.get_toppings():
        return Response("Topping does not exit in pizza\n", status=400)
    all_pizza[pizza_id].toppings.delete_topping(to_be_removed)
    # for topping in find_topping["removed_toppings"]:
    #     all_pizza[pizza_id].toppings.delete_toppings(topping)
    return Response("Topping successfully deleted\n", status=200)


@app.route('/create_new_toppings', methods=['POST'])
def create_new_toppings():
    """
    curl -X POST -H "Content-Type: application/json" \
      -d '{"topping_type": "ham", "price": 2}' \
    http://127.0.0.1:5000/create_new_toppings
    """
    new_topping_type = request.get_json()
    if new_topping_type is None:
        return Response("Topping type no received\n", status=400)
    if len(new_topping_type) != 2 or "topping_type" not in new_topping_type or "price" not in new_topping_type:
        return Response(".json file invalid\n", status=400)
    topping_dict = {new_topping_type["topping_type"]: new_topping_type["price"]}
    with open("topping_type_to_price.json", "r+") as file:
        data = json.load(file)
        data.update(topping_dict)
        file.seek(0)
        json.dump(data, file)
    return Response("New topping added into topping_type_to_price.json\n", status=200)


@app.route('/create_new_pizza_type', methods=['POST'])
def create_new_pizza_types():
    """
    curl -X POST -H "Content-Type: application/json" \
      -d '{"pizza_type": "Hawaiian", "description": "Pineapple might not be the first thing that comes to mind when you think pizza. But add in some ham and it creates an unexpectedly solid sweet and salty combination for this type of pizza.",
      "toppings" : ["ham", "pineapple"]}' \
    http://127.0.0.1:5000/create_new_pizza_type

    Pineapple might not be the first thing that comes to mind when you think pizza. \
                            But add in some ham and it creates an unexpectedly solid sweet and salty combination for this type of pizza.
    """
    new_pizza_type = request.get_json()
    if new_pizza_type is None:
        return Response("Pizza type no received\n", status=400)
    if len(new_pizza_type) != 3 or "pizza_type" not in new_pizza_type or "description" not in new_pizza_type \
            or "toppings" not in new_pizza_type:
        return Response(".json file invalid\n", status=400)
    pizza_type_to_toppings_dict = {new_pizza_type["pizza_type"]: new_pizza_type["toppings"]}
    pizza_type_to_description_dict = {new_pizza_type["pizza_type"]: new_pizza_type["description"]}
    with open("pizza_type_to_toppings.json", "r+") as file1:
        data = json.load(file1)
        data.update(pizza_type_to_toppings_dict)
        file1.seek(0)
        json.dump(data, file1)
    with open("pizza_type_to_description.json", "r+") as file2:
        data = json.load(file2)
        data.update(pizza_type_to_description_dict)
        file2.seek(0)
        json.dump(data, file2)
    return Response("New pizza type created\n", status=200)


# add delivery details
@app.route('/delivery', methods = ['POST'])
def add_delivery():
    """
    curl -X POST -H "Content-Type: application/json" \
    -d '{"order_id": 6000, "delivery_method": "Ubereats", "address": "15 grenville st", "postal_code": "M4Y0B9"}'\
    http://127.0.0.1:5000/delivery
    """
    delivery_info = request.get_json()
    if delivery_info is None:
        return Response("Delivery information not received\n", status=400)
    if len(delivery_info) != 4:
        return Response(".json file invalid\n", status=400)
    if "order_id" not in delivery_info or delivery_info["order_id"] not in all_order:
        return Response("Order does not exist\n", status=400)
    order_id = delivery_info["order_id"]
    if delivery_info["delivery_method"] not in ["Ubereats", "Foodora", " In-house delivery"]:
        return Response("Please choose a valid delivery method\n", status=400)
    # save info in .csv and .json
    order = all_order[delivery_info["order_id"]]
    order.set_address_postal_code(delivery_info["address"], delivery_info["postal_code"])
    order.set_delivery_method(delivery_info["delivery_method"])
    if order.get_status() == "UNPAID":
        return Response("You have not paid for this order, please checkout first\n", status=400)
    else:
        if delivery_info["delivery_method"] == "Ubereats":
            all_order[order_id].delivery_info_in_json()
        elif delivery_info["delivery_method"] == "Foodora":
            all_order[order_id].delivery_info_in_csv()
        return Response("order will send to your address soon\n", status=200)


# cancel a new order
@app.route('/cancel_order', methods=['DELETE'])
def cancel_order():
    """
    curl -X DELETE -H "Content-Type: application/json" \
      -d '{"order_id":6000}' \
      http://127.0.0.1:5000/cancel_order
    """
    if request.json is None or request.json["order_id"] is None:
        return Response("Order ID is invalid\n", status=500)
    order_id = int(request.json["order_id"])
    if order_id not in all_order:
        return Response("Order does not exist\n", status=405)
    all_order.pop(order_id)
    return Response("Your order is canceled\n", status=200)


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    curl -X POST -H "Content-Type: application/json" \
      -d '{"order_id":6000}' \
      http://127.0.0.1:5000/checkout
    """
    summary = request.json
    if summary is None or "order_id" not in summary or summary["order_id"] is None:
        return Response("Order_id not received\n", status=405)
    order_id = int(summary["order_id"])
    if len(summary) != 1:
        return Response(".json file invalid\n", status=400)
    elif order_id not in all_order:
        return Response("Order does not exist\n", status=400)
    elif all_order[order_id].get_status() == "PAID":
        return Response("You already paid for this order!\n", status=400)
    else:
        all_order[order_id].change_status("PAID")
        return Response("Your order is checked out and ready for delivery\n", status=200)


if __name__ == "__main__":
    app.run(debug=True)
