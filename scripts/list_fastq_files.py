import os

# Specify the directory path
directory = '/home/erin/Projects/WDFW/SPSid/GTseq_November2024/'

# Get all .fastq files in the directory
fastq_files = [f for f in os.listdir(directory) if f.endswith('.fastq')]

# Write the filenames to a text file
with open('GTseq_Nov2024_fastq_files_list.txt', 'w') as output_file:
    for file in fastq_files:
        output_file.write(f"{file}\n")

print(f"List of .fastq files has been saved to GTseq_Nov2024_fastq_files_list.txt")