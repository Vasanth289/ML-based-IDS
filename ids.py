import sys
import os
import time

if len(sys.argv) == 2:
	path = sys.argv[1]

elif len(sys.argv) == 5 and sys.argv[2] == "live":
	path = sys.argv[1]
	os.system("touch " + path)
	os.system("chmod o=rw " + path)
	os.system("sudo tshark -i " + sys.argv[4] + " -c" + sys.argv[3] + " -w " + path)
	
else:
	print("\tusage: {} <capture_file>".format(sys.argv[0]))
	print("\tusage: {} <output_file> live count iface".format(sys.argv[0]))
	exit(1)

os.system("zeek -r " + path + " darpa2gurekddcup.bro > conn.list")
os.system("sort -n conn.list > conn_sort.list")
os.system("gcc trafAld.c -o trafAld")
os.system("./trafAld conn_sort.list")

filename = path.split('/')[1]
filename = filename.split('.')[0]

os.system("cp trafAld.list lists/" + filename + ".list")

os.system("python3 catmodel.py lists/" + filename + ".list")

f = open("ip.list", "r")

for ip in f.readlines():
	ip = ip.replace('\n', '')
	os.system("sudo iptables -A INPUT -s " + ip + " -j REJECT")
