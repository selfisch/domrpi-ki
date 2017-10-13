#!/bin/bash

hostname=`cat /etc/hostname`

cd ~

mkdir -p ~/domrpi-ki

# Mopidy sources
 wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
 sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/stretch.list

# apt
 sudo apt-get update
 sudo apt-get purge -y python python-dev python-pip

 sleep 5

 sudo apt-get clean
 sudo apt-get autoclean
 sudo apt-get -y autoremove

 sleep 5

 sudo apt-get install -y mopidy libspotify12 libspotify-dev \
 git python3 python3-dev python3-pip libffi-dev python3-spotify

 sleep 5

# pip
 sudo pip3 install evdev python-mpd2 Mopidy-Iris pyspotify mopidy-spotify

# git
 cd ~/domrpi-ki
 git clone https://github.com/selfisch/domrpi-ki.git

# mopidy config
mv /etc/mopidy/mopidy.conf /etc/mopidy/mopidy.bak
touch /etc/mopidy/mopidy.conf
chown mopidy:root /etc/mopidy/mopidy.conf

echo "[core]
cache_dir = /var/cache/mopidy
config_dir = /etc/mopidy
data_dir = /var/lib/mopidy

[http]
enabled = true
hostname = 0.0.0.0
port = 6680
static_dir =
zeroconf = Mopidy HTTP server on $hostname

[audio]
mixer = software
mixer_volume =
output = alsasink
buffer_time =

[logging]
config_file = /etc/mopidy/logging.conf
debug_file = /var/log/mopidy/mopidy-debug.log

[local]
media_dir = /var/lib/mopidy/media

[m3u]
playlists_dir = /var/lib/mopidy/playlists" > /etc/mopidy/mopidy.conf

if [ -f ~/domrpi-ki/conf/spotify.conf ] then
 exec  ~/domrpi-ki/conf/spotify.conf
else
 echo "Wenn Spotify in Mopidy genutzt werden soll, bitte die Datei
 ~/domrpi-ki/conf/spotify.template beachten."

systemctl enable mopidy
