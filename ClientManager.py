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
import tkMessageBox 
import os
import subprocess
import webbrowser
import MySQLdb

from subprocess import call
from Tkinter import *
from MySQLdb.constants import FIELD_TYPE


 












#------------------------DEFINITIONS


chart =[]
# chart of data from the csv file (Hostname, Mac adress, IP adress)

status = []
# chart of client status (checkbox, awake/idle, busy)

status_name = []

vardb = 0
server = "mysql.fr"
DB = "databasename"
user1 = "username"
pwd = "passwordL"
site = "site"
experiment = "experimentname"
user2 = "username"

#-------------------------- Event



def event(var):
	# function use to show to the user what the code is doing 
	
	
	text_event = Label(frame8, text = var, bg = "white")
	# var is the text argument
	
	text_box.window_create("end", window = text_event)
	text_box.insert("end", "\n") 
	# insert the text in the text_box with the scrollbar
	
	
	
	
	sb2.config(command = text_box.yview)
	sb3.config(command = text_box.xview)
	
	
	text_box.see(END)
	# configuration for the scrollbar








#--------------------------Check client's status



def idle(client):
	# function to check if the clients are idle
	
	
	
	
	
		
	if status[client][1] != "1":
			
		output_ping = os.popen ("fping -c1 %s &" % chart[client][2], "r").readline()
		# first send a basic ping to see if it's awake or not
		event("Sending ping to %s ..." % chart[client][0])
			
		if output_ping.find("0% loss") != -1:
			output_X11 = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s 'ps aux | grep X' &" % chart[client][0], "r").read()
			# if it's awake search for any the X11 (= Client idle)
				
			if output_X11.find("/usr/bin/X") != -1:
				all_button[client].configure(fg = "green")
				# if it's idle put the hostname in green 
				status[client][1] = 1
				# and complete the status chart (1 = idle)
					
			else:
				status[client][1] = 0
				# complete the status chart (O = awake but not idle)
					
				all_button[client].configure(fg = "orange")
				# put the hostname client as orange
					
		else:
			status[client][1] = -1
			all_button[client].configure(fg = "black")
			# if client is down then let it black 
			# complete the status chart (-1 = down)
				
	
			




	
def busy(client):
	
	
	support_task = var_sup.get()
	
	
	
		
	if status[client][1] == "1":
		# only if client is awake and idle check if octave is running
		# if a client is only awake it couldn't be busy
			
		output_busy = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s 'ps aux | grep %s' " % (chart[client][0], support_task), "r").read()
		event("Sending busy question...")
			
		if output_busy.find("xterm -e %s" % support_task) != -1:
			all_button[client].configure(fg = "red")
			# if it's busy put the hostname as red
				 
			status[client][2] = 1
			# complete the status chart (1 = busy)
				
		else:
			all_button[client].configure(fg = "green")
			status[client][2] = 0
			# complete the status chart (0 = idle but not busy)
	else:
		all_button[client].configure(fg = "black")
		status[client][2] = -1
		#complete the status chart (-1 = not idle)
	
			
#---------------------------Verification of which box is checked


def check_box():
	# function to count and complete the status chart
	
	global nc, status
	
	var0= 0
	
	for v in vars:
		status[var0][0] = v.get() 
		var0 = var0 + 1  
		# put all value of checkboxes in the status chart 
	
	box = 0	
	number_checked = 0
	
	for box in range(len(status)):
		
		if status[box][0] == "1":
			number_checked = number_checked + 1
			# counting number of checkboxes selected
	
	nc = number_checked
	return nc
	event("Check box done.")
	text_number_checked.config(text = "\n Number of client selected : %s" % nc)
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


#---------------------------- Definition of counting

nb_idle = 0

def counting():
	
	global nb_idle
	client = 0
	nb_idle = 0
	for client in range(len(status)):
		
		if status[client][1] == '1':
			if status[client][0] == '1':
				nb_idle= nb_idle + 1
				# counting number of client idle
	return nb_idle
	event("Number of idle client : %s" % nb_idle)
