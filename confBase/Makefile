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

	shc -v -r -f source/crossinit.sh
	mv source/crossinit.sh.x _build/crossinit

	shc -v -r -f source/restartx.sh
	mv source/restartx.sh.x _build/restartx

	shc -v -r -f source/restorepoint.sh
	mv source/restorepoint.sh.x _build/restorepoint

	pyinstaller --onefile source/simulateKeys.py --distpath _build/ --workpath /tmp/
