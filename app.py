from apscheduler.schedulers.blocking import BlockingScheduler

from libs.backgroundModeSkeleton import SMWinservice
from libs.dbController import DBController
from libs.fileMeta import FileMetaData
from libs.fileScraper import FileScraper


def download_job():
    metadata = FileMetaData()
    scraper = FileScraper()
    db_controller = DBController()

    metadata.file_url, metadata.date = scraper.get_file_metadata()

    if db_controller.check_file_update(metadata):
        scraper.download_file(metadata)

    db_controller.close_db()


class BackgroundMode(SMWinservice):
    _svc_name_ = "FileDownloader"
    _svc_display_name_ = "File Downloader"
    _svc_description_ = "Download file automatically and periodically"

    def __init__(self, args):
        super().__init__(args)
        self.scheduler = BlockingScheduler()

    def start(self):
        self.scheduler.add_job(download_job, 'interval', id='download_job', seconds=10)

    def stop(self):
        self.scheduler.remove_job('download_job')
        self.scheduler.shutdown()

    def main(self):
        self.scheduler.start()


if __name__ == '__main__':
    BackgroundMode.parse_command_line()
