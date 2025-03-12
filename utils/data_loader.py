import json
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor

def remove_non_ranked_matches(files_in_directory):
    for file_name in files_in_directory:
        file_path = f"New folder/{file_name}"
        try:
            with open(file_path, 'r', encoding="utf8") as file:
                data = json.load(file)
                file.close()
            if not data.get("matchInfo", {}).get("isRanked", True):
                os.remove(file_path)
        except (json.JSONDecodeError, KeyError):
            print(f"Skipping file {file_name} due to error in reading or missing keys.")


def process_file(file_name, zip_ref, files_in_directory):
    # Check if the file already exists
    if file_name in files_in_directory:
        print(f"File {file_name} already in folder")
        return
    else:
        # Extract the file content
        print("Checking for ranked")
        with zip_ref.open(file_name) as file:
            data = json.load(file)
            # print("Loaded JSON. Checking for Ranked.")
            # Check if the match is ranked
            print(f"The value for isRanked for file {file_name} is {data.get("matchInfo", {}).get("isRanked")}")
            if data.get("matchInfo", {}).get("isRanked", True):
                # Extract the file to the New folder
                zip_ref.extract(file_name, path="New folder")
                print(f"Saved {file_name}")

def extract_data_from_zipfile(files_in_directory):




    # Open the zip file
    with zipfile.ZipFile('export_v10_03_limited.zip', 'r') as zip_ref:

        print("Loaded zip file")

        # Get the list of all file names in the zip
        all_files = zip_ref.namelist()[::-1]
        print("Got all names of files within zip")

        # Use ThreadPoolExecutor to parallelize the processing
        # with ThreadPoolExecutor(max_workers=8) as executor:
        #     executor.map(lambda file_name: process_file(file_name, zip_ref), all_files)

        for file_name in all_files:
            process_file(file_name=file_name, zip_ref=zip_ref, files_in_directory= files_in_directory)


            # if file_name in files_in_directory:
            #     print(f"File {file_name} already in folder")
            #     zip_ref.extract(member=file_name, path="New folder")
            #     print(f"Saved {file_name} to New folder")


