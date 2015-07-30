import load_data as ld

def run(display=True):
  '''
  Loads metadata from 'metadata.json' and images from 'images' folder which
  both must be located in the same directory as the python files 
  '''
  # I manually labeled the images with artifacts in order to train the model
  # It's likely that I missed some of the bubbles during my visual inspection
  rolling = [15462, 15502, 15552]
  bubble_dict = {1: [15022, 15042, 15052, 15062, 15092, 15122, 15142, 15152,
                     15202, 15232, 15252, 15332, 15372, 15392, 15432, 15482,
                     15512],
                 2: [15102,  15172, 15182, 15282]}
  data = ld.LoadData()
  print "loading metadata and labeling artifacts"
  data.load_metadata('metadata.json')
  data.label_artifacts(bubbles=bubble_dict, rolling=rolling)
  data.pix_intensity('images', display=display)
  print data.df

def bubble_detection():
  ''' runs an example of the bubble detection which doesn't really work'''
  filename = 'images/15102_4eef5851-08cf-4836-9027-66945996b224.png'
  data = ld.LoadData()
  data.bubbles(filename,bottom_margin=7000, right_margin=1500)


if __name__ == '__main__':
  run()