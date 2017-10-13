#!/bin/bash

hostname=`cat /etc/hostname`

cur_dir=`pwd`

# check sudo
 sudo ls -al

# # Mopidy sources
#  wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
#  sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/stretch.list
#
# # apt
#  sudo apt-get update
#  sudo apt-get purge -y python python-dev python-pip
#
#  sleep 5
#
#  sudo apt-get -y dist-upgrade
#
#  sudo sleep 5
#
#  sudo apt-get clean
#  sudo apt-get autoclean
#  sudo apt-get -y autoremove
#
#  sleep 5
#
#  sudo apt-get install -y mopidy libspotify12 libspotify-dev \
#  git python3 python3-dev python3-pip libffi-dev python3-spotify
#
#  sleep 5
#
# # pip
#  sudo pip3 install evdev python-mpd2 Mopidy-Iris pyspotify mopidy-spotify

# mopidy config
 sudo mv /etc/mopidy/mopidy.conf /etc/mopidy/mopidy.bak
 sudo touch /etc/mopidy/mopidy.conf
 sudo chown mopidy:root /etc/mopidy/mopidy.conf

 sudo conf/mopidy.conf

if [ -f $cur_dir/conf/spotify.conf ]:
then
 sudo $cur_dir/conf/spotify.conf
else
 echo ""
 echo "Wenn Spotify in Mopidy genutzt werden soll, bitte die Datei
 $cur_dir/conf/spotify.template beachten."

if [ ! -f $cur_dir/plist.csv ]:
then
 echo ""
 echo "Bitte plist.template beachten!"
fi

sudo systemctl enable mopidy
sudo service mopidy restart
