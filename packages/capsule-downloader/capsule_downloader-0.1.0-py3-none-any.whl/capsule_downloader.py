import fnmatch
import os
import subprocess
import sys
from argparse import ArgumentParser

import requests
import wget
from bs4 import BeautifulSoup
from examples import custom_style_2
from PyInquirer import Separator, prompt


def find_localfiles(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
        break
    return result


def main():

    WEBSITE_URL = "https://aotu.ai"
    WEBSITE_PATH = "/docs/downloads/"
    HREF_STARTSWITH = "/release"
    VISIONCAPSULES_EXT = ".cap"
    brainframe_info_data_path = subprocess.getoutput("brainframe info data_path")
    DEFAULT_LOCAL_PATH = brainframe_info_data_path + "/capsules"

    parser = ArgumentParser(
        description="A helper utility for downloading BrainFrame capsules."
    )
    parser.add_argument(
        "capsules_path",
        help="The path to the BrainFrame capsules.",
        nargs="?",
        default=DEFAULT_LOCAL_PATH,
    )
    args = parser.parse_args()

    print("Usage: " + sys.argv[0] + " " + args.capsules_path + "\n")

    # Retrieve table from remote website
    print("Connect to VisionCapsules Marketplace at " + WEBSITE_URL)

    response = requests.get(WEBSITE_URL + WEBSITE_PATH)
    html = response.content.decode("utf-8")  # text
    soup = BeautifulSoup(html, features="lxml")
    table = soup.find("table")

    # Parse table head
    thead = table.find("thead")
    rows = thead.find_all("tr")
    for row in rows:
        cols = row.find_all("th")
        thead_name = cols[0].string.strip()
        thead_description = cols[1].string.strip()
        thead_hardware = cols[2].string.strip()
        thead_required_input = cols[3].string.strip()
        thead_output = cols[4].string.strip()

    # Parse table body
    TBODY_PRODUCTION = "✨"
    TBODY_REQUIRED_INPUT_TYPE = "Type:"
    TBODY_REQUIRED_INPUT_DETECTIONS = "Detections:"
    TBODY_REQUIRED_INPUT_TRACKED = "Tracked:"
    TBODY_OUTPUT_TYPE = "Type:"
    TBODY_OUTPUT_CLASSIFIES = "Classifies:"
    TBODY_OUTPUT_DETECTIONS = "Detections:"
    TBODY_OUTPUT_ENCODED = "Encoded:"
    TBODY_OUTPUT_TRACKED = "Tracked:"
    TBODY_OUTPUT_EXPAND = "Expand"

    TBODY_DOWNLOAD_URL = "a"
    TBODY_FILE_NAME = "FileName"

    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    vcap_table = []

    VisionCapsules_FullList = []
    for row in rows:
        tbody_production = ""
        tbody_required_input_type = ""
        tbody_required_input_detections = ""
        tbody_required_input_tracked = False
        tbody_output_type = ""
        tbody_output_classifies = ""
        tbody_output_detections = ""
        tbody_output_encoded = False
        tbody_output_tracked = False
        tbody_output_expand = False
        tbody_download_url = ""
        tbody_file_name = ""

        # Parse vcap download URL
        link = row.find("a")
        if link.has_attr("href"):
            linktext = link["href"]
            startswith = linktext.startswith(HREF_STARTSWITH)
            endswith = linktext.endswith(VISIONCAPSULES_EXT)
            if startswith and endswith:
                download_url = WEBSITE_URL + linktext
                VisionCapsules_FullList.append(download_url)

                tbody_download_url = download_url
                tbody_file_name = download_url.split("/")[-1]

        cols = row.find_all("td")

        # Parse the text in the first 3 columns: Name, Description, Hardware
        tbody_name = cols[0].string
        tbody_description = cols[1].string
        if tbody_description.startswith(TBODY_PRODUCTION):
            tbody_description = tbody_description.replace(TBODY_PRODUCTION, "").strip()
            tbody_production = "Ready"

        tbody_hardware = cols[2].get_text(separator=" ").strip()

        # Parse the text in the Required Input column
        vcap_required_input = cols[3].find_all("strong")
        items = cols[3].find_all("strong")
        for item in vcap_required_input:
            item_name = item.contents[0]

            next_item = item.nextSibling
            item_value = next_item.string

            if item_name == TBODY_REQUIRED_INPUT_TYPE:
                tbody_required_input_type = item_value
            if item_name == TBODY_REQUIRED_INPUT_DETECTIONS:
                tbody_required_input_detections = str(item_value)
            if item_name == TBODY_REQUIRED_INPUT_TRACKED:
                tbody_required_input_tracked = item_value

        # Parse the text in the Output column
        vcap_output = cols[4].find("summary")
        if vcap_output:
            tbody_output_expand = True

        vcap_output = cols[4].find_all("strong")
        for item in vcap_output:

            item_name = item.contents[0]

            next_item = item.nextSibling
            item_value = next_item.string

            next_item = next_item.nextSibling
            item_detail = next_item

            if item_name == TBODY_OUTPUT_TYPE:
                tbody_output_type = item_value
            if item_name == TBODY_OUTPUT_DETECTIONS:
                tbody_output_detections = item_value
            if item_name == TBODY_OUTPUT_ENCODED:
                tbody_output_encoded = item_value
            if item_name == TBODY_OUTPUT_TRACKED:
                tbody_output_tracked = item_value
            if item_name == TBODY_OUTPUT_CLASSIFIES:
                if item_detail:
                    tbody_output_classifies = str(item_detail)
                    while next_item:
                        next_item = next_item.nextSibling  # skip a <br>
                        if next_item:
                            next_item = next_item.nextSibling
                            item_detail2 = next_item
                            tbody_output_classifies = (
                                tbody_output_classifies + ". " + str(item_detail2)
                            )

        vcap_item = {
            thead_name: tbody_name,
            thead_description: tbody_description,
            TBODY_PRODUCTION: tbody_production,
            thead_hardware: tbody_hardware,
            # thead_required_input: vcap_required_input,
            TBODY_REQUIRED_INPUT_TYPE: tbody_required_input_type,
            TBODY_REQUIRED_INPUT_DETECTIONS: tbody_required_input_detections,
            TBODY_REQUIRED_INPUT_TRACKED: tbody_required_input_tracked,
            # thead_output:         vcap_output,
            TBODY_OUTPUT_TYPE: tbody_output_type,
            TBODY_OUTPUT_CLASSIFIES: tbody_output_classifies,
            TBODY_OUTPUT_DETECTIONS: tbody_output_detections,
            TBODY_OUTPUT_ENCODED: tbody_output_encoded,
            TBODY_OUTPUT_TRACKED: tbody_output_tracked,
            TBODY_OUTPUT_EXPAND: tbody_output_expand,
            TBODY_DOWNLOAD_URL: tbody_download_url,
            TBODY_FILE_NAME: tbody_file_name,
        }

        vcap_table.append(vcap_item)

    # Build VisionCapsules lists from local path
    vcap_local_list = find_localfiles("*" + VISIONCAPSULES_EXT, args.capsules_path)

    # Initialize the Choices list, mark the downloaded VisionCapsules as True in the list
    vcap_choices = []
    last_selection_name = ""
    for vcap_rol in vcap_table:

        vcap_url = vcap_rol.get(TBODY_DOWNLOAD_URL)

        # Use the first word of the vcap file name as the section name
        vcap_remote_file_name = vcap_rol.get(TBODY_FILE_NAME)
        selection_name = vcap_remote_file_name.split("_")[0]

        exists = False
        for vcap_local_file_path in vcap_local_list:

            vcap_local_file_name = vcap_local_file_path.split("/")[-1]
            if vcap_remote_file_name == vcap_local_file_name:
                exists = True
                break
            else:
                exists = False

        if selection_name != last_selection_name:
            SeparatorText = "======== " + selection_name + " ========"
            vcap_choices.append(Separator(SeparatorText))
            last_selection_name = selection_name

        # Add VisionCapsules download url line
        vcap_choices.append({"name": vcap_url, "checked": exists})

        # Add VisionCapsules Name, Description
        vcap_text = vcap_rol.get(thead_name) + ": "
        if vcap_rol.get(TBODY_PRODUCTION):
            vcap_text = (
                vcap_text + "(Production " + vcap_rol.get(TBODY_PRODUCTION) + ") "
            )

        vcap_text = vcap_text + vcap_rol.get(thead_description)

        vcap_choices.append(Separator("  " + vcap_text))

        # Add VisionCapsules Hardware, Required Input, Output
        vcap_text = thead_hardware + ": " + vcap_rol.get(thead_hardware)
        vcap_choices.append(Separator("  " + vcap_text))

        vcap_text = (
            thead_required_input + ": " + vcap_rol.get(TBODY_REQUIRED_INPUT_TYPE)
        )
        if vcap_rol.get(TBODY_REQUIRED_INPUT_TRACKED):
            vcap_text = vcap_text + ". " + TBODY_REQUIRED_INPUT_TRACKED + "True "
        if vcap_rol.get(vcap_rol.get(TBODY_REQUIRED_INPUT_DETECTIONS)):
            vcap_text = vcap_text + ". " + vcap_rol.get(TBODY_REQUIRED_INPUT_DETECTIONS)
        vcap_choices.append(Separator("  " + vcap_text))

        vcap_text = thead_output + ": " + vcap_rol.get(TBODY_OUTPUT_TYPE)
        if vcap_rol.get(TBODY_OUTPUT_ENCODED):
            vcap_text = vcap_text + ". " + TBODY_OUTPUT_ENCODED + "True "
        if vcap_rol.get(TBODY_OUTPUT_TRACKED):
            vcap_text = vcap_text + ". " + TBODY_OUTPUT_TRACKED + "True "
        if vcap_rol.get(TBODY_OUTPUT_CLASSIFIES):
            vcap_text = (
                vcap_text
                + ". "
                + TBODY_OUTPUT_CLASSIFIES
                + " "
                + vcap_rol.get(TBODY_OUTPUT_CLASSIFIES)
            )
        if vcap_rol.get(TBODY_OUTPUT_DETECTIONS):
            vcap_text = (
                vcap_text
                + ". "
                + TBODY_OUTPUT_DETECTIONS
                + " "
                + vcap_rol.get(TBODY_OUTPUT_DETECTIONS)
            )
        vcap_choices.append(Separator("  " + vcap_text))

    questions = [
        {
            "type": "checkbox",
            "qmark": "[?]",
            "message": "Select VisionCapsules",
            "name": "vcap choices",
            "choices": vcap_choices,
            "validate": lambda answer: "You must choose at least one topping."
            if len(answer) == 0
            else True,
        }
    ]

    answers = prompt(questions, style=custom_style_2)

    vcap_selected_list = answers.get("vcap choices")

    # Download newly selected VisionCapsules
    for vcap_url in vcap_selected_list:

        vcap_local_file_name_to_be_downloaded = (
            args.capsules_path + "/" + vcap_url.split("/")[-1]
        )

        if not os.path.exists(vcap_local_file_name_to_be_downloaded):

            print("\nDownloading " + vcap_url)
            wget.download(vcap_url, out=args.capsules_path)

    for vcap_local_file_path in vcap_local_list:

        vcap_local_file_name = vcap_local_file_path.split("/")[-1]
        delete_me = True
        for vcap_url in vcap_selected_list:
            if vcap_local_file_name in vcap_url:
                delete_me = False
                break
        if delete_me:
            os.remove(vcap_local_file_path)

    print("Done.")
    print("VisionCapsules are in " + args.capsules_path)


if __name__ == "__main__":
    main()
