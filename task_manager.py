import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Read tasks from file
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}
    # Save tasks as a list and split them by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#function for user registration#
def reg_user(a):  #a is userinput
    '''This function take userinput and check if the name has already in use, 
    and only do password confirmation after ensure the name is not in use.'''
    user_avaliable=False  
    while not user_avaliable: #check if username exited
        if a in username_password.keys():
            print("This user name is taken, please use other name.")
            a = input("New Username: ")
            continue
        elif a not in username_password.keys():
            print("User name accepted!")
            user_avaliable=True
          
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            with open("user.txt", "w+") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
        else:
            print("Passwords do no match")
#function reg_user end#
#function for add task#
def add_task(a): # a is username
    '''This fuction take username and task details and save it to task.txt.'''
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
            "username": a,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")
#function end#
#function for view mine #
#sub-function for VM : mark as completed
def mark_completed(a): # a is task_selected(int)
    '''This fuction take the userinput number (task_selected) and username to find the task which user wish to change,
    and change the completed to true, then save it back to task list.'''
    tasknum=0
    mark_as_complete={}
    j=""
    for i in range (len(task_list)):
        if task_list[i]['username']==curr_user:
            tasknum+=1
            if tasknum==a:
                j=int(i)
                mark_as_complete=task_list[j]
    mark_as_complete['completed']=True

    task_list[j]=mark_as_complete
