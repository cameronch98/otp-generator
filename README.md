# One Time Password Generator

An application to generate QR codes for use in Google Authenticator and display the associated one time passwords for that secret key in the terminal. The one time passwords are timed one time passwords (TOTPs) on a 30 second timer. For any given user/email, the one time passwords displayed in the terminal can be compared to those displayed in the Google Authenticator app after scanning the QR code. They should be the same since they are using the same base32 secret key! For the same reason, the generate-qr and get-otp commands can be run in any order for a particular user. The application utilizes the qrcode and pyotp packages to generate the QR codes and display one time passwords. Multiple user support is included, although it isn't intended to be secure as secrets are listed in a readable JSON file. Typer was used to implement the CLI.

# Setup

### MacOS/Linux

First, clone the repository or download/extract the files. Then, it is recommended to go to the project directory and create a virtual environment as follows: 

```
python<version> -m venv <name-for-venv>
```

Then, we need to activate the venv by running:

```
source <name-for-venv>/bin/activate
```

Now that the virtual environment is enabled in the terminal, we need to install the packages required by the program that reside in requirements.txt. To do so, we can run the following command:

```
pip install -r requirements.txt
```

# Usage

### General Info

To get general info about the options and commands available, we can run the program with no arguments:

```
python otp.py
```
```
python3 otp.py
```
```
<name-for-venv>/bin/python otp.py
```

NOTE: we've shown three different ways to call the program here. From here on out, we will use python3 to demonstrate the program.

### Generate QR Code

To generate a QR code for an example email/user, we can use one of the following commands:

```
python3 otp.py generate-qr
```

To generate a QR code for a specific email/user, we can use one of the following commands:

```
python3 otp.py generate-qr <email>
```

### Retrieve One-Time Password

To retrieve a one time password for the example email/user, we can use one of the following commands:

```
python3 otp.py get-otp
```

To retrieve a one time password for a specific email/user, we can use one of the following commands:

```
python3 otp.py get-otp <email>
```

To repeat the display of one time passwords every 30 seconds until the user quits, add the --repeat option:

```
python3 otp.py get-otp <email> --repeat
```

### Help

To get help for any command or the program in general, use the --help option:

```
python3 otp.py --help
```
```
python3 otp.py generate-qr --help
```
```
python3 otp.py get-otp --help
```
