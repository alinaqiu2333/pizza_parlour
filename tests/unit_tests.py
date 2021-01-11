import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PizzaParlour import app
from main import *
import mock


def test_get_menu():
    """
    test full_menu route
    """
    response = app.test_client().get('/full_menu')
    assert response.status_code == 200
    menu = "Welcome to Pizza Planet! ^ ^\n\nHere are the prices of pizzas:\n6inch size pizza $7.99\n9inch size pizza $10.99\n12inch size pizza $15.99\n"
    menu += "\nHere are the types of pizzas: \npepperoni type pizza includes toppings: ['olives', 'tomatoes', 'pepperoni']\nmargherita type pizza includes toppings: ['mushrooms', 'jalapenoes']\n"
    menu += "vegetarian type pizza includes toppings: ['olives', 'tomatoes', 'mushrooms']\nneapolitan type pizza includes toppings: ['chicken', 'beef', 'pepperoni']\nHawaiian type pizza includes toppings: ['ham', 'pineapple']\n"
    menu += "\nHere are the prices of drinks: \nCoke $2.99\nDiet Coke $2.99\nCoke Zero $2.99\nPepsi $0.99\nDiet Pepsi $0.99\nDr Pepper $2.99\nWater $1.99\nJuice $3.99\n"
    menu += "\nHere are the prices of toppings: \nolives $2\ntomatoes $2\nmushrooms $2\njalapenos $2\nchicken $3\nbeef $3\npepperoni $3\nham $2\npineapple $2\n"
    assert response.data.decode('UTF-8') == menu


