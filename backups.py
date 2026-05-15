    def create_staff_box(self):
        # Create the main frame
        manage_admin_frame = tk.Frame(self, borderwidth=8, relief="groove", bg="black", width=800, height=600)
        self.center_window(manage_admin_frame, 1100, 700)  # Center the box
        manage_admin_frame.pack_propagate(False)

        # Add "The Swan Hotel" text at the top
        tk.Label(manage_admin_frame, text="The Swan Hotel", font=("Arial", 26), bg="black", fg="white").pack(pady=5)

        # Add the Welcome label below the Department label
        label_welcome = tk.Label(manage_admin_frame, text=f"Username: {self.username}", font=("Arial", 18), bg="black", fg="white")
        label_welcome.pack(pady=5)

        # Create a frame for department-specific content
        department_container = tk.Frame(manage_admin_frame, bg="gray")
        department_container.pack(fill="both", expand=True, pady=10)

        # Add department label
        tk.Label(department_container, text=f"{self.department}", font=("Arial", 22), bg="gray", fg="white").pack(pady=5)

        # Create a frame for buttons in two columns
        buttons_frame = tk.Frame(department_container, bg="gray")
        buttons_frame.pack(pady=10)

        # Function to clear department_container and load new content
        def clear_and_load(new_content_method):
            for widget in department_container.winfo_children():
                widget.destroy()  # Clear current content
            new_content_method(department_container)

        # Create a container for holding each interface content
        content_container = tk.Frame(department_container, bg="white", width=780, height=400)
        content_container.pack(fill="both", expand=True, pady=10)

        # Define the button actions based on department
        if self.department == "HouseKeeping":
            tk.Button(
                buttons_frame,
                text="Task Sheet",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_task_sheet)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Room Allocation",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_room_allocation)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Arrivals",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_arrivals)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Requisitions",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_requisitions)  # Call appropriate method
            ).pack(pady=10)

        elif self.department == "FnB":
            tk.Button(
                buttons_frame,
                text="Menu",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_menu)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Billings",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_billings)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Stocks",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_stocks)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Requisitions",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_requisitions)  # Call appropriate method
            ).pack(pady=10)

        elif self.department == "Finance":
            tk.Button(
                buttons_frame,
                text="Invoice processing",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_invoice_processing)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Reports",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_reports)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Payroll processing",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_payroll_processing)  # Call appropriate method
            ).pack(pady=10)

            tk.Button(
                buttons_frame,
                text="Audit",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_audit)  # Call appropriate method
            ).pack(pady=10)

        elif self.department == "Front Office":
            # Front Office buttons in grid
            front_office_button = tk.Button(
                buttons_frame,
                text="Reception",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_front_office)  # Call appropriate method
            )
            front_office_button.grid(row=0, column=0, padx=10, pady=10)

            laundry_button = tk.Button(
                buttons_frame,
                text="Cashier",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_cashier)  # Call appropriate method
            )
            laundry_button.grid(row=0, column=1, padx=10, pady=10)

            sales_button = tk.Button(
                buttons_frame,
                text="Reservations",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_bookings)  # Call appropriate method
            )
            sales_button.grid(row=0, column=2, padx=10, pady=10)

            bookings_button = tk.Button(
                buttons_frame,
                text="Night Audit",
                bg="black",
                fg="white",
                font=("Arial", 14),
                width=20,
                command=lambda: clear_and_load(self.show_audit)  # Call appropriate method
            )
            bookings_button.grid(row=0, column=3, padx=10, pady=10)

        # Logout Button
        logout_button = tk.Button(manage_admin_frame, text="Logout", command=self.logout, bg="black", fg="white", font=("Arial", 14))
        logout_button.pack(side="bottom", pady=(0, 10))