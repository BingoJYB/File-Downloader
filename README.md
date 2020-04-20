# File-Downloader

## Introduction

This is a file downloader which can download a file called **_Monthly business figures (historic)_** on the website [Deutsche Börse Group - Statistics - Deutsche Börse AG](https://www.deutsche-boerse.com/dbg-en/investor-relations/statistics) automatically and periodically.

The script should run on Windows as a Windows Service. It uses `cron` and runs at 10 o'clock every morning to check the update of file on the website. File metadata will be saved in a database and a hash value calculated based on the downloading link of the file is also saved. This hash is used for checking whether a file has been updated or not. Only when a file is updated, a new file will be downloaded. Each file will be downloaded only once.

## Setup

**_config.csv_** -- user can add custom directory path of downloading file. If this file is not provided, the downloading file will be stored in a default folder called **_download_files_**.

**_install.bat_** -- install as Windows Service with the service name _File Downloader_. Then start the service with startup type _auto_.

**_uninstall.bat_** -- stop and remove the Windows Service _File Downloader_.

Both batch files must **run as administrator**.
