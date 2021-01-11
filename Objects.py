# from PizzaParlour import *
import json, os, csv

# load all .json files
# print('=='*30)
# print(os.path.dirname(os.path.realpath(__file__)))
with open('./drink_name_to_price.json', 'r') as f:
    drink_name_to_price = json.load(f)
with open('./pizza_size_to_price.json', 'r') as f:
    pizza_size_to_price = json.load(f)
with open('./topping_type_to_price.json', 'r') as f:
    topping_type_to_price = json.load(f)
with open('./pizza_type_to_description.json', 'r') as f:
    pizza_type_to_description = json.load(f)
with open('./pizza_type_to_toppings.json', 'r') as f:
    pizza_type_to_toppings = json.load(f)


class Topping:
    def __init__(self):
        self.toppings = None

    def set_toppings(self, topping_list: list):
        self.toppings = topping_list

    def add_toppings(self, topping_list: list):
        self.toppings.extend(topping_list)

    def get_toppings(self):
        return self.toppings

    def delete_topping(self, delete_topping: str):
        temp_t = self.toppings[:]
        for t in temp_t:
            if t == delete_topping:
                self.toppings.remove(t)
        return

    def get_price(self):
        total = 0
        if self.toppings is not None:
            for ingredients in self.toppings:
                total += topping_type_to_price[ingredients]
        return total


class Pizza:
    def __init__(self):
        self.id = None
        self.type = None
        self.toppings = None
        self.size = None
        self.price = None
        self.description = None

    def set_pizza_id(self, pizza_id: int):
        self.id = pizza_id

    def set_pizza_type_description(self, pizza_type: str):
        self.type = pizza_type
        self.description = pizza_type_to_description[pizza_type]

    def set_pizza_size(self, size: str):
        self.size = size

    def set_pizza_toppings(self, toppings: Topping):
        self.toppings = toppings

    def set_pizza_price(self):
        self.price = pizza_size_to_price[self.size]
        self.price += self.toppings.get_price()

    def get_price(self):
        return self.price


class Drink:
    def __init__(self):
        self.name = None
        self.price = None

    def set_name_price(self, name: str):
        self.name = name
        self.price = drink_name_to_price[name]

    def get_price(self):
        return self.price


class Order:
    def __init__(self):
        self.id = None
        self.pizzas = []
        self.drinks = []
        self.delivery_method = None
        self.postal_code = None
        self.address = None
        # default
        self.status = "UNPAID"

    def set_order_id(self, order_id: int):
        self.id = order_id

    def add_pizza(self, pizza: Pizza):
        self.pizzas.append(pizza)

    def add_drink(self, drink: Drink):
        self.drinks.append(drink)

    def delete_pizza(self, pizza_id: str):
        for pizza in self.pizzas:
            if pizza.id == pizza_id:
                self.pizzas.remove(pizza)

    def delete_drink(self, drink_name: str):
        tmp = self.drinks[:]
        for drink in tmp:
            if drink.name == drink_name:
                self.drinks.remove(drink)
                break

    def get_total_price(self):
        order_total = 0
        if self.pizzas is not None:
            for pizzas in self.pizzas:
                order_total += pizzas.get_price()
        if self.drinks is not None:
            for drink in self.drinks:
                order_total += drink.get_price()
        return order_total

    def set_delivery_method(self, method):
        self.delivery_method = method

    def set_address_postal_code(self, address, postal_code):
        self.address = address
        self.postal_code = postal_code

    def change_status(self, status: str):
        self.status = status

    def get_status(self):
        return self.status

    def delivery_info_in_json(self):
        json_info = {"order_id": self.id, "address": self.address, "postal_code": self.postal_code,
                     "items": [str(i) for i in self.pizzas]}
        json_info["items"] += [str(j) for j in self.drinks]
        with open('./saved_orders/' + str(self.id) + '.json', 'w') as file:
            json.dump(json_info, file)

    def delivery_info_in_csv(self):
        csv_info = [["order number", self.id], ["address", self.address],
                ["items"] + [str(i) for i in self.pizzas] + [str(j) for j in self.drinks]]
        with open('./saved_orders/' + str(self.id) + '.csv', 'w') as file:
            writer = csv.writer(file)
            for row in csv_info:
                writer.writerow(row)
# #testing
# t1 = Topping()
# t2 = Topping()
# t1.set_toppings(["pepperoni"])
# t2.set_toppings(["pepperoni"])
# p1 = Pizza()
# p1.set_pizza_toppings(t1)
# p1.set_pizza_size_price('6inch')
# p2 = Pizza()
# p2.set_pizza_toppings(t2)
# p2.set_pizza_size_price('9inch')
# # d1 = Drink()
# # d1.set_name_price("Pepsi")
# ordd = Order()
# # ordd.set_order_drinks([d1])
# ordd.set_order_pizzas([p1, p2])
# # print(ordd.drinks)
# print(ordd.get_total_price())
