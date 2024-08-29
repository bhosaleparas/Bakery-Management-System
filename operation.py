class Admin:
    admin_registry = {}
    product_catalog = []

    def __init__(self, admin_id, username, password, name, contact_details):
        self.admin_id = admin_id
        self.username = username
        self.password = password
        self.name = name
        self.contact_details = contact_details
        Admin.admin_registry[username] = self

    @classmethod
    def register_admin(cls, admin_id, username, password, name, contact_details):
        if username in cls.admin_registry:
            raise ValueError("Admin with this username already exists.")

        new_admin = cls(admin_id, username, password, name, contact_details)
        return new_admin

    @classmethod
    def validate_admin(cls, username, password):
        admin = cls.admin_registry.get(username)

        if admin and admin.password == password:
            return True

        return False

    def update_contact_details(self, new_contact_details):
        self.contact_details = new_contact_details

    def add_product(self, product_id, name, category, price, quantity_available, ingredients):
        new_product = Product(product_id, name, category,price, quantity_available, ingredients)
        Admin.product_catalog.append(new_product)
        print(f"Product '{name}' added successfully.")

    def remove_product(self, product_id):
        product_to_remove = None

        for product in Admin.product_catalog:
            if product.product_id == product_id:
                product_to_remove = product
                break

        if product_to_remove:
            Admin.product_catalog.remove(product_to_remove)
            print(f"Product '{product_to_remove.name}' removed successfully.")

        else:
            print(f"Product with ID {product_id} not found.")


    def update_product(self, product_id, name=None, category=None, price=None, quantity_available=None, ingredients=None):
        product_to_update = None

        for product in Admin.product_catalog:
            if product.product_id == product_id:
                product_to_update = product
                break

        if product_to_update:
            if name:
                product_to_update.name = name
            if category:
                product_to_update.category = category
            if price:
                product_to_update.price = price
            if quantity_available is not None:
                product_to_update.quantity_available = quantity_available
            if ingredients:
                product_to_update.ingredients = ingredients
            print(f"Product '{product_to_update.name}' updated successfully.")

        else:
            print(f"Product with ID {product_id} not found.")


    @staticmethod
    def view_all_products():
        print("---- All Products ----")

        for product in Admin.product_catalog:
            print(f"- {product.product_id}: {product.name} | Category: {product.category} | Price: ${product.price} | Available: {product.quantity_available}")
        print("----------------------")



    @staticmethod
    def view_bakery_details(orders):
        print("---- Bakery Details ----")
        print(f"Total Products: {len(Admin.product_catalog)}")

        for product in Admin.product_catalog:
            print(
                f"- {product.name}: {product.quantity_available} available at ${product.price} each")

        print(f"Total Orders: {len(orders)}")

        for order in orders:
            print(
                f"- Order ID {order.order_id}: {len(order.products)} products, Total: ${order.calculate_total()}")
        print("------------------------")


class Customer:
    customer_registry = {}
    order_registry = []

    def __init__(self, customer_id, username, password, name, contact_details):
        self.customer_id = customer_id
        self.username = username
        self.password = password
        self.name = name
        self.contact_details = contact_details
        self.cart = []
        Customer.customer_registry[username] = self


    @classmethod
    def register_customer(cls, customer_id, username, password, name, contact_details):
        if username in cls.customer_registry:
            raise ValueError("Customer with this username already exists.")

        new_customer = cls(customer_id, username,
                           password, name, contact_details)

        return new_customer


    @classmethod
    def login_customer(cls, username, password):
        customer = cls.customer_registry.get(username)

        if customer and customer.password == password:
            return customer

        return None


    def view_products(self):
        print("---- Available Products ----")

        for product in Admin.product_catalog:
            print(f"- {product.product_id}: {product.name} | Category: {product.category} | Price: ${product.price} | Available: {product.quantity_available}")

        print("----------------------------")


    def add_to_cart(self, product_id, quantity):
        product = next(
            (p for p in Admin.product_catalog if p.product_id == product_id), None)

        if product and product.quantity_available >= quantity:
            self.cart.append((product, quantity))
            print(f"Added {quantity} of '{product.name}' to the cart.")

        else:
            print(f"Product not found or insufficient stock.")



    def purchase_cart(self):
        if not self.cart:
            print("Cart is empty.")
            return

        total_amount = sum(
            product.price * quantity for product, quantity in self.cart)

        new_order = Order(len(Customer.order_registry) + 1, self)

        for product, quantity in self.cart:
            new_order.add_product(product, quantity)

        self.cart = []          # Empty the cart after purchase

        Customer.order_registry.append(new_order)

        invoice = Invoice(len(Customer.order_registry), new_order)

        invoice.generate_invoice()

        print(f"Order placed successfully. Total amount: ${total_amount}")


    def cancel_order(self, order_id):
        order_to_cancel = next(
            (o for o in Customer.order_registry if o.order_id == order_id), None)

        if order_to_cancel and order_to_cancel.status == "Pending":
            for product, quantity in order_to_cancel.products:
                # Revert stock changes
                product.update_stock(quantity)
            Customer.order_registry.remove(order_to_cancel)
            print(f"Order ID {order_id} has been canceled.")

        else:
            print(f"Order ID {order_id} not found or cannot be canceled.")



