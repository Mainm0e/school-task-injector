import sys
import mmap

def merge_programs(target_program_path, other_program_path):
    # Open the target program
    with open(target_program_path, 'r+b') as target_file:
        target_data = mmap.mmap(target_file.fileno(), 0)

        # Open the other program
        with open(other_program_path, 'rb') as other_file:
            other_data = other_file.read()

            # Find the end of the target program's PE header
            pe_header_offset = target_data.find(b'PE\x00\x00', 0x18)
            if pe_header_offset == -1:
                print("Invalid PE file: PE header not found.")
                return

            # Find the start of the target program's section table
            section_table_offset = pe_header_offset + 0x18 + 0x60
            num_sections_offset = pe_header_offset + 0x6

            # Extract the number of sections
            num_sections = target_data[num_sections_offset]

            # Find the last section's raw data size
            last_section_offset = section_table_offset + (num_sections - 1) * 0x28
            last_section_raw_size_offset = last_section_offset + 0x10
            last_section_raw_size = int.from_bytes(target_data[last_section_raw_size_offset:last_section_raw_size_offset + 4], byteorder='little')

            # Calculate the new size of the target program
            new_size = len(target_data) - last_section_raw_size + len(other_data)

            # Resize the target program
            target_data.resize(new_size)

            # Write the other program's data after the last section
            target_data[last_section_raw_size:new_size] = other_data

    print("Merged successfully!")

def main():
    if len(sys.argv) != 3:
        print("Usage: {} <target_program> <other_program>".format(sys.argv[0]))
        sys.exit(1)

    target_program_path = sys.argv[1]
    other_program_path = sys.argv[2]

    merge_programs(target_program_path, other_program_path)

if __name__ == "__main__":
    main()
