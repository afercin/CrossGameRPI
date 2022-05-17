emulators="/emulators/rpi/emulators"
tmpfolder="/third-party"

mkdir -p "/emulators/rpi/emulators"

if [[ ! -d "$tmpfolder/ps1" ]]; then
    echo "Downloading PS1 emulator code..."
    git clone "https://github.com/stenzek/duckstation.git" -b dev "$tmpfolder/ps1"
else
    cd "$tmpfolder/ps1/"
    echo "Pulling PS1 emulator code..."
    git pull
fi

echo "Compiling PS1 emulator..."
mkdir "$tmpfolder/ps1/build/"
cd "$tmpfolder/ps1/build"
cmake -DCMAKE_BUILD_TYPE=Release -GNinja "$tmpfolder/ps1/"
ninja 

echo "Copying PS1 emulator files to emulator folder..."
mv "$tmpfolder/ps1/build/bin" "$emulators/ps1"

if [[ ! -d "$tmpfolder/psp" ]]; then
    echo "Downloading PSP emulator code..."
    git clone --recurse-submodules "https://github.com/hrydgard/ppsspp.git" "$tmpfolder/psp"
else
    cd "$tmpfolder/psp/"
    echo "Pulling PSP emulator code..."
    git pull
fi

echo "Compiling PS1 emulator..."
mkdir "$tmpfolder/psp/build/"
cd "$tmpfolder/psp/build/"
cmake ..
cmake -j 4 ..
make install

echo "Copying PSP emulator files to emulator folder..."
mkdir "$emulators/psp"
cp "$tmpfolder/psp/build/PPSSPPSDL" "$emulators/psp/"