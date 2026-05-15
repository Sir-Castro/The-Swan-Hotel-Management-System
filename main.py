#Create interface for manager
#Remember to save individual tables when exporting
#To export database use backup option, to import use restore then choose file name.
import tkinter as tk
from tkinter import PhotoImage
from login import Login
from PIL import Image, ImageTk
from dep import Departments
from users import Users
from heads import Heads
from admin import Admin

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("The Swan Hotel")
        self.logged_in_user = None
        # Set the window to full screen
        self.root.attributes('-fullscreen', True)

        # Set the background image
        self.set_background()

        # Show the logo first and then transition to the login frame
        self.show_logo()
        

    def set_background(self):
        # Load the background image
        self.background_image = Image.open("images/lounge4.jpg")
        self.background_image = self.background_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))  # Removed ANTIALIAS
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

    def show_logo(self):
        # Load the image using PIL for resizing
        original_image = Image.open("images/swan1.png")  # Ensure logo.png exists
        resized_image = original_image.resize((300, 300))  # Set desired width and height (400x400)

        # Convert the resized image back to a PhotoImage for Tkinter
        self.logo_image = ImageTk.PhotoImage(resized_image)

        # Create a label to hold the resized logo image with border and style
        self.logo_label = tk.Label(self.root, image=self.logo_image, bg="white", bd=10, relief="raised")
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")  # Position at the center

        # Start fading out the logo after 3 seconds
        self.root.after(3000, self.fade_out_logo)

    def fade_out_logo(self):
        # Fade out the logo by progressively decreasing its opacity
        self.fade_step = 0.016  # Adjust the fade step for smoother transition (smaller steps)
        self.fade_out(self.logo_label, 1.0)  # Start fading from full opacity

    def fade_out(self, widget, opacity):
        # Decrease the opacity gradually (visibility) with smaller increments for smoother transition
        if opacity > 0:
            # Set the widget's opacity without changing its size (remove width/height resizing)
            widget.place_configure(relx=0.5, rely=0.5, anchor="center")  # Keep the position centered

            # Simulate the opacity change by updating the widget's background color
            red = int(255 * opacity)  # Adjust the intensity of the color channels
            green = int(255 * opacity)
            blue = int(255 * opacity)
            color = f"#{red:02x}{green:02x}{blue:02x}"  # Create a hex color string
            widget.config(bg=color)  # Update the background color

            # Schedule the next fade step
            self.root.after(30, self.fade_out, widget, opacity - self.fade_step)  # Recursive call for next fade step
        else:
            # Once logo is fully faded out, destroy it and show the login frame
            widget.destroy()
            self.show_login_frame()



    def show_login_frame(self):
        # Ensure to destroy the existing frames, but keep the background
        for widget in self.root.winfo_children():
            if widget != self.bg_label:  # Do not destroy the background label
                widget.destroy()
        
        self.login_frame = Login(self.root, self)
        

    def show_dashboard(self):
        # Destroy the login frame properly
        self.login_frame.frame_login.destroy()
        
        # Destroy the close button if it exists
        if hasattr(self.login_frame, 'close_button'):
            self.login_frame.close_button.destroy()
 
        # Show the dashboard
        self.heads_frame = Admin(self.root, Admin, self)  # Pass 'self' for the main app
        self.heads_frame.pack(fill=tk.BOTH, expand=True)

    def show_department_frame(self, username):
           # Destroy the login frame properly
        self.login_frame.frame_login.destroy()
        
        # Destroy the close button if it exists
        if hasattr(self.login_frame, 'close_button'):
            self.login_frame.close_button.destroy()
            
        # Create and pack the new Departments frame
        self.departments_frame = Departments(self.root, username, self)
        self.departments_frame.pack(fill=tk.BOTH, expand=True)
    def show_users_frame(self, username):
    
        self.login_frame.frame_login.destroy()
        
        # Destroy the close button if it exists
        if hasattr(self.login_frame, 'close_button'):
            self.login_frame.close_button.destroy()

        # Create and pack the Users frame for the logged-in user
        self.users_frame = Users(self.root, username, self)
        self.users_frame.pack(fill=tk.BOTH, expand=True)

    def show_heads_frame(self, username):
        self.login_frame.frame_login.destroy()
        
        # Destroy the close button if it exists
        if hasattr(self.login_frame, 'close_button'):
            self.login_frame.close_button.destroy()

        self.heads_frame = Heads(self.root, username, self)  # Pass 'self' for the main app
        self.heads_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
