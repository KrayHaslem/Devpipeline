import sqlite3
import csv
import datetime


'''
Idea for this file is to be able to import it into main.py and run a manager menu
'''

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
        print('list of all users')
    elif vs_selection == '2':
        first_name = input('Please enter desired search first name. (If none just press enter)\n>')
        last_name = input('Please enter the desired search last name. (If none just press enter.\n>')
elif manager_selection == '2':
    print('Creation Menu')
    print()
    cm_selection = input('''
[1] Add a user.
[2] Add a competency.
[3] Add assessment to competency.
[4] Add assessment result.
    ''')
elif manager_selection == '3':
    print('Update Menu')
    print()
    em_selection = input('''
[1] Update a user's information.
[2] Update a competency.
[3] Update an assessment.
[4] Update an assessment result.
[5] Delete an assessmetn result.
    ''')
elif manager_selection == '4':
    print('CSV Menu')
    print()
    rm_selection = input('''
[1] Export Compentency report CSV by compentency and users
[2] Export Compentency report CSV for single user
[3] Import CSV assessment result
    ''')

else:
    exit()