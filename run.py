import load_data as ld

def run():
  rolling = [15462, 15502, 15552]
  bubble_dict = {1: [15022, 15042, 15052, 15062, 15092, 15122, 15142, 15152,
                     15202, 15232, 15252, 15332, 15372, 15392, 15432, 15482,
                     15512],
                 2: [15102,  15172, 15182, 15282]}
  data = ld.LoadData()
  data.load_metadata('metadata.json')
  data.label_rolling(rolling)
  data.label_bubbles(bubbles=bubble_dict)
  data.pix_intensity('images')
  print data.df

if __name__ == '__main__':
  run()