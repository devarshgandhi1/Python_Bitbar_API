from testdroid import Testdroid
import json
import sys, getopt, os
import argparse

#python azure_python.py --projectName AzureDemo --os IOS --app calculator.ipa --testApp calculatorUITests-Runner.zip --frameworkId 612 --deviceGroup 39557 --apiKey <>
class RunTest:

    usrname=None
    pwd = None
    config={}
    obj = None
    prj_details = None
    local_config = None
    file_ids = None
    prj_id = None
    test_run = None

    prjName = None
    os = None
    app = None
    testApp = None
    deviceGroup = None
    frameworkId = None

    def __init__(self, argv):
        #self.api_key = argv[1]
        self.api_key = argv.apiKey
        self.prjName = argv.projectName
        self.os = argv.os
        self.app = argv.app
        self.testApp = argv.testApp
        self.deviceGroup = argv.deviceGroup
        self.frameworkId = argv.frameworkId

    def authenticate(self):
        # res = curl -u {x}: https://cloud.bitbar.com/api/me
        # print(res)
        self.obj = Testdroid(apikey=self.api_key)
        self.obj.polling_interval_mins = 1
        #self.obj = Testdroid(username=self.usrname,password=self.pwd)
        #print(self.obj)

    def check_project(self,name):
        prjs = self.obj.get_projects()['data']
        print(prjs)
        for prj in prjs:
            if prj['name'] == name:
                self.prj_details = prj
                return prj['id']
        
        return None

    def check_project_id(self,id):
        prjs = self.obj.get_projects()['data']
        print(prjs)
        for prj in prjs:
            if prj['projectId'] == id:
                self.prj_details = prj
        
        return None

    def run_test(self):
        self.config['files'] = self.file_ids
        self.config['projectId'] = self.prj_id
        files_list = self.file_ids
        file_json = [{"id": f_id} for f_id in files_list]
        self.config['files'] = file_json
        self.config['frameworkId'] = self.frameworkId
        self.config['deviceGroupId'] = self.deviceGroup
        print("After changing the config")
        print(self.config)
        self.test_run = self.obj.start_test_run_using_config(test_run_config=json.dumps(self.config))
        print('***Test Run Created*** - ' + str(self.test_run['id']))
        self.obj.wait_test_run(self.prj_id, self.test_run['id'])
        self.obj.download_test_run(self.prj_id, self.test_run['id'])
        #self.obj.start_wait_test_run(test_run_config=json.dumps(self.config))
        #self.obj.start_wait_download_test_run(test_run_config=json.dumps(self.config))

    def create_project(self):
        prj = self.obj.create_project(self.prjName, self.os)
        self.prj_id = prj['id']
        self.file_ids = self.upload_app_test(prj['id'])
        return prj,self.file_ids
    
    def upload_app_test(self, id):
        apk_id = self.obj.upload_file(self.app)
        test_id = self.obj.upload_file(self.testApp)
        return [apk_id['id'], test_id['id']]

    def get_projects(self, identifier):
        if not identifier:
            print('in if')
            all_prj = self.obj.get_projects()
            return all_prj
        else:
            prj = self.obj.get_project(identifier)
            return prj
    


def main(argv):
    run_inst = RunTest(argv)
    run_inst.authenticate()
    prj_created, file_ids = run_inst.create_project()
    #prj_id = prj_created['id']
    #print(prj_created)
    #198606417
    #prj_id = 198606417
    #prj = run_inst.get_projects(prj_id)
    if prj_created:
        print('***Project Created ****')
        print(prj_created)
        print(file_ids)
    run_inst.run_test()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--projectName')
    parser.add_argument('--os')
    parser.add_argument('--app')
    parser.add_argument('--testApp')
    parser.add_argument('--deviceGroup')
    parser.add_argument('--frameworkId')
    parser.add_argument('--apiKey')
    args = parser.parse_args()
    main(args)