#----------------------------Defnition of wake_up fonction 



def wake_up():
	# function to wake up selected clients
	# server may be slow so it may need to divise the total to wake up
	
	global number_awake
	
	client = 0
	event("Wake-up")
	nc = check_box()
	
	event("Checking idle clients...")
	for client in range(len(chart)):
		if status[client][0] == '1':
			idle(client)
	event("Check idle client done.")		
	# to wake only down client
	  
	entry_nb = int (nb.get())
	# get the x of "wake up x by x"
	n = 0	
	number_awake = 0
			
	for n in range(len(chart)):
		
		if status[n][0] == "1" and status[n][1] == "-1":
				
			output_awake = os.popen("awake %s" % chart[n][1], "r").readline()
			# send the magic packet to wake up client
				
			event ("Sending magic packets to %s" % chart[n][0])
			print("Sending magic packets to %s" % chart[n][0])	
			if output_awake.find("Sending") == 0:
				all_button[n].configure(fg = "orange")
				# if it's weel done then put hostname orange
				status[n][1] = 0
			number_awake = number_awake + 1
			
				
			if number_awake == entry_nb:
				
				nb_idle = counting()
				
				event("Checking idle clients...")
				while nb_idle < number_awake:
					for client in range(len(chart)):
						if status[client][0] =='1':
							idle(client)	
					
					nb_idle = counting()
					print ("%s left to be idle." % (nc - nb_idle))
				event("Check idle client done.")	
					# wait until all client selected are idle
				number_awake = number_awake - 1
				
	
	client = 0
	
	event("Checking idle clients...")
	for client in range(len(chart)):
		if status[client][0] == '1':
			idle(client)	
	nb_idle = counting()
	
	while nb_idle != nc:
		for client in range(len(chart)):
			if status[client][0] == '1':
				idle(client)
			
		nb_idle = counting()	
		event("%s left to be idle." % (nc - nb_idle))
		print ("%s left to be idle." % (nc - nb_idle))		
	event("Check idle client done.")
	event("Clients awake.")	
		
		
			
				
				
				
		
	
	
#---------------------------Definition of shut_down fonction

def shut_down():
	# function to shut_down clients selected
	
	event("Shut down")
	check_box() 
	client=0
	
	for client in range(len(chart)):
		
		if status[client][0] == "1":
			# it can only work on idle clients
			
			call(["ssh", "-q", "-o", "UserKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=no", "-f", "neurodebian@%s" % chart[client][0],"''sudo poweroff''"])
			# send a ssh command to shut down
			
			event("Sending shut down command to %s" % chart[client][0])
			all_button[client].configure(fg = "black")
			#  put the hostname black
			
			status[client][1] = -1
			# complete the status chart
			
	event("Shut down done.")	
			

#-------------------------- Definition of slot_browse

def slot_browse():
	#function to get the file path of the task experiment file selected
	
	global file_path
	
	_fpath = tkFileDialog.askopenfilename()
	# open the TkFileDialog so that user can choose his file
	
	file_path.set(_fpath)

	basename_task =	os.path.basename(file_path.get())
	text_path.config(text = "Task file selected : %s " % basename_task)
	event("Task file selected.")
	
	


#-------------------------Open file

def open_csvfile():
	# client to open the client list file and set status and chart chart
	global chart, status, status_name
	
	file_name = str(path_client.get())			
	file_open = open (file_name, "rb")	
	# open the file and read it
	
	
	
	chart = np.loadtxt(file_open, dtype = str, delimiter = ",")	
	# put the data into a chart and see them as a string
	
	status = np.copy(chart)
	status_name = np.copy(chart)
	
	
	
	
#--------------------------Definition of select-file

