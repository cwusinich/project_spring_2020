#CW 4.19.2020
#written for python 3.7

#output of these functions include marker files (for marker placement in MEG file processing) and behavioral data results (adds them to master spreadsheet)

import sys,os
import csv
import numpy as np
import pandas as pd
import statistics

#set some variables
rootdir='/data/MoodGroup/07M0021_meg_analysis/MID_data/'
default_sublist=rootdir + 'scripts/swarm/processinglist.txt'
subdir_pref=rootdir + 'subjects/' + 'sub-'

##############################
#STEP 1: MAKE MARKER TXT FILES
#MEG preprocessing step 1 must be run first so that the cue files exist
def make_markerfiles_MID(subjectlist=default_sublist):
	"""Makes marker text files for each subject in input list and puts them in subject's meg folder."""	
	sublist=open(subjectlist, 'r')
	proclist=sublist.readlines()
	proclist=map(lambda x: x.strip(), proclist)
	#loop through all subjects in input list begins here!
	for subject in proclist:
		subdir=subdir_pref + subject
		#pull data from cue_marks file
		stimtime=pd.read_csv(subdir + '/meg/cue_marks',delimiter=' ',names=["Onset","Time"])

		#read MID behavior file
		data_read=pd.read_csv(subdir + '/behavior/MID1-' + subject + '-1_behavior.txt',delimiter='\t',skiprows=1,encoding='utf-16',engine='python')

		#pull data from cue file and behavior file to make a stimtimes variables (includes all trial types)
		trial=data_read[['Cue']]
		frames=[trial,stimtime]
		stimtimes_full=pd.concat(frames,axis=1)

		#from stimtimes_full, pulls out win stim times and adds to a matrix (df_#_win)
		stimtimes_win=stimtimes_full[stimtimes_full.Cue=='Win2']
		df_win=stimtimes_win[stimtimes_win.columns[1:3]]

		#repeats the above for lose stims
		stimtimes_lose=stimtimes_full[stimtimes_full.Cue=='Lose2']
		df_lose=stimtimes_lose[stimtimes_lose.columns[1:3]]

		#repeats the above for control stims
		stimtimes_cont=stimtimes_full[stimtimes_full.Cue=='Control']
		df_cont=stimtimes_cont[stimtimes_cont.columns[1:3]]

		#adds win, lose, and control stim time matrices each to its own text file in each subjects meg folder; these text files are used in MEG preprocessing step 2 to add trial type stim markers
		df_win.to_csv(subdir + '/meg/' + subject + '_win.txt',index=False,header=False,sep=' ')
		df_lose.to_csv(subdir + '/meg/' + subject + '_lose.txt',index=False,header=False,sep=' ')
		df_cont.to_csv(subdir + '/meg/' + subject + '_cont.txt',index=False,header=False,sep=' ')


