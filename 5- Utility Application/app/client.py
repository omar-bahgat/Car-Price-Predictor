import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sv_ttk

import requests
import json


root = tk.Tk()
root.geometry("1200x750")  
root.title("ML-Spring 2024 Project") 

#---------------------------------------------------------------------------------------------------------------------------------------

# Theme

def toggle_theme():
    if sv_ttk.get_theme() == "dark":
        sv_ttk.use_light_theme()
    else:
        sv_ttk.use_dark_theme()

style = ttk.Style()
style.configure("On.TButton", background="#4CAF50", foreground="white")
style.configure("Off.TButton", background="#ccc", foreground="black")

sv_ttk.set_theme("dark")

theme_button = ttk.Checkbutton(root, text="Theme", command=toggle_theme, style="On.TButton")
theme_button.place(relx=0.066, rely=0.93, anchor='center')  

#---------------------------------------------------------------------------------------------------------------------------------------

# File handling 

def upload_file():
    filename = filedialog.askopenfilename()

upload_button = ttk.Button(root, text="Upload Car Info", command=upload_file)
upload_button.place(relx=0.93, rely=0.93, anchor='center')

#---------------------------------------------------------------------------------------------------------------------------------------

# Heading

heading = ttk.Label(root, text="Used Car Price Predictor", font=("Arial", 18, "bold"))
heading.place(relx=0.5, rely=0.035, anchor="center")

line = tk.Canvas(root, width=1220, height=1, bg="white", highlightthickness=0)
line.place(relx=0.5, rely=0.07, anchor="center")

#--------------------------------------------------------------FIRST-ROW--------------------------------------------------------------

def validate_range(new_value, min_value, max_value):
    if new_value == "":
        return True
    
    if not new_value[0].isdigit() or new_value[0] == '0':
        return False
    
    try:
        value = int(new_value)
        return min_value <= value <= max_value
    except ValueError:
        return False

# Car Manufacturer

label = ttk.Label(root, text="Car Manufacturer", font=("Arial", 12, "bold"))
label.place(relx=0.15, rely=0.12, anchor="center")  

manufacturer_value = tk.StringVar()
manufacturer_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=manufacturer_value, 
    values=['-- Select --', 'Acura', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 
    'Chrysler', 'Dodge', 'Ford', 'GMC', 'Honda', 'Hyundai', 'INFINITI', 'Jaguar', 
    'Jeep', 'Kia', 'Land Rover', 'Lexus', 'Lincoln', 'Mazda', 'Mercedes-Benz', 
    'Mitsubishi', 'Nissan', 'Porsche', 'RAM',  'Subaru', 'Tesla', 'Toyota', 
    'Volkswagen', 'Volvo', 'Other'],
    width=15, state="readonly", )

manufacturer_menu.current(0) 
manufacturer_menu.place(relx=0.15, rely=0.16, anchor="center")  
manufacturer_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear())  

# Car Model

label = ttk.Label(root, text="Car Model", font=("Arial", 12, "bold"))
label.place(relx=0.325, rely=0.12, anchor="center")  

model_value = tk.StringVar()

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=model_value)
input_field.place(relx=0.325, rely=0.16, anchor="center")  

# Year Produced

label = ttk.Label(root, text="Year Produced", font=("Arial", 12, "bold"))
label.place(relx=0.5, rely=0.12, anchor="center")  

year_value = tk.StringVar()

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=year_value,  validate="key", 
    validatecommand=(root.register(lambda new_value: validate_range(new_value, 0, 2024)), "%P"))

input_field.place(relx=0.5, rely=0.16, anchor="center") 

# Mileage

label = ttk.Label(root, text="Mileage", font=("Arial", 12, "bold"))
label.place(relx=0.675, rely=0.12, anchor="center")  

mileage_value = tk.StringVar()

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=mileage_value,  validate="key", 
    validatecommand=(root.register(lambda new_value: validate_range(new_value, 0, 999999)), "%P"))
    
input_field.place(relx=0.675, rely=0.16, anchor="center") 

# MPG

label = ttk.Label(root, text="MPG", font=("Arial", 12, "bold"))
label.place(relx=0.85, rely=0.12, anchor="center")  

