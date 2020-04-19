import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from libs.backgroundModeSkeleton import SMWinservice
from libs.dbController import DBController
from libs.fileMeta import FileMetaData
from libs.fileScraper import FileScraper
from libs.logger import Logger

logger = Logger(__name__, level=logging.INFO).logger


def download_job():
    """
        The job downloads file by checking file metadata in database. If file
        has been updated, downloading. If not, don't download it
    """

    metadata = FileMetaData()
    scraper = FileScraper()
    db_controller = DBController()

    try:
        metadata.file_url, metadata.date = scraper.get_file_metadata()
    except Exception as err:
        logger.error(f"Could not get file metadata: {err}")

    if db_controller.check_file_update(metadata):
        try:
            scraper.download_file(metadata)
            logger.info(
                f"Download file from {metadata.file_url} on {metadata.date}")
        except Exception as err:
            logger.error(f"Could not download file: {err}")

    db_controller.close_db()


class BackgroundMode(SMWinservice):
    _svc_name_ = "FileDownloader"
    _svc_display_name_ = "File Downloader"
    _svc_description_ = "Download file automatically and periodically"

    def __init__(self, args):
        super().__init__(args)
        self.scheduler = BlockingScheduler()

    def start(self):
        """Set up the scheduler before starting"""

        self.scheduler.add_job(download_job, 'interval',
                               id='download_job', seconds=5)

    def stop(self):
        """Clean up before stopping scheduler"""

        self.scheduler.remove_job('download_job')
        self.scheduler.shutdown()

    def main(self):
        self.scheduler.start()


if __name__ == '__main__':
    BackgroundMode.parse_command_line()
