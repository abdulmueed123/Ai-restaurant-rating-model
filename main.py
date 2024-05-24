import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class RestaurantRatingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Restaurant Rating Prediction")
        self.master.geometry("450x300")
        self.master.configure(bg='#f0f0f0')
        
        # Styling options
        self.label_font = ("Helvetica", 12)
        self.entry_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")

        # Header
        self.header = tk.Label(master, text="Restaurant Rating Prediction", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
        self.header.pack(pady=10)

        # Frame for location input
        self.location_frame = tk.Frame(master, bg='#f0f0f0', pady=10)
        self.location_frame.pack(fill='x')
        self.label1 = tk.Label(self.location_frame, text="Select location:", font=self.label_font, bg='#f0f0f0')
        self.label1.pack(side='left', padx=(20, 10))
        self.location_options = ['Multan', 'Lahore']
        self.location_combobox = ttk.Combobox(self.location_frame, values=self.location_options, font=self.entry_font)
        self.location_combobox.pack(side='left', padx=(0, 20))

        # Frame for cuisine input
        self.cuisine_frame = tk.Frame(master, bg='#f0f0f0', pady=10)
        self.cuisine_frame.pack(fill='x')
        self.label2 = tk.Label(self.cuisine_frame, text="Select cuisine:", font=self.label_font, bg='#f0f0f0')
        self.label2.pack(side='left', padx=(20, 10))
        self.cuisine_options = ['Italian', 'Mexican', 'Chinese', 'Pakistani']
        self.cuisine_combobox = ttk.Combobox(self.cuisine_frame, values=self.cuisine_options, font=self.entry_font)
        self.cuisine_combobox.pack(side='left', padx=(0, 20))

        # Frame for price input
        self.price_frame = tk.Frame(master, bg='#f0f0f0', pady=10)
        self.price_frame.pack(fill='x')
        self.label3 = tk.Label(self.price_frame, text="Enter price range (1-5):", font=self.label_font, bg='#f0f0f0')
        self.label3.pack(side='left', padx=(20, 10))
        self.price_entry = ttk.Entry(self.price_frame, font=self.entry_font)
        self.price_entry.pack(side='left', padx=(0, 20))

        # Frame for predict button
        self.button_frame = tk.Frame(master, bg='#f0f0f0', pady=20)
        self.button_frame.pack(fill='x')
        self.predict_button = ttk.Button(self.button_frame, text="Predict Rating", command=self.predict_rating, style="TButton")
        self.predict_button.pack(pady=10)

        # Style for the button
        s = ttk.Style()
        s.configure('TButton', font=self.button_font, padding=6)

    def load_data(self):
        # Load the dataset from a CSV file
        try:
            self.data = pd.read_csv("Ai.csv")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def preprocess_data(self):
        # Convert categorical variables into dummy variables
        self.data = pd.get_dummies(self.data, columns=["Location", "Cuisine"], drop_first=True)

    def predict_rating(self):
        try:
            self.load_data()
            self.preprocess_data()

            # Features and target variable
            X = self.data.drop(columns=["Rating"])
            y = self.data["Rating"]

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train linear regression model
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Predict rating
            location = self.location_combobox.get()
            cuisine = self.cuisine_combobox.get()
            price = float(self.price_entry.get())

            # Convert input location and cuisine into dummy variables
            input_data = pd.DataFrame([[0] * len(X.columns)], columns=X.columns)
            if f"Location_{location}" in input_data.columns:
                input_data[f"Location_{location}"] = 1
            if f"Cuisine_{cuisine}" in input_data.columns:
                input_data[f"Cuisine_{cuisine}"] = 1
            input_data["Price"] = price

            predicted_rating = model.predict(input_data)[0]

            messagebox.showinfo("Prediction", f"Predicted Rating: {predicted_rating:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = RestaurantRatingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
