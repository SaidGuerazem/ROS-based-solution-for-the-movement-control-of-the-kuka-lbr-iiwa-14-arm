#!/usr/bin/env python
import pandas as pd
import rosbag
import re
from math import floor    
from client_lib import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
   
# Making a connection object.
my_client = kuka_iiwa_ros_client()
    
# Wait until iiwa is connected zzz!
while (not my_client.isready): pass
print('Started!')




ag= rosbag.Bag('r.bag') # spécifier le nom du fichier .bag ici
genBag = bag.read_messages(topics="/ToolPosition") # spécifier le nom du topic ici
genBag_df = pd.DataFrame.from_dict(genBag)

# On definie une fonction qui permettera de visualiser les données de tool position sous forme de list exploitable

def std_msg_to_list(sentence):
    s = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(sentence))]
    del s[-1]
    return s
# Preparation des données
genBag_df.pop('topic')
genBag_df.pop('timestamp')

for i in range(0,genBag_df.shape[0]):
    genBag_df["message"][i]= std_msg_to_list(genBag_df["message"][i])
# Créer une copie df\_int qui servira comme base avec un type int
def flooring(list_1):
    for i in range(0,len(list_1)):
        list_1[i]=floor(list_1[i])
    return list_1

df_int=genBag_df.copy()
for i in range(0,genBag_df.shape[0]):
    df_int["message"][i]= flooring(df_int["message"][i])

df_int.to_csv('data_collection.csv') # récuperer les données dans un fichier .csv

df_new = pd.DataFrame(df_int['message'].tolist(), columns=['x', 'y', 'z', 'alpha', 'beta', 'gamma'])

# extract position and angle values for first row
pos = df_new.iloc[0,:3].values
ang = df_new.iloc[0,3:].values

# create 3D plot
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')

# plot starting point
ax.scatter(pos[0], pos[1], pos[2], c='r', marker='o')

# plot trajectory
for i in range(1, len(df_new)):
    pos = df_new.iloc[i,:3].values
    ax.plot([pos[0], df_new.iloc[i-1,0]], [pos[1], df_new.iloc[i-1,1]], [pos[2], df_new.iloc[i-1,2]], c='b')

# set plot parameters
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Trajectory of Robot Arm')
plt.show()

