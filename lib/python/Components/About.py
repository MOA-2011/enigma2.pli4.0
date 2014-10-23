import sys
import os
import time
from Tools.HardwareInfo import HardwareInfo

def getVersionString():
	return getImageVersionString()

def getImageVersionString():
	try:
		if os.path.isfile('/var/lib/opkg/status'):
			st = os.stat('/var/lib/opkg/status')
		else:
			st = os.stat('/usr/lib/ipkg/status')
		tm = time.localtime(st.st_mtime)
		if tm.tm_year >= 2011:
			# [ IQON : by LeeWS : %Y-%m-%d -> %m-%d-%Y
			return time.strftime("%m-%d-%Y %H:%M:%S", tm)
			# IQON ] : by LeeWS
	except:
		pass
	return _("unavailable")

def getEnigmaVersionString():
	import enigma
	enigma_version = enigma.getEnigmaVersionString()
	if '-(no branch)' in enigma_version:
		enigma_version = enigma_version [:-12]
	# [ IQON : by LeeWS : return enigma_version is replaced to below 2 lines.
		list = enigma_version.split("-")
	return list[1] + "-" + list[2] + "-" + list[0]
	# IQON ] : by LeeWS

def getKernelVersionString():
	try:
		return open("/proc/version","r").read().split(' ', 4)[2].split('-',2)[0]
	except:
		return _("unknown")

def getHardwareTypeString():
	return HardwareInfo().get_device_string()

def getBrandString():
	try:
		return open("/etc/.brandtype","r").read()
	except:
		return _("unknown")

# [ IQON : by knuth
def getHardwareModelString():
	try:
		if getBrandString() == "technomate":
			if open("/proc/stb/info/hwmodel","r").read() in ("force1plus"):
				model = "TM-NANO-3T COMBO"
				return getBrandString().capacity() + model
		elif getBrandString() == "edision":
			if open("/proc/stb/info/hwmodel","r").read() in ("force1plus"):
				model = "OPTIMUSS OS3+"
				return getBrandString().capitalize() + model
		else:
			return open("/proc/stb/info/modelname","r").read()
	except:
		return _("unknown")

def getMacAddressString(ifname):
	import fcntl, socket, struct
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
	return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def getMicomVersionString():
	try:
		import fcntl, array
		f = array.array('h', [0])
		fp = open('/dev/dbox/fp0', 'w')
		fcntl.ioctl(fp.fileno(), 0x428, f, 1)
		return '%s' % f.tolist()[0]
	except:
		return _("unknown")
# IQON] : by knuth

def getImageTypeString():
	try:
		return open("/etc/issue").readlines()[-2].capitalize().strip()[:-6]
	except:
		pass
	return _("undefined")

# For modules that do "from About import about"
about = sys.modules[__name__]
