import yaml
import os


def read_yaml(file_path):
    try:
        cur_path = os.path.dirname(os.path.abspath(__file__))

        root_path = os.path.dirname(cur_path)

        abs_path = os.path.join(root_path, file_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            test_cases = yaml.safe_load(f)
        return test_cases
    except FileNotFoundError as fe:
        print(f"file not found : {fe}")

        return []
    except Exception as e:
        print(f"unknown error:{e}")
        return []
