# Importing all of tkinter
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
import tkinter as tk
# Importing Pillow for working with images in the window
from PIL import *
from PIL import Image, ImageTk
# Importing the ttkbootstrap for better UI
from ttkbootstrap.constants import *
import ttkbootstrap as tb
# Importing subprocess for Knit Out
import subprocess
# Importing datetime for current date and time
from datetime import datetime
# Importing mysql.connector for database
import mysql.connector
# Importing matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Defining the PMS class
class PMS:
    def __init__(self, root):
        
        # Initializing the PMS class with the root window
        self.root = root
        # Set the geometry of the window
        self.root.geometry('1440x900') # This could be useful after Restoring Down the window
        self.root.state('zoomed') # Setting the window state to 'zoomed'
        self.root.title('Gajul Fabrics') # Setting the window title
        self.root.iconbitmap('images/favicon.ico')  # Setting the window icon
        
        
        # ===Loading the Icon Image===
        self.icon_title = PhotoImage(file='images/favicon-3.png')
        
        # ===Label for title=== 
        title_label = Label(
            self.root,
            text=" Production & Payroll Management System", 
            image=self.icon_title, compound=LEFT, 
            font=("Garamond", 40, "bold"), 
            anchor='w'
        ).place(x=0,y=0,relwidth=1, height=70)  # Placing the title label inside the window
        
        # ===Logout Button===
        logout_button = Button(
            self.root, text="Knit Out", 
            font=("Garamond", 20, "bold"),
            cursor="hand2",
            command=self.redirect_to_homepage
        ).place(x=1750, y=20, height=50, width=150)  # Placing the logout button inside the window
        
        # ===Clock===
        self.clock_label = Label(
            self.root,
            text="Clock", # Initialize with empty text
            font=("Garamond", 15)
        )
        self.clock_label.place(x=0,y=70,relwidth=1, height=30)  # Placing the title label inside the window
        self.update_clock() # Update the clock label every 1000 milliseconds (1 second)

        # Execute the database creation query before making the connection
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin"
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS production")
            
        except mysql.connector.Error as error:
            print("Error creating database: {}".format(error))
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        
        # Making the database connection here 
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="production"
        )

        # Create a cursor object to execute SQL queries
        self.mycursor = self.mydb.cursor(buffered=True)
            
        execute_once = True
        
        while execute_once:
            try:
                
                # Product Table Creation ==========================================================================
                
                self.mycursor.execute('''
                    CREATE TABLE IF NOT EXISTS Product(
                    Product_Id INT AUTO_INCREMENT,
                    Name VARCHAR(100) NOT NULL,
                    Size INT NOT NULL,
                    Price FLOAT NOT NULL,
                    CONSTRAINT c_pi_pk PRIMARY KEY(Product_Id)
                    )
                ''')
                        
                self.mydb.commit()
                        
                self.mycursor.execute('''
                    ALTER TABLE Product auto_increment = 101
                ''')
                
                self.mydb.commit()
                        
                self.mycursor.execute(
                    '''
                    INSERT INTO Product(Product_Id, Name, Size, Price) VALUES(101, 'Towel', 3060, 9.1)
                    '''
                )
                
                self.mydb.commit()
                
                
                # Looms Table Creation ==========================================================================
                
                self.mycursor.execute('''
                    CREATE TABLE Looms (
                    Loom_No INT,
                    Product_Id INT NOT NULL,
                    CONSTRAINT c_ln_pk PRIMARY KEY (Loom_No),
                    CONSTRAINT c_pi_fk FOREIGN KEY (Product_Id) REFERENCES Product(Product_Id),
                    CONSTRAINT c_max_looms CHECK (Loom_No <= 16)
                    )
                ''')
                        
                self.mydb.commit()
                        
                self.mycursor.execute(
                    '''
                    INSERT INTO Looms (Loom_No, Product_Id)
                    SELECT Looms.Loom_No, Product.Product_Id
                    FROM (
                            SELECT 1 AS Loom_No UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
                            UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
                            UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 
                            UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16
                        ) AS Looms
                        JOIN (
                            SELECT Product_Id FROM Product WHERE Product_Id = 101
                        ) AS Product ON 1=1;
                    '''
                )
                        
                self.mydb.commit()
                
                
                # Workers Table Creation ==========================================================================
                
                self.mycursor.execute(
                    '''
                    CREATE TABLE Workers(
                        Worker_Id INT AUTO_INCREMENT,
                        Name VARCHAR(30) NOT NULL,
                        Surname VARCHAR(30) NOT NULL,
                        CONSTRAINT c_wi_pk PRIMARY KEY(Worker_Id)
                    )
                    '''
                )
                        
                self.mydb.commit()
                        
                self.mycursor.execute(
                    '''
                    ALTER TABLE Workers AUTO_INCREMENT = 201;
                    '''
                )
                        
                self.mydb.commit()   
                
                
                # Production Table Creation ==========================================================================
                
                self.mycursor.execute(
                    '''
                    CREATE TABLE Production(
                        Production_Id INT AUTO_INCREMENT PRIMARY KEY,
                        Date date NOT NULL,
                        Day VARCHAR(20) NOT NULL,
                        Loom_No INT NOT NULL,
                        Worker_Id INT NOT NULL,
                        Production INT NOT NULL,
                        CONSTRAINT c_ln_fk FOREIGN KEY(Loom_No) REFERENCES Looms(Loom_No),
                        CONSTRAINT c_wi_fk FOREIGN KEY(Worker_Id) REFERENCES Workers(Worker_Id),
                        CONSTRAINT ck_production_day CHECK (Day = DAYNAME(Date))
                    )
                    '''
                )
                        
                self.mydb.commit()
                
                
                # Salaries Table Creation ==========================================================================             
                
                self.mycursor.execute(
                    '''
                    CREATE TABLE Salaries (
                        Worker_Full_Name VARCHAR(70) NOT NULL,
                        Payment_Date DATE NOT NULL,
                        Work_Start_Date DATE NOT NULL,
                        Work_End_Date DATE NOT NULL,
                        Total_Salary FLOAT NOT NULL
                    )
                    '''
                )
                
                self.mydb.commit()
                
            except mysql.connector.Error:
                pass
                    
            execute_once = False
        
        # Define a function named switch_frames that takes a number as input to switch between multiple frames
        def switch_frames(number):
            
            
            
            
            
            
            
            
            
            # === 1. Salary Frame ===
