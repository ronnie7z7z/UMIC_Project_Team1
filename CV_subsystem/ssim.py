from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt 
import numpy as np 
import cv2
import os

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
	# show the images
	#plt.show()

	return s

# load the images -- the original, the original + contrast,
# and the original + photoshop
frame1 = cv2.imread("saved_images/1.png")
cv2.imshow("img", frame1)
frame2 = cv2.imread("saved_images/3.png")
frame3 = cv2.imread("saved_images/7.png")

#resize the images
frame1 = cv2.resize(frame1, (480,480))
frame2 = cv2.resize(frame2, (480,480))
frame3 = cv2.resize(frame3, (480,480))

# convert the images to grayscale
frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

# initialize the figure
fig = plt.figure("Images")
images = ("1", frame1), ("9", frame2), ("3", frame3)
# loop over the images
for (i, (name, image)) in enumerate(images):
	# show the image
	ax = fig.add_subplot(1, 3, i + 1)
	ax.set_title(name)
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")
# show the figure
#plt.show()
# compare the images
'''compare_images(frame1, frame2, "1 vs 2")
compare_images(frame1, frame3, "1 vs 3")
compare_images(frame2, frame3, "2 vs 3")'''

img1 = cv2.imread("saved_images/0.png") 
img1 = cv2.resize(img1, (480,480))
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

for i in range(1,10):
 	img2 = cv2.imread("saved_images/{}.png".format(i))
 	img2 = cv2.resize(img2, (480,480))
 	img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

 	s = compare_images(img1, img2, "1 vs all")
 	print("{} = {}".format(i, s))
 	if s>0.8:
 		os.remove("saved_images/{}.png".format(i))