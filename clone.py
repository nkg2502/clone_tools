import string
import os
import glob
from Tkinter import *

# use command 'net use'
def connect_path(drive_letter, path):
	cmd = 'net use {} {}'.format(drive_letter, path)
	os.system(cmd)

# use command 'net use'
def disconnect_path(drive_letter):
	cmd = 'net use {} /delete'.format(drive_letter)
	os.system(cmd)

def get_path():
	path = ''
	try:
		path = open('path.txt').readline()
	except:
		pass

	user_input = raw_input('path[{}]: '.format(path))

	return user_input.rstrip() if user_input.rstrip() else path

def get_build_id(path):
	return path.split('\\')[-1]


# find drive letter
def get_drive_letter():

	# string.ascii_uppercase[-1:1:-1] == 'ZYXWVUTSRQPONMLKJIHGFEDC'
	for letter in string.ascii_uppercase[-1:1:-1]:
		is_used_letter = glob.glob(letter + ':')
		if not is_used_letter:
			return letter + ':'

	return None

def get_files(dst, src, files):
	cmd = 'robocopy {} {} {} /e'.format(dst, src, files)
	os.system(cmd)

# MAIN
drive_letter = get_drive_letter()
if None == drive_letter:
	print 'Fatal: EVERY DRIVE LETTER USED'
	sys.exit(1)

path = get_path()
if '' == path:
	print 'Fatal: NO PATH'
	sys.exit(2)

print path
os.mkdir(get_build_id(path))

connect_path(drive_letter, path)

get_files(drive_letter, get_build_id(path), '*')

disconnect_path(drive_letter)

