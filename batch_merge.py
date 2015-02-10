from glob import glob

filebase = "/Users/jot/Desktop/test"
channels = ['Topo', 'AUX1', 'AUX2', 'Amplitude0', 'Phase0', 'Amplitude 1st', 'Phase 1st']

containers = {}
for channel in channels:
	paths = glob(filebase + "/*" + channel + "*.tiff")
	for path in paths:
		number = path[-8:-5]
		c = gwy_file_load(path, gwy.RUN_NONINTERACTIVE)
		containers[channel, number] = c

scannumbers = [path[-8:-5] for path in topopaths]


for path in aux1paths:
	c = gwy_file_load(path, gwy.RUN_NONINTERACTIVE)
	aux1cons[path[-8:-5]] = c

c1 = gwy_file_load("%s/test.tiff" % filebase, gwy.RUN_NONINTERACTIVE)
c2 = gwy_file_load("%s/test2.tiff" % filebase, gwy.RUN_NONINTERACTIVE)

gwy.gwy_app_data_browser_add(c1)
gwy_app_data_browser_select_data_field(c1, 0)
gwy_app_data_browser_merge(c2)

gwy_file_save(c1, "testy.gwy", gwy.RUN_NONINTERACTIVE)