def select_file():
	#function to get the file path of the client list file selected
	
	global path_client, vars, all_button
	
	path_file = tkFileDialog.askopenfilename(filetypes = [("Fichier csv", "*.csv")])
	# open the TkFileDialog so that user can choose his file
	
	(path_client).set(path_file)
	text_path_client.config(text = "Client list file selected : %s " % path_client.get())
	open_csvfile()
	text.delete("0.0", END)
	# delete what was in the text that countain list of checkboxes
	
	del(vars[:])
	del(all_button[:])
	# delete the list value and the list of checkboxes
	
	list_box()
	# recreate the new listbox with the new data
	Refresh()
	Window.update()
	# refresh
	
	
	
	
	
#------------------------- Definition of start_task


def start_task():
	# function to launch a task
	global int2, status_name
	
	event("Start task")
	
	check_box()
	support_task = var_sup.get()
	entire_path = file_path.get()
	
	if entire_path.find("/nfsroot/experiments/") != -1:
		split_path = entire_path.split("/")
		split_path[1] = 'media'
		join_path = "/".join(split_path)
		path_task = join_path
	
	else:
		path_task = file_path.get()
	
		
	dirname_task = os.path.dirname(path_task) 
	basename_task =	os.path.basename(path_task)
	basename_task = basename_task.split('.')
	basename_task.remove(basename_task[1])
	
	client = 0
	stat_db = vardb
	
	
		
	if stat_db == 1:
		
		event("Start task using database")
		
		my_conv = { FIELD_TYPE.LONG: int }
		database = MySQLdb.connect(server, user1, pwd, DB, conv= my_conv)
		cursor = database.cursor()
		
		add_session = ("INSERT INTO session (User, Experiment, Site)  VALUES ('%s','%s', '%s')" % (user2, experiment, site))
		cursor.execute(add_session)
		database.commit()
		
		event ("Database session created")
		
		select_session = ("SELECT MAX(SessionID) FROM session")
		cursor.execute(select_session)
		nb_session = cursor.fetchall()
		int1 = reduce(lambda rst, d: rst * 10 + d, nb_session)
		int2 = reduce(lambda rst, d: rst * 10 + d, int1)
		
		
		
		for client in range(len(chart)):
			
			status_name[client][2] = chart[client][0].lower()
			
			
			if status[client][0] == "1":
				if status[client][1] == "1":
					status_name[client][0] = "IDDLE"
				if status[client][1] == "0":
					status_name[client][0] = "AWAKE"
				if status[client][1] == "-1":
					status_name[client][0] = "SLEEPY"	
			
				
				add_subject = ("INSERT INTO subjects (Hostname, Session, TriggerCode, Status)  VALUES ('%s', '%s', '%s', '%s')" % (status_name[client][2], int2, (client +1), status_name[client][0]))
				cursor.execute(add_subject)
				database.commit()
				select_hostname = ("SELECT MAX(SubjectID) FROM subjects")
				cursor.execute(select_hostname)
				nb_hostname = int(cursor.fetchone()[0])
				
				status_name[client][1] = nb_hostname
				
				event("Database subjects created")
				print("Database subjects created")
		for client in range(len(chart)):
			
			if status[client][0] == '1' and status[client][1] == '1':
				
				output_start = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s 'export DISPLAY=:0; cd %s; pwd; xterm -e %s --eval %s' " % (chart[client][0], dirname_task, support_task, basename_task[0]))
				
				# if client are idle then launch the ..
				# .. task file to clients selected
				busy(client)
				event("Task %s send to %s." % (file_path.get(), chart[client][0]))
				print ("Task %s send to %s." % (file_path.get(), chart[client][0]))
		event("Checking busy clients...")
	
		for client in range(len(chart)):	
			while status[client][0] == "1" and status[client][2] != "1":
				busy(client)
				
		event("Check busy clients done.")
		# check if they're busy
				
		for client in range(len(chart)):		
			if status[client][0] == "1":
				if status[client][2] == "1":
					status_name[client][0] = "BUSY"
				
				update_subject = ("UPDATE subjects SET Status = '%s' WHERE SubjectID = '%s' " % (status_name[client][0], status_name[client][1]))
				cursor.execute(update_subject)
				database.commit()
		database.close()
	
	else:
		for client in range(len(chart)):
			if status[client][1] == '1' and status[client][1] == '1':
				output_start = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s 'export DISPLAY=:0; cd %s; pwd; xterm -e %s --eval %s' " % (chart[client][0], dirname_task, support_task, basename_task[0]), "r").read()
				# if client are idle then launch the ..
				# .. task file to clients selected
				busy(client)
				event("Task %s send to %s." % (file_path.get(), chart[client][0]))
				print("Task %s send to %s." % (file_path.get(), chart[client][0]))
		event("Checking busy clients...")
	
		for client in range(len(chart)):
			while status[client][0] == "1" and status[client][2] != "1":
				busy(client)
				# check if they're busy
		event("Check busy clients done.")




