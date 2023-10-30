#!/bin/bash

sudo apt update
sudo apt -y upgrade
sudo apt -y install gnome-tweaks
sudo apt -y install vim
sudo apt -y install tmux
stty stop undef
git config --global user.email "kohzu.fumiya.code@gmail.com"
git config --global user.name "Fumiya Kohzu"
git config --global core.editor vim

#raspberry-piのときにいるかも？
#setxkbmap jp
