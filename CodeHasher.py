import hashlib
from tqdm import tqdm
import os
from colorama import init, Fore, Style
import sys

# Initialize colorama
init(autoreset=True)

def calculate_hash(file_path, algorithm='sha256'):
    hash_function = hashlib.new(algorithm)
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_path, ascii=True,
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}, {percentage:.0f}%]") as pbar:
            for block in iter(lambda: f.read(4096), b""):
                hash_function.update(block)
                pbar.update(len(block))
                
    return hash_function.hexdigest()

def print_large_text(text, color='white', size=10, file=sys.stdout):
    # Print star pattern above and below text
    print(f"{'*' * 30}", file=file)
    print(f"{'*' * 30}", file=file)
    print(f"{text.center(26)}", file=file)
    print(f"{'*' * 30}", file=file)
    print(f"{'*' * 30}", file=file)


print("""
******************************
******************************
        CodeHasher        
******************************
******************************
""")



# Ask user for file path
file_path = input("Enter the file path: ").strip()

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' does not exist.")
    sys.exit(1)

# Determine output file path
base_output_file = os.path.splitext(os.path.basename(file_path))[0] + "_codehasher"
output_file = f"{base_output_file}.txt"
increment = 1

# Check if file already exists and incrementally rename
while os.path.exists(output_file):
    output_file = f"{base_output_file}_{increment}.txt"
    increment += 1

# Redirect output to file if not already redirected
if sys.stdout.isatty():
    with open(output_file, 'w') as f:
        # Print large "CodeHasher" in red with star pattern to file
        print_large_text("CodeHasher", color='red', size=10, file=f)
        
        # Print hash calculation message to file
        print("\nCalculating the hash value of the source code...\n", file=f)
        
        # Print hashes without ANSI escape codes to file
        print(f"MD5: {calculate_hash(file_path, 'md5')}", file=f)
        print(f"SHA1: {calculate_hash(file_path, 'sha1')}", file=f)
        print(f"SHA256: {calculate_hash(file_path, 'sha256')}", file=f)

else:
    # Print large "CodeHasher" in red with star pattern to console
    print_large_text("CodeHasher", color='red', size=10)
    
    # Print hash calculation message to console
    print("\nCalculating the hash value of the source code...\n")
    
    # Print hashes with ANSI escape codes to console
    print(f"MD5: {Fore.GREEN}{calculate_hash(file_path, 'md5')}{Style.RESET_ALL}")
    print(f"SHA1: {Fore.GREEN}{calculate_hash(file_path, 'sha1')}{Style.RESET_ALL}")
    print(f"SHA256: {Fore.GREEN}{calculate_hash(file_path, 'sha256')}{Style.RESET_ALL}")

print(f"Output saved to {output_file}")
