from time import time
from simpleping import isup

f=open("ips.txt","r")

start = time()
for ip in f:
	ip = ip.strip()
	print(ip,isup(ip))
end = time()
print(end - start)

f.close()
