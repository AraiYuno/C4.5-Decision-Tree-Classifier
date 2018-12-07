class Node:
	def __init__(self, isLeaf, attribute, gainRatio):
		self.attribute = attribute
		self.gainRatio = gainRatio
		self.isLeaf = isLeaf
		self.children = []