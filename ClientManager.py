# cliente-up/shutdown program of GATELAB for clients through a server
# Program.py
# python 2.7

# This program needs to have the awake, numpy and tkinter librairies


# To launch the program just tap in a terminal "sudo python Programme.py"


import csv
import numpy as np
import awake
import Tkinter 
import tkFileDialog
import os
import subprocess
from subprocess import call
from Tkinter import *



 












#------------------------DEFINITIONS


chart =[]
# chart of data from the csv file (Hostname, Mac adress, IP adress)

status = []
# chart of client status (checkbox, awake/ready, busy)


#-------------------------- Event



def event(var):
	# function use to show to the user what the code is doing 
	
	
	text_event = Label(frame8, text = var, bg = "white")
	# var is the text argument
	
	text_box.window_create("end", window = text_event)
	text_box.insert("end", "\n") 
	# insert the text in the text_box with the scrollbar
	
	text_box.pack(side = "top", fill = "both", expand = True)
	sb2.config(command = text_box.yview)
	# configuration for the scrollbar

#--------------------------Check client's status



def ready():
	# function to check if the clients are ready
	
	client = 0
	
	event("Check ready clients...")
	
	for client in range(len(chart)):
		
		if status[client][1] != "1":
			
			output_ping = os.popen ("fping -B1 %s &" % chart[client][2], "r").read()
			# first send a basic ping to see if it's awake or not
			event("Sending ping to %s ..." % chart[client][0])
			
			if output_ping.find("alive") != -1:
				output_X11 = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s ''ps aux | grep X'' &" % chart[client][0], "r").read()
				# if it's awake search for any the X11 (= Client ready)
				
				if output_X11.find("/usr/bin/X") != -1:
					all_button[client].configure(fg = "green")
					# if it's ready put the hostname in green 
					status[client][1] = 1
					# and complete the status chart (1 = ready)
					
				else:
					status[client][1] = 0
					# complete the status chart (O = awake but not ready)
					
					all_button[client].configure(fg = "orange")
					# put the hostname client as orange
					
			if output_ping.find("unreachable") != -1:
				status[client][1] = -1
				# if client is down then let it black 
				# complete the status chart (-1 = down)
				
	event("Check ready client done.")
			




	
def busy():
	
	client = 0
	
	event("Check busy clients...")
	
	for client in range(len(chart)):
		
		if status[client][1] == "1":
			# only if client is awake and ready check if octave is running
			# if a client is only awake it couldn't be busy
			
			output_busy = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s ''ps aux | grep octave'' &" % chart[client][0], "r").read()
			event("Sending busy question...")
			
			if output_busy.find("/usr/bin/octave") != -1:
				all_button[client].configure(fg = "red")
				# if it's busy put the hostname as red
				 
				status[client][2] = 1
				# complete the status chart (1 = busy)
				
			else:
				status[client][2] = 0
				# complete the status chart (0 = ready but not busy)
		else:
			status[client][2] = -1
			#complete the status chart (-1 = not ready)
	
	event("Check busy clients done.")
			
#---------------------------Verification of which box is checked


def check_box():
	# function to count and complete the status chart
	
	global nc
	
	var = 0
	
	for v in vars:
		status[var][0] = v.get() 
		var = var + 1  
		# put all value of checkboxes in the status chart 
	
	box = 0	
	number_checked = 0
	
	for box in range(len(status)):
		
		if status[box][0] == "1":
			number_checked = number_checked + 1
			# counting number of checkboxes selected
	
	nc = number_checked
	event("Check box done.")
	text_number_checked.config(text = "\n Number of client selected : %s"  % nc)
	# update number of checkboxes selected in GUI

#---------------------Definition of select_all and deselect_all function		


def select_all():
	#function to select all checkboxes in one clic
	
    for i in all_button:
        i.select()
		
    event("Select all")



def deselect_all():
	#function to deselect all checkboxes in one clic
	
    for i in all_button:
        i.deselect() 
    
    event("Deselect all")   
        
#----------------------------Defnition of wake_up fonction 



