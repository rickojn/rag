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

def interleave_sections(section1, section2):
    # Interleave lines from both sections
    interleaved = []
    max_len = max(len(section1), len(section2))
    for i in range(max_len):
        if i < len(section1):
            interleaved.append(section1[i])
        if i < len(section2):
            interleaved.append(section2[i])
    return interleaved

if __name__ == "__main__":
    section1, section2 = extract_sections(
        input_file='graph-trace.txt',
        marker='db_num_tokens ='
    )
    interleaved = interleave_sections(section1, section2)
    with open('interleaved.txt', 'w') as out_f:
        out_f.writelines(interleaved)