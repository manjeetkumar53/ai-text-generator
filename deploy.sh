#!/bin/bash

echo "deleting old app"
sudo rm -rf /var/www/

echo "creating app folder"
sudo mkdir -p /var/www/ai-text-generator 

echo "moving files to app folder"
sudo mv  * /var/www/ai-text-generator

# Navigate to the app directory
cd /var/www/ai-text-generator/

# Move environment file
sudo mv env .env

# Install Python and pip
echo "installing python and pip"
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Create and activate virtual environment
echo "creating virtual environment"
python3 -m venv .venv
source .venv/bin/activate

# Install application dependencies from requirements.txt
echo "Install application dependencies from requirements.txt"
python3 -m pip install -r requirements.txt

# Update and install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    echo "Installing Nginx"
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Configure Nginx to act as a reverse proxy if not already configured
if [ ! -f /etc/nginx/sites-available/myapp ]; then
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo bash -c 'cat > /etc/nginx/sites-available/myapp <<EOF
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/ai-text-generator/myapp.sock;
    }
}
EOF'

    sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
    sudo systemctl restart nginx
else
    echo "Nginx reverse proxy configuration already exists."
fi

# Stop any existing Gunicorn process
sudo pkill gunicorn
sudo rm -rf myapp.sock

# Start Gunicorn with the Flask application
# Replace 'server:app' with 'yourfile:app' if your Flask instance is named differently.
# gunicorn --workers 3 --bind 0.0.0.0:8000 server:app &
echo "starting gunicorn"
sudo gunicorn --workers 3 --bind unix:myapp.sock  appserver:app --user www-data --group www-data --daemon
echo "started gunicorn 🚀"
