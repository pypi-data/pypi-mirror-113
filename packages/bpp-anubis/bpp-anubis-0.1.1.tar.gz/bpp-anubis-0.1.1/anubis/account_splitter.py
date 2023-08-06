import configparser
import sys
import os


def get_accounts(
        num_processes: int,
        accounts_file_path: str,
        accounts_section: str
) -> list:
    # get account data available for parallel runs
    data = configparser.ConfigParser()
    data.read(accounts_file_path)
    accounts_data = data[accounts_section]

    # kill everything if more accounts are requested than exists
    if num_processes > len(list(accounts_data.values())):
        print("Not enough accounts; Cannot run tests")
        sys.exit(1)
    else:
        return [acc for acc in list(accounts_data.items())]