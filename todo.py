import os
import pickle
import uuid
from datetime import datetime
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
        return (f'{self.tasks}')
        
    # def pickle_tasks(self):
    #     """Picle your task list to a file"""
    #     # your code here
    #     pass  
    
    # # Complete the rest of the methods, change the method definitions as needed
    # def list(self):
    #     pass

    # def report(self):
    #     pass

    # def done(self):
    #     pass

    # def query(self):
    #     pass

    def add(self):
        
        pass
    
    def _load_tasks(self):
        if os.path.isfile('.todo.pickle'):
        # look for the pickle file. and read it in if its found
            with open('.todo.pickle', 'rb') as f:
                return (pickle.load(f))
        # if it's not found then go ahead and make one
        else:
            try:
                print("Could not find a previous instance of .todo.pickle\nMaking a new file")
                with open(".todo.pickle", 'wb') as f:
                    # make initial task of making todo list
                    
                    # add completed time
                    task_list = []
                    initialTask = Task('To do List', 1, '12.8.2022 10:40:00')
                    task_list.append(initialTask)
                    pickle.dump(task_list, f)
                with open('.todo.pickle', 'rb') as f:
                    return (pickle.load(f))
                # return (self._load_tasks())
            except:
                raise DirectoryPermissionsError("Please provide read and write access to current working directory")
                    
        # else raise an error that you don't have permission to make a .todo. file




 
class Task:
    """ Representation of a task
       Attributes:
         - created - date
         - completed - date
         - name - string
         - unique id - number
         - priority - int value of 1, 2, or 3; 1 is default
         - due date - date, this is optional """

    def __init__(self, name, priority=1, due_date = None, completed = None):
        """Instantiates a task object"""
        self.name = name
        self.priority = priority
        self.due_date = self._parseDueDate(due_date) 
        self.unique_id = uuid.uuid4() # Generate a unique id uuid.uuid4()
        self.created = datetime.now() # .timestamp() # self._time_created()
        self.complted = completed
        
    def __str__(self):
        return f'Name: {self.name}\nPriority: {self.priority}\nDue Date = {self.due_date}\nID: {self.unique_id}\nTime Created: {self.created}\nCompleted: {self.complted}'

            
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
def main():
    """main _summary_
    """
    parser = argparse.ArgumentParser(description='update your ToDo list')
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list')
    parser.add_argument('--priority', type=int, required=False, default=1, help='priority of task; default value is 1')
    
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Create instance of Tasks
    task_list = Tasks()
    
    # Read out arguments
    if args.add:
        print(f"we need to add {args.add} to the todo list with a priority of {args.priority}")
        task_list.add(args.add, args.priority)
    elif args.report:
        print("print out the report")
    

#     pass




# if __name__ == "__main__":
#     main()

x = Tasks()
print(x)
with open('.todo.pickle', 'rb') as f:
    testList = pickle.load(f)
    newList = []
    for testObj in testList:
        newList.append(testObj)
    newObj = Task('To do List 2', 1, '12.8.2022 11:40:00')
    newList.append(newObj)
    for obj in newList:
        print(obj)
