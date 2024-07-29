from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

class GroceryChatBot:
    def __init__(self):
        self.menu = {
            'Fruits': {'Apple': 1.23, 'Banana': 0.5, 'Orange': 0.75},
            'Vegetables': {'Carrot': 0.25, 'Broccoli': 1.25, 'Spinach': 1.0},
            'Dairy': {'Milk': 2.0, 'Cheese': 3.0, 'Yogurt': 1.5},
            'Bakery': {'Bread': 2.5, 'Croissant': 1.75, 'Muffin': 1.5}
        }
        self.cart = {}

    def add_to_cart(self, category, item, quantity):
        if category in self.menu and item in self.menu[category]:
            if item in self.cart:
                self.cart[item] += quantity
            else:
                self.cart[item] = quantity

    def remove_from_cart(self, item):
        if item in self.cart:
            del self.cart[item]

    def update_cart(self, item, quantity):
        if item in self.cart:
            self.cart[item] = quantity

    def clear_cart(self):
        self.cart.clear()

    def get_category(self, item_name):
        for category, items in self.menu.items():
            if item_name in items:
                return category
        return None

bot = GroceryChatBot()

@app.route('/')
def index():
    return render_template('index.html', menu=bot.menu)

@app.route('/add', methods=['POST'])
def add_to_cart():
    category = request.form['category']
    item = request.form['item']
    quantity = int(request.form['quantity'])
    bot.add_to_cart(category, item, quantity)
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = bot.cart
    total = 0
    for item, quantity in cart.items():
        category = bot.get_category(item)
        price = bot.menu[category][item]
        total += price * quantity
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove', methods=['POST'])
def remove_from_cart():
    item = request.form['item']
    bot.remove_from_cart(item)
    return redirect(url_for('view_cart'))

@app.route('/update', methods=['POST'])
def update_cart():
    item = request.form['item']
    quantity = int(request.form['quantity'])
    bot.update_cart(item, quantity)
    return redirect(url_for('view_cart'))

@app.route('/clear')
def clear_cart():
    bot.clear_cart()
    return redirect(url_for('view_cart'))

if __name__ == "__main__":
    app.run(debug=True)


mkdir templates

