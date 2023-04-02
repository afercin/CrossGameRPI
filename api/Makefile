#title           :Makefile
#description     :Create all executable script for Unit
#author			 :Adrián Fernández Cintado <afercin@gmail.com>
#date            :20160726
#version         :1.0
#usage			 :makefile
#==============================================================================

all: scriptSource

clean:
	rm -rf _build
	rm -rf source/*.x.c

scriptSource:
	mkdir -p _build/

	pyinstaller --onefile source/changeResolution.py --distpath _build/ --workpath /tmp/

	cp source/cgAPI.py _build/

	cp -r source/apiModules _build/