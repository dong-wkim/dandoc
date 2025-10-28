import re,os,json
import yaml

def convert(input_file, output_file, file_name=None):
    with open(input_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)