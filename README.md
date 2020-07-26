# Zapp automation framework for running UI Tests
Python project for running automation UI tests on the following platforms based on Appium and Selenium:
1. Android mobile
2. iOS mobile
3. Android TV 
4. Apple TV 
5. Web



#### Prerequisites: ####
- python 3.8.3 [Download](https://www.python.org/downloads/)
(Tip: If your local machine has other versions of python installed I would advise to uninstall it and stay with a single version)
- __For iOS Mobile developers only who want to run the tests on real devices:__:<br>http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/
- For mobile testings download and install Appium desktop server version 1.15.1:<br>http://appium.io/
- Command line tools: git, pip, brew, node and npm
- For mobile testings install in advance any Applicaster app with "Appium UI Tests" plugin


#### Installation: ####
`git clone https://github.com/applicaster/ZappAutomationInfrastructure`<br>
`cd ZappAutomationInfrastructure`<br>
`sudo pip install -r requierments.txt`


#### Generate config.cfg settings file: ####
https://github.com/applicaster/ZappAutomationInfrastructure/wiki/Generating-config.cfg<br>

__Example config.cfg files:__
https://github.com/applicaster/ZappAutomationInfrastructure/blob/master/config_files/feature_app.cfg<br>
(choose your correct configuration according to the platform and comment out the rest)

#### Example Test: ####
An example can be found here: __ZappAutomationInfrastructure/tests/feature_app/test_zapp_sanity.py__<br>

In order to run it from command line first define the python path to your project:<br>
`export PYTHONPATH=~/<full path to project>/ZappAutomationInfrastructure/`<br>
For mobile testings start the Appium server before starting the test.
Then run: <br>
`py.test tests/mobile/feature_app/ -m "test_advertising_screen" -v -s --log-level=CRITICAL`

#### Documentations: ####
__Appium API:__ https://appium.io/docs/en/about-appium/api/<br>
__Appium Desired Capabilities:__ http://appium.io/docs/en/writing-running-appium/caps/




