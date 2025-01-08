#!/bin/bash

# Update package list and upgrade existing packages
sudo apt-get update
sudo apt-get upgrade -y

#configure unattended updates
sudo apt install unattended-upgrades apt-listchanges -y
sudo dpkg-reconfigure -plow unattended-upgrades

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
sudo apt install nodejs -y

# Install Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install -y python3.12 python3-pip

# Install MariaDB
sudo apt install mariadb-server -y

# Install Nginx
sudo apt install nginx -y

# Enable firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
