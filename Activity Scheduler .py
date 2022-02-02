#!/usr/bin/env python
# coding: utf-8

# # Activity Scheduler

# ## Code by: Eisha

# Step 1: Creating a table with all desired activities to be done.

# In[2]:


from IPython.display import Image
Image(filename="et1.png")


# In[6]:


from IPython.display import Image
Image(filename="et2.png")


# Step 2: storing information about these activities and sub-tasks

# I have used one list in Python to store the all the tasks as separate lists. These sublists include the task ID, task name, time required and the dependencies. The time constraints have been ignored due to the afforementioned inclusion of "time required" which will be used within the algorithm to ensure that if adequate time is available then the task will be carried out.

# In[3]:


#Example of creating Task-List (for regular activities only)

tasks = [ [0, 'Grocery Shopping', 60, []],
         [1, 'Cooking', 90, [0]],
         [2, 'Finishing Assignments', 120, []],
         [3, 'Applying to Internships', 60, [],[]],
         [4, 'Work Study', 120, []]
]


# how the scheduler will work

# In this algorithm, the priority queue is formed by the list of all tasks. The scheduler will first look at the task dependencies and choose the tasks which have no dependencies and can thus be performed immediately. It will then look at the time required and "prioritise" the task with minimum time. This is because I would like to get done with the easiest (fastest) tasks earlier so that I have more motivation to do the rest. Priority queues allow us to dequeue the elements with the highest priority, which is useful for this algorithm. Once this task has been completed, it will be noted as being complete (and the tasks for which it may be a dependency also altered accordingly). Then the algorithm will repeat and do the same for the next task. This will run until the last task has been completed.
# 
# 

# Creating an activity scheduler in Python, which receives the list of tasks above as input and returns a schedule for you to follow:

# In[8]:


#From my CS110 session 5.1 PCW

def left(i):             # left(i): takes as input the array index of a parent node in the binary tree and 
    return 2*i + 1       #          returns the array index of its left child.

def right(i):            # right(i): takes as input the array index of a parent node in the binary tree and 
    return 2*i + 2       #           returns the array index of its right child.

def parent(i):           # parent(i): takes as input the array index of a node in the binary tree and
    return (i-1)//2      #            returns the array index of its parent



class MinHeapq:
    """ 
    This class implements properties and methods that support a min 
    priority queue data structure
    
    Attributes
    ----------
    heap : list
        A Python list where key values in the min heap are stored
        
    heap_size : int
        An integer counter of the number of keys present in the min heap
        
    """ 
    
    
    def __init__(self):
        """
        Class initialization method.
        
        """
        self.heap       = []
        self.heap_size  = 0

        
    def mink(self):
        """
        This method returns the lowest key in the priority queue
        
        """
        return self.heap[0] 
    
     
    def heappush(self, key):   
        """
        Inserts the value of key onto the priority queue, maintaining the
        min heap invariant.
        
        """
        self.heap.append([0,float("inf")])
        self.decrease_key(self.heap_size,key)
        self.heap_size+=1
        
    def decrease_key(self, i, key): 
        """
        This method implements the DECREASE_KEY operation, which modifies 
        the value of a key in the min priority queue with a lower value. 
        
        Note
        ----
        Use heapq_var.decrease_key(i, new_key)
        """
        if key > self.heap[i]:
            raise ValueError('new key is bigger than the current key')
        self.heap[i] = key
        while i > 0 and self.heap[parent(i)] > self.heap[i]:
            j = parent(i)
            holder = self.heap[j]
            self.heap[j] = self.heap[i]
            self.heap[i] = holder
            i = j  
            
            
    def heapify(self, i):
        """
        This method implements the MIN_HEAPIFY operation for the min priority
        queue. The input is the array index of the root node of the subtree to 
        be heapify.
        
        Note
        ----
        Use heapq_var.heapify(i)
        """
        l = left(i)
        r = right(i)
        heap = self.heap
        if l <= (self.heap_size-1) and heap[l][1]<heap[i][1]:
            smallest = l
        else:
            smallest = i
        if r <= (self.heap_size-1) and heap[r][1] < heap[smallest][1]:
            smallest = r
        if smallest !=i:
            heap[i], heap[smallest] = heap[smallest], heap[i]
            self.heapify(smallest)
        
    def heappop(self):
            
        """
        This method implements the EXTRACT_MIN operation. It returns the smallest
        key in the min priority queue and removes this key from the min priority 
        queue.
        
        """
        if self.heap_size < 1:
            raise ValueError('Heap underflow: There are no keys in the priority queue ')
        mink = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heap_size-=1
        self.heapify(0)
        return mink


