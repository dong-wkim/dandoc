import sys
from pathlib import Path
import src
import os

def main():
    input_format = input('Enter input file format: ').strip().lower()
    output_format = input('Enter output file format: ').strip().lower()
    file_name = input('Enter file name (without extension): ').strip()
    data_dir = Path('./data/')
    input_file = data_dir / input_format / f'{file_name}.{input_format}'
    output_file = data_dir / output_format / f'{file_name}.{output_format}'
    os.makedirs(output_file.parent, exist_ok=True)

    try:
        convert_func = src.get_converter(input_format, output_format)
    except (ImportError, AttributeError) as e:
        print(f'Error: No conversion function found for {input_format} to {output_format}: {e}')
        sys.exit(1)

    print(f'Converting {input_file} to {output_file} using {input_format}_{output_format} module...')
    # converters follow signature: convert(file_name, input_path, output_path)
    convert_func(file_name, str(input_file), str(output_file))

if __name__ == '__main__':
    main()