#####################################################
#STEP 2: CLEAN MID BEHAVIORAL DATA AND OUTPUT DESCRIPTIVES
def clean_beh_MID(subjectlist=default_sublist):
	"""Makes cleaned behavior file and descriptives file (mean reaction time and accuracy by win/lose/control trial type) for each subject and puts it in their beh folder and a group behavior files folder"""
	sublist=open(subjectlist, 'r')
	processinglist=sublist.readlines()
	processinglist=map(lambda x: x.strip(), processinglist)
	#initiate aggregate df for later
	df_all=[]
	#loop through all subjects in input list begins here!
	for subject in processinglist:
		subdir=subdir_pref + subject
		#read in subject's behavior data file
		data_read=pd.read_csv(subdir + '/behavior/MID1-' + subject + '-1_behavior.txt',delimiter='\t',skiprows=1,encoding='utf-16',engine='python')
		behavior=data_read[['Cue','ResponseType','Target.RT']]

		#assign win/loss/control hits and misses to variables respectively
		behavior_win=behavior[behavior.Cue=='Win2']
		behavior_win_hit=behavior_win[behavior_win.ResponseType=='GoodResponse']
		behavior_win_miss=behavior_win[behavior_win.ResponseType=='NoResponse']

		behavior_lose=behavior[behavior.Cue=='Lose2']
		behavior_lose_hit=behavior_lose[behavior_lose.ResponseType=='GoodResponse']
		behavior_lose_miss=behavior_lose[behavior_lose.ResponseType=='NoResponse']

		behavior_cont=behavior[behavior.Cue=='Control']
		behavior_cont_hit=behavior_cont[behavior_cont.ResponseType=='GoodResponse']
		behavior_cont_miss=behavior_cont[behavior_cont.ResponseType=='NoResponse']

		#calculate reaction times and accuracy for each trial type and assign to variables respectively
		win_hit_RT=behavior_win_hit['Target.RT'][behavior_win_hit['Target.RT']!=0].mean()
		win_hit_acc=behavior_win_hit.count()
		win_miss_RT=behavior_win_miss['Target.RT'][behavior_win_miss['Target.RT']!=0].mean()
		win_miss_acc=behavior_win_miss.count()
		lose_hit_RT=behavior_lose_hit['Target.RT'][behavior_lose_hit['Target.RT']!=0].mean()
		lose_hit_acc=behavior_lose_hit.count()
		lose_miss_RT=behavior_lose_miss['Target.RT'][behavior_lose_miss['Target.RT']!=0].mean()
		lose_miss_acc=behavior_lose_miss.count()
		cont_hit_RT=behavior_cont_hit['Target.RT'][behavior_cont_hit['Target.RT']!=0].mean()
		cont_hit_acc=behavior_cont_hit.count()
		cont_miss_RT=behavior_cont_miss['Target.RT'][behavior_cont_miss['Target.RT']!=0].mean()
		cont_miss_acc=behavior_cont_miss.count()

		#create dataframe for holding these variables; Type = type of trial (win, lose, control), Outcome = outcome of trial (hit, miss), RT = mean reaction times for each trial type/outcome, Acc = mean accuracy for each trial type/outcome
		d={'Type':['Win','Win','Lose','Lose','Cont','Cont'],
		   'Outcome':['Hit','Miss','Hit','Miss','Hit','Miss'],
		   'RT':[win_hit_RT,win_miss_RT,lose_hit_RT,lose_miss_RT,cont_hit_RT,cont_miss_RT],
		   'Acc':[win_hit_acc.Cue,win_miss_acc.Cue,lose_hit_acc.Cue,lose_miss_acc.Cue,cont_hit_acc.Cue,cont_miss_acc.Cue]}
		df=pd.DataFrame(d)

		#put dataframe from above into a csv (in case we want this data at some point)
		df.to_csv(subdir + '/behavior/' + subject + '_behavior_MID.csv',index=False,sep=' ')

		#calculate mean RTs for each trial type (collapsing outcome)
		win_RT=behavior_win['Target.RT'][behavior_win['Target.RT']!=0].mean()
		lose_RT=behavior_lose['Target.RT'][behavior_lose['Target.RT']!=0].mean()
		cont_RT=behavior_cont['Target.RT'][behavior_cont['Target.RT']!=0].mean()

		#calculate average accuracy for each trial type (collapsing outcome)
		win_acc=win_hit_acc.Cue/26
		lose_acc=lose_hit_acc.Cue/26
		cont_acc=cont_hit_acc.Cue/26

		#make new dataframe for collapsed data
		d_2={'Type':['Win','Lose','Cont'],
		   'RT':[win_RT,lose_RT,cont_RT],'Acc':[win_acc,lose_acc,cont_acc]}
		df_2=pd.DataFrame(d_2)

		#put dataframe from above into a csv in subject's behavior directory (this is the data we want to analyze for now)
		df_2.to_csv(subdir + '/behavior/' + subject + '_behavior_MID_bytrial.csv',index=False,sep=' ')

		#put dataframe from above into a csv in aggregate behavior data folder
		df_2.to_csv(rootdir + 'processed_MID_all/behavior_all/' + subject + '_behavior_MID_bytrial.csv',index=False,sep=' ')

		#add each subject's collapsed data into one csv with their subject number
		df_2['Subject']=subject
		df_all.append(df_2)
	df_all=pd.concat(df_all)
	df_all.to_csv(rootdir + 'processed_MID_all/behavior_all/all_behavior_MID_bytrial.csv',index=False,sep=' ')

if __name__=='__main__':
	make_markerfiles_MID()	
	clean_beh_MID()
