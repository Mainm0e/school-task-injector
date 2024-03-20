import sys

def merge_programs(target_program_path, other_program_path):
    try:
        # Read the contents of the target program
        with open(target_program_path, 'rb') as target_file:
            target_data = target_file.read()

        # Read the contents of the other program
        with open(other_program_path, 'rb') as other_file:
            other_data = other_file.read()

        # Merge the programs
        merged_data =  other_data + target_data

        # Write the merged data back to the target program
        with open(target_program_path, 'wb') as merged_file:
            merged_file.write(merged_data)

        print("Merged successfully!")

    except Exception as e:
        print("An error occurred:", e)

def main():
    if len(sys.argv) != 3:
        print("Usage: {} <target_program> <other_program>".format(sys.argv[0]))
        sys.exit(1)

    target_program_path = sys.argv[1]
    other_program_path = sys.argv[2]

    merge_programs(target_program_path, other_program_path)

if __name__ == "__main__":
    main()
