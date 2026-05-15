import tkinter as tk
from tkinter import ttk

from tkinter import messagebox
from PIL import Image, ImageTk
from database import get_db_connection
from psycopg2 import sql
import psycopg2
from tkcalendar import Calendar
from tkinter import font

class Departments(tk.Frame):
    def __init__(self, root, username, main_app):
        super().__init__(root)  
        self.root = root
        self.username = username
        self.main_app = main_app  

        # Set up background image
        self.background_image = Image.open("images/lounge4.jpg")
        self.background_image = self.background_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        )
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Create layout frames
        self.frame_left = tk.Frame(self.root, borderwidth=8, relief="groove", bg="black")
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_right = tk.Frame(self.root, borderwidth=8, relief="groove", bg="black")
        self.frame_right.pack(side=tk.RIGHT, fill=tk.Y)

        self.frame_bottom = tk.Frame(self.root, borderwidth=8, relief="groove", bg="black")
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.Y) 

        # Start the fade-in effect
        self.show_logo_with_fade()

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
            self.logo_label.place_forget()
            # Once fully faded out, display the main content
            self.create_staff_box()
            self.create_button_container()
            self.edit_staff_box()
            self.delete_staff_box()
            self.roles_box()
            self.print_logs_box()
            self.lock_account_box()



    def create_button_container(self):
        # Create a black container frame to hold all the buttons
        button_container = tk.Frame(self.frame_bottom, borderwidth=8, relief="groove", bg="lightgray", height=200, width=500)
        button_container.pack(side=tk.RIGHT, padx=5, pady=10, fill=tk.BOTH)

        button_container.pack_propagate(False)

        # Add a centered title at the top of the container
        title_label = tk.Label(button_container, text="Operations", font=("Arial", 22), fg="black", bg="white")
        title_label.grid(row=0, column=0, columnspan=4, pady=20)  # Centered title with padding

        # Create buttons inside the container and position them
        refresh_button = tk.Button(button_container, borderwidth=1, text="Refresh", command=self.refresh, font=("Arial", 16),  bg="black", fg="white", width=7, height=1)
        refresh_button.grid(row=4, column=1, padx=10, pady=20)

        logout_button = tk.Button(button_container, borderwidth=1, text="Logout", command=self.logout, font=("Arial", 16), bg="black", fg="white", width=7, height=1)
        logout_button.grid(row=4, column=2, padx=10, pady=20)

        reports_button = tk.Button(button_container, borderwidth=5, text="Reports", command=self.refresh, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        reports_button.grid(row=1, column=0, padx=5, pady=5)

        audit_button = tk.Button(button_container, borderwidth=5, text="Audit", command=self.logout, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        audit_button.grid(row=1, column=2, padx=5, pady=5)

        systems_button = tk.Button(button_container, borderwidth=5, text="Systems", command=self.refresh, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        systems_button.grid(row=2, column=0, padx=5, pady=5)

        logs_button = tk.Button(button_container, borderwidth=5, text="Logs", command=self.logout, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        logs_button.grid(row=1, column=1, padx=5, pady=5)

        rights_button = tk.Button(button_container, borderwidth=5, text="Rights", command=self.refresh, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        rights_button.grid(row=2, column=1, padx=5, pady=5)

        sessions_button = tk.Button(button_container, borderwidth=5, text="Sessions", command=self.logout, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        sessions_button.grid(row=2, column=2, padx=5, pady=5)

        summary_button = tk.Button(button_container, borderwidth=5, text="Summary", command=self.refresh, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        summary_button.grid(row=1, column=3, padx=5, pady=5)

        functions_button = tk.Button(button_container, borderwidth=5, text="Functions", command=self.logout, font=("Arial", 16), bg="lightgray", fg="black", width=7, height=1)
        functions_button.grid(row=2, column=3, padx=5, pady=5)

        # Call the method to create the manage admin box


    def create_staff_box(self):
        manage_admin_frame = tk.Frame(self.frame_left, borderwidth=8, relief="groove", bg="lightgray", width=250, height=370)
        manage_admin_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        manage_admin_frame.pack_propagate(False)

        title_label = tk.Label(manage_admin_frame, text="Create Staff", font=("Arial", 22), fg="black")
        title_label.pack(pady=10)

        tk.Label(manage_admin_frame, text="User ID:", fg="black", bg="lightgray", font=("Arial", 12)).pack(pady=5)
        self.entry_user_id = tk.Entry(manage_admin_frame, state="disabled")
        self.entry_user_id.pack(pady=5)

        tk.Label(manage_admin_frame, text="Full name:", fg="black", bg="lightgray", font=("Arial", 12)).pack(pady=5)
        self.entry_fullname = tk.Entry(manage_admin_frame)
        self.entry_fullname.pack(pady=5)

        tk.Label(manage_admin_frame, text="Username:", fg="black", bg="lightgray", font=("Arial", 12)).pack(pady=5)
        self.entry_username = tk.Entry(manage_admin_frame)
        self.entry_username.pack(pady=5)

        tk.Label(manage_admin_frame, text="Department:", fg="black", bg="lightgray", font=("Arial", 12)).pack(pady=5)
        self.entry_department = tk.Entry(manage_admin_frame)
        self.entry_department.insert(0, self.username)  # Autofill department
        self.entry_department.config(state='readonly')  # Make it uneditable
        self.entry_department.pack(pady=5)

        tk.Label(manage_admin_frame, text="Password:", fg="black", bg="lightgray", font=("Arial", 12)).pack(pady=5)
        self.entry_password = tk.Entry(manage_admin_frame, show='*')
        self.entry_password.pack(pady=5)

        button_create = tk.Button(manage_admin_frame, text="Create Staff", font=("Arial", 12), command=self.create_staff, fg="black")
        button_create.pack(pady=10)
        self.generate_user_id()

    def delete_staff_box(self):
        # Create the manage admin frame with specified width and height
        manage_admin_frame = tk.Frame(self.frame_left, borderwidth=8, relief="groove", bg="lightgray", width=250, height=200)
        manage_admin_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        custom_font = font.Font(family="Arial", size=12)
        # Make the frame size consistent
        manage_admin_frame.pack_propagate(False)

        # Title label for the delete staff box
        title_label = tk.Label(manage_admin_frame, text="Delete Staff", font=("Arial", 22), fg="black")
        title_label.pack(pady=10)

        # Dropdown for selecting search criteria
        self.search_criteria_var = tk.StringVar(value="Search by")
        criteria_options = ["Username", "User ID"]
        self.criteria_dropdown = tk.OptionMenu(manage_admin_frame, self.search_criteria_var, *criteria_options)
        self.criteria_dropdown.pack(pady=5)


        # Frame for the search box and button
        search_frame = tk.Frame(manage_admin_frame, bg="lightgray")
        search_frame.pack(pady=5)

        # Search box
        self.entry_search = tk.Entry(search_frame)
        self.entry_search.pack(side=tk.LEFT, padx=2)

        # Search button
        search_button = tk.Button(search_frame, text="Search", font=("Arial", 12), command=self.search_staff_for_deletion, fg="black")
        search_button.pack(side=tk.LEFT, padx=5)

        # Frame for listbox and scrollbar
        listbox_frame = tk.Frame(manage_admin_frame)
        listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Scrollable list for displaying search results
        self.result_listbox = tk.Listbox(listbox_frame, width=20, height=1)
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Make the listbox scrollable
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.result_listbox.yview)
        self.result_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 

        # Button to delete selected staff member
        delete_button = tk.Button(manage_admin_frame, text="Delete", font=("Arial", 12), command=self.delete_selected_staff, fg="black")
        delete_button.pack(pady=5)

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
    def edit_staff_box(self):
        # Create the manage admin frame with specified width and height
        manage_admin_frame = tk.Frame(self, borderwidth=8, relief="groove", bg="lightgray", width=520, height=500)
        manage_admin_frame.pack(padx=10, pady=10, anchor="n", fill=tk.X) 

        manage_admin_frame.pack_propagate(False)

        # Title label for the edit staff box
        title_label = tk.Label(manage_admin_frame, text=f"{self.username} Department", font=("Arial", 22), fg="black")
        title_label.pack(pady=10)

        # Text widget for displaying all users
        self.result_text = tk.Text(manage_admin_frame, height=10, wrap=tk.WORD, fg="black", font=("Arial", 10))
        self.result_text.pack(pady=3, padx=3, fill=tk.BOTH, expand=True)

        # Disable editing the text widget
        self.result_text.config(state=tk.DISABLED)

        # Enable scrolling with the mouse wheel
        self.result_text.bind("<MouseWheel>", self.scroll_listbox)

        # Populate the listbox with all users
        self.populate_user_list()

    def scroll_listbox(self, event):
        """Scroll the listbox using the mouse wheel."""
        # Use the event.delta value to scroll
        self.result_listbox.yview_scroll(-1 * (event.delta // 120), "units")

    def populate_user_list(self):
        """Fetch users from the database whose departments match the logged-in department and display them in the text widget."""
        try:
            connection = get_db_connection()  # Replace this with your database connection method
            cursor = connection.cursor()

            # Fetch user IDs, usernames, user types, roles, and lock status where the department matches the logged-in department
            query = """
                SELECT user_id, username, user_type, role_name, lock_status
                FROM staff 
                WHERE department = %s
                ORDER BY username ASC
            """
            cursor.execute(query, (self.username,))  # Assuming self.username holds the current department
            results = cursor.fetchall()

            # Clear previous entries in the text widget
            self.result_text.config(state=tk.NORMAL)  # Enable text widget for editing
            self.result_text.delete(1.0, tk.END)

            if not results:
                self.result_text.insert(tk.END, "No users found for this department.")
            else:
                for row in results:
                    # Get lock status and display the appropriate message
                    lock_status = "Locked" if row[4] else "Unlocked"
                    
                    # Insert user data in the text widget
                    self.result_text.insert(tk.END, f"ID: {row[0]}, Username: {row[1]}, User: {row[2]}, Role: {row[3]}, Account: {lock_status}\n")
            
            self.result_text.config(state=tk.DISABLED)  # Disable text widget for editing

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()



    def roles_box(self):
        # Create the main frame for roles management
        manage_roles_frame = tk.Frame(self.frame_bottom, borderwidth=8, relief="groove", bg="lightgray", width=230, height=350)
        manage_roles_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)  # Positioned to the left

        # Make the frame size consistent
        manage_roles_frame.pack_propagate(False)

        # Title label for the User Roles box
        title_label = tk.Label(manage_roles_frame, text="User Roles", font=("Arial", 22), fg="black", bg="white")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)  # Title spans both columns

        # Create the Create Role frame (top-left)
        create_role_frame = tk.Frame(manage_roles_frame, bg="lightgray")
        create_role_frame.grid(row=1, column=0, padx=10, pady=5)

        # Create Role Label and Input
        tk.Label(create_role_frame, text="Create Role:", font=("Arial", 12), fg="black", bg="lightgray").pack(pady=5)
        self.role_name_var = tk.StringVar()

        # Create and assign entry field for role name to self.entry_role_name
        self.entry_role_name = tk.Entry(create_role_frame, textvariable=self.role_name_var, width=17, bg="white")
        self.entry_role_name.pack(pady=5)

        save_role_button = tk.Button(create_role_frame, text="Save Role", font=("Arial", 12), command=self.save_role, fg="black", bg="lightgray")
        save_role_button.pack(pady=5)

        # Create the Delete Role frame (below the Create Role frame)
        delete_role_frame = tk.Frame(manage_roles_frame, bg="lightgray")
        delete_role_frame.grid(row=2, column=0, padx=10, pady=5)

        # Delete Role Label
        self.selected_role = tk.StringVar(value="Roles")  # Default text is "Search"
        tk.Label(delete_role_frame, text="Delete Role:", font=("Arial", 12), fg="black", bg="lightgray").pack(pady=10)

        # Search Button to open the role list popup
        search_button = tk.Button(delete_role_frame, text="Select", font=("Arial", 12), command=self.open_role_search_popup, fg="black", bg="lightgray")
        search_button.pack(pady=5)

        # Create the Assign Role frame (beside the Create and Delete Role frames)
        assign_role_frame = tk.Frame(manage_roles_frame, bg="lightgray")
        assign_role_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=5)

        # Assign Role Label and User Dropdown
        tk.Label(assign_role_frame, text="Select User:", bg="lightgray", font=("Arial", 12)).pack(pady=5)

        self.user_selection_var = tk.StringVar(value="Users")  # Default text for user selection

        # Fetch the staff members
        staff_list = self.fetch_staff()  # Ensure this returns a list of tuples like [(id, username), ...]

        # Check if the staff list is not empty
        if staff_list:
            staff_options = [user for user in staff_list]  # The list should now contain only usernames
            self.user_dropdown = tk.OptionMenu(assign_role_frame, self.user_selection_var, *staff_options)
            self.user_dropdown.pack(pady=5)
        else:
            tk.Label(assign_role_frame, text="No users found", font=("Arial", 12), fg="black", bg="lightgray").pack(pady=5)

        # Dropdown for assigning a role
        tk.Label(assign_role_frame, text="Assign Role:", font=("Arial", 12), fg="black", bg="lightgray").pack(pady=5)
        self.role_selection_var = tk.StringVar(value="Roles")  # Default text for role selection

        role_list = self.fetch_roles()  # Ensure this returns a list of tuples like [(id, role_name), ...]

        if role_list:
            role_options = [role[1] for role in role_list]  # Extract role names from the list
            self.role_dropdown = tk.OptionMenu(assign_role_frame, self.role_selection_var, *role_options)
            self.role_dropdown.pack(pady=5)
        else:
            tk.Label(assign_role_frame, text="No roles found", font=("Arial", 12), fg="black", bg="lightgray").pack(pady=5)

        update_button = tk.Button(assign_role_frame, text="Update", font=("Arial", 12), command=self.assign_role, fg="black", bg="lightgray")
        update_button.pack(pady=5)


    def print_logs_box(self):
        # Create the manage admin frame with specified width and height
        manage_admin_frame = tk.Frame(self.frame_right, borderwidth=8, relief="groove", bg="lightgray", width=250, height=310)
        manage_admin_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Prevent the frame from resizing to fit its contents
        manage_admin_frame.pack_propagate(False)

        # Title label for the manage admin box
        title_label = tk.Label(manage_admin_frame, text="Print logs", font=("Arial", 22), fg="black", bg="white",)
        title_label.pack(pady=10)

        # Dropdown for Select User
        tk.Label(manage_admin_frame, text="Select User:", bg="lightgray", font=("Arial", 12), fg="black", ).pack(pady=5)
        self.user_combobox = ttk.Combobox(manage_admin_frame, state="readonly")
        self.user_combobox.set("Select User")  # Default placeholder text
        self.user_combobox.pack(pady=5)

        # Fetch the list of users from `fetch_staff` method (assumed to return a list of usernames)
        user_list = self.fetch_staff()  # Assuming fetch_staff() method exists and returns a list of usernames
        self.user_combobox['values'] = user_list  # Populate the combobox with usernames

        # Start Date input field in dd/mm/yy format with hint
        self.start_date_label = tk.Label(manage_admin_frame, text="Start Date:", bg="lightgray", font=("Arial", 12), fg="black")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = tk.Entry(manage_admin_frame, justify='center')
        self.start_date_entry.insert(0, "DD/MM/YY")  # Insert the hint text
        self.start_date_entry.bind("<FocusIn>", self.clear_hint)  # Clear the hint text on focus
        self.start_date_entry.bind("<FocusOut>", self.set_hint)  # Restore hint text if empty
        self.start_date_entry.pack(pady=5)

        # End Date input field in dd/mm/yy format with hint
        self.end_date_label = tk.Label(manage_admin_frame, text="End Date:", font=("Arial", 12), fg="black")
        self.end_date_label.pack(pady=5)
        self.end_date_entry = tk.Entry(manage_admin_frame, justify='center')
        self.end_date_entry.insert(0, "DD/MM/YY")  # Insert the hint text
        self.end_date_entry.bind("<FocusIn>", self.clear_hint)  # Clear the hint text on focus
        self.end_date_entry.bind("<FocusOut>", self.set_hint)  # Restore hint text if empty
        self.end_date_entry.pack(pady=5)

        # Centered button for printing the data log
        self.print_button = tk.Button(manage_admin_frame, text="Print Data Log", font=("Arial", 12), command=self.print_data_log, fg="black")
        self.print_button.pack(pady=10)

    def lock_account_box(self):
        # Create the manage admin frame with specified width and height
        manage_admin_frame = tk.Frame(self.frame_right, borderwidth=8, relief="groove", bg="lightgray", width=250, height=320)
        manage_admin_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Prevent the frame from resizing to fit its contents
        manage_admin_frame.pack_propagate(False)

        # Title label for the manage admin box
        title_label = tk.Label(manage_admin_frame, text="Accounts", font=("Arial", 22), fg="black")
        title_label.pack(pady=10)

        # Dropdown for Select User
        tk.Label(manage_admin_frame, text="Select User:", font=("Arial", 12), fg="black").pack(pady=5)
        self.user_combobox = ttk.Combobox(manage_admin_frame, state="readonly")
        self.user_combobox.set("Users")  # Default placeholder text
        self.user_combobox.pack(pady=5)

        # Fetch the list of users from `fetch_staff` method (assumed to return a list of usernames)
        user_list = self.fetch_staff()  # Assuming fetch_staff() method exists and returns a list of usernames
        self.user_combobox['values'] = user_list  # Populate the combobox with usernames

        # Lock and Unlock Buttons
        button_frame = tk.Frame(manage_admin_frame, bg="lightgray")
        button_frame.pack(pady=10)

        self.lock_button = tk.Button(button_frame, text="Lock", command=self.lock_account, font=("Arial", 12), fg="black")
        self.lock_button.pack(side=tk.LEFT, padx=5)

        self.unlock_button = tk.Button(button_frame, text="Unlock", command=self.unlock_account, font=("Arial", 12), fg="black")
        self.unlock_button.pack(side=tk.LEFT, padx=5)

        # Password Reset Button
        self.password_reset_button = tk.Button(manage_admin_frame, text="Password Reset", font=("Arial", 12), command=self.password_reset, fg="black")
        self.password_reset_button.pack(pady=10)

    def populate_user_roles(self):
        """Fetch user-role data and populate the user records box."""
        # Fetch user-role data from the database
        user_roles = self.fetch_user_roles()  # Ensure this method retrieves the data

        # Remove existing user-role entries before repopulating the list
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Create header row for the table if it's not already there
        label_width = 26  # Fixed width for the columns

        # Create the new rows for each user-role pair
        for username, role_name in user_roles:
            # Only add the row if both username and role_name are non-empty
            if username and role_name:
                row_frame = tk.Frame(self.scrollable_frame)
                row_frame.pack(fill=tk.X)  # Fill horizontally

                # Set the same width for both labels in the row
                tk.Label(row_frame, text=username, bg="white", width=label_width, fg="black",
                         borderwidth=1, relief="solid").pack(side=tk.LEFT, fill=tk.X, expand=True)
                tk.Label(row_frame, text=role_name, bg="white", width=label_width, fg="black",
                         borderwidth=1, relief="solid").pack(side=tk.LEFT, fill=tk.X, expand=True)

    def fetch_user_roles(self):
        """Fetch users and their roles from the staff_roles table."""
        user_roles = []
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT username, role FROM staff")
            user_roles = cursor.fetchall()  # This will be a list of tuples (username, role_name)
        except Exception as e:
            print("Error fetching user roles:", e)
        finally:
            if connection:
                cursor.close()
                connection.close()
        
        return user_roles
    
    def create_staff(self):
        user_id = self.entry_user_id.get()
        fullname = self.entry_fullname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        department = self.entry_department.get()

        if not user_id or not username or not fullname or not password:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        # Connect to the PostgreSQL database and insert the staff data
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Create a new staff entry, including the user_type (set to None/NULL by default)
            insert_query = """
            INSERT INTO staff (user_id, fullname, username, department, password, user_type, lock_status, role_name) 
            VALUES (%s, %s, %s, %s, %s, %s, FALSE, NULL)
            """
            cursor.execute(insert_query, (user_id, fullname, username, department, password, "Staff"))


            connection.commit()
            messagebox.showinfo("Success", "Staff created successfully.")
            # Clear the input fields
            self.entry_user_id.delete(0, tk.END)
            self.entry_fullname.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()

    def search_staff(self):
        """Search for staff based on the selected criteria."""
        criteria = self.search_criteria_var.get()
        search_value = self.entry_search.get()

        if not search_value:
            messagebox.showerror("Input Error", "Please enter a value to search.")
            return

        # Connect to the database and fetch the results
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            if criteria == "Username":
                query = "SELECT user_id, username FROM staff WHERE username ILIKE %s"
                cursor.execute(query, (f"%{search_value}%",))
            else:  # User ID
                query = "SELECT user_id, username FROM staff WHERE user_id::text ILIKE %s"
                cursor.execute(query, (f"%{search_value}%",))

            results = cursor.fetchall()
            self.result_listbox.delete(0, tk.END)  # Clear previous results

            for row in results:
                self.result_listbox.insert(tk.END, f"ID: {row[0]}, Username: {row[1]}")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()

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

    def fetch_staff(self):
        """Fetch staff usernames for the dropdown, but use both user_id and username internally, 
        filtered by the currently logged-in department."""
        staff_list = []
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch staff from the currently logged-in department
            query = "SELECT user_id, username FROM staff WHERE department = %s"
            cursor.execute(query, (self.username,))  # Assuming self.username holds the department info

            staff_list = cursor.fetchall()  # Fetch all data as tuples (user_id, username)

        except Exception as e:
            print("Error fetching staff:", e)
        finally:
            if connection:
                cursor.close()
                connection.close()

        # We will only display the usernames in the dropdown, but keep the user_id internally for lookup
        return [user[1] for user in staff_list]  # Return only the usernames for the combobox

    def fetch_roles(self):
        """Fetch roles for the dropdown."""
        role_list = []
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT role_id, role_name FROM roles")
            role_list = cursor.fetchall()  # Fetch all data as tuples
        except Exception as e:
            print("Error fetching roles:", e)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return role_list  # Return list of tuples (role_id, role_name)



    def save_role(self):
        """Save the new role to the roles table."""
        role_name = self.entry_role_name.get()
        if not role_name:
            messagebox.showwarning("Input Error", "Please enter a role name.")
            return
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO roles (role_name) VALUES (%s)", (role_name,))
            connection.commit()
            messagebox.showinfo("Success", "Role saved successfully.")
            self.entry_role_name.delete(0, tk.END)  # Clear the entry field
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()


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



    def center_window(self, window, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.place(x=x, y=y, width=width, height=height)

    def open_role_search_popup(self):
        """Open a popup to search and select a role to delete."""
        popup = tk.Toplevel(self.root)  # Create a new top-level window (popup)
        popup.title("Select Role to Delete")
        
        # Define the size of the popup window
        popup_width = 300
        popup_height = 300

        # Center the popup window on the screen using the center_window method
        self.center_window(popup, popup_width, popup_height)

        # Create a listbox to display the roles
        role_list = self.fetch_roles()  # Get the roles from the database
        role_names = [role[1] for role in role_list]  # Extract role names
        
        # If no roles exist, show a message
        if not role_names:
            tk.Label(popup, text="No roles found", bg="black", fg="white").pack(pady=10)
        else:
            listbox = tk.Listbox(popup, height=10, width=30)  # Create listbox
            for role_name in role_names:
                listbox.insert(tk.END, role_name)  # Insert each role name into the listbox
            listbox.pack(pady=10)

            # Function to handle double-click event
            def on_role_select(event):
                selected_index = listbox.curselection()
                if selected_index:
                    role_name = listbox.get(selected_index)
                    self.selected_role.set(role_name)  # Set the selected role name
                    popup.destroy()  # Close the popup
                    
                    # Confirm role deletion
                    self.confirm_delete_role(role_name)
            
            # Bind double-click to select a role
            listbox.bind("<Double-1>", on_role_select)

        popup.mainloop()  # Start the popup window

    def confirm_delete_role(self, role_name):
        """Open a confirmation dialog to ask if the user is sure about deleting the role."""
        confirm_popup = tk.Toplevel(self.root)
        confirm_popup.title("Confirm Delete Role")

        # Define the size of the confirmation popup
        confirm_width = 300
        confirm_height = 150
        self.center_window(confirm_popup, confirm_width, confirm_height)

        # Add label for confirmation message
        label = tk.Label(
            confirm_popup,
            text=f"Are you sure you want to delete the role '{role_name}'?",
            fg="black",
            bg="white",  # Set background color for better visibility
            wraplength=250  # Limit text width for smaller popups
        )
        label.pack(pady=10)

        # Function to handle confirmation
        def on_confirm():
            self.delete_role(role_name)  # Delete the role
            confirm_popup.destroy()  # Close the confirmation popup
            messagebox.showinfo("Success", f"Role '{role_name}' deleted successfully.")  # Show success message

        # Function to handle cancel
        def on_cancel():
            confirm_popup.destroy()  # Close the confirmation popup

        # Create a frame to hold the buttons and center them
        button_frame = tk.Frame(confirm_popup, bg="white")  # Match popup background
        button_frame.pack(pady=10)  # Add padding to separate buttons from text

        # Create the "Yes" button
        yes_button = tk.Button(
            button_frame,
            text="Yes",
            command=on_confirm,
            bg="black",
            fg="white",
            width=10  # Set a consistent width for buttons
        )
        yes_button.grid(row=0, column=0, padx=10)  # Use grid for better alignment

        # Create the "No" button
        no_button = tk.Button(
            button_frame,
            text="No",
            command=on_cancel,
            bg="black",
            fg="white",
            width=10  # Match width with "Yes" button
        )
        no_button.grid(row=0, column=1, padx=10)

        confirm_popup.configure(bg="white")  # Set popup background for consistency


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
            cursor.execute("UPDATE staff SET role = NULL WHERE role = %s", (role_name,))
            connection.commit()

            # Finally, delete the role from the roles table
            cursor.execute("DELETE FROM roles WHERE role_id = %s", (role_id,))
            connection.commit()



        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_staff_id(self, username):
        """Retrieve staff ID based on username."""
        user_id = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT user_id, username FROM staff WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if result:
                user_id = result[0]  # Get the first element, which is staff_id
        except Exception as e:
            print("Error fetching staff ID:", e)
        finally:
            if connection:
                cursor.close()
                connection.close()
        
        return user_id

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

    def lock_account(self):
        selected_user = self.user_combobox.get()
        if selected_user != "Select User":
            # Fetch the current lock status from the staff table
            lock_status = self.get_lock_status(selected_user)

            if lock_status:  # Account is already locked
                messagebox.showinfo("Account Locked", f"Account {selected_user} is already locked.")
            else:
                # Lock the account (update lock_status to False)
                self.update_lock_status(selected_user, True)
                messagebox.showinfo("Account Locked", f"Account {selected_user} has been locked successfully.")
        else:
            messagebox.showwarning("Select User", "Please select a user first.")

    def unlock_account(self):
        selected_user = self.user_combobox.get()
        if selected_user != "Select User":
            # Fetch the current lock status from the staff table
            lock_status = self.get_lock_status(selected_user)

            if not lock_status:  # Account is already unlocked
                messagebox.showinfo("Account Unlocked", f"Account {selected_user} is already unlocked.")
            else:
                # Unlock the account (update lock_status to True)
                self.update_lock_status(selected_user, False)
                messagebox.showinfo("Account Unlocked", f"Account {selected_user} has been unlocked successfully.")
        else:
            messagebox.showwarning("Select User", "Please select a user first.")

    def print_data_log(self):
        # Print the data log based on selected user and date range
        selected_user = self.user_combobox.get()
        start_date = self.start_date_calendar.get_date()
        end_date = self.end_date_calendar.get_date()
        print(f"Printing data log for {selected_user} from {start_date} to {end_date}")
        # You can replace the print statement with actual log printing functionality.

    def clear_hint(self, event):
        # Clear hint text when the entry field gets focus
        if event.widget.get() == "DD/MM/YY":
            event.widget.delete(0, tk.END)

    def set_hint(self, event):
        # Set hint text back if the entry field is empty
        if event.widget.get() == "":
            event.widget.insert(0, "DD/MM/YY")

    def lock_unlock_account(self):
        selected_user = self.user_combobox.get()
        if selected_user != "Select User":
            # Fetch the user_id and department associated with the selected user from the staff table
            user_id, department = self.fetch_user_id_and_department_for_user(selected_user)

            if user_id is None:
                messagebox.showwarning("User Not Found", f"Could not find user with username {selected_user}.")
                return

            # Get the current lock status from the staff table
            lock_status = self.get_lock_status(selected_user)

            if lock_status is None:  # If user is not found in the staff table
                messagebox.showwarning("User Not Found", f"No account found for {selected_user}.")
                return

            # Toggle the lock status (True -> False, False -> True)
            new_lock_status = not lock_status

            # Update the lock status in the staff table
            self.update_lock_status(selected_user, new_lock_status)

            # Show success message
            if new_lock_status:
                messagebox.showinfo("Account Unlocked", f"Account {selected_user} unlocked successfully.")
            else:
                messagebox.showinfo("Account Locked", f"Account {selected_user} locked successfully.")
        else:
            messagebox.showwarning("Select User", "Please select a user first.")

    def fetch_user_id_and_department_for_user(self, username):
        """Fetch the user_id and department of a user from the staff table based on username."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch the user_id and department of the user from the staff table based on username
        cursor.execute("SELECT user_id, department FROM staff WHERE username = %s;", (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result[0], result[1]  # Return user_id and department as a tuple
        else:
            return None, None  # If the user is not found, return None

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

    def password_reset(self):
        # Get the selected username from the combobox
        selected_user = self.user_combobox.get()
        if selected_user == "Select User":
            messagebox.showwarning("Select User", "Please select a user first.")
            return

        # Create the password reset pop-up
        self.password_reset_popup(selected_user)

    def password_reset_popup(self, username):
        # Create the pop-up window
        reset_window = tk.Toplevel(self.master)
        reset_window.title("Password Reset")
        reset_window.geometry("300x250")  # Adjust the size as needed
        self.center_window(reset_window, 300, 250)

        # Username label (non-editable)
        tk.Label(reset_window, text="Username:", fg="black").pack(pady=5)
        self.username_label = tk.Label(reset_window, text=username, bg="black", fg="white")
        self.username_label.pack(pady=5)

        # Password label and entry
        tk.Label(reset_window, text="New Password:", fg="black").pack(pady=5)
        self.password_entry = tk.Entry(reset_window, show='*')  # Display password as asterisks
        self.password_entry.pack(pady=5)

        # Save Changes button
        save_button = tk.Button(reset_window, text="Save Changes", command=lambda: self.save_password_changes(username), bg="black", fg="white")
        save_button.pack(pady=10)

    def save_password_changes(self, username):
        # Get the new password from the entry field
        new_password = self.password_entry.get()

        if not new_password:
            messagebox.showwarning("Empty Password", "Password cannot be empty.")
            return

        # Here, you would update the password in the staff table (this is just a placeholder)
        print(f"Password for {username} has been updated to: {new_password}")

        # Close the password reset window after saving the changes
        messagebox.showinfo("Password Reset", f"Password for {username} has been updated.")
        self.password_entry.master.destroy()  # Close the pop-up window

    def refresh(self):
        """Handle the refresh functionality."""
        try:
            # Fetch the latest user-role data from the database
            self.populate_user_roles()
            self.fetch_staff()
        except Exception as e:
            print(f"Error refreshing data: {e}")
            messagebox.showerror("Error", f"Failed to refresh data: {e}")

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            # Destroy the current frame
            self.destroy()  # Destroy the current frame
            
            # Call the method to show the login frame in the main application
            self.main_app.show_login_frame()