def wake_up():
	# function to wake up selected clients
	# server may be slow so it may need to divise the total to wake up
	
	event("Wake-up")
	check_box()
	ready()
	# to wake only down client
	  
	entry_nb = int (entry.get())
	# get the x of "wake up x by x"
	n = 0	
	
	
	if nc <= entry_nb:
		# it doesn't need to be divided
		
		event("number_checked <= %s" % entry_nb)
		
		for n in range(len(chart)):
			
			if status[n][0] == "1" and status[n][1] == "0":
				output_awake=os.popen("awake %s" % chart[n][1], "r").readline()
				# send the magic packet to wake up client
				
				event ("Sending magic packets to %s" % chart[n][0])
				
				if output_awake.find("Sending") == 0:
					all_button[n].configure(fg = "orange")
					# if it's weel done then put hostname orange
			ready()
			
			while status[n][0] == "1" and status[n][1] == "0":
				ready()	
				# wait until all client selected are ready
	
	else:
		# nedd to divise the number to wake up
		
		event ("number_checked > %s" % entry_nb)
		number_awake = 0
		client =0
		
		for n in range(len(chart)):
			
			while number_awake <= entry_nb and status[n][0] == '1' and status[n][1] != '1' :
				# wake up only the x first clients
				
				for client in range(len(chart)):
					
					if status[client][0] == "1" and status[client][1] == "0":
						output_awake=os.popen("awake %s" % chart[client][1], "r").readline()
						# send the magic packet to wake up client
						
						event ("Sending magic packets to %s" % chart[client][0])
						
						if output_awake.find("Sending") == 0:
							all_button[client].configure(fg = "orange")	
							# if it's weel done then put hostname orange
							
						number_awake = number_awake + 1		
					
					if number_awake == entry_nb:
						ready()
						while status[client][1] == "0":
							ready()
						number_awake = 0
						# wait until all client selected are ready
						
	event("Clients awake.")	
		
		
			
				
				
				
		
	
	
#---------------------------Definition of shut_down fonction

def shut_down():
	# function to shut_down clients selected
	
	event("Shut down")
	check_box() 
	client=0
	
	for client in range(len(chart)):
		
		if status[x][0] == "1":
			# it can only work on ready clients
			
			call(["ssh", "-q", "-o", "UserKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=no", "-f", "neurodebian@%s" % chart[client][0],"''sudo poweroff''"])
			# send a ssh command to shut down
			
			event("Sending shut down command to %s" % chart[client][0])
			all_button[client].configure(fg = "black")
			#  put the hostname black
			
			status[client][1] = 2
			# complete the status chart
			
	event("Shut down done.")	
			

#-------------------------- Definition of slot_browse

def slot_browse():
	#function to get the file path of the task experiment file selected
	
	global file_path
	
	_fpath = tkFileDialog.askopenfilename(multiple)
	# open the TkFileDialog so that user can choose his file
	
	file_path.set(_fpath)
	


#-------------------------Open file

def open_csvfile():
	# client to open the client list file and set status and chart chart
	global chart, status
	
	file_name = str(path_client.get())			
	file_open = open (file_name, "rb")	
	# open the file and read it
	
	chart = np.loadtxt(file_open, dtype = str, delimiter = ",")	
	# put the data into a chart and see them as a string
	
	status = np.copy(chart)
	
	
	
	
#--------------------------Definition of select-file

def select_file():
	#function to get the file path of the client list file selected
	
	global path_client, vars, all_button
	
	path_file = tkFileDialog.askopenfilename(filetypes = [("Fichier csv", "*.csv")])
	# open the TkFileDialog so that user can choose his file
	
	(path_client).set(path_file)
	open_csvfile()
	text.delete("0.0", END)
	# delete what was in the text that countain list of checkboxes
	
	del(vars[:])
	del(all_button[:])
	# delete the list value and the list of checkboxes
	
	list_box()
	# recreate the new listbox with the new data
	
	Window.update()
	# refresh
	
	
	
	
	
#------------------------- Definition of start_task

def start_task():
	# function to launch a task
	
	client = 0
	
	for client in range(len(chart)):
		
		if status[client][1] == '1':
			output_X11 = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s ''  '' &" % chart[client][0], "r").read()
			# if client are ready then launch the task file to clients selected
			
	event("Task send %s." % file_path)
	busy()
	# check if they're busy
				
	
		






#------------------------- Definition of end_task	
	
	
def end_task():
	# function to kill all tasks
	client = 0
	
	for client in range(len(chart)):
		
		if status[client][1] == '1':
			output_X11 = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s '' killall '' &" % chart[client][0], "r").read()
			# if clients are ready then kill ALL task so that it isn't busy anymore
			
	event("Tasks end.")
	busy()	
	ready()	
	
	
	
	
	
	
			
			
#--------------------------WINDOWS'S CREATION		





#-----------------------Creation of window

    
Window = Tk()
# create a graphic window
																		   
Window.title("Wake-up/Shutdown manager")
Window["bg"] = "bisque"
																   
 

vsb = Scrollbar(Window, orient = VERTICAL)
vsb.grid(row = 0, column = 1, rowspan = 10, sticky = N+S)
# create a scrollbar for all the Window

