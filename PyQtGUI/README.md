# Multiple Widget Application using PyQt

## What You Need

I recommend using virtualenv to create a virtual environment for the clock.

```bash
pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Use pip to install necessary packages.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 mirror.py
```

## Other Information

This application uses Gmail, Google Calendar, and Twitter API's. It is useful to note: for the google APIs, you need to enable them first and obtain a tocken.pickle file. 
You may also need to update the credentials.json file as well.
The twitter API should work as is using Ali's API key.
