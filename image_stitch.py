from PIL import Image
import os, sys, glob

def stitch_scans(channels = ['Topography', 'MIM-Re Lifted', 'MIM-Im Lifted'], numbers, direction = 'v'):
	'''Stitch together row/column images of same channel for output pngs of batch_merge_proc
	
	channels: channel names (list)
	numbers: ordered list of scan numbers (eg. range(1,7,2))
	direction: v or h
	'''
	
	#Load Input Files
	images = {}
	for channel in channels:
		images[channel] = []
		for number in numbers:
			images[channel].append(Image.open('scan'+ str(number) + "_" + str(channel) + '.png'))
	
	#Merge images
	size = images[channels[0]][0].size
	if direction == 'h':
		outsize = (size[0]*len(images[channels[0]]), size[1])
	elif direction == 'v':
		outsize = (size[0], size[1]*len(images[channels[0]]))
	else:
		return ValueError
			
	results = [Image.new('RGB', outsize)]*len(channels)
	
	for m, channel in enumerate(channels):
		for n, image in enumerate(images[channel]):
			if direction == 'h':
				results[m].paste(image, (n*size[0], 0))
			if direction == 'v':
				results[m].paste(image, (0, n*size[1]))
		#results[m].show
		results[m].save('stitch_' + str(min(numbers)) + '-' + str(max(numbers)) + '_' + channel + '.png')
		
def stitch_channels(channels, direction = 'h'):
	'''Stitch together row/column images of same scan(s), different channels
	
	channels: channel names (ordered list)
	direction: v or h
	'''
	
	#Load input files:
	images = []
	for channel in channels:
		scans = []
		filenames = []
		for filename in glob.glob("*" + channel + ".png"):
			scans.append(Image.open(filename))
			filenames.append(filename[:-(4 + len(channel))])
		images.append([filenames, scans])
	
	#organize groups to be merged
	organized_images = []
	for topo_scan in images[0]:
		filenames = topo_scan[0]
		scans = topo_scan[1]
		for n, filename in enumerate(filenames):
			organized_images.append(topo_scan[n]) #add filename and scan
			for channel_images in images[1:]:
				c_filenames = channel_images[0]
				c_scans = channel_images[1]
				for m, c_filename in enumerate(c_filenames):
					if filename == c_filename:
						organized_images[n].append(c_scans[m])
						
	#Stitch images
	for group in organized_images:
		size = group[1].size
		if direction == 'h':
			outsize = (size[0]*len(images[channels[0]]), size[1])
		elif direction == 'v':
			outsize = (size[0], size[1]*len(images[channels[0]]))
		else:
			return ValueError
		result = Image.new('RGB', outsize)