mpg_value = tk.StringVar()

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=mpg_value,  validate="key", 
    validatecommand=(root.register(lambda new_value: validate_range(new_value, 0, 100)), "%P"))

input_field.place(relx=0.85, rely=0.16, anchor="center") 

#--------------------------------------------------------------SECOND-ROW--------------------------------------------------------------

# Transmission

label = ttk.Label(root, text="Transmission", font=("Arial", 12, "bold"))
label.place(relx=0.15, rely=0.25, anchor="center")  

transmission_value = tk.StringVar()

transmission_value = tk.StringVar()
transmission_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=transmission_value, 
    values=['-- Select --', 'Automatic', 'Semi-Automatic', 'Manual', 'Dual Clutch', 'Other'],
    width=15, state="readonly", )

transmission_menu.current(0) 
transmission_menu.place(relx=0.15, rely=0.29, anchor="center")  
transmission_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear())  

# Cylinders

label = ttk.Label(root, text="Number of Cylinders", font=("Arial", 12, "bold"))
label.place(relx=0.325, rely=0.25, anchor="center")  

cylinders_value = tk.StringVar()

cylinders_value = tk.StringVar()
cylinders_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=cylinders_value, 
    values=['-- Select --', '2', '3', '4', '5', '6', 'Other'],
    width=15, state="readonly", )

cylinders_menu.current(0) 
cylinders_menu.place(relx=0.325, rely=0.29, anchor="center")  
cylinders_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear()) 

# Injection Type

label = ttk.Label(root, text="Injection Type", font=("Arial", 12, "bold"))
label.place(relx=0.5, rely=0.25, anchor="center")  

injection_type_value = tk.StringVar()
injection_type_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=injection_type_value, 
    values=['-- Select --', 'DI', 'FSI', 'GDI', 'MPFI', 'PGM-FI', 'SIDI', 'SPFI', 'TFSI','Other'],
    width=15, state="readonly", )

injection_type_menu.current(0) 
injection_type_menu.place(relx=0.5, rely=0.29, anchor="center")  
injection_type_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear()) 

# Horsepower

label = ttk.Label(root, text="Horsepower", font=("Arial", 12, "bold"))
label.place(relx=0.675, rely=0.25, anchor="center")  

horsepower_value = tk.StringVar()

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=horsepower_value,  validate="key", 
    validatecommand=(root.register(lambda new_value: validate_range(new_value, 0, 999)), "%P"))

input_field.place(relx=0.675, rely=0.29, anchor="center") 

# Turbo

style = ttk.Style()
style.configure("Custom.TRadiobutton", font=("Arial", 12))

label = ttk.Label(root, text="Turbo", font=("Arial", 12, "bold"))
label.place(relx = 0.85, rely=0.25, anchor="center")  

turbo_value = tk.StringVar(value="0")

yes_radio = ttk.Radiobutton(root, text="Yes", variable=turbo_value, value="1", style="Custom.TRadiobutton")
yes_radio.place(relx=0.81, rely=0.29, anchor="center")  

no_radio = ttk.Radiobutton(root, text="No", variable=turbo_value, value="0", style="Custom.TRadiobutton")
no_radio.place(relx=0.89, rely=0.29, anchor="center")  

#--------------------------------------------------------------THIRD-ROW--------------------------------------------------------------

# Drivetrain

label = ttk.Label(root, text="Drivetrain", font=("Arial", 12, "bold"))
label.place(relx=0.15, rely=0.38, anchor="center")  

drivetrain_value = tk.StringVar()
drivetrain_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=drivetrain_value, 
    values=['-- Select --', 'All-Wheel Drive', 'Four-Wheel Drive',  'Front-Wheel Drive', 'Rear-Wheel Drive', 'Other'],
    width=15, state="readonly", )

drivetrain_menu.current(0) 
drivetrain_menu.place(relx=0.15, rely=0.42, anchor="center")  
drivetrain_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear()) 

# Fuel-type

label = ttk.Label(root, text="Fuel-type", font=("Arial", 12, "bold"))
label.place(relx=0.325, rely=0.38, anchor="center")  

