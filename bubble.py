from matplotlib import pyplot as plt
from skimage.feature import blob_doh
from skimage import io
import matplotlib.cm as cm


def bubbles(filename):
	image = io.imread(filename)[:2000,500:1700]
	bubble_locs = blob_doh(image, max_sigma=100, min_sigma=50, threshold=.008)
	title = 'bubbles'
	plot(image, title, circles=bubble_locs)

def plot(image, title, circles=[]):
	'''
	parameters:
	image: ndarray of pixel intensities
	title: title to display on plot
	circles: list of positions to circle in image in (y, x, radius) format
	'''
	fig, ax = plt.subplots()
	ax.set_title(title)
	ax.imshow(image,cmap = cm.Greys_r)
	for circle in circles:
	    y, x, r = circle
	    c = plt.Circle((x, y), r, color='red', linewidth=5, fill=False)
	    ax.add_patch(c)
	plt.show()

def run():
	filename = 'images/15102_4eef5851-08cf-4836-9027-66945996b224.png'
	bubbles(filename)