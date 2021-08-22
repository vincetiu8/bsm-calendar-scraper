# BSM Calendar Scraper
This is a handy tool to automatically transfer your subjects from iSAMS to your
google calendar. The process only needs you to sign in to both your school 
gmail account and iSAMS.

If you need help with anything or something's not working, feel free to reach out to me!

### Pre-built Binaries
A pre-built binary is available for Linux in the releases page.
If you want to contribute and build the binary for other targets, please reach out to me!

### Instructions
1. Install [python 3.6+](https://www.python.org/downloads/)
2. Install requirements: `pip install -r requirements.txt`
3. Download an appropriate version of [chromedriver](https://chromedriver.chromium.org/downloads)
    and save it as `chromedriver` in this folder.
    This comes with chromedriver for chrome 92, skip this step if you have that version of chrome
4. Run `python main.py` and login when prompted
5. The events automatically appear as a different calendar in google!