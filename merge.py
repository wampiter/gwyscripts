filebase = "/Users/jot/Desktop/test"

c1 = gwy_file_load("%s/test.tiff" % filebase, gwy.RUN_NONINTERACTIVE)
c2 = gwy_file_load("%s/test2.tiff" % filebase, gwy.RUN_NONINTERACTIVE)

gwy.gwy_app_data_browser_add(c1)
gwy_app_data_browser_select_data_field(c1, 0)
gwy_app_data_browser_merge(c2)

gwy_file_save(c1, "testy.gwy", gwy.RUN_NONINTERACTIVE)