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

	fake_subdir= basedir / "MID_test_data" / "subjects"
	fake_scriptsdir = fake_subdir.with_name("scripts")
	fake_swarmdir= fake_scriptsdir / "swarm"

	os.makedirs(fake_swarmdir,exist_ok=True)

	#set sub fake sub ID numbers; these were picked to test that prefix length calculation in make_param() works with a variety of ID lengths
	fake_sub_file = fake_scriptsdir / "fake_sub_file.txt"
	fake_sub_file.write_text('\n'.join(FAKE_SUBS))

	for sub in FAKE_SUBS:
		os.makedirs(fake_subdir / f"sub-{sub}"/ "meg" , exist_ok=True)
		os.makedirs(fake_subdir / f"sub-{sub}" / "behavior", exist_ok=True)
	return fake_subdir,fake_sub_file

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
		fake_beh=pd.DataFrame(df2,columns=['Cue','ResponseType','Target.RT'])
		fake_beh.to_csv(fake_subdir / f'sub-{sub}' / 'behavior' / beh_name, sep=' ', mode='a', index=False)


#first test is for the param file maker function
def test_make_param():
	"""This tests if make_param() can make parameter files with a few non-default inputsarguments and put them in fake subjects' meg folders."""
	fake_subdir, _ = make_test_data()
	mid.make_param(rootdir=fake_subdir,Marker1='cue', marker1window='0 4')
	paramfiles_exist=[os.path.exists(fake_subdir / f"sub-{sub}" / "meg" / "highgamma_cue.param") for sub in FAKE_SUBS]
	assert paramfiles_exist==[1]*len(FAKE_SUBS),'Param files were not created properly--oh no!'

	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)

        
#second test will test the swarm making functions
def test_make_swarms():
	"""This tests if make_swarm_newDs() and make_swarm_sam() make their respective swarm files with a fake subject list and some non-default args"""
	fake_subdir, fake_sub_file = make_test_data()
	fake_swarmdir = fake_subdir.parent / "scripts" / "swarm"
	mid.make_swarm_newDs(subjectlist=fake_sub_file,newds='_MID_cue-f',marker='cue',timewindow='0 4',swarmdir=fake_swarmdir)
	mid.make_swarm_sam(subjectlist=fake_sub_file,ds='_MID_cue-f.ds',marker='cue',swarmdir=fake_swarmdir)
	swarmfiles_exist=[os.path.exists(f'{fake_swarmdir}newDs_{DATE_TODAY}.swarm'),os.path.exists(f'{fake_swarmdir}sam_cov_highgamma_cue_{DATE_TODAY}.swarm'),os.path.exists(f'{fake_swarmdir}sam_wts_highgamma_cue_{DATE_TODAY}.swarm'),os.path.exists(f'{fake_swarmdir}sam_3d_highgamma_cue_{DATE_TODAY}.swarm')]

	assert swarmfiles_exist==[1,1,1,1],'Swarm files not created. UGH!'

	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)

        
#third test will check the behavior data functions (still under construction)
def test_clean_beh():
	"""This tests if 

	#remove the evidence
	shutil.rmtree(fake_subdir.parent, ignore_errors=False, onerror=None)


if __name__=='__main__':
	test_make_param()
	test_make_swarms()



#celebrate
print('All tests passed! Woo!!')