Canvas_sb = Canvas(Window, yscrollcommand = vsb.set)
# create a canvas because it isn't possible to put a scrollbar on frames

Canvas_sb["bg"] = "bisque"
Canvas_sb.grid(row = 0, column = 0, sticky = "sewn")
vsb.config(command = Canvas_sb.yview)

Window.grid_rowconfigure(0, weight = 1)
Window.grid_columnconfigure(0, weight = 1)



Frame_Canvas = Frame(Canvas_sb)
Frame_Canvas["bg"] = "bisque"
# create the big frame in the canvas

text = Label(Frame_Canvas, text = "\n Please  select your Client list file and then check clients and then you can wake-up/shut-down or start/end a task \n" ,fg="black", bg="bisque")    
text.grid(row = 0, column = 0, columnspan = 2) 	



#------------------- frame 1 : Creation of brows your client list


frame1 = Frame(Frame_Canvas)
frame1["bg"] = "bisque"

text_path_client = Label( frame1, text = "Select your Client list file (csv only): ", bg = "bisque")
text_path_client.grid(row = 0 , column = 0)

path_client = StringVar()
path_client.set("Clients_list_example.csv")	
# variable of the entry set as normal to point my client list

entry_path_client = Entry (frame1, textvariable = path_client)
entry_path_client.grid(row = 0, column = 1 )

browse_button_client = Button(frame1, text = "Browse", command = select_file)
browse_button_client.grid(row = 0, column = 2)
# button linked to the select_file function

text_space1 = Label (frame1, text = "\n", bg = "bisque")
text_space1.grid (row = 1, column = 0, columnspan = 3)

open_csvfile()	

	
frame1.grid(row = 1, column = 0, columnspan = 2)
			
			
#-------------------frame2 : Creation of checked list box with scrollbar

frame2 = Frame(Frame_Canvas)
frame2['bg'] = "bisque"

text_frame2 = Label(frame2, text = "Client list to select ", bg= "bisque")
text_frame2.pack(side = "top")

sb = Scrollbar(frame2, orient = "vertical")
text = Text(frame2, width = 15, height = 20, yscrollcommand = sb.set)

sb.pack(side = "right", fill = "y")


vars = list()
all_button = []
i = 0

def list_box():
	
	global var, vars, all_button, text
	
	for i in range(len(chart)):
		var = IntVar(value = 0)
		# set the value of checkboxes to 0
		
		cb = Checkbutton(frame2, text = chart[i][0], bg = "white", variable = var, padx = 0, pady = 0, bd = 0)
		vars.append(var)
		# put values into a list
		
		all_button.append(cb)
		# put checkboxes into a list
		
		text.window_create("end", window = cb)
		text.insert("end", "\n") 
	text.pack(side = "top", fill = "both",expand = True)
	sb.config(command = text.yview)
	# insert all checkboxes to the text with it's scrollbar

list_box()



frame2.grid(row = 2, column = 0, rowspan = 2)

		
		
		
#------------------------frame3 : Creation of legend


frame3 = Frame(Frame_Canvas)
frame3["bg"] = "bisque"

text_frame3 = Label(frame3, text = "Legend : \n ", bg = "bisque")
text_frame3.grid(row = 0, column = 0, columnspan = 2)
frame_black = Canvas(frame3, width = 8, height = 8)
frame_black["bg"] = "bisque"
rect_black = frame_black.create_rectangle(8,0,8,0, fill = "black", outline = "black", width = 16)
frame_black.grid(row = 1, column = 0)
text_black = Label(frame3, text = "Client down", bg = "bisque")
text_black.grid(row = 1, column = 1)

frame_orange = Canvas(frame3, width = 8, height = 8)
frame_orange["bg"] = "bisque"
rect_orange = frame_orange.create_rectangle(8,0,8,0, fill = "orange", outline = "orange", width = 16)
frame_orange.grid(row = 2, column = 0)
text_orange = Label(frame3, text = "Client awake", bg = "bisque")
text_orange.grid(row = 2, column = 1)

frame_green = Canvas(frame3, width = 8, height = 8)
frame_green['bg'] = 'bisque'
rect_green = frame_green.create_rectangle(8,0,8,0, fill = "black", outline = "green", width = 16)
frame_green.grid(row = 3, column = 0)
text_green = Label(frame3, text = "Client ready", bg = "bisque")
text_green.grid(row = 3, column = 1)

