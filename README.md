# artifact-detection

## Motivation


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



## Bubble detection

![Bubble detection](/path/to/image.jpg)


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
