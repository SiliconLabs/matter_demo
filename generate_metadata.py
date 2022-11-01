from genericpath import isdir
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom



root_dir = os.getcwd()
examples_dir = os.path.join(root_dir, "Examples")
root_sub_dirs = os.listdir(root_dir)


'''
Recurse all directories and remove undesired files 
'''

def recurse_dir(file_or_dir):

    if os.path.isdir(file_or_dir):
        subdirs = os.listdir(file_or_dir)
        for unit in subdirs:
            recurse_dir(os.path.join(file_or_dir, unit))
    else:
        if '.ds_store' in file_or_dir.lower():
            os.remove(file_or_dir)
        if 'BRD' in os.path.basename(os.path.dirname(file_or_dir)):          
            if '.s37' not in file_or_dir:
                os.remove(file_or_dir)
        

recurse_dir(root_dir)


'''
Scan Examples folder to account for all demos present
'''

example_map = {
    'Examples': {}
}

if os.path.isdir(examples_dir):
    list_of_examples = os.listdir(examples_dir)
else:
    raise Exception("%s doesn't exist!")

for example in list_of_examples:

    example_name = ' '.join((example.split("-")))
    example_tech = (example.split("-"))[-1]
    if example_tech == 'thread':  
        example_map['Examples'][example_name] = os.listdir(
            os.path.join(examples_dir, example))

    elif example_tech == 'wifi':
        example_map['Examples'][example_name] = {'wf200': os.listdir(
            os.path.join(examples_dir, example, 'wf200')),
            'rs9116': os.listdir(
            os.path.join(examples_dir, example, 'rs9116')),
            'siwx917': os.listdir(
            os.path.join(examples_dir, example, 'siwx917'))}



'''
generate demo metadata
'''

demos = ET.Element('demos')

demos.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
demos.set('xsi:noNamespaceSchemaLocation',
          "http://www.silabs.com/ss/Demo.ecore")

for example in example_map['Examples']:
    if (example.split(' '))[-1] == 'thread':
        demo_name = ""
        for name in example.split(" "):
            if name == 'app':
                break
            else:
                demo_name += name + " "
        demo_name = demo_name.strip()

        for board in example_map['Examples'][example]:

            demo = ET.SubElement(demos, 'demo')
            blurbProp = ET.SubElement(demo, 'property')
            partCompatibilityProp = ET.SubElement(demo, 'property')
            boardCompatibilityProp = ET.SubElement(demo, 'property')
            imageFileProp = ET.SubElement(demo, 'property')
            readmeFileProp = ET.SubElement(demo, 'property')
            filtersProp = ET.SubElement(demo, 'property')
            qualityProp = ET.SubElement(demo, 'property')
            description = ET.SubElement(demo, 'description')

            demo.set('name', board.lower()+".demo."+example.replace(" ", "_"))
            demo.set('label', "Matter "+"- " +
                     demo_name.capitalize() + " over Thread")

            blurbProp.set('key', 'demos.blurb')
            blurbProp.set('value', "Matter "+"- " +
                          demo_name.capitalize() + " app")

            partCompatibilityProp.set('key', 'core.partCompatibility')
            partCompatibilityProp.set('value', ".*")

            boardCompatibilityProp.set('key', 'core.boardCompatibility')
            boardCompatibilityProp.set('value', board.lower())

            imageFileProp.set('key', 'demos.imageFile')
            imageFileProp.set('value', os.path.join(
                "Examples", ("".join(demo_name+" app"+" thread")).replace(" ", "-"), board.upper(), "".join("chip efr32 " + demo_name + " example.s37").replace(" ", "-")))

            readmeFileProp.set('key', 'core.readmeFiles')
            readmeFileProp.set(
                'value', "https://github.com/SiliconLabs/matter#readme")

            filtersProp.set('key', 'filters')
            filtersProp.set('value', "Wireless\ Technology|Matter")

            qualityProp.set('key', 'core.quality')
            qualityProp.set('value', "PRODUCTION")
            description.text = "".join("This is a Matter " + demo_name.capitalize() +
                                       " Application over Thread for " + board.upper())

    elif (example.split(' '))[-1] == 'wifi':
        demo_name = ""
        for name in example.split(" "):
            if name == 'app':
                break
            else:
                demo_name += name + " "
        demo_name = demo_name.strip()

        for wstk in example_map['Examples'][example]:
            for board in example_map['Examples'][example][wstk]:

                demo = ET.SubElement(demos, 'demo')
                blurbProp = ET.SubElement(demo, 'property')
                partCompatibilityProp = ET.SubElement(demo, 'property')
                boardCompatibilityProp = ET.SubElement(demo, 'property')
                imageFileProp = ET.SubElement(demo, 'property')
                readmeFileProp = ET.SubElement(demo, 'property')
                filtersProp = ET.SubElement(demo, 'property')
                qualityProp = ET.SubElement(demo, 'property')
                description = ET.SubElement(demo, 'description')

                demo.set('name', board.lower()+".demo." +
                         "".join(example.replace(" ", "_")) + "_" + wstk)
                demo.set('label', "Matter "+"- " +
                         demo_name.capitalize() + " over Wi-Fi")

                blurbProp.set('key', 'demos.blurb')
                blurbProp.set('value', "Matter "+"- " +
                              demo_name.capitalize() + " app")

                partCompatibilityProp.set('key', 'core.partCompatibility')
                partCompatibilityProp.set('value', ".*")

                boardCompatibilityProp.set('key', 'core.boardCompatibility')
                boardCompatibilityProp.set('value', board.lower())

                imageFileProp.set('key', 'demos.imageFile')
                imageFileProp.set('value', os.path.join(
                    "Examples", ("".join(demo_name+" app"+" wifi")).replace(" ", "-"), wstk, board.upper(), "".join("chip efr32 " + demo_name + " example.s37").replace(" ", "-")))

                readmeFileProp.set('key', 'core.readmeFiles')
                readmeFileProp.set(
                    'value', "https://github.com/SiliconLabs/matter#readme")

                filtersProp.set('key', 'filters')
                filtersProp.set('value', "Wireless\ Technology|Matter")

                qualityProp.set('key', 'core.quality')
                qualityProp.set('value', "PRODUCTION")
                description.text = "".join("This is a Matter " + demo_name.capitalize() +
                                           " Application for " + board.upper() + " to be used with " +  ('SiWx917' if wstk.lower() == 'siwx917' else wstk.upper()) + (' Wi-Fi Evaluation kit' if wstk.lower() == 'rs9116' else ' Wi-Fi expansion board'))

outputString = ET.tostring(demos, encoding='UTF-8')
dom = xml.dom.minidom.parseString(outputString)
pretty_xml_as_string = dom.toprettyxml()

demosXmlFilePath = os.path.join(root_dir, "demos.xml")
with open(demosXmlFilePath, "w") as demosXmlFile:
    demosXmlFile.write(pretty_xml_as_string)