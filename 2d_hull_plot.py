import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 2D cross product
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

file_name = 'vdwOpt2_Energy.log'
comps_file = 'compositions.dat'

#df = pd.read_csv(comps_file, delim_whitespace=True, header=None, names=["Compound", "Nb", "C"])
df = pd.read_csv(comps_file, delim_whitespace=True, header=None, names=["Compound", "Nb", "C"])
df["x_C"] = df["C"] / (df["Nb"] + df["C"])
df= df[["Compound", "x_C"]]
df["Energy"] = np.nan

# Filtering out formation energy 
lines=[]
with open(file_name, "r") as f:
    for line in f:
        line=line.lstrip()
        if line.startswith("Formation energy of") and not "diamond" in line:
                line=line.strip()
                line=line.rstrip()
                lines.append(line.strip())

# Adding the energy data to data frame 
for i in lines:
    i=i.split()
    indx=df.index[df["Compound"] == i[3]]
    df.loc[indx, "Energy"] = float(i[5])


df_with_energy = df[df["Energy"].notna()]

elements = pd.DataFrame({
    "Compound": ["Nb", "C"],
    "x_C": [0, 1],
    "Energy": [0,0]
})


df_with_energy = pd.concat([df_with_energy, pd.DataFrame(elements)], ignore_index=True)
pts = np.column_stack((df_with_energy['x_C'].values, df_with_energy['Energy'].values))
order = np.lexsort((pts[:,1], pts[:,0]))
pts_sorted = pts[order]
cmpnd_sorted = df_with_energy['Compound'].values[order]



lower = []
lower_idx = []
for i, p in enumerate(pts_sorted):
    while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
        lower.pop()
        lower_idx.pop()
    lower.append(p)
    lower_idx.append(i)
lower = np.array(lower)
lower_idx = np.array(lower_idx, dtype=int)


hull_points = pts_sorted[lower_idx]
hull_formulas = cmpnd_sorted[lower_idx]


stable_mask = np.zeros(len(pts_sorted), dtype=bool)
stable_mask[lower_idx] = True
stable_mask


tol = 1e-8
for i in range(len(lower)-1):
    a = lower[i]; b = lower[i+1]
    vec = b - a
    den = vec.dot(vec)
    for j, p in enumerate(pts_sorted):
        t = vec.dot(p - a) / den if den != 0 else 0.0
        if -tol <= t <= 1+tol and abs(cross(a, b, p)) <= 1e-6:
            stable_mask[j] = True

fig, ax = plt.subplots(figsize=(10,7))
ax.plot(pts_sorted[:,0], pts_sorted[:,1], 'o', label="All compounds")

# Convex hull line
ax.plot(hull_points[:,0], hull_points[:,1], '-o', label="Convex hull")

# Annotate and mark stable compounds
for i, (x, y) in enumerate(pts_sorted):
    label = cmpnd_sorted[i]
    if stable_mask[i]:
        ax.plot(x, y, marker='*', markersize=10)
        ax.text(x, y, f" {label}", va='top', fontsize=18)
    else:
        ax.text(x, y, f" {label}", va='bottom', fontsize=10, color='gray')

ax.set_xlabel("Mole fraction of C", fontsize=18)
ax.set_ylabel("Formation energy, eV/atom", fontsize=18)
ax.set_title("vdw-DF3", fontsize=18)
ax.grid(True)
#ax.legend()
plt.tight_layout()
#plt.show()

# ============================
# SAVE PLOT
# ============================
fig.savefig("vdw.png", dpi=500)
#print("Plot saved as 'binary_convex_hull.png'")

