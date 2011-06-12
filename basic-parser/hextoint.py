import sys, struct
""" Very basic convert hex to integer script. 
	Pass the hex as a non delimited string. e.g. "ce0f0b00" 
"""

def main(argv):
	raw_hex = argv[0]
	print int(struct.unpack_from('i', raw_hex)[0])

if __name__ == "__main__":
	main(sys.argv[1:])