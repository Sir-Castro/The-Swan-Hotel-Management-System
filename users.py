import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from psycopg2 import sql
from database import get_db_connection
from tkinter import messagebox, simpledialog
from datetime import datetime

class Users(tk.Frame):
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

        # Fetch department from database
        #To remove fade in and fade out just delete show logo with fade, fade in logo and fade out logo methods
        #Remember to initialize the method held in fade out logo else statements
        self.department = self.get_department()
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
            # Once fully faded out, display the main content
            self.create_staff_box()

    def get_department(self):
        """Fetch the department from the staff table based on the username."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = sql.SQL("SELECT department FROM staff WHERE username = %s")
            cursor.execute(query, (self.username,))
            result = cursor.fetchone()
            return result[0] if result else "Unknown"
        except Exception as e:
            print(f"Error fetching department: {e}")
            return "Unknown"
        finally:
            if connection:
                cursor.close()
                connection.close()

    def create_staff_box(self):
        # Create the main frame
        manage_admin_frame = tk.Frame(self, borderwidth=8, relief="groove", bg="black", width=800, height=600)
        self.center_window(manage_admin_frame, 1100, 700)  # Center the box
        manage_admin_frame.pack_propagate(False)

        # Add department label
        tk.Label(manage_admin_frame, text=f"{self.department} Department", font=("Arial", 22), bg="black", fg="white").pack(pady=5)

        # Create a frame for department-specific content
        department_container = tk.Frame(manage_admin_frame, bg="gray")
        department_container.pack(fill="both", expand=True, pady=10)

        # Add the Welcome label below the Department label
        label_welcome = tk.Label(department_container, text=f"Staff: {self.username}", font=("Arial", 18), bg="gray", fg="white")
        label_welcome.pack(pady=5)

        # Create a frame for buttons in two columns
        buttons_frame = tk.Frame(department_container, bg="gray")
        buttons_frame.pack(pady=10)

        # Create a container for holding each interface content with scrollable functionality
        canvas = tk.Canvas(department_container, bg="gray", height=300)
        scrollbar = tk.Scrollbar(department_container, bg="gray", orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg="gray", width=780)

        # Configure the scrollbar and canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the scrollbar and canvas inside the department container
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a window inside the canvas to hold the content
        canvas.create_window((5, 5), window=content_frame, anchor="nw")

        # Bind the canvas to resize the content when the window size changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", on_frame_configure)

        # Add a default "Welcome" label to the content_frame
        welcome_label = tk.Label(content_frame, text="The Swan Hotel", font=("Arial", 45), fg="white", bg="gray", anchor="center")
        welcome_label.pack(expand=True, padx=300, pady=150)

        # Function to clear department_container and load new content
        def clear_and_load(content_container, new_content_method):
            # Destroy the existing widgets (e.g., the "Welcome" label)
            for widget in content_container.winfo_children():
                widget.destroy()

            # Call the new content method to load content into the container
            new_content_method(content_container)

        # Dictionary defining buttons for each department
        department_buttons = {
            "HouseKeeping": [("Task Sheet", self.show_front_office),
                             ("Room Allocation", self.show_front_office),
                             ("Arrivals", self.show_front_office),
                             ("Requisitions", self.show_front_office)],
            "FnB": [("Menu", self.show_front_office),
                    ("Billings", self.show_front_office),
                    ("Stocks", self.show_front_office),
                    ("Requisitions", self.show_front_office)],
            "Finance": [("Invoice processing", self.show_front_office),
                        ("Reports", self.show_front_office),
                        ("Payroll processing", self.show_front_office),
                        ("Audit", self.show_front_office)],
            "Front Office": [("Reservations", self.show_front_office),
                             ("Reception", self.show_front_office),
                             ("Cashier", self.show_front_office),
                             ("Night Audit", self.show_front_office)],
            "ICT": [("Support Ticketing", self.support_tickets),
                    ("Security Management", self.security_management),
                    ("Maintenance", self.maintenance_logs),
                    ("Data Backup", self.data_backup)],
        }

        # Create buttons dynamically for the current department
        buttons = department_buttons.get(self.department, [])
        for i, (text, command) in enumerate(buttons):
            button = tk.Button(
                buttons_frame,
                text=text,
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda cmd=command: clear_and_load(content_frame, cmd)
            )
            button.grid(row=0, column=i, padx=10, pady=10)

        # Logout Button
        logout_button = tk.Button(manage_admin_frame, text="Logout", command=self.logout, bg="black", fg="white", font=("Arial", 14))
        logout_button.pack(side="bottom", pady=(0, 10))

    def center_window(self, window, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.place(x=x, y=y, width=width, height=height)

    def logout(self):
        """Log out and return to the login screen"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            # Destroy the current frame (the Users frame)
            self.destroy()
            
            # Call the method to show the login frame in the main application
            self.main_app.show_login_frame()

    def check_ins(self):
        # Capture the values for check-in and room allocation
        full_name = self.full_name_entry.get()
        check_in_date = self.check_in_date_entry.get()
        id_number = self.id_number_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        period_stay = self.period_stay_entry.get()
        room_pref = self.room_pref_combobox.get()
        purpose = self.purpose_combobox.get()
        
        # Staff username performing the check-in
        staff_username = self.username  # Uses self.username for the logged-in staff

        # Simple validation (you can add more sophisticated checks)
        if not full_name or not check_in_date or not id_number or not phone_number:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        # Insert guest check-in data into the database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = sql.SQL("""
                INSERT INTO checkins (full_name, check_in_date, id_number, phone_number, email, period_stay, room_pref, purpose, staff)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(query, (full_name, check_in_date, id_number, phone_number, email, period_stay, room_pref, purpose, staff_username))
            connection.commit()
            messagebox.showinfo("Success", "Guest check-in recorded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def check_out_guest(self):
        # Capture the values for check-out and billing
        check_out_date = self.check_out_date_entry.get()
        billing_amount = self.billing_amount_entry.get()
        payment_method = self.payment_method_entry.get()

        # Simple validation
        if not check_out_date or not billing_amount or not payment_method:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        # Process check-out and billing
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = sql.SQL("""
                INSERT INTO billing (check_out_date, billing_amount, payment_method)
                VALUES (%s, %s, %s)
            """)
            cursor.execute(query, (check_out_date, billing_amount, payment_method))
            connection.commit()
            messagebox.showinfo("Success", "Guest checked out and billed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def show_front_office(self, parent_frame):
        # Clear the parent frame but keep the parent frame itself intact
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Add Check-In and Check-Out interfaces within the same parent_frame
        main_content = tk.Frame(parent_frame, bg="black", width=1040, height=350)
        main_content.pack_propagate(False)
        main_content.pack(padx=10, pady=5)

        # Left section for Check-In and Room Allocation
        left_frame = tk.Frame(main_content, bg="lightgray", width=550)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        tk.Label(left_frame, text="Check-In and Room Allocation", bg="lightgray", fg="black", font=("Arial", 14)).grid(row=0, column=0, columnspan=4, pady=10)

        # Group 1: Full Name, Check-In Date, ID Number, Phone Number
        tk.Label(left_frame, text="Full Name:", bg="lightgray", fg="black").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.full_name_entry = tk.Entry(left_frame, width=20)
        self.full_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Date of Check-In:", bg="lightgray", fg="black").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.check_in_date_entry = tk.Entry(left_frame, width=20, state="readonly")
        self.check_in_date_entry.grid(row=1, column=3, padx=5, pady=5)

        # Use a StringVar to manage the content of the read-only Entry
        self.check_in_date_var = tk.StringVar()
        self.check_in_date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.check_in_date_entry.configure(textvariable=self.check_in_date_var)

        tk.Label(left_frame, text="ID Number:", bg="lightgray", fg="black").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.id_number_entry = tk.Entry(left_frame, width=20)
        self.id_number_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Phone Number:", bg="lightgray", fg="black").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.phone_number_entry = tk.Entry(left_frame, width=20)
        self.phone_number_entry.grid(row=2, column=3, padx=5, pady=5)

        # Group 2: Email Address, Number of Guests, Room Preference, Purpose of Stay
        tk.Label(left_frame, text="Email Address:", bg="lightgray", fg="black").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = tk.Entry(left_frame, width=20)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Period of stay:", bg="lightgray", fg="black").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.period_stay_entry = tk.Entry(left_frame, width=20)
        self.period_stay_entry.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(left_frame, text="Room Preference:", bg="lightgray", fg="black").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.room_pref_combobox = ttk.Combobox(left_frame, width=17, state="readonly")
        self.room_pref_combobox['values'] = [
            "Delux Single", "Delux Double", "Delux Triple",
            "Executive Delux Single", "Executive Delux Double", "Executive Delux Triple",
            "Junior Suite Single", "Junior Suite Double", "Junior Suite Triple",
            "1 Bedroom Single", "1 Bedroom Double", "1 Bedroom Triple",
            "2 Bedroom",
            "Presidential Suite"
        ]
        self.room_pref_combobox.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Purpose of Stay:", bg="lightgray", fg="black").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.purpose_combobox = ttk.Combobox(left_frame, width=17, state="readonly")
        self.purpose_combobox['values'] = ["Leisure", "Business"]
        self.purpose_combobox.grid(row=4, column=3, padx=5, pady=5)

        # Allocate Room Button
        tk.Button(left_frame, text="Check in", bg="black", fg="white", command=self.check_ins).grid(row=5, column=0, columnspan=4, pady=10)

        # Right section for Check-Out and Billing
        right_frame = tk.Frame(main_content, bg="lightgray", width=550)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        tk.Label(right_frame, text="Check-Out and Billing", bg="lightgray", fg="black", font=("Arial", 14)).grid(row=0, column=0, columnspan=4, pady=10)

        # Group 1: Full Name and Room Number
        tk.Label(right_frame, text="Full Name:", bg="lightgray", fg="black").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.full_name_checkout_entry = tk.Entry(right_frame, width=20)
        self.full_name_checkout_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="Room Number:", bg="lightgray", fg="black").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.room_number_entry = tk.Entry(right_frame, width=20)
        self.room_number_entry.grid(row=1, column=3, padx=5, pady=5)

        # Group 2: Billing (Room Charges and Food Charges)
        tk.Label(right_frame, text="Room Charges:", bg="lightgray", fg="black").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.room_charges_entry = tk.Entry(right_frame, width=20)
        self.room_charges_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="Food Charges:", bg="lightgray", fg="black").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.food_charges_entry = tk.Entry(right_frame, width=20)
        self.food_charges_entry.grid(row=2, column=3, padx=5, pady=5)

        # Group 3: Payment Method and Payment Code
        tk.Label(right_frame, text="Payment Method:", bg="lightgray", fg="black").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.payment_method_entry = tk.Entry(right_frame, width=20)
        self.payment_method_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="Payment Code:", bg="lightgray", fg="black").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.payment_code_entry = tk.Entry(right_frame, width=20)
        self.payment_code_entry.grid(row=3, column=3, padx=5, pady=5)

        # Group 4: Check-Out Date and Time (auto-captured)
        tk.Label(right_frame, text="Check-Out Date and Time:", bg="lightgray", fg="black").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.check_out_date_time_label = tk.Label(right_frame, text="", bg="lightgray", fg="black", font=("Arial", 10))
        self.check_out_date_time_label.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Update Check-Out Date and Time automatically
        #from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.check_out_date_time_label.config(text=current_time)

        # Check-Out Button
        tk.Button(right_frame, text="Check Out", bg="black", fg="white", command=self.check_out_guest).grid(row=5, column=0, columnspan=4, pady=10)

    def support_tickets(self, parent_frame):
        # Clear the parent frame but keep it intact
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Create a single frame filling the entire parent container
        main_frame = tk.Frame(parent_frame, bg="black")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title Label (Centered)
        title_label = tk.Label(main_frame, text="Ticketing", bg="black", fg="white", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # ListView (Treeview for displaying tickets)
        columns = ("Ticket No.", "Dept", "Description", "Date/Time", "Status", "Review")
        ticket_list = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

        # Define column headings
        for col in columns:
            ticket_list.heading(col, text=col)
            ticket_list.column(col, anchor="center", width=170)  # Adjust width as needed

        ticket_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample Data (You can replace this with actual data fetching logic)
        sample_tickets = [
            (1, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Good work", ),
            (2, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Good work", ),
            (3, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Good work", ),
        ]

        for ticket in sample_tickets:
            ticket_list.insert("", "end", values=ticket)


    def maintenance_logs(self, parent_frame):
        # Clear the parent frame but keep it intact
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Create a single frame filling the entire parent container
        main_frame = tk.Frame(parent_frame, bg="black")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title Label (Centered)
        title_label = tk.Label(main_frame, text="Maintenance Logs", bg="black", fg="white", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # ListView (Treeview for displaying tickets)
        columns = ("Log No.", "Dept", "Description", "Date/Time", "Status", "Review")
        ticket_list = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

        # Define column headings
        for col in columns:
            ticket_list.heading(col, text=col)
            ticket_list.column(col, anchor="center", width=170)  # Adjust width as needed

        ticket_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample Data (You can replace this with actual data fetching logic)
        sample_tickets = [
            (1, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Good work", ),
            (2, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Good work", ),
            (3, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Good work", ),
        ]

        for ticket in sample_tickets:
            ticket_list.insert("", "end", values=ticket)


    def data_backup(self, parent_frame):
        # Clear the parent frame but keep it intact
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Create a single frame filling the entire parent container
        main_frame = tk.Frame(parent_frame, bg="black")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title Label (Centered)
        title_label = tk.Label(main_frame, text="Data Backup", bg="black", fg="white", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # ListView (Treeview for displaying tickets)
        columns = ("Log No.", "Department", "Description", "Date/Time", "Status", "Action")
        ticket_list = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

        # Define column headings
        for col in columns:
            ticket_list.heading(col, text=col)
            ticket_list.column(col, anchor="center", width=170)  # Adjust width as needed

        ticket_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample Data (You can replace this with actual data fetching logic)
        sample_tickets = [
            (1, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Button", ),
            (2, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Button", ),
            (3, "Front Office", "Internet Down", "2025-02-19 9:00am",  "Resolved", "Button", ),
        ]

        for ticket in sample_tickets:
            ticket_list.insert("", "end", values=ticket)



    def security_management(self, parent_frame):
        # Clear parent frame but keep it intact
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Main content frame
        main_content = tk.Frame(parent_frame, bg="black", width=1040, height=420)
        main_content.pack_propagate(False)
        main_content.pack(padx=5, pady=5)

        # Left section - Network Monitor
        left_frame = tk.Frame(main_content, bg="lightgray", width=600)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(left_frame, text="Network Monitor", bg="lightgray", fg="black", font=("Arial", 14)).pack(pady=10)
        
        network_listbox = tk.Listbox(left_frame, width=50, height=18)
        network_listbox.pack(padx=10, pady=5, fill="x")
        
        # Sample data for network monitoring
        network_data = [
            "Router: Online",
            "Firewall: Active",
            "Bandwidth Usage: 70%",
            "Server 1: Running",
            "Server 2: Running",
            "Database: Connection Stable"
        ]
        for item in network_data:
            network_listbox.insert(tk.END, item)

        # Buttons below the listbox
        button_frame_left = tk.Frame(left_frame, bg="lightgray")
        button_frame_left.pack(pady=5)
        
        tk.Button(button_frame_left, text="Firewall Testing", bg="lightgray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame_left, text="Network Analysis", bg="lightgray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame_left, text="Device Configuration", bg="lightgray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
        
        # Right section - System Updates
        right_frame = tk.Frame(main_content, bg="lightgray", width=600)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(right_frame, text="System Updates", bg="lightgray", fg="black", font=("Arial", 14)).pack(pady=10)
        
        updates_listbox = tk.Listbox(right_frame, width=50, height=18)
        updates_listbox.pack(padx=10, pady=5, fill="x")
        
        # Sample data for system updates
        updates_data = [
            "Security Patch Applied - 2025-02-19",
            "Database Backup Completed",
            "New Firewall Rules Implemented",
            "User Access Logs Updated",
            "System Health Check Completed"
        ]
        for item in updates_data:
            updates_listbox.insert(tk.END, item)

        button_frame_right = tk.Frame(right_frame, bg="lightgray")
        button_frame_right.pack(pady=5)
        
        tk.Button(button_frame_right, text="Security Patch", bg="lightgray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame_right, text="System Health Checks", bg="lightgray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame_right, text="User Access Logs", bg="lightgray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)



