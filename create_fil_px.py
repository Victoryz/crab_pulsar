import struct
import pylab
import time
import numpy as np
import os
from pprint import pprint
import matplotlib.pyplot as plt
#import pylab as plt
from astropy.coordinates import Angle
from astropy.time import Time
from filterbank_utils import *
import sys
from random import randint

def get_data(filename):
    """ Read data in Deepthi's file format 
    
    This uses np.fromfile and numpy arrays instead of struct,
    which should make it faster than the original version
    """
    n_data = 2097152   # Number of data points per buffer
    n_flag = 1024      # Number of flags per buffer
    
    with open(filename, 'r') as fp:
        file_size = os.stat(filename).st_size
        no_cpy_buf = int(file_size/4195328)
        #noise = np.random.normal(0,1,100)
        #print no_cpy_buf
        
        raw_data = np.zeros((no_cpy_buf, n_data), dtype='<H')
        for ii in range(no_cpy_buf):    
            #copy = struct.unpack(struct_fmt, fp.read(struct_len))
            data = np.fromfile(fp, dtype='<H', count=n_data)
            flag = np.fromfile(fp, dtype='<B', count=n_flag)
            zeros = np.zeros(2048, dtype='<H')
            for y in range(len(flag)):
                if flag[y] == 255:
                    data[2048*y:2048*(y+1)] = zeros
            raw_data[ii] = data
		#noise = data
        total_data = raw_data.flatten()
	xx      = total_data[0::4]
        yy      = total_data[1::4]
        xy_img  = total_data[2::4].view('int16')
        xy_real = total_data[3::4].view('int16')
	#pylab.subplot(311)
	for kk in range(0,50):
		
		pylab.plot(xx[kk*4096:(kk+1)*4096-1]+kk*10000, 'b')

	pylab.xlabel('Freq Channels')
	pylab.ylabel('Amp')
	plt.show()
	return power

if __name__ == '__main__':
    header_filename = 'HEADER.txt'
    filename = raw_input("Please enter filename to read:\n")
    #data_old = get_data_old(filename)
    data = get_data(filename)
    #pprint(data)
    # Check the two functions do the same thing
    #print data_old.shape
    #print data.shape
    #assert np.allclose(data)#, data_old)

    # Read header
    raw_header = dict(np.genfromtxt(header_filename, dtype='str'))
    
    # Generate a filterbank header
    fil_header = {}
    fil_header['nbits'] = 8
    fil_header['tsamp'] = .00099865*2**2
    fil_header['nchans'] = 4096    
    fil_header['nifs'] = 1
    fil_header['data_type'] = 1
    #fil_header['fch1'] = 1049.87
    fil_header['fch1'] = 2099.87
    fil_header['foff'] = -.256
    fil_header['tstart'] = 55500
    fil_header['telescope_id']  = 1      # This is pretty much just made up
    """fil_header['data_type']     = 1       # Filterbank data
    fil_header['barycentric']   = 0
    fil_header['nbits']         = 16
    fil_header['rawdatafile']   = filename
    fil_header['source_name']   = 'Crab' 
    fil_header['tstart']        = 55500 
    fil_header['tsamp']         = 1.0
    fil_header['fch1']          = 1.0
    fil_header['foff']          = 1.0
    fil_header['nchans']        = 4096      
    fil_header['nifs']          = 1
    fil_header['src_raj']       = Angle('05:34:31.94', unit='hour')
    fil_header['src_dej']       = Angle('22:00:52.2', unit='hour')
    #fil_header['az_start']      = 0
    #fil_header['za_start']      = 0     
    #fil_header['nsamples']      
    #fil_header['ibeam']        
    #fil_header['refdm']        
    #fil_header['period']       
    #fil_header['machine_id']   
    #fil_header['pulsarcentric'] = 0
    """
    pprint(raw_header)
    pprint(fil_header)
   
    # Now, serialize the header into sigproc format
    fil_header_str = generate_sigproc_header(fil_header)
    
    # Save to disk
    filename_out = raw_input('Please enter file name for output (ex: filterbank_test.fil): ')
    print("creating %s" % filename_out)
    with open(filename_out, 'w') as fbfile:
        fbfile.write(fil_header_str)
        data.tofile(fbfile)

    
