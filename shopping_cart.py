from abc import ABC, abstractmethod

# Prototype design pattern to create a copy of the product
class Product(ABC):
    def __init__(self, name, price, availability):
        self.name = name
        self.price = price
        self.availability = availability

    @abstractmethod
    def clone(self):
        pass

class Laptop(Product):
    def __init__(self, name, price, availability, ram):
        super().__init__(name, price, availability)
        self.ram = ram

    def clone(self):
        return Laptop(self.name, self.price, self.availability, self.ram)

    def __str__(self):
        return f"{self.name} - Rs.{self.price} - {self.availability} - {self.ram}"

class Headphones(Product):
    def __init__(self, name, price, availability, noise_cancelling):
        super().__init__(name, price, availability)
        self.noise_cancelling = noise_cancelling

    def clone(self):
        return Headphones(self.name, self.price, self.availability, self.noise_cancelling)

    def __str__(self):
        return f"{self.name} - Rs.{self.price} - {self.availability} - {self.noise_cancelling}"

class Teabags(Product):
    def __init__(self, name, price, availability, flavour):
        super().__init__(name, price, availability)
        self.flavour = flavour

    def clone(self):
        return Teabags(self.name, self.price, self.availability, self.flavour)

    def __str__(self):
        return f"{self.name} - Rs.{self.price} - {self.availability} - {self.flavour}"

# Strategy design pattern to calculate the discount
class Discount(ABC):
    @abstractmethod
    def apply_discount(self, cart_items):
        pass

class NoDiscount(Discount):
    def apply_discount(self, cart_items):
        # No discount is applied, so return 0.
        return 0

class PercentageDiscount(Discount):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, cart_items):
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        discount_amount = total_price * self.percentage / 100
        for item in cart_items:
            item.subtotal -= discount_amount

class BuyOneGetOneFreeDiscount(Discount):
    def apply_discount(self, cart_items):
        for item in cart_items:
            if item.quantity >= 2:
                discount_amount = (item.product.price * (item.quantity // 2))
                item.subtotal -= discount_amount

# Initializing the shopping cart using a dictionary to store the various items
class ShoppingCart:
    def __init__(self):
        self.cart = {}
        self.discount = NoDiscount()

    def add_to_cart(self, product_info, quantity=1):
        product_name = product_info["name"]
        if product_name in self.cart:
            self.cart[product_name]["quantity"] += quantity
        else:
            self.cart[product_name] = {"product": product_info, "quantity": quantity}

    def remove_from_cart(self, product_info, quantity=1):
        product_name = product_info["name"]
        if product_name in self.cart:
            if self.cart[product_name]["quantity"] <= quantity:
                del self.cart[product_name]
            else:
                self.cart[product_name]["quantity"] -= quantity
        else:
            print(f"{product_name} not found in the cart.")

    def view_cart(self):
        for product_name, cart_item in self.cart.items():
            product_info = cart_item["product"]
            quantity = cart_item["quantity"]
            print(f"You have {quantity} {product_name} in your cart")

    def apply_discount(self, discount):
        self.discount = discount
        self.discount.apply_discount(self.cart.items())

    # def total_price(self):
    #     total_price = sum(product.price * quantity for product, quantity in self.cart.items())
    #     return total_price


    def checkout(self):
        print("Your cart:")
        total_price = 0

        for product_name, cart_item in self.cart.items():
            product_info = cart_item["product"]
            quantity = cart_item["quantity"]
            subtotal = product_info["price"] * quantity
            total_price += subtotal
            print(f"{product_name} - Quantity: {quantity} - Price: Rs.{product_info['price']} - Subtotal: Rs.{subtotal}")

        print(f"Total: Rs.{total_price}")

        self.cart = {}
        self.discount = NoDiscount()
    
    def update_quantity(self, product_info, new_quantity):
        product_name = product_info["name"]
        if product_name in self.cart:
            self.cart[product_name]["quantity"] = new_quantity
        else:
            print(f"{product_name} not found in the cart.")

# Initializing the shopping cart
cart = ShoppingCart()

def main():
    # Create product list
    products = [
        {"name": "Laptop", "price": 10000, "available": True},
        {"name": "Headphones", "price": 500, "available": True},
        {"name": "Teabags", "price": 200, "available": True},
    ]

    # Display available products
    print("Available Products:")
    for idx, product in enumerate(products, start=1):
        availability = "Available" if product["available"] else "Not Available"
        print(f"{idx}. {product['name']} - Rs.{product['price']} - {availability}")

    # Initialize the shopping cart
    cart = ShoppingCart()

    while True:
        print("\nOptions:")
        print("1. Add item to cart")
        print("2. Update item quantity in cart")
        print("3. Remove item from cart")
        print("4. View cart")
        print("5. Checkout")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                item_number = int(input("Enter the product number to add to cart: "))
                quantity = int(input("Enter the quantity: "))
                if 1 <= item_number <= len(products):
                    product = products[item_number - 1]
                    if product["available"]:
                        cart.add_to_cart(product, quantity)
                        print(f"{quantity} {product['name']} added to cart.")
                    else:
                        print(f"{product['name']} is not available.")
                else:
                    print("Invalid product number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "2":
            cart.view_cart()
            try:
                item_number = int(input("Enter the product number to update quantity: "))
                new_quantity = int(input("Enter the new quantity: "))
                if 1 <= item_number <= len(products):
                    product = products[item_number - 1]
                    cart.update_quantity(product, new_quantity)
                    print(f"{product['name']} quantity updated in cart.")
                else:
                    print("Invalid product number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "3":
            cart.view_cart()
            try:
                item_number = int(input("Enter the product number to remove from cart: "))
                if 1 <= item_number <= len(products):
                    product = products[item_number - 1]
                    cart.remove_from_cart(product)
                    print(f"{product['name']} removed from cart.")
                else:
                    print("Invalid product number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "4":
            cart.view_cart()

        elif choice == "5":
            cart.checkout()
            break

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()