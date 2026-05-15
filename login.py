import tkinter as tk
from tkinter import messagebox
from database import get_db_connection
from psycopg2 import sql
import bcrypt

class Login:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.valid_users = self.load_admin_credentials()  # Load all admin credentials from the database
        self.valid_departments = self.load_departments()
        self.valid_staff = self.load_staff()  

        # Create a frame with a black border
        self.frame_login = tk.Frame(root, bg="black", bd=5)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame
        self.logged_in_user = None
        # Set the dimensions of the frame
        self.frame_login.config(width=300, height=400)

        # Create a canvas for rounded corners
        self.canvas = tk.Canvas(self.frame_login, bg="white", width=300, height=400, highlightthickness=0)
        self.canvas.pack()

        # Draw rounded rectangle
        self.rounded_rectangle(self.canvas, 10, 10, 290, 390, radius=20, fill="black", outline="black")

        # Create and place the title label
        self.label_title = tk.Label(self.canvas, text="The Swan Hotel", font=("Arial", 20), bg="black", fg="white")
        self.label_title.place(x=50, y=30)

        # Create and place the username label and entry
        self.label_username = tk.Label(self.canvas, text="Username:", font=("Arial", 12), bg="black", fg="white")
        self.label_username.place(x=30, y=100)

        self.entry_username = tk.Entry(self.canvas)
        self.entry_username.place(x=30, y=130, width=240)

        # Create and place the password label and entry
        self.label_password = tk.Label(self.canvas, text="Password:", font=("Arial", 12), bg="black", fg="white")
        self.label_password.place(x=30, y=170)

        self.entry_password = tk.Entry(self.canvas, show='*')
        self.entry_password.place(x=30, y=200, width=240)

        # Create and place the Login button
        self.button_login = tk.Button(self.canvas, text="Login", font=("Arial", 12), command=self.login, bg="black", fg="white")
        self.button_login.place(x=30, y=250, width=240)

        # Create and place the Close button
        self.create_close_button()

    def create_close_button(self):
        self.close_button = tk.Button(self.root, text="Close", command=self.close, bg="black", fg="white", font=("Arial", 12))
        self.close_button.pack(side=tk.BOTTOM, pady=230)  # Centered at the bottom with padding

    def close(self):
        self.root.destroy()

    def rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        # Create rounded rectangle
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        canvas.create_polygon(points, **kwargs, smooth=True)

    def load_admin_credentials(self):
        connection = None
        admin_credentials = {}
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT username, hashed_password FROM admin")
            results = cursor.fetchall()
            for row in results:
                admin_credentials[row[0]] = row[1]  # Store all admin usernames and passwords
        except Exception as error:
            print("Error loading admin credentials:", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return admin_credentials  # Return all admin credentials

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the user exists and if the password is correct
        if username in self.valid_users and self.valid_users[username] == password:
            # Compare entered password with stored password
            if password == self.valid_users[username]:
                self.logged_in_user = username
                self.main_app.logged_in_user = username
                self.main_app.show_dashboard()  # Redirect to dashboard for Admin
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        elif username in self.valid_departments:
            if password == self.valid_departments[username]:
                # Department login successful
                self.main_app.show_department_frame(username)  # Assuming this method exists
            else:
                messagebox.showerror("Login Failed", "Invalid department username or password.")
        elif username in self.valid_staff:
            staff_member = self.valid_staff[username]
            if staff_member['lock_status']:  # Check if the account is locked
                messagebox.showerror("Account Locked", "Your account has been locked. Please contact administrator.")
            elif password == staff_member['password']:
                # Check the user type (staff, supervisor, manager)
                user_type = self.load_heads(username)

                if user_type == "Supervisor":
                    # Show heads frame for Supervisor/Manager
                    self.main_app.show_heads_frame(username)
                if user_type == "Staff":
                    # Show Users frame for Staff
                    self.main_app.show_users_frame(username)

                if user_type != "Supervisor" and user_type != "Manager" and user_type != "Staff":
                    messagebox.showerror("Login Failed", "Invalid user type.")  # Error for invalid user type

            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showerror("Login Failed", "User not found.")
#Add a manager interface whereby he has his own independent interface as a superuser below the admin.
#if user_type == "Supervisor" or user_type == "Manager":




    def load_staff(self):
        staff = {}
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch staff details
            cursor.execute("SELECT user_id, username, department, password, lock_status FROM staff")
            rows = cursor.fetchall()  # Fetch all rows from the result

            for row in rows:
                user_id, username, department, password, lock_status = row
                staff[username] = {
                    'password': password.strip(),
                    'lock_status': lock_status,
                    'department': department
                }

        except Exception as error:
            print(f"Error loading staff: {error}")
        
        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

        return staff

    def load_departments(self):
        departments = {}
        try:
            # Establish the database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all departments
            cursor.execute("SELECT dept_id, dept_name, dept_password FROM departments")
            rows = cursor.fetchall()  # Fetch all rows from the result

            for row in rows:
                dept_id, dept_name, dept_password = row
                departments[dept_name] = dept_password.strip()  # Use department name as key

        except Exception as error:
            print(f"Error loading departments: {error}")
        
        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

        return departments



    def load_heads(self, username):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if the current user is a Supervisor or Manager
            query = sql.SQL("SELECT user_type FROM staff WHERE username = %s")
            cursor.execute(query, (username,))
            user_type = cursor.fetchone()

            if user_type:  # If user_type is not None, fetch the value
                return user_type[0]  # Return the first value from the tuple (user_type)
            else:
                return None  # Return None if no user type was found for the username

        except Exception as e:
            print(f"Error loading user type: {e}")
            messagebox.showerror("Error", "An error occurred while loading data.")
            return None

        finally:
            if connection:
                cursor.close()
                connection.close()
