"""
Script for processing and organizing MEG data into BIDS format.

Authors: Hamideh Sadat Bagherzadeh, Ph.D. and Aqil Izadysadr
Created: 09/09/2023

This script scans directories for MEG data (primarily CTF), anonymizes them,
converts them to BIDS format, and saves additional data like anatomical images
and transformations. It then generates a CSV file mapping subject names to
numbers. It can be adapted for other MEG datasets.

"""

import os
import re
import logging
import shutil
import mne
from mne_bids import BIDSPath, write_raw_bids
import csv

# Parent directory where all the MEG data is stored
SEARCH_DIRECTORY = "/MEG Parent Directory Example"

# Regular expression pattern to match directory names (adjust the pattern as needed)
PATTERN = r".*_example-REST_.*\_01.ds$"

# Output directory for BIDS dataset
BIDS_ROOT_DIR = '/MEG Output Example/BIDS'

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    filename='bids.log'
)

def find_meg_directories(search_directory: str, pattern: str):
    """
    Find all sub-directories matching the given pattern in the specified parent directory.

    Args:
        search_directory (str): Directory to search in.
        pattern (str): Regular expression pattern to match directories.

    Returns:
        list: List of directories matching the pattern.
    """
    meg_dirs = []
    for root, dirs, files in os.walk(search_directory):
        for directory in dirs:
            if re.match(pattern, directory):
                meg_dirs.append(os.path.join(root, directory))
    return meg_dirs

def get_subject_data(meg_dirs: list):
    """
    Get subject data by extracting sub-directory names and mapping to the
    corresponding data.

    Args:
        meg_dirs (list): List of MEG directories.

    Returns:
        dict: Mapping of subjects to their data paths.
    """
    sub_dirs = []
    sub_names = []
    for meg in meg_dirs:
        sub_dir = os.path.dirname(meg)
        sub_dirs.append(sub_dir)
        sub_name = os.path.basename(sub_dir)
        sub_names.append(sub_name)

    sub_names = sorted(list(set(sub_names)))

    sub_data = {}
    for sub in sub_names:
        for m in meg_dirs: 
            meg = os.path.basename(m)
            if sub in meg:
                sub_data[sub] = m
    return sub_data, sub_names

def process_subject_data(sub_names: list, sub_data: dict):
    """
    Process subject data: anonymize, convert to BIDS format, and copy relevant
    anatomical images and transformations.

    Args:
        sub_names (list): List of subject names.
        sub_data (dict): Dictionary mapping subjects to their MEG data (e.g. restig state).
    """
    sub_num = {}
    sub_dataset = {}
    num = 1

    for sub in sub_names:
        sub_rest = sub_data[sub]
        print(sub_rest)
        path = os.path.join(os.path.dirname(sub_rest), 'anat')
        sub_anat = os.path.join(path, (sub + '.mri'))
        sub_trans = os.path.join(path, (sub + '-trans.fif'))
        print(sub_anat)
        sub_dataset[sub] = (sub_rest, sub_anat)

        try: 
            # Read and preprocess the CTF MEG data (could be adapted for data from other MEG systems)
            raw = mne.io.read_raw_ctf(sub_rest, preload=False, verbose=False)
            raw = mne.io.RawArray(raw.get_data(), info=raw.info)

            # Anonymize the data
            raw.anonymize(verbose=False)
            print(f"{sub} anonymized")

            # Create a BIDSPath object for the output
            bids_path = BIDSPath(subject=str(num), task='rest', root=BIDS_ROOT_DIR)

            # Write the data to BIDS format
            write_raw_bids(raw, bids_path, overwrite=True, verbose=False,
                           allow_preload=True, format='FIF')

        except RuntimeError as e:
            print("\n\n Runtime error: ", e)        
            logging.info(f"{sub} caused {e}") 
            print("\n\n\tOperation failed!!!********************************s\n\n")
            continue
        
        sub_num[sub] = num
        
        # Ensure the anatomical directory exists in BIDS
        str_bids_path = str(bids_path.directory)
        bids_anat = os.path.join(str_bids_path, 'anat')
        print(bids_anat)
        
        if not os.path.exists(bids_anat):
            os.makedirs(bids_anat)

        # Copy anatomical files to the BIDS anat directory
        shutil.copy(sub_anat, os.path.join(bids_anat, f'sub-{num}_T1w_defaced.mri'))
        shutil.copy(sub_trans, os.path.join(bids_anat, f'sub-{num}-trans.fif'))

        num += 1
        print("=================================================================")

def save_subject_mapping(sub_num: dict, output_path: str):
    """
    Save the subject mapping (subject name to number) to a CSV file.

    Args:
        sub_num (dict): Dictionary mapping subject names to numbers.
        output_path (str): Path to save the CSV file.
    """
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Subject', 'Number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for subject, number in sub_num.items():
            writer.writerow({'Subject': subject, 'Number': number})

    print(f"Dictionary saved as '{output_path}' in CSV format.")

def main():
    # Step 1: Find MEG directories matching the pattern
    meg_dirs = find_meg_directories(SEARCH_DIRECTORY, PATTERN)

    # Step 2: Get subject data from the directories
    sub_data, sub_names = get_subject_data(meg_dirs)

    # Step 3: Process each subject's data
    process_subject_data(sub_names, sub_data)

    # Step 4: Save the subject mapping to CSV
    save_subject_mapping(sub_num, '/MEG Output Example/subjects.csv')

if __name__ == "__main__":
    main()
