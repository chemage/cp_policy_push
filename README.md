# Checkpoint Policy Push by ChatGPT

https://chat.openai.com/share/a4cc9ad0-aabe-4abe-ac0e-cba2cf9929f8


## Policy Push Script Documentation

This script automates the process of pushing policies to multiple targets using Check Point's Management API. It concurrently processes up to 5 policy pushes at a time, with a delay of 2 seconds between each push. The script generates an HTML report of the push results and sends it via email.

### Dependencies

Install the necessary libraries in your virtual environment:

```bash
pip install cp-mgmt-api-sdk python-dotenv Jinja2 smtplib
```

### Configuration Files

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

### HTML Report Template

Create a directory named `templates` and within it, create a file named `report_template.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .success { color: green; }
        .failure { color: red; }
    </style>
    <title>Policy Push Report</title>
</head>
<body>
<table>
    <tr>
        <th>Policy Name</th>
        <th>Target Name</th>
        <th>Push Successful</th>
        <th>Error Message</th>
    </tr>
    {% for result in data.policy_push_results %}
    <tr class="{{ 'success' if result.success else 'failure' }}">
        <td>{{ result.policy_name }}</td>
        <td>{{ result.target_name }}</td>
        <td>{{ result.success }}</td>
        <td>{{ result.error_message }}</td>
    </tr>
    {% endfor %}
</table>
</body>
</html>
```

### Python Script (`main.py`)

The main script consists of multiple functions to handle logging, policy pushing, report generation, and email sending. The `main()` function orchestrates these tasks.

```python
import json
import logging
import os
from cp_mgmt_api_sdk_py import APIClient
import dotenv
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from concurrent.futures import ThreadPoolExecutor

# ... rest of your script

if __name__ == '__main__':
    main()
```

#### Key Functions

- **`push_policy(client, policy_name, target_name)`**:
  - Handles pushing a policy to a specified target, with a 2-second delay.
- **`create_html_report(data)`**:
  - Generates an HTML report using the Jinja2 template.
- **`send_email(html_file_path)`**:
  - Sends the HTML report via email.

#### Main Function

The `main()` function performs the following steps:

1. Loads environment variables and configuration from files.
2. Sets up logging.
3. Initializes the Check Point API client and logs in using the API token.
4. Retrieves the list of policy packages.
5. Creates a thread pool to process policy pushes concurrently.
6. Collects the results of each policy push.
7. Generates an HTML report of the push results.
8. Sends the HTML report via email.
9. Logs out of the Check Point API.

### Running the Script

1. Ensure that all configuration files are properly set up and placed in the correct directories.
2. Run the `main.py` script:

```bash
python main.py
```

The script will process the policy pushes, generate the report, and send it via email.

--- 

This Markdown documentation provides a detailed overview of your script and its setup. It should help anyone understand how to use and modify the script as needed.