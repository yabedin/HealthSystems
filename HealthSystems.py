from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from database import Database
import datetime

# ----------------Import database-------------

db = Database('healthsystems.db')

# ----------------Styling----------------------

heading1 = ("Calibri", 25, 'bold')
heading2 = ("Calibri", 20)
heading3 = ("Calibri", 16, 'bold')
body = ("Verdana", 12)
heading_bg = ("cadet blue")

# ---------------Page windows-------------------

class HealthSys(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_geometry(self, "1400x800")
        Tk.wm_title(self, "Health Systems - Manage Health")
        
        page = Frame(self)
        page.pack(side="top", fill="both", expand=True)
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for window in (HomePage, GPportal, AdminLoginPage, RegisterPage, UserPage, AdminPortal, Admin_ManageGPs, Admin_ManagePatients):

            frame = window(page, self)
            self.frames[window] = frame
            frame.grid(row=0, column=0, sticky="nsew") 

        self.show_frame(HomePage)
    
    def show_frame(self, pge):
        frame = self.frames[pge]
        frame.tkraise()

class HomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        title = Label(self, text="Health Systems", bg = heading_bg, width = "800", height = '2', font = heading1)
        title.pack()

        Label(self, text = "").pack()
        Label(self, text = "").pack()
        Label(self, text = "Welcome to Health Systems - a simple way to better healthcare.", font=heading2).pack()
        Label(self, text = "").pack()
        Label(self, text = "").pack()
        Label(self, text = "Choose your role to get started.", font=heading3).pack()
        Label(self, text = "").pack()
        
        global user_type
        user_type = StringVar()
        ttk.OptionMenu(self, user_type, "", "Patient", "GP", "Admin").pack()
        Label(self, text = "").pack()
        loginbtn = ttk.Button(self, text="Go", padding=10, command=lambda: self.useroption_func(controller, user_type.get())).pack()

        
        Label(self, text = "").pack()
        Label(self, text = "").pack()
        Label(self, text = "Want to sign up to Health Systems as a patient? Register below.", font=heading3).pack()
        Label(self, text = "").pack()
        registerbtn = ttk.Button(self, text="Register as a patient", command=lambda: controller.show_frame(RegisterPage)).pack()

    # Function to decide which page to load depending on user option 
    def useroption_func(self, cont, type):
        print(type)
        if type == "Patient":
            cont.show_frame(UserPage)
        elif type == "GP":
            cont.show_frame(GPportal)
        elif type == "Admin":
            cont.show_frame(AdminLoginPage)
        else:
            messagebox.showinfo("Select role", "Please select a role to proceed.")

class GPportal(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        title = Label(self, text="GP Portal", font = heading2)
        title.grid(row=0, column=0, padx=30, pady=30, sticky=W)

        # Retrieve gp details via login form 
        Label(self, text="Please login", font=heading3).grid(row = 1, column = 0, sticky=W, padx=30)
        Label(self, text="Username:").grid(row=2, column=0, sticky=W, padx = 30)
        Label(self, text="Password:").grid(row=3, column=0, sticky=W, padx = 30)

        # Login form entry fields
        gp_username_login = StringVar()
        gp_username_login_entry = Entry(self, textvariable=gp_username_login)
        gp_username_login_entry.grid(row=2, column=0, sticky=W, padx=120)

        gp_password_login = StringVar()
        gp_password_login_input = Entry(self, textvariable=gp_password_login)
        gp_password_login_input.grid(row=3, column=0, sticky=W, padx=120)

        loginbtn = ttk.Button(self, text="Login", command=lambda: self.gplogin_verify(controller, gp_username_login_entry, gp_password_login_input))
        loginbtn.grid(row=3,column=0, sticky=E, pady=10)
        homebtn = ttk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(HomePage)).grid(row=3, column=3, sticky=W, padx=10) 

    def gplogin_verify(self, cont, username, password):
        gp_u = username.get()
        gp_pw = password.get()
        print(gp_u, gp_pw)

        # Check if login details are stored 
        if db.gp_login(gp_u, gp_pw):
            username.delete(0, END)
            password.delete(0,END)
            print("logged in")

            gp_id_tuple = db.fetch_gp_id(gp_u)
            loggedin_gp_id = gp_id_tuple[0][0]
            print(loggedin_gp_id)
            self.show_options(loggedin_gp_id, cont)
        else:
            messagebox.showinfo("Error", "Incorrect username or password") 

    def show_options(self, loggedin_gp_id, cont):
        print("GP ID is ", loggedin_gp_id)
        
        # Choose GP action 
        apt_btn = ttk.Button(self, text="Appointments", command=lambda: self.gp_apt_page(cont, loggedin_gp_id))
        apt_btn.grid(row=4, column=0, sticky=W, padx=30, pady=10)

        availability_btn = ttk.Button(self, text="My availability", command=lambda: self.gp_availability(cont, loggedin_gp_id))
        availability_btn.grid(row=5, column=0, sticky=W, padx=30, pady=10)
        
        presc_btn = ttk.Button(self, text="Patient prescriptions", command=lambda: self.prescriptions_page(cont, loggedin_gp_id))
        presc_btn.grid(row=6, column=0, sticky=W, padx=30, pady=10)

    def gp_apt_page(self, cont, gp_id): 

        # New window to manage appointments
        gpapt = Toplevel(self)
        gpapt.wm_title("GP availability")
        gpapt.wm_minsize(width=900, height=700)
        print("gp id is ", gp_id)

        Label(gpapt, text="Manage your appointments", font = heading2).grid(row=1,column=0, sticky=W, padx=30, pady=10)
        global gp_apt_listbox
        gp_apt_listbox = Listbox(gpapt, height=20, width = 90, border=1, exportselection=0)
        gp_apt_listbox.grid(row = 3, column=0, sticky = W, columnspan = 7, rowspan = 13, padx=30)

        # Insert patient's appointment details 
        gp_apt_listbox.delete(0, END)
        for row in db.fetch_gp_aptdetails(gp_id):
            gp_apt_listbox.insert(END, "PATIENT ID: {} DATE: {} TIME: {} REASON: {} CONFIRMATION STATUS: {}".format(row[0], row[1], row[2], row[3], row[4]))
        
        # Bind selected apt 
        def gp_select_apt(event):
            global gp_selected_apt
            index = gp_apt_listbox.curselection()[0]
            gp_selected_apt = gp_apt_listbox.get(index)
            print(gp_selected_apt)

            split_gp_selected_apt = gp_selected_apt.split()
            print(split_gp_selected_apt)

            global selected_patient_id 
            selected_patient_id = int(split_gp_selected_apt[2])

            global gp_selected_apt_date
            gp_selected_apt_date = split_gp_selected_apt[4]

            global gp_selected_apt_time 
            gp_selected_apt_time = split_gp_selected_apt[6]
        gp_apt_listbox.bind('<<ListboxSelect>>', gp_select_apt)

        # Buttons to manage appointments
        cancel_apt_btn = ttk.Button(gpapt, text="Cancel appointment", command=lambda: self.cancel_apt(gp_id))
        cancel_apt_btn.grid(row=18, column=0, sticky=W, padx=30, pady=10)

        confirm_apt_btn = ttk.Button(gpapt, text="Confirm appointment", command=lambda: self.confirm_apt(gp_id))
        confirm_apt_btn.grid(row=18, column=0, sticky=E, pady=10)

    def prescriptions_page(self, cont, gp_id): 
        # New window for prescriptions page
        gppr = Toplevel(self)
        gppr.wm_title("Prescriptions")
        gppr.wm_minsize(width=1300, height=800)
        Label(gppr, text="Manage your prescriptions", font=heading2).grid(row=1, column=0, sticky=W, padx=30, pady=10)

        # Listbox for prescriptions
        global pres_listbox
        pres_listbox = Listbox(gppr, height=10, width = 160, border=1, exportselection=0)
        pres_listbox.grid(row = 3, column=0, sticky = W, columnspan = 10, rowspan = 10, padx=30)
        
        # Insert prescriptions that logged in GP has issued  
        pres_listbox.delete(0, END)
        for row in db.fetch_gp_prescriptions(gp_id):
            pres_listbox.insert(END, "PRESCRIPTION ID {} PATIENT ID: {} DRUG: {} DOSAGE: {} INDICATION: {} WHEN TO TAKE: {} INSTRUCTIONS: {} DATE PRESCRIBED: {}".format(row[0], row[1], row[3], row[4], row[5], row[6], row[8], row[7])) 

        # Bind selected apt 
        def gp_select_pres(event):
            global selected_pres
            index = pres_listbox.curselection()[0]
            selected_pres = pres_listbox.get(index)
            print(selected_pres)

            split_selected_pres = selected_pres.split()
            print(split_selected_pres)
            
            global presc_id 
            presc_id = int(split_selected_pres[2])
            print(presc_id)
        pres_listbox.bind('<<ListboxSelect>>', gp_select_pres)

        # Button to remove prescription
        remove_pres = ttk.Button(gppr, text="Remove prescription", command=lambda: self.remove_pres(gp_id, presc_id))
        remove_pres.grid(row=17, column=0, sticky=W, padx=30, pady=10)
        Label(gppr, text="").grid(row=18, column=0)

        # Form for inputting prescriptions 
        Label(gppr, text="Enter a new prescription below", font=heading3).grid(row=19, column=0, padx=30, sticky=W)
        
        # Choose the patient to write a prescription for (these are confirmed patients)
        Label(gppr, text="Patient").grid(row=20, column=0, padx=30, sticky=W)
        global pat_listbox  
        pat_listbox = Listbox(gppr, height = 5, width = 70, exportselection=0)
        pat_listbox.grid(row=21, column=0, padx=33, sticky=W, rowspan = 4, columnspan=3)

        pat_listbox.delete(0, END)
        for row in db.fetch_patients():
            pat_listbox.insert(END, "PATIENT ID: {} NAME: {} {}".format(row[0], row[1], row[2]))
        
        # Bind selected prescription
        def pat_select(event):
            index = pat_listbox.curselection()[0]
            selected_pat = (pat_listbox.get(index)).split()
            print(selected_pat)

            global selected_pat_id
            selected_pat_id = int(selected_pat[2])
            print(selected_pat_id)
        pat_listbox.bind('<<ListboxSelect>>', pat_select)

        # Prescription entry fields
        Label(gppr, text = "Drug", font=body).grid(row=26, column=0, padx=30, sticky=W)
        drug_name = StringVar()
        drug_name_input = Entry(gppr, textvariable=drug_name)
        drug_name_input.grid(row=27, column=0, padx=30, sticky=W)

        Label(gppr, text = "Dosage", font=body).grid(row=28, column=0, padx=30, sticky=W)
        dosage = StringVar()
        dosage_input = Entry(gppr, textvariable=dosage)
        dosage_input.grid(row=29, column=0, padx=30, sticky=W)

        Label(gppr, text = "Indication", font=body).grid(row=30, column=0, padx=30, sticky=W)
        indication = StringVar()
        indication_input = Entry(gppr, textvariable=indication)
        indication_input.grid(row=31, column=0, padx=30, sticky=W)

        Label(gppr, text = "When to take", font=body).grid(row=32, column=0, padx=30, sticky=W)
        when_take = StringVar()
        when_take_input = Entry(gppr, textvariable=when_take)
        when_take_input.grid(row=33, column=0, padx=30, sticky=W)

        Label(gppr, text = "Further instructions", font=body).grid(row=34, column=0, padx=30, sticky=W)
        instructions = StringVar()
        instructions_input = Entry(gppr, textvariable=instructions)
        instructions_input.grid(row=35, column=0, padx=30, sticky=W)

        add_pres_btn = ttk.Button(gppr, text="Add prescription", command=lambda: self.add_pres(gp_id, drug_name_input, dosage_input, indication_input, when_take_input, instructions_input))
        add_pres_btn.grid(row=36, column=0, sticky=W, padx=30, pady=10)
        
    def gp_availability(self, cont, gp_id):

        # Window for availability listbox
        gpav = Toplevel(self)
        gpav.wm_title("GP availability")
        gpav.wm_minsize(width=900, height=700)
        Label(gpav, text="Manage your availability", font=heading2).grid(row=1,column=0, pady=10, sticky=W, padx=30)

        global availability_listbox
        availability_listbox = Listbox(gpav, height=15, width = 30, border=1, exportselection=0)
        availability_listbox.grid(row = 3, column=0, sticky = W, columnspan = 7, rowspan = 7, padx=30)

        # Insert gp availability 
        availability_listbox.delete(0, END)
        for row in db.fetch_gp_availability(gp_id):
            availability_listbox.insert(END, "DATE: {} TIME: {}".format(row[0], row[1]))

        # Bind selected date & time in availability box 
        def gp_datetime_selected(event):
            global gp_selected_datetime
            index = availability_listbox.curselection()[0]
            gp_selected_datetime = availability_listbox.get(index)
            
            split_gp_selected_datetime = gp_selected_datetime.split()
            print(split_gp_selected_datetime)

            global aval_date 
            aval_date = split_gp_selected_datetime[1]

            global aval_time 
            aval_time = split_gp_selected_datetime[3]

            print(gp_selected_datetime, aval_date, aval_time)
        availability_listbox.bind('<<ListboxSelect>>', gp_datetime_selected)
        
        Label(gpav, text=" ", font=heading3).grid(row=10, padx=30, column=0, sticky=W)        
        Label(gpav, text="Add your availability", font=heading3).grid(row=11, padx=30, column=0, sticky=W)

        # Date selection box 
        Label(gpav, text="Date?", font=body).grid(row=12,column=0, padx=30, sticky=W)
        global gp_date_listbox
        gp_date_listbox = Listbox(gpav, height=8, width = 15, border=1)
        gp_date_listbox.grid(row = 13, column=0, sticky = W, columnspan = 1, rowspan = 3, padx=30)

        # Insert dates (7 days ahead)
        today = datetime.date.today()
        for i in range(8):
            apt_day = datetime.timedelta(days=i)
            gp_date_listbox.insert(END, today+apt_day)

        # Bind selected date 
        def date_selected(event):
            global gp_selected_date
            index = gp_date_listbox.curselection()[0]
            gp_selected_date = gp_date_listbox.get(index)
            print(gp_selected_date)
        gp_date_listbox.bind('<<ListboxSelect>>', date_selected)
        
        # Time selection box 
        Label(gpav, text="Time?", font=body).grid(row=12,column=0, padx=170, sticky=W)
        global gp_time_listbox 
        gp_time_listbox = Listbox(gpav, height=8, width = 15, border=1, exportselection=0)
        gp_time_listbox.grid(row = 13, column=0, padx=170, sticky = W, columnspan = 1, rowspan = 3)

        # Insert times
        times = ['0900', '0930', '1000', '1030', '1100', '1130', '1300', '1330', '1400', '1430']
        for time in times:
            gp_time_listbox.insert(END, time)

        # Bind selected time 
        def gp_time_selected(event):
            global gp_selected_time
            index = gp_time_listbox.curselection()[0]
            gp_selected_time = gp_time_listbox.get(index)
            print(gp_selected_time)
        gp_time_listbox.bind('<<ListboxSelect>>', gp_time_selected)

        # Buttons to manage availability
        add_datetimes = ttk.Button(gpav, text="Add slot", command=lambda: self.add_avail(gp_id))
        add_datetimes.grid(row=18, column=0, padx=30, sticky=W, pady=10)

        remove_datetimes = ttk.Button(gpav, text="Remove slot", command=lambda: self.remove_avail(gp_id))
        remove_datetimes.grid(row=10, column=0, sticky=W, pady=10, padx=30)
    
    def add_avail(self, gp_id):
        # Add availability to GP availability table
        try:
            print(gp_selected_date, gp_selected_time)
        except:
            messagebox.showerror('Error', 'Please click on the date and time of the slot you would like to add') 
        else:
            if gp_date_listbox.curselection():
                if db.existing_time_slot(gp_selected_date, gp_selected_time, gp_id):
                    print("slot exists")
                    messagebox.showerror('Existing slot', "Appointment slot already added.")
                else: 
                    print("no slot exists")
                    db.insert_availability(gp_selected_date, gp_selected_time, gp_id)
                    availability_listbox.delete(0, END)
                    for row in db.fetch_gp_availability(gp_id):
                        availability_listbox.insert(END, "DATE: {} TIME: {}".format(row[0], row[1]))       

    def remove_avail(self, gp_id):
        # Remove availability from availability table
        if availability_listbox.curselection():
            delete_check = messagebox.askokcancel('Delete slot', 'Are you sure you would like to remove this slot?')
            if delete_check == True:
                # fix the selected date and time variables 
                db.remove_slot(gp_id, aval_date, aval_time)
                availability_listbox.delete(0, END)
                for row in db.fetch_gp_availability(gp_id):
                    availability_listbox.insert(END, "DATE: {} TIME: {}".format(row[0], row[1]))
        else:
            messagebox.showerror('Error', 'Please click on the slot you would like to cancel')            
    
    def cancel_apt(self, gp_id):
        # Cancel appointment - check if appointment is selected first
        if gp_apt_listbox.curselection():
            delete_check = messagebox.askokcancel('Delete appointment', 'Are you sure you would like to cancel this appointment?')
            if delete_check == True:
                db.delete_apt(gp_id, gp_selected_apt_date, gp_selected_apt_time)
                gp_apt_listbox.delete(0, END)
                for row in db.fetch_gp_aptdetails(gp_id):
                    gp_apt_listbox.insert(END, "PATIENT ID: {} DATE: {} TIME: {} REASON: {} CONFIRMATION STATUS: {}".format(row[0], row[1], row[2], row[3], row[4]))
        else:
            messagebox.showerror('Error', 'Click on the appointment you would like to cancel')
    
    def confirm_apt(self, gp_id):
        # Confirm appointment - check if an appointment is selected first 
        if gp_apt_listbox.curselection():
            confirm_check = messagebox.askokcancel('Confirm appointment', 'Are you sure you would like to confirm this appointment?')
            if confirm_check == True:
                db.apt_confirmation(gp_id, gp_selected_apt_date, gp_selected_apt_time)
                print("confirmed")
                gp_apt_listbox.delete(0, END)
                for row in db.fetch_gp_aptdetails(gp_id):
                    gp_apt_listbox.insert(END, "PATIENT ID: {} DATE: {} TIME: {} REASON: {} CONFIRMATION STATUS: {}".format(row[0], row[1], row[2], row[3], row[4]))
        else:
            messagebox.showerror('Error', 'Click on the appointment you would like to confirm')

    def add_pres(self, gp_id, drug, dosage, indication, when_take, instructions):
        # Form input fields saved in a list called 'entrys' 
        entrys = [drug, dosage, indication, when_take, instructions]

        # Get the values of the input fields
        drug = drug.get()
        dosage = dosage.get()
        indication = indication.get()
        when_take = when_take.get()
        instructions = instructions.get()

        # Insert prescription timestamp (current time)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if all fields complete, then enter prescription into database
        if drug == "" or dosage == "" or indication == "" or when_take == "" or instructions == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else: 
            db.insert_prescription(selected_pat_id, gp_id, drug, dosage, indication, when_take, now, instructions) 
            pres_listbox.delete(0, END)
            for row in db.fetch_gp_prescriptions(gp_id):
                pres_listbox.insert(END, "PRESCRIPTION ID {} PATIENT ID: {} DRUG: {} DOSAGE: {} INDICATION: {} WHEN TO TAKE: {} INSTRUCTIONS: {} DATE PRESCRIBED: {}".format(row[0], row[1], row[3], row[4], row[5], row[6], row[8], row[7]))  
            for entry in entrys:
                entry.delete(0, END)
    
    def remove_pres(self, gp_id, presc_id):
        # Remove prescription - check if a prescription has been selected first 
        if pres_listbox.curselection():
            delete_check = messagebox.askokcancel('Delete prescription', 'Are you sure you would like to permanently delete this prescription?')
            if delete_check == True:
                db.delete_prescription(gp_id, presc_id)
                pres_listbox.delete(0, END)
                for row in db.fetch_gp_prescriptions(gp_id):
                    pres_listbox.insert(END, "PRESCRIPTION ID {} PATIENT ID: {} DRUG: {} DOSAGE: {} INDICATION: {} WHEN TO TAKE: {} INSTRUCTIONS: {} DATE PRESCRIBED: {}".format(row[0], row[1], row[3], row[4], row[5], row[6], row[8], row[7])) 
        else:
            messagebox.showerror('Error', 'Click on the appointment you would like to remove')

class AdminLoginPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        title = Label(self, text="Admin Login page", bg = heading_bg, width = "500", height = '2', font = heading2)
        title.pack()

        Label(self, text = "Please enter your details to login", font = heading3).pack()
        Label(self, text = "").pack()

        # Login form 
        Label(self, text = "Username", font=body).pack()
        global adminusername_login
        adminusername_login = StringVar()
        global adminusernamelogin_input
        adminusernamelogin_input = Entry(self, textvariable=adminusername_login)
        adminusernamelogin_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Password", font=body).pack()
        global adminpassword_login
        adminpassword_login = StringVar()
        global adminpasswordlogin_input
        adminpasswordlogin_input = Entry(self, textvariable=adminpassword_login)
        adminpasswordlogin_input.pack()

        Label(self, text = "").pack()
        submitbtn = ttk.Button(self, text = "Login", command=lambda: self.admin_login_verify(controller)).pack()
        
        Label(self, text = "").pack()
        homebtn = ttk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(HomePage)).pack() 

    def admin_login_verify(self, cont):
        admin_u = adminusername_login.get()
        admin_pw = adminpassword_login.get()

        # Check if admin login details are saved in admin table 
        if db.admin_login(admin_u, admin_pw):
            cont.show_frame(AdminPortal)
            adminusernamelogin_input.delete(0, END)
            adminpasswordlogin_input.delete(0,END)
        else:
            messagebox.showinfo("Error", "Incorrect username or password") 

