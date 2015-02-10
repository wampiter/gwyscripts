from glob import glob

filebase = "/Users/jot/Desktop/test"
channels = ['Topography', 'AUX1', 'AUX2', 'Amplitude0', 'Phase0', 'Amplitude 1st', 'Phase 1st']
names = ['Topography', 'MIM-Im', 'MIM-Re', 'MIM-Im Lifted', 'MIM-Re Lifted', 'MIM-Im First Pass', 'MIM-Im First Pass']

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
for number, topo_container in enumerate([scan[0] for scan in containers]):
	if topo_container != None:
		gwy_app_data_browser_add(topo_container)
		gwy_app_data_browser_select_data_field(topo_container, 0)
		for index, other_container in enumerate(containers[number][1:]):
			if other_container != None:
				gwy_app_set_data_field_title(other_container, 0, names[index+1])
				gwy_app_data_browser_merge(other_container)
		gwy_file_save(topo_container, filebase + "/proc/scan" + str(number) + ".gwy", gwy.RUN_NONINTERACTIVE)
  
