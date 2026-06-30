RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'
banner = r"""
 ___      _   _               _              
| _ \_  _| |_| |_  ___ _ _   | |   ___  __ _ 
|  _/ || |  _| ' \/ _ \ ' \  | |__/ _ \/ _` |
|_|  \_, |\__|_||_\___/_||_| |____\___/\__, |
     |__/                              |___/ 
   _             _                 
  /_\  _ _  __ _| |_  _ ______ _ _ 
 / _ \| ' \/ _` | | || |_ / -_) '_|
/_/ \_\_||_\__,_|_|\_, /__\___|_|  
                   |__/            
Creator: Alon Agronov | Student NO:s16 | XE105 | Lecturer: Natalie Erez
"""
print(f"{CYAN}{banner}{RESET}")
print('=' * 70)

commands = []
new_users = []
del_users = []
p_change = []
su = []
failed_sudo = []
with open('/var/log/auth.log') as f:
	for line in f:
		if 'COMMAND=' in line and ('NOT in sudoers' in line or 'incorrect password' in line):
			timestamp = line.split()[0]
			post_sudo = line.split('sudo:', 1)[1]
			active_user = post_sudo.split(' : ', 1)[0].strip()
			command = line.split('COMMAND=', 1)[1].strip()
			if 'NOT in sudoers' in line:
				reason = "NOT in sudoers"
			else:
				reason = "wrong password"
			row = f"\033[91mALERT!\033[0m {timestamp:<35}{active_user:<15}{reason:<20}{command}"
			failed_sudo.append(row)
		elif 'COMMAND=' in line:
			fields = line.split()
			timestamp = fields[0]
			after_sudo = line.split('sudo:', 1)[1]
			User = after_sudo.split(' : ', 1)[0]
			Ex_User = User.strip()
			command = line.split('COMMAND=', 1)[1].strip()
			row = f"{timestamp:<35}{Ex_User:<20}{command}"
			commands.append(row)
		elif 'new user:' in line:
			fields = line.split()
			timestamp = fields[0]
			after_name = line.split('name=', 1)[1].split(',', 1)[0].strip()
			row = f"{timestamp:<35}{after_name}"
			new_users.append(row)
		elif 'delete user' in line:
			fields = line.split()
			timestamp = fields[0]
			after_del = line.split('delete user', 1)[1].strip(" '\n")
			row = f"{timestamp:<35}{after_del}"
			del_users.append(row)
		elif 'password changed for' in line:
			fields = line.split()
			timestamp = fields[0]	
			username = line.split('password changed for', 1)[1].strip()
			row = f"{timestamp:<35}{username}"
			p_change.append(row)
		elif 'su[' in line and '(to ' in line:
			fields = line.split()
			timestamp = fields[0]
			target = line.split('(to ', 1)[1].split(')', 1)[0].strip()
			from_user = line.split(') ', 1)[1].split(' on', 1)[0].strip()
			row = f"{timestamp:<35}{from_user:<20}{target}"
			su.append(row)


print("=== Commands Used ===")
print(f"{'Timestamp:':<35}{'Executing User:':<20}{'Command Used:'}")
for row in commands:
	print(row)

print("\n=== New Users ===")
print(f"{'Timestamp:':<35}{'New User:'}")
for row in new_users:
    print(row)  
    
print("\n=== Deleted Users ===")
print(f"{'Timestamp:':<35}{'Deleted Users:'}")
for row in del_users:
    print(row)


print("\n=== Password Changes ===")
print(f"{'Timestamp:':<35}{'User:'}")
for row in p_change:
    print(row)
    
    
print("\n=== su Usage ===")
print(f"{'Timestamp:':<35}{'From User:':<20}{'To User:'}")
for row in su:
    print(row)

print("\n=== FAILED Sudo ===")
print(f"       {'Timestamp:':<35}{'User:':<15}{'Reason:':<20}{'Command:'}")
for row in failed_sudo:
    print(row)
