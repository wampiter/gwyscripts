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
	images = numbers
	for channel in channels:
		for n, number in enumerate(numbers):
			images[n] = Image.open('scan'+ str(number) + "_" + str(channel) + '.png')
	
	#Merge images
	size = images[0].size
	if direction == 'h':
		outsize = (size[0]*len(images), size[1])
	elif direction == 'v':
		outsize = (size[0], size[1]*len(images))
	else:
		return ValueError
			
	result = Image.new('RGB', outsize)
	
	for n, image in enumerate(images):
		if direction == 'h':
			result.paste(image, (n*size[0], 0))
		if direction == 'v':
			result.paste(image, (0, n*size[1]))
	
	result.show()
	#Save files
#image_stitch(['Topography'], xrange(1,9,2), 'v')