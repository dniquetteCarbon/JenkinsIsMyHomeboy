import jenkins
import logging
import os


class JenkinsQuery():
    def __init__(self):
        self.user = os.environ.get('JENKINS_USERNAME')
        self.password = os.environ.get('JENKINS_PASSWORD')
        self.jenkins_url = os.environ.get('JENKINS_URL')
        if not self.jenkins_url:
            self.jenkins_url = 'https://jenkins-qa.cbenglab.com'

        self.jenkins_server = jenkins.Jenkins(self.jenkins_url, username=self.user, password=self.password)

    def get_latest_build(self, job_name):
        last_build_number = self.jenkins_server.get_job_info(job_name)['lastCompletedBuild']['number']
        logging.info("%s Latest Build: %s", job_name, last_build_number)

        build_info = self.jenkins_server.get_build_info(job_name, last_build_number)
        return build_info

    def get_latest_test_results(self, job_name):
        latest_build_info = self.get_latest_build(job_name)
        logging.info(latest_build_info)

        test_results = {'result': latest_build_info['result'].lower()}

        if test_results['result'] == 'unstable' or test_results['result'] == 'success':
            for action in latest_build_info['actions']:
                if action:
                    if action['_class'].lower() == 'hudson.tasks.junit.testresultaction':
                        test_results['total'] = action['totalCount']
                        test_results['fail'] = action['failCount']
                        test_results['skip'] = action['skipCount']
                        test_results['success'] = test_results['total'] - (test_results['fail'] + test_results['skip'])
                        return test_results

        return test_results


if __name__ == "__main__":
    jenkins_query = JenkinsQuery()
    jenkins_query.get_latest_test_results('cbda_end_to_end_windows')