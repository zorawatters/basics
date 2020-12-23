#!/usr/bin/python

import tkinter as tk

# side note: I should have done this in a jupyter notebook lol

# create window
window = tk.Tk()

# WIDGETS

# label - displays text to the window 
label = tk.Label(text="Hello World", fg="white", bg="black", width=10, height=10) #background and foreground; attributes can be used for most widgets

# buttons
button = tk.Button()
check = tk.Checkbutton()
check = tk.Checkbutton()
# user selecton
lb = tk.Listbox()
lb.insert(1, "option 1") #index, option
lb.pack()
# user entry
input1 = tk.Entry() #one line
input2 = tk.Text() #multi line
# working with user entry
input1.get() 
input1.delete(0, tk.END) #(index, index) just like slicing; (0, tk.END) for total deletion
input1.insert(0, "inserted") # (index, "string to insert")
# for text entries it is required to pass an argument specifying line number and character position w/ format lineNum.index. Same w all commands for text
input2.get("1.0", tk.END) #gets whole text
input2.delete("1.0") #deletes first line
input2.insert("2.0", "\nWorld") #need to use newline char to start on newline
input1.pack()
input2.pack()

# DISPLAY

# organizing widgets - you can pass a frame as a widget's "master" with master = frame as the first argument.
frame = tk.Frame(master=window, width=250, height=250) # (master, relief, text. ect.)
#relief is the style of the frame. can be tk.FLAT, RAISED, SUNKEN, GROOVE, or RIDGE

# use .pack() on all created widgets to put them into the window (block)
# NOTE: the order that you pack things will alter the appearance of the window
frame.pack() 
#if you want to fill space, use either fill=tk.X Y or BOTH as an argument in pack. you can also set side=tk.TOP BOTTOM LEFT or RIGHT. use expand=True to make responsive
frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# use .place() on created widgets to put them in specific spots
placed_label =  tk.Label(master=frame, text="I'm at (25, 25)", bg="red")
placed_label.place(x=25,y=25) #in pixels
#.place is not responsive

# use .grid() on all created widgets to display them table-style. this will split the window or frame into rows and columns (starting from 0,0)
# best way to create this is probably a loop
# 3x3 grid: 
for i in range(3):
    # here is where we make the grid responsive. we want to make sure we give index, weight (factor of growth for each section), and minimum size of each section
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)
    for j in range(3):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        # here, grid is attatched to the window and we are placing each frame in a section
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"row {i}\n column {j}")
        label.pack() #can also pad with pack

# use the following values in the grid function w/ the sticky attribute to override the default center placing of widgets in cells. this is the eqiv. of fill in .pack
# "n" or "N" to align to the top-center part of the cell
# "e" or "E" to align to the right-center side of the cell
# "s" or "S" to align to the bottom-center part of the cell
# "w" or "W" to align to the left-center side of the cell
#can use 2+ to fill in different directions; nsew = BOTH


#EVENTS

#we use the .bind to call event handlers on widgets. it always takes 2 arguments: the event, and the function that will handle it. first write a handler...
def handle_keypress(event):
    print(event.char)
#then bind it to the event so that mainloop can read it
window.bind("<Key>", handle_keypress)

#we can assign function directly to the widget with the command attribute 
 

# run event loop - listens for events in the window and blocks code execution til window is closed
window.mainloop()

#window.destroy() will manually kill loop

# EXAMPLE OF FRAMING FROM REALPYTHON.COM
# border_effects = {
#     "flat": tk.FLAT,
#     "sunken": tk.SUNKEN,
#     "raised": tk.RAISED,
#     "groove": tk.GROOVE,
#     "ridge": tk.RIDGE,
# }

# window = tk.Tk()

# for relief_name, relief in border_effects.items():
#     frame = tk.Frame(master=window, relief=relief, borderwidth=5)
#     frame.pack(side=tk.LEFT)
#     label = tk.Label(master=frame, text=relief_name)
#     label.pack()

# window.mainloop()

# COMMENT OUT ALL ABOVE CODE (except imports) AND RUN BELOW CODE TO MAKE BASIC GUI WITH BUTTONS, COMMANDS, AND GRID

def increase_num():
    value = int(counter['text'])
    counter['text'] = f"{value + 1}"

def decrease_num():
    value = int(counter['text'])
    counter['text'] = f"{value - 1}"

window = tk.Tk()
#set grid - 1x3
#layout: - num +
window.rowconfigure(0, weight = 1, minsize = 75)
window.columnconfigure([0,1,2], weight = 1, minsize = 75)
#set buttons and counter
dec_button = tk.Button(master=window, text=" - ", command=decrease_num)
dec_button.grid(row=0, column=0, sticky="nsew") #fill entire cell

counter = tk.Label(master=window, text='0')
counter.grid(row=0, column=1)

inc_button = tk.Button(master=window, text=" + ", command=increase_num)
inc_button.grid(row=0, column=2, sticky="nsew") #fill entire cell

window.mainloop()