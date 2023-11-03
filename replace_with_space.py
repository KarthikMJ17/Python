import re
import os
import tkinter as tk 
from tkinter import filedialog
import numpy as np
import sys
import os
#
root = tk.Tk()
root.withdraw()
#file name choosing dialog box
#filename = filedialog.askopenfilename(title="select a file",filetypes=(("dat files","*.dat"),("all files","*.*")))
if len(sys.argv)  > 1:
	folder=os.getcwd()
	file_name=sys.argv[1]
	filename = os.path.join(folder, file_name) 
else:
	filename = filedialog.askopenfilename(title="select a file",filetypes=(("dat files","*.dat"),("all files","*.*")))
#print(filename)
with open(filename,'r') as file:
	content = file.read()
content = re.sub(r' +', '\t', content)
content = re.sub(r'\t+', '\t', content)
content = re.sub(r'[ \t]+', ' ', content)
with open(filename,'w') as file:
	file.write(content)
print('Reduced white spaces with single space sucessfully!')
