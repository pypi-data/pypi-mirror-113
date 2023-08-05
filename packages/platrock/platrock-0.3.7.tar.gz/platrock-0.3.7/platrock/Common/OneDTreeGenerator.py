"""
Copyright (c) 2017, 2018, 2019 Irstea
Copyright (c) 2017, 2018, 2019 François Kneib
Copyright (c) 2017, 2018, 2019 Franck Bourrier
Copyright (c) 2017, 2018, 2019 David Toe
Copyright (c) 2017, 2018, 2019 Frédéric Berger
Copyright (c) 2017, 2018, 2019 Stéphane Lambert

This file is part of PlatRock.

PlatRock is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

PlatRock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np

class TreeGenerator():
	def __init__(self,treesDensity=0.1,trees_dhp=0.3,dRock=0.5,sim=None): # in ar/m², meters.
		self.treesDensity = treesDensity
		self.d_ar = trees_dhp
		self.d_roc = dRock
		self.sim=sim
		self.precomputeData()
	def precomputeData(self):
		self.l=1/np.sqrt(self.treesDensity)			# virtual distance between two trees
		self.q=1-(self.d_ar+self.d_roc)/self.l		# probability to pass through 1 screen of trees without impact, i.e. through to travel self.l distance without impact.
		self.prob0=self.PDF_impact(0)				# probability to hit a tree immediately
		if(self.sim==None):
			self.random_generator=np.random
		else:
			self.random_generator=self.sim.random_generator
	
	# NOTE: NOT USED, just for information.
	def CDF_impact(self,x):
		return 1-self.q**(x/self.l)
	def PDF_impact(self,x):
		return -(self.q**(x/self.l))/self.l * np.log(self.q)
	# This will get one random number between 0 and the PDF maximum value (at dist=0), then get a distance from this PDF.
	def getOneRandomTreeImpactDistance(self):
		random=self.prob0*self.random_generator.rand()
		return np.log(-random*self.l/np.log(self.q))*self.l/np.log(self.q)