class Product:
    def __init__(self, product_id, name, category, price, quantity_available, ingredients):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity_available = quantity_available
        self.ingredients = ingredients


    def update_stock(self, quantity):
        """Update the stock of the product by adding the specified quantity."""
        self.quantity_available += quantity
        print(f"Stock for '{self.name}' updated to {self.quantity_available}.")


    def reduce_stock(self, quantity):
        """Reduce the stock of the product by the specified quantity if sufficient stock is available."""
        if self.quantity_available >= quantity:
            self.quantity_available -= quantity
            print(
                f"Stock for '{self.name}' reduced to {self.quantity_available}.")
        else:
            raise ValueError("Insufficient stock available.")


    def get_details(self):
        """Return a string with details of the product."""
        return (f"Product ID: {self.product_id}\n"
                f"Name: {self.name}\n"
                f"Category: {self.category}\n"
                f"Price: ${self.price}\n"
                f"Available Quantity: {self.quantity_available}\n")


    def calculate_cost(self):
        """Calculate the cost of the product based on its ingredients."""
        total_cost = sum(
            ingredient.cost_per_unit for ingredient in self.ingredients)
        return total_cost


    def add_ingredient(self, ingredient):
        """Add a new ingredient to the product."""
        self.ingredients.append(ingredient)
        print(f"Ingredient '{ingredient.name}' added to '{self.name}'.")


    def remove_ingredient(self, ingredient_name):
        # Remove an ingredient from the product by its name

        ingredient_to_remove = next(
            (i for i in self.ingredients if i.name == ingredient_name), None)

        if ingredient_to_remove:
            self.ingredients.remove(ingredient_to_remove)
            print(
                f"Ingredient '{ingredient_name}' removed from '{self.name}'.")

        else:
            print(
                f"Ingredient '{ingredient_name}' not found in '{self.name}'.")


    def update_product(self, name=None, category=None, price=None, quantity_available=None):
        # Update the product's details

        if name:
            self.name = name
        if category:
            self.category = category
        if price is not None:
            self.price = price
        if quantity_available is not None:
            self.quantity_available = quantity_available
        print(f"Product '{self.product_id}' updated successfully.")



class Order:
    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.products = []  # List of tuples (product, quantity)
        self.status = "Pending"


    def add_product(self, product, quantity):
        if quantity <= product.quantity_available:
            product.reduce_stock(quantity)
            self.products.append((product, quantity))
            print(
                f"Added {quantity} of '{product.name}' to order ID {self.order_id}.")

        else:
            print(f"Insufficient stock for product '{product.name}'.")


    def calculate_total(self):
        return sum(product.price * quantity for product, quantity in self.products)


    def complete_order(self):
        self.status = "Completed"
        print(f"Order ID {self.order_id} completed.")


    def cancel_order(self):
        self.status = "Cancelled"

        for product, quantity in self.products:
            product.update_stock(quantity)

        print(f"Order ID {self.order_id} has been canceled.")



class Invoice:
    def __init__(self, invoice_id, order):
        self.invoice_id = invoice_id
        self.order = order

    def generate_invoice(self):
        print(f"---- Invoice ID {self.invoice_id} ----")
        print(f"Order ID: {self.order.order_id}")
        for product, quantity in self.order.products:
            print(
                f"{product.name} | Quantity: {quantity} | Price: ${product.price * quantity}")
        print(f"Total: ${self.order.calculate_total()}")
        print("------------------------------")
