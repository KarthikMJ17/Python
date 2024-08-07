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
#
#This code is directly copied from our old xyplot code  
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
#
#For saving foler name in the same folder 
base_folder=filename
#base_folder=base_folder[:base_folder.rfind('/')+1].replace('\\', '/')
base_folder=base_folder[:base_folder.rfind('/')+1]
# rfind finds the last occurane of the string --> resturn the id of last ocurane --> the we can chop the fileneme
# ---file name to get the base folder name , here we used '+1' to also include last '/' in the string
#same logic can be used for getting what is the file name
only_file_name=filename[filename.rfind('/')+1:]
#
xlength=11.5000
ylength=11.5000
x_label_anchor=0.85
y_label_anchor=0.05
anchor_step=0.03
symbol_size=0.20
char_size=0.25
#
data=np.genfromtxt(filename)
#
with open(base_folder+only_file_name.replace('.dat','')+'_EXP'+'.exp', 'w') as f:
    f.write('PROLOG 1\n')
    min_x=min(data[:,0])
    max_x=max(data[:,0])+0.05*max(data[:,0])
    #max_x=max(data[:,0])
    min_y=min(data[:,1])
    max_y=max(data[:,1])+0.05*max(data[:,1])
    #max_y=max(data[:,1])
    f.write('XSCALE'+'   '+str(min_x)+'  '+str(max_x)+'\n')
    f.write('YSCALE'+'   '+str(min_y)+'  '+str(max_y)+'\n')
    f.write('XTYPE LINEAR'+'\n'+'YTYPE LINEAR'+'\n'+'XLENGTH'+'  '+str(xlength)+'\n'+'YLENGTH'+'  '+str(ylength)+'\n')
    f.write('DATASET 1'+'\n'+'CHAR '+str(char_size)+'\n'+'COLOR 1'+'\n'+'SYMBOLSIZE '+str(symbol_size)+'\n')
    f.write('BLOCK X=C1; Y=C2;  GOC=C3,MAWS1;\n')
    for i,a in enumerate(authors):
        f.write('CLIP ON\n')
        for j in range(0,len(locals()[a+'_data'])):
            xd=(locals()[a+'_data'])[j,0]
            yd=(locals()[a+'_data'])[j,1]
            sym='S'+str(i+2)
            f.write(str(xd)+' '+str(yd)+' '+sym+'\n')
        f.write('CLIP OFF\n')
        f.write(str(x_label_anchor)+' '+str(y_label_anchor)+' '+'N'+sym+"'"+a+'\n')
        y_label_anchor+=anchor_step
        f.write('COLOR '+str(i+2)+'\n')
    f.write('BLOCKEND')
    #for i in authors:
f.close()
print("Done sucessfuly")