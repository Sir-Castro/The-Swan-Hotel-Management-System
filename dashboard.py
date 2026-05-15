import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox, StringVar, simpledialog
import datetime
import bcrypt  
from PIL import Image, ImageTk
from database import get_db_connection
from psycopg2 import sql
import psycopg2
from tkinter import font
import hashlib 


class Dashboard:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        
        self.frame_dashboard = tk.Frame(root)
        self.frame_dashboard.pack(fill=tk.BOTH, expand=True)
        self.hashed_password = self.load_hashed_password()  # Load the hashed password
        # Load and set the background image
        self.background_image = Image.open("images/lounge4.jpg")
        self.background_image = self.background_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        )
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.frame_dashboard, image=self.bg_photo)  # Change 'self' to 'self.frame_dashboard'
        self.bg_label.place(relwidth=1, relheight=1)  # Cover the entire frame


        # Create a grid layout for two columns
        self.frame_left = tk.Frame(self.frame_dashboard, borderwidth=8, relief="groove", bg="black")
        self.frame_left.pack(side=tk.LEFT, fill=tk.BOTH)

        self.frame_right = tk.Frame(self.frame_dashboard, borderwidth=8, relief="groove", bg="black")
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.show_logo_with_fade()

    def show_logo_with_fade(self):
        # Load the logo image and resize it to the desired dimensions
        desired_width = 100  # Set your desired width here
        desired_height = 100  # Set your desired height here
        self.logo_image = Image.open("images/swan2.png").resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Create a label for the logo image
        self.logo_label = tk.Label(self.frame_dashboard, image=self.logo_photo, bg="black", relief="raised", borderwidth=7)
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
            self.root.after(50, self.fade_out_logo, alpha)
        else:
            self.logo_label.config(image='')
            # Once fully faded out, display the main content
            self.create_manage_admin_box()

                    # Create User Interface
            self.create_user_interface()

            # Create Department Interface
            self.create_department_interface()

            # Delete User Interface
            self.create_delete_user_interface()

            # Delete Department Interface
            self.create_delete_department_interface()

            # Create Edit User Box
            self.create_edit_user_box()

            # Add the Update Button
            self.create_update_button()
            self.create_update_button2()
            self.create_update_button3()
            self.button_passwords()
            self.create_update_button5()
            self.create_update_button6()
        
    def create_update_button(self):
        """
        Create a standalone update button and its functionality, allowing it to be moved freely.
        """
        self.update_button = tk.Button(self.frame_dashboard, text="Management", 
                                       font=("Arial", 14), bg="black", fg="white", width=10, height=1, borderwidth=8)
        # Place the button at an initial position (x, y)
        self.update_button.place(x=400, y=100)
    def create_update_button2(self):
        """
        Create a standalone update button and its functionality, allowing it to be moved freely.
        """
        self.update_button = tk.Button(self.frame_dashboard, text="Analysis", 
                                       font=("Arial", 14), bg="black", fg="white", width=10, height=1, borderwidth=8)
        # Place the button at an initial position (x, y)
        self.update_button.place(x=400, y=200)
    def create_update_button3(self):
        """
        Create a standalone update button and its functionality, allowing it to be moved freely.
        """
        self.update_button = tk.Button(self.frame_dashboard, text="Review", 
                                       font=("Arial", 14), bg="black", fg="white", width=10, height=1, borderwidth=8)
        # Place the button at an initial position (x, y)
        self.update_button.place(x=400, y=300)
    def button_passwords(self):
        """Create a standalone update button to manage passwords."""
        self.update_button = tk.Button(
            self.frame_dashboard, text="Passwords",
            font=("Arial", 14), bg="black", fg="white", width=10, height=1, borderwidth=8,
            command=self.open_password_popup
        )
        self.update_button.place(x=850, y=100)  # Initial position for the button

    def create_update_button5(self):
        """
        Create a standalone update button and its functionality, allowing it to be moved freely.
        """
        self.update_button = tk.Button(self.frame_dashboard, text="System", 
                                       font=("Arial", 14), bg="black", fg="white", width=10, height=1, borderwidth=8)
        # Place the button at an initial position (x, y)
        self.update_button.place(x=850, y=200)
    def create_update_button6(self):
        """
        Create a standalone update button and its functionality, allowing it to be moved freely.
        """
        self.update_button = tk.Button(self.frame_dashboard, text="Reports", 
                                       font=("Arial", 14), bg="black", fg="white", width=10, height=1, borderwidth=8)
        # Place the button at an initial position (x, y)
        self.update_button.place(x=850, y=300)

    def open_update_popup(self, event):
        """Open a popup to update selected user or department details."""
        selected_item = self.edit_listbox.curselection()
        if not selected_item:
            messagebox.showwarning("Input Error", "Please select an item to update.")
            return

        selected_index = selected_item[0]
        selected_type = self.edit_type_var.get()
        search_term = self.entry_search.get().strip()

        if selected_type == "Staff":
            users = self.load_users()
            filtered_users = [user for user in users if search_term.lower() in user['username'].lower() or
                                                          search_term.lower() in user['department'].lower() or
                                                          search_term.lower() in user['user_type'].lower()]

            if selected_index >= len(filtered_users):
                messagebox.showerror("Error", "Selected index out of range.")
                return
            
            user_data = filtered_users[selected_index]
            self.update_user_popup(user_data)

        elif selected_type == "Department":
            departments = self.load_departments()
            filtered_departments = [dept for dept in departments if search_term.lower() in dept['name'].lower() or
                                                                         search_term.lower() in dept['rights'].lower()]

            if selected_index >= len(filtered_departments):
                messagebox.showerror("Error", "Selected index out of range.")
                return

            dept_data = filtered_departments[selected_index]
            self.update_department_popup(dept_data)

    def update_user_popup(self, user_data):
        """Create a popup for updating user details."""
        popup = tk.Toplevel(self.root)
        popup.title("Update User Details")
        
        # Center the popup
        self.center_window(popup, 300, 250)

        # Current department label
        current_dept_label = tk.Label(popup, text="Current Department:")
        current_dept_label.pack(pady=5)

        # Display current department
        current_dept_var = tk.StringVar(value=user_data['department'])
        current_dept_entry = tk.Entry(popup, textvariable=current_dept_var, state='readonly')
        current_dept_entry.pack(pady=5)

        # Dropdown for selecting new department
        departments = self.load_departments()
        department_names = [dept['name'] for dept in departments]  # Extract department names

        new_dept_var = tk.StringVar(popup)
        new_dept_var.set(department_names[0])  # Default value

        dept_dropdown = tk.OptionMenu(popup, new_dept_var, *department_names)
        dept_dropdown.pack(pady=5)

        # Current user type label
        current_user_type_label = tk.Label(popup, text="Current User Type:")
        current_user_type_label.pack(pady=5)

        # Fetch the user type depending on whether the user exists in the 'users' or 'staff' table
        user_type = self.get_user_type(user_data['id'])

        # Display current user type
        current_user_type_var = tk.StringVar(value=user_type)
        current_user_type_entry = tk.Entry(popup, textvariable=current_user_type_var, state='readonly')
        current_user_type_entry.pack(pady=5)

        # Dropdown for selecting new user type
        user_types = ["Supervisor", "Staff"]  # Example user types, update as necessary
        new_user_type_var = tk.StringVar(popup)
        new_user_type_var.set(user_type)  # Default to current user type

        user_type_dropdown = tk.OptionMenu(popup, new_user_type_var, *user_types)
        user_type_dropdown.pack(pady=5)

        # Update button
        update_button = tk.Button(popup, text="Update", command=lambda: self.save_user_updates(user_data, new_dept_var.get(), new_user_type_var.get(), popup))
        update_button.pack(pady=10)

    def get_user_type(self, user_id):
        """Fetch the user type from the 'staff' table."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if the user exists in the 'staff' table
            cursor.execute("SELECT user_type FROM staff WHERE user_id = %s", (user_id,))
            staff_type_row = cursor.fetchone()

            if staff_type_row:
                return staff_type_row[0]  # Return the user type from 'staff' table
            else:
                return "User not found."  # Return 'Unknown' if the user is not found in the 'staff' table

        except Exception as error:
            print(f"Error fetching user type: {error}")
            return "Select user type"  # Return 'Error' if something goes wrong

        finally:
            if connection:
                cursor.close()
                connection.close()

    def center_window(self, window, width, height):
        """Center the window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def save_user_updates(self, user_data, new_department, new_user_type, popup):
        """Save updated user details in the 'staff' table."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if the user exists in the 'staff' table
            cursor.execute("SELECT * FROM staff WHERE user_id = %s", (user_data['id'],))
            staff_exists = cursor.fetchone()

            if staff_exists:
                # Update the department and user type in the 'staff' table
                cursor.execute("""
                    UPDATE staff
                    SET department = %s, user_type = %s
                    WHERE user_id = %s
                """, (new_department, new_user_type, user_data['id']))
                print("User updated in 'staff' table.")

                # Commit the changes
                connection.commit()

                # Show success message and close the popup
                messagebox.showinfo("Success", "User details updated successfully!")
                popup.destroy()
            else:
                # If the user is not found in the 'staff' table, show an error
                messagebox.showerror("Error", "User not found in the 'staff' table.")

        except Exception as error:
            print(f"Error updating user: {error}")
            messagebox.showerror("Error", "An error occurred while updating user details.")

        finally:
            if connection:
                cursor.close()
                connection.close()

    def update_department_popup(self, dept_data):
        """Popup to update department rights."""
        def save_changes():
            # Gather the rights from the listbox
            selected_rights = [listbox.get(i) for i in range(listbox.size())]
            
            try:
                connection = get_db_connection()
                cursor = connection.cursor()

                # Update the department's rights in the database (as a comma-separated list)
                cursor.execute("""
                    UPDATE departments
                    SET dept_rights = %s
                    WHERE dept_id = %s
                """, (", ".join(selected_rights), dept_data['id']))

                # Commit the changes
                connection.commit()

                messagebox.showinfo("Success", "Department rights updated successfully!")
                popup.destroy()
                self.fetch_data("Department")  # Refresh the department list

            except Exception as error:
                print(f"Error updating department: {error}")
                messagebox.showerror("Error", "An error occurred while updating department rights.")

            finally:
                if connection:
                    cursor.close()
                    connection.close()

        def open_add_rights_popup():
            """Popup to select rights to add."""
            add_popup = tk.Toplevel(popup)
            add_popup.title("Select Rights to Add")
            self.center_window(add_popup, 400, 400)

            rights_listbox = tk.Listbox(add_popup, selectmode=tk.SINGLE, height=10, width=40)
            rights_listbox.pack(pady=10, padx=10)

            # Fetch all rights from the database to display
            try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT right_data FROM rights")
                rights = cursor.fetchall()
                for right in rights:
                    rights_listbox.insert(tk.END, right[0])
            except Exception as e:
                print(f"Error fetching rights: {e}")
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

            def add_selected_right():
                selected_right = rights_listbox.get(tk.ACTIVE)
                if selected_right and selected_right not in listbox.get(0, tk.END):
                    listbox.insert(tk.END, selected_right)

            button_add = tk.Button(add_popup, text="Add Right", command=add_selected_right)
            button_add.pack(pady=10)

            button_save = tk.Button(add_popup, text="Save", command=add_popup.destroy)
            button_save.pack(pady=10)

        def remove_selected_right():
            selected = listbox.curselection()
            if selected:
                listbox.delete(selected)

        popup = tk.Toplevel(self.root)
        popup.title("Update Department Rights")

        # Center the popup window
        self.center_window(popup, 500, 400)

        tk.Label(popup, text="Current Rights:").pack(pady=5)

        # Create the listbox to show current rights
        listbox = tk.Listbox(popup, selectmode=tk.SINGLE, height=10, width=40)
        listbox.pack(pady=10, padx=10)

        # Pre-fill current rights for the department
        if dept_data['rights']:
            for right in dept_data['rights'].split(', '):
                listbox.insert(tk.END, right)

        # Buttons to add or remove rights
        frame_buttons = tk.Frame(popup)
        frame_buttons.pack(pady=10)

        button_add = tk.Button(frame_buttons, text="+", command=open_add_rights_popup)
        button_add.pack(side=tk.LEFT, padx=10)

        button_remove = tk.Button(frame_buttons, text="-", command=remove_selected_right)
        button_remove.pack(side=tk.LEFT, padx=10)

        # Save button to apply changes
        button_save_changes = tk.Button(popup, text="Save Changes", command=save_changes)
        button_save_changes.pack(pady=10)

    def create_manage_admin_box(self):
        # Create a title label for the Admin Dashboard
        title_label = tk.Label(self.frame_dashboard, text="Admin Dashboard", font=("Arial", 26), bg="black", fg="white")
        title_label.pack(pady=(10, 10))  # Padding to position it nicely

        # Create the manage admin frame
        manage_admin_frame = tk.Frame(
            self.frame_dashboard,
            borderwidth=8,
            relief="groove",
            bg="black",
            width=300,  # Set the desired width
            height=300  # Set the desired height
        )
        manage_admin_frame.pack(pady=10, padx=10)

        # Prevent the frame from resizing to fit its contents
        manage_admin_frame.pack_propagate(False)

        label_manage_admin = tk.Label(manage_admin_frame, text="Change Password", font=("Arial", 16), bg="black", fg="white")
        label_manage_admin.pack(pady=10)

        tk.Label(manage_admin_frame, text="Current Password:", font=("Arial", 12), bg="black", fg="white").pack(pady=5)
        self.entry_current_password = tk.Entry(manage_admin_frame, show='*')
        self.entry_current_password.pack(pady=5)

        tk.Label(manage_admin_frame, text="New Password:", bg="black", font=("Arial", 12), fg="white").pack(pady=5)
        self.entry_new_password = tk.Entry(manage_admin_frame, show='*')
        self.entry_new_password.pack(pady=5)

        button_update = tk.Button(manage_admin_frame, text="Change Password", font=("Arial", 12), command=self.change_password, bg="black", fg="white")
        button_update.pack(pady=10)

        self.button_logout = tk.Button(manage_admin_frame, text="Logout", font=("Arial", 12), command=self.logout, bg="black", fg="white")
        self.button_logout.pack(pady=10)

    def create_edit_user_box(self):
        """Create the interface for editing users or departments."""
        edit_user_frame = tk.Frame(self.frame_dashboard, borderwidth=8, relief="groove", bg="black")
        edit_user_frame.pack(padx=5, fill=tk.Y)
        custom_font = font.Font(family="Arial", size=12)
        # Left Frame: Update Details
        left_frame = tk.Frame(edit_user_frame, borderwidth=8, relief="groove", height=400, width=300)
        left_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X)
        left_frame.pack_propagate(False)

        label_update_details = tk.Label(left_frame, text="Update Data", font=("Arial", 20))
        label_update_details.pack(pady=5)

        # Dropdown to select between Staff and Department
        self.edit_type_var = StringVar(left_frame)
        self.edit_type_var.set("Select Type")
        self.dropdown_edit_type = tk.OptionMenu(left_frame, self.edit_type_var, "Staff", "Department")
        self.dropdown_edit_type.pack(pady=5)
        self.dropdown_edit_type.config(font=custom_font)

        # Search Frame
        search_frame = tk.Frame(left_frame)
        search_frame.pack(pady=5)

        # Search Button
        button_search = tk.Button(search_frame, text="Search", command=self.perform_search, width=7, font=("Arial", 12))
        button_search.pack(side=tk.RIGHT)

        # Search Entry
        self.entry_search = tk.Entry(search_frame, width=10)
        self.entry_search.pack(side=tk.LEFT, padx=(5, 1))

        # Listbox for search results
        self.edit_listbox = tk.Listbox(left_frame, width=50, height=25, borderwidth=5, relief="groove",)
        self.edit_listbox.pack(pady=5)

        # Bind double-click event for Listbox
        self.edit_listbox.bind("<Double-1>", self.open_update_popup)


        # Right Frame: View Data
        right_frame = tk.Frame(edit_user_frame, borderwidth=8, relief="groove", height=400, width=500)
        right_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X)
        right_frame.pack_propagate(False)

        label_view_users = tk.Label(right_frame, text="View Data", font=("Arial", 20))
        label_view_users.pack(pady=5)

        # Dropdown to view all users or departments
        self.view_type_var = StringVar(right_frame)
        self.view_type_var.set("View")
        self.dropdown_view_type = tk.OptionMenu(right_frame, self.view_type_var, "All Users", "All Departments", command=self.update_view_list)
        self.dropdown_view_type.pack(pady=10)
        self.dropdown_view_type.config(font=custom_font)

        # Listbox and Scrollbar for data view
        listbox_frame = tk.Frame(right_frame)
        listbox_frame.pack(pady=5)

        self.view_listbox = tk.Listbox(listbox_frame, width=80, height=30, borderwidth=8, relief="groove")
        self.view_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.view_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.view_listbox.config(yscrollcommand=scrollbar.set)

    def update_view_list(self, selection):
        """Updates the view_listbox based on the selected option."""
        self.view_listbox.delete(0, tk.END)  # Clear the listbox

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            if selection == "All Users":
                # Clear the listbox before fetching new data
                self.view_listbox.delete(0, tk.END)

                try:
                    # Fetch all usernames from the 'staff' table
                    cursor.execute("SELECT fullname, username, department FROM staff")
                    staff = cursor.fetchall()

                    # Insert usernames from the 'staff' table into the listbox
                    if staff:
                        for member in staff:
                            display_text = f"Staff: {member[0]} | Username: {member[1]} | Department: {member[2]}"
                            self.view_listbox.insert(tk.END, display_text)
                    else:
                        # Display message if no staff members are found
                        self.view_listbox.insert(tk.END, "No staff available")

                except Exception as error:
                    print(f"Error fetching users: {error}")
                    self.view_listbox.insert(tk.END, "Error loading staff")


            elif selection == "All Departments":
                # Clear the listbox before fetching new data
                self.view_listbox.delete(0, tk.END)

                try:
                    # Fetch all departments from the departments table
                    cursor.execute("SELECT dept_name FROM departments")
                    departments = cursor.fetchall()

                    for department in departments:
                        # Assuming department is a tuple, fetch the name
                        self.view_listbox.insert(tk.END, department[0])  # Insert department name into the listbox

                    if not departments:
                        self.view_listbox.insert(tk.END, "No departments available")

                except Exception as error:
                    print(f"Error fetching departments: {error}")
                    self.view_listbox.insert(tk.END, "Error loading departments")

        except Exception as error:
            print(f"Error updating view list: {error}")
            messagebox.showerror("Error", "An error occurred while updating the view list.")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def update_details(self):
        """Update selected user's or department's details."""
        selected_item = self.edit_listbox.curselection()
        new_details = self.entry_edit_details.get().strip()
        search_term = self.entry_search.get().strip()
        selected_type = self.edit_type_var.get()

        if not selected_item or len(new_details) < 1 or not search_term:
            messagebox.showwarning("Input Error", "Please select an item, enter a search term, and provide new details.")
            return

        selected_index = selected_item[0]

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            if selected_type == "User":
                # Fetch filtered users from the database
                cursor.execute("""
                    SELECT user_id, username, department, user_type FROM users
                    WHERE username ILIKE %s OR department ILIKE %s OR user_type ILIKE %s
                """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                filtered_users = cursor.fetchall()

                if not filtered_users:
                    messagebox.showerror("Error", f"No user found for '{search_term}'.")
                    return

                if selected_index >= len(filtered_users):
                    messagebox.showerror("Error", "Selected index out of range.")
                    return

                user_id = filtered_users[selected_index][0]  # Get user_id of the selected user

                # Update specific fields based on user input
                if self.update_field_var.get() == "Department":
                    cursor.execute("""
                        UPDATE users SET department = %s WHERE user_id = %s
                    """, (new_details, user_id))
                elif self.update_field_var.get() == "User Type":
                    cursor.execute("""
                        UPDATE users SET user_type = %s WHERE user_id = %s
                    """, (new_details, user_id))

            elif selected_type == "Department":
                # Fetch filtered departments from the database
                cursor.execute("""
                    SELECT dept_id, name, rights FROM departments
                    WHERE name ILIKE %s OR rights ILIKE %s
                """, (f'%{search_term}%', f'%{search_term}%'))
                filtered_departments = cursor.fetchall()

                if not filtered_departments:
                    messagebox.showerror("Error", f"No department found for '{search_term}'.")
                    return

                if selected_index >= len(filtered_departments):
                    messagebox.showerror("Error", "Selected index out of range.")
                    return

                dept_id = filtered_departments[selected_index][0]  # Get dept_id of the selected department
                # Assuming we update the department name
                cursor.execute("""
                    UPDATE departments SET name = %s WHERE dept_id = %s
                """, (new_details, dept_id))

            # Commit the transaction
            connection.commit()
            messagebox.showinfo("Success", "Details updated successfully!")
            self.fetch_data(selected_type)  # Refresh the listbox

        except Exception as error:
            print(f"Error updating details: {error}")
            messagebox.showerror("Error", "An error occurred while updating details.")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def perform_search(self):
        """Perform a search in the staff or departments based on selected criteria."""
        search_term = self.entry_search.get().strip().lower()
        results = []

        if self.edit_type_var.get() == "Staff":
            # Load all staff data
            users = self.load_users()
            if not search_term:  # If no search term is provided, display all staff by username
                results = sorted(users, key=lambda x: x['username'].lower())
            else:  # Search based on the username or department
                for user in users:
                    if search_term in user['username'].lower() or search_term in user['department'].lower():
                        results.append(user)

        elif self.edit_type_var.get() == "Department":
            # Load all department data
            departments = self.load_departments()
            if not search_term:  # If no search term is provided, display all departments by name
                results = sorted(departments, key=lambda x: x['name'].lower())
            else:  # Search based on department name
                for dept in departments:
                    if search_term in dept['name'].lower():
                        results.append(dept)

        # Update the Listbox with results
        self.edit_listbox.delete(0, tk.END)
        for result in results:
            display_text = f"{result['id']} - {result['username']}" if self.edit_type_var.get() == "Staff" else f"{result['id']} - {result['name']}"
            self.edit_listbox.insert(tk.END, display_text)

        if not results:
            messagebox.showinfo("No Results", f"No results found for '{search_term}'.")

    def fetch_user_search_fields(self):
        """Fetch distinct values for user-specific search fields."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch distinct departments and user types from the users table
            cursor.execute("SELECT DISTINCT department FROM staff")
            departments = [row[0] for row in cursor.fetchall() if row[0] is not None]

            cursor.execute("SELECT DISTINCT user_type FROM staff")
            user_types = [row[0] for row in cursor.fetchall() if row[0] is not None]

            return departments, user_types

        except Exception as error:
            print(f"Error fetching user search fields: {error}")
            return [], []

        finally:
            if connection:
                cursor.close()
                connection.close()

    def fetch_department_search_fields(self):
        """Fetch distinct values for department-specific search fields."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch distinct rights from the departments table
            cursor.execute("SELECT DISTINCT dept_rights FROM departments")
            rights = [row[0] for row in cursor.fetchall() if row[0] is not None]

            return rights

        except Exception as error:
            print(f"Error fetching department search fields: {error}")
            return []

        finally:
            if connection:
                cursor.close()
                connection.close()

    def update_search_options(self, selection=None):
        """Update search options based on the selected type."""
        self.dropdown_search_field['menu'].delete(0, 'end')

        try:
            if self.edit_type_var.get() == "Staff":
                departments, user_types = self.fetch_user_search_fields()
                search_fields = ["Username"]
            elif self.edit_type_var.get() == "Department":
                rights = self.fetch_department_search_fields()
                search_fields = ["Department Name"]
            else:
                search_fields = []

            for field in search_fields:
                self.dropdown_search_field['menu'].add_command(label=field, command=tk._setit(self.search_field_var, field))

            self.search_field_var.set("Select Search Field")  # Reset to default

        except Exception as error:
            print(f"Error updating search options: {error}")
            messagebox.showerror("Error", "An error occurred while updating search options.")

    def fetch_data(self, selection):
        """Fetch data based on user or department selection."""
        self.edit_listbox.delete(0, tk.END)  # Clear previous entries

        try:
            if selection == "Staff":
                users = self.load_users()  # This should fetch users from the database
                for user in staff:
                    # Display formatted user info
                    display_text = f"{user['id']} - {user['username']} ({user['department']}, {user['user_type']})"
                    self.edit_listbox.insert(tk.END, display_text)

            elif selection == "Department":
                departments = self.load_departments()  # This should fetch departments from the database
                for dept in departments:
                    # Display formatted department info
                    display_text = f"{dept['id']} - {dept['name']} ({dept['rights']})"
                    self.edit_listbox.insert(tk.END, display_text)

        except Exception as error:
            print(f"Error fetching data: {error}")
            messagebox.showerror("Error", "An error occurred while fetching data.")

    def save_users(self, users):
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Clear the existing users (optional, based on your requirement)
            cursor.execute("DELETE FROM staff")

            # Insert new users
            for user in staff:
                cursor.execute("""
                    INSERT INTO staff (user_id, username, password, department, user_type)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user['id'], user['username'], user['password'], user['department'], user['user_type']))

            # Commit the transaction
            connection.commit()
            print("Users saved successfully!")

        except Exception as error:
            print(f"Error saving users: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def save_departments(self, departments):
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Clear the existing departments (optional, based on your requirement)
            cursor.execute("DELETE FROM departments")

            # Insert new departments
            for dept in departments:
                cursor.execute("""
                    INSERT INTO departments (dept_id, dept_name, dept_password, dept_rights)
                    VALUES (%s, %s, %s, %s)
                """, (dept['id'], dept['name'], dept['password'], dept['rights']))

            # Commit the transaction
            connection.commit()
            print("Departments saved successfully!")

        except Exception as error:
            print(f"Error saving departments: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def load_hashed_password(self):
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch the hashed password from the admin table
            cursor.execute("SELECT hashed_password FROM admin LIMIT 1")  # Adjust the query as needed
            result = cursor.fetchone()  # Fetch the first result

            if result:
                return result[0].encode('utf-8')  # Return the hashed password as bytes
            else:
                # If no password found, set an initial password
                self.set_initial_password("Admin")
                return self.load_hashed_password()

        except Exception as error:
            print(f"Error loading hashed password: {error}")
            return None  # Return None if there was an error

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def load_users(self):
        users = []
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all users from the `staff` table
            cursor.execute("SELECT user_id, username, password, department, user_type FROM staff")
            staff_rows = cursor.fetchall()

            for row in staff_rows:
                try:
                    user_id = row[0]
                    username = row[1]
                    password = row[2]
                    department = row[3]
                    user_type = row[4]

                    users.append({
                        'id': user_id,
                        'username': username.strip(),
                        'password': password.strip(),
                        'department': department.strip(),
                        'user_type': user_type.strip() if user_type else "Staff"  # Default to "Staff" if user_type is None
                    })
                except IndexError:
                    print(f"Invalid staff row: {row}")

        except Exception as error:
            print(f"Error loading users: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

        return users

    def load_departments(self):
        departments = []
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all departments from the database
            cursor.execute("SELECT dept_id, dept_name, dept_password, dept_rights FROM departments")
            rows = cursor.fetchall()  # Fetch all rows

            for row in rows:
                try:
                    dept_id = row[0]
                    dept_name = row[1]
                    dept_password = row[2]
                    dept_rights = row[3]

                    departments.append({
                        'id': dept_id,
                        'name': dept_name.strip(),
                        'password': dept_password.strip(),
                        'rights': dept_rights.strip()
                    })
                except IndexError:
                    print(f"Invalid department row: {row}")

        except Exception as error:
            print(f"Error loading departments: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

        return departments

    def change_password(self):
        """Validate the current password and change to the new password."""
        current_password = self.entry_current_password.get()
        new_password = self.entry_new_password.get()

        if self.validate_current_password(current_password):
            # Hash the new password
            new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Update the hashed password in the admin table
                cursor.execute("""
                    UPDATE admin SET hashed_password = %s
                """, (new_hashed.decode('utf-8'),))  # Store hashed password as a string

                # Commit the transaction
                connection.commit()

                messagebox.showinfo("Success", "Password changed successfully!")

            except Exception as error:
                print(f"Error changing password: {error}")
                messagebox.showerror("Database Error", "Error changing password.")

            finally:
                # Close the database connection
                if connection:
                    cursor.close()
                    connection.close()
        else:
            messagebox.showwarning("Input Error", "Current password is incorrect.")

    def create_user_interface(self):
        user_frame = tk.Frame(self.frame_left, borderwidth=8, relief="groove")
        user_frame.pack(pady=5, padx=5)
        custom_font = font.Font(family="Arial", size=12)
        label_user = tk.Label(user_frame, text="Create User", font=("Arial", 20))
        label_user.pack(pady=10)

        # User ID field (disabled)
        tk.Label(user_frame, text="User ID:", font=("Arial", 12)).pack(pady=5)
        self.entry_user_id = tk.Entry(user_frame, state="disabled", width=30)  # Fixed width for User ID field
        self.entry_user_id.pack(pady=5)

        # Full Name field
        tk.Label(user_frame, text="Full Name:", font=("Arial", 12)).pack(pady=5)
        self.entry_fullname = tk.Entry(user_frame, width=30)  # Fixed width for Full Name field
        self.entry_fullname.pack(pady=5)

        # Username field
        tk.Label(user_frame, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.entry_username = tk.Entry(user_frame, width=30)  # Fixed width for Username field
        self.entry_username.pack(pady=5)

        # Password field
        tk.Label(user_frame, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.entry_password = tk.Entry(user_frame, show='*', width=30)  # Fixed width for Password field
        self.entry_password.pack(pady=5)

        # Department dropdown
        tk.Label(user_frame, text="Department:", font=("Arial", 12)).pack(pady=5)
        self.department_var = StringVar(user_frame)
        self.department_var.set("Select")  # Default value

        # Set the department dropdown with fixed width
        self.dropdown_department = tk.OptionMenu(user_frame, self.department_var, "Select Department")
        self.dropdown_department.pack(pady=5, padx=10)
        self.dropdown_department.config(font=custom_font, width=20)  # Fixed width for department dropdown

        # Load departments into the dropdown
        self.update_department_dropdown()

        # User Type dropdown
        tk.Label(user_frame, text="User Type:", font=("Arial", 12)).pack(pady=5)
        self.user_type_var = StringVar(user_frame)
        self.user_type_var.set("Select")  # Default value
        self.dropdown_user_type = tk.OptionMenu(user_frame, self.user_type_var, "Manager", "Supervisor", "Staff")
        self.dropdown_user_type.pack(pady=5)
        self.dropdown_user_type.config(font=custom_font, width=20)  # Fixed width for user type dropdown

        # Create User button
        button_create_user = tk.Button(user_frame, text="Create User", font=("Arial", 12), command=self.create_user)
        button_create_user.pack(pady=10)

        # Automatically generate the User ID when the interface is created
        self.generate_user_id()

    def create_delete_user_interface(self):
        delete_user_frame = tk.Frame(self.frame_left, borderwidth=8, relief="groove")
        delete_user_frame.pack(pady=10, padx=10, fill=tk.X)

        label_delete_user = tk.Label(delete_user_frame, text="Delete User", font=("Arial", 20))
        label_delete_user.pack(pady=5)

        # Button to display a popup of users
        button_search_user = tk.Button(delete_user_frame, text="Search User", font=("Arial", 12), command=self.show_user_list)
        button_search_user.pack(pady=5)

        self.search_var = StringVar(delete_user_frame)
        self.search_entry = tk.Entry(delete_user_frame, textvariable=self.search_var, state="disabled", width=20)  # Width set to 20
        self.search_entry.pack(pady=5)

        button_delete_user = tk.Button(delete_user_frame, text="Delete User", font=("Arial", 12), command=self.delete_user)
        button_delete_user.pack(pady=10)
        
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

    def create_department_interface(self):
        dept_frame = tk.Frame(self.frame_right, borderwidth=8, relief="groove", height=500)
        dept_frame.pack(pady=5, padx=10, fill=tk.Y, expand=True)
        custom_font = font.Font(family="Arial", size=12)
        label_dept = tk.Label(dept_frame, text="Create Department", font=("Arial", 18))
        label_dept.pack(pady=10)

        tk.Label(dept_frame, text="Department ID:", font=("Arial", 12)).pack(pady=5)
        self.entry_dept_id = tk.Entry(dept_frame, state="disabled") 
        self.entry_dept_id.pack(pady=5)

        tk.Label(dept_frame, text="Department Name:", font=("Arial", 12)).pack(pady=5)
        self.entry_dept_name = tk.Entry(dept_frame)
        self.entry_dept_name.pack(pady=5)

        tk.Label(dept_frame, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.entry_dept_password = tk.Entry(dept_frame, show='*')
        self.entry_dept_password.pack(pady=5)

        tk.Label(dept_frame, text="Department Rights:", font=("Arial", 12)).pack(pady=5)
        self.dept_rights_var = StringVar(dept_frame)
        self.dept_rights_var.set("Select")  # Default value
        self.rights_button = tk.Button(dept_frame, text=self.dept_rights_var.get(), command=self.open_rights_popup, width=10, font=custom_font)
        self.rights_button.pack(pady=5)

        button_create_dept = tk.Button(dept_frame, text="Create Department", font=("Arial", 12), command=self.create_department)
        button_create_dept.pack(pady=10)
        self.generate_department_id()

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

    def show_user_list(self):
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Retrieve all usernames from the `staff` table
            cursor.execute("SELECT username FROM staff")
            staff = [row[0] for row in cursor.fetchall()]

            if staff:
                # Create a popup window to display users
                popup = tk.Toplevel(self.frame_left)
                popup.title("Select User")

                # Center the popup window
                popup_width = 200
                popup_height = 200
                self.center_window(popup, popup_width, popup_height)

                label = tk.Label(popup, text="Select User", font=("Arial", 14))
                label.pack(pady=10)

                listbox = tk.Listbox(popup)
                for user in sorted(staff):  # Sort usernames alphabetically for better readability
                    listbox.insert(tk.END, user)
                listbox.pack(pady=10, fill=tk.BOTH, expand=True)

                # Event handler for double-click on listbox item
                def on_user_select(event):
                    selected_user = listbox.get(tk.ACTIVE)
                    if selected_user:
                        self.search_var.set(selected_user)
                        self.search_entry.config(state="disabled")  # Make the entry field non-editable
                        popup.destroy()

                # Bind double-click event to the listbox
                listbox.bind("<Double-1>", on_user_select)

            else:
                messagebox.showinfo("Info", "No users available to display.")

        except Exception as error:
            messagebox.showerror("Database Error", f"Error retrieving users: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()


    def create_delete_department_interface(self):
        delete_dept_frame = tk.Frame(self.frame_right, borderwidth=8, relief="groove")
        delete_dept_frame.pack(pady=10, padx=10)
        custom_font = font.Font(family="Arial", size=12)

        label_delete_dept = tk.Label(delete_dept_frame, text="Delete Department", font=("Arial", 18))
        label_delete_dept.pack(pady=10)

        tk.Label(delete_dept_frame, text="Search Department:", font=("Arial", 12)).pack(pady=5)
        self.search_dept_entry = tk.Entry(delete_dept_frame, state="readonly")  # Initially read-only
        self.search_dept_entry.pack(pady=5)

        button_search_dept = tk.Button(delete_dept_frame, text="Search", font=("Arial", 12), command=self.open_department_popup)
        button_search_dept.pack(pady=5)

        button_delete_dept = tk.Button(delete_dept_frame, text="Delete Department", font=("Arial", 12), command=self.delete_department)
        button_delete_dept.pack(pady=10)

    def open_department_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Select Department")

        # Center the popup window
        self.center_window(popup, 300, 400)  # Adjust the width and height as needed

        tk.Label(popup, text="Available Departments", font=("Arial", 14)).pack(pady=10)

        listbox = tk.Listbox(popup, width=30, height=15)
        listbox.pack(pady=10, padx=10)

        # Fetch department names from the database
        try:
            connection = get_db_connection()  # Assuming a function to establish DB connection
            cursor = connection.cursor()
            cursor.execute("SELECT dept_name FROM departments")
            departments = cursor.fetchall()

            # Populate listbox with department names
            for dept in departments:
                listbox.insert(tk.END, dept[0])

            if not departments:
                listbox.insert(tk.END, "No departments available")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch departments: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

        def on_department_select(event):
            selected_department = listbox.get(listbox.curselection())
            self.search_dept_entry.config(state="normal")  # Enable editing to set the value
            self.search_dept_entry.delete(0, tk.END)
            self.search_dept_entry.insert(0, selected_department)
            self.search_dept_entry.config(state="readonly")  # Make the field read-only again
            popup.destroy()

        listbox.bind("<Double-1>", on_department_select)

    def load_hashed_password(self):
        """Load the hashed password from the database."""
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch the hashed password from the admin table
            cursor.execute("SELECT hashed_password FROM admin LIMIT 1")  # Adjust the query as needed
            result = cursor.fetchone()  # Fetch the first result

            if result:
                return result[0].encode('utf-8')  # Return the hashed password as bytes
            else:
                # If no password found, set an initial password
                self.set_initial_password("Admin")
                return self.load_hashed_password()

        except Exception as error:
            print(f"Error loading hashed password: {error}")
            return None  # Return None if there was an error

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def set_initial_password(self, password):
        """Set the initial password and save its hash to the database."""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert or update the hashed password in the admin table
            cursor.execute("""
                INSERT INTO admin (hashed_password) VALUES (%s)
                ON CONFLICT (id) DO UPDATE SET hashed_password = EXCLUDED.hashed_password
            """, (hashed.decode('utf-8'),))  # Store hashed password as a string

            # Commit the transaction
            connection.commit()

        except Exception as error:
            print(f"Error setting initial password: {error}")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

    def validate_current_password(self, current_password):
        return bcrypt.checkpw(current_password.encode('utf-8'), self.hashed_password)

    def create_user(self):
        user_id = self.entry_user_id.get()  # User ID is generated automatically
        fullname = self.entry_fullname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        department = self.department_var.get()
        user_type = self.user_type_var.get()

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

                # Insert user data into the database
                cursor.execute("""
                    INSERT INTO staff (user_id,fullname, username, password, department, user_type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, fullname, username, password, department, user_type))

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
                self.update_department_dropdown()


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

    def update_user_dropdown(self):
        self.dropdown_user['menu'].delete(0, 'end')

        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all users
            cursor.execute("SELECT username FROM staff")
            users = cursor.fetchall()  # Fetch all usernames

            if users:
                for user in staff:
                    username_display = user[0]  # Access the first element in the tuple
                    self.dropdown_user['menu'].add_command(label=username_display, command=tk._setit(self.user_var, username_display))
            else:
                self.user_var.set("No users available")

        except Exception as error:
            print(f"Error fetching users: {error}")
            self.user_var.set("Error loading users")

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

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

    def delete_user(self):
        username = self.search_var.get().strip()
        if username:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {username}?"):
                try:
                    # Establish the database connection
                    connection = get_db_connection()
                    cursor = connection.cursor()

                    # Check and delete from `staff` table
                    cursor.execute("SELECT COUNT(*) FROM staff WHERE username = %s", (username,))
                    if cursor.fetchone()[0] > 0:
                        cursor.execute("DELETE FROM staff WHERE username = %s", (username,))
                        connection.commit()
                        messagebox.showinfo("Success", f"User '{username}' deleted.")

                    
                    # Clear the search input
                    self.search_var.set("")  
                    self.search_entry.config(state="normal")  
                    self.search_entry.delete(0, tk.END)
                    self.search_entry.config(state="disabled")  

                except Exception as error:
                    messagebox.showerror("Database Error", f"Error deleting user: {error}")

                finally:
                    # Close the database connection
                    if connection:
                        cursor.close()
                        connection.close()
            else:
                messagebox.showinfo("Cancelled", "User deletion cancelled.")
        else:
            messagebox.showwarning("Input Error", "Please select a user to delete.")

    def find_user_by_username(self, username):
        if username:
            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Query to find the user by username
                cursor.execute("""
                    SELECT user_id, username, password, department, user_type FROM staff WHERE LOWER(username) = LOWER(%s)
                """, (username,))

                user = cursor.fetchone()  # Fetch the user data

                if user:
                    # Create a dictionary to return the user data
                    return {
                        'id': user[0],
                        'username': user[1],
                        'password': user[2],
                        'department': user[3],
                        'user_type': user[4]
                    }
                else:
                    return None  # User not found

            except Exception as error:
                print(f"Error finding user: {error}")
                return None  # Return None if there was an error

            finally:
                # Close the database connection
                if connection:
                    cursor.close()
                    connection.close()
        else:
            return None  # Return None if username is empty

    def delete_department(username):
        department_to_delete = self.search_dept_entry.get()

        if not department_to_delete:
            messagebox.showerror("Error", "Please select a department to delete.")
            return

        try:
            connection = get_db_connection()  # Assuming a function to establish DB connection
            cursor = connection.cursor()
            cursor.execute("DELETE FROM departments WHERE dept_name = %s", (department_to_delete,))
            connection.commit()

            messagebox.showinfo("Success", f"Department '{department_to_delete}' deleted successfully.")
            self.search_dept_entry.config(state="normal")  # Enable the field for clearing
            self.search_dept_entry.delete(0, tk.END)
            self.search_dept_entry.config(state="readonly")  # Make it read-only again

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete department: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete_users_by_department(self, department_name):
        if department_name:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all users in the department {department_name}?"):
                try:
                    # Establish the database connection
                    connection = get_db_connection()
                    cursor = connection.cursor()

                    # Delete users by department from the database
                    cursor.execute("""
                        DELETE FROM staff WHERE department = %s
                    """, (department_name,))

                    # Commit the transaction
                    connection.commit()

                    messagebox.showinfo("Success", f"All users in the department '{department_name}' deleted successfully!")

                except Exception as error:
                    messagebox.showerror("Database Error", f"Error deleting users: {error}")

                finally:
                    # Close the database connection
                    if connection:
                        cursor.close()
                        connection.close()
            else:
                messagebox.showinfo("Cancelled", "User deletion cancelled.")
        else:
            messagebox.showwarning("Input Error", "Please select a valid department.") # Log malformed lines for debugging

    def search_department(self):
        search_term = self.search_dept_entry.get().strip()
        
        if search_term:
            try:
                # Establish the database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Query to search for the department in the database
                cursor.execute("""
                    SELECT dept_name FROM departments WHERE LOWER(dept_name) = LOWER(%s)
                """, (search_term,))

                found_department = cursor.fetchone()  # Fetch the first matching department

                if found_department:
                    self.dept_to_delete_var.set(found_department[0])  # Update label with found department name
                else:
                    self.dept_to_delete_var.set("Department not found")  # Update label if not found

            except Exception as error:
                messagebox.showerror("Database Error", f"Error searching for department: {error}")

            finally:
                # Close the database connection
                if connection:
                    cursor.close()
                    connection.close()

        else:
            self.dept_to_delete_var.set("Please enter a department name.")  

    def logout(self):
        self.frame_dashboard.destroy()  # Destroy the dashboard frame
        self.main_app.show_login_frame()  # Show the login frame again


    def open_password_popup(self):
        """Open the password management popup."""
        self.password_popup = tk.Toplevel(self.root)
        self.password_popup.title("Password Management")
        self.password_popup.geometry("400x300")  # Set popup dimensions
        self.center_window(self.password_popup, 400, 300)  # Center the popup
        
        self.current_frame = None
        self.show_select_category_frame()  # Show the initial frame

    def switch_frame(self, new_frame_func):
        """Switch the content of the popup to a new frame."""
        if self.current_frame:
            self.current_frame.destroy()  # Remove the existing frame
        self.current_frame = tk.Frame(self.password_popup, bg="black")
        self.current_frame.pack(fill="both", expand=True)
        new_frame_func()  # Call the new frame's function to populate the interface

    def show_select_category_frame(self):
        """Show the initial category selection frame."""
        self.switch_frame(lambda: self.populate_select_category_frame())

    def populate_select_category_frame(self):
        """Populate the category selection frame."""
        tk.Label(
            self.current_frame, text="Change Password", font=("Arial", 18),
            bg="black", fg="white"
        ).pack(pady=20)
        
        category_var = tk.StringVar(value="Select Category")
        
        # Dropdown for category selection
        categories = ["Staff", "Departments"]
        category_dropdown = tk.OptionMenu(self.current_frame, category_var, *categories)
        category_dropdown.pack(pady=10)
        
        def handle_category_selection():
            category = category_var.get()
            if category == "Staff":
                self.show_select_user_frame()
            elif category == "Departments":
                self.show_select_department_frame()
        
        # Button to confirm category selection
        tk.Button(
            self.current_frame, text="Select", bg="black", fg="white",
            command=handle_category_selection
        ).pack(pady=20)

    def show_select_user_frame(self):
        """Show the frame for selecting a user."""
        self.switch_frame(lambda: self.populate_select_user_frame())

    def populate_select_user_frame(self):
        """Populate the user selection frame."""
        tk.Label(
            self.current_frame, text="Select User", font=("Arial", 18),
            bg="black", fg="white"
        ).pack(pady=20)

        staff_list = self.fetch_staff()  # Fetch users from the staff table
        if not staff_list:
            tk.Label(self.current_frame, text="No users found", bg="black", fg="white").pack(pady=10)
            return
        
        # Listbox to display staff
        listbox = tk.Listbox(self.current_frame, height=10, width=30)
        for user in staff_list:
            listbox.insert(tk.END, user[1])  # Add usernames to the listbox
        listbox.pack(pady=10)
        
        def handle_user_select(event):
            selected_index = listbox.curselection()
            if selected_index:
                username = listbox.get(selected_index)
                self.show_update_password_frame(username)
        
        listbox.bind("<Double-1>", handle_user_select)

    def show_update_password_frame(self, username):
        """Show the frame to update a user's password."""
        self.switch_frame(lambda: self.populate_update_password_frame(username))

    def populate_update_password_frame(self, username):
        """Populate the frame for updating a user's password."""
        # Clear and set the frame's configuration
        self.current_frame.configure(bg="black")
        
        # Add the title
        tk.Label(
            self.current_frame, text=f"Update Password for '{username}'", font=("Arial", 14),
            bg="black", fg="white"
        ).pack(pady=10)

        # Label for current password
        tk.Label(
            self.current_frame, text="Current Password:", bg="black", fg="white"
        ).pack(pady=5)

        # Frame for the password input field and show/hide label
        password_frame = tk.Frame(self.current_frame, bg="black")
        password_frame.pack(pady=5)

        # Variable to store the current password
        self.current_password_var = tk.StringVar()

        # Input field for the current password (initially hidden)
        self.current_password_entry = tk.Entry(
            password_frame, textvariable=self.current_password_var, show="*", state="readonly", width=15
        )
        self.current_password_entry.pack(side=tk.LEFT, padx=5)

        # Label for Show / Hide toggle
        self.show_hide_label = tk.Label(
            password_frame, text="Show", bg="black", fg="white", cursor="hand2"
        )
        self.show_hide_label.pack(side=tk.LEFT, padx=5)
        self.show_hide_label.bind("<Button-1>", lambda event: self.toggle_current_password_visibility())

        # Fetch and populate the current password for the user
        self.fetch_and_populate_current_user_password(username)

        # Label for new password
        tk.Label(
            self.current_frame, text="Enter New Password:", bg="black", fg="white"
        ).pack(pady=5)

        # Input field for new password
        self.new_password_var = tk.StringVar()
        tk.Entry(self.current_frame, textvariable=self.new_password_var, show="*", width=25).pack(pady=5)

        # Label for confirming password
        tk.Label(
            self.current_frame, text="Re-enter Password:", bg="black", fg="white"
        ).pack(pady=5)

        # Input field for confirm password
        self.confirm_password_var = tk.StringVar()
        tk.Entry(self.current_frame, textvariable=self.confirm_password_var, show="*", width=25).pack(pady=5)

        # Button for handling password update
        tk.Button(
            self.current_frame, text="Enter", bg="black", fg="white",
            command=lambda: self.show_confirm_password_frame(username, self.new_password_var.get())
        ).pack(pady=20)

    def fetch_and_populate_current_user_password(self, username):
        """Fetch the current password for the selected user and populate the input field."""
        try:
            # Establish a connection to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch the current password for the given username
            cursor.execute("SELECT password FROM staff WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                current_password = result[0]  # Assuming 'password' is the first column
                self.current_password_var.set(current_password)  # Populate the input field with the password
            else:
                messagebox.showerror("Error", f"Password for user '{username}' not found.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()

    def toggle_current_password_visibility(self):
        """Toggle the visibility of the current password field."""
        current_state = self.current_password_entry.cget("show")
        if current_state == "*":
            # Show password
            self.current_password_entry.config(show="")
            self.show_hide_label.config(text="Hide", fg="white")
        else:
            # Hide password
            self.current_password_entry.config(show="*")
            self.show_hide_label.config(text="Show", fg="white")



    def show_confirm_password_frame(self, username, password):
        """Show the frame to confirm the password."""
        self.switch_frame(lambda: self.populate_confirm_password_frame(username, password))

    def populate_confirm_password_frame(self, username, password):
        """Populate the frame to confirm the password."""
        tk.Label(
            self.current_frame, text="Confirm Password", font=("Arial", 18),
            bg="black", fg="white"
        ).pack(pady=20)
        
        confirm_password_var = tk.StringVar()
        tk.Entry(self.current_frame, textvariable=confirm_password_var, show="*").pack(pady=10)
        
        def handle_confirmation():
            if confirm_password_var.get() == password:
                self.update_staff_password(username, password)
                messagebox.showinfo("Success", f"Password successfully updated for '{username}'.")
                self.password_popup.destroy()
            else:
                messagebox.showerror("Error", "Passwords do not match.")
        
        tk.Button(
            self.current_frame, text="Confirm", bg="black", fg="white",
            command=handle_confirmation
        ).pack(pady=20)

    def show_select_department_frame(self):
        """Show the frame for selecting a department."""
        self.switch_frame(lambda: self.populate_select_department_frame())

    def populate_select_department_frame(self):
        """Populate the department selection frame."""
        tk.Label(
            self.current_frame, text="Select Department", font=("Arial", 18),
            bg="black", fg="white"
        ).pack(pady=20)
        
        department_list = self.fetch_departments()  # Fetch departments from the database
        if not department_list:
            tk.Label(self.current_frame, text="No departments found", bg="black", fg="white").pack(pady=10)
            return
        
        listbox = tk.Listbox(self.current_frame, height=10, width=30)
        for dept in department_list:
            listbox.insert(tk.END, dept[1])  # Add department names to the listbox
        listbox.pack(pady=10)
        
        def handle_department_select(event):
            selected_index = listbox.curselection()
            if selected_index:
                department_name = listbox.get(selected_index)
                self.show_update_department_password_frame(department_name)
        
        listbox.bind("<Double-1>", handle_department_select)

    def fetch_staff(self):
        """Fetch staff members from the database."""
        try:
            connection = get_db_connection()  # Replace with your database connection method
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, username FROM staff ORDER BY username ASC")  # Adjust columns as per your table schema
            staff_list = cursor.fetchall()  # Returns a list of tuples [(id, username), ...]
            return staff_list
        except Exception as e:
            messagebox.showerror("Database Error", str(e))  # Show error message
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()





    def update_staff_password(self, username, password):
        """Update the password for a staff member."""
        try:
            connection = get_db_connection()  # Replace with your database connection method
            cursor = connection.cursor()
            
            # Optionally hash the password
            #hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Update the password in the database
            cursor.execute(
                "UPDATE staff SET password = %s WHERE username = %s",
                (password, username)
                #(hashed_password, username)
            )
            connection.commit()

            # Show success feedback
            #messagebox.showinfo("Success", f"Password successfully updated for '{username}'.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update password: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()
    def fetch_departments(self):
        """Fetch all departments from the database."""
        try:
            connection = get_db_connection()  # Replace with your database connection method
            cursor = connection.cursor()

            # Query to fetch all department names
            cursor.execute("SELECT dept_id, dept_name FROM departments")
            department_list = cursor.fetchall()  # Fetch all results

            return department_list  # Return the list of tuples [(id, name), ...]

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch departments: {e}")
            return []  # Return an empty list on error

        finally:
            if connection:
                cursor.close()
                connection.close()
    def show_update_department_password_frame(self, department_name):
        """Show the frame to update the password for the selected department."""
        self.switch_frame(lambda: self.populate_update_department_password_frame(department_name))

    def populate_update_department_password_frame(self, department_name):
        """Populate the interface for updating the password of a department."""
        # Clear the current frame and set the title
        self.current_frame.configure(bg="black")
        tk.Label(self.current_frame, text=f"Update Password for {department_name} Department", 
                 font=("Arial", 14), bg="black", fg="white").pack(pady=10)

        # Current password label
        tk.Label(self.current_frame, text="Current Password:", bg="black", fg="white").pack(pady=5)

        # Variable to store current password
        self.current_password_var = tk.StringVar()

        # Frame to hold the current password input field and show/hide button
        current_password_frame = tk.Frame(self.current_frame, bg="black")
        current_password_frame.pack(pady=5)

        # Current password entry field
        self.current_password_entry = tk.Entry(current_password_frame, textvariable=self.current_password_var, show="*",state="readonly", width=15)
        self.current_password_entry.pack(side=tk.LEFT, padx=5)

        # Show/hide password functionality
        def toggle_current_password_visibility():
            if self.current_password_entry.cget("show") == "*":
                self.current_password_entry.config(show="")
                toggle_button.config(text="Hide")
            else:
                self.current_password_entry.config(show="*")
                toggle_button.config(text="Show")

        # Toggle button for current password visibility
        toggle_button = tk.Button(current_password_frame, text="Show", command=toggle_current_password_visibility, bg="black", fg="white", borderwidth=0)
        toggle_button.pack(side=tk.LEFT)

        # Fetch and populate the current password for the department
        self.fetch_and_populate_current_password(department_name)

        # New password label and entry
        tk.Label(self.current_frame, text="Enter New Password:", bg="black", fg="white").pack(pady=5)
        self.new_password_var = tk.StringVar()
        tk.Entry(self.current_frame, textvariable=self.new_password_var, show="*", width=25).pack(pady=5)

        # Confirm password label and entry
        tk.Label(self.current_frame, text="Confirm Password:", bg="black", fg="white").pack(pady=5)
        self.confirm_password_var = tk.StringVar()
        tk.Entry(self.current_frame, textvariable=self.confirm_password_var, show="*", width=25).pack(pady=5)

        # Submit button
        submit_button = tk.Button(self.current_frame, text="Update Password", bg="black", fg="white", 
                                   command=lambda: self.update_department_password(department_name))
        submit_button.pack(pady=10)

    def fetch_and_populate_current_password(self, department_name):
        """Fetch the current password for the selected department from the database and populate the input field."""
        try:
            # Get a database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch the current password
            cursor.execute("SELECT dept_password FROM departments WHERE dept_name = %s", (department_name,))
            result = cursor.fetchone()

            if result:
                current_password = result[0]  # Assuming dept_password is in the first column
                self.current_password_var.set(current_password)  # Populate the input field with the password
            else:
                messagebox.showerror("Error", f"Password for department '{department_name}' not found.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection:
                cursor.close()
                connection.close()



    def update_department_password(self, department_name):
        """Update the password for the given department."""
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not new_password or not confirm_password:
            messagebox.showerror("Input Error", "Please enter and confirm the password.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Mismatch Error", "Passwords do not match.")
            return

        try:
            connection = get_db_connection()  # Replace with your database connection function
            cursor = connection.cursor()

            # Update the password for the department in the database
            cursor.execute("UPDATE departments SET dept_password = %s WHERE dept_name = %s", 
                           (new_password, department_name))
            connection.commit()

            messagebox.showinfo("Success", f"Password updated successfully for department '{department_name}'.")
            

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update password: {e}")

        finally:
            if connection:
                cursor.close()
                connection.close()

