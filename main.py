from operation import Admin,Customer,Product,Order


def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("---- Bakery Management System ----")
        print("1. Register Admin")
        print("2. Login Admin")
        print("3. Register Customer")
        print("4. Login Customer")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_admin()
        elif choice == '2':
            login_admin()
        elif choice == '3':
            register_customer()
        elif choice == '4':
            login_customer()
        elif choice == '5':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

def register_admin():
    """Handles admin registration."""
    admin_id = int(input("Enter Admin ID: "))
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    name = input("Enter Name: ")
    contact_details = input("Enter Contact Details: ")
    try:
        Admin.register_admin(admin_id, username, password, name, contact_details)
        print("Admin registered successfully.")
    except ValueError as e:
        print(e)

def login_admin():
    """Handles admin login."""
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    if Admin.validate_admin(username, password):
        print("Login successful.")
        admin_menu(username)
    else:
        print("Invalid username or password.")

def register_customer():
    """Handles customer registration."""
    customer_id = int(input("Enter Customer ID: "))
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    name = input("Enter Name: ")
    contact_details = input("Enter Contact Details: ")
    try:
        Customer.register_customer(customer_id, username, password, name, contact_details)
        print("Customer registered successfully.")
    except ValueError as e:
        print(e)

def login_customer():
    """Handles customer login."""
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    customer = Customer.login_customer(username, password)
    if customer:
        print("Login successful.")
        customer_menu(customer)
    else:
        print("Invalid username or password.")

def admin_menu(username):
    """Displays the admin menu and handles admin operations."""
    while True:
        print("\n---- Admin Menu ----")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Update Product")
        print("4. View All Products")
        print("5. View Bakery Details")
        print("6. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            remove_product()
        elif choice == '3':
            update_product()
        elif choice == '4':
            Admin.view_all_products()
        elif choice == '5':
            Admin.view_bakery_details(Customer.order_registry)
        elif choice == '6':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")

def add_product():
    """Handles product addition."""
    product_id = int(input("Enter Product ID: "))
    name = input("Enter Product Name: ")
    category = input("Enter Product Category: ")
    price = float(input("Enter Product Price: "))
    quantity_available = int(input("Enter Quantity Available: "))
    ingredients = []
    Admin.product_catalog.append(Product(product_id, name, category, price, quantity_available, ingredients))
    print("Product added successfully.")

def remove_product():
    """Handles product removal."""
    product_id = int(input("Enter Product ID to remove: "))
    Admin().remove_product(product_id)

def update_product():
    """Handles product update."""
    product_id = int(input("Enter Product ID to update: "))
    name = input("Enter new Product Name (leave empty to keep current): ")
    category = input("Enter new Product Category (leave empty to keep current): ")
    price = input("Enter new Product Price (leave empty to keep current): ")
    quantity_available = input("Enter new Quantity Available (leave empty to keep current): ")
    ingredients = [] 
    Admin().update_product(
        product_id,
        name=name if name else None,
        category=category if category else None,
        price=float(price) if price else None,
        quantity_available=int(quantity_available) if quantity_available else None,
        ingredients=ingredients
    )


def customer_menu(customer):
    """Displays the customer menu and handles customer operations."""
    while True:
        print("\n---- Customer Menu ----")
        print("1. View Products")
        print("2. Add Product to Cart")
        print("3. Purchase Cart")
        print("4. Cancel Order")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            customer.view_products()
        elif choice == '2':
            add_to_cart(customer)
        elif choice == '3':
            customer.purchase_cart()
        elif choice == '4':
            cancel_order(customer)
        elif choice == '5':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")

def add_to_cart(customer):
    """Handles adding products to the cart."""
    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Quantity: "))
    customer.add_to_cart(product_id, quantity)

def cancel_order(customer):
    """Handles canceling an order."""
    order_id = int(input("Enter Order ID to cancel: "))
    customer.cancel_order(order_id)

# Run the main menu
if __name__ == "__main__":
    main_menu()
