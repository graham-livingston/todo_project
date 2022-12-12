import os
import pickle
import uuid
from datetime import datetime
from datetime import date
import argparse



class Tasks:
    """ A List of Task objects

    Raises:
        DirectoryPermissionsError: Raised if read/write permissions are not granted to current working directory

    Returns:
        A List of Task objects
    """
    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = self._load_tasks()

    def __str__(self):
        for testObj in self.tasks:
            return (f'{testObj}')
        
    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open(".todo.pickle", 'wb') as f:
            pickle.dump(self.tasks, f)  
    
    def list(self):
        """list returns list of uncompleted tasks sorted by the due date. If tasks have the same due date, sort by decreasing priority (1 is the highest priority). If tasks have no due date, then sort by decreasing priority.
        """
        print('\nID\tAge\tDue Date\tPriority\tTask') # prints the header
        x = self._sort_tasks()

        for obj in x:
            if not hasattr(obj, 'completed'):
                age = date.today() - obj.created.date()
                print(f'{obj.unique_id}\t{age.days}d\t{obj.due_date}\t{obj.priority}\t{obj.name}')

    def report(self):
        """returns list of all tasks competed and incomplete. sorted by due date then by priority
        """
        x = self._sort_tasks()

        print('\nID\tAge\tDue Date\tPriority\tTask\tCreated\tCompleted') # prints the header
        
        for obj in x:
            age = date.today() - obj.created.date()
            if hasattr(obj, 'completed'):
                print(f'{obj.unique_id}\t{age.days}d\t{obj.due_date}\t{obj.priority}\t{obj.name}\t{obj.created}\t{obj.completed}')    
            else:
                print(f'{obj.unique_id}\t{age.days}d\t{obj.due_date}\t{obj.priority}\t{obj.name}\t{obj.created}\t-')    
                
    def delete(self, submited_ID):
        """delete deletes a task from your task list using the unique ID

        Arguments:
            ID -- str matching the unique id of the item to remove
        """
        try: 
            # get the index of the item 
            n = 0
            for task in self.tasks:
                # print(task.unique_id)
                if str(task.unique_id) == str(submited_ID):
                    # print(f'index: {n}')
                    return self.tasks.pop(n)  
                else:
                    n += 1  

        except:
            raise DeleteError("An error occured while trying to delete your item. Run 'todo -h' for usage instructions.")
    
    def done(self, submitted_ID):
        """done Marks a task from your task list as completed including the current date.

        Arguments:
            ID -- str matching the unique id of the item to remove
        """
        try: 
            # get the index of the item 
            n = 0
            for task in self.tasks:
                # print(task.unique_id)
                if str(task.unique_id) != str(submitted_ID):
                    n += 1
                else:
                    setattr(self.tasks[n], 'completed', date.today())
                    return(self.tasks[n].completed)                

        except:
            raise CompletionError("An error occured while trying to mark your item as completed. Make sure the ID is correct. Run 'todo -h' for usage instructions.")
        
    def query(self, query):
        try:
            seen = []
            for task in self.tasks:
                for q in query:
                # print(task.name)
                    if q.lower() == task.name.lower():
                        seen.append(task)
            if len(seen) > 0:
                print('\nID\tAge\tDue Date\tPriority\tTask\tCreated\tCompleted') # prints the header
                for task in seen:
                    age = date.today() - task.created.date()
                    if hasattr(task, 'completed'):
                        print(f'{task.unique_id}\t{age.days}d\t{task.due_date}\t{task.priority}\t{task.name}\t{task.created}\t{task.completed}')    
                    else:
                        print(f'{task.unique_id}\t{age.days}d\t{task.due_date}\t{task.priority}\t{task.name}\t{task.created}\t-')    
            else:
                print('No results matching your search query')
        except:
            QueryError('There was an error with your query terms')
                        
    def add(self, name, priority, due_date= None):
        """add _summary_

        Arguments:
            name -- _description_
            priority -- _description_
            due_date -- _description_
        """
        try:
            newTask = Task(name, priority, due_date)
            return self.tasks.append(newTask)
        except:
            raise AddError("There was an error in creating your task. Run 'todo -h' for usage instructions.")

    def _load_tasks(self):
        if os.path.isfile('.todo.pickle'):
        # look for the pickle file. and read it in if its found
            with open('.todo.pickle', 'rb') as f:
                tasks = pickle.load(f)
                return tasks
        # if it's not found then go ahead and make one
        else:
            try:
                print("Could not find a previous instance of .todo.pickle\nMaking a new file")
                with open(".todo.pickle", 'wb') as f:
                    # make initial task of making todo list
                    
                    task_list = []
                    initialTask = Task('To do List', 1, '12.8.2022 10:40:00')
                    task_list.append(initialTask)
                    pickle.dump(task_list, f)
                with open('.todo.pickle', 'rb') as f:  
                    tasks = pickle.load(f)
                    return tasks
            except:
                raise DirectoryPermissionsError("Please provide read and write access to current working directory")
                    
    def _sort_tasks(self):
        has_date = []
        no_date = []
        for obj in self.tasks:
            if obj.due_date != None:
                has_date.append(obj)
            else:
                no_date.append(obj)

        newlist_with_dates = sorted(has_date, key=lambda x: (x.due_date, x.priority))
        newlist_withOut_dates = sorted(no_date, key=lambda x: x.priority)
        sorted_List = newlist_with_dates + newlist_withOut_dates
     
        return(sorted_List)
        


 
