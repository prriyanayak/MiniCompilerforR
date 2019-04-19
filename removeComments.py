import sys
import re
def main():
	#print("Enter the name of the Source file to compile")
	filename='ex.r'
	#print("Enter the name of the destination file")
	filename1='ex1.r'
	finalcode = ''
	with open(filename, 'r') as f:
		for line in f:
			i = 0
			while i < len(line)-1:
				ch = line[i]
				if ch=='\n':
					break
				if ch == '#':
					break

				finalcode += ch
				i+=1
			finalcode += line[len(line)-1]
	finalcode = re.sub(r'\n+', '\n', finalcode).strip()               #removes extra lines from the i/p file
	with open(filename1, 'w') as f:
		f.write(finalcode)


if __name__ == '__main__':
	main()
