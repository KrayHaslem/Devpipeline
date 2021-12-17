import sqlite3
import csv
import datetime
import bcrypt

class Competency:
    def __init__(self, competency_id, competency_name, competency_description, scale_notes):
        self.competency_id = competency_id
        self.competency_name = competency_name
        self.competency_description = competency_description
        self.scale_notes = scale_notes

class Users:
    def __init__(self):
        self.user_id = None 
        self.first_name = None 
        self.last_name = None 
        self.phone = None 
        self.email = None 
        self.__password = None
        self.active = None 
        self.date_created = None
        self.hire_date = None
        self.user_type = None
        self.salt = b'$2b$12$V62jpTY0AjTqpqoJn.WjW.'

    def set_all(self,user_id,first_name,last_name,phone,email,password,active,date_created,hire_date,user_type):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.__password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        self.active = active
        self.date_created = date_created
        self.hire_date = hire_date
        self.user_type = user_type

    # def save(self, cursor):
    #     insert_sql = '''
    #     INSERT INTO Users (first_name, last_name, phone, email, password, date_created, hire_date,user_type)
    #     VALUES (?,?,?,?,?,?,?,?)
    #     ;'''
    #     cursor.execute(insert_sql,(self.first_name,self.last_name,self.phone,self.email,self.__password,today,self.hire_date,self.user_type))
    #     cursor.connection.commit()

    def update(self, cursor):
        update_sql = '''
        UPDATE Users
        SET first_name=?, last_name=?, phone=?, email=?, date_created=?, hire_date=? ,user_type =?
        WHERE user_id = ?
        ;'''
        cursor.execute(update_sql,(self.first_name,self.last_name,self.phone,self.email,self.date_created,self.hire_date,self.user_type,self.user_id))
        cursor.connection.commit()

    def edit(self,user_columns):
        self.print_user_info()
        for key,value in enumerate(user_columns):
            print(f'[{key +1}] {value}')

        while True:
            update_selection = input('Please enter the number ID for the value to update or enter nothing to return to main menu.\n>')

            try:

                if update_selection == '':
                    break

                if int(update_selection) > 0 and int(update_selection) <= len(user_columns):
                    reset_var = int(update_selection)
                    break

            except:
                print('That selection is invalid, please enter a number.')
                continue
       
        if update_selection == '1':
            fname = input("New First Name:\n>")
       
            if fname:
                logged_user.first_name = fname
                logged_user.update(cursor)
       
        if update_selection == '2':
            lname = input("New Last Name:\n>")
       
            if lname:
                logged_user.last_name = lname
                logged_user.update(cursor)
       
        if update_selection == '3':
            name = input("New Phone:\n>")
         
            if name:
                logged_user.phone = name
                logged_user.update(cursor)
        
        if update_selection == '4':
            name = input("New email:\n>")
       
            if name:
                logged_user.email = name
                logged_user.update(cursor)
        
        if update_selection == '6':
            name = input("Hire Date: YYYY-MM-DD\n>")
            if name:
                logged_user.hire_date = name
                logged_user.update(cursor)

        if update_selection == '5':
            while True:
                new_password = input("Please input a secure password:\n>")
                verify_password = input("Please re-enter the same password:\n>")

                if new_password == verify_password:
                    bcrypt_password = bcrypt.hashpw(new_password.encode('utf-8'),logged_user.salt)
                    logged_user.update_pass_sql(cursor,bcrypt_password,user_email)
                    break
                else:
                    print("Unfortunately, your passwords did not match.\nTry again.")
                    continue

    # def change_password(self, new_password):
    #   if new_password:
    #      self.__password = bcrypt.hashpw(new_password.encode('utf-8'), self.salt)
    #      encoded_password = bcrypt.hashpw(new_password.encode('utf-8'), self.salt)
    #      self.update_pass_sql(cursor,encoded_password,self.email,)
   
    def update_pass_sql(self,cursor, new_password, email):
        update_sql = '''
        UPDATE Users
        SET password = (?)
        WHERE email = (?);
        '''
        cursor.execute(update_sql, (new_password, email,))
        connection.commit()

    # def change_email(self,new_email):
    #     self.email = new_email
    
    def print_user_info(self):
        print(f'{self.first_name}{self.last_name}')
        print(f'Phone: {self.phone}')
        print(f'Email: {self.email}')
        print(f'Hire Date: {self.hire_date}')
        print(f'User Created: {self.date_created}')

    def print_user_competency_summary(self,user_id,cursor):
        print(f'Name : {self.last_name},{self.first_name}')
        sql_competency = "SELECT Competencies.competency_name,  AssessmentResults.score, MAX(AssessmentResults.assessment_date) FROM Competencies INNER JOIN Assessments ON Competencies.competency_id = Assessments.competency_id INNER JOIN AssessmentResults ON Assessments.assessment_id = AssessmentResults.assessment WHERE AssessmentResults.user = ? GROUP BY Competencies.competency_name;"
        rows = cursor.execute(sql_competency,user_id)
        print(f'Competency                      Score     Date Taken')
        for row in rows:
            print(f'{row[0]:<35} {row[1]:<5} {row[2]}')

    # def load(self,cursor):
    #     select_sql = '''
    #     SELECT * FROM USERS WHERE user_id=?;
    #     '''
    #     row = cursor.execute(select_sql, (self.user_id,)).fetchone()
        
    def check_password(self, email, password, cursor):
      password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
      select_sql = '''
         SELECT email FROM Users WHERE password=? AND email=?
      ;'''
    

      row = cursor.execute(select_sql, (password, email)).fetchone()
      return (row != None)