# In[9]:


#From session 4.1 of CS110 Class (IN-class code)

"""
A Simple Daily Task Scheduler Using Priority Queues
"""
import heapq

def print_input_tasks(tsks):
    """ 
    Input: list of tasks 
    Task Status:
    - 'N' : Not yet in priority queue (default status)
    - 'I' : In priority queue
    - 'C' : Completed
    Output: print statement with all the tasks to be included in the scheduler
    """
    print('Input List of Tasks')
    for t in tsks:
        print(f"task:{t[0]} \t {t[1]} \t duration:{t[2]} \t depends on: {t[3]} \t Status: {t[4]}")



def initialize_tasks( tsks ):
    """
    Input: list of tasks 
    Output: initializes all tasks with default status (not yet in the priority queue).
    """  
    for b in range(len(tsks)):
        tasks[b].append('N')
        
def unscheduled_tasks( tsks ):
    """
    Input: list of tasks 
    Output: boolean (checks the status of all tasks and returns `True` if at least one task has status = 'N')
    """
    for t in tsks:
        if t[4] == 'N':
            return True
    return False

        
def remove_dependency( tsks, tid ):
    """
    Input: list of tasks and task_id of the task just completed
    Output: lists of tasks with t_id removed
    """
    for t in range(len(tsks)):
        if tsks[t][0] != tid and tid in tsks[t][3]:
            tsks[t][3].remove(tid)

            
def get_ready_tsks( tsks ):
    """ 
    Implements step 1 of the scheduler
    Input: list of tasks
    Output: list of tasks that are ready to execute (i.e. tasks with no pendending task dependencies)
    """
    rtsks = []
    for i in range(len(tsks)):
        if tsks[i][4] == 'N' and not tsks[i][3]:   # If tasks has no dependencies and is not yet in queue
            tsks[i][4] = 'I'                       # Change status of the task
            rtsks.append((tsks[i][0],tsks[i][2]))  # add (task_id, duration) to the list of tasks 
                                                   # to be pushed onto the priority queue                                      
    return rtsks

# Inputs Parameters to the Scheduler
step_sz = 10  # step size of scheduler in minutes
c_time = 480  # current time is set to the initial time in minutes (8:00 AM = 8x60)

tasks = [ [0, 'Grocery Shopping', 60, []],
         [1, 'Cooking', 90, [0]],
         [2, 'Finishing Assignments', 120, []],
         [3, 'Applying to Internships', 60, []],
         [4, 'Work Study', 120, []],
         [5, 'Networking', 90, []],
         [6, 'Enjoying Nature', 90, []],
         [7, 'Making Videos', 120, []],

         
]
ntasks = len(tasks)  # Number of tasks
pqueue = [] # Priority Queue

# STEP 0: Initialize the status of all tasks in the input list
initialize_tasks(tasks)
print_input_tasks(tasks)


def add_tasks_pqueue(pqueue, rtsks):
    """ 
    Implements step 2 of the scheduler
    
    Input: list of tasks
    Output: priority queue of tasks that have no dependencies
    """  
    if rtsks:
        if not pqueue:  # If the priority queue is non-exitent/ vacant
            pqueue = rtsks #create new priority queue
            
        else:
            for t in rtsks: #add every new task after the last element of the priority queue
                if t not in pqueue:
                    pqueue.append(t)
    
    return pqueue


# In[18]:


#new empty list created to store the order for the execution of tasks
timetable = []

#this runs for as long as there exist unexecuted tasks
while unscheduled_tasks(tasks) or pqueue:
#firstly those tasks are taken that do not have any dependencies and added to the priority queue
    rtsks = get_ready_tsks( tasks )  
    pqueue = add_tasks_pqueue(pqueue, rtsks)
    #the ones with the shortest time requirement are prioritised via minheap
    minheap = MinHeapq() 