frame_red = Canvas(frame3, width = 8, height = 8)
frame_red['bg'] = 'bisque'
rect_red = frame_red.create_rectangle(8,0,8,0, fill = "red", outline = "red", width = 16)
frame_red.grid(row = 4, column = 0)
text_red = Label(frame3, text = "Client busy", bg = "bisque")
text_red.grid(row = 4, column = 1)


frame3.grid(row = 2, column = 1)




#------------------------frame4 : Creation of Button select/deselect

frame4 = Frame(Frame_Canvas)
frame4["bg"] = "bisque"

Button(frame4, text = "Select all", command = select_all).pack()
# button linked to the select_all function

Button(frame4, text = "Deselect all", command = deselect_all).pack()
# button linked to the deselect_all function

frame4.grid(row = 3, column = 1)


#------------------------frame5 : Creation of entry text

frame5 = Frame(Frame_Canvas)
frame5["bg"] = "bisque"

nc = 0

text_number_checked = Label(frame5, text = "\n Number of client selected : %s"  % nc, bg = "bisque")
text_number_checked.grid(row = 0, column = 0, columnspan = 2)

button_refresh = Button(frame5, text = "refresh", command = check_box)
button_refresh.grid(row = 0, column = 2)
# button linked to the check_box function to uptdate nc =  number of client selected

text_choice = Label(frame5, text = "Total of client to awake divise by ", bg = "bisque")
text_choice.grid (row = 1, column = 0)

nb = IntVar()
nb.set(3)
# variable of the entry widget set at 3

entry = Entry(frame5,textvariable = nb, width = 15)
entry.grid(row = 1, column = 1)

text_min = Label (frame5, text = "(min = 3)", bg = "bisque")
text_min.grid (row = 1, column = 2)

text_space = Label (frame5, text = "\n", bg = "bisque")
text_space.grid (row = 2, column = 0, columnspan = 3)

frame5.grid(row = 4, column = 0, columnspan = 2)



#------------------------frame6 : Creation of wake-up/shut-down button


frame6 = Frame(Frame_Canvas)
frame6["bg"] = "bisque"		

button1 = Button(frame6, text = "wake up", command = wake_up) 						   
button1.grid(row = 0, column = 0) 
# button linked to the wake_up function

button2 = Button(frame6, text = "Shut down", command = shut_down) 					  
button2.grid(row = 0, column = 1) 
# button linked to the shut down function

text_space2 = Label (frame6, text = "\n", bg = "bisque")
text_space2.grid (row = 1, column = 0, columnspan = 2)

frame6.grid(row = 5 , column = 0 , columnspan = 2)


#------------------------frame7 : Creation of sart/end task button


frame7 = Frame(Frame_Canvas)
frame7["bg"] = "bisque"

text_path = Label( frame7, text = "Select your task file : ", bg = "bisque")
text_path.grid(row = 0 , column = 0)

file_path = StringVar()
entry_path = Entry (frame7, textvariable = file_path)
entry_path.grid(row = 0, column = 1 )

browse_button = Button(frame7, text = "Browse", command = slot_browse)
browse_button.grid(row = 0, column = 2)
# button linked to the slot_browse function

button_task = Button(frame7, text = 'Start Task', command = start_task)
button_task.grid(row  = 1, column = 2)
# button linked to the start_task function

button_etask = Button(frame7, text = 'End Task', command = end_task)
button_etask.grid(row  = 1, column = 3)
# button linked to the end_task function

text_space3 = Label (frame7, text = "\n", bg = "bisque")
text_space3.grid (row = 1, column = 0, columnspan = 3)

frame7.grid(row = 6 , column = 0, columnspan = 2)


#------------------------frame8: Creation of event_log

frame8 = Frame(Frame_Canvas)
frame8 ["bg"] = "bisque"

text_frame8 = Label(frame8, text = "Event log : ", bg= "bisque")
text_frame8.pack(side = "top")

sb2 = Scrollbar(frame8, orient = "vertical")
text_box = Text(frame8, yscrollcommand = sb2.set) 

sb2.pack(side = "right", fill = "y")
# configuration of the scrollbar

event("Event log start.")

frame8.grid(row = 7, column = 0, columnspan = 2)



#---------------------- END

text_space4 = Label (Frame_Canvas, text = "\n", bg = "bisque")
text_space4.grid(row = 8, column = 0, columnspan = 2)


button3 = Button(Frame_Canvas, text = "Quit", command = Window.destroy) 						   
button3.grid(row = 9, column = 1) 		

event("Window launch")
	
ready()
busy()			


Canvas_sb.create_window(0,0,  window = Frame_Canvas)
Frame_Canvas.update_idletasks()
Canvas_sb.config(scrollregion = Canvas_sb.bbox("all"))	

Window.mainloop()


