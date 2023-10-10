Apologies for the confusion. Here is the revised `README.md` in markdown format:

---

# Policy Push Script Documentation

This script automates the process of pushing policies to multiple targets using Check Point's Management API. It concurrently processes up to 5 policy pushes at a time, with a delay of 2 seconds between each push. The script generates an HTML report of the push results and sends it via email.

## Dependencies

Install the necessary libraries in your virtual environment:

```bash
pip install cp-mgmt-api-sdk python-dotenv Jinja2 smtplib
```

## Configuration Files

1. **`config.json`**:
   - Holds configuration for the Check Point Management server, logging, and email settings.

```json
{
    "checkpoint": {
        "server_address": "your-server-address",
        "exception_list": ["Exception1", "Exception2"]
    },
    "logging": {
        "log_dir": "./logs",
        "log_level": "INFO"
    },
    "email": {
        "sender_address": "your-email@example.com",
        "receiver_address": "recipient@example.com",
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "smtp_username": "your-email@example.com",
        "smtp_password": "your-email-password"
    }
}
```

2. **`.env`**:
   - Stores the API token for authentication.

```plaintext
API_TOKEN=your-api-token
```

## HTML Report Template

Create a directory named `templates` and within it, create a file named `report_template.html` with the necessary HTML content for the report.

## Python Script (`main.py`)

The `main.py` script is the core of this project. It communicates with the Check Point Management server using the Check Point Management API, pushing policies to multiple targets. Here are the main sections of the script:

### Importing Necessary Libraries

The script begins by importing the necessary libraries such as `json`, `logging`, `os`, `dotenv`, `jinja2`, `smtplib`, `APIClient` from `cp_mgmt_api_sdk_py`, and others required for the script to function properly.

### Loading Configuration and Setting Up Logging

The script loads configurations from a `config.json` file and a `.env` file for the API token. It also sets up logging to capture important events and errors.

### Define `push_policy` Function

This function handles the individual policy push operations. It takes the `APIClient` instance, policy name, and target name as arguments, and sends a request to the Check Point Management server to push the specified policy to the specified target. It returns a dictionary containing the result of the operation.

### Define `create_html_report` Function

This function generates an HTML report based on the results of the policy push operations. It uses the Jinja2 library to render an HTML template with the provided data.

### Define `send_email` Function

This function handles sending the HTML report via email. It sets up an SMTP connection, composes an email with the HTML report as the body, and sends the email.

### Define `main` Function

The `main` function orchestrates the entire process. It performs the following steps:

1. Creates an `APIClient` instance.
2. Authenticates to the Check Point Management server.
3. Retrieves the list of policies.
4. Initiates concurrent policy push operations using a `ThreadPoolExecutor`. The script is configured to perform a maximum of 5 concurrent policy pushes to prevent overwhelming the server, with a delay of 2 seconds between each push. This is achieved by setting the `max_workers` parameter of `ThreadPoolExecutor` to 5.
5. Collects the results of the policy push operations.
6. Generates an HTML report based on the results.
7. Sends the report via email.
8. Logs out of the Check Point Management server.

Here's the relevant code snippet from the `main.py` script that configures the concurrency:

```python
with ThreadPoolExecutor(max_workers=5) as executor:
    for policy_package in show_policy_res.data['packages']:
        policy_name = policy_package['name']
        if policy_name not in exception_list:
            for target in policy_package['targets']:
                target_name = target['name']
                future = executor.submit(push_policy, client, policy_name, target_name)
                policy_push_futures.append(future)
```

In this code snippet, `ThreadPoolExecutor` is utilized with `max_workers` set to 5, which limits the script to a maximum of 5 concurrent policy push operations.

### Script Execution

The script execution begins from the standard `if __name__ == '__main__':` block which calls the `main` function.

### Error Handling

Throughout the script, appropriate error handling is included to catch and log errors, ensuring that the script can fail gracefully in case of unexpected issues.

## Makefile

A `Makefile` is provided to automate the setup of a virtual environment, installation of dependencies, and running the script.

```make
# Makefile

VENV_NAME?= .venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

# Targets

all: venv

venv: $(VENV_NAME)/bin/activate  # Create virtual environment
$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

run:  # Run the script
	${VENV_ACTIVATE} && ${PYTHON} main.py

clean:  # Clean up the virtual environment
	rm -rf $(VENV_NAME)

.PHONY: all venv run clean
```

## Usage

1. Ensure that all configuration files are properly set up and placed in the correct directories.
2. Run `make` in the terminal to set up the virtual environment in the `.venv` directory and install dependencies.
3. Run `make run` to execute your `main.py` script.
4. (Optional) Run `make clean` to delete the virtual environment and clean up the project directory.

## .gitignore

Create a `.gitignore` file to exclude unnecessary files from your git repository:

```gitignore
# Python
*.pyc
*.pyo
*.pyd
__pycache__/

# Virtual Environment
.venv/

# Logs
logs/

# HTML report
report.html

# Miscellaneous
*.swp
.DS_Store
```

--- 

This should preserve the markdown formatting when copied.