#for the tasks in the priority queue
#timereq= time remaining (from the required time)
    if pqueue:
        #the tasks id and remaining time of these tasks becomes the first element of pqueue
        (tid, timereq) =  pqueue[0]  

        #runs until there is still time available to finish the task
        while timereq>0:
            tstep = step_sz   
            #depending on the time remainign the size of the step for task is adjusted
            if timereq < step_sz:                    
                tstep = timereq
            print(f"The ID of the task being executed is {tid}; and the remaining time for this task is {timereq} min") 
            #the remaining time is adjusted after task
            timereq -= tstep                  
            c_time += tstep 
        #if there is no time left to finish the task    
        if timereq == 0: 
            #this acts as a "marker" for a completed task
            print(f"✅ The task {tid} - '{tasks[tid][1]}' has been completed!") 
        
       
            new = [tasks[tid][1]]
            #this places tasks according to their order of completion
            timetable.append(new) 
            #this will adjust the dependent tasks by removing the dependency
            remove_dependency(tasks,tid) 
            pqueue.pop(0) #this removes the task from the pqueue
        
        
        
    


# how the scheduler prioritizes tasks based on their priority value.

# In addition to the actual scheduler, this algorithm also takes into account the "time required" for each task and its dependencies. This two-fold approach guarentees that the easier (or fastest) tasks are completed first before moving on to those that are highly dependent on the completion of these previous tasks, or simply take more time.

# What changes do we need to make to the first version of the scheduler to include multi-tasking activities? How are constraints in the scheduling process handled by a priority queue?

# The multi-tasking scheduler can be made by updating the regular scheduler input list to include boolean values (True or False) in the fourth index. This boolean value can be considered as an indicator as to whether the task in question can be multitasked or not. It will more likely be the case that it cannot (as only task 6 and 7 can be multitasked in my personal case). This would allow the tasks with this capability to be executed simultaneously with each other.
# 
# One major constraint in the scheduling process is that of the inability to perform multiple tasks at once. With a multitasker, this is made possible with extra input information demonstrating whether tasks can be multitasked or not. These can then be given priority over others via heapify (if they are strategically placed on top of the heap).

# Activity priority scheduler with multi-tasking capability in Python:

# In[4]:


#From my session 5.1 PCW

def left(i):             # left(i): takes as input the array index of a parent node in the binary tree and 
    return 2*i + 1       #          returns the array index of its left child.

def right(i):            # right(i): takes as input the array index of a parent node in the binary tree and 
    return 2*i + 2       #           returns the array index of its right child.

def parent(i):           # parent(i): takes as input the array index of a node in the binary tree and
    return (i-1)//2      #            returns the array index of its parent



class MinHeapq:
    """ 
    This class implements properties and methods that support a min 
    priority queue data structure
    
    Attributes
    ----------
    heap : list
        A Python list where key values in the min heap are stored
        
    heap_size : int
        An integer counter of the number of keys present in the min heap
        
    """ 
    
    
    def __init__(self):
        """
        Class initialization method.
        
        """
        self.heap       = []
        self.heap_size  = 0

        
    def mink(self):
        """
        This method returns the lowest key in the priority queue
        
        """
        return self.heap[0] 
    
     
    def heappush(self, key):   
        """
        Inserts the value of key onto the priority queue, maintaining the
        min heap invariant.
        
        """
        self.heap.append([0,float("inf")])
        self.decrease_key(self.heap_size,key)
        self.heap_size+=1
        
    def decrease_key(self, i, key): 
        """
        This method implements the DECREASE_KEY operation, which modifies 
        the value of a key in the min priority queue with a lower value. 
        
        Note
        ----
        Use heapq_var.decrease_key(i, new_key)
        """
        if key > self.heap[i]:
            raise ValueError('new key is bigger than the current key')
        self.heap[i] = key
        while i > 0 and self.heap[parent(i)] > self.heap[i]:
            j = parent(i)
            holder = self.heap[j]
            self.heap[j] = self.heap[i]
            self.heap[i] = holder
            i = j  
            
            
    def heapify(self, i):
        """
        This method implements the MIN_HEAPIFY operation for the min priority
        queue. The input is the array index of the root node of the subtree to 
        be heapify.
        
        Note
        ----
        Use heapq_var.heapify(i)
        """
        l = left(i)
        r = right(i)
        heap = self.heap
        if l <= (self.heap_size-1) and heap[l][1]<heap[i][1]:
            smallest = l
        else:
            smallest = i
        if r <= (self.heap_size-1) and heap[r][1] < heap[smallest][1]:
            smallest = r
        if smallest !=i:
            heap[i], heap[smallest] = heap[smallest], heap[i]
            self.heapify(smallest)
        
    def heappop(self):
            
        """
        This method implements the EXTRACT_MIN operation. It returns the smallest
        key in the min priority queue and removes this key from the min priority 
        queue.
        
        """
        if self.heap_size < 1:
            raise ValueError('Heap underflow: There are no keys in the priority queue ')
        mink = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heap_size-=1
        self.heapify(0)
        return mink


