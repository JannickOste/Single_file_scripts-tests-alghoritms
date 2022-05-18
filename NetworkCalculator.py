from ctypes import Union
from ctypes.wintypes import CHAR
import math
import re, os, itertools

# Most calculations output: class C networks, convert these as you go.
# Made while studying for networking.

def __clearScreen(): 
    os.system("clear")

def __binaryToDecimal(binaryStr) -> int: 
    if re.match("^[01]+$", binaryStr) is None:
        raise "invalid binary str"

    sum: int = 0
    for i in range(0, len(binaryStr)):
        current: CHAR = binaryStr[i]
        if current == '1':
            sum += math.pow(2, len(binaryStr)-1-i)

    return math.floor(sum)

def __decimalToBinary(num):
    current = ""
    while(num > 0):
        current += str(num%2)
        num = math.floor(num/2)

    return current[::-1]

def __getBinaryIPAddr():
    error = ""
    while True:
        __clearScreen()
        print(error)
        binaryIp = input("Enter an binary IP address (leave open to exit): ")

        if len(binaryIp) == 0: 
            return None
        elif re.match("[01]{8}.[01]{8}.[01]{8}.[01]{8}", binaryIp) is None:
            error = "Invalid ip structure"
        else: return binaryIp 
    

def __getDecimalIPv4Addr():
    error = ""
    while True:
        __clearScreen()
        print(error)
        binaryIp = input("Enter a IPv4 address (leave open to exit): ")

        if len(binaryIp) == 0: 
            return None
        elif re.match("[0-9]+.[0-9]+.[0-9]+.[0-9]+", binaryIp) is None:
            error = "Invalid ip structure"
        else: return binaryIp 

def __getIPv6Addr():
    error = ""
    while True:
        __clearScreen()
        if len(error):
            print(error)
        binaryIp = input("Enter an IPv6 address (leave open to exit): ")

        if len(binaryIp) == 0: 
            return None
        elif re.match("^[0-9A-F]{4}.[0-9A-F]{4}.[0-9A-F]{4}.[0-9A-F]{4}.[0-9A-F]{4}.[0-9A-F]{4}.[0-9A-F]{4}.[0-9A-F]{4}", binaryIp) is None:
            error = "Invalid ip structure"
        else: return binaryIp 
    

def ToDecimalIPAddr() -> str:
    """
        Convert a binary address to a decimal IP address.
    """
    binaryIp = __getBinaryIPAddr()
    if binaryIp is None: 
        return

    output: str = ""
    slices: Union = [i[::-1] for i in binaryIp.split(".")]
    for i in range(0, len(slices)):
        output += "{0}{1}".format(__binaryToDecimal(slices[i]), '.' if i != len(slices)-1 else '')
    
    print("Decimal address: "+output)


def ToBinaryIPAddr() -> str:
    __clearScreen()
    ipAddr = __getDecimalIPv4Addr()
    if ipAddr:
        """
            Convert an IP address to a binary IP address
        """
        slices: Union = ipAddr.split(".")
        output: str = ""
        for i in range(0, len(slices)):
            slice = slices[i]
            num: int = int(slice)
            current: str = ""
            while(num > 0):
                current += str(num%2)
                num = math.floor(num/2)
            
            output += "{0}{1}".format(current[::-1] if len(current) == 8 else ("0"*(8-len(current)))+current, '.' if i != len(slices)-1 else '')
        
        print("Binary address: "+output)


def ShorthandToSubnetmask(ipAddr = "") -> str: 
    error = ""
    while not len(ipAddr): 
        __clearScreen()
        if len(error):
            print(error)
        ipAddr = input("Enter a decimal IP address with a shorthand mask (ex: 192.168.0.1/24): ")
        
        """
            Generate binary mask from ipAddr 
        """
        if re.match("[0-9]+.[0-9]+.[0-9]+.[0-9]+\/[0-9]+", ipAddr) is None:
            error = "Wrong ip notation"
            ipAddr = ""
        else: 
            break
        
    bitCount: int = int(ipAddr.split("/")[-1])
    output = ""
    for i in range(0, 4):
        current = ""
        for j in range(0, 8):
            current += "1" if bitCount > 0 else "0"
            bitCount -= 1
        output += "{0}{1}".format(current, "." if i != 3 else "")

    print("Binary mask: "+output)
    print("subnetmask: "+".".join([str(__binaryToDecimal(i)) for i in output.split(".")]))


def NetworkIdIdentifier() -> None: 
    binaryIp = __getBinaryIPAddr()
    if binaryIp is None: 
        return

    print(binaryIp)
    print("-"*(binaryIp.index("0") if binaryIp[binaryIp.index("0")-1] != "." else binaryIp.index("0")-1))
    if binaryIp.index("0") > len("Network ID"):
        print((" "*int((binaryIp.index("0")/2)-len("Network ID")/2))+"Network ID")
    else:
        print("Network ID")
    

def HostIdIdentifier() -> None: 
    binaryMask = __getBinaryIPAddr()
    if binaryMask is None:
        return

    print(binaryMask)
    print(" "*(len(binaryMask)-binaryMask[::-1].index("1"))+"-"*binaryMask[::-1].index("1"))
    print(" "*(len(binaryMask)-binaryMask[::-1].index("1"))+"Host ID")


