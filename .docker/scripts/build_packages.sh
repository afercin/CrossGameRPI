#!/bin/bash

chmod 775 ./*/DEBIAN
chmod 775 ./*/DEBIAN/*

compilationNumber=$(cat ./crossGameServer/DEBIAN/control | grep Version | awk '{print $2}')
newNumber=$(echo $compilationNumber | tr "." " " | awk '{print $1 "." $2 "." (($3+1))}')

for folder in $(find . -maxdepth 1 -name "crossGame*" -type d)
do
    sed -i "s/$compilationNumber/$newNumber/" "$folder/DEBIAN/control"
done

echo "##########################################################################"
echo "###################### Building new version ($newNumber) ######################"
echo "##########################################################################"
echo
for package in $(find . -maxdepth 1 -type d -name "crossGame*" | cut -d "/" -f2); do
    echo "## Creating $package package..."
    dpkg-deb --build --root-owner-group "$package"
    echo "## Moving package to release folder"
    mv "$package.deb" "/release/$package.deb"
    echo
done
echo "## Done"
