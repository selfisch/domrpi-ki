#!/bin/bash

hostname=`cat /etc/hostname`

cur_dir=`pwd`

# check sudo
 sudo su

# # Mopidy sources
#  wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
#  sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/stretch.list
#
# # apt
#  apt-get update
#  apt-get purge -y python python-dev python-pip
#
#  sleep 5
#
#  apt-get -y dist-upgrade
#
#  sleep 5
#
#  apt-get clean
#  apt-get autoclean
#  apt-get -y autoremove
#
#  sleep 5
#
#  apt-get install -y mopidy libspotify12 libspotify-dev \
#  git python3 python3-dev python3-pip libffi-dev python3-spotify
#
#  sleep 5
#
# # pip
#  pip3 install evdev python-mpd2 Mopidy-Iris pyspotify mopidy-spotify

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

if [ -f $cur_dir/conf/spotify.conf ] then
 exec $cur_dir/conf/spotify.conf
else
 echo ""
 echo "Wenn Spotify in Mopidy genutzt werden soll, bitte die Datei
 $cur_dir/conf/spotify.template beachten."

if [ ! -f $cur_dir/plist.csv ] then
 echo ""
 echo "Bitte plist.template beachten!"
fi

systemctl enable mopidy
