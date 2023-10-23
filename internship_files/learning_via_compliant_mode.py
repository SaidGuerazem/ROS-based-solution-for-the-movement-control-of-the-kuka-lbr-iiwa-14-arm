import pandas as pd
import rosbag
import re
from math import floor
import scipy.spatial.distance as Dist
from client_lib import *

if __name__ == '__main__':
    my_client = kuka_iiwa_ros_client()  # Making a connection object.
    while (not my_client.isready):
        pass  # Wait until iiwa is connected zzz!
    print('Started')

    # Initializing Tool 1
    my_client.send_command('setTool tool2')

    # Initializing
    my_client.send_command('setJointAcceleration 0.2')
    my_client.send_command('setJointVelocity 0.2')
    my_client.send_command('setJointJerk 0.2')
    my_client.send_command('setCartVelocity 100')


    bag= rosbag.Bag('r.bag')
    genBag = bag.read_messages(topics="/ToolPosition")
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
    # Elaborer les valeurs afin de pouvoir les envoyer directement comme une commande
    def elaborate_values(list1):
        s=str( )
        for i in range(0,len(list1)):
            s = s + str(floor(list1[i])) + ' '
        return s
        
    for i in range(0,genBag_df.shape[0]):
        genBag_df["message"][i]= elaborate_values(genBag_df["message"][i])

    # Envoie des commandes vers le client kuka
    for i in range(0, genBag_df.shape[0]//10):
        my_client.send_command('setPositionXYZABC '+ genBag_df['message'][i*10] +'ptp')
        start_time=time.time()
        while Dist.euclidean(my_client.ToolPosition[0], df_int['message'][i]) > 5: 
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:
                break
            pass

    my_client.send_command('setPosition XYZABC '+ genBag_df['message'][genBag_df.shape[0]-1] +'ptp')