#------------------------- Definition of end_task	
	
	
def end_task():
	# function to kill all tasks
	
	global status_name
	
	client = 0
	support_task = var_sup.get()
	path_task = file_path.get()
	basename_task =	os.path.basename(path_task)

	for client in range(len(chart)):
		
		if status[client][1] == '1' and status[client][0] == '1':
			output_X11 = os.popen("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -f neurodebian@%s '' killall -9 %s '' &" % (chart[client][0], support_task), "r").read()
			# if clients are idle then kill ALL task so that it isn't busy anymore
			busy(client)	
			idle(client)
			event("Task end command send to %s" % chart[client][0])
	
	for client in range(len(chart)):
		while status[client][0] == "1" and status[client][2] == "1":
			busy(client)
			# check if they're busy
	
	stat_db = vardb
	
	
	if stat_db == '1':
		
		my_conv = { FIELD_TYPE.LONG: int }
		database = MySQLdb.connect(server, user1, pwd, DB, conv= my_conv)
		cursor = database.cursor()
		
		for client in range(len(chart)):		
			if status[client][0] == "1":
				if status[client][2] == "0":
					status_name[client][0] = "IDLE"
				
				update_subject = ("UPDATE subjects SET Status = '%s' WHERE SubjectID = '%s' " % (status_name[client][0], status_name[client][1]))
				cursor.execute(update_subject)
				database.commit()	
				
				event("Database subject status update")		
		database.close()
	event("Tasks end.")
		

#------------------------ Definition of web_wiki

def web_wiki():
	webbrowser.open('https://github.com/marie-aguirre/Client-Manager/wiki')

	

#------------------------ Definition of about

def about():
	About = Toplevel()
	About.title("About")
	About["bg"] = "bisque"

	event("About.")

	text_about = Label (About, text = "\n Client manager \n Release on November 2014 by Marie Aguirre  \n\n  Version 1.2 \n", bg = "bisque")
	text_about.pack()
	
	
	
	web_button  = Button( About, text = "https://github.com/marie-aguirre/Client-Manager/wiki", command = web_wiki)
	web_button.pack()
	
	About.mainloop()



#---------------------- Definition of help_cm

def help_cm():
	webbrowser.open('https://github.com/marie-aguirre/Client-Manager/wiki/4.How-to-use')
	

#---------------------- Definition of save_config


def save_config():
	
	event("Database settings modify")
	
	global vardb, server, DB, user1, pwd, site, experiment, user2
	
	vardb = var_db.get()
	server = server_config.get()
	DB = DB_config.get() 
	user1 = user1_config.get() 
	pwd = pwd_config.get() 

	site = site_config.get() 
	experiment = experiment_config.get() 
	user2 = user2_config.get()
	
	
	
	


#----------------------Definition of save_support

def save_support():
	
	event("Suport setting modify")
	
	global support_task
	
	support_task = var_sup.get()
	
	
	

	






