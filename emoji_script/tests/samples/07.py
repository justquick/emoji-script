prices = {'apple': 0.40, 'banana': 0.50}
my_purchase = {
    'apple': 1,
    'banana': 6}
grocery_bill = 0
for fruit in my_purchase:
    grocery_bill += prices[fruit] * my_purchase[fruit]
print('I owe the grocer $%.2f' % grocery_bill)
