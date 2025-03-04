# MEG Data BIDS Conversion

## Overview
This script scans directories for MEG data (primarily CTF), anonymizes them, converts them to BIDS format, and saves additional data like anatomical images and transformations. It then generates a CSV file mapping subject names to numerical identifiers. This script can be adapted for other MEG system datasets.

## Features
- **Automated MEG data discovery**: Searches for MEG directories matching a predefined pattern.
- **Anonymization**: Ensures subject privacy by anonymizing the MEG data.
- **BIDS conversion**: Converts MEG data to the Brain Imaging Data Structure (BIDS) format.
- **Inclusion of anatomical images and transformations**: Copies associated MRI and transformation files to the BIDS dataset.
- **Subject mapping**: Generates a CSV file mapping subject names to numerical IDs.
- **Logging**: Captures errors and processing details in a log file.

## Prerequisites
### Dependencies
Ensure the following Python packages are installed:
```bash
pip install mne mne-bids numpy scipy pandas
```
These libraries are required for MEG data handling, BIDS conversion, and general data processing.

## Usage
### Running the Script
To execute the script, run:
```bash
python script_name.py
```
This will perform the following steps:
1. Scan for MEG data directories matching the pattern (adjust the pattern as needed).
2. Extract subject data and associate them with their MEG recordings.
3. Anonymize and convert MEG data into BIDS format.
4. Copy anatomical images and transformation files into the BIDS structure.
5. Save a CSV file containing subject mappings.

### Output Files
- **BIDS dataset**: The converted MEG data
- **Log file**: A log of errors and processing details 
- **CSV file**: A mapping of subject names to numerical identifiers

## Script Details
### Key Functions
- `find_meg_directories(search_directory, pattern)`: Scans for MEG directories matching the pattern.
- `get_subject_data(meg_dirs)`: Extracts subject names and maps them to MEG recordings.
- `process_subject_data(sub_names, sub_data)`: Processes each subject's MEG data, anonymizing and converting it to BIDS.
- `save_subject_mapping(sub_num, output_path)`: Saves the subject-name-to-number mapping to a CSV file.

### Error Handling
If an error occurs during processing (e.g., missing files or data corruption), the script logs the error in `bids.log` and moves to the next subject.

## Customization
- **Modify directory paths**: Update `SEARCH_DIRECTORY` and `BIDS_ROOT_DIR` to match your dataset locations.
- **Adjust file naming conventions**: Modify `PATTERN` if your MEG dataset follows a different naming pattern.