#pulls available emails and appends them to email_list from the DB to check against input for proper credentials
def pull_emails():
    query = 'SELECT email FROM Users WHERE active = 1;'
    rows = cursor.execute(query).fetchall()
    for row in rows:
        email_list.append(row[0])

def collect_info():
    first_name = input('Input your first name: TEXT\n>')
    last_name = input('Input your first name: TEXT\n>')
    phone = input('Input your phone number: TEXT\n>')
    email = input('Input your contact email: TEXT\n>')
    return (first_name,last_name,phone,email)

# def read_infile():
#     with open('infile.csv','r') as data:
#         csv_reader = csv.reader(data)
#         for line in csv_reader:
#             print(line)

# def output_csv():
#     with open('output.csv', 'w') as csvfile:
#         fields = ['first_name', 'last_name']#, additionalcode]
#         writer = csv.DictWriter(csvfile, fieldnames=fields)
#         writer.writeheader()
#         writer.writerow({'first_name': 'John', 'last_name':'Smith'})#, 'additionalcode' :'Value'})

def initialize_database(cursor):
    with open('schema.sql') as sql_file:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
    connection.commit()    

def load(cursor,user_email):
    user_email = user_email.strip()
    select_query = 'SELECT * FROM Users WHERE email = (?)'
    row = cursor.execute(select_query,(user_email,)).fetchone()
    if not row:
         print("NOTHING RETURNED")
         return
    ind_id = row[0]
    ind_first_name = row[1]
    ind_last_name = row[2]
    ind_phone = row[3]
    ind_email = row[4]
    ind_password = row[5]
    ind_active = row[6]
    ind_date_created = row[7]
    ind_date_hired = row[8]
    ind_type = row[9]
    logged_user_str =  f'{ind_id}, {ind_first_name}, {ind_last_name}, {ind_phone}, {ind_email}, {ind_password}, {ind_active}, {ind_date_created}, {ind_date_hired}, {ind_type}'
    return logged_user_str

def test_mail_login(user_email):
    if email_list == []:
        print("Welcome to setup.\n The Database is empty and that has put you in the setup process.\n To start please login using \"admin\" as the login email credential.\nThe default password for admin for this initial setup is \"adminpw\".\nLogin to admin, create yourself as a user, login to your new created user.\nDELETE ADMIN USER! THIS MUST BE DONE BEFORE COMPANY WIDE IMPLEMENTATION!")
        empty_db_sql = 'INSERT INTO Users (first_name, email, password, user_type) VALUES (?,?,?,?)'
        values = ('admin','admin','adminpw','M')
        cursor.execute(empty_db_sql, values)
        connection.commit()
        pull_emails()
    while user_email not in email_list:
        print('Please try again. Email not found.')
        return False