#------------------------Definition of handler

def handler_win():
    if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
        Window.destroy()
        




#----------------------- Definition of refresh

def Refresh():
	
	event("Refresh Status")
	
	event("Checking idle clients...")
	event("Checking busy clients...")
	
	for client in range(len(chart)):
		idle(client)
		busy(client)
	event("Check idle client done.")
	event("Check busy clients done.")





#------------------------ Config




   
def Config():
	
	global var_db, server_config, DB_config, user1_config, pwd_config 
	global site_config, experiment_config, user2_config
	
	event("Config")
	
	Config = Toplevel()
	

	Config.title("Settings menu")
	Config["bg"] = "bisque"



	text_spa = Label (Config, text = "\n ", bg = "bisque")
	text_spa.grid(row = 0, column = 0, columnspan = 2)

	
	cb_database = Checkbutton(Config, text = "use a Database", variable = var_db, bg = "bisque")
	cb_database.grid(row = 1, column = 0)

	text_spa = Label (Config, text = "\n --- \n", bg = "bisque")
	text_spa.grid(row = 2, column = 0, columnspan = 2)	

	
	text_config = Label(Config, text = "Parameters to reach the database",
	bg = "bisque")
	text_config.grid(row = 3, column = 0)	
	
	text_spa2 = Label (Config, text = "\n ", bg = "bisque")
	text_spa2.grid(row = 4, column = 0, columnspan = 2)

	text_server = Label(Config, text = "Server name :", bg = "bisque")
	text_server.grid(row = 5, column = 0)
	
	
	entry_server = Entry(Config,textvariable = server_config)
	entry_server.grid(row = 5, column = 1)
	
	text_DB = Label(Config, text = "DataBase name :", bg = "bisque")
	text_DB.grid(row = 6, column = 0)
	
	
	entry_DB = Entry(Config,textvariable = DB_config)
	entry_DB.grid(row = 6, column = 1)
	
	text_user = Label(Config, text = "User :", bg = "bisque")
	text_user.grid(row = 7, column = 0)
	
	
	entry_user = Entry(Config,textvariable = user1_config)
	entry_user.grid(row = 7, column = 1)
	
	text_pwd = Label(Config, text = "Password :", bg = "bisque")
	text_pwd.grid(row = 8, column = 0)
	
	
	entry_pwd = Entry(Config,textvariable = pwd_config)
	entry_pwd.grid(row = 8, column = 1)
	
	text_spa3 = Label (Config, text = "\n --\n ", bg = "bisque")
	text_spa3.grid(row = 9, column = 0, columnspan = 2)
	
	text_write = Label (Config, 
	text = "Parameter writing in the data base session ",
		bg = "bisque")
	text_write.grid(row = 10, column = 0)
	
	text_site = Label(Config, text = "Site :", bg = "bisque")
	text_site.grid(row = 11, column = 0)
	
	
	entry_site = Entry(Config,textvariable = site_config)
	entry_site.grid(row = 11, column = 1)
	
	
	text_experiment = Label(Config, text = "Experiment :", 
		bg = "bisque")
	text_experiment.grid(row = 12, column = 0)
		
	
	entry_experiment = Entry(Config, textvariable = experiment_config)
	entry_experiment.grid(row = 12, column = 1)
	
	text_user2 = Label(Config, text = "User :", bg = "bisque")
	text_user2.grid(row = 13, column = 0)
		
	
	entry_user2 = Entry(Config,textvariable = user2_config)
	entry_user2.grid(row = 13, column = 1)
	
	
	text_spa4 = Label (Config, text = "\n  ", bg = "bisque")
	text_spa4.grid(row = 14, column = 0, columnspan = 2)
	
	
	
	OK_button = Button (Config, text = "Save", command = save_config)
	OK_button.grid(row = 15, column = 0)
	
	cancel_button = Button(Config, text = "Cancel", 
		command = Config.destroy) 
	cancel_button.grid(row = 15, column = 1)
	
	Config.mainloop()






