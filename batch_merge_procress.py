from glob import glob
import gwyutils
import os
from collections import OrderedDict

filebase = "/Users/jot/Desktop/6-19_JP"
for directory in [filebase+'/proc',filebase + '/pproc',filebase + '/pproc/png']:
	if not os.path.exists(directory):
		os.makedirs(directory)
channels = ['Topography', 'AUX1', 'AUX2', 'Amplitude0', 'Phase0', 'Amplitude 1st', 'Phase 1st']
names = ['Topography', 'MIM-Im', 'MIM-Re', 'MIM-Im Lifted', 'MIM-Re Lifted', 'MIM-Im First Pass', 'MIM-Re First Pass']
liftchannels = ['MIM-Im Lifted', 'MIM-Re Lifted', 'MIM-Im First Pass', 'MIM-Re First Pass']
proc = OrderedDict([('scars_remove', [0]),('level',[0,3,4]), ('line_correct_median',[0]), ('threshold', [0,3,4]), ('fix_zero',[0])])
invert_channels = [1]

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
for scan_number, topo_container in enumerate(topo_containers):
	if topo_container != None:
		mim_id = ['Null']*4
		for chan_number in xrange(len(channels)):		
			name = gwy_app_get_data_field_title(topo_container, chan_number)[:-2]
			for liftchan_number, setname in enumerate(liftchannels):
				if name == setname:
					mim_id[liftchan_number] = chan_number
		if mim_id[0] != 'Null':
			mim_data_arrays = ['Null']*4
			mim_data_fields = ['Null']*4
			for n, idn in enumerate(mim_id):
				gwy_app_data_browser_select_data_field(topo_container, idn)
				datafield = gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
				mim_data_fields[n] = datafield
				data_array = gwyutils.data_field_data_as_array(datafield)
				mim_data_arrays[n] = data_array
			for j in [0,1]: #for im and re: relies on order of lift list
				mim_data_arrays[j][...] = mim_data_arrays[j+2] - mim_data_arrays[j]
				if j in invert_channels:
					mim_data_arrays[j] *= -1
				mim_data_fields[j].data_changed()
			
		else:
			print "no lifted channel for scan" + str(scan_number)
		gwy_file_save(topo_container, filebase + "/proc/scan" + str(scan_number) + ".gwy", gwy.RUN_NONINTERACTIVE)

#modify process (module) settings
settings = gwy_app_settings_get()
settings.set_int32_by_name('/module/threshold/mode', 2)
settings.set_double_by_name('/module/threshold/sigma', 4.0)

#process by channel:
for number, topo_container in enumerate(topo_containers):
	if topo_container != None:
		for key in proc:
			for n in xrange(len(names)):
				if gwy_app_get_data_field_title(topo_container, n)[:-2] in names:
					if names.index(gwy_app_get_data_field_title(topo_container, n)[:-2]) in proc[key]:
						if names.index(gwy_app_get_data_field_title(topo_container, n)[:-2]) == 4:
							settings.set_double_by_name('/module/threshold/sigma', 2.0)
						else:
							settings.set_double_by_name('/module/threshold/sigma', 4.0)
						gwy_app_data_browser_select_data_field(topo_container, n)
						gwy_process_func_run(key, topo_container, gwy.RUN_IMMEDIATE)
						gwyutils.save_dfield_to_png(topo_container, '/%s/data' % n, '%s/pproc/png/scan%s_%s.png' % (filebase,number,gwy_app_get_data_field_title(topo_container, n)[:-2]), gwy.RUN_NONINTERACTIVE)
		gwy_file_save(topo_container, filebase + "/pproc/scan" + str(number) + ".gwy", gwy.RUN_NONINTERACTIVE)
			
print 'done'