fuel_type_value = tk.StringVar()
fuel_type_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=fuel_type_value, 
    values=['-- Select --', 'Gasoline', 'Diesel', 'Electric', 'Hybrid', 'Other'],
    width=15, state="readonly", )

fuel_type_menu.current(0) 
fuel_type_menu.place(relx=0.325, rely=0.42, anchor="center")  
fuel_type_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear()) 

# Exterior Color

label = ttk.Label(root, text="Exterior Color", font=("Arial", 12, "bold"))
label.place(relx=0.5, rely=0.38, anchor="center")  

exterior_color_value = tk.StringVar()
exterior_color_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=exterior_color_value, 
    values=['-- Select --', 'Black', 'Blue', 'Clearcoat', 'Crystal', 'Gray', 'Metallic', 'Pearl', 'Red', 'Silver', 'white' 'Other'],
    width=15, state="readonly", )

exterior_color_menu.current(0) 
exterior_color_menu.place(relx=0.5, rely=0.42, anchor="center")  
exterior_color_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear()) 

# Interior Color

label = ttk.Label(root, text="Interior Color", font=("Arial", 12, "bold"))
label.place(relx=0.675, rely=0.38, anchor="center")  

interior_color_value = tk.StringVar()
interior_color_menu = ttk.Combobox(root, font=("Arial", 12), textvariable=interior_color_value, 
    values=['-- Select --', 'Beige', 'Black', 'Charcoal', 'Dark', 'Ebony', 'Graphite', 'Gray', 'Jet', 'Light', 'Other'],
    width=15, state="readonly", )

interior_color_menu.current(0) 
interior_color_menu.place(relx=0.675, rely=0.42, anchor="center")  
interior_color_menu.bind("<FocusIn>", lambda event: event.widget.selection_clear()) 

# Seller Rating

def validate_rating(rating):
    if rating == "":
        return True    
    try:
        value = float(rating)
        if 1 <= value <= 5:
            decimal_part = rating.split('.')[1] if '.' in rating else ''
            return len(decimal_part) <= 1
        else:
            return False
    except ValueError:
        return False


def increase_rating(rating):
    current_rating = float(rating.get())
    new_rating = min(current_rating + 0.1, 5)
    rating.set("{:.1f}".format(new_rating))

def decrease_rating(rating):
    current_rating = float(rating.get())
    new_rating = max(current_rating - 0.1, 1)
    rating.set("{:.1f}".format(new_rating))


seller_rating_value = tk.StringVar()
seller_rating_value.set("1.0")

label = ttk.Label(root, text="Seller Rating", font=("Arial", 12, "bold"))
label.place(relx=0.85, rely=0.38, anchor="center")

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=seller_rating_value, validate="key", validatecommand=(root.register(validate_rating), "%P"))
input_field.place(relx=0.85, rely=0.42, anchor="center")

up_button = ttk.Label(root, text="▲", font=("Arial", 9))
up_button.place(relx=0.912, rely=0.41, anchor="center")
up_button.bind("<Button-1>", lambda event: increase_rating(seller_rating_value))

down_button = ttk.Label(root, text="▼", font=("Arial", 9))
down_button.place(relx=0.912, rely=0.43, anchor="center")
down_button.bind("<Button-1>", lambda event: decrease_rating(seller_rating_value))

#--------------------------------------------------------------FOURTH-ROW--------------------------------------------------------------

# Driver Rating 

driver_rating_value = tk.StringVar()
driver_rating_value.set("1.0")

label = ttk.Label(root, text="Driver Rating", font=("Arial", 12, "bold"))
label.place(relx=0.15, rely=0.51, anchor="center")

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=driver_rating_value, validate="key", validatecommand=(root.register(validate_rating), "%P"))
input_field.place(relx=0.15, rely=0.55, anchor="center")

up_button = ttk.Label(root, text="▲", font=("Arial", 9))
up_button.place(relx=0.212, rely=0.54, anchor="center")
up_button.bind("<Button-1>", lambda event: increase_rating(driver_rating_value))

down_button = ttk.Label(root, text="▼", font=("Arial", 9))
down_button.place(relx=0.212, rely=0.56, anchor="center")
down_button.bind("<Button-1>", lambda event: decrease_rating(driver_rating_value))

# Driver Reviews Num

