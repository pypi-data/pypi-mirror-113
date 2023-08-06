import time
import os
import numpy as np
import pandas as pd

from angeutils.format_utils import colored_string, TEXT_COLOR


def time_recorder(func):
    def record_time(*arg):
        start_time = time.time()  # datetime.datetime.now()
        print(f"[time info] start run function {func.__name__}...")

        result = func(*arg)

        end_time = time.time()  # datetime.datetime.now()
        print(f"[time info] finished run function {func.__name__}.")

        cost_time = (end_time-start_time)  # .microseconds
        print(f"[time info] function {func.__name__} spent {cost_time} seconds.")
        return result
    return record_time


def file_exists_checker(func):
    def file_exists(*arg):
        filepath = func(*arg)
        is_file_exists = os.path.isfile(filepath)
        print(f"check file is exists: {filepath}")
        print(f"result: {is_file_exists}")
        return filepath
    return file_exists


def dir_exists_checker(func):
    def dir_exist(*arg):
        dir = func(*arg)
        is_dir_exists = os.path.exists(dir)
        print(f"check dir is exists: {dir}")
        print(f"result: {is_dir_exists}")
        return dir
    return dir_exist


def results_printer(func):
    def print_result(*args):
        results = func(*args)
        print(f"\n*************** FUNCTION [{func.__name__}]'s results ****************")
        for result in results:
            print(type(result), ':', result)
        print(f"*************** FUNCTION [{func.__name__}]'s results ****************\n")
        return results
    return print_result


def result_printer(func):
    def print_result(*args):
        result = func(*args)
        print(f"\n*************** FUNCTION [{func.__name__}]'s result ****************")
        print(type(result), ':', result)
        print(f"*************** FUNCTION [{func.__name__}]'s result ****************\n")
        return result
    return print_result


def csvfile_writer(func):
    def write_csvfile(*args):
        results = func(*args)
        df_file = results[-2]
        filename = results[-1]
        if df_file is not None:
            df_file.to_csv(filename)
        else:
            print(f"data is None, write {filename} to csv failed.")
        return results
    return write_csvfile


def results_checker(func):
    # supported-types: int, float, str, dict, list, pd.DataFrame
    def check_results(*args):
        results, refer_results = func(*args)
        checks = []
        print(f"\n**************** FUNCTION [{func.__name__}]'s RESULTS and REFER-RESULTS *****************")
        for (i, (result, refer_result)) in enumerate(zip(results, refer_results)):
            is_equal = (result == refer_result) if type(refer_result)!=type(pd.DataFrame()) else result.equals(refer_result)
            checks.append(is_equal)
            str_is_euqal = colored_string(raw_str=f"{'True' if is_equal else 'False'}",
                                          text_color=(TEXT_COLOR.GREEN) if is_equal else TEXT_COLOR.RED)
            print(f"-----param_{i}-----\n"
                  f"{type(result)}: {result}\n<->\n{type(refer_result)}: {refer_result}\n"
                  f"is_equal: {str_is_euqal}")
        print(f"**************** FUNCTION [{func.__name__}]'s RESULTS and REFER-RESULTS *****************")
        is_pass = np.array(checks).astype(float).sum() == len(checks)
        str_check_result = colored_string(raw_str=f"{'Passed' if is_pass else 'Failed'} the test",
                                          text_color=(TEXT_COLOR.GREEN if is_pass else TEXT_COLOR.RED))
        print(f"check_results: {checks} -> {is_pass}; {str_check_result}.")
        return results, refer_results
    return check_results


def result_checker(func):
    # supported-types: int, float, str, dict, list, pd.DataFrame
    def check_result(*args):
        result, refer_result = func(*args)
        print(f"\n**************** FUNCTION [{func.__name__}]'s RESULT and REFER-RESULT *****************")
        is_pass = (result == refer_result) if type(refer_result) != type(pd.DataFrame()) else result.equals(
            refer_result)
        print(f"{type(result)}: {result}\n<->\n{type(refer_result)}: {refer_result}")
        print(f"**************** FUNCTION [{func.__name__}]'s RESULT and REFER-RESULT *****************")
        str_check_result = colored_string(raw_str=f"{'Passed' if is_pass else 'Failed'} the test",
                                          text_color=(TEXT_COLOR.GREEN if is_pass else TEXT_COLOR.RED))
        print(f"check_results: {is_pass}; {str_check_result}.")
        return result, refer_result
    return check_result





