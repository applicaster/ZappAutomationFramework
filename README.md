# Zapp automation framework for running UI tests

**Python project for running automation UI tests on the following platforms based on Appium and Selenium:**

1. Android mobile
2. iOS mobile
3. Android TV
4. Apple TV
5. Web
   <br><br>

### Setting up the project

#### Prerequisites

You will need to have a QB app running locally on your machine. This means you will need the [QuickBrick repo](https://github.com/applicaster/QuickBrick), as well as the native builder repositories for [Apple (tvOS / iOS)](https://github.com/applicaster/ZappAppleBuilder) and [Android (mobile, TV, amazon fire)](https://github.com/applicaster/zapp-platform-android).
Check out these repositories to see how to configure and prepare an app locally.

Make sure you have these tools installed:

- Command line tools: git, pip, brew, node and npm
- [Download and install](https://www.python.org/downloads/) python 3.8.x

#### Install Appium CLI tool

you will need appium to run the automated tests. You can install it using npm as described below, or you can install the [Appium client app for Mac OS](https://github.com/appium/appium-desktop/releases/tag/v1.18.3). You will also need the chromium web driver for the samsung tests, and make sure you have a chrome browser available

```bash
npm install -g appium@1.17.1 chromedriver
npm install wd
```

After appium is installed, you will need to restart your terminal.

#### Setup the automation Framework

First, clone this repo and install the repo's dependencies.

```bash
$ git clone git@github.com:applicaster/ZappAutomationFramework.git
$ cd ZappAutomationFramework
$ sudo pip install -r requierments.txt
```

you will then need to set this repo in your python path

```bash
$ export PYTHONPATH=<full path to where project is cloned>/ZappAutomationFramework/
```

You're now set to run the automated tests locally. Follow on reading for precise instructions on how to run tests on a specific platform

### Run tests locally

#### Generate config.cfg settings file

In order for the tests to run, you need to provide a config.cfg file with all the information about the app and the appium settings.
The config.cfg file has the default configuration for all platforms. Depending on which platform you want to run, you can simply leave the section corresponding to the platform you want to run uncommented. If you get an error, check out these [instructions](https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/1048510939/Framework+config.cfg+settings+file) to customise this file

#### prepare your environment

Follow this steps before running the tests:

- make sure you have the flag which disables React Native's yellow box
- make sure you set up the flag which enables accessibility items in the app

```bash
# in ~/.zshrc or ~/.bash_profile
export DISABLE_REACT_YELLOW_BOX=true
export ZAPP_UI_TESTS_ENV=true

# after setting these environment variables in your bash profile
# restart your terminal or run
source ~/.zshrc
# or
source ~/.bash_profile
```

Last but not least, open a new terminal window, and start the appium server by running `appium`. Alternatively, you can start the appium server from the desktop app if you chose to use it over the npm package.

#### Prepare your app

The automated tests are running on the [Feature App](https://zapp.applicaster.com/app_families/623/releases), which is built specifically for this purpose. You can see releases for each of the platforms running automated tests, and the target of the release is the app which is set up to run on Azure.

Select the release for the platform you want to run, and prepare that app on the QuickBrick repo, using the relevant native builder repo for all native platforms. Samsung app don't require to use another repo as the tests are running in a browser environment.

Once your app is set up, start the react-native packager. You are now all set to run the automated tests

#### Run the tests from the CLI

the command to run the test is the following:

```bash
$ pytest applications/feature_app/<flavor>/tests/ -m "<my_test_marker>" -v -s --log-level=CRITICAL
```

Depending on which platform you are running, you will need different values for <flavor> and <my_test_markers>

| platform   | Azure pipeline | flavor value | test marker value         |
| ---------- | -------------- | ------------ | ------------------------- |
| ios        | UI tests check |  mobile      | qb_ios_mobile             |
| ios        | QB nightly run |  mobile      |  qb_ios_mobile_nightly    |
| android    | UI tests check |  mobile      |  qb_android_mobile        |
| android    | QB nightly run |  mobile      | qb_android_mobile_nightly |
| tvos       | UI tests check |  tv          | tvos                      |
| tvos       | QB nightly run | tv           | tv_os_nightly             |
| android TV | UI tests check |  tv          | android_tv                |
| android TV | QB nightly run |  tv          | android_tv_nightly        |
| samsung    | UI tests check |  tv          | samsung_tv                |
| samsung    | QB nightly run |  tv          | samsung_tv_nightly        |

If you want to run one or several specific tests for debug purposes, you can leverage the test markers for that.
in front of the test you want to run (either in `applications/feature_app/tv/tests/*.py` or `applications/feature_app/mobile/tests/*.py`), you can define a custom marker by adding a decorator to the test function

```python

# in applications/feature_app/mobile/tests/*.py

@pytest.mark.do_test
def test_verify_something(self)
```

then you can run `pytest applications/feature_app/mobile/tests/ -m do_test -v -s --log-level=CRITICAL` to simply run this test alone and skip the others. The same marker can be added to multiple test to run a specific subset of tests.

#### How to test changes in Azure ?

Even if tests pass locally, it is good to check on azure that the tests are running properly as expected.
This can be achieved by pushing a new branch to this repo with the modified tests, and trigger a manual run of the pipeline in azure.
You can select to run either the UI tests check, which are running on every PR in the QB repo, or the nightly which runs every night.
First select the branch of the QB repo you want to run. Then select the option to add an environment variable, and create a new environment variable called `custom_branch`, and assign it to the name of the branch from this repo which contains your changes. This will trigger a run of the tests in Azure, and you can confirm that the results are in line with the expectations.

### More

#### Example Test:

[Web view cell test](https://github.com/applicaster/ZappAutomationFramework/blob/master/applications/feature_app/mobile/tests/test_web_view_link.py)
<br><br>

#### More Documentations

[Appium API](https://appium.io/docs/en/about-appium/api/) <br>
[Appium Desired Capabilities](http://appium.io/docs/en/writing-running-appium/caps/) <br>
[Azure UI Tests check for Quick Brick pull requests](https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/904527967/Azure+UI+Tests+check+for+Quick+Brick+pull+requests) <br>
[Instructions for running against real devices (iOS Only)](http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/)  
[Download Appium Desktop App](http://appium.io/)
<br><br>
