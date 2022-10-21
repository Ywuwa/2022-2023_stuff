# Import the tkinter module
import tkinter
from tkinter import *  
#Turing-machine stuff
class turing:
    def __init__(self, st, pos, limit):
        self.st=st
        self.pos=pos
        self.limit=limit
    
def switch_command(sign):
    if sign=='0': return '0'
    elif sign=='1': return '1'
    elif sign==' ': return '_'
    elif sign=='' or sign=='*': return '*'

def switch_replace(sign,target,pos):
    if sign=='0': 
        target[pos]=sign 
        ''.join(target)
    elif sign=='1': 
        target[pos]=sign 
        ''.join(target)
    elif sign=='_': 
        target[pos]=' ' 
        ''.join(target)
    
def switch_move(sign):
    if sign=='r': 
        return 1
    elif sign=='l': 
        return -1
    elif sign=='*': 
        return 0
    
def switch_st(command,st,target,pos):
    if command[3]=='h': 
        M.st=-1
        if pos>len(target)-1:
            target.insert(len(target), '')
            pos=len(target)-1
        if pos<1:
            target.insert(0,'')
            pos=0
        target[pos]=command[1] 
        ''.join(target)
    else :
        st=int(command[3])
        for i in range(0,len(command)-4):
            st=st*10+int(command[4+i])
        M.st=st
'''
according to command's order replaces target[pos] symbol 
according to command's order changes head's position(pos) 
according to command's order changes status 
'''   
def execute(command,st,target,pos):
    switch_replace(command[1],target,pos)
    M.pos+=switch_move(command[2])
    if M.pos>len(target):
        target.insert(len(target), '')
        M.pos=len(target)-1
    if M.pos<0:
        target.insert(0,'')
        M.pos=0
    switch_st(command,st,target,M.pos)
'''
reads head's symbol, 
search the exact command[i] from the set command[st], 
executes it
''' 
def commands(command,st,target,pos):
    if M.pos>len(target)-1 or M.pos<0:
        act='*'
        if M.pos>len(target)-1:
            target.insert(len(target), '')
            M.pos=len(target)-1
        if M.pos<1:
            target.insert(0,'')
            M.pos=0
    else: 
        act=switch_command(target[pos])
    for i in range(0,len(command)):
        if act==command[i][0] and st>=0:
            execute(command[i],M.st,target,M.pos)
            
# Creating the GUI window.
window = tkinter.Tk()
window.title("Turing Machine Emulator")

l1 = tkinter.Label(window,text="""
Turing-machine Emulator
    first: read file, create list of statuses, create list of statuses' commands
    second: gets an input (please, type it into the texteditor below)
    third: runs the input (the user has typed)
INSTRUCTION:
    PLEASE print statuses as "qi" where i is integer & i>=0
    Any symbol exept numbers, "q", "1", "0", "*", "_", "r", "l", "h", ";" will terminate program
    (or it will not work properly)
    r-head moves right, l-head moves left
    h-halt, finilize the program, ;-comment, e.c. after it nothing in the line will be read
EXAMPLE:
    q0 0 1 r q0 ; default status q0, head reads '0', it changes '0'->'0', moves right, set status q1  
    q0 1 0 r q0 ; default status q0, head reads '1', it changes '1'->'0', moves right, set status q0
    q0 * @ r h ; default status q0, head reads '*' (aka nothing), it changes '*'->' ', finilize th program
WARNING:
    input can contain only '0','1',' ' and '' symbols, otherwise the program won't execute properly'
""",
           relief=RIDGE, width=300, height=20, font=("Arial", 12), justify=LEFT, anchor=NW)
l1.pack(fill=BOTH)

#where to write
fram = Frame(window)
input_text = Entry(fram)
input_text.pack(fill=BOTH)
input_text.focus_set()
#initialize target aka input for further execution
target=input_text.get()

# Setting up the buttons, compile_iii_button() 
# is passed as a command
compile_run_button = tkinter.Button(fram, height=1, width=10, text="Run")
compile_run_button.pack()
compile_step_button = tkinter.Button(fram, height=1, width=10, text="Step")
compile_step_button.pack()

fram.pack(side = TOP,fill=X)
# adding scrollbar
scrollbar0 = tkinter.Scrollbar(fram,width=10)  
# packing scrollbar
scrollbar0.pack(side=TOP, fill=X)
scrollbar0.config(orient=HORIZONTAL,command=input_text.xview)
#init turing-class element
M=turing(0,0,1)
# Creating the function to compile the text 
# with the help of compile_button
def compile_text():
    data = ''
    stats = []
    prog.config(state=DISABLED)
    file=prog.get('1.0',END)
    target=input_text.get()
    target=list(target)
    if len(target)<1:
        '''prog.config(state=NORMAL)
        prog.delete('1.0',END)
        prog.insert('1.0', 'no input')'''
        str(target.append('no input'))
        input_text.delete(0,END)
        input_text.insert(0,target)
    elif len(file)<=2:
        prog.config(state=NORMAL)
        prog.delete('1.0',END)
        prog.insert('1.0', 'no program here')
    else:
        ind=0 
        f=file[ind]
        while ind<len(file)-1:
            if f == ';':
                while f!='\n':
                    ind+=1
                    f=file[ind]
            else: 
                data=data+f#data.append(f)
                ind+=1
                f=file[ind]
        
        #place lists of commands into stats list 
        k=0
        space=0 #how many empty statuses between current 'i' and previous 'space'
        for i in range(0,4*len(data)):
            if "q"+"{id}".format(id=i) in data:
                for j in range(space,i+1):
                    stats.append([])
                    k+=1
                space=i
        data=data.replace('\n\n\n','\n')
        data=data.replace('\n\n','\n')
        lines=data.splitlines()
        for i in range(0,k):
            for j in range(0,len(lines)):
                if "q"+"{id}".format(id=i)+" " in lines[j][:int(len(lines[j])/2)]:
                    stats[i].append(lines[j])
        #adjust stats list of lists        
        for i in range(0,k):
            for j in range(0,len(stats[i])):
                stats[i][j]=stats[i][j].strip(' ')
                stats[i][j]=stats[i][j].lstrip("q"+"{id}".format(id=i) )
                stats[i][j]=stats[i][j].replace(' ', '')
                stats[i][j]=stats[i][j].replace('q', '')
        if len(stats)<1:
            prog.config(state=NORMAL)
            prog.delete('1.0',END)
            prog.insert('1.0', 'no program here')
        
        else:
            c=0
            while (M.st>=0 and c<M.limit):
                #print(M.st,M.pos)
                #print(target)
                commands(stats[M.st],M.st,target,M.pos)
                c+=1
    
    input_text.delete(0,END)
    for i in range(len(target)):
        input_text.insert(0,target[len(target)-i-1])
    prog.config(state=NORMAL)
def compile_full_text():
    M.limit=10000
    compile_text()
def compile_step_text():
    M.limit=1
    compile_text()
# adding scrollbar
scrollbar = tkinter.Scrollbar(window)  
# packing scrollbar
scrollbar.pack(side=RIGHT, fill=Y)

# text box in root window
prog = tkinter.Text(window, yscrollcommand=scrollbar.set)
# text program area at index 1 in text window
prog.insert('1.0', ' ')
prog.pack(side = BOTTOM, fill=X)

scrollbar.config(command=prog.yview)
compile_run_button.config(command = compile_full_text)
compile_step_button.config(command = compile_step_text)
window.mainloop()
