import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import messagebox
from database import get_db_connection
from tkinter import messagebox, StringVar, simpledialog
import bcrypt
import psycopg2

class Admin(tk.Frame):
    def __init__(self, root, admin, main_app):
        super().__init__(root)
        self.root = root
        self.admin = admin  # Data for heads of departments
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

    def clear_central_view(self):
        """Clears the central view area for new content."""
        for widget in self.central_view.winfo_children():
            widget.place_forget()
    def center_window(self, window, width, height):
        """Center the window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_heads_frame(self):
        # Create the heads frame (on top of the background image)
        heads_frame = tk.Frame(self, bg="lightgray", borderwidth=2, relief="groove")
        heads_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)

        # Title label
        title_label = tk.Label(heads_frame, text="Admin Dashboard", font=("Arial", 25, "bold"), bg="lightgray")
        title_label.pack(pady=10)

        # Create a frame for arranging buttons and the central view area
        content_frame = tk.Frame(heads_frame, bg="lightgray")
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Button titles
        top_buttons = ["Create Staff", "Delete Staff", "Create Department", "Delete Department", "Admin Password"]
        side_buttons = ["Staff Password", "Department Password", "View Records", "Update Rights", "Logout"]

        # Button width
        button_width = 15  # Set static width for buttons

        # Add top buttons
        top_frame = tk.Frame(content_frame, bg="lightgray")
        top_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10))  # Top row spanning multiple columns

        # Central view area (white box)
        self.central_view = tk.Frame(content_frame, bg="white", width=600, height=450, relief="groove", borderwidth=3)
        self.central_view.grid(row=1, column=1, rowspan=2, columnspan=3, sticky="nsew")

        # Default text inside central view area
        self.default_label = tk.Label(self.central_view, text="The Swan Hotel", font=("Arial", 24, "bold"), bg="white")
        self.default_label.place(relx=0.5, rely=0.5, anchor="center")

        def create_staff_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Create Staff", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=5)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add form fields
            # User ID
            tk.Label(form_frame, text="User ID:", font=("Arial", 12), bg="white").place(x=40, y=20)
            self.entry_user_id = tk.Entry(form_frame, font=("Arial", 12), state="disabled")
            self.entry_user_id.place(x=200, y=20, width=170)

            # Full Name
            tk.Label(form_frame, text="Full Name:", font=("Arial", 12), bg="white").place(x=40, y=60)
            self.entry_fullname = tk.Entry(form_frame, font=("Arial", 12))
            self.entry_fullname.place(x=200, y=60, width=170)

            # Username
            tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="white").place(x=40, y=100)
            self.entry_username = tk.Entry(form_frame, font=("Arial", 12))
            self.entry_username.place(x=200, y=100, width=170)

            # Password
            tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white").place(x=40, y=140)
            self.entry_password = tk.Entry(form_frame, show="*", font=("Arial", 12))
            self.entry_password.place(x=200, y=140, width=170)

            # Department dropdown
            tk.Label(form_frame, text="Department:", font=("Arial", 12), bg="white").place(x=40, y=180)
            self.department_var = tk.StringVar(form_frame)
            self.department_var.set("Select")
            self.dropdown_department = tk.OptionMenu(form_frame, self.department_var, "Select Department")
            self.dropdown_department.place(x=200, y=180, width=170)
            self.dropdown_department.config(font=("Arial", 12), width=20)

            self.update_department_dropdown()


            # User Type dropdown
            tk.Label(form_frame, text="User Type:", font=("Arial", 12), bg="white").place(x=40, y=220)
            self.user_type_var = tk.StringVar()
            self.user_type_var.set("Select")
            dropdown_user_type = tk.OptionMenu(form_frame, self.user_type_var, "Manager", "Supervisor", "Staff")
            dropdown_user_type.place(x=200, y=220, width=170)
            dropdown_user_type.config(font=("Arial", 12), width=20)

            # Submit button
            tk.Button(form_frame, text="Submit", font=("Arial", 12), bg="black", fg="white", command=self.create_user).place(x=150, y=280)

            self.generate_user_id()
        def delete_staff_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Delete Staff", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add instructions
            title_label = tk.Label(form_frame, text="Delete Staff", font=("Arial", 22), fg="black")
            title_label.place(relx=0.5, rely=0.25, anchor="n")  # Position at 10% height of the frame

            # Frame for listbox and scrollbar
            listbox_frame = tk.Frame(form_frame)
            listbox_frame.pack(pady=30, padx=10, fill=tk.BOTH, expand=True)
            list_title = tk.Label(listbox_frame, text="Staff", font=("Arial", 12), fg="black")
            list_title.pack(side=tk.TOP, pady=1)

            # Scrollable list for displaying search results
            self.result_listbox = tk.Listbox(listbox_frame, width=20, height=1)
            self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Make the listbox scrollable
            scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
            scrollbar.config(command=self.result_listbox.yview)
            self.result_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Populate the listbox with staff usernames
            self.populate_listbox_staff2()

            # Bind double-click event to listbox
            self.result_listbox.bind("<Double-1>", self.confirm_deletion_user)

        def create_department_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Create Department", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=5)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            #instructions = tk.Label(form_frame, text="Create Department", font=("Arial", 16), bg="white")
            #instructions.place(relx=0.5, rely=0.01, anchor="n")  # Position at 10% height of the frame

            # Add form fields using place
            self.label_dept_id = tk.Label(form_frame, text="Department ID:", font=("Arial", 12), bg="white")
            self.label_dept_id.place(x=40, y=60)  # Adjust position
            self.entry_dept_id = tk.Entry(form_frame, font=("Arial", 12), relief="groove", borderwidth=5, state="disabled")
            self.entry_dept_id.place(x=200, y=60, width=150)  # Adjust position and width

            self.label_dept_name = tk.Label(form_frame, text="Department Name:", font=("Arial", 12), bg="white")
            self.label_dept_name.place(x=40, y=110)  # Adjust position
            self.entry_dept_name = tk.Entry(form_frame, font=("Arial", 12), relief="groove", borderwidth=5)
            self.entry_dept_name.place(x=200, y=110, width=150)  # Adjust position and width

            self.label_password = tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white")
            self.label_password.place(x=40, y=160)  # Adjust position
            self.entry_dept_password = tk.Entry(form_frame, show='*', font=("Arial", 12), relief="groove", borderwidth=5)
            self.entry_dept_password.place(x=200, y=160, width=150)  # Adjust position and width

            tk.Label(form_frame, text="Department Rights:", font=("Arial", 12), bg="white").place(x=40, y=210)
            self.dept_rights_var = StringVar(form_frame)
            self.dept_rights_var.set("Select")  # Adjust position
            self.rights_button = tk.Button(form_frame, text=self.dept_rights_var.get(), font=("Arial", 12), relief="groove", borderwidth=5, command=self.open_rights_popup)
            self.rights_button.place(x=200, y=210, width=150)  # Adjust position and width

            # Submit button at the bottom
            submit_button = tk.Button(form_frame, text="Submit", font=("Arial", 12), bg="black", fg="white", command=self.create_department)
            submit_button.place(relx=0.5, rely=0.8, anchor="center") 
            self.generate_department_id()

        def delete_department_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Delete Department", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Frame for listbox and scrollbar
            listbox_frame = tk.Frame(form_frame)
            listbox_frame.pack(pady=30, padx=10, fill=tk.BOTH, expand=True)
            # Add instructions
            tk.Label(listbox_frame, text="Departments", font=("Arial", 12), fg="black").pack(side=tk.TOP, pady=1)

            # Scrollable list for displaying search results
            self.result_listbox = tk.Listbox(listbox_frame, width=20, height=1)
            self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Make the listbox scrollable
            scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
            scrollbar.config(command=self.result_listbox.yview)
            self.result_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.populate_listbox_departments()

            # Bind double-click event to listbox
            self.result_listbox.bind("<Double-1>", self.confirm_deletion_department)

        def admin_password_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Admin Password", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=5)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            #instructions = tk.Label(form_frame, text="Create Department", font=("Arial", 16), bg="white")
            #instructions.place(relx=0.5, rely=0.01, anchor="n")  # Position at 10% height of the frame

            # Add form fields using place
            tk.Label(form_frame, text="Current Password:", font=("Arial", 12), bg="white").place(x=40, y=60)  # Adjust position
            self.entry_current_password = tk.Entry(form_frame, font=("Arial", 12), relief="groove", borderwidth=5, show="*")  # Adjust position and width
            self.entry_current_password.place(x=200, y=60, width=100)
            # Button to toggle show/hide password
            self.toggle_button = tk.Button(form_frame, text="Show", font=("Arial", 10), command=self.toggle_password)
            self.toggle_button.place(x=300, y=57)
            
            tk.Label(form_frame, text="New Password:", font=("Arial", 12), bg="white").place(x=40, y=110)  # Adjust position
            self.entry_new_password = tk.Entry(form_frame, font=("Arial", 12), relief="groove", borderwidth=5, show="*")
            self.entry_new_password.place(x=200, y=110, width=150)
            
            tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12), bg="white").place(x=40, y=160)  # Adjust position
            self.entry_confirm_password = tk.Entry(form_frame, font=("Arial", 12), relief="groove", borderwidth=5, show="*")
            self.entry_confirm_password.place(x=200, y=160, width=150)
            

            button_update = tk.Button(form_frame, text="Change Password:",  command=self.validate_admin_passwords, font=("Arial", 12), bg="white").place(x=110, y=210)  # Adjust position
            self.fetch_admin_password()
        def staff_password_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Staff Password", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=5)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            tk.Label(form_frame, text="Select Staff:", font=("Arial", 12), bg="white").place(x=40, y=60)
            self.staff_var = tk.StringVar(form_frame)
            self.staff_var.set("Select")
            self.dropdown_staff = tk.OptionMenu(form_frame, self.staff_var, "Select Staff")
            self.dropdown_staff.place(x=200, y=60, width=150)
            self.dropdown_staff.config(font=("Arial", 12), width=20)

            self.update_staff_dropdown()
            self.staff_var.trace("w", self.on_staff_selected)

            tk.Label(form_frame, text="Current Password:", font=("Arial", 12), bg="white").place(x=40, y=110)  # Adjust position
            self.entry_current_password = tk.Entry(form_frame, font=("Arial", 12), relief="groove", borderwidth=5, show="*")  # Adjust position and width
            self.entry_current_password.place(x=200, y=110, width=100)
            self.toggle_button = tk.Button(form_frame, text="Show", font=("Arial", 10), command=self.toggle_password)
            self.toggle_button.place(x=300, y=110)

            tk.Label(form_frame, text="New Password:", font=("Arial", 12), bg="white").place(x=40, y=160)  # Adjust position
            self.entry_new_password = tk.Entry(form_frame, font=("Arial", 12), show="*", relief="groove", borderwidth=5)
            self.entry_new_password.place(x=200, y=160, width=150)  # Adjust position and width

            label_password = tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12), bg="white")
            label_password.place(x=40, y=210)  # Adjust position
            self.entry_confirm_password = tk.Entry(form_frame, font=("Arial", 12), show="*", relief="groove", borderwidth=5)
            self.entry_confirm_password.place(x=200, y=210, width=150)  # Adjust position and width

            # Submit button at the bottom
            submit_button = tk.Button(form_frame, text="Submit", command=self.validate_user_passwords, font=("Arial", 12), bg="black", fg="white")
            submit_button.place(relx=0.5, rely=0.8, anchor="center") 

        def department_password_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Department Password", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=5)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            tk.Label(form_frame, text="Select Department:", font=("Arial", 12), bg="white").place(x=40, y=60)
            self.department_var = tk.StringVar(form_frame)
            self.department_var.set("Select")
            self.dropdown_department = tk.OptionMenu(form_frame, self.department_var, "Select Staff")
            self.dropdown_department.place(x=200, y=60, width=150)
            self.dropdown_department.config(font=("Arial", 12), width=20)

            self.update_department_dropdown()
            self.department_var.trace("w", self.on_department_selected)

            tk.Label(form_frame, text="Current Password:", font=("Arial", 12), bg="white").place(x=40, y=110)  # Adjust position
            self.entry_current_password = tk.Entry(form_frame, font=("Arial", 12), relief="groove", borderwidth=5, show="*")  # Adjust position and width
            self.entry_current_password.place(x=200, y=110, width=100)
            self.toggle_button = tk.Button(form_frame, text="Show", font=("Arial", 10), command=self.toggle_password)
            self.toggle_button.place(x=300, y=110)


            tk.Label(form_frame, text="New Password:", font=("Arial", 12), bg="white").place(x=40, y=160)  # Adjust position
            self.entry_new_password = tk.Entry(form_frame, font=("Arial", 12), show="*", relief="groove", borderwidth=5)
            self.entry_new_password.place(x=200, y=160, width=150)  # Adjust position and width

            label_password = tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12), bg="white")
            label_password.place(x=40, y=210)  # Adjust position
            self.entry_confirm_password = tk.Entry(form_frame, font=("Arial", 12), show="*", relief="groove", borderwidth=5)
            self.entry_confirm_password.place(x=200, y=210, width=150)  # Adjust position and width

            # Submit button at the bottom
            submit_button = tk.Button(form_frame, text="Submit", command=self.validate_department_passwords, font=("Arial", 12), bg="black", fg="white")
            submit_button.place(relx=0.5, rely=0.8, anchor="center") 


        def view_records_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="View Records", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Toggle button
            self.view_mode = tk.StringVar(value="Staff")  # Default to Staff
            toggle_button = tk.Button(form_frame, text="View Departments", command=self.toggle_view, width=20)
            toggle_button.pack(side=tk.TOP, pady=10)

            # Frame for listbox and scrollbar
            listbox_frame = tk.Frame(form_frame)
            listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

            # Add instructions
            self.list_title = tk.Label(listbox_frame, text="Staff List", font=("Arial", 12), fg="black")
            self.list_title.pack(side=tk.TOP, pady=1)

            # Scrollable list for displaying search results
            self.result_listbox = tk.Listbox(listbox_frame, width=20, height=1)
            self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Make the listbox scrollable
            scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
            scrollbar.config(command=self.result_listbox.yview)
            self.result_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate the listbox with staff usernames
            self.populate_listbox_staff()
            self.toggle_button = toggle_button

        def update_rights_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Update Rights", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Frame for listbox and scrollbar
            listbox_frame = tk.Frame(form_frame)
            listbox_frame.pack(pady=30, padx=10, fill=tk.BOTH, expand=True)
            # Add instructions
            tk.Label(listbox_frame, text="Departments", font=("Arial", 12), fg="black").pack(side=tk.TOP, pady=1)

            # Scrollable list for displaying search results
            self.result_listbox = tk.Listbox(listbox_frame, width=20, height=1)
            self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Make the listbox scrollable
            scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
            scrollbar.config(command=self.result_listbox.yview)
            self.result_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.populate_listbox_departments()

            # Bind double-click event to listbox
            self.result_listbox.bind("<Double-1>", self.update_department_rights)



        # Add top buttons
        for title in top_buttons:
            if title == "Create Staff":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=create_staff_form)
            elif title == "Delete Staff":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=delete_staff_form)
            elif title == "Create Department":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=create_department_form)
            elif title == "Delete Department":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=delete_department_form)
            elif title == "Admin Password":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=admin_password_form)
            else:
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width)
            button.pack(side="left", padx=10)


        # Assigning commands to side buttons
        side_frame = tk.Frame(content_frame, bg="lightgray")
        side_frame.grid(row=1, column=0, sticky="ns", rowspan=3)  # Left column

        for button_text in side_buttons:
            if button_text == "Staff Password":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=staff_password_form)
            elif button_text == "Department Password":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=department_password_form)
            elif button_text == "View Records":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=view_records_form)
            elif button_text == "Update Rights":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=update_rights_form)
            elif button_text == "Logout":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=self.logout)
            
            else:
                button = tk.Button(side_frame, text=button_text, width=button_width, bg="black", fg="white")
            button.pack(pady=20)


    def logout(self):
        """Log out and return to the login screen"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            # Destroy the current frame (the Users frame)
            self.destroy()

            # Call the method to show the login frame in the main application
            self.main_app.show_login_frame()
    def create_user(self):
        user_id = self.entry_user_id.get()  # User ID is generated automatically
        fullname = self.entry_fullname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        department = self.department_var.get()
        user_type = self.user_type_var.get()

        # Ensure required fields are filled
        if fullname and username and password and department != "Select Department" and user_type != "Select User Type":
            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Check if the user_id already exists
                cursor.execute("SELECT COUNT(*) FROM staff WHERE user_id = %s", (user_id,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showwarning("User ID Exists", "The User ID already exists. Please choose a different User ID.")
                    return  # Exit the function if the user ID exists

                # Insert user data into the database with additional fields
                cursor.execute("""
                    INSERT INTO staff (user_id, fullname, username, password, department, user_type, lock_status, role_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, fullname, username, password, department, user_type, False, None))

                # Commit the transaction
                connection.commit()
                messagebox.showinfo("Success", "User created successfully!")

                # Clear the input fields
                self.entry_fullname.delete(0, tk.END)
                self.entry_username.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                self.department_var.set("Select Department")
                self.user_type_var.set("Select User Type")

                # Generate a new user ID for the next user
                self.generate_user_id()

            except Exception as error:
                messagebox.showerror("Database Error", f"Error creating user: {error}")

            finally:
                # Close the database connection
                if connection:
                    cursor.close()
                    connection.close()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields correctly.")

    def generate_user_id(self):
            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Get the highest user_id from the database
                cursor.execute("SELECT MAX(user_id) FROM staff")
                max_user_id = cursor.fetchone()[0]

                # Generate a new user_id
                if max_user_id is None:
                    new_user_id = 1  # Start at 1 if no user exists
                else:
                    new_user_id = max_user_id + 1

                # Check if the generated user_id already exists
                cursor.execute("SELECT COUNT(*) FROM staff WHERE user_id = %s", (new_user_id,))
                user_id_exists = cursor.fetchone()[0] > 0

                # If the user_id exists, increment and check again
                while user_id_exists:
                    new_user_id += 1
                    cursor.execute("SELECT COUNT(*) FROM staff WHERE user_id = %s", (new_user_id,))
                    user_id_exists = cursor.fetchone()[0] > 0

                # Set the new user_id in the input field
                self.entry_user_id.config(state="normal")  # Enable the field temporarily
                self.entry_user_id.delete(0, tk.END)
                self.entry_user_id.insert(0, new_user_id)
                self.entry_user_id.config(state="disabled")  # Disable the field again

            except Exception as error:
                messagebox.showerror("Database Error", f"Error generating user ID: {error}")

            finally:
                # Close the database connection
                if connection:
                    cursor.close()
                    connection.close()
    

    def populate_listbox_staff(self):
        """Fetch staff details and populate the listbox."""
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Retrieve all required fields from the `staff` table, setting default value for role_name
            cursor.execute("""
                SELECT username, fullname, COALESCE(role_name, 'Staff') AS role_name, department 
                FROM staff
            """)
            staff = cursor.fetchall()

            # Clear the listbox and add the formatted staff details
            self.result_listbox.delete(0, tk.END)
            for row in staff:
                username, fullname, role_name, department = row
                display_text = f"{username} | {fullname} | {role_name} | {department}"
                self.result_listbox.insert(tk.END, display_text)

        except Exception as error:
            messagebox.showerror("Database Error", f"Error retrieving staff: {error}")

        finally:
            if connection:
                cursor.close()
                connection.close()

    def populate_listbox_staff2(self):
        """Fetch staff usernames and full names, then populate the listbox."""
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Retrieve only username and fullname from the `staff` table
            cursor.execute("SELECT username, fullname FROM staff")
            staff = cursor.fetchall()

            # Clear the listbox and add the formatted staff details
            self.result_listbox.delete(0, tk.END)
            for username, fullname in staff:
                display_text = f"{username} | {fullname}"
                self.result_listbox.insert(tk.END, display_text)

        except Exception as error:
            messagebox.showerror("Database Error", f"Error retrieving staff: {error}")

        finally:
            if connection:
                cursor.close()
                connection.close()


    def populate_listbox_departments(self):
        """Fetch department names and populate the listbox."""
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Retrieve all department names from the `departments` table
            cursor.execute("SELECT dept_name FROM departments")
            departments = cursor.fetchall()

            # Clear the listbox and add department names
            self.result_listbox.delete(0, tk.END)
            for row in departments:
                dept_name = row[0]  # Extract dept_name from the tuple
                self.result_listbox.insert(tk.END, dept_name)

        except Exception as error:
            messagebox.showerror("Database Error", f"Error retrieving departments: {error}")

        finally:
            if connection:
                cursor.close()
                connection.close()


    def confirm_deletion_user(self, event):
        """Handle double-click event to confirm deletion."""
        selected_user = self.result_listbox.get(tk.ACTIVE)  # Get the selected row
        if selected_user:
            # Extract username from the selected row
            username = selected_user.split(" | ")[0]  # Assuming username is the first field
            response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {username}?")
            if response:
                self.delete_user(username)
    def confirm_deletion_department(self, event):
        """Handle double-click event to confirm deletion."""
        selected_dept = self.result_listbox.get(tk.ACTIVE)  # Get the selected row
        if selected_dept:
            # Extract username from the selected row
            dept_name = selected_dept.split(" | ")[0]  # Assuming username is the first field
            response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {dept_name} Department?")
            if response:
                self.delete_department(dept_name)
    def delete_user(self, username):
        """Delete the selected user from the database."""
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if the user exists in the database
            cursor.execute("SELECT COUNT(*) FROM staff WHERE username = %s", (username,))
            if cursor.fetchone()[0] > 0:
                # Delete the user
                cursor.execute("DELETE FROM staff WHERE username = %s", (username,))
                connection.commit()

                # Show success message
                messagebox.showinfo("Success", f"User '{username}' deleted.")

                # Refresh the listbox
                self.populate_listbox_staff()
            else:
                messagebox.showwarning("Not Found", f"User '{username}' does not exist in the database.")

        except Exception as error:
            messagebox.showerror("Database Error", f"Error deleting user: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()
    def delete_department(self, dept_name):
        """Delete the selected user from the database."""
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if the user exists in the database
            cursor.execute("SELECT COUNT(*) FROM departments WHERE dept_name = %s", (dept_name,))
            if cursor.fetchone()[0] > 0:
                # Delete the user
                cursor.execute("DELETE FROM departments WHERE dept_name = %s", (dept_name,))
                connection.commit()

                # Show success message
                messagebox.showinfo("Success", f"{dept_name} Department deleted.")

                # Refresh the listbox
                self.populate_listbox_departments()
            else:
                messagebox.showwarning("Not Found", f"{username} Department does not exist in the database.")

        except Exception as error:
            messagebox.showerror("Database Error", f"Error deleting department: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()
    def generate_department_id(self):
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Get the highest dept_id from the database
            cursor.execute("SELECT MAX(dept_id) FROM departments")
            max_dept_id = cursor.fetchone()[0]

            # Generate a new dept_id
            if max_dept_id is None:
                new_dept_id = 1  # Start at 1 if no department exists
            else:
                new_dept_id = max_dept_id + 1

            # Check if the generated dept_id already exists
            cursor.execute("SELECT COUNT(*) FROM departments WHERE dept_id = %s", (new_dept_id,))
            dept_id_exists = cursor.fetchone()[0] > 0

            # If the dept_id exists, increment and check again
            while dept_id_exists:
                new_dept_id += 1
                cursor.execute("SELECT COUNT(*) FROM departments WHERE dept_id = %s", (new_dept_id,))
                dept_id_exists = cursor.fetchone()[0] > 0

            # Set the new dept_id in the input field
            self.entry_dept_id.config(state="normal")  # Enable the field temporarily
            self.entry_dept_id.delete(0, tk.END)
            self.entry_dept_id.insert(0, new_dept_id)
            self.entry_dept_id.config(state="disabled")  # Disable the field again

        except Exception as error:
            messagebox.showerror("Database Error", f"Error generating department ID: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def create_department(self):
        dept_id = self.entry_dept_id.get()
        dept_name = self.entry_dept_name.get()
        dept_password = self.entry_dept_password.get()
        dept_rights = self.dept_rights_var.get()

        if dept_id and dept_name and dept_password and dept_rights != "Select Rights":
            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Insert department data into the database
                cursor.execute("""
                    INSERT INTO departments (dept_id, dept_name, dept_password, dept_rights)
                    VALUES (%s, %s, %s, %s)
                """, (dept_id, dept_name, dept_password, dept_rights))

                # Commit the transaction
                connection.commit()
                messagebox.showinfo("Success", "Department created successfully!")

                # Update department dropdown or any other UI element
                #self.update_department_dropdown()


                # Clear the input fields
                self.entry_dept_id.delete(0, tk.END)
                self.entry_dept_name.delete(0, tk.END)
                self.entry_dept_password.delete(0, tk.END)
                  # Reset the rights button
                self.dept_rights_var.set("Select Rights")
                self.rights_button.config(text=self.dept_rights_var.get(), state=tk.NORMAL)

            except Exception as error:
                messagebox.showerror("Database Error", f"Error creating department: {error}")

            finally:
                # Close the database connection
                if connection:
                    cursor.close()
                    connection.close()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields correctly.")

    def open_rights_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Select Rights")

        # Center the popup window
        self.center_window(popup, 400, 400)  # Adjust the width and height as needed

        rights_frame = tk.Frame(popup)
        rights_frame.pack(pady=10, padx=10)

        # Button to add rights
        btn_add = tk.Button(rights_frame, text="+", command=self.add_right_entry)
        btn_add.pack(side=tk.LEFT, padx=10)

        self.rights_listbox = tk.Listbox(popup, selectmode=tk.MULTIPLE, height=10, width=40)
        self.rights_listbox.pack(pady=10, padx=10)

        self.right_entries = []  # List to store the entry widgets

        button_update_rights = tk.Button(popup, text="Update Rights", command=self.update_rights)
        button_update_rights.pack(pady=10)

    def add_right_entry(self):
        # Create an entry for the new right
        entry = tk.Entry(self.rights_listbox)
        entry.insert(0, "New Right")
        entry.pack(fill=tk.X, padx=5, pady=2)  # Add padding between entries

        # Add the entry to the list
        self.right_entries.append(entry)

        # Make the entry editable when double-clicked
        entry.bind("<Double-1>", lambda event, e=entry: self.edit_right_entry(e))

    def edit_right_entry(self, entry):
        # Set the entry to be editable when double-clicked
        entry.config(state=tk.NORMAL)
        entry.focus()  # Focus the entry widget to start typing

    def update_rights(self):
        selected_rights = []
        for entry in self.right_entries:
            selected_rights.append(entry.get())  # Collect the text from each entry

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            for right in selected_rights:
                # Insert each right into the rights table; right_id auto-increments automatically
                cursor.execute("INSERT INTO rights (right_data) VALUES (%s)", (right,))
            
            connection.commit()  # Commit the transaction
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return
        finally:
            # Ensure the cursor and connection are closed
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        # Update the button and display success message
        self.dept_rights_var.set(", ".join(selected_rights))  # Join selected rights with comma
        self.rights_button.config(text="Rights Updated", state=tk.DISABLED)  # Update button text and disable it

        messagebox.showinfo("Rights Updated", "Rights have been saved and updated successfully.")

    def update_department_dropdown(self):
        self.dropdown_department['menu'].delete(0, 'end')

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all departments
            cursor.execute("SELECT dept_name FROM departments")
            departments = cursor.fetchall()  # Fetch all department names

            if departments:
                for dept in departments:  # Iterate over the fetched departments
                    dept_name = dept[0]  # Access the first element in the tuple
                    self.dropdown_department['menu'].add_command(
                        label=dept_name, 
                        command=tk._setit(self.department_var, dept_name)
                    )
            else:
                self.department_var.set("No departments available")

        except Exception as error:
            print(f"Error fetching departments: {error}")
            self.department_var.set("Error loading departments")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def update_staff_dropdown(self):
        self.dropdown_staff['menu'].delete(0, 'end')

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all usernames from the staff table
            cursor.execute("SELECT username FROM staff")
            staff_members = cursor.fetchall()  # Fetch all usernames

            if staff_members:
                for member in staff_members:  # Iterate over the fetched staff members
                    username = member[0]  # Access the first element in the tuple (username)
                    self.dropdown_staff['menu'].add_command(
                        label=username, 
                        command=tk._setit(self.staff_var, username)
                    )
            else:
                self.staff_var.set("No staff members available")

        except Exception as error:
            print(f"Error fetching staff members: {error}")
            self.staff_var.set("Error loading staff members")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def fetch_admin_password(self):
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch the hashed password from the admin table
            cursor.execute("""
                SELECT hashed_password FROM admin WHERE username = %s
            """, ("Admin",))  # Use parameterized queries for security
            result = cursor.fetchone()

            if result:
                # Get the hashed password from the result
                hashed_password = result[0]
                self.entry_current_password.config(state="normal")  # Enable entry for inserting data
                self.entry_current_password.delete(0, tk.END)  # Clear any existing text
                self.entry_current_password.insert(0, result[0])  # Assuming result[0] is the password
                self.entry_current_password.config(state="readonly")  # Assuming result[0] is the password
            else:
                messagebox.showwarning("Not Found", "Admin password not found.")

        except Exception as error:
            print(f"Error fetching password: {error}")
            messagebox.showerror("Database Error", "Error fetching password.")
        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def on_staff_selected(self, *args):
        selected_staff = self.staff_var.get()
        if selected_staff != "Select":
            self.fetch_staff_password() 

    def on_department_selected(self, *args):
        selected_department = self.department_var.get()
        if selected_department != "Select":
            self.fetch_department_password() 

    def toggle_password(self):
        if self.entry_current_password.cget("show") == "*":
            self.entry_current_password.config(show="")
            self.toggle_button.config(text="Hide")
        else:
            self.entry_current_password.config(show="*")
            self.toggle_button.config(text="Show")

    def validate_admin_passwords(self):
        """Validates if new password and confirm password match, then updates the database with the hashed password."""
        new_password = self.entry_new_password.get()
        confirm_password = self.entry_confirm_password.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "New Password and Confirm Password do not match!")
            return


        try:
            # Connect to the PostgreSQL database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Update the hashed password for the Admin user
            update_query = "UPDATE admin SET hashed_password = %s WHERE username = 'Admin'"
            cursor.execute(update_query, (new_password,))

            # Commit changes and close connection
            conn.commit()
            cursor.close()
            conn.close()
            self.entry_new_password.delete(0, 'end')  # Clear any existing text
            self.entry_confirm_password.delete(0, 'end')  # Clear any existing text
            messagebox.showinfo("Success", "Password changed successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def validate_user_passwords(self):
        """Validates if new password and confirm password match, then updates the database with the hashed password."""
        new_password = self.entry_new_password.get()
        confirm_password = self.entry_confirm_password.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "New Password and Confirm Password do not match!")
            return

        # Get the selected staff username from the dropdown
        selected_username = self.staff_var.get()

        if selected_username == "Select":
            messagebox.showerror("Error", "Please select a staff member!")
            return

        try:
            # Connect to the PostgreSQL database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Update the hashed password for the selected staff user
            update_query = "UPDATE staff SET password = %s WHERE username = %s"
            cursor.execute(update_query, (new_password, selected_username))  # Use the selected username

            # Commit changes and close connection
            conn.commit()
            cursor.close()
            conn.close()
            self.entry_new_password.delete(0, 'end')  # Clear any existing text
            self.entry_confirm_password.delete(0, 'end')  # Clear any existing text
            messagebox.showinfo("Success", "Password changed successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def validate_department_passwords(self):
        """Validates if new password and confirm password match, then updates the database with the hashed password."""
        new_password = self.entry_new_password.get()
        confirm_password = self.entry_confirm_password.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "New Password and Confirm Password do not match!")
            return

        # Get the selected staff username from the dropdown
        selected_username = self.department_var.get()

        if selected_username == "Select":
            messagebox.showerror("Error", "Please select a staff member!")
            return

        try:
            # Connect to the PostgreSQL database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Update the hashed password for the selected staff user
            update_query = "UPDATE departments SET dept_password = %s WHERE dept_name = %s"
            cursor.execute(update_query, (new_password, selected_username))  # Use the selected username

            # Commit changes and close connection
            conn.commit()
            cursor.close()
            conn.close()
            self.entry_new_password.delete(0, 'end')  # Clear any existing text
            self.entry_confirm_password.delete(0, 'end')  # Clear any existing text
            messagebox.showinfo("Success", "Password changed successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def fetch_staff_password(self):
        username = self.staff_var.get()  # Get the selected staff username

        if username != "Select Staff" and username != "No staff members available" and username != "Error loading staff members":

            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Query to get the password for the selected staff
                cursor.execute("SELECT password FROM staff WHERE username = %s", (username,))
                result = cursor.fetchone()

                cursor.close()
                connection.close()

                if result:
                        # Display the password in self.entry_current_password
                    self.entry_current_password.config(state="normal")  # Enable entry for inserting data
                    self.entry_current_password.delete(0, tk.END)  # Clear any existing text
                    self.entry_current_password.insert(0, result[0])  # Assuming result[0] is the password
                    self.entry_current_password.config(state="readonly")  # Assuming result[0] is the password
                else:
                    messagebox.showerror("Error", "No password found for the selected staff.")
            except Exception as error:
                print(f"Error fetching password: {error}")
                messagebox.showerror("Database Error", "Error fetching password.")

    def toggle_view(self):
        """Toggle between displaying staff and departments and update list title."""
        if self.view_mode.get() == "Staff":
            self.populate_listbox_departments()
            self.view_mode.set("Departments")
            self.toggle_button.config(text="Show Staff")
            self.list_title.config(text="Departments List")  # Update title
        else:
            self.populate_listbox_staff()
            self.view_mode.set("Staff")
            self.toggle_button.config(text="Show Departments")
            self.list_title.config(text="Staff List")  # Update title


    def fetch_department_password(self):
        dept_name = self.department_var.get()  # Get the selected staff username

        if dept_name != "Select Staff" and dept_name != "No staff members available" and dept_name != "Error loading staff members":

            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Query to get the password for the selected staff
                cursor.execute("SELECT dept_password FROM departments WHERE dept_name = %s", (dept_name,))
                result = cursor.fetchone()

                cursor.close()
                connection.close()

                if result:
                        # Display the password in self.entry_current_password
                    self.entry_current_password.config(state="normal")  # Enable entry for inserting data
                    self.entry_current_password.delete(0, tk.END)  # Clear any existing text
                    self.entry_current_password.insert(0, result[0])  # Assuming result[0] is the password
                    self.entry_current_password.config(state="readonly")  # Assuming result[0] is the password
                else:
                    messagebox.showerror("Error", "No password found for the selected staff.")
            except Exception as error:
                print(f"Error fetching password: {error}")
                messagebox.showerror("Database Error", "Error fetching password.")





    def update_department_rights(self, event):
        # Get selected department from listbox
        selected_index = self.result_listbox.curselection()
        if not selected_index:
            return

        selected_department = self.result_listbox.get(selected_index[0])

        # Fetch department rights from the database
        try:
            self.conn = get_db_connection()  # Store connection as an instance variable
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT dept_rights FROM departments WHERE dept_name = %s", (selected_department,))
            result = self.cursor.fetchone()

            dept_rights = result[0] if result and result[0] else ""

            # Clear previous form widgets
            for widget in self.central_view.winfo_children():
                widget.destroy()

            # Form Title
            tk.Label(self.central_view, text="Update Rights", font=("Arial", 20)).place(relx=0.5, rely=0.03, anchor="n")

            # Form Frame
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

            # Department Name (Uneditable)
            tk.Label(form_frame, text="Department Name:", font=("Arial", 12)).pack(pady=5)
            dept_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            dept_name_entry.pack(pady=5)
            dept_name_entry.insert(0, selected_department)
            dept_name_entry.config(state="readonly")  # Set to readonly AFTER inserting text

            # Department Rights (Readonly with Add Button)
            tk.Label(form_frame, text="Department Rights:", font=("Arial", 12)).pack(pady=5)

            rights_frame = tk.Frame(form_frame)
            rights_frame.pack(pady=5)

            dept_rights_entry = tk.Entry(rights_frame, font=("Arial", 12), width=25)
            dept_rights_entry.pack(side=tk.LEFT, padx=5)
            dept_rights_entry.insert(0, dept_rights)
            dept_rights_entry.config(state="readonly")

            add_button = tk.Button(rights_frame, text="+", font=("Arial", 12), command=self.open_dept_rights_popup(dept_rights_entry))
            add_button.pack(side=tk.LEFT, padx=5)

            # Save Changes Button
            def save_changes():
                new_rights = dept_rights_entry.get().strip()
                if not new_rights:
                    messagebox.showwarning("Warning", "Rights field cannot be empty.")
                    return

                try:
                    self.cursor.execute("UPDATE departments SET dept_rights = %s WHERE dept_name = %s",
                                        (new_rights, selected_department))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Department rights updated successfully!")

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update department rights: {e}")

            save_button = tk.Button(form_frame, text="Save Changes", font=("Arial", 12), command=save_changes)
            save_button.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")


    def open_dept_rights_popup(self, dept_rights_entry):
        """Opens a popup to manage department rights."""
        popup = tk.Toplevel()
        popup.title("Manage Rights")
        popup.geometry("300x300")
        popup.resizable(False, False)
        self.center_window(popup, 400, 400)
        rights_list = set(dept_rights_entry.get().split(", ")) if dept_rights_entry.get() else set()

        # Input Frame for + and - buttons
        input_frame = tk.Frame(popup)
        input_frame.pack(pady=10)

        rights_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        rights_entry.pack(side=tk.LEFT, padx=5)

        def add_right():
            new_right = rights_entry.get().strip()
            if new_right and new_right not in rights_list:
                rights_list.add(new_right)
                listbox.insert(tk.END, new_right)
                rights_entry.delete(0, tk.END)

        def remove_right():
            selected_index = listbox.curselection()
            if selected_index:
                selected_right = listbox.get(selected_index[0])
                rights_list.discard(selected_right)
                listbox.delete(selected_index[0])

        add_button = tk.Button(input_frame, text="+", font=("Arial", 12), command=add_right)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(input_frame, text="-", font=("Arial", 12), command=remove_right)
        remove_button.pack(side=tk.LEFT, padx=5)

        # Listbox to display rights
        listbox = tk.Listbox(popup, font=("Arial", 12), width=30, height=10)
        listbox.pack(pady=5)

        for right in rights_list:
            listbox.insert(tk.END, right)

        def save_popup():
            updated_rights = ", ".join(sorted(rights_list))
            dept_rights_entry.config(state="normal")
            dept_rights_entry.delete(0, tk.END)
            dept_rights_entry.insert(0, updated_rights)
            dept_rights_entry.config(state="readonly")
            popup.destroy()

        save_popup_button = tk.Button(popup, text="Save", font=("Arial", 12), command=save_popup)
        save_popup_button.pack(pady=10)
