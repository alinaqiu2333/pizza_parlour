import requests
# since the customers are not using curl, we need methods to send request for post/get to server


def ask_for_full_menu():
    """
    client ask flask API for menu
    """
    res = requests.get(url='http://127.0.0.1:5000/full_menu')
    return res.text


def get_item_prices(user_data):
    """
    client ask API for specific item prices
    """
    res = requests.get(url='http://127.0.0.1:5000/get_item_prices', json=user_data)
    return res.text


def create_new_order():
    """
    client ask flask API for creating a new order
    """
    res = requests.get(url='http://127.0.0.1:5000/new_order')
    return res.text


def create_new_pizza(user_data):
    """
    client ask flask API for add a new pizza to an exisiting order
    """
    pizza_res = requests.post(url = "http://127.0.0.1:5000/new_pizza", json=user_data)
    return pizza_res.text


def create_new_drink(user_data):
    """
    client ask flask API for add a new drink to an exisiting order
    """
    drink_res = requests.post(url = "http://127.0.0.1:5000/add_drink", json=user_data)
    return drink_res.text


def customer_delete_pizza(user_data):
    """
    client ask flask API to remove a pizza from an exisiting order
    """
    delete_res = requests.post(url = "http://127.0.0.1:5000/remove_pizza", json=user_data)
    return delete_res.text


def delete_drink(user_data):
    """
    client ask flask API to remove a drink from an exisiting order
    """
    delete_res = requests.post(url = "http://127.0.0.1:5000/remove_drink", json=user_data)
    return delete_res.text


def add_topping(user_data):
    """
    client ask flask API to add some toppings to an existing pizza
    """
    top_res = requests.post(url = "http://127.0.0.1:5000/add_toppings", json=user_data)
    return top_res.text


def remove_topping(user_data):
    """
    client ask flask API to remove some toppings to an existing pizza
    """
    top_res = requests.post(url='http://127.0.0.1:5000/remove_toppings', json=user_data)
    return top_res.text


def add_delivery_details(user_data):
    """
    client ask flask API to add delivery details to specific order
    """
    delivery_res = requests.post(url = "http://127.0.0.1:5000/delivery", json=user_data)
    return delivery_res.text


def cancel_order(user_data):
    """
    client ask flask API to cancel specific order
    """
    can_res = requests.delete(url="http://127.0.0.1:5000/cancel_order", json=user_data)
    return can_res.text


def checkout(user_data):
    """
    client ask flask API to checkout specific order
    """
    checkout_res = requests.post(url="http://127.0.0.1:5000/checkout", json=user_data)
    return checkout_res.text


def order_total(user_data):
    """
    client ask flask API to return the total amount of the order
    """
    total_res = requests.get(url="http://127.0.0.1:5000/order_total", json=user_data)
    return total_res.text


def change_item_prices(user_data):
    """
     client ask flask API to change a price of an item
    """
    change_price_res = requests.post(url="http://127.0.0.1:5000/change_item_prices", json=user_data)
    return change_price_res.text


def create_new_toppings(user_data):
    """
     client ask flask API to create a new topping for the menu
    """
    new_topping_res = requests.post(url="http://127.0.0.1:5000/create_new_toppings", json=user_data)
    return new_topping_res.text


def create_new_pizza_type(user_data):
    """
     client ask flask API to create a new topping for the menu
    """
    new_pizza_type_res = requests.post(url="http://127.0.0.1:5000//create_new_pizza_type", json=user_data)
    return new_pizza_type_res.text


