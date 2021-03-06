import os
import argparse
import subprocess



# create parser and arguments
parser = argparse.ArgumentParser()
parser._action_groups.pop()

# required arguments (positional)
required = parser.add_argument_group("required arguments")
required.add_argument("path", help="File path", type=str, nargs=1)
required.add_argument("valid", help="Valid hash", type=str, nargs=1)

# optional arguments
optional = parser.add_argument_group("optional arguments")
optional.add_argument("-a", "--algo", help="Algorithm to be used", dest="algorithm", type=str, required=True, default="SHA256")
optional.add_argument("-s", "--show", help="View comparison of hashes (true, t, y)", dest="show_hashes", type=str)

# get arguments
args = parser.parse_args()



def show_hashes(valid, file):
    """
    Prints checksums

    Args:
        valid (str): Valid checksum
        file (str): File checksum
    """
    print(f"Original:\t{valid}\nFilehash:\t{file}\n")



def checksum(file_path, valid_hash, algorithm="SHA256", compare=False):
    """
    Uses Powershell to check the validity of a file's checksum
    
    Args:
        file_path (path): Path of file to be checked
        algorithm (string): Name of hashing algorithm to be used. Options: SHA1, SHA256, SHA384, SHA512, and MD5.
        original_checksum (string): File hash as provided by author(s) / organisation
    """
    
    # prepare Powershell command, return only line with algorithm, hash, and filepath
    cmd = f"Get-FileHash -Path {file_path} -Algorithm {algorithm} | findstr '{algorithm}'"
    
    # get output of command
    file_hash = subprocess.run(["powershell", "-Command", cmd], capture_output=True).stdout
    
    # extract hash as lowercase string from the output, drops algorithm and filepath
    file_hash = str(file_hash).lower().split()[1]
    
    # get lowercase hash of valid checksum
    valid_hash = valid_hash.lower()
    
    # compare and output result
    if valid_hash == file_hash:
        print("\n" + "*"*10, "CHECKSUM PASSED", "*"*10)
        # only print if requested
        if compare: show_hashes(valid_hash, file_hash)
        else: print()

    else:
        print("\n" + "#"*10, "ALERT! CHECKSUM FAILED", "#"*10)
        # print for manual overview
        show_hashes(valid_hash, file_hash)
    
    
    return file_hash, valid_hash




if __name__ == '__main__':

    if os.path.isfile(args.path[0]):

        print("""
        WARNING! This script doesn't check the validity of the hash you submit, it only compares it to the file hash. 
        Ensure the hash provided is valid (sourced from author/organisation of the file).""")
        
        # convert string to boolean
        show = True if args.show_hashes.lower() in ['true', 't', 'y'] else False
        
        # call validator function
        checksum(file_path=args.path[0],
                        valid_hash=args.valid[0],
                        algorithm=args.algorithm,
                        compare=show)

    else:
        raise FileNotFoundError("The first argument must be the file path.")
