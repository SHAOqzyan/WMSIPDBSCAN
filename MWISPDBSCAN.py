
from astrodendro import Dendrogram

from astropy.io import fits
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np


from astropy.table import Table
from astrodendro import Dendrogram, ppv_catalog
from sklearn.cluster import DBSCAN



def dbscanClouds(COFITS,saveFITS=None):

	"""
	Only used to mask
	:param COFITS:
	:param saveFITS:
	:return:
	"""

	hdu= fits.open(COFITS)[0]

	data=hdu.data
	head=hdu.header
	goodIndices=np.where(data> 0.5  )

	coordinates= zip( goodIndices[0] , goodIndices[1] ,goodIndices[2]  )

	db = DBSCAN(eps=1.5 , min_samples= 16      ).fit(coordinates)


	labels = db.labels_

	#u,c= np.unique(labels,return_counts=True)

	#print len(u)

	mask=np.zeros_like(data)-1

	mask[goodIndices]= labels
	if saveFITS==None:
		fits.writeto("dbscanMask1Sigma.fits",mask,header=head,overwrite=True)

	else:
		fits.writeto(saveFITS ,mask,header=head,overwrite=True)


CO12FITS=  "G2650Local30.fits"
import datetime
if 1:
	#produceRMS( CO12FITS )
	#dbscanClouds(CO12FITS,saveFITS="G214.fits")
	print datetime.datetime.now()
	dbscanClouds(CO12FITS,saveFITS="G2650Local30DB.fits")
	print datetime.datetime.now()