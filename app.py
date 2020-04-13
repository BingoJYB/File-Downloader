from apscheduler.schedulers.blocking import BlockingScheduler

from libs.backgroundModeSkeleton import SMWinservice
from libs.dbController import DBController
from libs.fileMeta import FileMetaData
from libs.fileScraper import FileScraper


class BackgroundMode(SMWinservice):
    _svc_name_ = "FileDownloader"
    _svc_display_name_ = "File Downloader"
    _svc_description_ = "Download file automatically and periodically"

    def job(self):
        metadata = FileMetaData()
        scraper = FileScraper()
        db_controller = DBController()

        url, date = scraper.get_file_metadata()
        metadata.file_url = url
        metadata.date = date

        if db_controller.check_file_update(metadata):
            scraper.download_file(metadata)

        db_controller.close_db()

    def main(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.job, 'interval', seconds=10)
        scheduler.start()


if __name__ == '__main__':
    BackgroundMode.parse_command_line()
