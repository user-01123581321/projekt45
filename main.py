from tkinter import *
from tkinter import simpledialog
from PIL import Image, ImageTk

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = 'admin'

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = 'customer'

class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery App")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#f0f0f0")
        self.current_user = None
        self.food_items = self.load_data('data.txt')
        self.message_frame = None
        self.create_login_frame()

    def show_message(self, message, color="#FFC107"):

        if self.message_frame:
            self.message_frame.destroy()

        # Create new message frame
        self.message_frame = Frame(self.root, bg=color)
        self.message_frame.pack(pady=10, fill=X)
        self.message_frame.lift()

        # Add label with the message
        Label(self.message_frame, text=message, bg=color, font=("Arial", 12)).pack(pady=5)

        # Force update UI
        self.root.update_idletasks()

    def create_login_frame(self):
        if self.message_frame:
            self.message_frame.destroy()
        self.login_frame = Frame(self.root, bg="#f0f0f0")
        self.login_frame.pack(fill=BOTH, expand=True, pady=20)

        self.background_image = PhotoImage(file=r"image/back.png")
        self.background_label = Label(self.login_frame, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        Label(self.login_frame, text="Username", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.username_entry = Entry(self.login_frame, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        Label(self.login_frame, text="Password", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.password_entry = Entry(self.login_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        Button(self.login_frame, text="Login", command=self.login, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=5)
        Button(self.login_frame, text="Register", command=self.create_register_frame, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=5)

    def create_register_frame(self):
        if self.message_frame:
            self.message_frame.destroy()
        self.login_frame.destroy()
        self.register_frame = Frame(self.root, bg="#f0f0f0")
        self.register_frame.pack(pady=20)
        Label(self.register_frame, text="Username", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.reg_username_entry = Entry(self.register_frame, font=("Arial", 12))
        self.reg_username_entry.pack(pady=5)
        Label(self.register_frame, text="Password", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.reg_password_entry = Entry(self.register_frame, show="*", font=("Arial", 12))
        self.reg_password_entry.pack(pady=5)
        Label(self.register_frame, text="Role (admin/customer)", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.reg_role_entry = Entry(self.register_frame, font=("Arial", 12))
        self.reg_role_entry.pack(pady=5)
        Button(self.register_frame, text="Register", command=self.register, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=5)
        Button(self.register_frame, text="Back to Login", command=self.back_to_login, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=5)

    def back_to_login(self):
        if self.message_frame:
            self.message_frame.destroy()
        self.register_frame.destroy()
        self.create_login_frame()

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_entry.get()


        min_password_length = 8
        max_password_length = 20

        if username == "" or password == "" or role not in ['admin', 'customer']:
            self.show_message("Invalid username, password, or role", "red")
            return

        if len(password) < min_password_length or len(password) > max_password_length:
            self.show_message(f"Password must be between {min_password_length} and {max_password_length} characters", "red")
            return

        with open('users.txt', 'a') as file:
            file.write(f"{username},{password},{role}\n")
        self.show_message("User registered successfully", "green")
        self.back_to_login()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "" or password == "":
            self.show_message("Please fill in all fields", "red")
            return
        user = self.authenticate(username, password)
        if user:
            self.current_user = user
            self.login_frame.destroy()
            self.create_main_frame()
        else:
            self.show_message("Invalid username or password", "red")

    def authenticate(self, username, password):
        with open('users.txt', 'r') as file:
            users = file.readlines()
        for line in users:
            u, p, r = line.strip().split(',')
            if u == username and p == password:
                if r == 'admin':
                    return Admin(username, password)
                elif r == 'customer':
                    return Customer(username, password)
        return None

    def create_main_frame(self):
        if self.message_frame:
            self.message_frame.destroy()

        # Create the main frame
        self.main_frame = Frame(self.root, bg="#f4f4f4")
        self.main_frame.pack(fill=BOTH, expand=True, pady=20)

        # Add background image
        self.user_background_image = PhotoImage(file="image/file.png")  # Specify the path to your image
        self.user_background_label = Label(self.main_frame, image=self.user_background_image)
        self.user_background_label.place(relwidth=1, relheight=1)

        # Add title and other widgets based on user role
        if self.current_user.role == 'customer':
            self.title_label = Label(self.main_frame, text="Click to select food", fg="blue",
                                     font=("Arial", 16, "bold"))
            self.title_label.place(x=20, y=20)  # Position in pixels from top-left corner
            self.main_frame.configure(bg="orange")
            Button(self.main_frame, text="Order", command=self.place_order, font=("Arial", 12), bg="#4CAF50",
                   fg="white").place(x=20, y=380)

        Label(self.main_frame, text=f"Welcome {self.current_user.username}", fg="green",
              font=("Arial", 16)).place(x=20, y=60)

        if self.current_user.role == 'admin':
            # Arrange the buttons in a column
            Button(self.main_frame, text="Show Food Items", command=self.show_food_items, font=("Arial", 12),
                   bg="#2196F3", fg="white").place(x=20, y=100)
            Button(self.main_frame, text="Add Food Item", command=self.add_food_item, font=("Arial", 12), bg="#4CAF50",
                   fg="white").place(x=20, y=140)
            Button(self.main_frame, text="Delete Food Item", command=self.delete_food_item, font=("Arial", 12),
                   bg="#f44336", fg="white").place(x=20, y=180)
            Button(self.main_frame, text="Edit Food Item", command=self.edit_food_item, font=("Arial", 12),
                   bg="#FFC107", fg="white").place(x=20, y=220)
            Button(self.main_frame, text="Search Food Item", command=self.search_food_item, font=("Arial", 12),
                   bg="#9C27B0", fg="white").place(x=20, y=260)
            Button(self.main_frame, text="Sort Food Items", command=self.sort_food_items, font=("Arial", 12),
                   bg="#3F51B5", fg="white").place(x=20, y=300)

        # Add Listbox for displaying food items
        self.food_listbox = Listbox(self.main_frame, bg="#ffffff", font=("Arial", 12), width=50, height=15)
        self.food_listbox.place(x=200, y=70)

        # Add 'Back' button to return to the login screen
        Button(self.main_frame, text="Logout", command=self.logout, font=("Arial", 12), bg="#FF5722", fg="white").place(
            x=20, y=440)

        self.update_food_list()

    def update_food_list(self):
        self.food_listbox.delete(0, END)
        for item in self.food_items:
            self.food_listbox.insert(END, item)

    def show_food_items(self):
        self.update_food_list()

    def add_food_item(self):
        name = simpledialog.askstring("Add Food Item", "Enter food item name:")
        if name:
            price = simpledialog.askfloat("Add Food Item", "Enter food item price:")
            quantity = simpledialog.askinteger("Add Food Item", "Enter food item quantity:")
            if price is not None and quantity is not None:
                self.food_items.append(f"{name} - ${price} - Quantity: {quantity}")
                self.save_data('data.txt', self.food_items)
                self.update_food_list()
                self.show_message("Food item added successfully", "green")
            else:
                self.show_message("Invalid price or quantity", "red")

    def delete_food_item(self):
        selected_item = self.food_listbox.get(ACTIVE)
        if selected_item:
            self.food_items.remove(selected_item)
            self.save_data('data.txt', self.food_items)
            self.update_food_list()
            self.show_message("Food item deleted successfully", "green")
        else:
            self.show_message("No food item selected", "red")

    def edit_food_item(self):
        selected_item = self.food_listbox.get(ACTIVE)
        if selected_item:
            new_name = simpledialog.askstring("Edit Food Item", "Enter new food item name:", initialvalue=selected_item.split(' - ')[0])
            if new_name:
                new_price = simpledialog.askfloat("Edit Food Item", "Enter new food item price:")
                new_quantity = simpledialog.askinteger("Edit Food Item", "Enter new food item quantity:")
                if new_price is not None and new_quantity is not None:
                    index = self.food_items.index(selected_item)
                    self.food_items[index] = f"{new_name} - ${new_price} - Quantity: {new_quantity}"
                    self.save_data('data.txt', self.food_items)
                    self.update_food_list()
                    self.show_message("Food item updated successfully", "green")
                else:
                    self.show_message("Invalid price or quantity", "red")
        else:
            self.show_message("No food item selected", "red")

    def search_food_item(self):
        query = simpledialog.askstring("Search Food Item", "Enter food item name:")
        if query:
            found_items = [item for item in self.food_items if query.lower() in item.lower()]
            if found_items:
                self.food_listbox.delete(0, END)
                for item in found_items:
                    self.food_listbox.insert(END, item)
                self.show_message("Search completed", "green")
            else:
                self.show_message("No items found", "red")

    def sort_food_items(self):
        self.food_items.sort(key=lambda x: (x.lower()))
        self.save_data('data.txt', self.food_items)
        self.update_food_list()
        self.show_message("Food items sorted", "green")

    def save_data(self, filename, data):
        with open(filename, 'w') as file:
            for item in data:
                file.write(f"{item}\n")

    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []

    def place_order(self):
        selected_item = self.food_listbox.get(ACTIVE)
        if selected_item:
            quantity = simpledialog.askinteger("Place Order", "Enter quantity:")
            if quantity:
                self.show_message(f"Order placed for {quantity} of {selected_item}", "green")
            else:
                self.show_message("Invalid quantity", "red")
        else:
            self.show_message("No food item selected", "red")

    def logout(self):
        self.main_frame.destroy()
        self.create_login_frame()


root = Tk()
app = FoodDeliveryApp(root)
root.mainloop()
