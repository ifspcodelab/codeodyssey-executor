import json
import xmltodict
import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../..'))
from models.Result import Result
from models import ResultTestCase
from services.database.database import get_connection_and_cursor
import re


def test_result_to_dict(test_case_element):
    result_test_case = ResultTestCase(
        test_case_element['@name'],
        False if 'failure' in test_case_element else True,
        test_case_element['failure']['@message'] if 'failure' in test_case_element else None,
        test_case_element['@time'],
    )

    connection, cursor = get_connection_and_cursor()

    try:
        cursor.execute(
            f"INSERT INTO testcases (id, test_name, success, info, time, result_id)"
            f" VALUES ({result_test_case.id, result_test_case.testName, result_test_case.success, test_case_element.info, test_case_element.time})"
        )
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")

    print(result_test_case)

    exit()
    result = {
        'testName': test_case_element['@name'],
        'sucess': False if 'failure' in test_case_element else True,
        'info': test_case_element['failure']['@message'] if 'failure' in test_case_element else None,
        'time': test_case_element['@time'],
    }
    return result


def xml_to_json(activity_id,  xml_text_string):
    # test_result_dict = xmltodict.parse(xml_text_string)
    print(xml_text_string)

    exit()

    # result = Result(
    #     test_result_dict['@name'],
    #     test_result_dict['@time'],
    #     '',
    #     activity_id,
    # )

    # connection, cursor = get_connection_and_cursor()

    # try:
    #     cursor.execute(
    #         f"INSERT INTO testcases (id, test_name, success, info, time, result_id)"
    #         f" VALUES ({result_test_case.id, result_test_case.testName, result_test_case.success, test_case_element.info, test_case_element.time})"
    #     )
    #     connection.commit()
    # except Exception as e:
    #     print(f"Error: {e}")


    # test_result_testcases_dict = test_result_dict['testsuite']['testcase']
    # new_testcases_dict = [test_result_to_dict(testcase) for testcase in test_result_testcases_dict]
    # print(new_testcases_dict)

    # exit()



    return json.dumps(test_result_dict, indent=4)

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

    # save in db
    save_result(build_failed_result)

    return json.dumps(build_failed_result.asdict(), indent=4)

def save_result(result):
    connection, cursor = get_connection_and_cursor()

    try:
        query = "INSERT INTO results (id, name, time, error, activity_id) VALUES (%s, %s, %s, %s, %s)"
        data = (str(result.id), result.name, result.time, result.error, result.activity_id)

        cursor.execute(query, data)

        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()
        cursor.close()