class RegisterPage(Frame):
     
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        title = Label(self, text="Register", bg = heading_bg, width = "500", height = '2', font = heading2)
        title.pack()

        # Registration form 
        Label(self, text = "Please enter your details to register", font = heading3).pack()
        Label(self, text = "").pack()

        Label(self, text = "Firstname", font=body).pack()
        global firstname
        firstname = StringVar()
        global firstname_input
        firstname_input = Entry(self, textvariable=firstname)
        firstname_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Lastname", font=body).pack()
        global lastname
        lastname = StringVar()
        global lastname_input
        lastname_input = Entry(self, textvariable=lastname)
        lastname_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Username", font=body).pack()
        global username
        username = StringVar()
        global username_input
        username_input = Entry(self, textvariable=username)
        username_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Password", font=body).pack()
        global password
        password = StringVar()
        global password_input
        password_input = Entry(self, textvariable=password)
        password_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Confirm password", font=body).pack()
        global confirm_password
        confirm_password = StringVar()
        global confirm_password_input
        confirm_password_input = Entry(self, textvariable=confirm_password)
        confirm_password_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Date of birth in 'ddmmyy' format", font=body).pack()
        global dob
        dob = IntVar()
        global dob_input
        dob_input = Entry(self, textvariable=dob)
        dob_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Gender").pack()
        global gender 
        gender = StringVar()
        ttk.OptionMenu(self, gender, "", "Male", "Female").pack()
        Label(self, text = "").pack()

        Label(self, text = "Email", font=body).pack()
        global email
        email = StringVar()
        global email_input
        email_input = Entry(self, textvariable=email)
        email_input.pack()
        Label(self, text = "").pack()

        Label(self, text = "Mobile number", font=body).pack()
        global mobileno
        mobileno = IntVar()
        global mobileno_input
        mobileno_input = Entry(self, textvariable=mobileno)
        mobileno_input.pack()

        Label(self, text = "").pack()
        submitbtn = ttk.Button(self, text = "Register for review by admin", command=lambda: self.new_user(controller)).pack()

        Label(self, text = "").pack()
        homebtn = ttk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(HomePage))
        homebtn.pack()

    def new_user(self, cont):
        # Get values of fields in registration form 
        new_firstname = firstname.get()
        new_lastname = lastname.get()
        new_u = username.get()
        new_pw = password.get()
        con_pw = confirm_password.get()
        new_dob = dob.get()
        new_gender = gender.get()
        new_email = email.get()
        new_mob = mobileno.get()

        # Check if all fields are complete, if passwords match, or if there's an existing username
        if new_firstname == "" or new_lastname == "" or new_u == "" or new_pw == "" or con_pw == "" or new_dob == "" or new_gender == "" or new_email == "" or new_mob == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            if new_pw != con_pw:
                messagebox.showerror("Error", "Passwords do not match")
                print("passwords don't match")
            else: 
                if db.new_patient_username_check(new_u):
                    messagebox.showerror("Error", "Existing username")
                else:
                    db.insert_patient(new_u, new_pw, new_firstname, new_lastname, new_dob, new_gender, new_email, new_mob)
                    firstname_input.delete(0,END)
                    lastname_input.delete(0, END)
                    username_input.delete(0, END)
                    password_input.delete(0, END)
                    confirm_password_input.delete(0, END)
                    dob_input.delete(0, END)
                    email_input.delete(0, END)
                    mobileno_input.delete(0, END)

                    cont.show_frame(UserPage)