#=================================================
#sub-function for VM : editing tasks
def edit_task(a): #a is task selected
    '''This function let user edit taskowner and due date, then save it back to task list.'''
    tasknum=0
    edit_item={}
    j=""
    for i in range (len(task_list)):
        if task_list[i]['username']==curr_user:
            tasknum+=1
            if tasknum==a:
                j=int(i)
                edit_item=task_list[j]
    edit_item['username']= input("Please input taskowner: ")
    while True:
        try:
            edit_item['due_date']= datetime.strptime(input("New due date of task (YYYY-MM-DD): "), DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")    
    task_list[j]=edit_item
#============================================
#sub-function for VM : write back
def writeback():
    '''This function write the tasks back to task.txt.'''
    task_item=[]
    content_to_write=""
    for i in range (len(task_list)):
        content_to_write=task_list[i]['username']+";"
        content_to_write+=task_list[i]['title']+";"
        content_to_write+=task_list[i]['description']+";"
        content_to_write+=task_list[i]['due_date'].strftime(DATETIME_STRING_FORMAT)+";"
        content_to_write+=task_list[i]['assigned_date'].strftime(DATETIME_STRING_FORMAT)+";"
        content_to_write+= "Yes"if task_list[i]['completed'] else "No"
        task_item.append(content_to_write)
        content_to_write=""

    with open ("tasks.txt","w+")as file:
        for i in task_item:
            file.write("%s\n"% i)
#=================================================
def view_mine(a): #a is task_list
    '''This function contains functions (mark_completed, edit_task and writeback), 
    it allows users to choose the task they are assigned and see if they wish to mark as complete or edit task,
     then save it back to task.txt.'''
    tasknum=0
    for t in a:
        if t['username'] == curr_user:
            tasknum+=1
            disp_str = f"Task {tasknum}: \t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            if t['completed'] == False:
                disp_str += f"Completion: 'No' \n"
            else:
                disp_str += f"Completion: 'Yes' \n"
            print(disp_str)
    task_selected=int(input("Please insert numer to select the task you would like to change or insert '-1' to go back to main menu \n"))
    if task_selected==-1:
        print("Back to main menu.")
    elif task_selected in range (tasknum+1):   
        while True:
            try:
                choose=int(input('''What would you like to do?  
 1. Mark as complete  
 2. Edit task  
     Please select 1 or 2 \n'''))
                #Mark as completed
                if choose==1:
                    mark_completed(task_selected)
                    writeback()
                    print("Updated successfully!")
                    break
                #Editing tasks
                elif choose==2:
                    tasknum=0
                    check={}
                    for i in range (len(task_list)):
                        if task_list[i]['username']==curr_user:
                            tasknum+=1
                            if tasknum==task_selected:
                                check=task_list[i]
                    while True:
                        try:
                            if check['completed']==True:
                                print("This task is already completed, you can't change it.")
                                break
                            elif check['completed']==False:
                                edit_task(task_selected)
                                writeback()
                                print("Updated successfully!")
                                break
                        except ValueError:
                            print("Something went wrong.")  
                    break
                else:
                    print("Wrong value!")
            #Task selected out of scope
            except ValueError:
                print("The task you choose dose not exist.")
    else:
        print("Error! Please put in CORRECT NUMER!")
#function end
#function for generate task overview
def task_overview(a):#a is task_list
    '''This function provide a aummary of tasks in task_overview.txt. '''
    total_task=len(a)
    complete=0
    uncomplete=0
    overdue=0
    for i in range (len(a)):
        if a[i]['completed'] == True:
            complete+=1
        else:
            uncomplete+=1
            if (a[i]['completed']== False) and (a[i]['due_date'] < today):
                overdue+=1
    content_to_write=""
    content_to_write+=f"The total number of tasks: {total_task}"+"\n"
    content_to_write+=f"The number of tasks completed: {complete}"+"\n"
    content_to_write+=f"The number of tasks uncomplete: {uncomplete}"+"\n"
    content_to_write+=f"The number of tasks uncomplete and over due: {overdue}"+"\n"
    content_to_write+=f"The percentage of incomplete tasks: {uncomplete/total_task*100} %"+"\n"
    content_to_write+=f"The percentage of tasks overdue: {overdue/total_task*100} %"+"\n"

    task_item=[]
    task_item.append(content_to_write)
    with open ("Task_overview.txt","w+")as file:
        for i in task_item:
            file.write(i)
#=====================================================================
#function for generate user overview
def user_overview(a,b): #a is task_list, b is username
    '''This function provide an overview of the tasks that each user own and the status.'''
    task_assigned=0
    total_tasks=len(a)
    complete=0
    uncomplete=0
    overdue=0
    for i in range (len(a)):
        if a[i]['username'] == b:
            task_assigned+=1
            if a[i]['completed'] == True:
                complete+=1
            else:
                uncomplete+=1
                if (a[i]['completed']== False) and (a[i]['due_date'] < today):
                    overdue+=1

    content_to_write=""
    content_to_write+=f"The total tasks assigned to {b} is {task_assigned}"+"\n"
    content_to_write+=f"The percentage of the total number of tasks that have been assigned to {b} is {task_assigned/total_tasks*100} %"+"\n"
    content_to_write+=f"The percentage of completed tasks: {complete/task_assigned*100} %"+"\n"
    content_to_write+=f"The percentage of incomplete tasks: {uncomplete/task_assigned*100} %"+"\n"
    content_to_write+=f"The percentage of tasks overdue: {overdue/task_assigned*100} %"
    return content_to_write

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        new_username = input("New Username: ").lower()
        reg_user(new_username)

    elif menu == 'a':
        task_username=input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            try:
                print("User does not exist. Please enter a valid username") 
                task_username=input("Name of person assigned to task: ")
                
            except ValueError:
                        print("Invalid user name.")
        add_task(task_username)

    elif menu == 'va':
        '''Showing all tasks.'''
        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    elif menu == 'vm':
        view_mine(task_list)

    elif menu == 'gr':
        '''Generate reports task_overview.txt and user_overview.txt.'''
        with open("user.txt", "r") as user_file:
           user_data = user_file.read().replace("\n"," ").replace(";"," ")
           user=user_data.split()
        today = datetime.today()
        user_list=[]
        for i in range (0,len(user),2):
            user_list.append(user[i])
            usernum=len(user_list)
        task_overview(task_list)
        user_item=[]
        for i in range (len(user_list)):    
            user_item.append(user_overview(task_list,user_list[i]))
            with open ("User_overview.txt","w+")as file:
                file.write(f"The total number of users: {len(user_list)}"+"\n")
                file.write(f"The total number of tasks: {len(task_list)}"+"\n")
                file.write("="*80+"\n")
                for i in user_item:
                    file.write(i)
                    file.write("\n"+("="*80)+"\n")
        print("Reports generated!")
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks from task_overview.txt and user_overview.txt.'''
        if not (os.path.exists("Task_overview.txt")) or (os.path.exists("User_overview.txt")):
            with open("user.txt", "r") as user_file:
                user_data = user_file.read().replace("\n"," ").replace(";"," ")
                user=user_data.split()
            today = datetime.today()
            user_list=[]
            for i in range (0,len(user),2):
                user_list.append(user[i])
                usernum=len(user_list)
            task_overview(task_list)
            user_item=[]
            for i in range (len(user_list)):    
                user_item.append(user_overview(task_list,user_list[i]))
                with open ("User_overview.txt","w+")as file:                
                    file.write(f"The total number of users: {len(user_list)}"+"\n")
                    file.write(f"The total number of tasks: {len(task_list)}"+"\n")
                    file.write("="*80+"\n")
                    for i in user_item:
                        file.write(i)
                        file.write("\n"+("="*80)+"\n")
            print("Reports generated!")
        with open ("Task_overview.txt","r") as file:
            content=file.read()
            print(f"Tasks Overview: \n{content}")
            print("="*80)
        with open ("User_overview.txt","r")as file:
            content=file.read()
            print(f"Users Overview: \n{content}")   

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")

  
