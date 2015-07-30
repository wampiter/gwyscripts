import os

filebase = "LNO150727"
amp = "EFM Amplitude"
phase = "EFM Phase"
fst = " 1st"

for filename in reversed(os.listdir(".")):
    n = filename[-8:-5]
    if filename.startswith(filebase + amp + fst) or filename.startswith(filebase + phase + fst):
        #print filename[:-8] + "%03d"%(int(n) + 12) + ".tiff"
        #os.rename(filename, filename[:-8] + "%03d"%(int(n) + 12) + ".tiff")
        pass
    elif filename.startswith(filebase + amp) or filename.startswith(filebase + phase):
        #print filename[:-8] + "%03d"%(int(n) + 10) + ".tiff"
        #os.rename(filename, filename[:-8] + "%03d"%(int(n) + 10) + ".tiff")
        pass

for filename in os.listdir("."):
    if filename.startswith("LNO"):
        os.rename(filename, filename[3:])
    