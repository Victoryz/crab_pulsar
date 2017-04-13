import corr,time,numpy,struct,sys,logging,pylab
from optparse import OptionParser
from numpy import int32,uint32,array,zeros,arange
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.gridspec import GridSpec

HOST = 'rpirachel'
adc_1a = 256*[0]
adc_1b = 256*[0]
adc_2a = 256*[0]
adc_2b = 256*[0]

def exit_fail():
	print 'FAILURE DETECTED. Log entries: \n', lh.printMessages()
	try:
		fpg.stop()
	except: pass
	raise
	exit()

def exit_clean():
	try:
		fpg.stop()
	except: pass
	exit()

def myplot():
	plt.clf()
	fpga.write_int('adc_scope1_snapshot_ctrl',0)
	chl_a=fpga.snapshot_get('adc_scope0_snapshot', man_trig=True, man_valid=True)
	fpga.write_int('adc_scope1_snapshot_ctrl',1)
	chl_b=fpga.snapshot_get('adc_scope1_snapshot', man_trig=True, man_valid=True)
	value_a=numpy.fromstring(chl_a['data'], dtype = numpy.int8)
	value_b=numpy.fromstring(chl_b['data'], dtype = numpy.int8)

	adc1 = value_a[0::2]
	adc2 = value_a[1::2]
	adc3 = value_b[0::2]
	adc4 = value_b[1::2]
	x1 = arange(0,255,2)
	x2 = arange(1,256,2)

	for i in range(len(adc1)):
		adc_1a[adc1[i]+128-1] += 1

	for i in range(len(adc2)):
		adc_1b[adc1[i]+128-1] += 1

	for i in range(len(adc3)):
		adc_2a[adc3[i]+128-1] += 1
	
	for i in range(len(adc4)):
		adc_2b[adc4[i]+128-1] += 1

	print(len(adc_1a))
	print(len(x1))
	ax1 = plt.subplot(gs1[0])
	plt.title('ADC0')
	plt.ylabel('Level')
	plt.xlabel('ADC0 Zoom in 8x')
	plt.hist(adc4,256)
	plt.hist(adc3,256)

	fig.canvas.draw()
	fig.canvas.manager.window.after(200, myplot)

if __name__ == '__main__':
	print 'Connecting to board:', HOST
	fpga = corr.katcp_wrapper.FpgaClient(HOST)
	time.sleep(0.1)

	if fpga.is_connected():
		print 'DONE'
	else:
		print 'ERROR: Failed to connect to server %s!' %(HOST)
		sys.exit(0);
	fig = plt.figure(figsize=(12,6))

	gs1 = GridSpec(3,2)
	gs1.update(hspace=0.25)

	fig.canvas.manager.window.after(200,myplot)
	plt.show()
