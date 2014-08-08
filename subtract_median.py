#Script to do basic batch leveling from within gwyconsole.

import gwyutils, os, time, re
			
cons = gwy.gwy_app_data_browser_get_containers()

for c in cons:
    filename = c.get_string_by_name("/filename")#get full filename
    filename = os.path.splitext(filename)[0]#Remove filename extension
    [path,name] = os.path.split(filename)#Splite filepath from filename
    if not os.path.exists('%s/proc' % path):
        os.makedirs('%s/proc' % path)
    print('processing %s' % name)
    #I like this palette:
    c.set_string_by_name("/0/base/palette", "Gwyddion.net")
    dfields = gwyutils.get_data_fields_dir(c)
    for key in dfields.keys():
        datafield = dfields[key]
        gwy_process_func_run("line_correct_median", c, gwy.RUN_IMMEDIATE)
    #Save .gwy and .png in proc folder.
    #gwy_file_save(c, '%s/proc/%s.gwy' % (path,name), gwy.RUN_NONINTERACTIVE)
    #gwy_file_save(c, '%s/proc/%s.png' % (path,name), gwy.RUN_NONINTERACTIVE)
	gwyutils.save_dfield_to_png(c, key, '%s/proc/%s.png' % (path,name), gwy.RUN_NONINTERACTIVE)
