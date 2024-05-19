#!/bin/bash

# Constants
APP_DIR="/var/www/ai-text-generator"
SOCKET_FILE="$APP_DIR/myapp.sock"
NGINX_SITE_CONF="/etc/nginx/sites-available/myapp"
NGINX_SITE_LINK="/etc/nginx/sites-enabled/myapp"
VENV_DIR="$APP_DIR/venv"

# Run the script as the correct user
sudo -u ec2-user bash

echo "Deleting old app"
rm -rf $APP_DIR

echo "Creating app folder"
mkdir -p $APP_DIR

echo "Moving files to app folder"
rsync -av --exclude='deploy.sh' ./ $APP_DIR

# Set appropriate permissions for the app directory
chown -R ec2-user:ec2-user $APP_DIR

# Navigate to the app directory
cd $APP_DIR

# Check if .env exists before moving
if [ -f env ]; then
    mv env .env
fi

echo "Installing Python and pip"
apt-get update
apt-get install -y python3 python3-venv python3-pip

# Create a virtual environment
echo "Creating virtual environment"
python3 -m venv $VENV_DIR

# Activate the virtual environment
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
    apt-get install -y nginx
fi

# Configure Nginx to act as a reverse proxy if not already configured
if [ ! -f $NGINX_SITE_CONF ]; then
    echo "Configuring Nginx as reverse proxy"
    rm -f /etc/nginx/sites-enabled/default
    cat > $NGINX_SITE_CONF <<EOF
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
EOF
    ln -s $NGINX_SITE_CONF $NGINX_SITE_LINK
    systemctl restart nginx
else
    echo "Nginx reverse proxy configuration already exists."
fi

# Stop any existing Gunicorn process
echo "Stopping any existing Gunicorn processes"
pkill gunicorn

# Start Gunicorn with the Flask application
echo "Starting Gunicorn..."
$VENV_DIR/bin/gunicorn --workers 3 --bind unix:$SOCKET_FILE --daemon
chmod 666 $SOCKET_FILE
echo "Started Gunicorn 🚀"