def check_default_password():
    while True:
        if logged_user_tuple[5].strip() == 'password':
            new_password = input("New user, please input a secure password:\n>")
            verify_password = input("Please re-enter the same password:\n>")

            if new_password == verify_password:
                bcrypt_password = bcrypt.hashpw(new_password.encode('utf-8'),logged_user.salt)
                logged_user.update_pass_sql(cursor,bcrypt_password,user_email)
                break
            else:
                print("Unfortunately, your passwords did not match.\nTry again.")
                continue
        else:
            break

def select_user(email):
    user_load = load(cursor,email)
    user_tuple = []
    for i in user_load.split(','):
        user_tuple.append(i)
    user_tuple = tuple(user_tuple)
    selected_user = Users()
    selected_user.set_all(user_tuple[0],user_tuple[1],user_tuple[2],user_tuple[3],user_tuple[4],user_tuple[5],user_tuple[6],user_tuple[7],user_tuple[8],user_tuple[9])
    pass_id = selected_user.user_id
    selected_user.print_user_competency_summary(pass_id,cursor)

def competency_summary(email):
    print('Competency Summary:')
    competency_user = select_user(email)
    
def user_assessment_menu():
    assessment_input  = input("""
Welcome to the Assessment Menu 
Please select from the following:
[1]View Personal Competency Summary
[2]View Competency Results Summary
Any additional input for Main Menu
>""")
    if assessment_input == '1':
        email = logged_user.email
        competency_summary(email)
    elif assessment_input == '2':
        print('Available for competency detail:')
        select_competency = "SELECT competency_id,competency_name FROM Competencies ORDER BY competency_id;"
        rows = cursor.execute(select_competency).fetchall()
        for row in rows:
            print(f'[{row[0]}] {row[1]}')
        input_var = ''
        while True:
            competency_selection = input('Provide the numerical ID above for the desired competency\n>')
            try:
                if int(competency_selection) <= len(rows) and int(competency_selection) > 0:
                    input_var += competency_selection
                    break
                else:
                    print("That doesn't seem to be a valid integer, please try again.")

            except:
                print('Your selection does not seem to be valid, please enter a number corresponding to a competency.')
                continue
        sql_competency = "SELECT Competencies.competency_name,  AVG(AssessmentResults.score) FROM Competencies INNER JOIN Assessments ON Competencies.competency_id = Assessments.competency_id INNER JOIN AssessmentResults ON Assessments.assessment_id = AssessmentResults.assessment WHERE Competencies.competency_id = ? GROUP BY Competencies.competency_name;"
        rows = cursor.execute(sql_competency,(input_var,))
        for row in rows:
            print('Topic:',row[0],'Average Score for all users:',row[1])

        sql_report = "SELECT Users.first_name, Users.last_name , AssessmentResults.score, Assessments.assessment_description, Competencies.competency_name FROM Competencies INNER JOIN Assessments ON Competencies.competency_id = Assessments.competency_id INNER JOIN AssessmentResults ON Assessments.assessment_id = AssessmentResults.assessment INNER JOIN Users ON Users.user_id  = AssessmentResults.user WHERE Competencies.competency_id = ? AND AssessmentResults.user = ?;"
        rows = cursor.execute(sql_report,(input_var,logged_user.user_id,))
        for row in rows:
            print(f'Name:{row[0]} {row[1]}')
            print(f'Latest Score: {row[2]}. Assessment Taken: {row[3]}.')

