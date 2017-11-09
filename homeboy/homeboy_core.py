import os
import logging
from homeboy.jenkins_query import JenkinsQuery
from homeboy.homeboy_effects import HomeboyEffects
from apscheduler.schedulers.blocking import BlockingScheduler


class HomeboyCore():
    def __init__(self):
        self.jenkins_query = JenkinsQuery()
        self.homeboy_effects = HomeboyEffects()
        self.jenkins_jobs = {'win': 'cbda_end_to_end_windows',
                             'win_dev': 'cbda_end_to_end_windows_dev',
                             'mac': 'cbda_end_to_end_mac',
                             'mac_dev': 'cbda_end_to_end_mac_dev'}
        self.display_job = os.environ.get("DISPLAY_JOB")
        self.interval = os.environ.get("INTERVAL")
        self.build_data = {}

        self.scheduler = BlockingScheduler()
        self.query_jenkins_job = self.scheduler.add_job(self.update_display, 'interval', seconds=self.interval)
        self.scheduler.start()

    def update_display(self):
        self.get_latest_from_jenkins()
        self.display_effect()

    def get_latest_from_jenkins(self):
        logging.info('Querying Jenkins for latest')
        if self.display_job.lower() == 'all':
            for key,val in self.jenkins_jobs.items():
                self.build_data[key] = self.jenkins_query.get_latest_test_results(val)
        elif self.display_job.lower() == 'nightly':
            for key,val in self.jenkins_jobs.items():
                if 'dev' not in key:
                    self.build_data[key] = self.jenkins_query.get_latest_test_results(val)
        elif self.display_job.lower() == 'dev':
            for key,val in self.jenkins_jobs.items():
                if 'dev' in key:
                    self.build_data[key] = self.jenkins_query.get_latest_test_results(val)
        else:
            for key,val in self.jenkins_jobs.items():
                if self.display_job.lower() in key:
                    self.build_data[key] = self.jenkins_query.get_latest_test_results(val)

    def display_effect(self):
        logging.info("Updating effect")
        for key, val in self.build_data.items():
            if 'mac' in key:
                self.homeboy_effects.display_os = 'mac'
            else:
                self.homeboy_effects.display_os = 'win'

            self.homeboy_effects.show_result_effect(val)


if __name__ == "__main__":
    core = HomeboyCore()