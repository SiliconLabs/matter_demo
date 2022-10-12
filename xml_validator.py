import xml.etree.ElementTree as ET
import os
import sys


xml_doc_tree = ET.parse(str(sys.argv[1]))

xml_root = xml_doc_tree.getroot()
ROOT_DIR = os.getcwd()
success = True

for child in xml_root:
    for tag in child:
        for key in tag.attrib:
            if tag.attrib[key] == "core.boardCompatibility":
                boardName = tag.attrib["value"]

            elif tag.attrib[key] == "demos.imageFile":
                imagePath = tag.attrib["value"]

    if str(boardName).lower() in str(imagePath).lower():
        if (not (os.path.isfile(imagePath))):
            print("ERROR: binary for board %s presumably at path %s is missing!" % (
                boardName, str(imagePath)))
            success = False
    else:

        print("Path for the Binary pertaining to board %s might be incorrect" % boardName)
        success = False

if success:
    print("%s was successfully validated!" % str(sys.argv[1]))
else:
    print("Please fix the above listed errors and try again!")
