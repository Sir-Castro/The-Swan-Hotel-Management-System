import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import messagebox
from database import get_db_connection

class Departments(tk.Frame):
    def __init__(self, root, username, main_app):
        super().__init__(root)
        self.root = root
        self.username = username  # Data for heads of departments
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

    def create_heads_frame(self):
        # Create the heads frame (on top of the background image)
        heads_frame = tk.Frame(self, bg="lightgray", borderwidth=2, relief="groove")
        heads_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)

        # Title label
        title_label = tk.Label(heads_frame, text=f"{self.username} Department", font=("Arial", 25, "bold"), bg="lightgray")
        title_label.pack(pady=10)


        # Create a frame for arranging buttons and the central view area
        content_frame = tk.Frame(heads_frame, bg="lightgray")
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Button titles
        top_buttons = ["Create Staff", "Delete Staff", "Create Role", "Delete Role", "Assign Role"]
        side_buttons = ["Lock Account", "Unlock Account", "Staff List", "Password Reset", "Logout"]

        # Button width
        button_width = 15  # Set static width for buttons

        # Add top buttons
        top_frame = tk.Frame(content_frame, bg="lightgray")
        top_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10))  # Top row spanning multiple columns

        # Central view area (white box)
        self.central_view = tk.Frame(content_frame, bg="white", width=600, height=450, relief="groove", borderwidth=3)
        self.central_view.grid(row=1, column=1, rowspan=2, columnspan=3, sticky="nsew")

        # Default text inside central view area
        self.default_label = tk.Label(self.central_view, text="Department Dashboard", font=("Arial", 20), bg="white")
        self.default_label.place(relx=0.5, rely=0.5, anchor="center")

        def create_staff_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Create Staff", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=5)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add form fields
            tk.Label(form_frame, text="User ID:", font=("Arial", 12), bg="white").grid(row=0, column=0, pady=10, padx=10, sticky="w")
            self.entry_user_id = tk.Entry(form_frame, state="disabled", font=("Arial", 12))
            self.entry_user_id.grid(row=0, column=1, pady=10, padx=10)

            tk.Label(form_frame, text="Full Name:", font=("Arial", 12), bg="white").grid(row=1, column=0, pady=10, padx=10, sticky="w")
            self.entry_fullname = tk.Entry(form_frame, font=("Arial", 12))
            self.entry_fullname.grid(row=1, column=1, pady=10, padx=10)

            tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="white").grid(row=2, column=0, pady=10, padx=10, sticky="w")
            self.entry_username = tk.Entry(form_frame, font=("Arial", 12))
            self.entry_username.grid(row=2, column=1, pady=10, padx=10)

            tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white").grid(row=3, column=0, pady=10, padx=10, sticky="w")
            self.entry_password = tk.Entry(form_frame, show="*", font=("Arial", 12))
            self.entry_password.grid(row=3, column=1, pady=10, padx=10)

            tk.Label(form_frame, text="Department:", font=("Arial", 12), bg="white").grid(row=4, column=0, pady=10, padx=10, sticky="w")
            self.entry_department = tk.Entry(form_frame)
            self.entry_department.insert(0, self.username)  # Autofill department
            self.entry_department.config(state='readonly')  # Make it uneditable
            self.entry_department.grid(row=4, column=1, pady=10, padx=30, sticky="ew")
            self.entry_department.config(font=("Arial", 12), width=10)

            tk.Label(form_frame, text="User Type:", font=("Arial", 12), bg="white").grid(row=5, column=0, pady=10, padx=10, sticky="w")
            self.user_type_var = tk.StringVar()
            self.user_type_var.set("Select")
            self.dropdown_user_type = tk.OptionMenu(form_frame, self.user_type_var, "Supervisor", "Staff")
            self.dropdown_user_type.grid(row=5, column=1, pady=10, padx=10, sticky="w")
            self.dropdown_user_type.config(font=("Arial", 12), width=20)

            # Submit button
            tk.Button(form_frame, text="Submit", font=("Arial", 12), bg="black", fg="white", command=self.create_staff).grid(row=6, column=0, columnspan=2, pady=20)
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

        def staff_list_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Staff List", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=430, height=350)

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
            self.populate_listbox_staff3()

        def delete_role_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Delete Role", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)


            # Frame for listbox and scrollbar
            listbox_frame = tk.Frame(form_frame)
            listbox_frame.pack(pady=30, padx=10, fill=tk.BOTH, expand=True)
            list_title = tk.Label(listbox_frame, text="Roles", font=("Arial", 12), fg="black")
            list_title.pack(side=tk.TOP, pady=1)


            # Scrollable list for displaying search results
            self.result_listbox = tk.Listbox(listbox_frame, font=("Arial", 12), width=20, height=1)
            self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Make the listbox scrollable
            scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
            scrollbar.config(command=self.result_listbox.yview)
            self.result_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.fetch_roles()

            self.result_listbox.bind("<Double-1>", lambda event: self.confirm_delete_role())

        def create_role_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Create Role", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Create Role Label and Input
            tk.Label(form_frame, text="Create Role:", font=("Arial", 12), fg="black", bg="lightgray").place(relx=0.5, rely=0.25, anchor="n")
            self.role_name_var = tk.StringVar()

            # Create and assign entry field for role name to self.entry_role_name
            self.entry_role_name = tk.Entry(form_frame, textvariable=self.role_name_var, width=17, bg="white")
            self.entry_role_name.place(relx=0.5, rely=0.4, anchor="n")

            save_role_button = tk.Button(form_frame, text="Save Role", font=("Arial", 12), command=self.save_role, fg="black", bg="lightgray")
            save_role_button.place(relx=0.5, rely=0.5, anchor="n")

        def assign_role_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Assign Role", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add instructions
            instructions = tk.Label(form_frame, text="Select user:", font=("Arial", 14), bg="white")
            instructions.place(relx=0.2, rely=0.3, anchor="n")  # Position at 10% height of the frame
            # Select User Dropdown
            self.user_var = tk.StringVar()
            self.user_var.set("Select")
            self.dropdown_user = tk.OptionMenu(form_frame, self.user_var, "Select")  # Added at least one option
            self.dropdown_user.place(relx=0.4, rely=0.35, anchor="w")
            self.dropdown_user.config(font=("Arial", 12), width=15)
            self.update_staff_dropdown()
            #self.user_var.trace("w", self.on_staff_selected)

            # Add instructions
            instructions = tk.Label(form_frame, text="Select role:", font=("Arial", 14), bg="white")
            instructions.place(relx=0.2, rely=0.45, anchor="n")  # Position at 10% height of the frame
            # Select Role Dropdown
            self.role_var = tk.StringVar()
            self.role_var.set("Select")
            self.dropdown_role = tk.OptionMenu(form_frame, self.role_var, "Select")  # Added at least one option
            self.dropdown_role.place(relx=0.4, rely=0.5, anchor="w")
            self.dropdown_role.config(font=("Arial", 12), width=15)
            self.update_role_dropdown()

            # Update Button
            update_button = tk.Button(
                form_frame, text="Update", font=("Arial", 12), 
                command=self.assign_role_to_user, fg="black", bg="lightgray"
            )
            update_button.place(relx=0.5, rely=0.8, anchor="center")  # Center the button properly

        def lock_account_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Lock Account", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add instructions
            instructions = tk.Label(form_frame, text="Select user:", font=("Arial", 12), bg="white")
            instructions.place(relx=0.5, rely=0.25, anchor="n")  # Position at 10% height of the frame

            self.user_var = tk.StringVar()
            self.user_var.set("Select")
            self.dropdown_user = tk.OptionMenu(form_frame, self.user_var, "Select")  # Added at least one option
            self.dropdown_user.place(relx=0.5, rely=0.4, anchor="n")
            self.dropdown_user.config(font=("Arial", 12), width=10)
            self.update_staff_dropdown()

            # Button to delete the selected user
            button_delete_user = tk.Button(form_frame, text="Lock Account", command=self.lock_account, font=("Arial", 12))
            button_delete_user.place(relx=0.5, rely=0.6, anchor="n")  # Position closer to the bottom

        def unlock_account_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Unlock Account", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add instructions
            instructions = tk.Label(form_frame, text="Select user:", font=("Arial", 12), bg="white")
            instructions.place(relx=0.5, rely=0.25, anchor="n")  # Position at 10% height of the frame

            self.user_var = tk.StringVar()
            self.user_var.set("Select")
            self.dropdown_user = tk.OptionMenu(form_frame, self.user_var, "Select")  # Added at least one option
            self.dropdown_user.place(relx=0.5, rely=0.4, anchor="n")
            self.dropdown_user.config(font=("Arial", 12), width=10)
            self.update_staff_dropdown()

            # Button to delete the selected user
            button_delete_user = tk.Button(form_frame, text="Unlock Account", command=self.unlock_account, font=("Arial", 12))
            button_delete_user.place(relx=0.5, rely=0.6, anchor="n")  # Position closer to the bottom

        def pass_reset_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Password Reset", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add instructions
            instructions = tk.Label(form_frame, text="Select user to delete", font=("Arial", 12), bg="white")
            instructions.place(relx=0.5, rely=0.25, anchor="n")  # Position at 10% height of the frame

            # Search field
            self.search_var = tk.StringVar(form_frame)
            self.search_entry = tk.Entry(form_frame, textvariable=self.search_var, state="normal", width=20)  # Enable the entry field
            self.search_entry.place(relx=0.5, rely=0.4, anchor="n")  # Centered below search button

            # Button to delete the selected user
            button_delete_user = tk.Button(form_frame, text="Delete User", font=("Arial", 12))
            button_delete_user.place(relx=0.5, rely=0.5, anchor="n")  # Position closer to the bottom

        def pass_reset_form():
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

            self.update_staff_dropdown2()
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

        def update_records_form():
            self.clear_central_view()

            form_title = tk.Label(self.central_view, text="Update Records", font=("Arial", 20))
            form_title.place(relx=0.5, rely=0.03, anchor="n")  # Adjust form title position

            # Create a frame to hold the form with a border
            form_frame = tk.Frame(self.central_view, bg="white", relief="groove", borderwidth=10)
            form_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=350)

            # Add instructions
            instructions = tk.Label(form_frame, text="Select user to delete", font=("Arial", 12), bg="white")
            instructions.place(relx=0.5, rely=0.25, anchor="n")  # Position at 10% height of the frame

            # Search field
            self.search_var = tk.StringVar(form_frame)
            self.search_entry = tk.Entry(form_frame, textvariable=self.search_var, state="normal", width=20)  # Enable the entry field
            self.search_entry.place(relx=0.5, rely=0.4, anchor="n")  # Centered below search button

            # Button to delete the selected user
            button_delete_user = tk.Button(form_frame, text="Delete User", font=("Arial", 12))
            button_delete_user.place(relx=0.5, rely=0.5, anchor="n")  # Position closer to the bottom

        # Add top buttons
        for title in top_buttons:
            if title == "Create Staff":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=create_staff_form)
            elif title == "Delete Staff":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=delete_staff_form)
            elif title == "Create Role":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=create_role_form)
            elif title == "Delete Role":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=delete_role_form)
            elif title == "Assign Role":
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width, command=assign_role_form)
            else:
                button = tk.Button(top_frame, text=title, bg="black", fg="white", font=("Arial", 10), width=button_width)
            button.pack(side="left", padx=10)


        # Assigning commands to side buttons
        side_frame = tk.Frame(content_frame, bg="lightgray")
        side_frame.grid(row=1, column=0, sticky="ns", rowspan=3)  # Left column

        for button_text in side_buttons:
            if button_text == "Lock Account":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=lock_account_form)
            elif button_text == "Unlock Account":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=unlock_account_form)
            elif button_text == "Staff List":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=staff_list_form)
            elif button_text == "Password Reset":
                button = tk.Button(side_frame, text=button_text, width=button_width, font=("Arial", 10), bg="black", fg="white", command=pass_reset_form)
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

    def search_staff_for_deletion(self):
            """Search for staff members based on the selected criteria and the department of the logged-in user."""
            criteria = self.search_criteria_var.get()
            search_value = self.entry_search.get().strip()

            try:
                connection = get_db_connection()
                cursor = connection.cursor()

                if not search_value:
                    # If no search value is given, retrieve all staff in the logged-in department
                    query = "SELECT user_id, username FROM staff WHERE department = %s"
                    cursor.execute(query, (self.username,))  # Assuming self.username holds the logged-in department name
                elif criteria == "Username":
                    query = "SELECT user_id, username FROM staff WHERE username ILIKE %s AND department = %s"
                    cursor.execute(query, (f"%{search_value}%", self.username))  # Filter by department
                else:  # criteria == "User ID"
                    query = "SELECT user_id, username FROM staff WHERE user_id = %s AND department = %s"
                    cursor.execute(query, (search_value, self.username))  # Filter by department

                results = cursor.fetchall()
                self.result_listbox.delete(0, tk.END)  # Clear previous results

                for user_id, username in results:
                    self.result_listbox.insert(tk.END, f"User ID: {user_id}, Username: {username}")

            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                if connection:
                    cursor.close()
                    connection.close()


    def delete_selected_staff(self):
        """Delete the selected staff member from the database."""
        selected_item = self.result_listbox.get(self.result_listbox.curselection())

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a staff member to delete.")
            return

        # Extract user_id from the selected item
        user_id = selected_item.split(",")[0].split(":")[1].strip()

        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete User ID: {user_id}?")

        if confirmation:
            try:
                connection = get_db_connection()
                cursor = connection.cursor()

                # Delete the selected staff member
                delete_query = "DELETE FROM staff WHERE user_id = %s"
                cursor.execute(delete_query, (user_id,))
                connection.commit()

                # Remove the item from the listbox
                self.result_listbox.delete(self.result_listbox.curselection())

                messagebox.showinfo("Success", "Staff member deleted successfully.")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                if connection:
                    cursor.close()
                    connection.close()
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

    def create_staff(self):
        user_id = self.entry_user_id.get()
        fullname = self.entry_fullname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        department = self.entry_department.get()
        user_type = self.user_type_var.get()  # Capture user type from dropdown

        if not user_id or not username or not fullname or not password or user_type == "Select":
            messagebox.showerror("Input Error", "Please fill all fields and select a user type.")
            return

        # Connect to the PostgreSQL database and insert the staff data
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Create a new staff entry with the selected user_type
            insert_query = """
            INSERT INTO staff (user_id, fullname, username, department, password, user_type, lock_status, role_name) 
            VALUES (%s, %s, %s, %s, %s, %s, FALSE, NULL)
            """
            cursor.execute(insert_query, (user_id, fullname, username, department, password, user_type))

            connection.commit()
            messagebox.showinfo("Success", "Staff created successfully.")

            # Clear input fields
            self.entry_user_id.delete(0, tk.END)
            self.entry_fullname.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.user_type_var.set("Select")  # Reset dropdown selection

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
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
            cursor.execute("SELECT username, fullname FROM staff WHERE department = %s", (self.username,))
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

    def populate_listbox_staff3(self):
        """Fetch staff usernames, full names, user types, roles, and lock status, then populate the listbox."""
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Retrieve relevant details from the `staff` table
            cursor.execute("SELECT username, fullname, user_type, role_name, lock_status FROM staff WHERE department = %s", (self.username,))
            staff = cursor.fetchall()

            # Clear the listbox and add the formatted staff details
            self.result_listbox.delete(0, tk.END)
            for username, fullname, user_type, role_name, lock_status in staff:
                # Convert lock_status to a readable format
                account_status = "Locked" if lock_status else "Unlocked"

                display_text = f"{username} | {fullname} | {user_type} | Role: {role_name} | Account: {account_status}"
                self.result_listbox.insert(tk.END, display_text)

        except Exception as error:
            messagebox.showerror("Database Error", f"Error retrieving staff: {error}")

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
                self.populate_listbox_staff2()
            else:
                messagebox.showwarning("Not Found", f"User '{username}' does not exist in the database.")

        except Exception as error:
            messagebox.showerror("Database Error", f"Error deleting user: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def fetch_roles(self):
        """Fetch roles from the database."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT role_id, role_name FROM roles WHERE department = %s", (self.username,)) # Ensure both fields are fetched
            role_list = cursor.fetchall()  # Fetch all data as tuples
            
                        # Clear the listbox and add the formatted staff details
            self.result_listbox.delete(0, tk.END)
            for role_id, role_name in role_list:
                display_text = f"{role_name}"
                self.result_listbox.insert(tk.END, display_text)

            return role_list  # Expecting list of tuples (role_id, role_name)
        
        except Exception as e:
            print("Error fetching roles:", e)
            return []  # Return an empty list in case of an error
        
        finally:
            if connection:
                cursor.close()
                connection.close()

    def save_role(self):
        """Save the new role to the roles table with department info."""
        role_name = self.entry_role_name.get()
        
        if not role_name:
            messagebox.showwarning("Input Error", "Please enter a role name.")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch department based on logged-in user
            cursor.execute("SELECT department FROM staff WHERE department = %s", (self.username,))
            department = cursor.fetchone()
            
            if not department:
                messagebox.showerror("Error", "Department not found for the logged-in user.")
                return
            
            department = department[0]  # Extract department value

            # Check if the role already exists
            cursor.execute("SELECT COUNT(*) FROM roles WHERE role_name = %s", (role_name,))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Duplicate Entry", "This role already exists.")
                return

            # Insert the new role with department
            cursor.execute("INSERT INTO roles (role_name, department) VALUES (%s, %s)", (role_name, department))
            connection.commit()

            messagebox.showinfo("Success", f" '{role_name}' role assigned in  '{department}' department saved successfully.")
            self.entry_role_name.delete(0, tk.END)  # Clear the entry field

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if connection:
                cursor.close()
                connection.close()

    def confirm_delete_role(self):
        """Open a confirmation dialog to ask if the user is sure about deleting the selected role."""
        selected_role = self.result_listbox.get(tk.ACTIVE)  # Get selected role

        if not selected_role:
            messagebox.showwarning("Selection Error", "Please select a role to delete.")
            return
        
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_role}'?")
        if response:
            self.delete_role(selected_role)  # Pass correct role name



    def assign_role(self):
        """Assign the selected role to the selected user."""
        selected_user = self.user_selection_var.get()
        selected_role = self.role_selection_var.get()
        
        if not selected_user or selected_role == "Roles":  # Assuming "Roles" is the default text
            messagebox.showwarning("Input Error", "Please select a user and a role.")
            return
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Get the user ID
            user_id = self.get_staff_id(selected_user)
            
            if user_id is None:
                messagebox.showwarning("Data Error", "Invalid user selected.")
                return
            
            # Get username and role name to store
            username = selected_user  # This should match the dropdown selection
            role_name = selected_role  # This should match the dropdown selection

            # Update the role name for the selected user in the staff table
            cursor.execute("""
                UPDATE staff 
                SET role_name = %s
                WHERE user_id = %s
            """, (role_name, user_id))

            # Commit the transaction
            connection.commit()
            messagebox.showinfo("Success", "Role assigned and updated successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete_role(self, role_name):
        """Delete the selected role from the database."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch the role_id of the role_name to be deleted
            cursor.execute("SELECT role_id FROM roles WHERE role_name = %s", (role_name,))
            role_id_result = cursor.fetchone()

            if not role_id_result:
                messagebox.showwarning("Delete Error", f"Role '{role_name}' does not exist.")
                return

            role_id = role_id_result[0]  # Extract role_id

            # Delete or update records in the staff_roles table
            cursor.execute("DELETE FROM roles WHERE role_id = %s", (role_id,))
            connection.commit()

            # Optionally, update the staff table for users with this role
            cursor.execute("UPDATE staff SET role_name = NULL WHERE role_name = %s", (role_name,))
            connection.commit()

            # Finally, delete the role from the roles table
            cursor.execute("DELETE FROM roles WHERE role_id = %s", (role_id,))
            connection.commit()

            # Show success message
            messagebox.showinfo("Success", f"Role '{role_name}' deleted.")

            # Refresh the listbox
            self.fetch_roles()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()


    def get_role_id(self, role_name):
        """Retrieve role ID based on role name."""
        role_id = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT role_id, role_name FROM roles WHERE role_name = %s", (role_name,))
            result = cursor.fetchone()
            
            if result:
                role_id = result[0]  # Get the first element, which is role_id
        except Exception as e:
            print("Error fetching role ID:", e)
        finally:
            if connection:
                cursor.close()
                connection.close()
        
        return role_id

    def center_window(self, window, width, height):
        """Center the window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def update_staff_dropdown(self):
        self.dropdown_user['menu'].delete(0, 'end')

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all usernames from the staff table
            cursor.execute("SELECT username FROM staff WHERE department = %s", (self.username,))
            staff_members = cursor.fetchall()  # Fetch all usernames

            if staff_members:
                for member in staff_members:  # Iterate over the fetched staff members
                    username = member[0]  # Access the first element in the tuple (username)
                    self.dropdown_user['menu'].add_command(
                        label=username, 
                        command=tk._setit(self.user_var, username)
                    )
            else:
                self.user_var.set("No records")

        except Exception as error:
            print(f"Error fetching staff members: {error}")
            self.user_var.set("Error loading staff members")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def update_staff_dropdown2(self):
        self.dropdown_staff['menu'].delete(0, 'end')

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all usernames from the staff table
            cursor.execute("SELECT username FROM staff WHERE department = %s", (self.username,))
            staff_members = cursor.fetchall()  # Fetch all usernames

            if staff_members:
                for member in staff_members:  # Iterate over the fetched staff members
                    username = member[0]  # Access the first element in the tuple (username)
                    self.dropdown_staff['menu'].add_command(
                        label=username, 
                        command=tk._setit(self.staff_var, username)
                    )
            else:
                self.staff_var.set("No records")

        except Exception as error:
            print(f"Error fetching staff members: {error}")
            self.staff_var.set("Error loading staff members")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def update_role_dropdown(self):
        self.dropdown_role['menu'].delete(0, 'end')

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all usernames from the staff table
            cursor.execute("SELECT role_name FROM roles WHERE department = %s", (self.username,))
            staff_members = cursor.fetchall()  # Fetch all usernames

            if staff_members:
                for member in staff_members:  # Iterate over the fetched staff members
                    username = member[0]  # Access the first element in the tuple (username)
                    self.dropdown_role['menu'].add_command(
                        label=username, 
                        command=tk._setit(self.role_var, username)
                    )
            else:
                self.role_var.set("No records")

        except Exception as error:
            print(f"Error fetching staff members: {error}")
            self.role_var.set("Error loading staff members")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def assign_role_to_user(self):
        selected_user = self.user_var.get()
        selected_role = self.role_var.get()

        if selected_user == "Select" or selected_role == "Select":
            print("Please select both a user and a role.")
            return  # Exit the function if selections are invalid

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Update the staff table to assign the selected role to the selected user
            update_query = """
            UPDATE staff SET role_name = %s WHERE username = %s
            """
            cursor.execute(update_query, (selected_role, selected_user))
            connection.commit()  # Commit changes

            messagebox.showinfo("Success", f"Role {selected_role} assigned to {selected_user}.")
            # Clear selections after update
            self.user_var.set("Select")
            self.role_var.set("Select")
        except Exception as error:
            print(f"Error updating role: {error}")
            connection.rollback()  # Rollback in case of failure

        finally:
            if connection:
                cursor.close()
                connection.close()
    def lock_account(self):
        selected_user = self.user_var.get()
        if selected_user != "Select User":
            # Fetch the current lock status from the staff table
            lock_status = self.get_lock_status(selected_user)

            if lock_status:  # Account is already locked
                messagebox.showinfo("Account Locked", f"Account {selected_user} is already locked.")
                self.user_var.set("Select")
            else:
                # Lock the account (update lock_status to False)
                self.update_lock_status(selected_user, True)
                messagebox.showinfo("Account Locked", f"Account {selected_user} has been locked successfully.")
                self.user_var.set("Select")
        else:
            messagebox.showwarning("Select User", "Please select a user first.")

    def unlock_account(self):
        selected_user = self.user_var.get()
        if selected_user != "Select User":
            # Fetch the current lock status from the staff table
            lock_status = self.get_lock_status(selected_user)

            if not lock_status:  # Account is already unlocked
                messagebox.showinfo("Account Unlocked", f"Account {selected_user} is already unlocked.")
                self.user_var.set("Select")
            else:
                # Unlock the account (update lock_status to True)
                self.update_lock_status(selected_user, False)
                messagebox.showinfo("Account Unlocked", f"Account {selected_user} has been unlocked successfully.")
                self.user_var.set("Select")

        else:
            messagebox.showwarning("Select User", "Please select a user first.")

    def get_lock_status(self, username):
        """Fetch the lock status of a user from the staff table."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch the lock status of the user from the staff table based on username
        cursor.execute("SELECT lock_status FROM staff WHERE username = %s;", (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result[0]  # Return the lock status (True/False)
        else:
            return None  # Return None if user is not found

    def update_lock_status(self, username, new_lock_status):
        """Update the lock status of a user in the staff table."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the lock status in the staff table for the given username
        cursor.execute("UPDATE staff SET lock_status = %s WHERE username = %s;", (new_lock_status, username))

        conn.commit()
        cursor.close()
        conn.close()

    def on_staff_selected(self, *args):
        selected_staff = self.staff_var.get()
        if selected_staff != "Select":
            self.fetch_staff_password()

    def fetch_staff_password(self):
        username = self.staff_var.get()  # Get the selected staff username

        if username != "Select Staff" and username != "No records" and username != "Error loading staff members":

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

    def toggle_password(self):
        if self.entry_current_password.cget("show") == "*":
            self.entry_current_password.config(show="")
            self.toggle_button.config(text="Hide")
        else:
            self.entry_current_password.config(show="*")
            self.toggle_button.config(text="Show")

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