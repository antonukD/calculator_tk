import uuid
import math
import json
import tkinter as tk
import hashlib
from tkinter import messagebox, ttk
from datetime import datetime

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def generate_uuid():
    return str(uuid.uuid1())


def generate_current_datetime():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


def show_calculator_window(authorization, username=None):

    root.withdraw()
    file_path_history = 'history_users.json'


    def history_of_user(username):


        def load_history():
            try:
                with open(file_path_history, 'r') as json_file:
                    data = json.load(json_file)
            
                filtered_data = [entry for entry in data if entry.get('user_name') == username]
                return filtered_data
            except FileNotFoundError as e:
                print(e)
                return None
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Error decoding JSON in file")
                print(e)
                return None
            
        history_data = load_history()

        history_window = tk.Toplevel(root)
        history_window.title("History")

        history_listbox = tk.Listbox(history_window, width=50, height=10)
        history_listbox.pack(padx=10, pady=10)
        

        if not history_data:
            history_listbox.insert(tk.END, 'History is empty')
        else:
            for entry in history_data:
                if entry['user_name'] == username:
                    history_listbox.insert(tk.END, f"Time: {entry['date']}\nOperation: {entry['operation']}\n\n")
        history_window.resizable(width=False, height=False)
                    


    def create_user_history(file_path_history, username, operation, result):
        
        try:
            with open(file_path_history, 'r') as json_file:
                data = json.load(json_file)
        except json.JSONDecodeError:
            data = []
        try:
            new_entry = {
                "id": generate_uuid(),
                "date": generate_current_datetime(),
                "operation": f"{operation} = {result}",
                "user_name": username
            }

            data.append(new_entry)

            with open(file_path_history, 'w') as json_file:
                json.dump(data, json_file, indent=2)

        except FileNotFoundError:
            print(f"File {file_path_history} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def trigonometric_functions(button_text, current_text):
        my_string_value = current_text.get()
        if button_text == "SIN":
            try:
                angle_degrees = float(my_string_value)
                angle_radians = math.radians(angle_degrees)
                result = math.sin(angle_radians)
                entry_var.set(result)
            except Exception as e:
                entry_var.set("Error")
                print(e)
        elif button_text == "COT":
            try:
                angle_degrees = float(my_string_value)
                angle_radians = math.radians(angle_degrees)
                tangent_result = math.tan(angle_radians)
                
                result = 1 / tangent_result if tangent_result != 0 else "Error: Cotangent is undefined for this angle"
                entry_var.set(result)
            except Exception as e:
                entry_var.set("Error")
                print(e)

        elif button_text == "TAN":
            try:
                angle_degrees = float(my_string_value)
                angle_radians = math.radians(angle_degrees)
                result = math.tan(angle_radians)
                entry_var.set(result)
            except Exception as e:
                entry_var.set("Error")
                print(e)
        else:
            entry_var.set(my_string_value + button_text)
        try:  
            operation_text = f'{button_text} {my_string_value}'
            create_user_history(file_path_history, username, operation_text, result)
        except Exception as e:
            print(e)
    

    def on_click(button_text, authorization=False):
            
        current_text = entry_var.get()

        if button_text == " = ":
            try:
                result = eval(current_text)
                entry_var.set(result)
                if current_text == str(result):
                    return None
                elif authorization:
                    create_user_history(file_path_history, username, current_text, result)
            except Exception as e:
                entry_var.set("Error")
        elif button_text == "C":
            entry_var.set("")
        else:
            entry_var.set(current_text + button_text)


    calculator_window = tk.Toplevel(root)
    calculator_window.title("Calculator")
    entry_var = tk.StringVar()
    entry_var.set("")

    entry = tk.Entry(calculator_window, textvariable=entry_var, font=("Arial", 14), justify="right")
    entry.grid(row=0, column=0, columnspan=4, sticky='nsew' )

    buttons = [
        '7', '8', '9', ' + ',
        '4', '5', '6', ' / ',
        '1', '2', '3', ' * ',
        '0', '.', ' = ', ' - ',
    ]

    row_val = 1
    col_val = 0

    if authorization == True: 
        # buttons[:0] = ['TAN', 'COT', 'SIN', 'C']
        row_val += 1
        tun_button = tk.Button(calculator_window, padx=20, pady=20, text="TAN", command=lambda: trigonometric_functions("TAN", entry_var), font=("Arial", 16))
        tun_button.grid(row=1, column=0, columnspan=1, sticky="nsew")
        cot_button = tk.Button(calculator_window, padx=20, pady=20, text="COT", command=lambda: trigonometric_functions("COT", entry_var), font=("Arial", 16))
        cot_button.grid(row=1, column=1, columnspan=1, sticky="nsew")
        sin_button = tk.Button(calculator_window, padx=20, pady=20, text="SIN", command=lambda: trigonometric_functions("SIN", entry_var), font=("Arial", 16))
        sin_button.grid(row=1, column=2, columnspan=1, sticky="nsew")
        c_button = tk.Button(calculator_window, padx=20, pady=20, text="C", command=lambda: on_click("C", entry_var), font=("Arial", 16))
        c_button.grid(row=1, column=3, columnspan=1, sticky="nsew")

        history_button = tk.Button(calculator_window, padx=20, pady=20, text="History", command=lambda: history_of_user(username), font=("Arial", 16))
        history_button.grid(row=6, column=0, columnspan=4, sticky="nsew")
       
    else:
        clear_button = tk.Button(calculator_window, padx=20, pady=20, text="C", command=lambda text="C": on_click("C"), font=("Arial", 16))
        clear_button.grid(row=6, column=0, columnspan=4, sticky="nsew")

    

    for button_text in buttons:
        tk.Button(calculator_window, text=button_text, padx=20, pady=20, font=("Arial", 16),
                  command=lambda text=button_text: on_click(text, authorization)).grid(row=row_val, column=col_val, sticky='nesw') 
        col_val += 1
        if col_val > 3:
            col_val = 0
            row_val += 1

    center_window(calculator_window)
    calculator_window.resizable(width=False, height=False)
    calculator_window.protocol("WM_DELETE_WINDOW", main_destroy)


def main_destroy():
    root.destroy()
    

def register():
    username = entry_name.get()
    password = entry_password.get()

    user_manager = UserManager()
    registration_result, message = user_manager.registration(username, password)

    print(registration_result, message)

    if registration_result:
        messagebox.showinfo('Success', message)
    else:
        messagebox.showinfo('Error', message)


def authenticate():
    username = entry_name.get()
    password = entry_password.get()

    user_manager = UserManager()
    authorization_result, message = user_manager.authorization(username, password)
    print(authorization_result, message)

    if authorization_result:
        show_calculator_window(authorization_result, username) 
    else:
        messagebox.showerror('Error', message)
        pass


class EmptyUser(Exception):
    def __init__(self, message="Your story is empty"):
        self.message = message
        super().__init__(self.message)


class UserManager:
    def __init__(self, file_path='users.json'):
        self.file_path = file_path
        self.registration_data = self.load_registration_data()

    def load_registration_data(self):
        try:
            with open(self.file_path, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}

    def save_registration_data(self):
        json_data = json.dumps(self.registration_data, indent=2)
        with open(self.file_path, 'w') as json_file:
            json_file.write(json_data)

    
    def registration(self, user_name, user_password):
        try:
            name = user_name
            password = user_password
            
            if name in self.registration_data or password in self.registration_data:
                return False, "User already registered!"
            else:
                if len(password) > 8 or password[0].isupper():
                    hashed_password = self.hash_password(password)
                    self.registration_data[name] = hashed_password
                    self.save_registration_data()
                    return True, "Registration successful, please authorize!"
                else:
                    return False, 'The password must begin with a capital letter and be at least 8 characters long!'
        except Exception as e:
            return False, f"An error occurred: {e}"

    def authorization(self, user_name, user_password):
        try:
            name = user_name
            password = user_password
            if name in self.registration_data and self.check_password(name, password):
                return  True, 'Authorization successful!'
            else:
                return False, 'User is not registered or incorrect password!'
        except Exception as e:
            return False, f"An error occurred: {e}"

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, user_name, password):
        hashed_password = self.registration_data.get(user_name)
        if hashed_password:
            return hashed_password == self.hash_password(password)
        return False

    def get_authenticated_user(self, name):
        if name in self.registration_data:
            return AuthorizedUser(name)
        else:
            return None


class AuthorizedUser:
    pass


root = tk.Tk()
center_window(root)
root.title("Calculator")
root.geometry('400x110')


for i in range(4):
    root.grid_rowconfigure(i, weight=1)

for i in range(4):
    root.grid_columnconfigure(i, weight=1)


label_name = tk.Label(root, text="Name:")
label_name.grid(row=0, column=0, columnspan=1, sticky="w")

entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, columnspan=3, sticky="nsew")

label_password = tk.Label(root, text="Password:")
label_password.grid(row=1, column=0, columnspan=1, sticky="w")

entry_password = tk.Entry(root, width=30)
entry_password.grid(row=1, column=1, columnspan=3, sticky="nsew")


authorization_button = tk.Button(root, text="Authorization", command=authenticate)
authorization_button.grid(row=2, column=0, columnspan=2, sticky="nsew")

registration_button = tk.Button(root, text="Registration", command=register)
registration_button.grid(row=2, column=2, columnspan=2, sticky="nsew")

guest_button = tk.Button(root, text="Guest", command=lambda: show_calculator_window(None))
guest_button.grid(row=3, column=0, columnspan=4, sticky="nsew")


root.mainloop()
