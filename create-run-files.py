def extract_sections(input_file, output_files, marker):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Find all marker line indices
    marker_indices = [i for i, line in enumerate(lines) if marker in line]

    # Ensure there are at least three markers
    if len(marker_indices) < 3:
        raise ValueError("Not enough marker instances found.")

    # Extract sections and write to output files
    for i in range(2):
        start = marker_indices[i]
        end = marker_indices[i+1]
        with open(output_files[i], 'w') as out_f:
            out_f.writelines(lines[start:end])

if __name__ == "__main__":
    extract_sections(
        input_file='graph-trace.txt',
        output_files=['run1.txt', 'run2.txt'],
        marker='db_num_tokens ='
    )