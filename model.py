from sklearn.lda import LDA
from scipy.stats import pearsonr

class Model(object):

	def __init__(self, df):
		self.df = df

	def corr(self):
		'''correlations between the machine properties and the artifacts'''
		return self.df.corr()[['bubbles', 'rolling']]

	def cam_temp(self):
		'''returns summary statistics for artifacts based on camera temp'''
		return self.df.groupby('camera_temp').describe()[['bubbles', 
														  'rolling']]
	def pix_intensity(self):
		'''returns summary statistics for pixel intensity based on rolling'''
		return self.df.groupby('rolling').describe()['pix_intensity'] 
														  
	def stat_signif(self, cols = ('bubbles', 'camera_temp')):
		return pearsonr(self.df[cols[0]], self.df[cols[1]])

	def train(self):
		mod = LDA():
		mod.train()