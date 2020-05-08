import MID_proc as mid
import os
import shutil
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import random

#set current date for use in filenames
DATE_TODAY = datetime.now().strftime('%m%d%Y')
FAKE_SUBS = ['7','13','101','102','99','990','9999']

def make_test_data(basedir=None):
	#set up some example directories and files for use with tests
	if not basedir:
		basedir= Path(os.getcwd())

	fake_subdir= basedir / 'MID_test_data' / 'subjects'
	fake_scriptsdir = fake_subdir.with_name('scripts')
	fake_swarmdir= fake_scriptsdir / 'swarm'
	fake_group_beh=basedir / 'MID_test_data' / 'group_behavior_data'

	os.makedirs(fake_swarmdir,exist_ok=True)
	os.makedirs(fake_group_beh,exist_ok=True)
        
	#set sub fake sub ID numbers; these were picked to test that prefix length calculation in make_param() works with a variety of ID lengths
	fake_sub_file = fake_scriptsdir / 'fake_sub_file.txt'
	fake_sub_file.write_text('\n'.join(FAKE_SUBS))

	for sub in FAKE_SUBS:
		os.makedirs(fake_subdir / f'sub-{sub}'/ 'meg' , exist_ok=True)
		os.makedirs(fake_subdir / f'sub-{sub}' / 'behavior', exist_ok=True)

	#make fake cue files for use in behavior data processing
	for sub in FAKE_SUBS:
		a=np.array([0]*78)
		b=np.array(np.linspace(10, 727, 78, False))
		cuemarks=np.column_stack((a,b))
		df = pd.DataFrame(cuemarks)
		df.to_csv(fake_subdir / f'sub-{sub}' / 'meg' / 'cue_marks', index=False, header=False, sep=' ')
        
	#make fake behavior data files (length based on maximum length of MID behavior file)
	for sub in FAKE_SUBS:
		beh_name=f'MID1-{sub}-1_behavior.txt'
		#create the three columns we're going to use with data those columns have IRL; I know this is REALLY clunky...but it works...
		win=['Win2']*26
		lose=['Lose2']*26
		cont=['Control']*26
		win.extend(lose)
		win.extend(cont)
		random.shuffle(win)
		cuewords=win
		col1=np.array(cuewords)
		resp=random.choices(['GoodResponse','NoResponse'], k=78)
		col2=np.array(resp)
		rt=np.random.randint(150,550,size=78)
		col3=rt
		df2=np.column_stack([col1,col2,col3])
		#add in top line that comes with actual e-prime data files and headers beneath it; top line will be removed so we need a throw-away top line in the fake data file too
		cola=np.array(['Cue'])
		colb=np.array(['ResponseType'])
		colc=np.array(['Target.RT'])
		df3=np.column_stack([cola,colb,colc])
		df4=pd.DataFrame(df2)
		df5=pd.DataFrame(df3)
		fake_beh=pd.concat([df5,df4],ignore_index=True)
		fake_beh.to_csv(fake_subdir / f'sub-{sub}' / 'behavior' / beh_name, sep='\t', mode='a', index=False)

	return fake_subdir,fake_sub_file,fake_group_beh


#first test is for the param file maker function
def test_make_param():
	'''This tests if make_param() can make parameter files with a few non-default inputsarguments and put them in fake subjects' meg folders directories.'''
	fake_subdir, fake_sub_file,fake_group_beh = make_test_data()
	mid.make_param(freq='alpha',rootdir=fake_subdir,Marker1='cue',marker1window='0 4')
	paramfiles_exist=[os.path.exists(fake_subdir / f'sub-{sub}' / 'meg' / 'alpha_cue.param') for sub in FAKE_SUBS]
	assert paramfiles_exist==[1]*len(FAKE_SUBS),'Param files were not created properly--oh no!'

	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)

        
#second test will test the swarm making functions
def test_make_swarms():
	'''This tests if make_swarm_newDs() and make_swarm_sam() make their respective swarm files with a fake subject list and some non-default args.'''
	fake_subdir, fake_sub_file,fake_group_beh = make_test_data()
	fake_swarmdir = fake_subdir.parent / 'scripts' / 'swarm'
	mid.make_swarm_newDs(subjectlist=fake_sub_file,newds='_MID_cue-f',marker='cue',timewindow='0 4',swarmdir=fake_swarmdir,subdir=fake_subdir)
	mid.make_swarm_sam(subjectlist=fake_sub_file,ds='_MID_cue-f.ds',marker='cue',freqband='highgamma',swarmdir=fake_swarmdir,subdir=fake_subdir)
	swarmfiles_exist=[os.path.exists(f'{fake_swarmdir}/newDs_{DATE_TODAY}.swarm'),os.path.exists(f'{fake_swarmdir}/sam_cov_highgamma_cue_{DATE_TODAY}.swarm'),os.path.exists(f'{fake_swarmdir}/sam_wts_highgamma_cue_{DATE_TODAY}.swarm'),os.path.exists(f'{fake_swarmdir}/sam_3d_highgamma_cue_{DATE_TODAY}.swarm')]

	assert swarmfiles_exist==[1,1,1,1],'Swarm files not created. UGH!'

	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)

        
#third, fourth, and fifth tests will check the behavior data functions
def test_make_markerfiles():
	'''This tests if make_markerfiles_MID() makes the 3 win, loss, and control marker files in each subjects' behavior directories.'''
	fake_subdir, fake_sub_file,fake_group_beh = make_test_data()
	mid.make_markerfiles_MID(fake_sub_file,fake_subdir)
	markerfiles_exist=[os.path.exists(fake_subdir / f'sub-{sub}' / 'meg' / f'{sub}_win.txt') for sub in FAKE_SUBS]+ [os.path.exists(fake_subdir / f'sub-{sub}' / 'meg' / f'{sub}_lose.txt') for sub in FAKE_SUBS]+[os.path.exists(fake_subdir / f'sub-{sub}' / 'meg' / f'{sub}_cont.txt') for sub in FAKE_SUBS]

	assert markerfiles_exist==[1]*(len(FAKE_SUBS)*3),'Marker files not found!'

	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)

def test_clean_beh():
	'''This tests if clean_beh_MID() makes and distributes cleaned behavior data csvs to each subject's behavior directories'''
	fake_subdir, fake_sub_file,fake_group_beh = make_test_data()
	mid.clean_beh_MID(fake_sub_file,fake_subdir,fake_group_beh)
	behfiles_exist=[os.path.exists(fake_subdir / f'sub-{sub}' / 'behavior' / f'{sub}_behavior_MID_bytrial.csv') for sub in FAKE_SUBS]
        
	assert behfiles_exist==[1]*len(FAKE_SUBS),'Behavior files are MIA!'
        
	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)

def test_masterbeh():
	'''This tests if clean_beh_MID() makes master descriptives file and puts it in output folder (generally some kind of group analysis folder)'''
	fake_subdir, fake_sub_file,fake_group_beh = make_test_data()
	mid.clean_beh_MID(fake_sub_file,fake_subdir,fake_group_beh)
	masterbeh_exists=os.path.exists(fake_group_beh / 'all_behavior_MID_bytrial.csv')
        
	assert masterbeh_exists==1, 'Master descriptives file is missing!'
        
	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)


if __name__=='__main__':
	test_make_param()
	test_make_swarms()
	test_make_markerfiles()
	test_clean_beh()
	test_masterbeh()


#celebrate
print('All tests passed! Woo!!')
