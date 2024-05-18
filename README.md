# ai-text-generator

AI project to Generate output based on user input using any LLM

This guide covers setting up the development environment, running the application, and deploying it using the provided CI/CD pipeline with GitHub Actions and AWS EC2.

````markdown
# Python Web Application

This is a Python web application. This guide will help you set up the development environment, run the application locally, and deploy it using GitHub Actions to an AWS EC2 instance.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- Git
- AWS account and access to create EC2 instances
- GitHub account

## Local Development Setup

1.  **Clone the Repository**

    ```sh
    git clone https://github.com/manjeetkumar53/ai-text-generator.git
    cd ai-text-generator
    ```

2.  **Create and Activate Virtual Environment**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Application**

    ```sh
    cd src
    python app.py # Or the entry point of your application

    ```

        Your application should now be running locally at `http://127.0.0.1:5000` (or the port specified in your app).

    ```

    ```

## Running Tests

If you have tests configured (e.g., using `pytest`), you can run them with:

```sh
pytest
```
````

## Running test using python unittest

# Run complete test: This will initiate the discovery process, locate all your test cases, and run them sequentially. You'll see the results displayed in the terminal, indicating which tests passed and if any failed.

    ```sh
    python -m unittest discover
    ```

# Run test for individual file

    ```sh
    python -m unittest test_dbhandler_mysql.py
    ```

## Deployment to AWS EC2

### 1. Set Up AWS EC2 Instance

- Launch an EC2 instance using the AWS Management Console.
- Choose an Amazon Linux 2 AMI.
- Create a new key pair or use an existing one for SSH access.
- Ensure the security group allows SSH (port 22) and HTTP/HTTPS (ports 80/443).

### 2. Configure GitHub Repository

- Push your code to a GitHub repository.

### 3. Set Up GitHub Actions

1. **Create GitHub Actions Workflow**

   In your GitHub repository, create a file at `.github/workflows/deploy.yml` with the following content:

   ```yaml
   name: CI/CD Pipeline

   on:
     push:
       branches:
         - main

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout code
           uses: actions/checkout@v2

         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: "3.8"

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt

         - name: Run tests
           run: |
             # Run your tests here, e.g.:
             # pytest

     deploy:
       needs: build
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main'

       steps:
         - name: Checkout code
           uses: actions/checkout@v2

         - name: Set up SSH
           uses: webfactory/ssh-agent@v0.5.3
           with:
             ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

         - name: Copy files to EC2
           run: |
             scp -o StrictHostKeyChecking=no -r * ec2-user@YOUR_EC2_PUBLIC_IP:/home/ec2-user/app

         - name: SSH and deploy
           run: |
             ssh -o StrictHostKeyChecking=no ec2-user@YOUR_EC2_PUBLIC_IP << 'EOF'
               cd /home/ec2-user/app
               # If using Docker
               # docker-compose down
               # docker-compose up -d --build
               # Otherwise, run your deployment commands, e.g.:
               # pip install -r requirements.txt
               # gunicorn --bind 0.0.0.0:80 app:app
             EOF
   ```

2. **Set Up GitHub Secrets**

   - Go to your GitHub repository settings.
   - Navigate to `Secrets` > `Actions`.
   - Add a new secret called `SSH_PRIVATE_KEY` and paste the contents of your EC2 instance's private key.

### 4. Update EC2 Instance (for docker only)

SSH into your EC2 instance and prepare it for the application:

```sh
sudo yum update -y
sudo yum install -y python3-pip
sudo pip3 install virtualenv
# If using Docker
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```

### 5. Deploy Application

- Commit and push your changes to the `main` branch of your GitHub repository.
- This triggers the GitHub Actions workflow, which builds the application, runs tests, and deploys it to your EC2 instance.

Your application should now be accessible via the public IP or DNS of your EC2 instance.

## Troubleshooting

- Ensure your EC2 instance's security group allows inbound traffic on the required ports.
- Check the GitHub Actions logs for any errors during the build or deployment process.
- Verify that the correct environment variables and secrets are set in GitHub.

## License

This project is licensed under the MIT License.

```

This README provides a comprehensive guide to set up and run the Python web application locally and deploy it to an AWS EC2 instance using GitHub Actions. Adjust the instructions as necessary to fit your specific application and environment.

```
