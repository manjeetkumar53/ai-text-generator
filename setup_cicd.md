### README for Setting Up CI/CD with deploy.yaml

This guide provides instructions on how to set up a CI/CD pipeline using GitHub Actions to deploy your application to an EC2 instance. The pipeline includes running tests before deploying.

#### Prerequisites

1. **AWS EC2 Instance**: Ensure you have an EC2 instance running with SSH access.
2. **GitHub Repository**: Your project should be in a GitHub repository.
3. **Secrets Configuration**: Set up the necessary secrets in your GitHub repository.

#### Setting Up GitHub Secrets

You need to configure the following secrets in your GitHub repository:

1. `EC2_SSH_KEY`: The SSH private key for accessing your EC2 instance.
2. `EC2_HOST`: The public IP address or hostname of your EC2 instance.
3. `EC2_USERNAME`: The username for SSH access to your EC2 instance (e.g., `ubuntu`).
4. `ENV`: The environment variable for your application (optional).
5. `OPENAI_API_KEY`: The OpenAI API key for your application (replace with your actual secret).

To set up secrets, go to your GitHub repository, navigate to `Settings` > `Secrets and variables` > `Actions`, and add the above secrets.

#### Creating the deploy.yaml File

Create a `.github/workflows/deploy.yaml` file in your repository with the following content:

```yaml
name: Deploy to EC2

on:
  push:
    branches: ["main"] # This triggers the workflow on push to the main branch

jobs:
  test: # New job for running tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2 # Checkout code
      - name: Install dependencies
        run: |
          python -m pip install -r requirements.txt  # Replace with your command to install dependencies
      - name: Run tests with pytest
        run: |
          python -m pytest tests  # Replace 'tests' with your test directory path

  deploy: # Deployment job
    runs-on: ubuntu-latest
    needs: test # This job needs the 'test' job to succeed before running
    steps:
      - name: Checkout current branch ✅
        uses: actions/checkout@v2

      - name: Set up SSH key and whitelist EC2 IP address 🐻‍❄️
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.EC2_SSH_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan ${{ secrets.EC2_HOST }} >> ~/.ssh/known_hosts

      - name: Create .env file dynamically 🧨
        env:
          ENV: ${{ secrets.ENV }}
          EC2_USERNAME: ${{ secrets.EC2_USERNAME }}
          OPENAI_API_KEY: ${{ secrets.EC2_API_KEY }} # Replace with your secrets
        run: |
          echo "ENV=${ENV}" >> env
          echo "EC2_USERNAME=${EC2_USERNAME}" >> env
          echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> env

      - name: Copy files to remote server 🚙
        env:
          EC2_HOST: ${{ secrets.EC2_HOST }}
          EC2_USERNAME: ${{ secrets.EC2_USERNAME }}
        run: |
          scp -r * $EC2_USERNAME@$EC2_HOST:/home/ubuntu/

      - name: Run Bash Script To Deploy App 🚀
        env:
          EC2_HOST: ${{ secrets.EC2_HOST }}
          EC2_USERNAME: ${{ secrets.EC2_USERNAME }}
        run: |
          ssh -o StrictHostKeyChecking=no $EC2_USERNAME@$EC2_HOST "chmod +x ./deploy.sh && ./deploy.sh"

      - name: Clean up SSH key (Optional, consider more secure key management) 🚀
        if: always()
        run: rm -f ~/.ssh/id_rsa
```

#### Running Tests Locally

To run your `unittest` tests locally, use the following script:

1. **Create a shell script to run tests locally**

Create a file named `run_tests.sh` in the root of your project:

```sh
#!/bin/bash

echo "Running unittest tests..."
python -m unittest discover tests

if [ $? -ne 0 ]; then
  echo "Unittest tests failed. Please fix the errors before committing."
  exit 1
fi

echo "Running pytest tests..."
python -m pytest tests

if [ $? -ne 0 ]; then
  echo "Pytest tests failed. Please fix the errors before committing."
  exit 1
fi

echo "All tests passed!"
```

2. **Make the script executable**

Run the following command to make your script executable:

```sh
chmod +x run_tests.sh
```

3. **Add a pre-commit hook to run tests**

You can use Git hooks to automatically run your tests before committing. Create a file named `pre-commit` in your `.git/hooks` directory:

```sh
#!/bin/bash
./run_tests.sh
```

Make the pre-commit hook executable:

```sh
chmod +x .git/hooks/pre-commit
```

Now, every time you attempt to commit changes, the `run_tests.sh` script will run, ensuring your `unittest` and `pytest` tests are executed locally before the commit is finalized.

#### Notes

- Ensure your `deploy.sh` script is executable and correctly set up to handle the deployment process on your EC2 instance.
- Review and customize the workflow and scripts according to your project's specific requirements.
