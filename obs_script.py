# Observing script to be run on the SNAP board after calibrating the
# ADCs with voltread_

import numpy as np
import corr.katcp_wrapper as k
import matplotlib.pyplot as plt
import struct
import math
import time

mac_comp = 0x90e2bac37cf4
mac_snap = 0xb827eba34523+12 
ip_snap = ((10<<24)+(0)+(10<<8)+(199))
mask = ((255<<24)+(255<<16)+(255<<8)+0)

snap = k.FpgaClient('gbt-pi')
time.sleep(0.1)

#snap.write_int('sync',math.factorial(9)*2**6)
snap.write_int('acc_len',512*1024)

snap.write_int('test',0)

snap.write_int('dest_ip',((10<<24)+(0)+(10<<8)+(10)))
snap.write_int('dest_port',10000)
snap.config_10gbe_core('xmit_gbe0', mac_snap, ip_snap, 10001, [mac_comp for i in range(256)], gateway=0, subnet_mask=mask)

snap.write_int('shift',2047)

snap.write_int('rst_of',1)
time.sleep(0.01)
snap.write_int('rst_of',0)

snap.write_int('valid_en',0)
snap.write_int('chan1',150)
snap.write_int('chan2',160)
snap.write_int('chan3',170)

snap.write_int('rst',1)
time.sleep(0.01)
snap.write_int('rst',0)

snap.write_int('valid_en',3)

freq = np.arange(256)*(250./512.)

for i in range(12):
    snap.write_int('antenna',i);
    time.sleep(2)
    arr = struct.unpack('>256Q',snap.read('spectrum',8*256))
    plt.plot(arr)

plt.show()
