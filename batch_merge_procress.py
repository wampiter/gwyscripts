from glob import glob
import gwyutils
import os

filebase = "/Users/jot/Desktop/test"
for directory in [filebase+'/proc',filebase + '/pproc']:
	if not os.path.exists(directory):
		os.makedirs(directory)
channels = ['Topography', 'AUX1', 'AUX2', 'Amplitude0', 'Phase0', 'Amplitude 1st', 'Phase 1st']
names = ['Topography', 'MIM-Im', 'MIM-Re', 'MIM-Im Lifted', 'MIM-Re Lifted', 'MIM-Im First Pass', 'MIM-Re First Pass']
liftchannels = ['MIM-Im Lifted', 'MIM-Re Lifted', 'MIM-Im First Pass', 'MIM-Re First Pass']
proc = {'level':[0], 'line_correct_median':[0]}

#Load all from channels by channel and scan number:
containers = []
for chan_index, channel in enumerate(channels):
	paths = glob(filebase + "/*" + channel + "*.tiff")
	for path in paths:
		number = path[-8:-5]
		while len(containers) <= int(number):
			containers.append([None]*len(channels))
		c = gwy_file_load(path, gwy.RUN_NONINTERACTIVE)
		containers[int(number)][chan_index] = c

#Merge other channels into topography container, save:
topo_containers = zip(*containers)[0]
for number, topo_container in enumerate(topo_containers):
	if topo_container != None:
		gwy_app_data_browser_add(topo_container)
		gwy_app_data_browser_select_data_field(topo_container, 0)
		gwy_app_set_data_field_title(topo_container, 0, names[0])
		for index, other_container in enumerate(containers[number][1:]):
			if other_container != None:
				gwy_app_set_data_field_title(other_container, 0, names[index+1])
				gwy_app_data_browser_merge(other_container)
		gwy_file_save(topo_container, filebase + "/proc/scan" + str(number) + ".gwy", gwy.RUN_NONINTERACTIVE)

#do subtraction for lifted channels
for number, topo_container in enumterate(topo_containers):
	mim_id = [Null]*4
	for n in xrange(len(channels)):		
		name = gwy_app_get_data_field_title(topo_container, n)[:-2]
		for m, setname in liftchannels:
			if name == setname:
				mim_id[m] = n
		if mim_id[0] != Null:
			mim_data_arrays = [Null]*4
			for n, idn in enumerate(mim_id):
				gwy_app_data_browser_select_data_field(topo_container, idn)
				datafield = gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
				data_array = gwyutils.data_field_data_as_array(datafield)
				mim_data_arrays[n] = data_array
			
			#mim_im_abs = field(mim_id[2]) - field(mim_id[0])
			
			
			

#process by channel:
for number, topo_container in enumerate(topo_containers):
	if topo_container != None:
		for key in proc:
			for n in xrange(len(channels)):
				if gwy_app_get_data_field_title(topo_container, n)[:-2] in channels:
					if channels.index(gwy_app_get_data_field_title(topo_container, n)[:-2]) in proc[key]:
						gwy_app_data_browser_select_data_field(topo_container, n)
						gwy_process_func_run(key, topo_container, gwy.RUN_IMMEDIATE)
		gwy_file_save(topo_container, filebase + "/pproc/scan" + str(number) + ".gwy", gwy.RUN_NONINTERACTIVE)
			
print 'done'