"""
https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/
https://github.com/google/google-authenticator/wiki/Key-Uri-Format
https://www.regular-expressions.info/email.html
https://typer.tiangolo.com/tutorial/
https://pypi.org/project/qrcode/
https://pypi.org/project/pyotp/
"""

import os
import re
import typer
import pyotp
import json
import time
import qrcode
from typing import Optional
from typing_extensions import Annotated


app = typer.Typer(
    no_args_is_help=True,
    help="Tool to generate QR codes for use in Google Authenticator and display the OTPs created.",
)


@app.command()
def generate_qr(email: Annotated[Optional[str], typer.Argument()] = None):
    """
    Generate QR code for user with EMAIL.

    If email not provided, will default to example@example.com.
    """
    # Default to example email if not provided
    email = "example@example.com" if not email else email

    # Validate email
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        print(f"otp: {email} is not a valid email address")
        return

    # Retrieve or generate secret key for URI creation
    if not (secret := get_secret(email)):
        secret = create_secret(email)

    # Generate URI
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="OTP App")

    # Generate QR code and save
    qr = qrcode.make(uri)
    qr.convert("RGB").save(f"qrcodes/{email}.jpg", "JPEG")
    print(f"otp: image saved at path qrcodes/{email}.jpg")


@app.command()
def get_otp(
    email: Annotated[Optional[str], typer.Argument()] = None,
    repeat: Annotated[
        Optional[bool], typer.Option(help="Continue generating OTPs until user quits.")
    ] = False,
):
    """
    Display OTP for user with EMAIL, optionally with a --repeat.

    If email not provided, will default to example@example.com.
    If --repeat is used, repeat display of OTP every 30 secs.
    """
    # Default to example email if not provided
    email = "example@example.com" if not email else email

    # Validate email
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        print(f"otp: {email} is not a valid email address")
        return

    # Retrieve secret key for user
    if not (secret := get_secret(email)):
        secret = create_secret(email)

    # Display OTPs
    totp = pyotp.TOTP(secret)
    print(f"otp: {totp.now()}")
    while repeat:
        time.sleep(30)
        print(f"otp: {totp.now()}")


def get_secret(email: str):
    """Search for secret key for a user with the given email"""
    # Load user database
    with open("users.json", "r") as f:
        users = json.load(f)

    # Search for user secret
    for user in users:
        if user["email"] == email:
            return user["secret"]


def create_secret(email: str):
    """Creates secret for a user and adds to JSON file"""
    # Create secret and user object
    secret = pyotp.random_base32()
    user = {"email": email, "secret": secret}

    # Add to JSON file
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("users.json", "w") as f:
        users.append(user)
        json.dump(users, f)

    return secret


if __name__ == "__main__":
    # Initialize JSON file if not already done
    if not os.path.exists("./users.json") and not os.path.exists("./qrcodes"):
        os.mkdir("./qrcodes")
        with open("users.json", "w") as f:
            f.write("[]")

    # Make commands available
    app()