def NetworkClassIdentifier() -> None: 
    ipAddr = __getBinaryIPAddr()
    if ipAddr is None:
        return

    privateRange = None
    netClass = None
    modifier = 0
    if re.match("[01]{8}.[01]{8}.[01]{8}.[01]{8}", ipAddr) is not None:
        firstSliceDecimal = __binaryToDecimal(ipAddr.split(".")[0])
        if firstSliceDecimal <= 126:
            netClass = 'A'
            privateRange = "10.0.0.0"
        elif firstSliceDecimal <= 191:
            netClass = 'B'
            privateRange = "172.16.0.0 - 172.31.0.0"
        else: 
            netClass = 'C'
            privateRange = "192.168.0.0 - 192.168.255.0"
        # D/E not implemented due not required for studies.

        modifier = (ord(netClass)-ord('A'))+1

    print("Network class {0}\n- Allowed hosts: {1}\n- Network bits: {2}\n- Private (free) range: {3}\n- Network mask: {4}".format(
        netClass, 
        math.floor(math.pow(2, 8*(modifier))-2),
        7*(modifier),
        privateRange,
        ".".join(["255" if i <= modifier-1 else "0" for i in range(0, 4)])
    ))

def HostsToSubnetmask(): 
    error = ""
    while True: 
        __clearScreen()
        if len(error):
            print(error)

        try:
            hosts = int(input("Hosts in network: "))
            hosts += 2
            break
        except:
            error = "Invalid input"
            

    bitsRequired = 0
    while math.pow(2, bitsRequired) < hosts:
        bitsRequired += 1

    ShorthandToSubnetmask("192.168.0.1/"+str(32-bitsRequired))
    print("Possible combinations: ")
    suffix = "0"*bitsRequired
    
    for prefix in ["".join([str(j) for j in list(i)]) for i in itertools.product([0, 1], repeat=8-bitsRequired)]:
        print("\nIPAddr: 192.168.0."+str(__binaryToDecimal(prefix+suffix)))
        print("Accesibility:")
        print("\tFirst accesible:\n\t\t-> 192.168.0."+prefix+suffix[0:len(suffix)-1]+"1")
        print("\tLast accesible:\n\t\t-> 192.168.0."+prefix+suffix.replace("0", "1")[0:len(suffix)-1]+"0")
        print("\tBroadcast IP:\n\t\t-> 192.168.0."+prefix+suffix.replace("0", "1"))

def BroadcastNetworksToSubnetmasks():
    __clearScreen()
    bitsRequired = len(__decimalToBinary(int(input("broadcast domains: "))-1))
    suffix = "0"*(8-bitsRequired)
    for prefix in ["".join([str(j) for j in list(i)]) for i in itertools.product([0, 1], repeat=bitsRequired)]:
        print("\nIPAddr: 192.168.0."+prefix+suffix)
        print("IPAddr: 192.168.0."+str(__binaryToDecimal(prefix+suffix)))
        print("Accesibility:")
        print("\tFirst accesible:\n\t\t-> 192.168.0."+prefix+suffix[0:len(suffix)-1]+"1")
        print("\tLast accesible:\n\t\t-> 192.168.0."+prefix+suffix.replace("0", "1")[0:len(suffix)-1]+"0")
        print("\tBroadcast IP:\n\t\t-> 192.168.0."+prefix+suffix.replace("0", "1"))

def IPv6Analyzer(): 
    __clearScreen()
    ipAddr = __getIPv6Addr()

    if ipAddr:
        capacity = 128
        networkBits = int(ipAddr.split("/")[-1])
        hostBits = capacity-networkBits
        networkPart = ipAddr.split(":")[0:math.floor((networkBits/16))]
        hostPart = [i.split("/")[0] for i in ipAddr.split(":")[math.floor((networkBits/16))::]]

        print("IPv6 addr: {0}\nNetwork bits: {1}\nHost bits: {2}\nNetwork part: {3}\nHost part: {4}".format(ipAddr, networkBits, hostBits, ":".join(networkPart), ":".join(hostPart)))

                    
def Menu():
    header = "Network tool by Oste Jannick"
    while True:
        __clearScreen()

        print("#"*(len(header)+4)+"\n# "+header+" #\n"+"#"*(len(header)+4))
        entries = {
            "Convert binary IP address to decimal" : ToDecimalIPAddr,
            "Convert decimal IP address to binary" : ToBinaryIPAddr,
            "Identify network ID in binary IP address": NetworkIdIdentifier,
            "Identify Host ID in binary IP address" : HostIdIdentifier,
            "Identify network class using binary IP address": NetworkClassIdentifier,
            "Convert shorthand mask to binary mask":ShorthandToSubnetmask,
            "Generate subnetmasks based on hosts in network":HostsToSubnetmask,
            "Generate subnetmasks based on required broadcast domains":BroadcastNetworksToSubnetmasks,
            "Analyze IPv6 address":IPv6Analyzer
        }

        for i, key in enumerate(entries):
            print("{0}. {1}".format(i, key))

        targetIndex = input("\n# ")
        if re.match("^[0-9]+$", targetIndex) is not None and int(targetIndex) < len(entries):
            entries[list(entries)[int(targetIndex)]]()
            _ = input("Press enter to go back to the main menu...")
        
Menu()