#------------------------ Support



def Support():
	
	global var_sup
	
	event("Support")
	
	Support = Toplevel()
	Support.title("Choice of Support")
	Support["bg"] = "bisque"
	
	
	text_spac = Label (Support, text = "\n ", bg = "bisque")
	text_spac.grid(row = 0, column = 0, columnspan = 2)
	
	text_support = Label (Support, text = "Support of your task : ", 
		bg = "bisque")
	text_support.grid(row = 1, column = 0)

		
	entry_support = Entry(Support, textvariable = var_sup)
	entry_support.grid(row = 1, column = 1)
	
	text_spac2 = Label (Support, text = "\n ", bg = "bisque")
	text_spac2.grid(row = 2, column = 0, columnspan = 2)
		
	
	OK_button = Button (Support, text = "Save", command = save_support)
	OK_button.grid(row = 3, column = 0)
	
	
	cancel_button = Button(Support, text = "Cancel",
		command = Support.destroy) 
	cancel_button.grid(row = 3, column = 1)
	
	Support.mainloop()
	





#-------------------------- Group

def Group():
	
	global nb
	
	event("Awaking group number")
	
	Group = Toplevel()
	Group.title("Awaking Group number")
	Group["bg"] = "bisque"
	
	
	text_spac = Label (Group, text = "\n ", bg = "bisque")
	text_spac.grid(row = 0, column = 0, columnspan = 2)
	
	text_choice = Label(Group, text = "Max awaking client group :", bg = "bisque")
	text_choice.grid (row = 1, column = 0)

	
	entry = Entry(Group, textvariable = nb, width = 3)
	entry.grid(row = 1, column = 1)

	text_min = Label (Group, text = "(min = 3)", bg = "bisque")
	text_min.grid (row = 2, column = 1)
		
	text_spac2 = Label (Group, text = "\n ", bg = "bisque")
	text_spac2.grid(row = 3, column = 0, columnspan = 2)
		
	
		
	OK_button = Button(Group, text = "OK",
		command = Group.destroy) 
	OK_button.grid(row = 4, column = 0)
	
	Group.mainloop()










			
			
#--------------------------WINDOWS'S CREATION		





#-----------------------Creation of window

    
Window = Tk()
# create a graphic window
												   
Window.title("Client manager")
Window["bg"] = "bisque"
Window.geometry("430x650+0+0")
Window.protocol("WM_DELETE_WINDOW", handler_win)


#---------------------- Variables

var_db = IntVar(value = 0)

server_config = StringVar()
server_config.set("mysql.fr")

DB_config = StringVar()
DB_config.set("databasename")

user1_config = StringVar()
user1_config.set("username")

pwd_config = StringVar()
pwd_config.set("password")
	

site_config = StringVar()
site_config.set("site")

experiment_config = StringVar()
experiment_config.set("experimetname")

user2_config = StringVar()
user2_config.set("username")

var_sup = StringVar()	
var_sup.set("octave")

nb = IntVar()
nb.set(3)


#---------------------- Menu bar

mainmenu = Menu(Window)  
 
menufile = Menu(mainmenu)  
menufile.add_command(label = "New Client list", command = select_file)
menufile.add_command(label = "New task file", command = slot_browse)
menufile.add_command(label = "Quit", command = handler_win) 



menuconfig = Menu(mainmenu)
menuconfig.add_command(label = "Data Base", command = Config)
menuconfig.add_command(label = " Support of your task ", 
	command = Support)
menuconfig.add_command(label = "Awaking Group number", command = Group)
  
menuHelp = Menu(mainmenu) 
menuHelp.add_command(label = "Help", command = help_cm)
menuHelp.add_command(label = "About", command = about) 
  