# In[5]:


#From session 4.1 of CS110 Class (IN-class code)

"""
A Simple Daily Task Scheduler Using Priority Queues
"""
import heapq

def print_input_tasks(tsks):
    """ 
    Input: list of tasks 
    Task Status:
    - 'N' : Not yet in priority queue (default status)
    - 'I' : In priority queue
    - 'C' : Completed
    Output: print statement with all the tasks to be included in the scheduler
    """
    print('Input List of Tasks')
    for t in tsks:
        print(f"task:{t[0]} \t {t[1]} \t duration:{t[2]} \t depends on: {t[3]} \t Status: {t[4]}")



def initialize_tasks( tsks ):
    """
    Input: list of tasks 
    Output: initializes all tasks with default status (not yet in the priority queue).
    """  
    for b in range(len(tsks)):
        tasks[b].append('N')
        
def unscheduled_tasks( tsks ):
    """
    Input: list of tasks 
    Output: boolean (checks the status of all tasks and returns `True` if at least one task has status = 'N')
    """
    for t in tsks:
        if t[4] == 'N':
            return True
    return False

        
def remove_dependency( tsks, tid ):
    """
    Input: list of tasks and task_id of the task just completed
    Output: lists of tasks with t_id removed
    """
    for t in range(len(tsks)):
        if tsks[t][0] != tid and tid in tsks[t][3]:
            tsks[t][3].remove(tid)

            
def get_ready_tsks( tsks ):
    """ 
    Implements step 1 of the scheduler
    Input: list of tasks
    Output: list of tasks that are ready to execute (i.e. tasks with no pendending task dependencies)
    """
    rtsks = []
    for i in range(len(tsks)):
        if tsks[i][4] == 'N' and not tsks[i][3]:   # If tasks has no dependencies and is not yet in queue
            tsks[i][4] = 'I'                       # Change status of the task
            rtsks.append((tsks[i][0],tsks[i][2]))  # add (task_id, duration) to the list of tasks 
                                                   # to be pushed onto the priority queue                                      
    return rtsks

# Inputs Parameters to the Scheduler
step_sz = 10  # step size of scheduler in minutes
c_time = 480  # current time is set to the initial time in minutes (8:00 AM = 8x60)

tasks = [ [0, 'Grocery Shopping', 60, []],
         [1, 'Cooking', 90, [0]],
         [2, 'Finishing Assignments', 120, []],
         [3, 'Applying to Internships', 60, []],
         [4, 'Work Study', 120, []],
         [5, 'Networking', 90, []],
         [6, 'Enjoying Nature', 90, []],
         [7, 'Making Videos', 120, []],

         
]
ntasks = len(tasks)  # Number of tasks
pqueue = [] # Priority Queue

# STEP 0: Initialize the status of all tasks in the input list
initialize_tasks(tasks)
print_input_tasks(tasks)


def add_tasks_pqueue(pqueue, rtsks):
    """ 
    Implements step 2 of the scheduler
    
    Input: list of tasks
    Output: priority queue of tasks that have no dependencies
    """  
    if rtsks:
        if not pqueue:  # If the priority queue is non-exitent/ vacant
            pqueue = rtsks #create new priority queue
            
        else:
            for t in rtsks: #add every new task after the last element of the priority queue
                if t not in pqueue:
                    pqueue.append(t)
    
    return pqueue