# =====================================================================================================================            
            if number == 1:
                # Call the delete_frames function to clear existing frames
                delete_frames()
                # Create a new frame called salary_frame within the main_frame
                salary_frame = Frame(main_frame) 
                
                # === All varibales ====================
                worker_id_sal = StringVar()


                def generate_salary_data():
                    
                    from_date = my_date.entry.get()
                    selected_from_date = datetime.strptime(from_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                    
                    to_date = my_date_1.entry.get()
                    selected_to_date = datetime.strptime(to_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                    
                    #Get the selected worker ID, from the user input
                    selected_worker_id = worker_id_sal.get()

                    if worker_id_sal.get() == "-Select-":
                        messagebox.showerror("Oops!", "Please select the Worker ID.")

                    else:
                        try:
                            sql_salary= """SELECT P.Date, P.Day, P.Loom_No, CONCAT(W.Name, ' ', W.Surname) AS Worker_Name, 
                            P.Production, ROUND((P.Production * PR.Price), 2) AS Salary
                            FROM Production P
                            JOIN Workers W ON P.Worker_Id = W.Worker_Id
                            JOIN Looms L ON P.Loom_No = L.Loom_No
                            JOIN Product PR ON L.Product_Id = PR.Product_Id
                            WHERE P.Worker_Id = %s AND P.Date BETWEEN %s AND %s
                            ORDER BY P.Date ASC"""
                            
                            self.mycursor.execute(sql_salary, (selected_worker_id, selected_from_date, selected_to_date))
                            salary_data = self.mycursor.fetchall()

                            
                            # Clear previous entries from the Treeview
                            for record in home_table.get_children():
                                home_table.delete(record)
                                
                            # Now add the current data when clicked
                            for record in salary_data:
                                home_table.insert('', "end",values=record)
                                
                            self.mydb.commit()
                            
                            # Index 6 corresponds to the 'Salary' column
                            total_salary = sum(record[5] for record in salary_data)
                            
                            
                            if total_salary == 0:
                                messagebox.showerror("Oops!", "No production data found for the selected worker during the specified date range.")
                            else:
                                save_salary = messagebox.askyesno("Total Salary", f"Total Salary: {total_salary:.2f}\nDo you want to save the salary data?")
                                
                                if save_salary == True:
                                    
                                    try:
                                        
                                        self.mycursor.execute("SELECT CONCAT(Name, ' ', Surname) AS Full_Name FROM Workers WHERE Worker_Id = %s", (selected_worker_id,))
                                        full_name = self.mycursor.fetchone()[0]

                                        sql_save_salary = "INSERT INTO Salaries VALUES(%s, CURDATE(),%s,%s,%s)"
                                        self.mycursor.execute(sql_save_salary, (full_name, selected_from_date, selected_to_date, total_salary))
                                        self.mydb.commit()
                                        
                                        messagebox.showinfo("Salary Saved", f"Salary information for {full_name} saved successfully.")

                                    except mysql.connector.Error as er:
                                        messagebox.showerror("Oops!", str(er))
                                    
                            
                        except mysql.connector.Error as err:
                            messagebox.showerror("Oops!", str(err))

                        get_salary_data()
                            
                    
                home_title = Label(
                    salary_frame,
                    text="Salary",
                    font=('Garamond', 20)
                )
                home_title.place(x=50, y=120, width=1200)
                
                home_worker_label = Label(
                    salary_frame,
                    text='Worker ID',
                    font=('Garamond', 15)
                )
                home_worker_label.place(x=350, y=200)
                
                self.mycursor.execute("SELECT Worker_Id FROM workers") # Fetch the Worker_Id values from the workers table
                worker_ids1 = self.mycursor.fetchall() # Fetch all rows from the query result
                worker_id_list = ["-Select-"] + [worker[0] for worker in worker_ids1] # Extract Worker_Id values from the result
                
                worker_combobox1 = Combobox(
                    salary_frame,
                    values=worker_id_list,
                    font=('Garamond', 12),
                    state="readonly",
                    justify=CENTER,
                    textvariable=worker_id_sal
                )
                worker_combobox1.current(0)
                worker_combobox1.place(x=540, y=200, height=30, width=180)
                
                
                
                from_date_label = Label(
                    salary_frame,
                    text="From Date",
                    font=('Garamond', 15)
                )
                from_date_label.place(x=350, y=270)

                my_date = tb.DateEntry(
                    salary_frame,
                    bootstyle="danger",
                )
                my_date.place(x=540, y=270)
                

                to_date_label = Label(
                    salary_frame,
                    text="To Date",
                    font=('Garamond', 15)
                )
                to_date_label.place(x=350, y=340)
                
                my_date_1 = tb.DateEntry(
                    salary_frame,
                    bootstyle="danger"
                )
                my_date_1.place(x=540, y=340)

                
                def get_salary_data():
                    self.mycursor.execute("SELECT * FROM salaries")
                    salaries = self.mycursor.fetchall()
                

                    
                    for record in salary_table.get_children():
                        salary_table.delete(record)

                    for salary in salaries:
                        salary_table.insert('', END, values=salary)

                
                
                generate_salary = Button(
                    salary_frame,
                    text='Generate Salary',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=generate_salary_data  
                )
                # generate_salary.bind('<Button-1>', get_salary_data)
                generate_salary.place(x=540, y=410, height=50, width=200)

                
                worker_table_frame3 = LabelFrame(
                    salary_frame,
                    text=' Salaries ',
                    font=('Garamond', 17, 'bold'),
                    bd=2,
                    relief=RIDGE
                )
                worker_table_frame3.place(x=900, y=180, width=690, height=300)
                # x=900, y=180, width=690, height=300
                
                p_sb_y2 = Scrollbar(
                    worker_table_frame3,
                    orient=VERTICAL
                )
                p_sb_y2.pack(side=RIGHT, fill=Y)
                p_sb_x2 = Scrollbar(
                    worker_table_frame3,
                    orient=HORIZONTAL
                )
                p_sb_x2.pack(side=BOTTOM, fill=X)
                
                salary_table = ttk.Treeview(
                    worker_table_frame3,
                    columns=("wfn", "pd", "wsd", "wed", "ts"),
                    yscrollcommand=p_sb_y2.set,
                    xscrollcommand=p_sb_x2.set
                )
                
                p_sb_y2.config(command=salary_table.yview)
                p_sb_x2.config(command=salary_table.xview)
                
                salary_table.heading("wfn", text="Worker Full Name")
                salary_table.heading("pd", text="Payment Date")
                salary_table.heading("wsd", text="Work Start Date")
                salary_table.heading("wed", text="Work End Date")
                salary_table.heading("ts", text="Total Salary")
                salary_table["show"] = "headings"
                
                salary_table.pack(fill=BOTH, expand=1)
                
                
                home_table_frame = LabelFrame(
                    salary_frame,
                    text=' Take a closer look at the table below for detailed Salary information ',
                    font=('Garamond', 17, 'bold'),
                    bd=2,
                    relief=RIDGE
                )
                home_table_frame.place(x=0, y=530, relwidth=1, height=300)
                
                p_sb_y9 = Scrollbar(
                    home_table_frame,
                    orient=VERTICAL
                )
                p_sb_y9.pack(side=RIGHT, fill=Y)
                p_sb_x9 = Scrollbar(
                    home_table_frame,
                    orient=HORIZONTAL
                )
                p_sb_x9.pack(side=BOTTOM, fill=X)
                
                home_table = ttk.Treeview(
                    home_table_frame,
                    columns=("Date", "Day", "Loom_No", "Worker_Name", "Production", "Salary"),
                    yscrollcommand=p_sb_y9.set,
                    xscrollcommand=p_sb_x9.set
                )
                
                p_sb_y9.config(command=home_table.yview)
                p_sb_x9.config(command=home_table.xview)
                
                home_table.heading("Date", text="Date")
                home_table.heading("Day", text="Day")
                home_table.heading("Loom_No", text="Loom No")
                home_table.heading("Worker_Name", text="Worker Name")
                home_table.heading("Production", text="Production")
                home_table.heading("Salary", text="Salary")
                home_table["show"] = "headings"
                
                home_table.pack(fill=BOTH, expand=1)
                
                
                get_salary_data()

                salary_frame.pack(fill='both', expand=True)  # Pack the salary_frame into the main_frame
            
            
            
            
            
            
            
            
            
            
            
                
            # === 2. Product Frame ===
# =====================================================================================================================
            elif number == 2:
                delete_frames()
                product_frame = Frame(main_frame)
                
                # === All variables used for coding Product ======================
                product_id_cb = StringVar()
                product_name_cb = StringVar()
                product_size_cb = StringVar()
                product_price_var = StringVar()
                product_name_var = StringVar()
                product_size_var = StringVar()
                    
                    
                def gather_product_data():
                    p_id_val = product_id_cb.get()
                    p_nm_val = product_name_cb.get()
                    p_si_val = product_size_cb.get()
                    p_pr_val = product_price_var.get()
                    
                    return p_id_val, p_nm_val, p_si_val, p_pr_val
                
                # Function to save the product data
                def save_product():
                    product_price_str = product_price_var.get().strip()
                    
                    if product_price_str == "":
                        messagebox.showerror("Oops!", "Please fill in all the required fields.")
                       
                    elif not product_name_var.get().replace(' ', '').isalpha() and not ' ' in product_name_var.get():
                        messagebox.showerror("Oops!", "Product name should not contain numbers.")

                    elif not product_size_var.get().isdigit():
                        messagebox.showerror("Oops!", "Product size should only contain numbers.")
                        
                    # elif product_size_str not in ("4070", "3060", "3056", "2754", "2030", "1421", "1218", "1212"):
                    #     messagebox.showerror("Oops!", "Product size should be one of: 4070, 3060, 3056, 2754, 2030, 1421, 1218, 1212.")
                        
                    elif not product_price_var.get().replace('.', '', 1).isdigit():
                        messagebox.showerror("Oops!", "Product Price accepts only numeric values.")
                         
                    else:
                        try:
                            # Convert price to float
                            product_price_float = float(product_price_str)
                            
                            name_of_product = product_name_var.get().strip()
                            size_of_product = product_size_var.get().strip()
                            
                            # Insert the new product into the database
                            sql_insert_product = "INSERT INTO Product (Name, Size, Price) VALUES (%s, %s, %s)"
                            product_data = (name_of_product, size_of_product, product_price_float)
                            self.mycursor.execute(sql_insert_product, product_data)
                            self.mydb.commit()

                            messagebox.showinfo("Success", "Product data saved successfully.")
                            product_name_var.set("")
                            product_size_var.set("")
                            product_price_var.set("")
                        except mysql.connector.Error as err:
                            messagebox.showerror("Oops!", str(err))
                           
                    show_product_data()

                
                # Function to retrive and display  data from the 'product' table in a TreeView widget
                def show_product_data():
                    
                    try:
                        # Execute the SQL Query to retrieve all rows from the 'product' table
                        self.mycursor.execute("SELECT * FROM product ORDER BY Product_Id")
                        
                        # Fetch all rows returned by the SQL query
                        rows1 = self.mycursor.fetchall()
                        
                        # Clear all the existing items in the TreeView to prevent duplication
                        product_table.delete(*product_table.get_children())
                        
                        # Iterate through each row fetched from the database
                        for row1 in rows1:
                            
                            # Insert a new item (row) into the TreeView with values from the current row
                            product_table.insert('', END, values=row1)
                    
                    # Error Handling
                    except Exception as ex:
                        
                        # If any error occurs during the execution of the query, this'll display an error message box
                        messagebox.showerror("Error", str(ex))
                        
                # Fuction for updating the data of the products
                def update_products():
                    product_id_str = product_id_cb.get().strip()

                    if product_id_str == "" or product_name_cb.get() == "" or product_size_cb.get() == "" or product_price_var.get() == "":
                        messagebox.showerror("Oops!", "You missed a spot. Please fill in the required textbox(s).")

                    elif product_id_str == "-Select-":
                        messagebox.showerror("Oops!", "Please select the Product ID.")

                    elif product_name_cb.get() == "-Select-":
                        messagebox.showerror("Oops!", "Please select the Product Name.")

                    elif product_size_cb.get() == "-Select-":
                        messagebox.showerror("Oops!", "Please select the Product Size.")
                                            
                    elif not product_price_var.get().replace('.', '', 1).isdigit():
                        messagebox.showerror("Oops!", "Product Price accepts only numeric values.")

                    else:
                        try:        
                            sql_check_product = "SELECT * FROM product WHERE Product_Id = %s"
                            self.mycursor.execute(sql_check_product, (product_id_str,))
                            existing_product = self.mycursor.fetchone()

                            if existing_product is None:
                                messagebox.showerror("Oops!", f"Product with ID {product_id_str} does not exist.")
                                
                            else:
                                p_id_val, p_nm_val, p_si_val, p_pr_val = gather_product_data()
                                sql_update = "UPDATE product SET Name = %s, Size = %s, Price = %s WHERE Product_Id = %s"
                                values = (p_nm_val, p_si_val, p_pr_val, p_id_val)
                                self.mycursor.execute(sql_update, values)
                                self.mydb.commit()

                                messagebox.showinfo("Success", "Product data updated successfully.")

                                product_id_cb.set("-Select-")
                                product_name_cb.set("-Select-")
                                product_size_cb.set("-Select-")
                                product_price_var.set("")

                        except mysql.connector.Error as err:
                            messagebox.showerror("Oops!", str(err))

                    clear_fields()
                    show_product_data()
                    


                # Function for enabling the combobox
                def enable_cb_product():
                    
                    save_button_p.config(state=DISABLED)
                    update_button_p.config(state=NORMAL)
                    
                    product_id_cb.set("-Select-")
                    
                    self.mycursor.execute("SELECT Product_Id FROM Product")
                    product_ids = self.mycursor.fetchall()
                    
                    product_id_list = ["-Select-"] + [id[0] for id in product_ids]
                    id_combobox_1.config(state=READONLY, values=product_id_list)
                    
                    product_name_entry.place_forget()
                    product_size_entry.place_forget()
                    
                    product_name_cb.set("-Select-")
                    
                    self.mycursor.execute("SELECT DISTINCT Name FROM Product")
                    product_names = self.mycursor.fetchall()
                    
                    product_name_list = ["-Select-"] + [name[0] for name in product_names]
                    name_combobox_1.config(values=product_name_list)
                    
                    name_combobox_1.place(x=540, y=270, height=30, width=180)
                    
                    product_size_cb.set("-Select-")
                    
                    self.mycursor.execute("SELECT DISTINCT Size FROM Product")
                    product_sizes = self.mycursor.fetchall()
                    
                    product_size_list = ["-Select-"] + [size[0] for size in product_sizes]
                    size_combobox_1.config(values=product_size_list)
                    
                    size_combobox_1.place(x=540, y=340, height=30, width=180)
                    
                    
                    
                    
                # Function for clear button
                def clear_fields():
                    product_id_cb.set("-Select-")
                    product_price_var.set("")
                    id_combobox_1.config(state=DISABLED)
                    save_button_p.config(state=NORMAL)
                    update_button_p.config(state=DISABLED)
                    
                    name_combobox_1.place_forget()
                    size_combobox_1.place_forget()
                    
                    product_name_entry.place(x=540, y=270, height=30, width=180)
                    product_size_entry.place(x=540, y=340, height=30, width=180)
                    
                    show_product_data()
                    
                
                def fill_product_details(eve):
                    try:
                        selected_id = product_id_cb.get()
                        self.mycursor.execute("SELECT * FROM Product WHERE Product_Id = %s", (selected_id,))
                        set_product = self.mycursor.fetchone()
                        
                        self.mydb.commit()
                        
                        if set_product:
                            selected_product_name = set_product[1]
                            selected_product_size = set_product[2]
                            selected_product_price = set_product[3]
                            
                            
                            name_combobox_1.set(selected_product_name)
                            size_combobox_1.set(selected_product_size)
                            product_price_var.set(selected_product_price)
                            
                        else:
                            # If no product is found with the given ID, clear the values in the widgets
                            product_name_cb.set("")
                            product_size_cb.set("")
                            product_price_var.set("")
                        
                    except mysql.connector.Error as er:
                        messagebox.showerror("Oops!", str(er))
                        
                        
                        
                # === Title Label ===
                product_title = Label(
                    product_frame,
                    text="Product Details",
                    font=('Garamond', 20)
                )
                product_title.place(x=50, y=120, width=1200)
                
                # === Label & Entry for Product ID ===
                id_label_1 = Label(
                    product_frame,
                    text='Product ID',
                    font=('Garamond', 15)
                )
                id_label_1.place(x=350, y=200)
                id_combobox_1 = Combobox(
                    product_frame,
                    font=('Garamond', 12),
                    state=DISABLED,
                    justify=CENTER,
                    textvariable=product_id_cb
                )
                id_combobox_1.bind("<<ComboboxSelected>>", fill_product_details)
                id_combobox_1.place(x=540, y=200, width=180)
                
                # === Label & Entry for Product Name ===
                name_label_1 = Label(
                    product_frame,
                    text='Product Name',
                    font=('Garamond', 15)
                )
                name_label_1.place(x=350, y=270)
                
                product_name_entry = Entry(
                    product_frame,
                    font=('Garamond', 12),
                    justify=CENTER,
                    textvariable=product_name_var
                )
                product_name_entry.place(x=540, y=270, height=30, width=180)
                
                name_combobox_1 = Combobox(
                    product_frame,
                    font=('Garamond', 12),
                    state=READONLY,
                    justify=CENTER,
                    textvariable=product_name_cb
                )
                
                
                # === Label & Combobox for Product Size ===
                size_label_1 = Label(
                    product_frame,
                    text='Prodcut Size',
                    font=('Garamond', 15)
                )
                size_label_1.place(x=350, y=340)
                
                product_size_entry = Entry(
                    product_frame,
                    font=('Garamond', 12),
                    justify=CENTER,
                    textvariable=product_size_var
                )
                product_size_entry.place(x=540, y=340, height=30, width=180)
                
                
                size_combobox_1 = Combobox(
                    product_frame,
                    state=READONLY,
                    justify=CENTER,
                    font=('Garamond', 12),
                    textvariable=product_size_cb
                )
                
                # === Label & Entry for Product Price ===
                price_label_1 = Label(
                    product_frame,
                    text='Prodcut Price',
                    font=('Garamond', 15)
                )
                price_label_1.place(x=350, y=410)
                price_entry_1 = Entry(
                    product_frame,
                    font=('Garamond', 12),
                    justify=CENTER,
                    textvariable=product_price_var
                )
                price_entry_1.place(x=540, y=410, height=30, width=180)
                
                # === Button for Save ===
                save_button_p = Button(
                    product_frame,
                    text='Add',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command= save_product
                )
                save_button_p.place(x=540, y=480, height=30, width=100)
                
                # === Edit Button ===
                edit_button_p = Button( product_frame,
                    text='Edit',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=enable_cb_product
                )
                edit_button_p.place(x=750, y=200, height=30, width=100)
                
                # === Update Button ===
                update_button_p = Button(
                    product_frame,
                    text='Update',
                    font=('Garamond', 15),
                    cursor="hand2",
                    state=DISABLED,
                    command= update_products
                )
                update_button_p.place(x=750, y=270, height=30, width=100)

                # === Button for Clear ===
                clear_button1 = Button(
                    product_frame,
                    text='Cancel',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=clear_fields
                )
                clear_button1.place(x=750, y=340, height=30, width=100)
                        
                # === Product Details ===
                table_frame_p = LabelFrame(
                    product_frame,
                    text=' Take a closer look at the table below for detailed product information. ',
                    font=('Garamond', 17, 'bold'),
                    bd=2,
                    relief=RIDGE
                )
                table_frame_p.place(x=0,y=530, relwidth=1, height=300)
                
                # === Scroll Bar for Table frame ===
                scrollbar_y = Scrollbar(
                    table_frame_p,
                    orient=VERTICAL
                )
                scrollbar_x = Scrollbar(
                    table_frame_p,
                    orient=HORIZONTAL
                )
                product_table = ttk.Treeview(
                    table_frame_p,
                    columns=("Product_Id", "name", "size", "price"),
                    yscrollcommand=scrollbar_y.set,
                    xscrollcommand=scrollbar_x.set
                )
                scrollbar_y.pack(side=RIGHT, fill=Y)
                scrollbar_y.config(command=product_table.yview)
                
                scrollbar_x.pack(side=BOTTOM, fill=X)
                scrollbar_y.config(command=product_table.xview)
                
                product_table.heading("Product_Id", text="Product ID")
                product_table.heading("name", text="Name")
                
                product_table.heading("size", text="Size")
                product_table.heading("price", text="Price")
                product_table["show"]= "headings"
                
                product_table.pack(fill=BOTH, expand=1)
                
                # Call function to display initial product data
                show_product_data()
                
                
                product_frame.pack(fill='both', expand=True) # Ensure product_frame expands to fill main_frame
            
            
            
            
            
            
            
            
            
            
            
            # === 3. Looms Frame ===    
# =====================================================================================================================
            elif number == 3:
                delete_frames()
                looms_frame = Frame(main_frame)
                
                # === All variables ==============
                loom_no_cb = StringVar()
                product_size = StringVar()
                
                
                def gather_looms_data():
                    loom_no_cb_val = loom_no_cb.get()
                    product_size_val = product_size.get()
                    return loom_no_cb_val, product_size_val



                def show_looms_data():
                    try:
                        self.mycursor.execute("SELECT Looms.Loom_No, Product.Size, Product.Name FROM Looms JOIN Product ON Looms.Product_Id = Product.Product_Id ORDER BY Loom_No")
                        rows = self.mycursor.fetchall()
                        
                        loom_table.delete(*loom_table.get_children())
                        for row in rows:
                            loom_table.insert('', END, values=row)
                            
                    except mysql.connector.Error as err:
                        messagebox.showerror("Oops!", str(err))
                 
                 
                        
                def update_looms_data():
                    
                    if loom_no_cb.get() == "-Select-":
                        messagebox.showerror("Oops!", "Please select the Loom No.")
                        
                    elif product_size.get() == "-Select-":
                        messagebox.showerror("Oops!", "Please select the Product Size.")
                        
                    else:
                        try:
                            loom_no_cb_val, product_size_val = gather_looms_data()
                            
                            # Check if the product size exists in the Product table
                            sql_check = "SELECT Product_Id FROM Product WHERE Size = %s"
                            self.mycursor.execute(sql_check, (product_size_val,))
                            product_id_row = self.mycursor.fetchone()
                            
                            if product_id_row:
                                product_id_val = product_id_row[0]
                                
                                # Update the Looms table with the retrieved Product_Id
                                sql_update_looms = "UPDATE Looms SET Product_Id = %s WHERE Loom_No = %s"
                                self.mycursor.execute(sql_update_looms, (product_id_val, loom_no_cb_val))
                                self.mydb.commit()
                                
                                messagebox.showinfo("Success", "Loom data updated successfully.")
                                loom_no_cb.set("-Select-")
                                product_size.set("-Select-")
                                
                            else:
                                messagebox.showerror("Oops", "Product size is not present, try adding it first.")
                                                        
                        except mysql.connector.Error as err:
                            messagebox.showerror("Oops!", str(err))
                          
                    show_looms_data()
                    
                    
                    
                
                def clear_all():
                    loom_no_cb.set("-Select-")
                    product_size.set("-Select-")
                    
                    
                
                def get_looms_data(event):
                    try:
                        r = loom_table.focus()
                        content = (loom_table.item(r))
                        
                        
                        row = content['values']
                        loom_no_cb.set(str(row[0]).strip())
                        product_size.set(str(row[1]).strip())
                    except IndexError:
                        pass
                    

                
                # === Title label ===
                looms_title = Label(
                    looms_frame,
                    text="Looms Detail",
                    font=('Garamond', 20)
                )
                looms_title.place(x=50, y=120, width=1200)
                
                # === Label and combobox for Loom No ===
                loom_no_label = Label(
                    looms_frame,
                    text='Loom No',
                    font=('Garamond', 15)
                )
                loom_no_label.place(x=350, y=200)
                
                value_list1 = ["-Select-"] + list(range(1, 17))
                loom_no_combobox = Combobox(
                    looms_frame,
                    values=tuple(value_list1),
                    state=READONLY,
                    justify=CENTER,
                    font=('Garamond', 12),
                    textvariable=loom_no_cb
                )
                loom_no_combobox.current(0)
                loom_no_combobox.place(x=540, y=200, height=30, width=180)
                
                product_id_label = Label(
                    looms_frame,
                    text='Product Size',
                    font=('Garamond', 15)
                )
                product_id_label.place(x=350, y=270)
                
                self.mycursor.execute("SELECT DISTINCT Size FROM Product")
                up_size = self.mycursor.fetchall()
                # print(up_size)
                
                up_size_list = ["-Select-"] + [size11[0] for size11 in up_size]
                
                product_id_combobox = Combobox(
                    looms_frame,
                    values=up_size_list,
                    font=('Garamond', 12),
                    state=READONLY,
                    justify=CENTER,
                    textvariable=product_size
                )
                product_id_combobox.current(0)
                product_id_combobox.place(x=540, y=270, height=30, width=180)
                
                loom_update = Button(
                    looms_frame,
                    text='Update',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=update_looms_data
                )
                loom_update.place(x=540, y=340, height=30, width=100)

                clear_entry = Button(
                    looms_frame,
                    text='Cancel',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=clear_all
                )
                clear_entry.place(x=750, y=200, height=30, width=100)
                
                loom_table_frame = LabelFrame(
                    looms_frame,
                    text=' Take a closer look at the table below for detailed Looms information ',
                    font=('Garamond', 17, "bold"),
                    bd=2,
                    relief=RIDGE
                )
                loom_table_frame.place(x=0, y=530, relwidth=1, height=300)
                
                loom_sb_y = Scrollbar(
                    loom_table_frame,
                    orient=VERTICAL
                )
                loom_sb_x = Scrollbar(
                    loom_table_frame,
                    orient=HORIZONTAL
                )
                
                loom_table = ttk.Treeview(
                    loom_table_frame,
                    columns=("Loom_No", "Size", "Name"),
                    yscrollcommand=loom_sb_y.set,
                    xscrollcommand=loom_sb_x.set
                )
                
                loom_sb_y.pack(side=RIGHT, fill=Y)
                loom_sb_y.config(command=loom_table.yview)
                
                loom_sb_x.pack(side=BOTTOM, fill=X)
                loom_sb_x.config(command=loom_table.xview)
                
                loom_table.heading("Loom_No", text="Loom No")
                loom_table.heading("Size", text="Size")
                loom_table.heading("Name", text="Name")
                loom_table["show"] = "headings"
                
                loom_table.pack(fill=BOTH, expand=1)
                loom_table.bind("<ButtonRelease-1>", get_looms_data)
                
                show_looms_data()
                
                looms_frame.pack(fill='both', expand=True) # Ensure looms_frame expands to fill main_frame
            
            
            
            
            
            
            
            
            
            
            
            # === 4. Workers Frame ===  
# =====================================================================================================================  
            elif number == 4:
                delete_frames()
                workers_frame = Frame(main_frame)
                
                # === All variables used for coding Workers ======================
                search_by = StringVar()
                search_text = StringVar()
                worker_id = StringVar()
                worker_name = StringVar()
                worker_surname = StringVar()
                
                        
                def gather_worker_data():
                    # Get the values entered by the manager/admin
                    name_value = worker_name.get()
                    surname_value = worker_surname.get()
                    return name_value, surname_value
                
                # Function to Save worker data
                def save_worker_data():
                    
                    # Check if the worker name or surname is empty
                    if worker_name.get() == "" or worker_surname.get() == "":
                        # If either of them is empty display error message prompting the user to fill the required textbox(Entry)
                        messagebox.showerror("Oops!", "You missed a spot. Please fill in the required textbox.")
                    
                    # Check if the worker name or surname contains digits
                    elif not worker_name.get().isalpha() or not worker_surname.get().isalpha():
                        # If yes then display an error message
                        messagebox.showerror("Oops!", "Name and Surname should include alphabets only.")
                    
                    else:
                        try:
                            # Call the gather_worker_data function to retrieve the values
                            name_value, surname_value = gather_worker_data()

                            # Execute SQL Insert Statement
                            sql_insert = "INSERT INTO workers(Name, Surname) VALUES (%s, %s)"
                            values = (name_value, surname_value)
                            self.mycursor.execute(sql_insert, values)

                            # Commit the transaction
                            self.mydb.commit()

                            # Display a success message
                            messagebox.showinfo("Success", "Worker data saved successfully")

                            # Clear input fields
                            worker_name.set("")
                            worker_surname.set("")

                        except mysql.connector.Error as err:
                            # Display an error message if the operation fails
                            messagebox.showerror("Oops!", str(err))
                    
                    # Refresh the worker data display
                    show_worker_data()

                            
                        
                # Function to Update worker data
                def update_worker_data():
                    worker_id_str = worker_id.get().strip()
                    
                    if worker_id.get() == "-Select-":
                        messagebox.showerror("Oops!", "Please select the Worker ID.")
                        
                    elif worker_name.get() == "" or worker_surname.get() == "":
                        messagebox.showerror("Oops!", "You missed a spot. Please fill in the required textbox.")

                    elif not worker_name.get().isalpha() or not worker_surname.get().isalpha():
                        messagebox.showerror("Oops!", "Name and Surname should include alphabets only.")
                        
                    else:
                        try:
                            
                            # Call the get_input function to retrive the values
                            name_value, surname_value = gather_worker_data()
                                
                            # Execute SQL Update Statement
                            sql_update = "UPDATE workers SET Name = %s, Surname = %s WHERE Worker_Id = %s"
                            values = (name_value, surname_value, worker_id_str)
                            self.mycursor.execute(sql_update, values)
                            
                            # Commit the transaction
                            self.mydb.commit()
                                
                            # Display a success message
                            messagebox.showinfo("Success", "Worker data updated successfully")
                            
                        except mysql.connector.Error as err:
                            messagebox.showerror("Oops!", str(err))
                    
                    clear_entry_fields()        
                    show_worker_data()
                    worker_id_combobox.config(state=DISABLED)
                    save_button.config(state=NORMAL)
                
                
                
                
                # Function to Delete worker data
                def delete_worker_data():
                    if worker_id.get() == "-Select-":
                        messagebox.showerror("Oops!", "Please enter Worker ID before proceeding.")

                    else:
                        try:
                            
                            accept = messagebox.askyesno("Confirm", "Do you really want to delete.")
                            if accept == True:
                            
                                id_value = worker_id.get()
                                    
                                sql_delete = "DELETE FROM workers WHERE Worker_Id = %s"
                                self.mycursor.execute(sql_delete, (id_value, ))
                                    
                                self.mydb.commit()
                                    
                                messagebox.showinfo("Deleted", "Worker data deleted successfully")
                            
                        except mysql.connector.Error as err:
                            messagebox.showerror("Oops!", str(err))
                            
                    clear_entry_fields()
                    show_worker_data()
                    worker_id_combobox.config(state=DISABLED)
                    save_button.config(state=NORMAL)
                                                    
                            
                # Function to clear the data in entry fields
                def clear_entry_fields():
                    worker_id.set("-Select-")           # Clear the worker ID entry field
                    worker_name.set("")         # Clear the worker Name entry field
                    worker_surname.set("")      # Clear the worker Surname entry field
                    search_by.set("-Select-")   # Set the combobox field to default
                    search_text.set("")         # Clear the search entry field
                    worker_id_combobox.config(state=DISABLED)
                    save_button.config(state=NORMAL)
                    update_button.config(state=DISABLED)
                    delete_button.config(state=DISABLED)
                    show_worker_data()
                    
                # Function to retrive and display  data from the 'workers' table in a TreeView widget
                def show_worker_data():
                    
                    try:
                        # Execute the SQL Query to retrieve all rows from the 'workers' table
                        self.mycursor.execute("SELECT * FROM workers ORDER BY Worker_Id")
                        
                        # Fetch all rows returned by the SQL query
                        rows = self.mycursor.fetchall()
                        
                        # Clear all the existing items in the TreeView to prevent duplication
                        worker_table.delete(*worker_table.get_children())
                        
                        # Iterate through each row fetched from the database
                        for row in rows:
                            
                            # Insert a new item (row) into the TreeView with values from the current row
                            worker_table.insert('', END, values=row)
                    
                    # Error Handling
                    except Exception as ex:
                        
                        # If any error occurs during the execution of the query, this'll display an error message box
                        messagebox.showerror("Error", str(ex))
                        
                # Define a function named get_data that takes an argument ev.
                # ev. because we've used bind() for TreeView
                def get_data(ev):
                    # Get the focus (selected item) of the worker_table widget.
                    r = worker_table.focus()
                    
                    # Retrieve the content of the selected row/item from the worker_table.
                    content = (worker_table.item(r))
                    
                    # Extract the values of the selected row and store them in the 'row' variable.
                    row = content['values']
                    
                    # Set tkinter variables (worker_id, worker_name, worker_surname) with data from the selected row.
                    worker_id.set(row[0])
                    worker_name.set(row[1])
                    worker_surname.set(row[2])
                    
                # Function for searching the Workers
                def search_worker():
                    try:
                        if search_by.get()== "":
                            messagebox.showerror("Oops!", "Please choose an option from the Combobox")
                           
                        # If combobox has '-Select-' option then show error message 
                        elif search_by.get() == "-Select-":
                            messagebox.showerror("Oops!", "Try another option")
                            
                        else:
                            # Check if the search text entry field is empty.
                            if search_text.get() == "":
                                # If it is empty, display an error message
                                messagebox.showerror("Oops!", "Please type something to search for.")
                            
                            else:
                                # Execute the SQL Query to retrieve all rows from the 'workers' table
                                self.mycursor.execute("SELECT * FROM workers WHERE " + search_by.get() + " LIKE '%" + search_text.get() + "%'")
                            
                                # Fetch all rows returned by the SQL query
                                rows = self.mycursor.fetchall()
                                
                                if len(rows) != 0:
                                    # Clear all the existing items in the TreeView to prevent duplication
                                    worker_table.delete(*worker_table.get_children())
                                
                                    # Iterate through each row fetched from the database
                                    for row in rows:
                                        
                                        # Insert a new item (row) into the TreeView with values from the current row
                                        worker_table.insert('', END, values=row)
                                      
                                    search_text.set("")
                                
                                # If no records matching the search criteria are found in the database        
                                else:
                                    # display an error message
                                    messagebox.showerror("Oops!", "No such record or data")
                                
                    # Error Handling
                    except Exception as ex:
                        
                        # If any error occurs during the execution of the query, this'll display an error message box
                        messagebox.showerror("Error", str(ex))
                
                
                        
                # Function for enabling the Worker ID Combobox
                def enable_worker_id():
                    # Fetch all worker ids from the Workers Table
                    self.mycursor.execute("SELECT Worker_Id FROM Workers")
                    up_w_ids = self.mycursor.fetchall()
                    up_w_id_list = ["-Select-"] + [up_w[0] for up_w in up_w_ids]
                    worker_id_combobox.config(state=READONLY, values=up_w_id_list)
                    save_button.config(state=DISABLED)
                    worker_id.set("-Select-")
                    update_button.config(state=NORMAL)
                    delete_button.config(state=NORMAL)
                    
                    
                    
                def fill_worker_details(event11):
                    try:
                        selected_worker_id = worker_id.get()
                        
                        self.mycursor.execute("SELECT * FROM Workers WHERE Worker_Id = %s", (selected_worker_id,))
                        set_workers = self.mycursor.fetchone()
                        
                        self.mydb.commit()
                        
                        # print(set_workers)
                        if set_workers:
                            selected_worker_name = set_workers[1]
                            selected_worker_surname = set_workers[2]
                            
                            # print(selected_worker_name, selected_worker_surname)
                            
                            worker_name.set(selected_worker_name)
                            worker_surname.set(selected_worker_surname)
                        else:
                            worker_name.set("")
                            worker_surname.set("")
                        
                    except mysql.connector.Error as err:
                        messagebox.showerror("Oops!", str(err))
                    
                    
                # --- Search frame ---
                search_frame = tk.LabelFrame(
                    workers_frame,
                    text=" Search Worker ",
                    font=('Garamond', 17, 'bold'),
                    bd=2,
                    relief=RIDGE
                )
                search_frame.place(x=350, y=10, width=700, height=100)  # Place the search_frame
                
                # === Label for Combobox ===
                label_for_combobox = Label(
                    search_frame,
                    text='Search By',
                    font=('Garamond', 12)
                )
                label_for_combobox.place(x=10, y=10)
                
                # === ComboBox for searching the worker inside the Search Frame ===
                search_combobox = ttk.Combobox(
                    search_frame,
                    values =('-Select-','Name', 'Surname'),
                    textvariable=search_by,
                    state="readonly",
                    justify=CENTER,
                    font=('Garamond', 12)
                )
                search_combobox.current(0)
                search_combobox.place(x=100, y=10, width=180)  # Place the combobox within search_frame
                
                # === Entry Widget for Searching Worker ===
                search_entry = Entry(
                    search_frame,
                    font=('Garamond', 12),
                    justify=CENTER,
                    textvariable=search_text
                )
                search_entry.place(x=290, y=10, height=30, width=180)
                
                # === Button for Searching ===
                search_button = Button(
                    search_frame,
                    text='Search',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=search_worker
                )
                search_button.place(x=480, y=10, height=30, width=100)
                
                # === Title Label ===
                worker_title = Label(
                    workers_frame,
                    text="Workers Details",
                    font=('Garamond', 20)
                )
                worker_title.place(x=50, y=120, width=1200)
                
                
                
                # === Label & Entry for Worker ID ===
                id_label = Label(
                    workers_frame,
                    text='Worker ID',
                    font=('Garamond', 15)
                )
                id_label.place(x=350, y=200)
                worker_id_combobox = Combobox(
                    workers_frame,
                    state=DISABLED,
                    justify=CENTER,
                    font=('Garamond', 12),
                    textvariable=worker_id
                )
                # worker_id_combobox.current(0)
                worker_id_combobox.place(x=540, y=200, height=30, width=180)
                worker_id_combobox.bind("<<ComboboxSelected>>", fill_worker_details)
                
                # === Label & Entry for Worker Name ===
                name_label = Label(
                    workers_frame,
                    text='Worker Name',
                    font=('Garamond', 15)
                )
                name_label.place(x=350, y=270)
                name_entry = Entry(
                    workers_frame,
                    font=('Garamond', 12),
                    justify=CENTER,
                    textvariable=worker_name
                )
                name_entry.place(x=540, y=270, height=30, width=180)
                
                # === Label & Entry for Worker Surname ===
                surname_label = Label(
                    workers_frame,
                    text='Worker Surname',
                    font=('Garamond', 15)
                )
                surname_label.place(x=350, y=340)
                surname_entry = Entry(
                    workers_frame,
                    font=('Garamond', 12),
                    justify=CENTER,
                    textvariable=worker_surname
                )
                surname_entry.place(x=540, y=340, height=30, width=180)
                
                # === Button for Save ===
                save_button = Button(
                    workers_frame,
                    text='Save',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=save_worker_data
                )
                save_button.place(x=540, y=410, height=30, width=100)
                
                # === Button for Edit ===
                edit_button_w = Button(
                    workers_frame,
                    text='Edit',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=enable_worker_id
                )
                edit_button_w.place(x=750, y=200, height=30, width=100)
                # === Button for Update ===
                update_button = Button(
                    workers_frame,
                    text='Update',
                    font=('Garamond', 15),
                    cursor="hand2",
                    state=DISABLED,
                    command=update_worker_data
                )
                update_button.place(x=750, y=270, height=30, width=100)
                
                # === Button for Delete ===
                delete_button = Button(
                    workers_frame,
                    text='Delete',
                    font=('Garamond', 15),
                    cursor="hand2",
                    state=DISABLED,
                    command=delete_worker_data
                )
                delete_button.place(x=750, y=340, height=30, width=100)
                
                # === Button for Clear ===
                clear_button = Button(
                    workers_frame,
                    text='Cancel',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=clear_entry_fields
                )
                clear_button.place(x=750, y=410, height=30, width=100)
                
                # === Worker Details ===
                table_frame = LabelFrame(
                    workers_frame,
                    text=' Take a closer look at the table below for detailed workers information. ',
                    font=('Garamond', 17, 'bold'),
                    bd=2,
                    relief=RIDGE
                )
                table_frame.place(x=0,y=530, relwidth=1, height=300)
                
                # === Scroll Bar for Table frame ===
                scroll_bar_y = Scrollbar(
                    table_frame,
                    orient=VERTICAL
                )
                scroll_bar_x = Scrollbar(
                    table_frame,
                    orient=HORIZONTAL
                )
                
                worker_table = ttk.Treeview(
                    table_frame,
                    columns=("Worker_Id", "Name", "Surname"),
                    yscrollcommand=scroll_bar_y.set,
                    xscrollcommand=scroll_bar_x.set
                )
                # ScrollBar packing
                scroll_bar_y.pack(side=RIGHT, fill=Y)
                scroll_bar_y.config(command=worker_table.yview)
                scroll_bar_x.pack(side=BOTTOM, fill=X)
                scroll_bar_x.config(command=worker_table.xview)
                
                worker_table.heading("Worker_Id", text="Worker ID")
                worker_table.heading("Name", text="Name")
                worker_table.heading("Surname", text="Surname")
                worker_table["show"]= "headings"
                
                worker_table.pack(fill=BOTH, expand=1)
                worker_table.bind("<ButtonRelease-1>", get_data)
                
                # Call the show_worker_data function to show the data in Treeview
                show_worker_data()

                workers_frame.pack(fill='both', expand=True) # Ensure workers_frame expands to fill main_frame

            
            
            
            
            
            
            
            
            
            
                
            # === 5. Prdouction Frame ===
# =====================================================================================================================
            elif number == 5:
                delete_frames()
                production_frame = Frame(main_frame)
                
                # === All variables ==============
                loom_no = StringVar()
                worker_id_cb =  StringVar()
                production = StringVar()
                p_id_cb = StringVar()
                
                
                def gather_production_data():
                    loom_no_var = loom_no.get()
                    worker_id_var = worker_id_cb.get()
                    production_var = production.get()
                    return loom_no_var, worker_id_var, production_var
                
                
                
                
                def save_production_data():
                    if production.get() == "":
                        messagebox.showerror("Oops", "You missed a spot. Please fill in the required textbox.")
                    elif loom_no.get() == "-Select-":
                        messagebox.showerror("Oops!", "Try another option for Loom No.")
                    elif worker_id_cb.get() == "-Select-":
                        messagebox.showerror("Oops!", "Try another option Worker ID.")
                    elif not production.get().isdigit():
                        messagebox.showerror("Oops!", "Production must be a numeric value.")
                    else:
                        loom_no_var, worker_id_var, production_var = gather_production_data()
                        
                        try:
                            # Check if a record with the same loom number exists for the same day
                            sql_check_existing = "SELECT * FROM Production WHERE Loom_No = %s AND DATE(Date) = CURDATE()"
                            self.mycursor.execute(sql_check_existing, (loom_no_var,))
                            existing_record = self.mycursor.fetchone()
                            
                            if existing_record:
                                messagebox.showerror("Oops!", "Production data for this loom number already exists for today.")
                            else:
                                # Define the SQL query to insert new data
                                sql_insert = "INSERT INTO Production (Date, Day, Loom_No, Worker_Id, Production) VALUES (CURDATE(), DAYNAME(NOW()), %s, %s, %s)"
                                
                                # Execute the query
                                self.mycursor.execute(sql_insert, (loom_no_var, worker_id_var, production_var))
                                self.mydb.commit()
                                
                                today_day = datetime.now().strftime('%A')
                                messagebox.showinfo("Success", f"{today_day}'s Production has been saved successfully.")
                                
                                # Reset the input fields
                                loom_no.set("-Select-")
                                worker_id_cb.set("-Select-")
                                production.set("")
                                
                        except mysql.connector.Error as err:
                            messagebox.showerror("Oops!", str(err))
                            
                    show_production_data()



                    
                
                def update_production_data():
                    if production.get() == "":
                        messagebox.showerror("Oops", "You missed a spot. Please fill in the required textbox.")
                    elif loom_no.get() == "-Select-":
                        messagebox.showerror("Oops!", "Try another option for Loom No.")
                    elif worker_id_cb.get() == "-Select-":
                        messagebox.showerror("Oops!", "Try another option Worker ID.")
                    elif not production.get().isdigit():
                        messagebox.showerror("Oops!", "Production must be a numeric value.")
                    else:
                        loom_no_var, worker_id_var, production_var = gather_production_data()
                        
                        try:
                            sql_check_query= "SELECT COUNT(*) FROM Production WHERE Loom_No = %s AND Date = CURDATE()"
                            self.mycursor.execute(sql_check_query, (loom_no_var,))
                            num_records = self.mycursor.fetchone()[0]
                            
                            # print(num_records)
                            if num_records == 0:
                                messagebox.showerror("No Data", f"No data found for Loom No {loom_no_var}. Please enter data for this loom first.")
                                
                            else:
                                sql_update_production = "UPDATE Production set Production = %s, worker_id = %s where loom_no = %s and Date = CURDATE()"
                                
                                self.mycursor.execute(sql_update_production, (production_var, worker_id_var, loom_no_var))
                                self.mydb.commit()
                                messagebox.showinfo("Success", f"Updated Loom no {loom_no_var}'s data for today.")
                            
                            loom_no.set("-Select-")
                            worker_id_cb.set("-Select-")
                            production.set("")
                            
                        except mysql.connector.connect as err:
                            messagebox.showerror("Oops!", str(err))
                    
                    show_production_data()    
                    clear_p_fields()

                        

                def show_production_data():
                    # try:
                        self.mycursor.execute
                        (
                            '''
                            SELECT  p.Production_Id, p.Date, p.Day, p.Loom_No, p.Worker_Id, w.Name, p.Production 
                            FROM Production p
                            JOIN Workers w
                            ON p.Worker_Id = w.Worker_Id ORDER BY p.Production_Id DESC
                            '''
                        )
                        
                        rows = self.mycursor.fetchall()
                        # This is because as we continue to enter the daily production the latest production will be at the bottom of the TreeView Widget
                        
                        production_table.delete(*production_table.get_children())
                        
                        for row in rows:
                            production_table.insert('', END, values=row)
                            
                        
                
                def clear_p_fields():
                    loom_no.set("-Select-")
                    worker_id_cb.set("-Select-")
                    production.set("")
                    p_id_cb.set("-Production ID-")
                    save_production.config(state=NORMAL)
                    update_production.config(state=DISABLED)
                           
                def get_production_data(event1):
                    r = production_table.focus()
                    content = (production_table.item(r))
                    row = content.get("values", [])
                    
                    if len(row) >= 5:
                        
                        loom_no.set(row[3])
                        worker_id_cb.set(row[4])
                        production.set(row[6])
                    
                
                
                # Function for enabling the Update button for production update
                def enable_production():
                    update_production.config(state=NORMAL)
                    save_production.config(state=DISABLED)
                    
                    
                    
                    
                production_title = Label(
                    production_frame,
                    text="Production Details",
                    font=('Garamond', 20)
                )
                production_title.place(x=50, y=120, width=1200)
                
                loom_label = Label(
                    production_frame,
                    text='Loom No',
                    font=('Garamond', 15)
                )
                loom_label.place(x=350, y=200)
                loom_combobox = Combobox(
                    production_frame,
                    font=('Garamond', 12),
                    state="readonly",
                    justify=CENTER,
                    textvariable=loom_no
                )
                value_list = ["-Select-"] + list(range(1, 17))
                loom_combobox['values'] = tuple(value_list)
                loom_combobox.current(0)
                loom_combobox.place(x=540, y=200, height=30, width=180)
                
                self.mycursor.execute("SELECT Worker_Id FROM workers") # Fetch the Worker_Id values from the workers table
                worker_ids = self.mycursor.fetchall() # Fetch all rows from the query result
                worker_id_list = ["-Select-"] + [worker[0] for worker in worker_ids] # Extract Worker_Id values from the result
                worker_label2 = Label(
                    production_frame,
                    text='Worker ID',
                    font=('Garamond', 15)
                )
                worker_label2.place(x=350, y=270)
                worker_combobox = Combobox(
                    production_frame,
                    values=worker_id_list,
                    font=('Garamond', 12),
                    state="readonly",
                    justify=CENTER,
                    textvariable=worker_id_cb
                )
                worker_combobox.current(0)
                worker_combobox.place(x=540, y=270, height=30, width=180)
                
                production_label = Label(
                    production_frame,
                    text='Production',
                    font=('Garamond', 15)
                )
                production_label.place(x=350, y=340)
                production_entry = Entry(
                    production_frame,
                    font=('Garamond', 12),
                    justify=CENTER,
                    textvariable=production
                )
                production_entry.place(x=540, y=340, height=30, width=180)
                save_production = Button(
                    production_frame,
                    text='Save',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=save_production_data
                )
                save_production.place(x=540, y=410, height=30, width=100)
                
                # Edit button for enabling the update button
                edit_production = Button(
                    production_frame,
                    text='Edit',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=enable_production
                )
                edit_production.place(x=750, y=200, height=30, width=100)
                
                update_production = Button(
                    production_frame,
                    text='Update',
                    font=('Garamond', 15),
                    cursor="hand2",
                    state=DISABLED,
                    command=update_production_data
                )
                update_production.place(x=750, y=270, height=30, width=100)
                
                clear_btn = Button(
                    production_frame,
                    text='Cancel',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=clear_p_fields
                )
                clear_btn.place(x=750, y=340, height=30, width=100)
                
                worker_table_frame2 = LabelFrame(
                    production_frame,
                    text=' Workers Information ',
                    font=('Garamond', 17, 'bold'),
                    bd=2,
                    relief=RIDGE
                )
                worker_table_frame2.place(x=900, y=180, width=690, height=300)
                
                p_sb_y1 = Scrollbar(
                    worker_table_frame2,
                    orient=VERTICAL
                )
                p_sb_y1.pack(side=RIGHT, fill=Y)
                p_sb_x1 = Scrollbar(
                    worker_table_frame2,
                    orient=HORIZONTAL
                )
                p_sb_x1.pack(side=BOTTOM, fill=X)
                
                workers_table1 = ttk.Treeview(
                    worker_table_frame2,
                    columns=("Worker_Id", "Name", "Surname"),
                    yscrollcommand=p_sb_y1.set,
                    xscrollcommand=p_sb_x1.set
                )
                
                p_sb_y1.config(command=workers_table1.yview)
                p_sb_x1.config(command=workers_table1.xview)
                
                workers_table1.heading("Worker_Id", text="Worker ID")
                workers_table1.heading("Name", text="Name")
                workers_table1.heading("Surname", text="Surname")
                workers_table1["show"] = "headings"
                
                workers_table1.pack(fill=BOTH, expand=1)
                
                self.mycursor.execute("SELECT * FROM workers")
                worker_ids1 = self.mycursor.fetchall()
                
                for record in workers_table1.get_children():
                    workers_table1.delete(record)
                    
                for worker in worker_ids1:
                    workers_table1.insert('', END, values=worker)
                
                production_table_frame = LabelFrame(
                    production_frame,
                    text=' Take a closer look at the table below for detailed Production information ',
                    font=('Garamond', 17, 'bold'),
                    bd=2,
                    relief=RIDGE
                )
                production_table_frame.place(x=0, y=530, relwidth=1, height=385)
                
                p_sb_y = Scrollbar(
                    production_table_frame,
                    orient=VERTICAL
                )
                p_sb_y.pack(side=RIGHT, fill=Y)
                p_sb_x = Scrollbar(
                    production_table_frame,
                    orient=HORIZONTAL
                )
                p_sb_x.pack(side=BOTTOM, fill=X)
                
                production_table = ttk.Treeview(
                    production_table_frame,
                    columns=("Production_Id","Date", "Day", "Loom_No", "Worker_Id", "Worker_Name", "Production"),
                    yscrollcommand=p_sb_y.set,
                    xscrollcommand=p_sb_x.set
                )
                
                p_sb_y.config(command=production_table.yview)
                p_sb_x.config(command=production_table.xview)
                
                production_table.heading("Production_Id", text="Production ID")
                production_table.heading("Date", text="Date")
                production_table.heading("Day", text="Day")
                production_table.heading("Loom_No", text="Loom No")
                production_table.heading("Worker_Id", text="Worker ID")
                production_table.heading("Worker_Name", text="Worker Name")
                production_table.heading("Production", text="Production")
                production_table["show"] = "headings"
                
                production_table.pack(fill=BOTH, expand=1)
                production_table.bind('<ButtonRelease-1>', get_production_data)
                
                show_production_data()
                
                production_frame.pack(fill='both', expand=True) # Ensure production_frame expands to fill main_frame
        
        
        








            # === 6. Report Frame ===
# =====================================================================================================================
            elif number == 6:
                delete_frames()
                report_frame = Frame(main_frame)

                # === All variables =============
                var = IntVar(value=1)
                
                # Function for displaying the report
                def display_report():
                    
                    from_date_report = report_from_date.entry.get()
                    to_date_report = report_to_date.entry.get()
                    
                    from_date1 = datetime.strptime(from_date_report, '%m/%d/%Y').date()
                    to_date1 = datetime.strptime(to_date_report, '%m/%d/%Y').date()
                    
                    # Placing the radiobuttons
                    rb1.place(x=840, y=15)
                    rb2.place(x=1000,y=15)
                    
                    f=Frame(report_frame)
                    
                    u = Frame(report_frame)
                    
                    
                    if var.get() == 1:
                        try:
                            
                            u.place_forget()
                            # 1. Fetch data from the database within the specified date range
                            self.mycursor.execute("SELECT Date, SUM(Production) FROM Production WHERE Date BETWEEN %s AND %s GROUP BY Date", (from_date1, to_date1))
                            production_data = self.mycursor.fetchall()

                            # 2. Extract dates and production values for plotting
                            dates = [str(row[0]) for row in production_data]
                            production_values = [float(row[1]) for row in production_data]
                            
                            # 3. Create the line graph within the report_frame
                            fig, ax = plt.subplots(figsize=(15.8, 8.5))  # Create a figure and axes within report_frame
                            ax.plot(dates, production_values, marker='o', linestyle='-')
                            ax.set_xlabel("Date(s)")
                            ax.set_ylabel("Production")
                            ax.set_title(f"Production Report from {from_date1} to {to_date1}")
                            fig.tight_layout()

                            

                            
                            # Embed the Matplotlib plot into a tkinter canvas within report_frame
                            canvas = FigureCanvasTkAgg(fig, master=f)
                            canvas.draw()
                            canvas.get_tk_widget().pack()  # Pack the canvas inside report_frame                            
                            
                            f.place(x=5, y=60)
                            self.mydb.commit()
                            
                        except Exception as e:
                            messagebox.showerror("Oops!", str(e))
                    
                    
                    elif var.get() == 2:
                        
                        try:
                        
                            f.place_forget()
                            sql_salary = "SELECT DISTINCT(Worker_Full_Name), Total_Salary FROM Salaries WHERE Payment_Date BETWEEN %s and %s" 
                            self.mycursor.execute(sql_salary, (from_date1, to_date1))
                            salaries_data = self.mycursor.fetchall()
                            
                            full_name = [str(fn[0]) for fn in salaries_data]
                            
                            abbreviated_names = [name.split()[0] + " " + name.split()[1][0] for name in full_name]
                            
                            
                            salaries_values = [float(sv[1]) for sv in  salaries_data]
                            
                            fig1, ax1 = plt.subplots(figsize=(15.8, 8.5))
                                
                            ax1.bar(abbreviated_names, salaries_values, color='skyblue')
                            ax1.set_xlabel('Worker Full Name')
                            ax1.set_ylabel('Total Salary')
                            ax1.set_title(f"Salaries paid between {from_date1} to {to_date1}")
                            ax1.tick_params(axis='x', rotation=45)
                            
                            canvas1 = FigureCanvasTkAgg(fig1, master=u)
                            canvas1.draw()
                            canvas1.get_tk_widget().pack()
                            
                            u.place(x=5, y=60)
                            
                            self.mydb.commit()
                            
                        except mysql.connector.Error as e11:
                            messagebox.showerror("Oops!", str(e11))    

                    
                rb1 = Radiobutton(
                    report_frame, 
                    text="Production",
                    font=('Garamond', 15),
                    variable=var,
                    value=1,
                    command=display_report
                )
                
                rb2 = Radiobutton(
                    report_frame,
                    text="Salaries",
                    font=('Garamond', 15),
                    variable=var,
                    value=2,
                    command=display_report
                )
                    
                # From and To date label
                date_label_from = Label(
                    report_frame,
                    text="From",
                    font=('Garamond', 20)
                )
                date_label_from.place(x=10, y=10)
                date_label_to = Label(
                    report_frame,
                    text="To",
                    font=('Garamond', 20)
                )
                date_label_to.place(x=350, y=10)
                
                # Date widget from ttkbootstrap
                report_from_date = tb.DateEntry(
                    report_frame,
                    bootstyle="danger"
                )
                report_from_date.place(x=100, y=15)
                report_to_date = tb.DateEntry(
                    report_frame,
                    bootstyle="danger"
                )
                report_to_date.place(x=405,y=15)
                
                report_button = Button(
                    report_frame,
                    text='Show Data',
                    font=('Garamond', 15),
                    cursor="hand2",
                    command=display_report  
                )
                report_button.place(x=650, y=15, height=30, width=150)

                
                report_frame.pack(fill='both', expand=True)
        
        

        
        
        
        
                
        # Define a function named delete_frames that removes all child widgets from main_frame
        def delete_frames():
            # Iterate over each child widget of main_frame
            for frame in main_frame.winfo_children():
                # Destroy the child widget
                frame.destroy()
        
        # === Frame1 for Menu ===
        left_menu_frame = Frame(self.root, relief=RIDGE, bd=2) # add bd = 2 if you want border to highlight
        left_menu_frame.place(x=0, y=100, width=300, height=920)
        
        # ===Menu Label inside the Frame===
        menu_label = Label(
            left_menu_frame, text="Menu", 
            font=("Garamond", 30),
            height=5
        ).pack(side=TOP, fill=X)  # Packing the 'Menu' label inside the frame
        
        # ===Production button inside the Frame===
        production_button = Button(
            left_menu_frame, 
            text="Production", 
            font=("Garamond", 17),
            cursor="hand2",
            bd=3,
            command=lambda:switch_frames(5)
        ).pack(side=TOP, fill=X, padx=20, pady=10) # Packing the 'Production' button inside the frame
        
        # ===Home button inside the Frame===
        home_button = Button(
            left_menu_frame, 
            text="Salary", 
            font=("Garamond", 17),
            cursor="hand2",
            bd=3,
            command=lambda:switch_frames(1)
        ).pack(side=TOP, fill=X, padx=20, pady=10) # Packing the 'Home' button inside the frame

        # === Report button inside the frame ===
        report_button = Button(
            left_menu_frame,
            text="Report",
            font=("Garamond", 17),
            cursor="hand2",
            bd=3,
            command=lambda:switch_frames(6)
        ).pack(side=TOP, fill=X, padx=20, pady=10)

        # ===Worker button inside the Frame===
        worker_button = Button(
            left_menu_frame, text="Workers", 
            font=("Garamond", 17),
            cursor="hand2",
            bd=3,
            command=lambda:switch_frames(4)
        ).pack(side=TOP, fill=X, padx=20, pady=10) # Packing the 'Worker' button inside the frame
        
        # ===Product button inside the Frame===
        product_button = Button(
            left_menu_frame, text="Product", 
            font=("Garamond", 17),
            cursor="hand2",
            bd=3,
            command=lambda:switch_frames(2)
        ).pack(side=TOP, fill=X, padx=20, pady=10) # Packing the 'Product' button inside the frame
        
        # ===Looms button inside the Frame===
        looms_button = Button(
            left_menu_frame, text="Looms", 
            font=("Garamond", 17),
            cursor="hand2",
            bd=3,
            command=lambda:switch_frames(3)
        ).pack(side=TOP, fill=X, padx=20, pady=10) # Packing the 'Looms' button inside the frame
        
        # === Logout Button inside the frame ===
        exit_button = Button(
            left_menu_frame, text="Exit", 
            font=("Garamond", 17),
            cursor="hand2",
            command=self.exit_the_window
        ).pack(side=TOP, fill=X, padx=20, pady=10)  # Packing the 'Exit' button inside the frame
        
        
        # === This frame2 will be displayed at starting of the window ===
        main_frame = Frame(self.root, bd=2, relief=RIDGE)
        main_frame.place(x=305, y=100, width=1600, height=920)
        
        # Load and Display the image
        image_path = 'images/android-chrome-512x512.png'
        img = Image.open(image_path)
        img = img.resize((300,300))
        img = ImageTk.PhotoImage(img)
        # Creating the Label to hold the image
        image_label = tk.Label(main_frame, image=img)
        image_label.image= img
        image_label.pack(pady=300)
        
        # ===Footer should be at last of the function for displaying it===
        footer_label = Label(
            self.root, 
            text="Developed by Uday Gajul.", 
            font=("Garamond", 10), 
            bg="#4d636d", 
            fg="black"
        ).pack(side=BOTTOM, fill=X)
    
    # Function for redirecting to main.py when clicked on 'Knit Out'
    def redirect_to_homepage(self):
        # Adding redirection logic to main.py
        subprocess.Popen(["python", "main.py"])
        self.root.quit() # Close the current window
    
    # Function for exting current window    
    def exit_the_window(self):
        # First closing the database connection
        if hasattr(self, 'mydb'):
            self.mydb.close()
        
        self.root.quit() # Close the current window
        
    # Function to update the clock label with current date and time
    
    def update_clock(self):
        # Get the current date and time in the specified format
        current_time = datetime.now().strftime("%A %m/%d/%Y %H:%M:%S")
        self.clock_label.config(
            text=f"Check the Date and Time\t\t Day: {current_time.split()[0]}\t\t Date: {current_time.split()[1]}\t\t Time: {current_time.split()[2]}"
        ) # Update the text of the clock label with the current date and time
        self.root.after(1000, self.update_clock)  # Schedule the next update after 1000 milliseconds (1 second) 
        
        
if __name__ == "__main__":
    # Creating an instance of the custom window class, setting the theme to 'superhero'
    root = tb.Window(themename='superhero') # Feel free to customize the themes to suit your preferences and visual style.
    # Light Themes = 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse','sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean'
    # Dark Themes = 'solar', 'superhero', 'darkly', 'cyborg', 'vapor'

    # Creating an instance of the PMS class with the custom window as an argument
    obj = PMS(root)
    root.protocol('WM_DELETE_WINDOW', root.quit)
    # Running the main event loop for the application
    root.mainloop()
