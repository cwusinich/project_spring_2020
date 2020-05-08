# project_spring_2020

[![CircleCI](https://circleci.com/gh/biof309/project_spring_2020/tree/master.svg?style=shield)](https://circleci.com/gh/biof309/project_spring_2020/tree/master)

## MID_proc
A very amateur python package by Christina Wusinich

Last updated: 04/08/2020

## Objective of package:  
A series of scripts for processing behavioral and MEG data from a reward processing task, called the Monetary Incentive Delay (MID) task.

## Background:  
The MID task shows various shapes which allow participants to win money, avoid losing money, or do nothing (a neutral condition) if they press a button within a particular time window following the shape. After pressing the button, they receive feedback indicating whether they won money, avoided losing money, or had no reward in either direction.

The goal of my initial analysis was to report on deep source activity (i.e. striatum in this case) in the task’s MEG data using synthetic aperture magnetometry (SAM) for source localization. Showing that this is possible in MEG (usually not known for deep source analyses) will pave the way for studying reward processing in mood disorders and the impact of novel treatments using MEG. Moving forward, we are going to (and already have done a bit) conduct analyses in different time windows in the task and in different frequency bands, so the scripts below were designed to make it easier to repeat processing steps with different parameters.

In terms of our analysis of behavior data, we need to gather mean reaction times and accuracy of button presses for analysis with an ANOVA (more details to come based on what factors will be involved).

## Files that need to be processed:  
-	Behavior data: a .txt output from the MID task that indicates button presses, timing of stimuli, etc.
-	MEG data: a CTF (NIH's MEG system) file of MEG data from the MID task
-	MRI data: structural MRIs for use with source localization (already converted to .nii before this)

## Setup of directories for use with this package:
-	Behavior data example: MID_data/subjects/sub-201/beh
-	MEG data example: MID_data/subjects/sub-201/meg
-	MRI data example: MID_data/subjects/sub-201/mri
-	swarm files: MID_data/scripts/swarm


# Processing steps (that this package helps with):  

##	Behavior processing
1.	**MID_beh.py** 
- make_markerfiles_MID(subjectlist,subdir_base): Makes marker files for more MEG processing; these markers will designate win/loss/neutral cues to be marked in the MEG file and are output as three separate .txt files to the subject’s MEG directory
-	clean_beh_MID(subjectlist,subdir_base,outputdir): Pulls columns from behavior data file and calculates mean RTs and accuracy by trial and subject and appends that to master behavior data sheet
2.	Input: cue markers text file (this is from a previous MEG processing step not included here), behavior text file
3.	Output: win/loss/neutral text files (3), two cleaned behavior csvs for each participant (deposited in their respective behavior folders), and master csv that includes mean reaction times and accuracy by participant and trial

##	Pre-SAM parameter file creation
1.	**make_paramfiles.py**:
-	make_param(freq,rootdir='/data/MoodGroup/07M0021_meg_analysis/MID_data/subjects', NumMarkers='1', Marker1='respwin', marker1window='0.5 2': Makes parameter files for use with SAM commands (see step below) and drops each param file into each subject's meg directory
2.	Input: function input parameters; it also needs to find subject folders in your "subjects" directory
3.	Output: a param file in each subject's meg directory

##	Create swarm files for MEG data processing
1.	**make_swarms.py**:
-	make_swarm_newDs(subjectlist,newds,marker,timewindow,swarmdir,subdir,origds='_MID-f.ds'): Makes a swarm file that will create new datasets from existing MEG datasets for all subjects in list (helpful if you want to look in a new time window or use different markers and make a fresh batch of datasets to work with)
-	make_swarm_sam(subjectlist,ds,marker,freqband,swarmdir,subdir): Makes three swarm files for all subjects in list; each swarm file has a a command for source localization in high gamma using SAM (from samsrcv3)
2. Note: origds is defaulted to the original filtered MID MEG data file
3.	Input: original MEG file (something.ds) and processinglist.txt (or some file with a list of participant ID numbers you want to include--one day this will be fancier, but this is what we're working with this week), MRI with fiducial markers set, parameter file (highgamma.param)
4.	Output: .swarm files in your swarm directory; also after running this, you will see the swarm command(s) you need to run as output in your terminal window


# Notes about this young and naive package
-	Obviously this package does not cover all of the MEG data processing steps involved for this task, but it has streamlined the process substantially and will hopefully one day grow up to be a mature MEG processing pipeline.
-	The SAM swarm script successfully creates the swarm files, and the swarm files run successfully (according to the output), but the files that are created are bad (as in not the same as if each SAM command was run individually and not in a swarm). 
- Future directions include solving the problem above, and making my scripts more useful and concise (any suggestions toward those latter goals would be appreciated!)