def managment_assessment_menu():
    assessment_input  = input("""
Welcome to the Assessment Menu 
Please select from the following:
[1]View Personal Competency Summary
[2]View Competency Results Summary
Any additional input for Main Menu
>""")
    if assessment_input == '1':
        email = logged_user.email
        competency_summary(email)
    elif assessment_input == '2':
        print('Available for competency detail:')
        select_competency = "SELECT competency_id,competency_name FROM Competencies ORDER BY competency_id;"
        rows = cursor.execute(select_competency).fetchall()
        for row in rows:
            print(f'[{row[0]}] {row[1]}')
        input_var = ''
        while True:
            competency_selection = input('Provide the numerical ID above for the desired competency\n>')
            try:
                if int(competency_selection) <= len(rows) and int(competency_selection) > 0:
                    input_var += competency_selection
                    break
                else:
                    print("That doesn't seem to be a valid integer, please try again.")

            except:
                print('Your selection does not seem to be valid, please enter a number corresponding to a competency.')
                continue
        sql_competency = "SELECT Competencies.competency_name,  AVG(AssessmentResults.score) FROM Competencies INNER JOIN Assessments ON Competencies.competency_id = Assessments.competency_id INNER JOIN AssessmentResults ON Assessments.assessment_id = AssessmentResults.assessment WHERE Competencies.competency_id = ? GROUP BY Competencies.competency_name;"
        rows = cursor.execute(sql_competency,(input_var,))
        for row in rows:
            print('Topic:',row[0],'Average Score for all users:',row[1])

        sql_report = "SELECT Users.first_name, Users.last_name , AssessmentResults.score, Assessments.assessment_description, Competencies.competency_name FROM Competencies INNER JOIN Assessments ON Competencies.competency_id = Assessments.competency_id INNER JOIN AssessmentResults ON Assessments.assessment_id = AssessmentResults.assessment INNER JOIN Users ON Users.user_id  = AssessmentResults.user WHERE Competencies.competency_id = ? GROUP BY Users.user_id;"
        rows = cursor.execute(sql_report,(input_var,))
        for row in rows:
            print(f'Name:{row[0]} {row[1]}')
            print(f'Latest Score: {row[2]}. Assessment Taken: {row[3]}.')

def run_menu():
    while True:
        password = input('Please enter your password:\n>')
        result = logged_user.check_password(user_email,password,cursor)
        if result:
            print('Login Success')
            break
        else:
            print("Login failed try again.")      

    while True:
        print('Main Menu')
        if logged_user.user_type.strip() == 'M':
            manager_option = input("""
Select one of the following:
[1]View assessment data
[2]Edit your user information
[3]Manager Menu
[0]Logout
[Q]Quit the application
> """)
            if manager_option.lower() == 'q':
                quit()
            elif manager_option.lower() == '0':
                break #This will allow the user to be logged out.
            elif manager_option.lower() == '1':
                managment_assessment_menu()
            elif manager_option.lower() == '2':
                logged_user.edit(user_columns)
            elif manager_option.strip() == '3':
                print("Hello World Line 381") 
                
                
                

        elif logged_user.user_type.strip() == 'U':
            user_option = input("""
    Select one of the following:
    [1]View your assessment data
    [2]Edit your user information
    [0]Logout 
    [Q]Quit the application
    >""")
            if user_option.lower() == 'q':
                quit()
            elif user_option.lower() == '0':
                break #This will allow the user to be logged out.
            elif user_option.lower() == '1':
                user_assessment_menu()
            elif user_option.lower() == '2':
                logged_user.edit(user_columns)    

today = str(datetime.date.today())
email_list = []
connection = sqlite3.connect('capstone.db')
cursor = connection.cursor()
user_columns = ['first_name','last_name','phone','email','password','hire_date','user_type']
print("\nWelcome to the Competency Tracking Tool\n")

initialize_database(cursor) #Creates a DB if none exists
pull_emails() #Compare to input to see if user is valid
while True: #this is the program's while loop that goes until exit program selection
    user_email = input("Please enter your login email: TEXT\n>") #Get the email
    test_mail_login(user_email)
    maybe = test_mail_login(user_email)
    if maybe != False:    
        logged_user_str = load(cursor,user_email)
        logged_user_tuple = []
        reset_var = 0
        for i in logged_user_str.split(','):
            logged_user_tuple.append(i)
        logged_user_tuple = tuple(logged_user_tuple)
        logged_user = Users()
        logged_user.set_all(logged_user_tuple[0],logged_user_tuple[1],logged_user_tuple[2],logged_user_tuple[3],logged_user_tuple[4],logged_user_tuple[5],logged_user_tuple[6],logged_user_tuple[7],logged_user_tuple[8],logged_user_tuple[9])
        check_default_password() 
        run_menu()