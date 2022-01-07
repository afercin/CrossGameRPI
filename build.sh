#!/bin/bash

chmod 775 ./*/DEBIAN
chmod 775 ./*/DEBIAN/*


compilationNumber=$(cat ./crossGameApp/DEBIAN/control | grep Version | awk '{print $2}')
newNumber=$(echo $compilationNumber | tr "." " " | awk '{print $1 "." $2 "." (($3+1))}')

for folder in $(find . -maxdepth 1 -name "crossGame*" -type d)
do
    sed -i "s/$compilationNumber/$newNumber/" "$folder/DEBIAN/control"
done

echo "##########################################################################"
echo "###################### Building new version ($newNumber) ######################"
echo "##########################################################################"
echo
echo "## Deleting old packages..."
rm ./*.deb
echo
echo "## Creating crossgameapp package..."
dpkg-deb --build --root-owner-group ./crossGameApp
echo
echo "## Creating crossgameemulators package..."
dpkg-deb --build --root-owner-group ./crossGameEmulators
echo
echo "## Creating crossgameserver package..."
dpkg-deb --build --root-owner-group ./crossGameServer
echo
echo "## Creating crossgameweb package..."
dpkg-deb --build --root-owner-group ./crossGameWeb
echo
echo "## Done"