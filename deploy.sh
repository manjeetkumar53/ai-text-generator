#!/bin/bash

# Constants
APP_DIR="/var/www/ai-text-generator"
SOCKET_FILE="$APP_DIR/myapp.sock"
NGINX_SITE_CONF="/etc/nginx/sites-available/myapp"
NGINX_SITE_LINK="/etc/nginx/sites-enabled/myapp"
VENV_DIR="$APP_DIR/venv"

echo "Deleting old app"
sudo rm -rf $APP_DIR

echo "Creating app folder"
sudo mkdir -p $APP_DIR 

echo "Moving files to app folder"
# Using rsync to avoid issues with `mv`
sudo rsync -av --exclude='deploy.sh' ./ $APP_DIR

# Set appropriate permissions for the app directory
sudo chown -R $USER:$USER $APP_DIR

# Navigate to the app directory
cd $APP_DIR

# Check if .env exists before moving
if [ -f env ]; then
    sudo mv env .env
fi

sudo apt-get update
echo "Installing Python and pip"
sudo apt-get install -y python3 python3-venv python3-pip

# Create a virtual environment
echo "Creating virtual environment"
python3 -m venv $VENV_DIR

# Activate the virtual environment
echo "Activating virtual environment"
source $VENV_DIR/bin/activate

# Install application dependencies from requirements.txt
echo "Installing application dependencies from requirements.txt"
pip install -r requirements.txt

# Install Gunicorn
echo "Installing Gunicorn"
pip install gunicorn

# Update and install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    echo "Installing Nginx"
    sudo apt-get install -y nginx
fi

# Configure Nginx to act as a reverse proxy if not already configured
if [ ! -f $NGINX_SITE_CONF ]; then
    echo "Configuring Nginx as reverse proxy"
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo bash -c "cat > $NGINX_SITE_CONF <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"
    sudo ln -s $NGINX_SITE_CONF $NGINX_SITE_LINK
    sudo systemctl restart nginx
else
    echo "Nginx reverse proxy configuration already exists."
fi

# Stop any existing Gunicorn process
echo "Stopping any existing Gunicorn processes"
sudo pkill gunicorn

# Start Gunicorn with the Flask application
echo "Starting Gunicorn..."
sudo $VENV_DIR/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 appserver:gunicorn_app --daemon

# Check if Gunicorn started correctly
echo "Checking Gunicorn status..."
if ! pgrep -f gunicorn > /dev/null; then
    echo "Gunicorn did not start correctly. Check the Gunicorn logs for errors."
    exit 1
fi

echo "Gunicorn started correctly. Starting Nginx..."
sudo systemctl restart nginx

# Check if Nginx started correctly
echo "Checking Nginx status..."
if ! pgrep -f nginx > /dev/null; then
    echo "Nginx did not start correctly. Check the Nginx logs for errors."
    exit 1
fi

echo "Nginx started correctly. Deployment complete!"