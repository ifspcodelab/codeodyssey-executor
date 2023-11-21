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


def save_testcase(testcase):
    connection, cursor = get_connection_and_cursor()

    try:
        query = "INSERT INTO testcases (id, test_name, success, info, time, result_id) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (str(testcase.id), testcase.test_name, testcase.success, testcase.info, testcase.time, str(testcase.result_id))

        cursor.execute(query, data)

        connection.commit()
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        connection.close()
        cursor.close()


def test_result_to_dict(result_id, test_case_element):
    result_test_case = ResultTestCase(
        test_case_element['@name'],
        False if 'failure' in test_case_element else True,
        test_case_element['failure']['@message'] if 'failure' in test_case_element else None,
        test_case_element['@time'],
        result_id,
    )

    save_testcase(result_test_case)

    return result_test_case.asdict()


def save_result(result):
    connection, cursor = get_connection_and_cursor()

    try:
        query = "INSERT INTO results (id, name, time, error, activity_id) VALUES (%s, %s, %s, %s, %s)"
        data = (str(result.id), result.name, result.time, result.error, result.activity_id)

        cursor.execute(query, data)

        connection.commit()
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        connection.close()
        cursor.close()


def xml_to_json(activity_id,  xml_text_string):
    test_result_dict = xmltodict.parse(xml_text_string)

    result = Result(
        test_result_dict['testsuite']['@name'],
        test_result_dict['testsuite']['@time'],
        None,
        activity_id,
    )

    save_result(result)

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

    save_result(build_failed_result)

    build_failed_result_dict = build_failed_result.asdict()
    build_failed_result_dict['testcases'] = []

    return json.dumps(build_failed_result_dict, indent=4)