import sys
import subprocess
def isup(ip):
	myos = sys.platform
	if myos == 'darwin':
		result = subprocess.run(["ping", "-c", "2", ip],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	else:
		result = subprocess.run(["ping", "-n", "2", ip],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	return not result.returncode