# Zapp automation framework for running UI tests
Python project for running automation UI tests on the following platforms based on Appium and Selenium:
1. Android mobile
2. iOS mobile
3. Android TV 
4. Apple TV 
5. Web
<br><br>

#### Prerequisites ####
- Command line tools: git, pip, brew, node and npm
- [Download and install](https://www.python.org/downloads/) python 3.8.3
- iOS Only - [Instructions](http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/) for running against real devices 
- [Download and install](http://appium.io/) Appium CLI tool 1.17.1
<br><br>

#### Install ####
`git clone git@github.com:applicaster/ZappAutomationFramework.git` <br>
`cd ZappAutomationFramework` <br>
`sudo pip install -r requierments.txt`
<br><br>

#### Generate config.cfg settings file ####
[Instructions](https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/1048510939/Framework+config.cfg+settings+file)
<br><br>

#### Example Test: ####
[Web view cell test](https://github.com/applicaster/ZappAutomationFramework/blob/master/applications/feature_app/mobile/tests/test_web_view_link.py)
<br><br>

#### Running test from CLI ####
1. Define the python path to your project:<br>
`export PYTHONPATH=<full path to project>/ZappAutomationFramework/`<br>
For mobile testings start the Appium server before starting the test.
2. Start Appium server from other terminal window: `appium`
3. `pytest applications/feature_app/mobile/tests/ -m "<my_test_marker>" -v -s --log-level=CRITICAL`
<br><br>

#### More Documentations ####
[Appium API](https://appium.io/docs/en/about-appium/api/) <br>
[Appium Desired Capabilities](http://appium.io/docs/en/writing-running-appium/caps/) <br>
[Azure UI Tests check for Quick Brick pull requests](https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/904527967/Azure+UI+Tests+check+for+Quick+Brick+pull+requests) <br>
<br><br>
