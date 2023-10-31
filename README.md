# Google Map Scraping
Extract Information of companies according to filters—Industry, Location, Job title.
(LinkedIn Profile of each company, director's contact info – Name, LinkedIn Profile, Email Address, Phone Number)

## Installation
### Python Environment (version 3.11.5)
- Download Python Installer from [here](https://www.python.org/downloads/release/python-3115/) and install on OS.
- Download Source from [Github repository](https://github.com/Stormy0611/py-flask-mvc-scraping).
- Install Python Virtual Environment in the root directory of the Project and Activate.
```cli
python -m venv venv
```
Windows:
```cli
.\venv\Scripts\activate
```
### Install Necessary Python Packages
```cli
pip install -r requirements.txt
```
### Set Up Environment (.env)
Following .env-example file.
| Key | Value |
|--|--|
|PROFILE_NUM|Integer Number|
|LIMIT|Integer Number|
- PROFILE_NUM
Check your Google Chrome account that you have logged in Google and [Lusha.com](https://www.lusha.com/) and input the correct number.
Ex. In Windows, C:\Users\Storm\AppData\Local\Google\Chrome\User Data\Profile x
- LIMIT
Represent the number of result data that will be extracted at once.
If it is omitted, there is no limitation in the number of results that will be extracted.

## Run
```cli
python server.py
```
If the server is running successfully, you will be able to see the opened browser.
After that, you can open another new tab, and access <http://localhost:8000> to start scraping.