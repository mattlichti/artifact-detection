# artifact-detection

The purpose of this project is to build a model for detecting imaging artifacts (rolling and bubbles) as well as determine if any process parameters are correlated with the artifacts. 

## Installation

This project uses anaconda python version 2.7 which can be downloaded [here](http://continuum.io/downloads).
I used the following python packages:
* numpy
* pandas
* json
* glob
* skimage
* scipy
* matplotlib

The code can be run from the command line with the following steps:

* git clone https://github.com/mattlichti/artifact-detection
* cd artifact_detection
* python run.py

run.py assumes the images to be examined are in the artifact-detection directory in a folder labeled 'images'


## Rolling Detection

Images with rolling have large dark splotches at the top. The simplest solution seemed to be to just compare the average pixel intensity of the tops of the images. I used the top 500 rows of pixels, but that was a pretty arbitrary choice. 

The average pixel intensity of the top 500 rows of the 53 images without rolling ranged from 125 to 203. An example of an image without rolling is pictured below.

![No Rolling](https://github.com/mattlichti/artifact-detection/blob/master/plots/no_rolling.png)

The average pixel intensity of the top 500 rows of the 3 images with with rolling ranged from 30 to 73. An example of an image with rolling is pictured below.

![Rolling](https://github.com/mattlichti/artifact-detection/blob/master/plots/rolling.png)

The clear separation in average intensity makes it easy to train a model to differentiate between images with and without rolling.

## Bubble detection

I still haven't gotten a bubble detection algorithm to work well. The best algorithm I've tried so far is blob detection using Determinant of Hessian (DoH). It still has lots of false positives. In addition, my laptop doesn't have enough memory to examine an entire image with the algorithms I've tried so I've only examined images in chunks. Ideally, I would run the algorithm on AWS but haven't tried that yet. The bubble detection can be run from the bubble_detection function in run.py. The output image below identifies the bubble but also has a false positive.

![Bubble detection](https://github.com/mattlichti/artifact-detection/blob/master/plots/bubble%20detection.png)


## Correlation between process parameters and artifacts

I used 11 machine properties whose values varied between the slices in my analysis. The rest of the properties were constant across the 56 slices so I can't find a correlation between those properties and the artifacts.

The highest correlation (-.36) and only statistically significant correlation was between the numbers of bubbles and the camera temperature. The p value of .006 is under than the conventional threshold for statistical significance of .05. However, since I was making 22 comparisons (2 artifacts * 11 machine parameters), there is a much higher chance of false positives. Using a bonferroni correction, the p value of .006 is no longer statistically significant because I would divide the threshold of .05 by 22 to get an adjusted threshold of .002. 

Even if the correlation is statistically significant, the correlation is likely caused by confounding variables. The first 22 samples had an average of .73 bubbles and were taken when the camera temp was 70.5 degrees. The next 34 had an average of .26 bubbles and were taken when the camera temp was 71 degrees. There are many possible reasons why there could more bubbles in the earlier samples than the later samples aside from the half degree change in temperature.

## Potential Next Steps

* Implement a much better bubble detection algorithm. I would need to read up more on edge detection and spend more time experimenting with scikit-image. 

* Try running on Spark and AWS.

* Use a much larger sample size when examining the correlation between the process parameters and the artifacts. This would greatly increase the chance of finding statistically significant correlations. It would also allow me to use multivariate regression or machine learning algorithms to better determine the relation between the parameters and the artifacts.