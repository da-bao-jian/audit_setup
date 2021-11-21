from solidity_parser import parser
import wget
import sys
import os


def fetch_openzeppelin(filename):

	source = parser.parse_file(filename)

	for file in source['children']:

		if file['type'] == 'ImportDirective' and file['path'][:13] == "@openzeppelin":

			url = "https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master"
			file_path_split = file['path'][14:].split('/')
			
			for folder_name in file_path_split:
				if folder_name == "math":
					url += f"/utils/{folder_name}" 
				else:
					url += f"/{folder_name}" 
			
			# to get the original .sol file
			url = url.replace("github.com", "raw.githubusercontent.com", 1)
			url = url.replace("tree/", "", 1)
			
			path = os.getcwd()

			wget.download(url, out=f"{path}/contracts")

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print('Input format: python3 contracts/<contract.sol>')
		exit(-1)

	filename = sys.argv[1]
	fetch_openzeppelin(filename)