#title           :Makefile
#description     :Create all executable script for Unit
#author			 :Adrián Fernández Cintado <afercin@gmail.com>
#date            :20220627
#version         :1.0
#usage			 :makefile
#==============================================================================

all: build

clean:
	rm -rf ./rpi || :
	rm -rf ./usr/local || :
	rm -rf ./usr/share || :

build:
	mkdir -p ./rpi/emulators
	/emulators/build_scripts/n64_build.sh
	/emulators/build_scripts/ps1_build.sh
	/emulators/build_scripts/psp_build.sh