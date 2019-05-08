Intro
=====

This is a project to demostrate the use of Testroid API to interact with [https://cloud.bitbar.com](https://cloud.bitbar.com) to create a project, upload the application and test files, start a test run and collect the logs/results.

Documentation
-------------
[Link to Bitbar API Documentation] (http://docs.bitbar.com/testing/api/index.html)

Pre-Reqs
--------
*   Python and pip

Contents
--------
*   `requirements.txt` -> Listing the package requirements
*   `azure_python.py` -> the program that triggers bitbar cloud to run the tests. This was created for Azure pipelines but works any python environment.

Run
---
*   From the directory of `.py` run
    `python azure_python.py --projectName "$PRJ_NAME" --os "$OS" --app com.companyname.UITestDemo.apk --testApp tests*.zip --frameworkId "$FRAMEWORK" --deviceGroup "$DEVICE_GROUP" --apiKey ${API_KEY}`
    All the parameters are mandatory.
*   Framework, device group id and apiKey can be found in [bitbar cloud](https://cloud.bitbar.com)
*   The results will be downloaded on successful completions in the work_dir.