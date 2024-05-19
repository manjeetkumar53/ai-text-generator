# Run Application suing gunicorn

To run Gunicorn, you need a Unix-based environment.

### Option 1: Use Windows Subsystem for Linux (WSL)

Windows Subsystem for Linux (WSL) allows you to run a Linux distribution on your Windows machine.

1. **Install WSL**:

   - Open PowerShell as Administrator and run:
     ```sh
     wsl --install
     ```
   - Restart your machine if prompted.

2. **Install a Linux Distribution**:

   - After restarting, you can install a Linux distribution from the Microsoft Store (e.g., Ubuntu).

3. **Set up Your Environment in WSL**:

   - Open your WSL terminal and navigate to your project directory.
   - Set up your virtual environment and install dependencies:
     ```sh
     sudo apt-get update
     sudo apt-get install python3-venv python3-pip
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     pip install gunicorn
     ```

4. **Run Gunicorn**:
   ```sh
   gunicorn --bind 127.0.0.1:5000 appserver:gunicorn_app
   ```

### Option 2: Use Docker

Docker allows you to run applications in isolated containers, which can include a Unix-like environment.

1. **Install Docker Desktop**:

   - Download and install Docker Desktop from [Docker's website](https://www.docker.com/products/docker-desktop).

2. **Create a Dockerfile**:
   Create a `Dockerfile` in your project root:

   ```dockerfile
   # Use the official Python image from the Docker Hub
   FROM python:3.12-slim

   # Set the working directory in the container
   WORKDIR /app

   # Copy the current directory contents into the container at /app
   COPY . /app

   # Install any needed packages specified in requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt

   # Expose port 5000 for the application
   EXPOSE 5000

   # Command to run the application
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "appserver:gunicorn_app"]
   ```

3. **Build the Docker Image**:

   ```sh
   docker build -t ai-text-generator .
   ```

4. **Run the Docker Container**:
   ```sh
   docker run -p 5000:5000 ai-text-generator
   ```

### Option 3: Deploy to AWS EC2 (Unix Environment)

If you're deploying to AWS EC2, you will likely be using a Unix-based instance (like Amazon Linux or Ubuntu), where `fcntl` is available.

1. **Connect to Your EC2 Instance**:

   - SSH into your EC2 instance:
     ```sh
     ssh -i /path/to/your-key-pair.pem ec2-user@your-ec2-public-dns
     ```

2. **Set up Your Environment**:

   - Update and install necessary packages:
     ```sh
     sudo apt-get update
     sudo apt-get install python3-venv python3-pip
     ```

3. **Transfer Your Project Files**:

   - Use SCP or another method to transfer your project files to the EC2 instance:
     ```sh
     scp -i /path/to/your-key-pair.pem -r /path/to/your/project ec2-user@your-ec2-public-dns:/home/ec2-user/
     ```

4. **Navigate to Your Project Directory and Set Up**:

   ```sh
   cd /home/ec2-user/your_project_directory
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Run Gunicorn**:
   ```sh
   gunicorn --bind 127.0.0.1:5000 appserver:gunicorn_app
   ```