def test_get_item_prices():
    """
    test get_item_prices route
    """
    # data is None
    data = None
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 405
    assert response.data == b'Item not received\n'
    # 4 keys in data
    data = {"item_type": "pizza", "size": "6inch", "type": "pepperoni", "wrong": "any str"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 400
    assert response.data == b'Invalid .json file\n'
    # no item_type
    data = {"size": "6inch", "type": "pepperoni"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 400
    assert response.data == b'Invalid .json file\n'
    # item_type is not pizza, drink or toppings
    data = {"item_type": "wrong", "size": "6inch", "type": "pepperoni"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 400
    assert response.data == b'Invalid .json file\n'
    # item size has key but value missing
    data = {"item_type": "pizza", "size": "superbig", "type": "pepperoni"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza info missing to get price\n'
    # pizza without size
    data = {"item_type": "pizza", "type": "pepperoni"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza info missing to get price\n'
    # valid pizza data
    data = {"item_type": "pizza", "size": "6inch", "type": "pepperoni"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 200
    assert response.data == b'14.99'
    # valid drink data
    data = {"item_type": "drink", "name": "Coke"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 200
    assert response.data == b'2.99'
    # valid topping data
    data = {"item_type": "topping", "name": "pepperoni"}
    response = app.test_client().get('/get_item_prices', json=data)
    assert response.status_code == 200
    assert response.data == b'3'


def test_change_item_prices():
    """
    test change_item_prices route
    """
    # data is None
    data = None
    response = app.test_client().post('/change_item_prices', json=data)
    assert response.status_code == 405
    assert response.data == b'Item not received\n'
    # price not in data
    data = {"pizza_size": "6inch", "get_len_right": 2}
    response = app.test_client().post('/change_item_prices', json=data)
    assert response.status_code == 400
    assert response.data == b'Invalid .json file\n'
    # len of data incorrect
    data = {"price": 999}
    response = app.test_client().post('/change_item_prices', json=data)
    assert response.status_code == 400
    assert response.data == b'Invalid .json file\n'
    # pizza data valid
    data = {"pizza_size": "6inch", "price": 9.99}
    response = app.test_client().post('/change_item_prices', json=data)
    assert response.status_code == 200
    assert response.data == b'Pizza price is successfully changed\n'
    # drink data valid
    data = {"drink_name": "Coke", "price": 100}
    response = app.test_client().post('/change_item_prices', json=data)
    assert response.status_code == 200
    assert response.data == b'Drink price is successfully changed\n'
    # topping data valid
    data = {"topping_name": "pepperoni", "price": 200}
    response = app.test_client().post('/change_item_prices', json=data)
    assert response.status_code == 200
    assert response.data == b'Topping price is successfully changed\n'
    # check if drink price is updated
    check_drink_data = {"item_type": "drink", "name": "Coke"}
    response = app.test_client().get('/get_item_prices', json=check_drink_data)
    assert response.status_code == 200
    assert response.data == b'100'
    # check if topping price is updated
    check_topping_data = {"item_type": "topping", "name": "pepperoni"}
    response = app.test_client().get('/get_item_prices', json=check_topping_data)
    assert response.status_code == 200
    assert response.data == b'200'
    # check if pizza price is updated
    check_pizza_data = {"item_type": "pizza", "size": "6inch"}
    response = app.test_client().get('/get_item_prices', json=check_pizza_data)
    assert response.status_code == 200
    assert response.data == b'9.99'


def test_order_total():
    """
    test for order_total route
    """
    order_id = int(app.test_client().get('/new_order').data)
    # data is None
    data = None
    response = app.test_client().get('order_total', json=data)
    assert response.status_code == 405
    assert response.data == b"order not received\n"
    # incorrect order name
    data = {"order_id": -999}
    response = app.test_client().get('order_total',json=data)
    assert response.status_code == 400
    assert response.data == b"order not found\n"
    # valid order .json
    data = {"order_id": order_id}
    response = app.test_client().get('order_total',json=data)
    assert response.status_code == 200
    assert response.data == b"0"


def test_new_order():
    """
    test for new_order route
    """
    response = app.test_client().get('/new_order')
    assert response.status_code == 200
    assert response.data == b'6001'
    response = app.test_client().get('/new_order')
    assert response.status_code == 200
    assert response.data == b'6002'
    app.test_client().get('/new_order')
    app.test_client().get('/new_order')
    response = app.test_client().get('/new_order')
    assert response.status_code == 200
    assert response.data == b'6005'


def test_new_pizza():
    """
    test new order route
    """
    response = app.test_client().get('/new_order')
    order_id = int(response.data)
    # data is None
    data = None
    response = app.test_client().post("/new_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'Order not received\n'
    # more than 3 keys in data
    data = {"order_id": order_id, "type": "pepperoni", "size": "6inch", "bug": "hee-hee"}
    response = app.test_client().post("/new_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # order_id incorrect
    data = {"order_id": -999, "type": "pepperoni", "size": "6inch"}
    response = app.test_client().post("/new_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'Order does not exist\n'
    # type not found
    data = {"order_id": order_id, "type": "wrong_type", "size": "6inch"}
    response = app.test_client().post("/new_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'Type not found\n'
    # size invalid
    data = {"order_id": order_id, "type": "pepperoni", "size": "1000inch"}
    response = app.test_client().post("/new_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'Size invalid\n'
    # pizza data valid
    data = {"order_id": 6000, "type": "pepperoni", "size": "6inch"}
    response = app.test_client().post("/new_pizza", json=data)
    assert response.status_code == 200
    assert response.data == b'1000'


def test_add_drink():
    """
    test add_drink route
    """
    # data is None
    data = None
    response = app.test_client().post("/add_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'Drink not received\n'
    response = app.test_client().get('/new_order')
    order_id = int(response.data)
    # less than two keys in data
    data = {"order_id": order_id}
    response = app.test_client().post("/add_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # order_id incorrect
    data = {"order_id": -999, "name": "Coke"}
    response = app.test_client().post("/add_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'Order does not exist\n'
    # name of drink is invalid
    data = {"order_id": order_id, "name": "not_a_drink"}
    response = app.test_client().post("/add_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'Drink name invalid\n'
    # valid drink data
    data = {"order_id": 6000, "name": "Coke"}
    response = app.test_client().post("/add_drink", json=data)
    assert response.status_code == 200
    assert response.data == b'Drink successfully added to order\n'


def test_remove_drink():
    """
    test remove_drink route
    """
    # data is None
    data = None
    response = app.test_client().delete("/remove_drink", json=data)
    assert response.status_code == 405
    assert response.data == b'Drink not received\n'
    # create an order with this particular drink:
    order_id = int(app.test_client().get('/new_order').data)
    coke_data = {"order_id": order_id, "name": "Coke"}
    coke_response = app.test_client().post("/add_drink", json=coke_data)
    # without a order_id
    data = {"name": "Coke"}
    response = app.test_client().delete("/remove_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'Order ID is invalid\n'
    # more than two attributes
    data = {"order_id": order_id, "name": "Coke", "wrong": "length"}
    response = app.test_client().delete("/remove_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # order_id is incorrect
    data = {"order_id": -999, "name": "Coke"}
    response = app.test_client().delete("/remove_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'Order ID is incorrect\n'
    # Drink not found in order
    data = {"order_id": order_id, "name": "Orange"}
    response = app.test_client().delete("/remove_drink", json=data)
    assert response.status_code == 400
    assert response.data == b'Drink not found in order\n'
    # valid drink data
    data = {"order_id": order_id, "name": "Coke"}
    response = app.test_client().delete("/remove_drink", json=data)
    assert response.status_code == 200
    assert response.data == b'Your drink is deleted\n'


def test_remove_pizza():
    """
    test remove_pizza route
    """
    # data is None
    data = None
    response = app.test_client().delete("/remove_pizza", json=data)
    assert response.status_code == 405
    assert response.data == b'Pizza not received\n'
    # pizza_id key missing
    data = {"wrong_id": 1000}
    response = app.test_client().delete("/remove_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza ID is invalid\n'
    # pizza_id value missing
    data = {"pizza_id": None}
    response = app.test_client().delete("/remove_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza ID is invalid\n'
    # wrong pizza_id
    data = {"pizza_id": -999}
    response = app.test_client().delete("/remove_pizza", json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza ID is incorrect\n'
    # valid pizza data
    data = {"pizza_id": 1000}
    response = app.test_client().delete("/remove_pizza", json=data)
    assert response.status_code == 200
    assert response.data == b'Your Pizza is deleted\n'


def test_add_topping():
    """
    test add_topping route
    """
    # data is None
    data = None
    response = app.test_client().post("/add_toppings", json=data)
    assert response.status_code == 400
    assert response.data == b'topping not received\n'

    # data is not none
    response = app.test_client().get('/new_order')
    order_id = int(response.data)
    pizza_data = {"order_id": order_id, "type": "pepperoni", "size": "6inch"}

    response = app.test_client().post('/new_pizza', json=pizza_data)
    pizza_id = int(response.data)
    # less than two keys in data
    data = {"pizza_id": pizza_id}
    response = app.test_client().post("/add_toppings", json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # pizza_id incorrect
    data = {"pizza_id": -999, "extra_toppings": ["pepperoni", "mushrooms"]}
    response = app.test_client().post("/add_toppings", json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza does not exist\n'
    # name of topping is invalid
    data = {"pizza_id": pizza_id, "extra_toppings": ["apple", "water"]}
    response = app.test_client().post("/add_toppings", json=data)
    assert response.status_code == 400
    assert response.data == b'Topping name invalid\n'


def test_remove_toppings():
    """
    test remove_topping route
    """
    # data is None
    data = None
    response = app.test_client().delete('/remove_toppings', json=data)
    assert response.status_code == 405
    assert response.data == b'Topping not received\n'
    # length of data is incorrect
    data = {"pizza_id": 1000, "removed_toppings": "pepperoni", "incorrect": "length"}
    response = app.test_client().delete('/remove_toppings', json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # pizza_id invalid
    data = {"pizza_id": -999, "removed_toppings": "pepperoni"}
    response = app.test_client().delete('/remove_toppings', json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza does not exist\n'
    # invalid topping name
    ord_id = int(app.test_client().get('/new_order').data)
    pizza_data = {"order_id": ord_id, "type": "pepperoni", "size": "6inch"}
    pizza_id = int(app.test_client().post("/new_pizza", json=pizza_data).data)

    data = {"pizza_id": pizza_id, "removed_toppings": "wrong_topping"}
    response = app.test_client().delete('/remove_toppings', json=data)
    assert response.status_code == 400
    assert response.data == b'Topping name invalid\n'
    # Topping does not exit in pizza
    data = {"pizza_id": pizza_id, "removed_toppings": 'mushrooms'}
    response = app.test_client().delete('/remove_toppings', json=data)
    assert response.status_code == 400
    assert response.data == b'Topping does not exit in pizza\n'
    # valid topping data
    data = {"pizza_id": pizza_id, "removed_toppings": "pepperoni"}
    response = app.test_client().delete('/remove_toppings', json=data)
    assert response.status_code == 200
    assert response.data == b'Topping successfully deleted\n'


def test_cancel_order():
    """
    test cancel_order route
    """
    # data is None
    data = None
    response = app.test_client().delete('/cancel_order', json=data)
    assert response.status_code == 500
    assert response.data == b'Order ID is invalid\n'

    order_response = app.test_client().get('/new_order')
    order_id = int(order_response.data)
    # order does not exit
    data = {"order_id": -999}
    response = app.test_client().delete('/cancel_order', json=data)
    assert response.status_code == 405
    assert response.data == b'Order does not exist\n'
    # order exits
    data = {"order_id": order_id}
    response = app.test_client().delete('/cancel_order', json=data)
    assert response.status_code == 200
    assert response.data == b'Your order is canceled\n'


def test_create_new_toppings():
    """
    test create_new_toppings route
    """
    # data is None {"topping_type": "ham", "price": 2}
    data = None
    response = app.test_client().post('/create_new_toppings', json=data)
    assert response.status_code == 400
    assert response.data == b'Topping type no received\n'
    # json file invalid
    data = {"topping_type": "ham", "price": 2, "invalid": "file"}
    response = app.test_client().post('/create_new_toppings', json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # json file invalid
    data = {"topping_type": "ham", "price": 2}
    response = app.test_client().post('/create_new_toppings', json=data)
    assert response.status_code == 200
    assert response.data == b'New topping added into topping_type_to_price.json\n'


def test_create_new_pizza_type():
    """
    test create_new_pizza_types route
    """
    # data is None:
    data = None
    response = app.test_client().post('/create_new_pizza_type', json=data)
    assert response.status_code == 400
    assert response.data == b'Pizza type no received\n'
    # .json file invalid
    data = {"pizza_type": "Hawaiian", "description": "Pineapple might not be the first thing that comes to mind when you think pizza."
            "But add in some ham and it creates an unexpectedly solid sweet and salty combination for this type of pizza.",
             "toppings": ["ham", "pineapple"], "wrong_file": "this"}
    response = app.test_client().post('/create_new_pizza_type', json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # valid .json file
    data = {"pizza_type": "Hawaiian", "description": "Pineapple might not be the first thing that comes to mind when you think pizza."
            "But add in some ham and it creates an unexpectedly solid sweet and salty combination for this type of pizza.",
             "toppings": ["ham", "pineapple"]}
    response = app.test_client().post('/create_new_pizza_type', json=data)
    assert response.status_code == 200
    assert response.data == b'New pizza type created\n'


def test_checkout():
    """
    test checkout route
    """
    # data is None
    data = None
    response = app.test_client().post('/checkout', json=data)
    assert response.status_code == 405
    assert response.data == b'Order_id not received\n'
    # .json file invalid
    data = {"order_id": -999, "wrong": "str"}
    response = app.test_client().post('/checkout', json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # order ID invalid
    data = {"order_id": -999}
    response = app.test_client().post('/checkout', json=data)
    assert response.status_code == 400
    assert response.data == b'Order does not exist\n'
    # order not paid
    order_id = int(app.test_client().get('/new_order').data)
    data = {"order_id": order_id}
    response = app.test_client().post('/checkout', json=data)
    assert response.status_code == 200
    assert response.data == b'Your order is checked out and ready for delivery\n'


def test_add_delivery_details():
    """
    test delivery route
    """
    # data is None
    data = None
    response = app.test_client().post("/delivery", json=data)
    assert response.status_code == 400
    assert response.data == b'Delivery information not received\n'
    # order ID does not exist
    data = {"order_id": -999, "address": "772 dundas street east", "postal_code": "L5G 2G1",
            "delivery_method": "Ubereats"}
    order_id = int(app.test_client().get("/new_order", json=data).data)
    response = app.test_client().post("/delivery", json=data)
    assert response.status_code == 400
    assert response.data == b'Order does not exist\n'
    # json file invalid
    data = {"order_id": order_id, "order_details": "pepperoni, Coke", "delivery_method": "Ubereats"}
    response = app.test_client().post("/delivery", json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # json file invalid
    data = {"order_id": order_id, "order_details": "pepperoni, Coke",
            "delivery_method1": "Ubereats", "delivery_method2": "Ubereats",
            "delivery_method3": "Ubereats", "delivery_method4": "Ubereats",
            "delivery_method5": "Ubereats", "delivery_method6": "Ubereats"}
    response = app.test_client().post("/delivery", json=data)
    assert response.status_code == 400
    assert response.data == b'.json file invalid\n'
    # order ID does not exist
    data = {"order_id": order_id, "address": "77 dundas street",
            "postal_code": "L5G 2G1", "delivery_method": "SkipTheDishes"}
    response = app.test_client().post("/delivery", json=data)
    assert response.status_code == 400
    assert response.data == b'Please choose a valid delivery method\n'
    data = {"order_id": order_id, "address": "772 dundas street east", "postal_code": "L5G 2G1",
            "delivery_method": "Ubereats"}
    response = app.test_client().post("/delivery", json=data)
    # does not checkout
    assert response.status_code == 400
    assert response.data == b"You have not paid for this order, please checkout first\n"
    # checkout this order
    checkout_data = {"order_id": order_id}
    checkout_response = app.test_client().post("/checkout", json=checkout_data)
    response = app.test_client().post("/delivery", json=data)
    assert response.status_code == 200
    assert response.data == b"order will send to your address soon\n"
    assert checkout_response.status_code == 200
    assert checkout_response.data == b'Your order is checked out and ready for delivery\n'
    # check if successfully saved in saved_orders

    json_data = {"order_id": order_id, "delivery_method": "Ubereats", "address": "ADDRESS", "postal_code": "POSTALCODE"}
    app.test_client().post("/delivery", json=json_data)
    csv_data = {"order_id":  order_id, "delivery_method": "Foodora", "address": "ADDRESS", "postal_code": "POSTALCODE"}
    app.test_client().post("/delivery", json=csv_data)
    files = os.listdir("./saved_orders")
    assert str(order_id) + '.json' in files
    assert str(order_id) + '.csv' in files


def test_customer_main():
    with mock.patch('builtins.input', return_value="1"):
        ask_for_full_menu()
        customer_main(True)
    with mock.patch('builtins.input', return_value="2"):
        item_json = {"item_type": 'pizza', "size": "6inch"}
        get_item_prices(item_json)
        item_json = {"item_type": 'drink', "name": "Coke"}
        get_item_prices(item_json)
        customer_main(True)
    with mock.patch('builtins.input', return_value="3"):
        #order 6000 and 6001
        create_new_order()
        create_new_order()
        customer_main(True)
    with mock.patch('builtins.input', return_value="4"):
        pizza_json = {"order_id": 6000, "type": "pepperoni", "size": "6inch"}
        create_new_pizza(pizza_json)
        pizza_json = {"order_id": 6001, "type": "pepperoni", "size": "9inch"}
        create_new_pizza(pizza_json)
        drink_json = {"order_id": 6000, "name": "Coke"}
        create_new_drink(drink_json)
        customer_main(True)
    with mock.patch('builtins.input', return_value="5"):
        pizza_json = {"pizza_id": 1000}
        customer_delete_pizza(pizza_json)
        drink_json = {"order_id": 6000, "name": "Coke"}
        delete_drink(drink_json)
        customer_main(True)
    with mock.patch('builtins.input', return_value="6"):
        topping_json = {"pizza_id": 1001, "extra_toppings": ["mushrooms"]}
        add_topping(topping_json)
        customer_main(True)
    with mock.patch('builtins.input', return_value="7"):
        cancel_order({"order_id": 6001})
    with mock.patch('builtins.input', return_value="8"):
        order_total({"order_id": 6000})
        checkout({"order_id": 6000})
    with mock.patch('builtins.input', return_value="9"):
        delivery_json = {"order_id": 6000, "address": "here", "postal_code": "any_code", "delivery_method": "Ubereats"}
        add_delivery_details(delivery_json)
        customer_main(True)
    with mock.patch('builtins.input', return_value="A"):
        pizza_json = {"pizza_type": "pepperoni", "description": "Made by pepperoni, a American variety of salami, made from a cured mixture of pork and beef seasoned with paprika or other chili pepper.", "toppings": ["olives", "tomatoes", "pepperoni"]}
        create_new_pizza_type(pizza_json)
        topping_json = {"topping_type": "pepperoni", "price": 3}
        create_new_toppings(topping_json)
        customer_main(True)
    with mock.patch('builtins.input', return_value="exit"):
        customer_main(True)


