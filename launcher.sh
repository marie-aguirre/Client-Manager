#!/usr/bin/expect -f 

spawn -noecho bash
expect "$ "
send "cd /path\n"
send "sudo python ClientManager.py\n"
interact
