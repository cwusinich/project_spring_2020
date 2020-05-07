#CW 5.6.2020
#written for python 3.7
#makes .param files and puts them in each subject's meg folder
#make sure to set param variables you want in here or when running the function!

import os,sys

#set directory, subject list, and some other things
default_rootdir='/data/MoodGroup/07M0021_meg_analysis/MID_data/subjects/'
alpha=['alpha','8 14']
beta=['beta','15 29']
gamma=['gamma','30 60']
highgamma=['highgamma','62 118']

#set default variables here:
default_NumMarkers='1'
default_Marker1='respwin'
default_marker1window='0.5 2'
default_freq=highgamma

#setting more variables
XBounds='-10 10'
YBounds='-9 9'
ZBounds='0 15'
ImageStep='.5'
ImageMetric='Power'
Model='Nolte'
CovType='SUM'
ImageFormat='TLRC 5'

def make_param(rootdir=default_rootdir, freq=default_freq, NumMarkers=default_NumMarkers, Marker1=default_Marker1, marker1window=default_marker1window):
	"""Makes param files for each subject in their meg folder."""
	#define subject list and some other things for the file
	root, dirs, files = os.walk(rootdir).__next__()
	sublist=list(dirs)	
	freqname,freqband=freq
	OrientBand=freqband
	NoiseBand=freqband
	CovBand=freqband
	ImageBand=freqband
	DataSegment=marker1window

	#bestow an appropriate name upon the new param file	
	paramfile_name=f'{freqname}_{Marker1}.param'
	
	#make param file for each subject and drop it in their meg folder
	for sub in sublist:
		new_paramfile=open(f'{rootdir}/{sub}/meg/{paramfile_name}','w+')	
		new_paramfile.write(f"""NumMarkers {NumMarkers}\nMarker1 {Marker1} {marker1window} TRUE\nOrientBand {OrientBand}\nNoiseBand {NoiseBand}\nCovBand {CovBand}\nImageBand {ImageBand}\nDataSegment {DataSegment}\nXBounds {XBounds}\nYBounds {YBounds}\nZBounds {ZBounds}\nImageStep {ImageStep}\nImageMetric {ImageMetric}\nPrefixLength {str(len(sub))}\nMRIDirectory {rootdir}{sub}/mri\nModel {Model}\nCovType {CovType}\nImageFormat {ImageFormat}""")
		new_paramfile.close()

	print("Param files have been added!")

if __name__=='__main__':
	make_param()
