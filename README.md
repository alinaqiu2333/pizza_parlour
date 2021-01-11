# a2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

# how to run the program
Pizzaparlour.py main.py 
Open two command line prompt, type python PizzaParlour.py in the first command line prompt which sets up the flask server. In order to get customers to order items, open another terminal and type python3 main.py, which runs the client command prompt interface. This shows customer the full menu, and other options that a customer may need. Eg: submit a new order or add a pizza into an existing order.
The customer types in standard input and our program retrieves data and send it to flask server. The flask server will handle the data, and if it has some error on the data it receives, it will report the error. 
Noted that since we started this assignment by using cURL commands only, therefore in docstring of each function there exists the corresponding cURL commands, which the user can also order items directly.  

# add new type specification: 
After running `python3 main.py`, the customer will see the following:
Hi, this is PizzaParlour. Anything I can help with?
1. Ask for full menu
2. Search specific item's price
3. Submit a new order
4. Add items to existing order
5. Remove items from exiting order
6. Update toppings in existing pizza
7. Cancel an order
8. Checkout an order
9. Add delivery details (you must checkout first)
A. MAKE CHANGES TO MENU
Choose 1,2,3,4,5,6,7,8,9,10,A: 

Noted that inputing "A" allows you to change the current menu. After adding new type of pizza, say "Cheese pizza", the menu will be automatically updated. However, since in tests/unit_tests.py, the test case for checking menu is hard-coded to make sure the menu is absolutely correct and exactly what we wanted. Therefore, if a change has been made on menu, including adding a new pizza type and adding a new topping type, test_get_menu() will occur an error. 
Please run `pytest tests/unit_tests.py`

# what each file does
1. main.py: client command prompt interface. A program that retrives user input data and send it to flask server. 
2. PizzaParlour.py: the flask server API module. It handles data receiving from main.py and send back some data when it is necessary. It will also output some error message when it has some error on the input data. 
3. Objects.py: A python module that contains all the objects we need in our program
4. functions.py: Using factory design pattern that can create different object without exposing the creation logic to the client

# Design pattern
1. factory design pattern. In functions.py, we create different object without exposing the creation logic to the client and refer to newly created object using a common interface. The objects we can create are Pizza, Drink, Order, Topping
2. Buider design pattern: For object Order, we separate the construction of this complex object from its representation so that the same construction process can create different representations. For instance, order 6000 can contain different kinds of pizzas and drinks, and order 6001 can contain some other kinds of pizzas and drinks. 
3. Encapsulation: Object oriented programming. We bund the data(attribute) with the methods that operate on that data, in order to restrict the direct access to some of an object's components. For instance, instead of directly touching an order's pizzas attribute, like self.pizzas = ['pepperoni', 'vegetarian'], we create method like set_order_pizzas(pizzas), set_order_id(id) so that we don't need to direct access to that object's components.
4. SOLID Principle: Single-responsibilty principle. Each class, module, or function in our program only do one job. All the methods in our object class only do one job without doing anything extra.
5. dependency injection: Our pizza object depends on the topping object. the method pizza.set_pizza_toppings(pizza_tyoe:str) create topping class internally in this method. It is a technique in which an object receives other objects that it depends on. These other objects are called dependencies.

# Pair programming
1. The git commit messages that start with ppaln are the features and code we pair programmindg together. alinaqiu2333 is the driver, and SkrPaoWang is the navigator.
feature: new pizza(), new order(). Users can be able to create pizza and add the pizza to that order.
Since this is one of the main features, we discuss about the design pattern we should use for this feature. We are thinking about composition, command design pattern, and some other patterns. Finally, we choose builder design patttern and factory design pattern for this part. Things went well are both of us are willing to contribute our own ideas on how to build this feature, and we have a great conversation since we heard how other people will design such a feature in his way and we find there are so many ways to write a program that outputs the correct results, but how to write elegant, and efficent code is much more important in software design. Things don't went too well are as time goes through. Since this is one of the early developed features (the ones we developed first), we dont know what to write for sure. Therefore, the more we wonders and talks, we gradually lose our attension. This casused our productivity gradually decrease. We find out next time we should have some small breaks during the discussion so we can focus better later. Also, even though it's necessary to spend time on designing the structure, the most important thing is get the coding started. In our first programming experience, although we did not get a lot done, but the progress get improved a lot after we finish these two features. the good part of this experience is it practise the ability of the navigator to talk about a structure, how to code, and why it makes sense other than just write it down. It also effectively prevents people who "pretends to listen during discussion and just nod along" (this does not appear in this assignment, but I believe we've all met people like that:) ); since this doesn't work during paired-programming: because no matter how much iteas your partner have, YOU still need to write the code.

2. The git commit messages that start with ppskr are the features and code we pair programming together. SkrPaoWang is the driver, and alinaqiu2333 is the navigator.
feature: add_delivery_details(). Users can be able to add delivery details to the flask server.
At first, we discuss about it and wrote some code down. Unfortunstely it behaves wrong. Because we let the user to type order id, order details and send order id and order details to flask API. Later, when we discuss about it again, we think it's not necessary to request order details. This is because if a user has already submitted an order, there is no need for that user to type again the order details (what he/she orders). It is better to implement this feature is to let user only type an order id plus the deliery method and address, and then the flask server can find the order info in the all_order dictionary and then we cast it to a json file. The good thing about this pair programming is the navigator finds the better way to implement this feature compared to the previous implementation, and the navigator tells the driver about it. It's how we can make better product, communication between each other. Coding part for this paired programming section is limited to the driver forces people to pay attension to every word the naviator said. This experiece helps both of the people to concentrate and focus on a specific feaure. Something not good is we wasted a few hours (before paired programming) on delivery method, and the tests for it is already finished. Therefore it takes time to change this method, along with its tests. 

# how to test
start a terminal and run `python3 PizzaParlous.py` as server. Then start another terminal, go to the same directory, which is assignment-2-24-alinaqiu2333-skrpaowang, and type `python3 tests/unit_tests.py`. If no error occurs, it means the code should be fine. 

# test coverages
All tests are written in tests/unit_tests.py . To see test coverage, simply go to directory assignment-2-24-alinaqiu2333-skrpaowang and run server, which is PizzaParlour.py. Then start another terminal and run `pytest --cov-report term --cov=. tests/unit_tests.py`. According to our output, the test coverage is 91%. result screenshot shown in folder test_results. 

# Code craftsmanship
We use 
lint to help us create clean code. We typically focus on main.py, PizzaParlour.py, and unit_test.py, since
they are the main part of our program.  It follows the style recommended by PEP 8, the Python style guide.