class UserPage(Frame): 
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        title = Label(self, text="Manage your appointments", font = heading1).grid(row=0,column=0, padx=30, pady=20, sticky=W)

        # Retrieve patient details via login form 
        Label(self, text="Please login", font=heading3).grid(row = 1, column = 0, sticky=W, padx=30)
        Label(self, text="Username:").grid(row=2, column=0, sticky=W, padx = 30)
        Label(self, text="Password:").grid(row=3, column=0, sticky=W, padx = 30)

        # Login form entry fields
        username_login = StringVar()
        username_login_entry = Entry(self, textvariable=username_login)
        username_login_entry.grid(row=2, column=0, sticky=W, padx=120)

        password_login = StringVar()
        password_login_input = Entry(self, textvariable=password_login)
        password_login_input.grid(row=3, column=0, sticky=W, padx=120)

        loginbtn = ttk.Button(self, text="Login", command=lambda: self.login_verify(controller, username_login_entry, password_login_input))
        loginbtn.grid(row=3,column=0, sticky=E)
        
        Label(self, text="").grid(row=4,column=0, padx=30, sticky=W)
        homebtn = ttk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(HomePage)).grid(row=4, column=0, sticky=W, padx=30, pady=5)

    def login_verify(self, cont, username, password):
        u = username.get()
        pw = password.get()
        print(u,pw)

        # If statement to check whether status confirmed or unconfirmed. If confirmed, redirect to book appointment winow
        if db.patient_login(u, pw):
            username.delete(0, END)
            password.delete(0,END)

            loggedin_pat_id = db.fetch_pat_id(u)
            pat_id = loggedin_pat_id[0][0]

            if db.patient_status(pat_id):
                messagebox.showerror("Awaiting Confirmation", "Sorry, your registration needs approval by the admin before you can book appointments.")
            else:
                print('confirmed')
                self.book_apt(loggedin_pat_id, cont)
        else:
            messagebox.showinfo("Error", "Incorrect username or password") 
    
    def book_apt(self,loggedin_pat_id, cont):
        Label(self, text="Book an appointment", font = heading2).grid(row=5,column=0, padx=30, pady=10, sticky=W)
        
        # GP name box
        Label(self, text="Which GP would you like to see? (GP ID & name shown below)", font=body).grid(row=6,column=0, padx=31, sticky=W)
        gp_listbox = Listbox(self, height=10, width = 40, border=1, exportselection=0)
        gp_listbox.grid(row = 7, column=0, sticky=W, columnspan = 1, rowspan = 3, padx=30)
        for row in db.fetch_gp_names():
            gp_listbox.insert(END, "{} {} {}".format(row[0], row[1], row[2]))

        # Bind selected gp 
        def gp_selected(event):
            global selected_gp
            index = gp_listbox.curselection()[0]
            gp = gp_listbox.get(index)
            selected_gp = gp.split()
            print(selected_gp[0])
        gp_listbox.bind('<<ListboxSelect>>', gp_selected)

        # Date selection box 
        Label(self, text="Date?", font=body).grid(row=13,column=0, padx=30, sticky=W)
        date_listbox = Listbox(self, height=8, width = 15, border=1)
        date_listbox.grid(row = 14, column=0, sticky = W, columnspan = 1, rowspan = 3, padx=30)

        # Insert dates (7 days ahead)
        today = datetime.date.today()
        for i in range(8):
            apt_day = datetime.timedelta(days=i)
            # print(today + apt_day)
            date_listbox.insert(END, today+apt_day)

        # Bind selected date 
        def date_selected(event):
            global selected_date
            index = date_listbox.curselection()[0]
            selected_date = date_listbox.get(index)
            print(selected_date)
        date_listbox.bind('<<ListboxSelect>>', date_selected)
        
        # Time selection box 
        Label(self, text="Time?", font=body).grid(row=13,column=0, padx=170, sticky=W)
        time_listbox = Listbox(self, height=8, width = 15, border=1, exportselection=0)
        time_listbox.grid(row = 14, column=0, sticky = W, columnspan = 1, rowspan = 3, padx=170)

        # Insert times
        times = ['0900', '0930', '1000', '1030', '1100', '1130', '1300', '1330', '1400', '1430']
        for time in times:
            time_listbox.insert(END, time)

        # Bind selected time 
        def time_selected(event):
            global selected_time
            index = time_listbox.curselection()[0]
            selected_time = time_listbox.get(index)
            print(selected_time)
        time_listbox.bind('<<ListboxSelect>>', time_selected)
        
        # Appointment reason entry field 
        Label(self, text="Appointment reason? (optional)", font=body).grid(row=19,column=0, padx=30, sticky=W)
        apt_reason = StringVar()
        apt_reason_entry = Entry(self, textvariable=apt_reason)
        apt_reason_entry.grid(row=20,column=0, padx=30, sticky=W+E)
        Label(self, text="").grid(row=21, column=0)
        ttk.Button(self, text="Add", command=lambda: self.add_apt(apt_reason_entry.get(), loggedin_pat_id[0][0])).grid(row=21,column=0, sticky=W, padx=30)

        # Appointment list box 
        Label(self, text="Your appointments", font = heading2).grid(row=5,column=1, pady=10, sticky=W)
        global apt_listbox
        apt_listbox = Listbox(self, height=20, width = 90, border=1, exportselection=0)
        apt_listbox.grid(row = 6, column=1, sticky = W, columnspan = 7, rowspan = 13)
        
        # Bind selected apt 
        def apt_selected(event):
            global selected_apt
            index = apt_listbox.curselection()[0]
            selected_apt = apt_listbox.get(index)
            print(selected_apt)
            split_selected_apt = selected_apt.split()

            global selected_gp_id 
            selected_gp_id = int(split_selected_apt[2])

            global selected_apt_date
            selected_apt_date = split_selected_apt[4]

            global selected_apt_time
            selected_apt_time = split_selected_apt[6]
        apt_listbox.bind('<<ListboxSelect>>', apt_selected)

        # Insert patient's appointment details 
        apt_listbox.delete(0, END)
        for row in db.fetch_aptdetails(loggedin_pat_id[0][0]):
            apt_listbox.insert(END, "GP ID: {} DATE: {} TIME: {} REASON: {} CONFIRMATION STATUS: {}".format(row[0], row[1], row[2], row[3], row[4]))

        # Buttons 
        ttk.Button(self, text="Clear text", command=lambda: self.clear_text(apt_reason_entry)).grid(row=21,column=0, sticky=E, padx=30, pady=3)
        ttk.Button(self, text="Delete appointment", command=lambda: self.delete_apt(loggedin_pat_id[0][0])).grid(row=19,column=5, sticky=E)
        ttk.Button(self, text="View my prescriptions", command=lambda: self.pat_prescriptions_page(cont, loggedin_pat_id[0][0])).grid(row=25,column=0, sticky=W, padx=30)
    
    def clear_text(self, apt_reason_entry):
        apt_reason_entry.delete(0, END)

    def add_apt(self, reason, pat_id):
        # Check if a GP, date and time have been selected
        try:
            gp_id = int(selected_gp[0])
            print(gp_id, selected_date, selected_time)
        except:
            messagebox.showerror("Error", "Please ensure you've selected a GP, date and time.")
        else:
            # If no errors, insert into database
            if db.existing_apt_check(gp_id, selected_date, selected_time):
                print("This appointment slot has been taken up, choose another GP, date or time")
                messagebox.showerror("Error", "This appointment slot has been filled, please select another GP, date or time")
            else:
                print("Insert into database")
                db.insert_apt(pat_id, gp_id, selected_date, selected_time, reason)
                apt_listbox.delete(0, END)
                for row in db.fetch_aptdetails(pat_id):
                    apt_listbox.insert(END, "GP ID: {} DATE: {} TIME: {} REASON: {} CONFIRMATION STATUS: {}".format(row[0], row[1], row[2], row[3], row[4]))

    def delete_apt(self, pat_id):
        # Check if an appointment has been clicked on 
        try:
            print(selected_gp_id, selected_apt_date, selected_apt_time, pat_id)
        except:
            print("None selected")
        if apt_listbox.curselection():
            delete_check = messagebox.askokcancel('Delete appointment', 'Are you sure you would like to permanently delete this appointment?')
            if delete_check == True:
                db.delete_apt(selected_gp_id, selected_apt_date, selected_apt_time)
                apt_listbox.delete(0, END)
                for row in db.fetch_aptdetails(pat_id):
                    apt_listbox.insert(END, "GP ID: {} DATE: {} TIME: {} REASON: {} CONFIRMATION STATUS: {}".format(row[0], row[1], row[2], row[3], row[4]))
        else:
            messagebox.showerror('Error', 'Click on the appointment you would like to remove')

    def pat_prescriptions_page(self, cont, pat_id):
        # New window for prescriptions 
        patpr = Toplevel(self)
        patpr.wm_title("My prescriptions")
        patpr.wm_minsize(width=1300, height=400)
        Label(patpr, text="View your prescriptions", font=heading2).grid(row=1, column=0, sticky=W, padx=30, pady=10)
 
        pat_pres = Listbox(patpr, height=10, width = 160, border=1, exportselection=0)
        pat_pres.grid(row = 3, column=0, sticky = W, columnspan = 10, rowspan = 10, padx=30)
        
        # Insert prescriptions that gp has issued  
        pat_pres.delete(0, END)
        for row in db.fetch_patient_prescriptions(pat_id):
            pat_pres.insert(END, "PRESCRIPTION ID {} GP ID: {} DRUG: {} DOSAGE: {} INDICATION: {} WHEN TO TAKE: {} INSTRUCTIONS: {} DATE PRESCRIBED: {}".format(row[0], row[2], row[3], row[4], row[5], row[6], row[8], row[7])) 