label = ttk.Label(root, text="Driver Reviews Num", font=("Arial", 12, "bold"))
label.place(relx=0.325, rely=0.51, anchor="center")  

driver_reviews_num_value = tk.StringVar()

input_field = ttk.Entry(root, font=("Arial", 12), textvariable=driver_reviews_num_value,  validate="key", 
    validatecommand=(root.register(lambda new_value: validate_range(new_value, 0, 10000)), "%P"))

input_field.place(relx=0.325, rely=0.55, anchor="center") 

# Accidents

style = ttk.Style()
style.configure("Custom.TRadiobutton", font=("Arial", 12))

label = ttk.Label(root, text="Accidents", font=("Arial", 12, "bold"))
label.place(relx = 0.5, rely=0.51, anchor="center")  

accidents_value = tk.StringVar(value="0.0")

yes_radio = ttk.Radiobutton(root, text="Yes", variable=accidents_value, value="1.0", style="Custom.TRadiobutton")
yes_radio.place(relx=0.46, rely=0.55, anchor="center")  

no_radio = ttk.Radiobutton(root, text="No", variable=accidents_value, value="0.0", style="Custom.TRadiobutton")
no_radio.place(relx=0.54, rely=0.55, anchor="center")  

# One Owner

label = ttk.Label(root, text="One Owner", font=("Arial", 12, "bold"))
label.place(relx = 0.675, rely=0.51, anchor="center")  

one_owner_value = tk.StringVar(value="1.0")

yes_radio = ttk.Radiobutton(root, text="Yes", variable=one_owner_value, value="1.0", style="Custom.TRadiobutton")
yes_radio.place(relx=0.635, rely=0.55, anchor="center")  

no_radio = ttk.Radiobutton(root, text="No", variable=one_owner_value, value="0.0", style="Custom.TRadiobutton")
no_radio.place(relx=0.715, rely=0.55, anchor="center")  

# Personal Use

label = ttk.Label(root, text="Personal Use Only", font=("Arial", 12, "bold"))
label.place(relx = 0.85, rely=0.51, anchor="center")  

personal_use_value = tk.StringVar(value="1.0")

yes_radio = ttk.Radiobutton(root, text="Yes", variable=personal_use_value, value="1.0", style="Custom.TRadiobutton")
yes_radio.place(relx=0.81, rely=0.55, anchor="center")  

no_radio = ttk.Radiobutton(root, text="No", variable=personal_use_value, value="0.0", style="Custom.TRadiobutton")
no_radio.place(relx=0.89, rely=0.55, anchor="center")  

#---------------------------------------------------------------------------------------------------------------------------------------

# Online Learning

line = tk.Canvas(root, width=1000, height=1, bg="white", highlightthickness=0)
line.place(relx=0.5, rely=0.75, anchor="center")



#---------------------------------------------------------------------------------------------------------------------------------------

user_features_test = ['Toyota', 'Yaris', '2010', '30000', '40', 
                      'Automatic', '4', 'Other', '150', '0',
                      'Front-Wheel Drive', 'Gasoline', 'Black', 'Black', '4.0',
                      '4.0', '50', '0.0', '1.0', '1.0']

user_features_test2 = ['Toyota', 'Yaris', '2010', '30000', '40', 
                      'Automatic', '4', 'Other', '150', '0',
                      'Front-Wheel Drive', 'Gasoline', 'Black', 'Black', '4.0',
                      '4.0', '50', '0.0', '1.0', '1.0', "20000"]

