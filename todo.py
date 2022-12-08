import os
import pickle
from datetime import datetime


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
        # your code here    
        
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

    # def add(self):
    #     pass
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
                    
                    pickle.dump("test object", f)
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
        self.unique_id = "" # Generate a unique id
        self.created = datetime.now() # .timestamp() # self._time_created()
        self.complted = completed
        
    def __str__(self):
        pass
            
    def _parseDueDate(self, due_date):
        if due_date == None:
            return None
        else:
            # convert to datetime from user input. day.month.Year Hour:Min:Second
            date_time = datetime.strptime(due_date, '%d.%m.%Y %H:%M:%S')
            return date_time

# def main():
#     pass


class DirectoryPermissionsError(Exception):
    """Exception raised for error when current directory cannont be written or read from"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return 'DirectoryPermissionsError, {0} '.format(self.message)

# if __name__ == "__main__":
#     main()

x = Task()
