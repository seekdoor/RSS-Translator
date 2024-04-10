from crontab import CronTab
from typing import Set, Tuple
# https://gitlab.com/doctormo/python-crontab/

class CrontabManager:
    def __init__(self):
        self.cron = CronTab(user='rsstranslator')
        
    def add_job(self, command, minute, comment='rsstranslator'):
        job = self.cron.new(command=command)
        job.minute.every(minute)
        job.set_comment(comment)
        self.cron.write()

    def remove_jobs(self, comment):
        self.cron.remove_all(comment=comment)
        self.cron.write()

    def dedupe_cron_jobs(self) -> CronTab:
        # Thanks to https://github.com/ArchiveBox/ArchiveBox/blob/1d49bee90bcf6a0b04905266f3e7e73306ed6f9c/archivebox/system.py#L170
        # Dedupe cron jobs by schedule and command
        deduped: Set[Tuple[str, str]] = set()

        for job in list(self.cron):
            unique_tuple = (str(job.slices), job.command)
            if unique_tuple not in deduped:
                deduped.add(unique_tuple)
            self.cron.remove(job)

        for schedule, command in deduped:
            job = self.cron.new(command=command, comment='rsstranslator')
            job.setall(schedule)
            job.enable()

        return self.cron

    # remove not in t_feed db jobs
    def clean_cron_jobs(self, feed_ids: Set[str]):
        for job in list(self.cron):
            if job.comment not in feed_ids:
                self.cron.remove(job)
        self.cron.write()
    