import os
import shutil
import argparse

import subprocess

parser = argparse.ArgumentParser()

parser.add_argument("-p", type=str, required=True)
parser.add_argument("-a", type=str, required=True, default="SHA256")
parser.add_argument("-cs", type=str, required=True)

args = parser.parse_args()


def checksum(file_path, algorithm, original_checksum):
    
    cmd = f"Get-FileHash -Path {file_path} -Algorithm {algorithm} | findstr '{algorithm}'"
    
    file_checksum = subprocess.run(["powershell", "-Command", cmd], capture_output=True).stdout
    file_checksum = str(file_checksum).lower().split()[1]

    original_checksum = original_checksum.lower()

    if original_checksum in file_checksum:
        print("*"*10, "Valid Checksum", "*"*10)
    else:
        print("!"*10, "Checksum Mismath", "!"*10)
    print(f"Original:\t{original_checksum}\nFilesum:\t{file_checksum}")


if __name__ == '__main__':
    checksum(args.p, args.a, args.cs)