def validate(type):

    manufacturer = manufacturer_value.get()
    model = model_value.get()
    year = year_value.get()
    mileage = mileage_value.get()
    mpg = mpg_value.get()

    transmission = transmission_value.get()
    cylinders = cylinders_value.get()
    injection_type = injection_type_value.get()
    horsepower = horsepower_value.get()
    turbo = turbo_value.get()

    drivetrain = drivetrain_value.get()
    fuel_type = fuel_type_value.get()
    exterior_color = exterior_color_value.get()
    interior_color = interior_color_value.get()
    seller_rating = seller_rating_value.get()

    driver_rating = driver_rating_value.get()
    driver_reviews_num = driver_reviews_num_value.get()
    accidents = accidents_value.get()
    one_owner = one_owner_value.get()
    personal_use = personal_use_value.get()

    actual_price = retrain_value.get()

 
    user_features = [
        manufacturer, model, year, mileage, mpg, 
        transmission, cylinders, injection_type, horsepower, turbo,
        drivetrain, fuel_type, exterior_color, interior_color, seller_rating,
        driver_rating, driver_reviews_num, accidents, one_owner, personal_use
    ]

    for feature in user_features:
        if feature == "" or feature == "-- Select --":
            pred_error_label.config(text="Please fill in all fields", foreground="red")
            return None
    pred_error_label.config(text="")

    if type == "retrain":
        if actual_price == "":
            retrain_error_label.config(text="Enter Car Price", foreground="red")
            return None
        else:
            user_features.append(actual_price)
    retrain_error_label.config(text="")

    return user_features

#---------------------------------------------------------------------------------------------------------------------------------------

def prediction_request():
    user_features = validate("predict")
    if user_features is not None:   

        url = 'http://localhost:5500'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=json.dumps(user_features))

        if response.status_code == 200:
            response = response.json()
            predicted_price = response['predicted_price']
            predicted_price = round(float(predicted_price), 2)
            predicted_value.set("$ " + str(predicted_price))
        else:
            print("Error:", response.status_code)


predict_button = ttk.Button(root, text="Predict", style="Blue.TButton", command=prediction_request)
predict_button.place(relx=0.4, rely=0.7, anchor="center", width=500)

predicted_value = tk.StringVar()

price_textbox = ttk.Entry(root, font=("Arial", 14), textvariable=predicted_value, state="readonly")
price_textbox.place(relx=0.7, rely=0.7, anchor="center", width=150)

pred_error_label = ttk.Label(root, text="", font=("Arial", 14, "bold"))
pred_error_label.place(relx=0.5, rely=0.64, anchor="center")

#---------------------------------------------------------------------------------------------------------------------------------------

def retraining_request():
    user_features = validate("retrain")
    if user_features is not None:   

        url = 'http://localhost:5500'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=json.dumps(user_features))

        if response.status_code == 200:
            print("\nData for retraining sent successfully!")

            response = response.json()
            retrain_left = response['retrain_left']
            retrain_left = int(retrain_left)

            if retrain_left >= 1:
                if 3 - retrain_left == 1:
                    message = "sample"
                else:
                    message = "samples"

                status = f"{str(3 - retrain_left)} more {message} needed for retraining to initiate"
                retrain_status_label.config(text= status, foreground="gray")
            else:
                retrain_status_label.config(text="Retraining completed successfully!", foreground="green")

        else:
            print("Error:", response.status_code)

retrain_button = ttk.Button(root, text="Retrain", style="Blue.TButton", command=retraining_request)
retrain_button.place(relx=0.44, rely=0.85, anchor="center", width=200)

retrain_value = tk.StringVar()

retrain_field = ttk.Entry(root, font=("Arial", 12), textvariable=retrain_value,  validate="key", 
    validatecommand=(root.register(lambda new_value: validate_range(new_value, 0, 999999)), "%P"))

retrain_field.place(relx=0.6, rely=0.85, anchor="center", width=100)

dollar_label = ttk.Label(root, text="$", font=("Arial", 14, "bold"))
dollar_label.place(relx=0.55, rely=0.85, anchor="center")

retrain_status_label = ttk.Label(root, text="", font=("Arial", 14, "bold"))
retrain_status_label.place(relx=0.5, rely=0.92, anchor="center")

retrain_error_label = ttk.Label(root, text="", font=("Arial", 14, "bold"))
retrain_error_label.place(relx=0.5, rely=0.92, anchor="center")

#---------------------------------------------------------------------------------------------------------------------------------------

# Copyright 

line = tk.Canvas(root, width=350, height=1, bg="white", highlightthickness=0)
line.place(relx=0.5, rely=0.95, anchor="center")

copyright_text = ttk.Label(root, text="© 2024 Used Car Price Predictor by Omar Bahgat and Omar Anwar", font=("Arial", 10))
copyright_text.place(relx=0.5, rely=0.975, anchor="center")

#---------------------------------------------------------------------------------------------------------------------------------------

root.mainloop()