class AdminPortal(Frame):
     
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        title = Label(self, text="Admin", bg = heading_bg, width = "500", height = '2', font = heading2)
        title.pack()

        Label(self, text="Welcome to your portal", font=heading2).pack()
        Label(self, text = "").pack()
        Label(self, text="Manage GPs or patients", font=heading3).pack()
        Label(self, text = "").pack()
        
        Label(self, text="I would like to manage...", font=body).pack()
        Label(self, text = "").pack()
        global admin_action
        admin_action = StringVar()
        ttk.OptionMenu(self, admin_action, "", "GPs", "Patients").pack()
        ttk.Button(self, text="Go", command=lambda: self.adminoption_func(controller,admin_action.get())).pack()

        Label(self, text = "").pack()
        homebtn = ttk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(HomePage)).pack()

    # Decide which page to load depending on admin action 
    def adminoption_func(self, cont, type):
        if type == "GPs":
            cont.show_frame(Admin_ManageGPs)
            # Redirect to GP manage page 
        elif type == "Patients":
            cont.show_frame(Admin_ManagePatients)
        else:
            messagebox.showerror("None selected", "Please choose GPs or patients to manage")

class Admin_ManageGPs(Frame):   
    
    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        title = Label(self, text="Manage GPs", font = heading1).grid(row=0,column=0, padx=30, sticky=W, pady=20)

        # GP form: firstname, lastname, username, password
        heading = Label(self, text="Add GPs", font = heading3).grid(row=1,column=0, padx=30, pady=10, sticky=W)
        
        Label(self, text="First Name", font=body).grid(row=2,column=0, padx=30, sticky=W)
        new_gp_firstname = StringVar()
        gpfname_entry = Entry(self, textvariable=new_gp_firstname)
        gpfname_entry.grid(row=3,column=0, padx=30)

        Label(self, text="Last Name", font=body).grid(row=4,column=0, padx=30, sticky=W)
        new_gp_lastname = StringVar()
        gplname_entry = Entry(self, textvariable=new_gp_lastname)
        gplname_entry.grid(row=5,column=0, padx=30)

        Label(self, text="Username", font=body).grid(row=6,column=0, padx=30, sticky=W)
        new_gp_username = StringVar()
        gpusname_entry = Entry(self, textvariable=new_gp_username)
        gpusname_entry.grid(row=7,column=0, padx=30)

        Label(self, text="Password", font=body).grid(row=8,column=0, padx=30, sticky=W)
        new_gp_password = StringVar()
        gppwname_entry = Entry(self, textvariable=new_gp_password)
        gppwname_entry.grid(row=9,column=0, padx=30)

        # Buttons 
        Label(self, text="").grid(row=10,column=0, padx=30)
        ttk.Button(self, text="Add", command=lambda: self.add_GP(controller, gpfname_entry, gplname_entry, gpusname_entry, gppwname_entry)).grid(row=11,column=0, sticky=W, padx=30, pady=5)
        ttk.Button(self, text="Clear text", command=lambda: self.clear_text(controller, gpfname_entry, gplname_entry, gpusname_entry, gppwname_entry)).grid(row=11,column=0, sticky=E, padx=20, pady=5)
        ttk.Button(self, text="See GP's availability", command=lambda: self.gp_availability(controller)).grid(row=13,column=0, sticky=W, padx=30, pady=5)
        ttk.Button(self, text="Delete GP", command=lambda: self.delete_gp(controller)).grid(row=14,column=0, sticky=W, padx=30, pady=5)
        ttk.Button(self, text="Deactivate GP", command=lambda: self.deactivate_gp(controller)).grid(row=15,column=0, sticky=W, padx=30, pady=5)
        ttk.Button(self, text="Activate GP", command=lambda: self.activate_gp(controller)).grid(row=16,column=0, sticky=W, padx=30, pady=5)
        Label(self, text="", font=heading).grid(row=17,column=0, padx=30)
        homebtn = ttk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(HomePage)).grid(row=18, column=0, sticky=W, padx=30, pady=5)
        gpportalbtn = ttk.Button(self, text="Back to Admin Portal", command=lambda: controller.show_frame(AdminPortal)).grid(row=19, column=0, sticky=W, padx=30, pady=5)

        # GP list box 
        global admin_gp_listbox 
        Label(self, text="", font=heading3).grid(row = 1, column = 1, sticky=W, padx=30)
        admin_gp_listbox = Listbox(self, height=20, width = 90, border=1)
        admin_gp_listbox.grid(row = 2, column=1, sticky = NW+E, columnspan = 4, rowspan = 11, padx=20)

        # Import GP data 
        admin_gp_listbox.delete(0, END)
        for row in db.fetch_gp():
            admin_gp_listbox.insert(END, "GP ID: {} FIRST NAME: {} LAST NAME: {} USERNAME: {} STATUS: {}".format(row[0], row[3], row[4], row[1], row[5]))

        # Bind selected item 
        def select_item(event):
            index = admin_gp_listbox.curselection()[0]
            selecteditem = admin_gp_listbox.get(index)
            split_items = selecteditem.split()
            global selected_gpid
            selected_gpid = int(split_items[2])
        admin_gp_listbox.bind('<<ListboxSelect>>', select_item)

    def add_GP(self, cont, firsname, lastname, username, password):
        # Get values in entry fields
        firsname = firsname.get()
        lastname = lastname.get()
        username = username.get()
        password = password.get()

        # Check for any empty fields, else insert into gp table
        if firsname == "" or lastname == "" or username == "" or password == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            db.insert_gp(username, password, firsname, lastname)
            admin_gp_listbox.delete(0, END)
            for row in db.fetch_gp():
                admin_gp_listbox.insert(END, "GP ID: {} FIRST NAME: {} LAST NAME: {} USERNAME: {} STATUS: {}".format(row[0], row[3], row[4], row[1], row[5]))
        
    def clear_text(self, cont, firstname, lastname, username, password):
        entrys = [firstname, lastname, username, password]
        for entry in entrys:
            entry.delete(0, END)
    
    def delete_gp(self, cont):
        # Check if there's a selected GP, then delete if cancel messagebox value is True
        try:
            print("Selected GP ID: ", selected_gpid)
        except:
            messagebox.showerror('Error', 'Click on the GP you would like to remove')
        else:
            result = messagebox.askokcancel('Remove GP', 'Are you sure you would like to permanently remove this GP?')
            if result == True:
                db.delete_gp(selected_gpid)
                admin_gp_listbox.delete(0, END)
                for row in db.fetch_gp():
                    admin_gp_listbox.insert(END, "GP ID: {} FIRST NAME: {} LAST NAME: {} USERNAME: {} STATUS: {}".format(row[0], row[3], row[4], row[1], row[5]))
    
    def deactivate_gp(self, cont):
        # Check if GP has been selected, then deactivate if messagebox value is True
        try:
            print("Selected GP ID: ", selected_gpid)
        except:
            messagebox.showerror('Error', 'Click on the GP you would like to deactivate')
        else:
            result = messagebox.askokcancel('Deactivate GP', 'Are you sure you would like to deactivate this GP?')
            if result == True:
                db.gp_deactivate(selected_gpid)
                admin_gp_listbox.delete(0, END)
                for row in db.fetch_gp():
                    admin_gp_listbox.insert(END, "GP ID: {} FIRST NAME: {} LAST NAME: {} USERNAME: {} STATUS: {}".format(row[0], row[3], row[4], row[1], row[5]))

    def activate_gp(self, cont):
        # Check if GP has been selected, then activate if messagebox value is True
        try:
            print("Selected GP ID: ", selected_gpid)
        except:
            messagebox.showerror('Error', 'Click on the GP you would like to activate')
        else:
            result = messagebox.askokcancel('Activate GP', 'Are you sure you would like to activate this GP?')
            if result == True:
                db.gp_activate(selected_gpid)
                admin_gp_listbox.delete(0, END)
                for row in db.fetch_gp():
                    admin_gp_listbox.insert(END, "GP ID: {} FIRST NAME: {} LAST NAME: {} USERNAME: {} STATUS: {}".format(row[0], row[3], row[4], row[1], row[5]))

    def gp_availability(self, cont):
        # Check if GP has been selected, then show GP window with availability of selected GP
        try:
            print("Selected GP ID: ", selected_gpid)
        except:
            messagebox.showerror('Error', 'Please select a GP.')
        else:
            view = Toplevel(self)
            view.wm_title("GP Availability")
            view.wm_minsize(width=100, height=250)

            Label(view, text="GP Availability", font = heading2).grid(row=1,column=0, sticky=W, padx=30, pady=10)
            gp_av_listbox = Listbox(view, height = 10, width = 30, exportselection=0)
            gp_av_listbox.grid(row=2, column=0, padx=33, sticky=W, rowspan = 10, columnspan=3)

            gp_av_listbox.delete(0, END)
            for row in db.fetch_gp_availability(selected_gpid):
                gp_av_listbox.insert(END, "DATE: {} TIME: {}".format(row[0], row[1]))

