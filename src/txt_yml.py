import pandas as pd
import yaml

def convert(lines, file_name, input_format, output_format):
    """Parse markdown syntax into hierarchical dictionary structure."""
    result = {}
    current_section = result
    section_stack = [(result, 0)]  # (dict, level)
    current_content = []
    pending_list_items = []
    
    def save_content_and_lists():
        """Save accumulated content and list items to current section."""
        nonlocal current_content, pending_list_items
        
        if pending_list_items:
            # If we have list items, they become the value
            if len(pending_list_items) == 1:
                # Single item becomes a string
                return pending_list_items[0]
            else:
                # Multiple items become a comma-separated string or list
                return ", ".join(pending_list_items)
        elif current_content:
            # Regular content
            content_text = '\n'.join(current_content).strip()
            return content_text if content_text else None
        return None
    
    def assign_to_section(section, key, value):
        """Assign value to section, handling existing keys."""
        if value is not None:
            if key in section:
                # If key exists and has content, append or merge
                existing = section[key]
                if isinstance(existing, str) and isinstance(value, str):
                    section[key] = f"{existing}\n{value}"
                else:
                    section[key] = value
            else:
                section[key] = value
    
    last_header_key = None
    
    for line in lines:
        line = line.rstrip('\n')
        
        # Handle headers
        if line.startswith('#'):
            # Save any accumulated content/lists to the previous header
            if last_header_key and (current_content or pending_list_items):
                content_value = save_content_and_lists()
                if content_value:
                    parent_section = section_stack[-1][0]
                    assign_to_section(parent_section, last_header_key, content_value)
                current_content = []
                pending_list_items = []
            
            # Determine header level
            level = 0
            while level < len(line) and line[level] == '#':
                level += 1
            
            if level <= 6:  # Valid header levels
                title = line[level:].strip()
                
                # Find appropriate parent level
                while len(section_stack) > 1 and section_stack[-1][1] >= level:
                    section_stack.pop()
                
                parent_section = section_stack[-1][0]
                
                # Create new section if it doesn't exist
                if title not in parent_section:
                    parent_section[title] = {}
                
                current_section = parent_section[title]
                section_stack.append((current_section, level))
                last_header_key = title
            else:
                current_content.append(line)
        
        # Handle lists
        elif line.strip().startswith(('- ', '* ', '+ ')):
            list_item = line.strip()[2:].strip()
            pending_list_items.append(list_item)
        
        # Handle numbered lists
        elif line.strip() and line.strip()[0].isdigit() and '. ' in line:
            parts = line.strip().split('. ', 1)
            if len(parts) == 2:
                list_item = parts[1].strip()
                pending_list_items.append(list_item)
        
        # Handle regular content
        elif line.strip():
            current_content.append(line)
        
        # Handle empty lines (preserve spacing in content)
        else:
            if current_content:  # Only add if we have content already
                current_content.append('')
    
    # Save any remaining content/lists
    if last_header_key and (current_content or pending_list_items):
        content_value = save_content_and_lists()
        if content_value:
            parent_section = section_stack[-1][0]
            assign_to_section(parent_section, last_header_key, content_value)
    
    return result

def dict_to_markdown(data, level=0):
    """Convert hierarchical dictionary back to markdown."""
    result = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            # Add header
            header_prefix = '#' * (level + 1)
            result.append(f"{header_prefix} {key}")
            
            if isinstance(value, dict):
                # Recurse for nested structure
                sub_content = dict_to_markdown(value, level + 1)
                if sub_content:
                    result.extend(sub_content)
            elif isinstance(value, str):
                # Check if it's a comma-separated list or regular content
                if ', ' in value and not '\n' in value:
                    # Likely a list, convert back to bullet points
                    items = [item.strip() for item in value.split(',')]
                    for item in items:
                        result.append(f"- {item}")
                else:
                    # Regular content
                    result.append(value)
            elif isinstance(value, list):
                # Handle list values
                for item in value:
                    result.append(f"- {item}")
    
    return result

def markdown_to_yaml(lines):
    """Convert markdown syntax to YAML structure."""
    parsed_dict = parse_markdown_to_dict(lines)
    return yaml.dump(parsed_dict, default_flow_style=False, allow_unicode=True, sort_keys=False)

def yaml_to_markdown(lines, file_name):
    """Convert YAML structure back to markdown syntax."""
    yaml_content = ''.join(lines)
    
    try:
        yaml_data = yaml.safe_load(yaml_content)
        if yaml_data is None:
            return ""
        
        markdown_lines = dict_to_markdown(yaml_data)
        return '\n'.join(markdown_lines)
        
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return f"# Error parsing YAML: {e}"

def convert(file_name, input_file, output_file):
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Determine conversion direction based on file formats
    if input_format.lower() == 'md' and output_format.lower() == 'yaml':
        # Markdown to YAML conversion
        print("Converting Markdown to YAML...")
        result = markdown_to_yaml(lines)
        
    elif input_format.lower() == 'yaml' and output_format.lower() == 'md':
        # YAML to Markdown conversion
        print("Converting YAML to Markdown...")
        result = yaml_to_markdown(lines)
        
    else:
        print(f"Unsupported conversion: {input_format} to {output_format}")
        print("Supported conversions: md -> yaml, yaml -> md")
        exit(1)

    # Write the result to output file
    output_path = directory + output_file_name
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(result)

    print(f"✅ Conversion completed! Output saved to: {output_path}") 