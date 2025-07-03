import re

def extract_sections(input_file, marker):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Find all marker line indices
    marker_indices = [i for i, line in enumerate(lines) if marker in line]

    # Ensure there are at least three markers
    if len(marker_indices) < 3:
        raise ValueError("Not enough marker instances found.")

    # Extract the two sections
    section1 = lines[marker_indices[0]:marker_indices[1]]
    section2 = lines[marker_indices[1]:marker_indices[2]]

    return section1, section2

def extract_element_number(line):
    # Match 'element = <number>' at the start of the line, ignoring leading whitespace
    match = re.search(r'el\s*=\s*(-?\d+(?:\.\d+)?)', line)
    return float(match.group(1)) if match else None

def interleave_sections(section1, section2):
    # Interleave lines from both sections, appending '>>>' if element numbers differ
    interleaved = []
    max_len = max(len(section1), len(section2))
    for i in range(max_len):
        line1 = section1[i] if i < len(section1) else None
        line2 = section2[i] if i < len(section2) else None

        if line1 and line2:
            num1 = extract_element_number(line1)
            num2 = extract_element_number(line2)
            if num1 != num2:
                # Prepend '>>>' to both lines if numbers differ
                line1 = '>>> ' + line1
                line2 = '>>> ' + line2
        if line1:
            interleaved.append(line1)
        if line2:
            interleaved.append(line2)
    return interleaved

if __name__ == "__main__":
    section1, section2 = extract_sections(
        input_file='graph-trace.txt',
        marker='db_num_tokens ='
    )
    interleaved = interleave_sections(section1, section2)
    with open('interleaved_diff.txt', 'w') as out_f:
        out_f.writelines(interleaved)