class Task:
    """ Representation of a task
       Attributes:
         - created - date
         - completed - date
         - name - string
         - unique id - number
         - priority - int value of 1, 2, or 3; 1 is default
         - due date - date, this is optional """

    def __init__(self, name, priority=1, due_date = None):
        """Instantiates a task object"""
        self.name = name
        self.priority = priority
        self.due_date = self._parseDueDate(due_date) 
        self.unique_id = uuid.uuid4() # Generate a unique id uuid.uuid4()
        self.created = datetime.now() # .timestamp() # self._time_created()
        
    def __str__(self):
        return f'{self.unique_id}\t{self.due_date}\t{self.priority}\t{self.name}'
          
    def _parseDueDate(self, due_date):
        if due_date == None:
            return None
        else:
            # convert to datetime from user input. day.month.Year Hour:Min:Second
            date_time = datetime.strptime(due_date, '%d.%m.%Y %H:%M:%S')
            return date_time
             
class DirectoryPermissionsError(Exception):
    """Exception raised for error when current directory cannont be written or read from"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return 'DirectoryPermissionsError, {0} '.format(self.message)

class AddError(Exception):
    """Exception raised for error when add fails"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return 'DirectoryPermissionsError, {0} '.format(self.message)

class DeleteError(Exception):
    """Exception raised for error when add fails"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return 'DirectoryPermissionsError, {0} '.format(self.message)

class CompletionError(Exception):
    """Exception raised for error when add fails"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return 'DirectoryPermissionsError, {0} '.format(self.message)

class QueryError(Exception):
    """Exception raised for error when add fails"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return 'DirectoryPermissionsError, {0} '.format(self.message)


def main():
    """main _summary_
    """
    parser = argparse.ArgumentParser(description='update your ToDo list')
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list')
    parser.add_argument('--delete', type=str, required=False, help='delete a task from your list using the unique ID')
    parser.add_argument('--done', type=str, required=False, help='mark a task from your list as completed using the unique ID')
    parser.add_argument('--priority', type=int, required=False, default=1, help='priority of task; default value is 1')
    parser.add_argument('--due', type=str, required=False, help='due date in dd.mm.yyyy HH:MM:SS format')
    parser.add_argument('--query', type=str, required=False, nargs="+", help='query by adding search terms')
    parser.add_argument('--list', action='store_true', required=False, help="list all tasks that have not been completed")
    parser.add_argument('--report', action='store_true', required=False, help="print formated report of all tasks")
        
    # Parse the arguments
    args = parser.parse_args()
    
    # Create instance of Tasks
    task_list = Tasks()
    
    # Read out arguments
    if args.add:
        print(f"we need to add {args.add} to the todo list with a priority of {args.priority}")
        task_list.add(args.add, args.priority, args.due)

    elif args.list:
        task_list.list() 
    
    elif args.report:
        task_list.report()
    
    elif args.delete:
        print(f"we need to add {args.add} to the todo list with a priority of {args.priority}")
        task_list.delete(args.delete)
    
    elif args.done:
        print(f"we need to add {args.add} to the todo list with a priority of {args.priority}")
        task_list.done(args.done)
    
    elif args.query:
        task_list.query(args.query)
    
    task_list.pickle_tasks()
    exit()






if __name__ == "__main__":
    main()