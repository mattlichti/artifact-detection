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
* sklearn
* scipy
* matplotlib

The code can be run from the command line with the following steps:

* git clone https://github.com/mattlichti/artifact-detection
* cd artifact_detection
* python run.py

run.py assumes the images to be examined are in the artifact-detection directory in a folder labeled 'images'


## Rolling Detection

Images with rolling have large dark splotches at the top. The simplist solution seemed to be to just compare the average pixel intensity of the tops of the images. I used the top 500 rows of pixels, but that was a pretty arbitrary choice. 

The average pixel intensity of the top 500 rows of the 53 images without rolling ranged from 125 to 203.

![No Rolling](https://github.com/mattlichti/artifact-detection/blob/master/plots/no_rolling.png)

The average pixel intensity of the top 500 rows of the 3 images with with rolling ranged from 30 to 73

![Rolling](https://github.com/mattlichti/artifact-detection/blob/master/plots/rolling.png)

This makes it easy to train a model to differentiate between images with and without rolling.

## Bubble detection

![Bubble detection](https://github.com/mattlichti/artifact-detection/blob/master/plots/bubble%20detection.png)

The bubble detection can be run from the bubble_detection function in run.py


## Correlation between process parameters and artifacts

Looking at the microscope properties, the highest correlation with the artifacts was camera temperature. 
The p value .006 is significantly lower than the conventional threshold of statistical significance of .05. However, since I was making 22 comparisons (2 artifacts * 11 machine parameters), there is a much higher chance of false positives. Using a bonferroni correction, the p value of .006 is no longer statistivally significant because I would divide the threshold of .05 by 22. 

Even if camera temperature and bubbles are correlated, the correlation is likely caused by a confounding variable. The first 22 samples were taken when the camera temp was 70.5 degrees and the next 34 when it was 71 degrees. There are many possible reasons why there could more bubbles in the earlier samples than the later samples aside from the half degree change in temperature.

## Next steps

Improve bubble finding algorithm
Run on AWS

More data will allow cross validation
Run machine learning algorithms on machine parameters with more data

Find correlation with much more data so results are more likely to be statistically significant. 
