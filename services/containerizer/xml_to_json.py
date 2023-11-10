import xml.etree.ElementTree as ET
import json

# Path to test report file
# xml_file = 'build/test-results/test/TEST-com.example.helloworld.hello.world.HelloWorldApplicationTests.xml'

# TODO: review to meet needs
def test_result_to_dict(test_case_element):
    result = {
        'name': test_case_element.get('name'),
        'classname': test_case_element.get('classname'),
        'time': test_case_element.get('time'),
        'status': 'passed' if test_case_element.find('success') is not None else 'failed',
    }
    return result

def xml_to_json(xml_text_string):
    # tree = ET.parse(xml_file) # In case xml_file is used
    # removing first line so it can be processed
    lines = xml_text_string.splitlines()
    lines = lines[1:]
    xml_string_without_first_line = '\n'.join(lines)
    tree = ET.ElementTree(ET.fromstring(xml_string_without_first_line))
    root = tree.getroot()
    test_results = [test_result_to_dict(test_case) for test_case in root.iter('testcase')]
    return json.dumps(test_results, indent=4)