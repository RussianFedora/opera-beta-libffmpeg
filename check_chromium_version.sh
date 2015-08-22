#!/bin/sh
mkdir -p ./opera-beta-$1
pushd ./opera-beta-$1 &> /dev/null
echo -en "\033[0;35m    Downloading Opera Beta package:\033[0m\n"
wget -N -q --show-progress ftp://ftp.opera.com/pub/opera-beta/$1/linux/opera-beta_$1_amd64.deb
echo -en "\033[0;35m    Opera Beta package hash:\033[0m\n"
echo -en "\033[0;32m$(md5sum opera-beta_$1_amd64.deb)\033[0m\n"
ar p opera-beta_$1_amd64.deb data.tar.xz | tar -xJf-
CHROMIUM_VER=$(strings ./usr/lib/x86_64-linux-gnu/opera-beta/opera-beta | grep Chrome/ | cut --delimiter=/ --fields=2)
echo -en "\033[0;35m    Chromium version:\033[0m\n"
echo -en "\033[0;32m$(echo $CHROMIUM_VER)\033[0m\n"
echo -en "\033[0;35m    Downloading Chromium sources archive:\033[0m\n"
wget -N -q --show-progress https://commondatastorage.googleapis.com/chromium-browser-official/chromium-$CHROMIUM_VER.tar.xz
echo -en "\033[0;35m    Chromium sources archive hash:\033[0m\n"
echo -en "\033[0;32m$(md5sum chromium-$CHROMIUM_VER.tar.xz)\033[0m\n"
popd &> /dev/null
exit 0