# In[6]:


#NEW LIST OF TASKS
#This includes a Boolean value for True or False dependening on the tasks' multitasking capability
tasks = [ [0, 'Grocery Shopping', 60, [], False  ],
         [1, 'Cooking', 90, [0], False],
         [2, 'Finishing Assignments', 120, [], False],
         [3, 'Applying to Internships', 60, [], False],
         [4, 'Work Study', 120, [], False ],
         [5, 'Networking', 90, [], True],
         [6, 'Enjoying Nature', 90, [], True],
         [7, 'Making Videos', 120, [], True],
        ]
  # step size of scheduler in minutes
step_sz = 10
# here the current time is 8 am in minutes to denote the start of the day
c_time = 480  
 # the priority Queue
pqueue = []
# the number of tasks
ntasks = len(tasks)  
#initialises the tasks
initialize_tasks(tasks)


# In[7]:


#this variable stores the order of execution for tasks
timetable = []

#this runs for as long as there exist unexecuted tasks
while unscheduled_tasks(tasks) or pqueue:
#firstly those tasks are taken that do not have any dependencies and added to the priority queue
    rtsks = get_ready_tsks( tasks )  
    pqueue = add_tasks_pqueue(pqueue, rtsks)
    #the ones with the shortest time requirement are prioritised via minheap
    minheap = MinHeapq() 

#for the tasks in the priority queue
#timereq= time remaining (from the required time)
    if pqueue:
        #the tasks id and remaining time of these tasks becomes the first element of pqueue
        (tid, timereq) =  pqueue[0]  
#here until there is time remaining the task is executed
        #multitasking empty list created
        multitasking = []
        #if we can multitask with this task
        if tasks[tid][4]: 
                if tasks[x] == False:
                    multitasking.append(i) 
                    multitasking.append(x[1]) 
                    #rhe task is removed from pqueue
                    pqueue.remove(x) 
                    break     
        #the task is completed and timestep adjusted until the completion of the task
        while timereq>0: 
            tstep = step_sz                        
            if timereq < step_sz:                    
                tstep = timereq
            
            #a statement is printed out while we are multitasking 
            if multitasking:     
                print(f"The scheduler is completing task {multitask[0]}; and it will be completed in {multitask[1]} minutes") 
                
               # A statement is printed upon completion of the task
                if multitasking[1] == 0: 
                    
                    print(f" This task has been completed {multitasking[0]} - '{tasks[multitasking[0]][1]}") 
                    #this removes the dependency from any other tasks
                    remove_dependency(tasks,multitasking[0]) 
                    #The schedule is now updated with the new order of completion of our tasks
                    schedule.append(new) 
                    #the activity is noted to be compelted and time remaining is updated accordingly
                    tasks[multitasking[0]][-1]="C" 
                    tasks[multitasking[0]][2]=0 
                    break 
            #the time remainign is updated
            timereq -= tstep                  
            c_time += tstep               
            
    
        


#  critical analysis of the scheduler in terms of the efficiency of your schedule (not scheduler)

# The proposed algorithm is successful in terms of providing an account of the various tasks required and theorder in which they should ideally be executed. However, it is very simlified such that it leaves a lot to be desired. For instance, although multitasking is a good additional feature, it does not take into account the sub-tasks of the tasks and whether all subtasks are compatible for multitasking. For instance, I may be able to make video while speaking with my friends (networking) but it may be unprofessional or impossible in a professional setting. Moreover, breaks for lunch and other menial tasks are not accounted for. And as I did not include them in my small list of "tasks" this would mean either additional time required to input them or manually finding the gaps. This current version of the algorithm is not the best fit for me to use. I would prefer to upgrade it to make a repeated timeslot for breaks in between activities and for meal times etc. This would require less effort in inputting activities and provide more time for changing up the activities and tasks every week etc. As for my schedule, I believe it is over-efficient to the point that it may be unrealistic for one day. I would have to leave a few of the tasks included in order to realistically incorporate these actitivities into my schedule with classes, civic projects etc

# ## Resources Used

# Code from CS110 Class and PCW from sessions 4.1 and 5.1 was used (and is tagged). 

# In[ ]:




