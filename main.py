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

# Load environment variables from .env file
dotenv.load_dotenv()

# Load configuration
with open('config.json') as f:
    config = json.load(f)

checkpoint_config = config['checkpoint']
logging_config = config['logging']
email_config = config['email']

# Set up logging
log_dir = logging_config['log_dir']
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_files = sorted(os.listdir(log_dir))
if len(log_files) >= 4:
    os.remove(os.path.join(log_dir, log_files[0]))

log_filename = os.path.join(log_dir, 'script_log.log')
logging.basicConfig(filename=log_filename, level=logging_config['log_level'], filemode='w')

exception_list = checkpoint_config['exception_list']

def push_policy(client, policy_name, target_name):
    time.sleep(2)  # Adding a delay of 2 seconds between pushes
    install_policy_res = client.api_call(
        'install-policy',
        {'policy-package': policy_name, 'targets': [target_name]}
    )
    result = {
        'policy_name': policy_name,
        'target_name': target_name,
        'success': install_policy_res.success,
        'error_message': install_policy_res.error_message if not install_policy_res.success else None
    }
    return result

def create_html_report(data):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_template.html')
    report_html = template.render(data=data)
    with open('report.html', 'w') as file:
        file.write(report_html)

def send_email(html_file_path):
    sender_address = email_config['sender_address']
    receiver_address = email_config['receiver_address']
    subject = "HTML Report"
    smtp_server = email_config['smtp_server']
    smtp_port = email_config['smtp_port']
    smtp_username = email_config['smtp_username']
    smtp_password = email_config['smtp_password']

    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = subject

    with open(html_file_path, 'r') as file:
        html_report = file.read()
    msg.attach(MIMEText(html_report, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_address, receiver_address, msg.as_string())

def main():
    client = APIClient(checkpoint_config['server_address'])
    api_token = os.getenv('API_TOKEN')
    login_res = client.login_with_token(api_token)
    if not login_res.success:
        logging.error(f'Failed to login: {login_res.error_message}')
        return

    show_policy_res = client.api_call('show-packages', {})
    if not show_policy_res.success:
        logging.error(f'Failed to retrieve policies: {show_policy_res.error_message}')
        client.logout()
        return

    policy_push_futures = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        for policy_package in show_policy_res.data['packages']:
            policy_name = policy_package['name']
            if policy_name not in exception_list:
                for target in policy_package['targets']:
                    target_name = target['name']
                    future = executor.submit(push_policy, client, policy_name, target_name)
                    policy_push_futures.append(future)

    policy_push_results = [future.result() for future in policy_push_futures]

    data = {
        'policy_push_results': policy_push_results,
        # ... other data
    }
    create_html_report(data)
    send_email('report.html')

    client.logout()

if __name__ == '__main__':
    main()
