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

    def edit_user(self,user_columns):
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
                self.first_name = fname
                self.update(cursor)
       
        if update_selection == '2':
            lname = input("New Last Name:\n>")
       
            if lname:
                self.last_name = lname
                self.update(cursor)
       
        if update_selection == '3':
            name = input("New Phone:\n>")
         
            if name:
                self.phone = name
                self.update(cursor)
        
        if update_selection == '4':
            name = input("New email:\n>")
       
            if name:
                self.email = name
                self.update(cursor)
        
        if update_selection == '6':
            name = input("Hire Date: YYYY-MM-DD\n>")
            if name:
                self.hire_date = name
                self.update(cursor)

        if update_selection == '5':
            print("User must set password, but you can reset to default, so user can set new.")
            selection_input = input('Would you like to reset to default? Y/N\n>')
            if selection_input.strip().lower() == 'y':
                reset_pass_sql = 'UPDATE Users SET password = password WHERE user_id = ?'
                user_id = self.user_id
                cursor.execute(reset_pass_sql,(user_id,))
                connection.commit()
                print("Password set to default.")
   
    def update_pass_sql(self,cursor, new_password, email):
        update_sql = '''
        UPDATE Users
        SET password = (?)
        WHERE email = (?);
        '''
        cursor.execute(update_sql, (new_password, email,))
        connection.commit()
    
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
        
    def check_password(self, email, password, cursor):
      password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
      select_sql = 'SELECT email FROM Users WHERE password=? AND email=?;'
    

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
    manager = input('Will this user have manager privileges? Y/N\n>')
    return (first_name,last_name,phone,email,manager)

def collect_comp_info():
    comp_name = input('Input Competency Name: \n>')
    comp_desc = input('Input Competency Description:\n>')
    scale_desc = input('Input any notes for the grading scale here:\n>')
    return (comp_name,comp_desc,scale_desc)

def collect_assessment_info():
    assessment_desc = input('Input Assessment Name:\n>')
    due_date = input('Due Date: YYYY-MM-DD\n>')
    creation_date = today
    available()
    competency_id = input('Input the id of the Compentency:\n>')
    return(assessment_desc,due_date,creation_date,competency_id)

def collect_result_info():
    available_users()
    user = input('Input User ID:\n>')
    available_assessments()
    assessment = input('Input Assessment ID:\n>')
    score = input('Input Score:\n>')
    assessment_date = today
    available_managers()
    manager = input('Input Manager ID if a manager administered. \n If no manager leave blank.\n>')
    if manager:
        return(user,assessment,score,assessment_date,manager)
    else:
        return(user,assessment,score,assessment_date,'')
    
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

def available():
    print('Available Competencies:')
    select_competency = "SELECT competency_id,competency_name FROM Competencies ORDER BY competency_id;"
    rows = cursor.execute(select_competency).fetchall()
    for row in rows:
        print(f'[{row[0]}] {row[1]}')

def available_users():
    print('Available Users:')
    select_user = "SELECT user_id,first_name,last_name FROM Users ORDER BY user_id;"
    rows = cursor.execute(select_user).fetchall()
    for row in rows:
        print(f'[{row[0]}] {row[1]} {row[2]}')

def available_managers():
    print('Available Users:')
    select_user = "SELECT user_id,first_name,last_name FROM Users WHERE user_type = 'M' ORDER BY user_id;"
    rows = cursor.execute(select_user).fetchall()
    for row in rows:
        print(f'[{row[0]}] {row[1]} {row[2]}')

def available_assessments():
    print('Available Assessments:')
    select_user = "SELECT assessment_id,assessment_description FROM Assessments ORDER BY assessment_id;"
    rows = cursor.execute(select_user).fetchall()
    for row in rows:
        print(f'[{row[0]}] {row[1]}')

def available_competency():
    print('Available Competencies:')
    select_user = "SELECT competency_id, competency_name FROM Competencies ORDER BY competency_id;"
    rows = cursor.execute(select_user).fetchall()
    for row in rows:
        print(f'[{row[0]}] {row[1]}')

def competency_detail():
    available()
    select_competency = "SELECT competency_id,competency_name FROM Competencies ORDER BY competency_id;"
    rows = cursor.execute(select_competency).fetchall()
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
        competency_detail()

