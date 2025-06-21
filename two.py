import os
import sys
import glob
import shutil
import logging
from datetime import datetime

def convert_odate_formats(odate_str):
    """Convert ODATE (dd-mm-yyyy) into yymmdd, yyyymmdd, ddmmyyyy formats."""
    dt = datetime.strptime(odate_str, "%d-%m-%Y")
    return {
        "yymmdd": dt.strftime("%y%m%d"),
        "yyyymmdd": dt.strftime("%Y%m%d"),
        "ddmmyyyy": dt.strftime("%d%m%Y")
    }

def main(job_name, odate):
    source_folder = r'C:\Python learn 1'
    destination_folder = r'C:\destination path'
    log_folder = r'C:\project log'  # This folder must exist

    # Convert ODATE to multiple date formats
    date_formats = convert_odate_formats(odate)

    # Define file patterns using all date formats
    file_patterns = [
        f"*{date_formats['yymmdd']}*",
        f"*{date_formats['yyyymmdd']}*",
        f"*{date_formats['ddmmyyyy']}*"
    ]

    # Setup logging
    log_filename = os.path.join(log_folder, f"move_log_{job_name}_{date_formats['yyyymmdd']}.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger()

    # Validate required folders
    for folder in [source_folder, destination_folder, log_folder]:
        if not os.path.exists(folder):
            logger.error(f"Folder does not exist: {folder}")
            sys.exit(1)

    logger.info(f"Job: {job_name} - Matching using date formats: {date_formats}")

    # Find all files matching any pattern
    matching_files = []
    for pattern in file_patterns:
        search_path = os.path.join(source_folder, pattern)
        found = glob.glob(search_path)
        matching_files.extend(found)
        logger.info(f"Pattern '{pattern}' matched {len(found)} file(s).")

    if not matching_files:
        logger.info(f"Job: {job_name} - No matching files found. Nothing to move.")
        sys.exit(0)

    # Move the files
    count = 0
    for file_path in matching_files:
        try:
            filename = os.path.basename(file_path)
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(file_path, destination_path)
            count += 1
            logger.info(f"Job: {job_name} - Moved file: {filename}")
        except Exception as e:
            logger.error(f"Job: {job_name} - Failed to move {file_path}: {e}")

    logger.info(f"Job: {job_name} - Total files moved: {count}")
    logger.info(f"Job: {job_name} - Log saved to: {log_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python two.py <job_name> <odate_dd-mm-yyyy>")
        sys.exit(1)

    job_name_arg = sys.argv[1]
    odate_arg = sys.argv[2]
    main(job_name_arg, odate_arg)
