from matplotlib import pyplot as plt
from skimage.feature import blob_doh, blob_dog, blob_log
from skimage import io
import matplotlib.cm as cm
import glob
import pandas as pd
from collections import defaultdict

def means(address):
	filelist = glob.glob(address + "/*.png")
	index = []	
	slices = defaultdict(list)
	for file in filelist:
		image = io.imread(file)[:,500:3300]
		index.append(file[len(address)+1:len(address)+6])
		slices[1].append(round(image[0:10].mean()))
		slices[2].append(image[1000:1010].mean())

	print slices
	return pd.DataFrame(slices, index = index)


def bubbles():
	# image = io.imread('bubble.png')
	# image = io.imread('images/15042_0c45140a-d88c-4b14-85b9-234e990721b1.png')
	# image = io.imread('images/15062_e268b731-1422-4269-b0c4-d2f1ab73d9fd.png')
	image = io.imread('images/15092_6242149e-5f21-4c55-b32a-c1f4e8263d72.png')
	# image = io.imread('test.png')
	image = image[1500:2800,400:3400]
	blobs = blob_doh(image, max_sigma=120, min_sigma=50, threshold=.005)
	# blobs = blob_dog(image, max_sigma=100, min_sigma=40, threshold=.08)
	# blobs = blob_log(image, max_sigma=100, min_sigma=50, threshold=.07)
	# title = ['blobs']
	print blobs
	blob_plot(image, blobs)

def blob_plot(image, blobs, title='blobs'):
	fig, ax = plt.subplots(1, 1)
	ax.set_title(title)
	ax.imshow(image,cmap = cm.Greys_r)
	for blob in blobs:

	    y, x, r = blob
	    c = plt.Circle((x, y), r, color='red', linewidth=2, fill=False)
	    ax.add_patch(c)

	plt.show()