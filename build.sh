#!/bin/bash -e
for folder in $(find . -maxdepth 1 -type d); do
    if [[ -d "$folder/source" ]]; then
        echo "##########################################"
        echo "# Building $folder"
        echo "##########################################"
        make -C $folder
    fi    
done
dpkg-buildpackage -rfakeroot -b -us -uc

mv /*.deb /src/release
ls -l /src/release

rm -f *.buildinfo
rm -f *.changes
rm $(find . -name "*.x.c") || :
rm $(find . -name "*.spec") || :