mainmenu.add_cascade(label = "File", menu = menufile) 
mainmenu.add_cascade(label = "Settings", menu = menuconfig)
mainmenu.add_cascade(label = "Help", menu = menuHelp) 
  




#----------------------- Scrollbar																   
 

vsb = Scrollbar(Window, orient = VERTICAL)
vsb.grid(row = 0, column = 1, rowspan = 7, sticky = N+S)
hsb = Scrollbar(Window, orient = HORIZONTAL)
hsb.grid(row = 1, column = 0, columnspan = 2, sticky = W+E)
# create a scrollbar for all the Window

Canvas_sb = Canvas(Window, yscrollcommand = vsb.set, xscrollcommand = hsb.set)
# create a canvas because it isn't possible to put a scrollbar on frames

Canvas_sb["bg"] = "bisque"
Canvas_sb.grid(row = 0, column = 0, sticky = "sewn")
vsb.config(command = Canvas_sb.yview)
hsb.config(command = Canvas_sb.xview)

Window.grid_rowconfigure(0, weight = 1)
Window.grid_columnconfigure(0, weight = 1)



Frame_Canvas = Frame(Canvas_sb)
Frame_Canvas["bg"] = "bisque"
# create the big frame in the canvas

	



#------------------- frame 1 : Creation of brows your client list


frame1 = Frame(Frame_Canvas)
frame1["bg"] = "bisque"



path_client = StringVar()
path_client.set("Clients_list.csv")	
# variable of the entry set as normal to point my client list


text_path_client = Label( frame1, 
	text = "\n Client list file selected : %s \n" % os.path.basename(path_client.get()), 
		bg = "bisque", width = 60)
text_path_client.grid(row = 0 , column = 0)

open_csvfile()	

	
frame1.grid(row = 0, column = 0, columnspan = 2)
			
			
#-------------------frame2 : Creation of checked list box with scrollbar

Frame2 = Frame(Frame_Canvas)
Frame2['bg'] = "bisque"

text_frame2 = Label(Frame2, text = "Client list to select ",
	bg= "bisque")
text_frame2.pack(side = "top")

frame2 = Frame(Frame2)
frame2['bg'] = "bisque"

sb = Scrollbar(frame2, orient = "vertical")
sbh = Scrollbar(frame2, orient = "horizontal")
text = Text(frame2, width = 15, height = 16, yscrollcommand = sb.set, xscrollcommand = sbh.set)

sb.pack(side = "right", fill = "y")
sbh.pack(side = "bottom", fill = "x")

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
	sbh.config(command = text.xview)
	# insert all checkboxes to the text with it's scrollbar

list_box()

frame2.pack()

Frame2.grid(row = 1, column = 0, rowspan = 2)

		
		
		
		
#------------------------frame3 : Creation of legend


frame3 = Frame(Frame_Canvas)
frame3["bg"] = "bisque"

text_frame3 = Label(frame3, text = "Legend : \n ", bg = "bisque")
text_frame3.grid(row = 0, column = 0, columnspan = 2)

frame_black = Canvas(frame3, width = 8, height = 8)
frame_black["bg"] = "bisque"
rect_black = frame_black.create_rectangle(8,0,8,0, fill = "black", 
	outline = "black", width = 16)
frame_black.grid(row = 1, column = 0)
text_black = Label(frame3, text = "Client down", bg = "bisque")
text_black.grid(row = 1, column = 1)

frame_orange = Canvas(frame3, width = 8, height = 8)
frame_orange["bg"] = "bisque"
rect_orange = frame_orange.create_rectangle(8,0,8,0, fill = "orange", 
	outline = "orange", width = 16)
frame_orange.grid(row = 2, column = 0)
text_orange = Label(frame3, text = "Client awake", bg = "bisque")
text_orange.grid(row = 2, column = 1)

frame_green = Canvas(frame3, width = 8, height = 8)
frame_green['bg'] = 'bisque'
rect_green = frame_green.create_rectangle(8,0,8,0, fill = "black", 
	outline = "green", width = 16)
