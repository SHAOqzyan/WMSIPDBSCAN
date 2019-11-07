
from astrodendro import Dendrogram

from astropy.io import fits
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np


from astropy.table import Table
from astrodendro import Dendrogram, ppv_catalog
from sklearn.cluster import DBSCAN
import datetime


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


def getMaskFromDBFITS(CO12FITS , DBFITS):

	hdu= fits.open(CO12FITS)[0]

	dataCO=hdu.data
	headCO=hdu.header

	hdu= fits.open(DBFITS)[0]

	dataDB=hdu.data

	dataCO[dataDB<0]=-1

	fits.writeto("DBMaskedCO.fits",dataCO,header=headCO,overwrite=True  )


def doDendro(maskedCOFITS):
	hdu= fits.open(maskedCOFITS)[0]

	dataCO=hdu.data
	headCO=hdu.header

	d = Dendrogram.compute(dataCO, min_value=0,  verbose=1, min_npix=16, min_delta=1.5 )

	d.save_to( "localDendro.fits"  )






CO12FITS=  "G2650Local30.fits"


if 1:
	doDendro("DBMaskedCO.fits")

	#getMaskFromDBFITS(CO12FITS,"G2650Local30DB.fits")




if 0:
	#produceRMS( CO12FITS )
	#dbscanClouds(CO12FITS,saveFITS="G214.fits")
	print datetime.datetime.now()
	dbscanClouds(CO12FITS,saveFITS="G2650Local30DB.fits")
	print datetime.datetime.now()