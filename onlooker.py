import sys
import os
import logging
import logging.config
import time
from ftplib import FTP


__author__ = "Christopher Hart"
__email__ = "chart2@cisco.com"
__copyright__ = "Copyright (c) 2019 Cisco Systems. All rights reserved."
__credits__ = ["Christopher Hart",]
__license__ = """
################################################################################
# Copyright (c) 2019 Cisco and/or its affiliates.
# 
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at
# 
#                https://developer.cisco.com/docs/licenses
# 
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.
################################################################################
"""

FTP_IP = os.getenv("FTP_IP")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
FTP_POLL = os.getenv("FTP_POLL", "1")
DEBUG = os.getenv("DEBUG", "False")

def main():
    log.info("[INIT] Initializing program")
    log.info("[FTP] Logging into FTP server...")
    log.debug("[FTP] Logging into %s with username %s and password %s", FTP_IP, FTP_USER, FTP_PASS)
    ftp_conn = FTP(host=FTP_IP, user=FTP_USER, passwd=FTP_PASS)
    log.info("[FTP] Login successful!")
    log.info("[FILES] Getting existing set of files on FTP server...")
    existing_fileset = get_fileset(ftp_conn)
    log.info("[FILES] Retrieved set of %s files from FTP server", len(existing_fileset))
    while True:
        for new_file in monitor_for_changes(ftp_conn, existing_fileset):
            log.info("[NEW] New file %s detected!", new_file)
            copy_file(ftp_conn, new_file)
            existing_fileset.add(new_file)
        log.debug("[NEW] Sleeping for %s minutes", FTP_POLL)
        time.sleep(int(FTP_POLL) * 60)

def copy_file(conn, new_file):
    filepath = "/storage/{}".format(new_file[1::])
    log.debug("[DNLD] Downloading new file to %s", filepath)
    with open(filepath, "wb") as infile:
        log.info("[DNLD] Downloading file...")
        conn.retrbinary("RETR {}".format(new_file), infile.write, 1024)
        log.info("[DNLD] Download complete!")

def get_fileset(conn):
    return set(conn.nlst("./"))

def monitor_for_changes(conn, ex_files):
    current_files = get_fileset(conn)
    log.debug("[NEW] Found %s files during this poll", len(current_files))
    new_files = current_files - ex_files
    if new_files:
        log.debug("[NEW] Total of %s new files in this poll", len(current_files))
        return new_files
    else:
        if len(current_files) < len(ex_files):
            log.debug("[NEW] Files were deleted on remote server - old number of files %s, new number %s", len(ex_files), len(current_files))
            ex_files = current_files
        log.debug("[NEW] No new files found this poll")
        return []

def configure_logging(debug_enabled, logfile="{}.log".format(__name__)):
    """Configures logging based upon user-defined paramaters.

    Args:
        debug_enabled: Boolean that determines whether stdout and logfile
            should contain debug-level logs.
        logfile: Filename for persistent logfile.

    Returns:
        Logger object that is used by module for logging.
    """
    default_cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)-15s %(levelname)-8s [%(funcName)20s] %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "logfile": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logfile,
                "maxBytes": 10000000,
            }
        },
        "loggers": {
            __name__: {
                "handlers": ["console", "logfile"],
                "level": "INFO",
                "propagate": False
            },
        }
    }
    if debug_enabled:
        default_cfg["loggers"][__name__]["level"] = "DEBUG"
    logging.config.dictConfig(default_cfg)
    return logging.getLogger(__name__)

log = configure_logging(DEBUG)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()