import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os
import sys
#using tkinter file file opening and closing without any disturbances
root = tk.Tk()
root.withdraw()
#file name choosing dialog box
#print(len(sys.argv))
if len(sys.argv)  > 1:
	folder=os.getcwd()
	file_name=sys.argv[1]
	filename = os.path.join(folder, file_name) 
else:
	filename = filedialog.askopenfilename(title="select a file",filetypes=(("dat files","*.dat"),("all files","*.*")))
data=np.genfromtxt(filename)
x = data[:,0]
y = data[:,1]
#sorting in order to make splines connected to next consecutive x for better look of plot(oterwise it will be connected randomly)
sort=np.argsort(x)
x=x[sort]
y=y[sort]
plt.plot(x,y)
plt.show()
