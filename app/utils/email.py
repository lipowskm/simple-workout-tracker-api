import logging
from pathlib import Path
from smtplib import SMTPException
from typing import Union

import emails
from emails.backend.response import SMTPResponse
from emails.template import JinjaTemplate

from app.core import config

password_reset_jwt_subject = "preset"


def send_email(email_to: str, subject_template="", html_template="", environment=None) -> Union[SMTPResponse, bool]:
    if environment is None:
        environment = {}
    assert config.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(config.EMAILS_FROM_NAME, config.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": config.SMTP_HOST, "port": config.SMTP_PORT}
    if config.SMTP_TLS:
        smtp_options["tls"] = True
    if config.SMTP_USER:
        smtp_options["user"] = config.SMTP_USER
    if config.SMTP_PASSWORD:
        smtp_options["password"] = config.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    try:
        response = message.send(to=email_to, render=environment, smtp=smtp_options)
        assert response.status_code == 250
        logging.info(f"Send email result: {response}")
    except AssertionError:
        logging.error(f"Failed to send email, send email result: {response}")
        return False
    except SMTPException as error:
        logging.error(f"Error while trying to send email: {error}")
        return False
    return response


def send_test_email(email: str):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    return send_email(
        email_to=email,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": config.PROJECT_NAME, "email": email},
    )


def send_reset_password_email(email: str, username: str, first_name: str, token: str):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {username}"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    server_host = config.SERVER_HOST
    link = f"{server_host}/reset-password?token={use_token}"
    return send_email(
        email_to=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": config.PROJECT_NAME,
            "username": username,
            "first_name": first_name,
            "valid_minutes": config.EMAIL_RESET_TOKEN_EXPIRE_MINUTES,
            "link": link,
        },
    )


def send_verify_account_email(email: str, username: str, first_name: str, token: str):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Verify account for user {username}"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "verify_account.html") as f:
        template_str = f.read()
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    server_host = config.SERVER_HOST
    link = f"{server_host}/verify-account?token={use_token}"
    return send_email(
        email_to=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": config.PROJECT_NAME,
            "username": username,
            "first_name": first_name,
            "link": link,
            "valid_minutes": config.EMAIL_NEW_ACCOUNT_TOKEN_EXPIRE_MINUTES
        }
    )


def send_new_account_email(email: str, username: str, first_name: str):
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Account {username} created successfully"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = config.SERVER_HOST
    return send_email(
        email_to=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": config.PROJECT_NAME,
            "username": username,
            "first_name": first_name,
            "link": link,
        }
    )
