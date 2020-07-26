# Zapp automation framework for running UI Tests
Python project for running automation UI tests on the following platforms based on Appium and Selenium:
1. Android mobile
2. iOS mobile
3. Android TV 
4. Apple TV 
5. Web

#### Prerequisites: ####
- Command line tools: git, pip, brew, node and npm
- python 3.8.3 [Download](https://www.python.org/downloads/)
(Tip: If your local machine has other versions of python installed I would advise to uninstall it and stay with a single version)
- iOS Mobile testers only who want to run the tests on real devices: [Instructions](http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/)
- Appium CLI tool 1.17.1 [Download](http://appium.io/)

#### Installation: ####
`git clone https://github.com/applicaster/ZappAutomationInfrastructure` <br>
`cd ZappAutomationFramework` <br>
`sudo pip install -r requierments.txt`

#### Generate config.cfg settings file: ####<br>
[Instructions](https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/1048510939/Framework+config.cfg+settings+file)

#### Example Test: ####
[Web view cell test](https://github.com/applicaster/ZappAutomationFramework/blob/master/applications/feature_app/mobile/tests/test_web_view_link.py)

#### Running test from CLI: ####
1. In order to run it from command line first define the python path to your project:<br>
`export PYTHONPATH=<full path to project>/ZappAutomationFramework/`<br>
For mobile testings start the Appium server before starting the test.
2. Start Appium server from other terminal window: `appium`
3. `pytest applications/feature_app/mobile/tests/ -m "<my_test_marker>" -v -s --log-level=CRITICAL`

#### Addional Documentations: ####
[Appium API](https://appium.io/docs/en/about-appium/api/)<br>
[Appium Desired Capabilities](http://appium.io/docs/en/writing-running-appium/caps/)<br>
[Azure UI Tests check for Quick Brick pull requests](https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/904527967/Azure+UI+Tests+check+for+Quick+Brick+pull+requests)<br>






