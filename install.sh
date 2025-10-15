#!/bin/bash

current_dir=$(pwd)

sudo cp -ar "$current_dir" /usr/lib/

sudo ln -sf /usr/lib/olam_rofi/main.py /usr/bin/olam
sudo chmod +x /usr/bin/olam

echo "Installation complete."
