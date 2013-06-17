import string
import os
import glob
from Tkinter import *

class PathDialog:

	def __init__(self, root):

		root.geometry('1000x100')
		root.resizable(0, 0)

		# key bind
		root.bind('<Return>', self.write_path_file)
		root.bind('<Escape>', self.cancel)

		frame = Frame(root)
		frame.pack(fill=BOTH, expand=1)

		path_entry = Entry(frame, font='Consolas 14')

		path_entry.insert(0, self.read_path_file())
		path_entry.focus_set()
		path_entry.select_range(0, END)

		path_entry.pack(side=TOP, fill=X)

		Button(frame, text='Cancel', font='Consolas 10', command=self.cancel).pack(side=RIGHT)
		Button(frame, text='  OK  ', font='Consolas 10', command=self.write_path_file).pack(side=RIGHT)

		self.root = root
		self.path_entry = path_entry

		root.mainloop()
	
	def write_path_file(self, event=None):
		path_file = open('path.txt', 'w')
		path_file.write(self.path_entry.get())

		self.cancel()
	
	def read_path_file(self):

		path = ''

		try:
			path_file = open('path.txt')
			path = path_file.readlines()[0]
		except:
			pass

		return path

	def cancel(self, event=None):
		self.root.destroy()

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

	return path

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

PathDialog(Tk())

path = get_path()
if '' == path:
	print 'Fatal: NO PATH'
	sys.exit(2)

print path
os.mkdir(get_build_id(path))

connect_path(drive_letter, path)

get_files(drive_letter, get_build_id(path), '*')

disconnect_path(drive_letter)

