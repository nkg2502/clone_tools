import string
import os
import glob
import zlib
from time import strftime, localtime
from Tkinter import *
from datetime import datetime

# GUI interface 
class PathDialog:

	def __init__(self, root):

		root.geometry('550x60')
		root.resizable(0, 0)

		# key bind
		root.bind('<Return>', self.write_path_file)
		root.bind('<Escape>', self.exit)
		root.protocol('WM_DELETE_WINDOW', self.exit)

		frame = Frame(root)
		frame.pack(fill=BOTH, expand=1)

		path_entry = Entry(frame, font='Consolas 14')

		path_entry.insert(0, self.read_path_file())
		path_entry.focus_set()
		path_entry.select_range(0, END)

		path_entry.pack(side=TOP, fill=X)

		Button(frame, text='Cancel', font='Consolas 14', command=self.exit).pack(side=RIGHT)
		Button(frame, text='  OK  ', font='Consolas 14', command=self.write_path_file).pack(side=RIGHT)

		self.root = root
		self.path_entry = path_entry

		root.mainloop()
	
	def write_path_file(self, event=None):
		path_file = open('path.txt', 'w')
		path_file.write(self.path_entry.get().rstrip())

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

	def exit(self, event=None):
		sys.exit(0)

def get_path():

	path = ''
	try:
		path = open('path.txt').readline()
	except:
		pass

	return path

def get_build_id(path):
	for raw_build_id in path.split('\\')[::-1]:
		build_id = raw_build_id.rstrip()
		
		if build_id:
			return build_id
	
	raise ValueError

# use robocopy
def get_files(src, dst, files = '*', depth = 0, log_file_name = 'download.log'):
	cmd = 'robocopy {} {} {} {} /e /w:5 /v /fp /eta /tee /log+:{}'.format(src, dst, files, '/lev:' + str(depth) if 0 < depth else '', log_file_name)
	# /njh /njs
	os.system(cmd)

# calculate CRC32
def crc(file_name):
	prev = 0
	for line in open(file_name,"rb"):
		prev = zlib.crc32(line, prev)
	return "%X" % (prev & 0xFFFFFFFF)

# MAIN

PathDialog(Tk())

path = get_path()
if '' == path:
	print 'Fatal: NO PATH'
	sys.exit(2)

print path
try:
	os.mkdir(get_build_id(path))
except OSError:
	pass

log_file_name = strftime("%Y.%m.%d[%H.%M.%S].log", localtime())
get_files(path, get_build_id(path), '*', 0, log_file_name)

# CRC32 checksum
print 'Calculating checksum...'
start_time = datetime.now()
checksum_file = open(log_file_name + '.checksum.txt', 'w')

for root_path, subdirs, files in os.walk('.'):

	for candidate in subdirs:
		if '.git' in candidate:
			subdirs.remove(candidate)

	for file_name in files:
		checksum_file.writelines([os.path.join(root_path, file_name), '\t', crc(os.path.join(root_path, file_name)), '\n'])

print 'Finished: {}'.format(datetime.now() - start_time)
os.system('pause')

