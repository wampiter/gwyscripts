from PIL import Image
import os, sys, glob

def image_stitch(channels, numbers, direction = 'v'):
	'''Stitch together row/column images
	
	channels: channel names (after scan number)
	numbers: ordered list of scan numbers
	direction: v or h
	'''
	ddict = {'v':1, 'h':0}
	dnum = ddict[direction]
	
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