class Admin_ManagePatients(Frame):   
    
    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        title = Label(self, text="Manage Patients", font = heading1).grid(row=0,column=0, padx=30, sticky=W, pady=20)

        # Insert all patient details into a box 
        global admin_pat_listbox
        admin_pat_listbox = Listbox(self, height = 30, width = 150, exportselection=0)
        admin_pat_listbox.grid(row=20, column=0, padx=33, sticky=W, rowspan = 10, columnspan=3)

        admin_pat_listbox.delete(0, END)
        for row in db.fetch_all_patients():
            admin_pat_listbox.insert(END, "PATIENT ID {} FIRST NAME: {} LAST NAME: {} DOB: {} EMAIL: {} NUMBER: 0{} STATUS: {}".format(row[0], row[3], row[4], row[5], row[7], row[8], row[9]))

        # Bind selected patient
        def select_patient(event):
            index = admin_pat_listbox.curselection()[0]
            patient_selected = admin_pat_listbox.get(index)
            
            global split_patient_selected
            split_patient_selected = patient_selected.split()

            global patientid
            patientid = int(split_patient_selected[2])
        admin_pat_listbox.bind('<<ListboxSelect>>', select_patient)

        # Buttons 
        confirm_btn = ttk.Button(self, text="Confirm registration", command=lambda: self.confirm_reg())
        confirm_btn.grid(row=31, column=0, padx=30, pady=5, sticky=W)

        delete_btn = ttk.Button(self, text="Delete patient record", command=lambda: self.delete_patient())
        delete_btn.grid(row=33, column=0, padx=30, pady=5, sticky=W)

        update_btn = ttk.Button(self, text="Update patient record", command=lambda: self.update_patient())
        update_btn.grid(row=32, column=0, padx=30, pady=5, sticky=W)

        refresh_btn = ttk.Button(self, text="Get most recent patient records", command=lambda: self.update_table())
        refresh_btn.grid(row=34, column=0, padx=30, pady=5, sticky=W)

        gpportalbtn = ttk.Button(self, text="Back to Admin Portal", command=lambda: controller.show_frame(AdminPortal)).grid(row=35, column=0, sticky=W+E, padx=30, pady=10)
    
    def confirm_reg(self):
        # Check if patient selected, then confirm registration 
        try:
            pat_id = patientid
        except:
            messagebox.showerror("No patient selected", "Select a patient to confirm their registration.")
        else:
            if admin_pat_listbox.curselection():
                confirm_check = messagebox.askokcancel('Register new patient', 'Are you sure you would like to confirm registering this patient?')
                if confirm_check == True:
                    db.patient_confirmation(pat_id)
                    admin_pat_listbox.delete(0, END)
                    for row in db.fetch_all_patients():
                        admin_pat_listbox.insert(END, "PATIENT ID {} FIRST NAME: {} LAST NAME: {} DOB: {} EMAIL: {} NUMBER: 0{} STATUS: {}".format(row[0], row[3], row[4], row[5], row[7], row[8], row[9]))
    
    def delete_patient(self):
        # Check if patient selected, then delete them if messagebox value is True  
        try:
            pat_id = patientid
        except:
            messagebox.showerror("No patient selected", "Select a patient to delete.")
        else:
            if admin_pat_listbox.curselection():
                delete_check = messagebox.askokcancel('Delete patient', 'Are you sure you would like to permanently remove this patient from the database?')
                if delete_check == True:
                    db.delete_patient(pat_id)
                    admin_pat_listbox.delete(0, END)
                    for row in db.fetch_all_patients():
                        admin_pat_listbox.insert(END, "PATIENT ID {} FIRST NAME: {} LAST NAME: {} DOB: {} EMAIL: {} NUMBER: 0{} STATUS: {}".format(row[0], row[3], row[4], row[5], row[7], row[8], row[9]))

    def update_patient(self):
        # Check if patient selected, then update their details  
        try:
            patid = patientid
        except:
            messagebox.showerror("No patient selected", "Select a patient to update their details.")
        else:
            # New window with entry fields with the details of the selected patient pre-filled 
            update = Toplevel(self)
            update.wm_title("Update patient details")
            update.wm_minsize(width=600, height=700)

            Label(update, text="Update patient details", font = heading2).grid(row=1,column=0, sticky=W, padx=30, pady=10)
            Label(update, text="Patient information", font = heading3).grid(row=2,column=0, sticky=W, padx=30)
            
            Label(update, text="First name:", font = body).grid(row=3,column=0, sticky=W, padx=30)
            new_firstname = StringVar()
            firstname_change = Entry(update, textvariable=new_firstname)
            firstname_change.grid(row=3, column=0, sticky=W, padx=110)
            firstname_change.delete(0, END)
            firstname_change.insert(END, split_patient_selected[5])

            Label(update, text="Last name:", font = body).grid(row=4,column=0, sticky=W, padx=30)
            new_lastname = StringVar()
            lastname_change = Entry(update, textvariable=new_lastname)
            lastname_change.grid(row=4, column=0, sticky=W, padx=110)
            lastname_change.delete(0, END)
            lastname_change.insert(END, split_patient_selected[8])

            Label(update, text="Date of birth:", font = body).grid(row=5,column=0, sticky=W, padx=30)
            new_dob = StringVar()
            dob_change = Entry(update, textvariable=new_dob)
            dob_change.grid(row=5, column=0, sticky=W, padx=115)
            dob_change.delete(0, END)
            dob_change.insert(END, split_patient_selected[10])

            Label(update, text="Email:", font = body).grid(row=6,column=0, sticky=W, padx=30)
            new_email = StringVar()
            email_change = Entry(update, textvariable=new_email)
            email_change.grid(row=6, column=0, sticky=W, padx=115)
            email_change.delete(0, END)
            email_change.insert(END, split_patient_selected[12])

            Label(update, text="Number:", font = body).grid(row=7,column=0, sticky=W, padx=30)
            new_number = StringVar()
            number_change = Entry(update, textvariable=new_number)
            number_change.grid(row=7, column=0, sticky=W, padx=115)
            number_change.delete(0, END)
            number_change.insert(END, split_patient_selected[14])

            update_btn = ttk.Button(update, text="Save changes", command=lambda: self.update_patient_info(patid, firstname_change, lastname_change, dob_change, email_change, number_change))
            update_btn.grid(row=8, column=0, sticky=W, padx=30, pady=10)

    def update_patient_info(self, pat_id, firstname, lastname, dob, email, number):
        # Get values from entry fields
        firstname = firstname.get()
        lastname = lastname.get()
        dob = dob.get()
        email = email.get()
        number = number.get()

        # Insert updated values into patient database
        db.update_patient_details(firstname, lastname, dob, email, number, pat_id)
        admin_pat_listbox.delete(0, END)
        for row in db.fetch_all_patients():
            admin_pat_listbox.insert(END, "PATIENT ID {} FIRST NAME: {} LAST NAME: {} DOB: {} EMAIL: {} NUMBER: 0{} STATUS: {}".format(row[0], row[3], row[4], row[5], row[7], row[8], row[9]))
        messagebox.showinfo("Saved", "Changes saved")
    
    def update_table(self):
        # Refresh patient table
        admin_pat_listbox.delete(0, END)
        for row in db.fetch_all_patients():
            admin_pat_listbox.insert(END, "PATIENT ID {} FIRST NAME: {} LAST NAME: {} DOB: {} EMAIL: {} NUMBER: 0{} STATUS: {}".format(row[0], row[3], row[4], row[5], row[7], row[8], row[9]))

# Run programme 
app = HealthSys()
app.mainloop()