def customer_main(test=False):
    continues = True
    while continues:
        print("Hi, this is PizzaParlour. Anything I can help with?")
        print("1. Ask for full menu")
        print("2. Search specific item's price")
        print("3. Submit a new order")
        print("4. Add items to existing order")
        print("5. Remove items from exiting order")
        print("6. Update toppings in existing pizza")
        print("7. Cancel an order")
        print("8. Checkout an order")
        print("9. Add delivery details (you must checkout first)")
        print("A. MAKE CHANGES TO MENU")
        user_input = input("Choose 1,2,3,4,5,6,7,8,9,10,A: ")

        if user_input == "1":   # show full menu
            menu = ask_for_full_menu()
            print(menu)
            if test:
                continues = False

        if user_input == "2":  # search specific item's price
            item_type = input("please input the type [pizza, drink, topping]\n")
            if item_type == "pizza":
                item_size = input("please input the size[6inch, 9inch, 12inch]\n")
                item_json = {"item_type": item_type, "size": item_size}
                print("the price is $" + get_item_prices(item_json))
            elif item_type == "drink":
                name = input("please input the name [Coke, Diet Coke, Coke Zero, Pepsi, Diet Pepsi, Dr. Pepper, Water, Juice]\n")
                item_json = {"item_type": item_type, "name": name}
                print("the price is $" + get_item_prices(item_json))
            elif item_type == "topping":
                name = input("please input the name [olives, tomatoes, mushrooms, jalapenos, chicken, beef, pepperoni]\n")
                item_json = {"item_type": item_type, "name": name}
                print("the price is $" + get_item_prices(item_json))
            if test:
                continues = False

        if user_input == "3":        # submit new order
            order_id = create_new_order()
            print("your order id is:", order_id)
            if test:
                continues = False

        if user_input == "4":   # update existing order/ add items
            type_input = input("item you willing to add [pizza, drink]\n")
            if type_input == "pizza":
                order_id_input = input("please input order id:")
                pizza_type_input = input("please input pizza_type:")
                pizza_size_input = input("please input pizza_size:")
                pizza_json = {"order_id": int(order_id_input), "type": pizza_type_input,
                "size": pizza_size_input}
                response = create_new_pizza(pizza_json)
                print("Your pizza id is:", response)
            elif type_input == "drink":
                order_id_input = input("please input order id:")
                drink_type_input = input("please input drink_type:")
                drink_json = {"order_id": int(order_id_input), "name": drink_type_input}
                response = create_new_drink(drink_json)
                print(response)
            if test:
                continues = False

        if user_input == "5":       # update existing order/ delete items
            type_input = input("item you willing to remove [pizza, drink]\n")
            if type_input == "pizza":
                pizza_id_input = input("please input pizza id:")
                pizza_json = {"pizza_id": int(pizza_id_input)}
                response = customer_delete_pizza(pizza_json)
                print(response)
            elif type_input == "drink":
                order_id_input = input("please input order id:\n")
                drink_name_input = input("please input drink name:\n")
                drink_json = {"order_id": int(order_id_input), "name": drink_name_input}
                response = delete_drink(drink_json)
                print(response)
            if test:
                continues = False

        if user_input == "6":  # update existing order/ Add or remove Topping to Pizza
            type_input = input("Do you want to remove or add toppings? [add, remove]\n")
            if type_input == "add":
                pizza_id_input = input("please input pizza id:")
                num_of_toppings = input("How many toppings you want to add:\n")
                topping_list = []
                for i in range(int(num_of_toppings)):
                    topping = input("Type topping name:\n")
                    topping_list.append(topping)

                topping_json = {"pizza_id": int(pizza_id_input), "extra_toppings": topping_list}
                response = add_topping(topping_json)
                print(response)
            elif type_input == "remove":
                pizza_id_input = input("please input pizza id:\n")
                removed_toppings = input("please input topping name:\n")
                topping_json = {"pizza_id": int(pizza_id_input), "removed_toppings": removed_toppings}
                response = remove_topping(topping_json)
                print(response)
            if test:
                continues = False

        if user_input == "7":   # cancel order
            order_id_input = input("please input order id:\n")
            order_json = {"order_id": int(order_id_input)}
            response = cancel_order(order_json)
            print(response)
            if test:
                continues = False

        if user_input == '8':   # checkout
            order_id_input = input("please input order id:\n")
            order_json = {"order_id": int(order_id_input)}
            response_amount = order_total(order_json)
            response_msg = checkout(order_json)
            print("your order is $", response_amount + "\n")
            print(response_msg)
            if test:
                continues = False

        if user_input == "9":    # add delivery details
            order_id_input = input("please input order id:\n")
            address = input("please type the address you want to deliver to:\n")
            postal_code = input("please type the postal code of that address:\n")
            delivery_method = input("Choose your delivery method(Ubereats,Foodora,In-house delivery): \n")
            if delivery_method == "Ubereats":
                delivery_json = {"order_id": int(order_id_input),"address": address,
                                 "postal_code": postal_code, "delivery_method": delivery_method}
                response = add_delivery_details(delivery_json)
                print(response, "\ndata saved in " + str(order_id_input) + " as json file")
            elif delivery_method == "Foodora":
                delivery_csv = {"order_id": int(order_id_input),"address": address,
                                 "postal_code": postal_code, "delivery_method": delivery_method}
                response = add_delivery_details(delivery_csv)
                print(response, "\ndata saved in " + str(order_id_input), "as csv file")
            if test:
                continues = False

        if user_input == "A": # create new featues
            feature_type = input("please type the item you want to create [pizza, topping]:\n")
            if feature_type == "pizza":
                pizza_type = input("please input the type of this pizza: \n")
                pizza_description = input("please input the description for this pizza: \n")
                pizza_toppings = input("please input the price of this pizza \n")
                pizza_json = {"pizza_type": pizza_type, "description": pizza_description, "toppings": [pizza_toppings]}
                response = create_new_pizza_type(pizza_json)
                print(response)
            elif feature_type == "topping":
                topping_name = input("please input the name of this topping: \n")
                topping_price = input("please input the price of this topping \n")
                topping_json = {"topping_type": topping_name, "price": topping_price}
                response = create_new_toppings(topping_json)
                print(response)
            if test:
                continues = False

        user_input = input("Type exit to exit the program or type anything to go back to main menu\n")

        if user_input == "exit":
            continues = False


if __name__ == "__main__":
    customer_main()
