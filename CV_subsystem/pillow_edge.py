
from PIL import Image, ImageSequence

from PIL import ImageFilter

import cv2

image = Image.open('trial_image.png')

index = 1

for frame in ImageSequence.Iterator(image):

	imageWithEdges = frame.filter(ImageFilter.FIND_EDGES)

	frame.show()

	imageWithEdges.show()

	frame.save("frame%d.png" % index)
	index = index + 1

