import json
import xmltodict
import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../..'))
from models.Result import Result
from models.ResultTestCase import ResultTestCase
from services.database.database import get_connection_and_cursor
import re
from services.logging.Logger import Logger


logger = Logger.get_logger_without_handler()


def test_result_to_dict(result_id, test_case_element):
    result_test_case = ResultTestCase(
        test_case_element['@name'],
        False if 'failure' in test_case_element else True,
        test_case_element['failure']['@message'] if 'failure' in test_case_element else None,
        test_case_element['@time'],
        result_id,
    )

    return result_test_case.asdict()


def xml_to_json(activity_id,  xml_text_string):
    test_result_dict = xmltodict.parse(xml_text_string)

    result = Result(
        test_result_dict['testsuite']['@name'],
        test_result_dict['testsuite']['@time'],
        None,
        activity_id,
    )

    test_result_testcases_dict = test_result_dict['testsuite']['testcase']
    new_testcases_dict = [test_result_to_dict(result.id, testcase) for testcase in test_result_testcases_dict]

    result_dict = result.asdict()
    result_dict['testcases'] = new_testcases_dict

    return json.dumps(result_dict, indent=4)


def json_when_build_fail(activity_id, logs):
    pattern = r"> Task :compileTestJava FAILED(.*?)FAILURE: Build failed with an exception."
    match = re.search(pattern, logs, re.DOTALL)
    error_text = match.group(1).strip()

    build_failed_result = Result(
        'Build failed',
        0.0,
        error_text,
        activity_id,
    )

    build_failed_result_dict = build_failed_result.asdict()
    build_failed_result_dict['testcases'] = []

    return json.dumps(build_failed_result_dict, indent=4)