#!/usr/bin/env bash

# install carthage
if [[ $1 == "local" ]]; then
    brew install carthage
fi

# install appium server cli
if [[ $1 == "local" ]]; then
    sudo npm install -g appium@1.16.0 #--unsafe-perm=true --allow-root
    npm install wd
fi

# install external python modules
sudo pip install -r requierments.txt
