import sys
from pathlib import Path
import src

def main():
    input_format = input('Enter input file format: ').strip().lower()
    output_format = input('Enter output file format: ').strip().lower()
    file_name = input('Enter file name (without extension): ').strip()
    data_dir = Path('./data/')
    input_file = data_dir / input_format / f'{file_name}.{input_format}'
    output_file = data_dir / output_format / f'{file_name}.{output_format}'
    module_name = f'{input_format}_{output_format}'
    convert_func = getattr(src,f'{input_format}_{output_format}', None)
    if convert_func is None:
        print(f'Error: No conversion function found for {input_format} to {output_format}')
        sys.exit(1)
    print(f'Converting {input_file} to {output_file} using {module_name} module...')
    convert_func(str(input_file), str(output_file))

if __name__ == '__main__':
    main()