def manager_menu():
    while True:
            
        print('Manager Menu')
        print('')
        manager_selection = input('''
Please select from the following:

[1] View/Search Submenu. (Looking for info? Try here.)
[2] Creation Submenu. (Do you have something new? Try here.)
[3] Update Submenu (If your goal is updating try here.)
[4] CSV Submenu
Any other input will exit the Manager Menu
>''')
        if manager_selection == '1':
            print('View/Search Menu')
            print()
            vs_selection = input('''
[1] View all users in a list.
[2] Search for user by name.
[3] View all user competencies by user.
[4] View all users competency levels by competency.
[5] View competency report for individual user.
[6] View a list of assessments for individaul user.
>''')
            if vs_selection == '1':
                active = ''
                not_active = ''
                select_sql = 'SELECT user_id, first_name, last_name, active FROM Users'
                rows = cursor.execute(select_sql)
                for row in rows:
                    if row[3]== 1:
                        active += f'[{str(row[0])}] '
                        active += f'{row[1].strip()}, '
                        active += row[2].strip()
                        active += '\n'
                    elif row[3]== 0:
                        not_active += f'[{str(row[0])}] '
                        not_active += f'{row[1].strip()}, '
                        not_active += row[2].strip()
                        not_active += '\n'
                print('Active Users:')
                print(active)
                print('Inactive Users:')
                print(not_active)
                    
            elif vs_selection == '2':
                while True:
                    first_name = input('Please enter desired search first name. (If none just press enter. For all spacebar then enter.)\n>')
                    last_name = input('Please enter the desired search last name. (If none just press enter. For all spacebar then enter.)\n>')
                    if first_name and last_name:
                        active = ''
                        not_active = ''
                        select_sql = 'SELECT user_id, first_name, last_name, active FROM Users WHERE first_name LIKE ? AND last_name LIKE ?'
                        fn_var = f'%{first_name.strip().lower()}%'
                        print(fn_var)
                        ln_var = f'%{last_name.strip().lower()}%'
                        print(ln_var)
                        rows = cursor.execute(select_sql,(fn_var,ln_var,))
                        for row in rows:
                            if row[3]== 1:
                                active += f'[{str(row[0])}] '
                                active += f'{row[1].strip()}, '
                                active += row[2].strip()
                                active += '\n'
                            elif row[3]== 0:
                                not_active += f'[{str(row[0])}] '
                                not_active += f'{row[1].strip()}, '
                                not_active += row[2].strip()
                                not_active += '\n'
                        print('Active Users:')
                        print(active)
                        print('Inactive Users:')
                        print(not_active)
                    if first_name:
                        active = ''
                        not_active = ''
                        select_sql = 'SELECT user_id, first_name, last_name, active FROM Users WHERE first_name LIKE ?'
                        fn_var = f'%{first_name.strip().lower()}%'
                        rows = cursor.execute(select_sql,(fn_var,))
                        for row in rows:
                            if row[3]== 1:
                                active += f'[{str(row[0])}] '
                                active += f'{row[1].strip()}, '
                                active += row[2].strip()
                                active += '\n'
                            elif row[3]== 0:
                                not_active += f'[{str(row[0])}] '
                                not_active += f'{row[1].strip()}, '
                                not_active += row[2].strip()
                                not_active += '\n'
                        print('Active Users:')
                        print(active)
                        print('Inactive Users:')
                        print(not_active)
                    if last_name:
                        active = ''
                        not_active = ''
                        select_sql = 'SELECT user_id, first_name, last_name, active FROM Users WHERE last_name LIKE ?'
                        ln_var = f'%{last_name.strip().lower()}%'
                        print(ln_var)
                        rows = cursor.execute(select_sql,(ln_var,))
                        for row in rows:
                            if row[3]== 1:
                                active += f'[{str(row[0])}] '
                                active += f'{row[1].strip()}, '
                                active += row[2].strip()
                                active += '\n'
                            elif row[3]== 0:
                                not_active += f'[{str(row[0])}] '
                                not_active += f'{row[1].strip()}, '
                                not_active += row[2].strip()
                                not_active += '\n'
                        print('Active Users:')
                        print(active)
                        print('Inactive Users:')
                        print(not_active)
                    continue_input = input('Search again? Y/N\n>')
                    if continue_input.lower() == 'y':
                        continue
                    else:
                        break
            elif vs_selection == '3':
                try:
                    comp_user = int(input('Which user id would you like to see competencies for?(This is the number in [#] on the search and view all lists.\nPress enter to return to the previous menu to search for user id.\n>'))
                    sql_find_email = 'SELECT email FROM users WHERE user_id = ?'
                    row = cursor.execute(sql_find_email, (comp_user,)).fetchone()
                    email = row[0]
                    competency_summary(email)
                except:
                    print("Invalid selection try searching your desired id # and try again.")
            elif vs_selection == '4':
                competency_detail()

            elif vs_selection == '5':
                try:
                    comp_user = int(input('Which user id would you like to see competencies for?(This is the number in [#] on the search and view all lists.\nPress enter to return to the previous menu to search for user id.\n>'))
                    sql_find_email = 'SELECT email FROM users WHERE user_id = ?'
                    row = cursor.execute(sql_find_email, (comp_user,)).fetchone()
                    email = row[0]
                    sql_comp_level_report = 'SELECT competency_name, score FROM Users u, AssessmentResults ar, Competencies c, Assessments a WHERE u.user_id = ar.user AND c.competency_id =  a.competency_id AND a.assessment_id = ar.assessment AND u.email = ?; '
                    rows = cursor.execute(sql_comp_level_report,(email,)).fetchall()
                    print('Competency Report')
                    for row in rows:
                        print(f'{row[0]:<30}', 'Score: ',row[1])


                except:
                    print("Invalid selection try searching your desired id # and try again.")
            
            elif vs_selection == '6':
                try:
                    comp_user = int(input('Which user id would you like to see assessments for?(This is the number in [#] on the search and view all lists.\nPress enter to return to the previous menu to search for user id.\n>'))
                    sql_find_email = 'SELECT email FROM users WHERE user_id = ?'
                    row = cursor.execute(sql_find_email, (comp_user,)).fetchone()
                    email = row[0]
                    sql_comp_level_report = 'SELECT assessment_description, score FROM Users u, AssessmentResults ar, Competencies c, Assessments a WHERE u.user_id = ar.user AND c.competency_id =  a.competency_id AND a.assessment_id = ar.assessment AND u.email = ?; '
                    rows = cursor.execute(sql_comp_level_report,(email,)).fetchall()
                    print('Assessment Report')
                    for row in rows:
                        print(f'{row[0]:<30}', 'Score: ',row[1])


                except:
                    print("Invalid selection try searching your desired id # and try again.")
            

        elif manager_selection == '2':
            print('Creation Menu')
            print()
            cm_selection = input('''
[1] Add a user.
[2] Add a competency.
[3] Add assessment to competency.
[4] Add assessment result.
>''')
            if cm_selection == '1':
                new_user = collect_info() #(first_name,last_name,phone,email,manager)
                manager_val = 'U'
                if new_user[-1].strip().lower() == 'y':
                    manager_val = 'M'
                sql_values = (new_user[0],new_user[1],new_user[2],new_user[3],today,manager_val)
                new_user_sql = "INSERT INTO Users (first_name, last_name, phone, email, date_created, user_type) VALUES (?,?,?,?,?,?)"
                connection.execute(new_user_sql,sql_values)
                connection.commit()
            elif cm_selection == '2':
                new_competency = collect_comp_info()
                sql_values = (new_competency[0],new_competency[1],new_competency[2])
                new_comp_sql = "INSERT INTO Competencies (competency_name, competency_description, scale_notes) VALUES (?,?,?)"
                connection.execute(new_comp_sql,sql_values)
                connection.commit()
            elif cm_selection == '3':
                new_assessment = collect_assessment_info()
                sql_values = (new_assessment[0],new_assessment[1],new_assessment[2],new_assessment[3])
                new_assessment_sql = "INSERT INTO Assessments (assessment_description, due_date, creation_date, competency_id) VALUES (?,?,?,?)"
                connection.execute(new_assessment_sql,sql_values)
                connection.commit()
            elif cm_selection == '4':
                new_result = collect_result_info()
                sql_values = (new_result[0],new_result[1],new_result[2],new_result[3],new_result[4])
                new_ar_sql = "INSERT INTO AssessmentResults (user,assessment,score,assessment_date,manager) VALUES (?,?,?,?,?)"
                connection.execute(new_ar_sql,sql_values)
                connection.commit()

        elif manager_selection == '3':
            print('Update Menu')
            print()
            em_selection = input('''
[1] Update a user's information.
[2] Update a competency.
[3] Update an assessment.
[4] Update an assessment result.
[5] Delete an assessmetn result.
>''')
            if em_selection == '1':
                available_users()
                u_id = int(input("Input User ID to update:\n>"))
                find_email_sql = 'SELECT email FROM Users WHERE user_id = ?'
                row = cursor.execute(find_email_sql,(u_id,)).fetchone()
                u_email  = row[0]
                update_user = Users()
                set_user_str = load(cursor,u_email)
                update_user_list = []
                for i in set_user_str.split(','):
                    update_user_list.append(i)
                set_user_tuple = tuple(update_user_list)
                update_user.set_all(set_user_tuple[0],set_user_tuple[1],set_user_tuple[2],set_user_tuple[3],set_user_tuple[4],set_user_tuple[5],set_user_tuple[6],set_user_tuple[7],set_user_tuple[8],set_user_tuple[9])
                update_user.edit_user(user_columns)
                
            elif em_selection == '2':
                available_competency()
                c_id = int(input("Input Competency ID to update:\n>"))
                comp_columns = ['competency_id','competency_name','competency_description','scale_notes']
                update_comp_sql = "SELECT * FROM Competencies WHERE competency_id = ?"
                row = connection.execute(update_comp_sql,(c_id,)).fetchone()
                for key,value in enumerate(row):
                    print(f'[{key}] {comp_columns[key]} {value}')
                update_what = int(input('Please enter the ID of the value you would like to update.\n>'))
                with_what = input('Please input the new value:\n>')
                competency_update_sql = "UPDATE Competencies SET ? = ? WHERE competency_id = ?"
                connection.execute(competency_update_sql,(comp_columns[update_what],with_what,c_id,))
                connection.commit()

            elif em_selection == '3':
                available_assessments()
                a_id = input("Input Assessment ID to update:\n>")
                assess_columns = ['assessment_id','assessment_description','due_date','creation_date','competency_id']
                update_assess_sql = "SELECT * FROM Assessments WHERE assessment_id = ?"
                row = connection.execute(update_assess_sql,(a_id,)).fetchone()
                for key,value in enumerate(row):
                    print(f'[{key}] {assess_columns[key]} {value}')
                update_what = int(input('Please enter the ID of the value you would like to update.\n>'))
                if update_what == 4:
                    available_competency()
                with_what = input('Please input the new value:\n>')
                competency_update_sql = "UPDATE Assesments SET ? = ? WHERE assesment_id = ?"
                connection.execute(competency_update_sql,(comp_columns[update_what],with_what,c_id,))
                connection.commit()
            
            elif em_selection == '4':
                available_users()
                u_id = int(input("Input User ID of User that has Assessment to Update:\n>"))
                ar_sql = 'SELECT result_id,assessment_description,score,assessment_date,manager FROM AssessmentResults ar, Assessments a WHERE a.assessment_id = ar.assessment AND user = ?'
                rows = cursor.execute(ar_sql,(u_id,)).fetchall()
                for key,row in enumerate(rows):
                    print(f'[{key}]. {row}')
                selected_ar = int(input('Which assessment from the list above would you like to update?\n>'))
                ar_info = rows[selected_ar]
                selected_ar_update = int(input(f'''
Your assessment is currently:
Result ID: {ar_info[0]}
[1]Assessment: {ar_info[1]}
[2]Score: {ar_info[2]}
[3]Assessment Date: {ar_info[3]}
[4]Manager ID: {ar_info[4]}
Select the ID of field to update:
>
'''))
                if selected_ar_update == 1:
                    available_assessments()
                    new_assessment = int(input('What assessment would you like to re-assign this result?'))
                    update_sql = 'UPDATE AssessmentResults SET assessment = ? WHERE result_id = ?'
                    cursor.execute(update_sql,(new_assessment,ar_info[0],))
                    connection.commit()
                elif selected_ar_update == 2:
                    new_score = input('Input the updated score:\n>')
                    update_sql = 'UPDATE AssessmentResults SET score = ? WHERE result_id = ?'
                    cursor.execute(update_sql,(new_score,ar_info[0],))
                    connection.commit()
                elif selected_ar_update == 3:
                    available_managers()
                    new_manager = input('Input the ID of new manager:\n>')
                    update_sql = 'UPDATE AssessmentResults SET manager = ? WHERE result_id = ?'
                    cursor.execute(update_sql,(new_manager,ar_info[0],))
                    connection.commit()
                else:
                    continue


        elif manager_selection == '4':
            print('CSV Menu')
            print()
            rm_selection = input('''
[1] Export Competency report CSV by competency and users
[2] Export Competency report CSV for single user
[3] Import CSV assessment result
>''')
            if int(rm_selection) == 1:
                available_competency()
                comp_export = input('Input the competency ID to export:\n>')
                header = ['Name','Competency Score','Assessment','Date Taken']
                rows = []
                rows_sql = "SELECT first_name || ' ' || last_name, score, assessment_description,assessment_date FROM Users u, AssessmentResults ar, Competencies c, Assessments a WHERE u.user_id = ar.user AND c.competency_id =  a.competency_id AND a.assessment_id = ar.assessment AND c.competency_id = ?"
                rows_iter = cursor.execute(rows_sql,((int(comp_export)),)).fetchall()
                for row in rows_iter:
                    rows.append(row)
                    
                with open("CompetencyResultsSummary.csv", 'w', newline='') as outfile:
                    wrt = csv.writer(outfile)
                    wrt.writerow(header)
                    wrt.writerows(rows)
                    
                print('Competenvy Results Summary Created.')

            if int(rm_selection) == 2:
                available_users()
                user_report = input('Input the User ID to export:\n>')
                id_header = ['Name','Email','Average Competency Score']
                id_row = []
                rows_sql = "SELECT first_name || ' ' || last_name, email, AVG(score) FROM Users u, AssessmentResults ar WHERE u.user_id = ar.user AND user_id = ?"
                rows_iter = cursor.execute(rows_sql,(int(user_report),)).fetchall()
                for row in rows_iter:
                    id_row.append(row)
                header = ['Competency','Score','Date']
                rows = []
                sql_competency = "SELECT Competencies.competency_name,  AssessmentResults.score, MAX(AssessmentResults.assessment_date) FROM Competencies INNER JOIN Assessments ON Competencies.competency_id = Assessments.competency_id INNER JOIN AssessmentResults ON Assessments.assessment_id = AssessmentResults.assessment WHERE AssessmentResults.user = ? GROUP BY Competencies.competency_name;"    
                iter_rows = cursor.execute(sql_competency,(int(user_report),))
                with open("UserCompetencySummary.csv", 'w', newline='') as outfile:
                    wrt = csv.writer(outfile)
                    wrt.writerow(id_header)
                    wrt.writerow(id_row)
                    wrt.writerow(header)
                    wrt.writerows(iter_rows)
                print('User Competenvy Summary Created.')
               
            elif int(rm_selection) == 3:
                file_name = input('Input the file name to import:\n>')
                with open(f'{file_name}','r') as csvfile:
                    csvreader = csv.reader(csvfile)
                    fields = next(csvreader)
                    results = []
                    for row in csvreader:
                        results.append(row)
                    for row in results:
                        new_ar_sql = "INSERT INTO AssessmentResults (user,assessment,score,assessment_date,manager) VALUES (?,?,?,?,?)"
                        connection.execute(new_ar_sql,(row[0],row[1],row[2],row[3],row[4],))
                        connection.commit()
                    print('Added Assessment Results')                      
        else:
            break

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
                manager_menu()                 

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
    if maybe != False:    #possibly just do# if maybe:                  
        logged_user_str = load(cursor,user_email)
        logged_user_tuple = []
        reset_var = 0
        for i in logged_user_str.split(','):
            logged_user_tuple.append(i)
        logged_user_tuple = tuple(logged_user_tuple)
        logged_user = Users()
        logged_user.set_all(logged_user_tuple[0],logged_user_tuple[1],logged_user_tuple[2],logged_user_tuple[3],logged_user_tuple[4],logged_user_tuple[5],logged_user_tuple[6],logged_user_tuple[7],logged_user_tuple[8],logged_user_tuple[9])
        check_default_password() 
        try:
            run_menu()
        except:
            print("Sorry that seemed to cause an issue. Try again.")
            run_menu()