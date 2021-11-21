#!/bin/bash

chmod 775 ./*/DEBIAN
chmod 775 ./*/DEBIAN/*


compilationNumber=$(cat ./crossGameApp/DEBIAN/control | grep Version | awk '{print $2}')
newNumber=$(echo $compilationNumber | tr "." " " | awk '{print $1 "." $2 "." (($3+1))}')

sed -i "s/$compilationNumber/$newNumber/" "./crossGameApp/DEBIAN/control"
sed -i "s/$compilationNumber/$newNumber/" "./crossGameServer/DEBIAN/control"

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
echo "## Creating crossgameapp package..."
dpkg-deb --build --root-owner-group ./crossGameServer
echo
echo "## Done"