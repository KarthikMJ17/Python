import numpy as np
from tkinter import filedialog
import tkinter as tk
import matplotlib.pyplot as plt
import sys
import os
#using tkinter file file opening and closing without any disturbances
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
#colors = ['r','b','g','y','c','m','k','lime','magneta','tab:olive','tab:purple','bisque','darkgrey','ornagered']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#17becf', '#bcbd22', '#98df8a', '#aec7e8', '#ffbb78', '#c5b0d5', '#c49c94', '#f7b6d2', '#dbdb8d', '#9edae5', '#17becf', '#a7ff83']
marker_list=['rx','bo','gs','cH','g^','y+','m*','cD','r^','yH','ko','k<','m*','k0']
##
lines=[]
with open(filename, "r") as f:
    for file in f:
        if not file.startswith("##"):
            file=file.strip()
            file=file.lstrip()
            file=file.rstrip()
            lines.append(file.strip())
authors = []
for i, line in enumerate(lines):
    if line.startswith("#$"):
        # Extract the author's name from the header
        #print(i)
        author = line[2:]
        authors.append(author)
        locals()[authors[-1]+'_data'] = np.empty((0, 2))
    else:
        if '\t' in line:
             temp_line=line.split('\t')
             temp_line=np.array([temp_line[:2]])
             locals()[authors[-1]+'_data'] = np.append(locals()[authors[-1]+'_data'], temp_line, axis=0)
        else:
             temp_line=line.split()
             temp_line=np.array([temp_line[:2]])
             locals()[authors[-1]+'_data'] = np.append(locals()[authors[-1]+'_data'], temp_line, axis=0)
#fig, ax = plt.subplots()
for i in range(0,len(authors)):
    locals()[authors[i]+'_data']=(locals()[authors[i]+'_data']).astype(float)
    plt.plot((locals()[authors[i]+'_data'])[:,0],(locals()[authors[i]+'_data'])[:,1],color=colors[i],label=authors[i])

# Increasing the font size of the x and y scales
plt.xlabel('X', fontsize=18)
plt.ylabel('Y', fontsize=18)
#plt.xlabel(fontweight="bold")
#plt.ylabel(fontweight="bold")
# Boldify x and y labels
#plt.xlabel(fontweight='bold')
#plt.ylabel(fontweight='bold')

# Bolidify the x and y scales
#plt.rcParams['xtick.labelsize'] = 'bold'
#plt.rcParams['ytick.labelsize'] = 'bold'
#plt.xticks(fontweight='bold')
#plt.yticks(fontweight='bold')
# font size of x y scales
plt.tick_params(axis='both', which='major', labelsize=12)
plt.legend()
plt.grid(True)

#aspect ratio
#ax.set_aspect(1/60)
plt.show()
