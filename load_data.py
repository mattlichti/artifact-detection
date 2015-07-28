import json
import pandas as pd

class LoadData(object):

	def __init__(self):
		# list of properties from metadata used in analysis
		self.prop_list = ['stage_x_current', 'stage_x_position', 'stage_y_current',
		'stage_y_position', 'stage_z_current', 'stage_z_position',
		'aux_flow_level', 'aux_temp', 'camera_lineFeedback','camera_temp']
		self.df = None # dataframe of information about slices

	def load_metadata(self, filename):
		f = open(filename)
		self.df = pd.DataFrame(json.loads(f.read()))
		self.df.set_index('sliceIndex', inplace=True)
		self.df = self.df[['time', 'properties']]
		self.df.time = pd.to_datetime(self.df.time, unit='ms')
		for prop in self.prop_list:
			self.df[prop] = self.df.properties.map(lambda x: x[prop])
		self.df.drop('properties', inplace=True, axis = 1)

	def label_bubbles(self, bubbles = {}):
		''' input dictionary containing number of bubbles as keys
		and list of indices of slices with that number of bubbles'''
		
		self.df['bubbles'] = 0
		for num_bubbles, slice_list in bubbles.iteritems():
			print num_bubbles
			self.df.bubbles[slice_list] = num_bubbles
	
	def label_rolling(self, rolling = []):
		''' input list with indices of slices with rolling'''
		self.df['rolling'] = 0	
		self.df.rolling[rolling] = 1

if __name__ == '__main__':
	rolling = [15462, 15502, 15552]
	bubble_dict = {1: [15022, 15042, 15052, 15062, 15092, 15122, 15142, 15152,
				15202, 15232, 15252, 15332, 15372, 15392, 15432, 15482,
				15512], 2: [15102,  15172, 15182, 15282]}
	data = LoadData()
	data.load_metadata('metadata.json')
	data.label_rolling(rolling)
	data.label_bubbles(bubbles=bubble_dict)
	print data.df