frame_green.grid(row = 3, column = 0)
text_green = Label(frame3, text = "Client idle", bg = "bisque")
text_green.grid(row = 3, column = 1)

frame_red = Canvas(frame3, width = 8, height = 8)
frame_red['bg'] = 'bisque'
rect_red = frame_red.create_rectangle(8,0,8,0, fill = "red",
	outline = "red", width = 16)
frame_red.grid(row = 4, column = 0)
text_red = Label(frame3, text = "Client busy", bg = "bisque")
text_red.grid(row = 4, column = 1)


frame3.grid(row = 1, column = 1)




#------------------------frame4 : Creation of Button select/deselect

frame4 = Frame(Frame_Canvas)
frame4["bg"] = "bisque"

Button(frame4, text = "Select all", command = select_all).pack()
# button linked to the select_all function

Button(frame4, text = "Deselect all", command = deselect_all).pack()
# button linked to the deselect_all function

frame4.grid(row = 2, column = 1)


#------------------------frame5 : Creation of entry text

frame5 = Frame(Frame_Canvas)
frame5["bg"] = "bisque"

refresh = Button(frame5, text = "Refresh status", command = Refresh)
refresh.pack()

frame5.grid(row = 3, column = 0, columnspan = 2)



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

frame6.grid(row = 4 , column = 0 , columnspan = 2)


#------------------------frame7 : Creation of sart/end task button


frame7 = Frame(Frame_Canvas)
frame7["bg"] = "bisque"


file_path = StringVar()
file_path.set("    ")

text_path = Label( frame7, text = "Task file selected: %s" % os.path.basename(file_path.get()), bg = "bisque")
text_path.grid(row = 0 , column = 0)

button_task = Button(frame7, text = 'Start Task', command = start_task)
button_task.grid(row  = 1, column = 0)
# button linked to the start_task function

button_etask = Button(frame7, text = 'End Task', command = end_task)
button_etask.grid(row  = 1, column = 1)
# button linked to the end_task function

text_space3 = Label (frame7, text = "\n", bg = "bisque")
text_space3.grid (row = 1, column = 0, columnspan = 2)

frame7.grid(row = 5 , column = 0, columnspan = 2)


#------------------------frame8: Creation of event_log

Frame8 = Frame(Frame_Canvas)
Frame8 ["bg"] = "bisque"

text_Frame8 = Label(Frame8, text = "\n Event log : ", bg= "bisque")
text_Frame8.pack(side = "top")

frame8 = Frame(Frame8)
frame8 ["bg"] = "bisque"

sb2 = Scrollbar(frame8, orient = "vertical")
sb3 = Scrollbar(frame8, orient = "horizontal")

text_box = Text(frame8, height = 8,width = 40, yscrollcommand = sb2.set, xscrollcommand = sb3.set ) 
text_box.grid(row = 0, column = 0, sticky=N+S+E+W)
 
sb3.grid(row = 1, column = 0, sticky = E+W)
sb2.grid(row = 0, column = 1, sticky = N+S)

# configuration of the scrollbar

frame8.grid_rowconfigure(0, weight=1)
frame8.grid_columnconfigure(0, weight=1)

frame8.pack()

event("Event log start.")

Frame8.grid(row = 6, column = 0, columnspan = 2)



#---------------------- END


stat_db = vardb
int2 = 0

	
	
	

event("Window launch.")
	
		


Canvas_sb.create_window(0,0,  window = Frame_Canvas)
Frame_Canvas.update_idletasks()
Canvas_sb.config(scrollregion = Canvas_sb.bbox("all"))	

Window.config(menu = mainmenu)


event("Checking idle clients...")
event("Checking busy clients...")
	
for client in range(len(chart)):
	idle(client)
	busy(client)
event("Check idle client done.")
event("Check busy clients done.")

Window.mainloop()







