# CCSPY

## Python-based Connctome Computation System

The tools of the Connectome Computation System.



## Download and Install

Install latest release python package.

First, install the python package and all of its bundled data and scripts. You can do this with a single command with pip.

**Note** the newest release of ccspy requires python 3 (python 2 no longer supported).

To install with pip, type the following in a terminal.
```sh
pip install ccspy
```



## ccspy Tools

+ **ccspy_anat_01_pre_freesurfer**:

  there are two options in this tool.

  + --CCS_DIR
  + --subject

+ **ccspy_anat_02_freesurfer**:

  there are three options in this tool.

  + --CCS_DIR
  + --SUBJECTS_DIR
  + --subject

+ **ccspy_anat_03_postfs**:

  there are three options in this tool.

  + --CCS_DIR
  + --SUBJECTS_DIR
  + --subject

+ **ccspy_anat**:

  ccspy_anat is a combination of ccspy_anat_01_pre_freesurfer, ccspy_anat_02_freesurfer and ccspy_anat_03_postfs. There are three options in this tool.

  + --CCS_DIR
  + --SUBJECTS_DIR
  + --subject



## Examples

```shell
ccspy_anat_01_pre_freesurfer --CCS_DIR /usr/local --subject 0001

ccspy_anat_02_freesurfer --CCS_DIR /usr/local --SUBJECTS_DIR /usr/local/freesurfer/7.1.1-1/subjects --subject 0001

ccspy_anat_03_postfs --CCS_DIR /usr/local --SUBJECTS_DIR /usr/local/freesurfer/7.1.1-1/subjects --subject 0001

ccspy_anat --CCS_DIR /usr/local --SUBJECTS_DIR /usr/local/freesurfer/7.1.1-1/subjects --subject 0001
```

