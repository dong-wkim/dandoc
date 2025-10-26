import re,os,json
import yaml

data_dir = "D:/python/data/"
input_dir = data_dir + "input/"
output_dir = data_dir + "output/"

input_file_name = input("Enter the name of the file you wish to convert from (with the extension): ")
file_name = re.match(r"^(.*)\.(.*)$", input_file_name).group(1).strip()
input_file_format = re.match(r"^(.*)\.(.*)$", input_file_name).group(2).strip()
output_file_format = input("What file format you like to convert this file to? ")

input_file = input_dir + input_file_format + "/" + file_name + "." + input_file_format
output_file = output_dir + output_file_format + "/" + file_name + "." + output_file_format

os.makedirs(output_dir, exist_ok=True)

with open(input_file, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

