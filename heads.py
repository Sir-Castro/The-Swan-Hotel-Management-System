import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import messagebox

class Heads(tk.Frame):
    def __init__(self, root, username, main_app):
        super().__init__(root)
        self.root = root
        self.username = username 
        self.main_app = main_app  # Reference to the main app

        # Set the background
        self.set_background()
        self.show_logo_with_fade()

    def set_background(self):
        # Load the background image
        self.background_image = Image.open("images/lounge4.jpg")
        self.background_image = self.background_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        )
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Cover the entire frame

    def show_logo_with_fade(self):
        # Load the logo image and resize it to the desired dimensions
        desired_width = 100  # Set your desired width here
        desired_height = 100  # Set your desired height here
        self.logo_image = Image.open("images/swan2.png").resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Create a label for the logo image
        self.logo_label = tk.Label(self, image=self.logo_photo, bg="black", relief="raised", borderwidth=7)
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # Start the fade-in effect
        self.fade_in_logo()

    def fade_in_logo(self, alpha=0):
        """Gradually fade in the logo."""
        if alpha <= 255:  # PIL uses alpha from 0 to 255
            faded_logo = self.logo_image.copy()
            faded_logo.putalpha(alpha)
            self.logo_photo = ImageTk.PhotoImage(faded_logo)
            self.logo_label.config(image=self.logo_photo)

            # Increment alpha and call the function again
            alpha += 15  # Adjust step for smoother or faster fading
            self.root.after(50, self.fade_in_logo, alpha)
        else:
            # Once fully visible, start fading out
            self.fade_out_logo(255)

    def fade_out_logo(self, alpha):
        """Gradually fade out the logo."""
        if alpha >= 0:  # Continue until fully transparent
            faded_logo = self.logo_image.copy()
            faded_logo.putalpha(alpha)
            self.logo_photo = ImageTk.PhotoImage(faded_logo)
            self.logo_label.config(image=self.logo_photo)

            # Decrement alpha and call the function again
            alpha -= 15  # Adjust step for smoother or faster fading
            self.after(50, self.fade_out_logo, alpha)
        else:
            # Once fully faded out, display the main content
            self.create_heads_frame()

    def create_heads_frame(self):
        # Create the heads frame (on top of the background image)
        heads_frame = tk.Frame(self, bg="lightgray", borderwidth=2, relief="groove")
        heads_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)

        # Title label
        title_label = tk.Label(heads_frame, text=f"Supervisor: {self.username}", font=("Arial", 16), bg="lightgray")
        title_label.pack(pady=10)

        # Create a frame for arranging buttons and the central view area
        content_frame = tk.Frame(heads_frame, bg="lightgray")
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Button titles
        top_buttons = ["Training", "Customer Service", "Operations", "Compliance", "Budgeting"]
        side_buttons = ["System", "Inventory", "Risk", "Perfomance"]

        # Button width
        button_width = 15  # Set static width for buttons

        # Add top buttons
        top_frame = tk.Frame(content_frame, bg="lightgray")
        top_frame.grid(row=0, column=0, columnspan=4, pady=(0, 10))  # Top row spanning multiple columns
        for title in top_buttons:
            button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width)
            button.pack(side="left", padx=10)

        # Add side buttons
        side_frame = tk.Frame(content_frame, bg="lightgray")
        side_frame.grid(row=1, column=0, sticky="ns", rowspan=3)  # Left column spanning multiple rows
        for title in side_buttons:
            button = tk.Button(side_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width)
            button.pack(pady=20)

        # Central view area (white box)
        central_view = tk.Frame(content_frame, bg="white", width=600, height=400, relief="groove", borderwidth=3)
        central_view.grid(row=1, column=1, rowspan=3, columnspan=3)

        # Adjust logout button position
        logout_button = tk.Button(
            side_frame, text="Logout", command=self.logout, bg="black", fg="white", font=("Arial", 10), width=button_width
        )
        logout_button.pack(pady=(20, 0))  # Add extra padding at the bottom for separation

    def logout(self):
        """Log out and return to the login screen"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            # Destroy the current frame (the Users frame)
            self.destroy()

            # Call the method to show the login frame in the main application
            self.main_app.show_login_frame()
