from scapy.all import *

class Traceroute:
    def __init__(self, host=None):
        self.host = host
        return

    def trace(self, target):
        # Traceroute with Scapy
        ans, unans = traceroute(target, verbose=False)
        
        hops = [{'ttl':snd.ttl, 'ip':rcv.src} for snd, rcv in ans]

        return hops

class Traceroute_Manager:

    def __init__(self, host_rt=None, remote_rt=None):

        self.host_rt = Runtime("http://iu-ps01.osris.org:8888") if host_rt is None else self.host_rt = host_rt
        self.remote_rt = Runtime("http://iu-ps01.osris.org:8888") if remote_rt is None else self.remote_rt = remote_rt
        return
    
    def _setup(self):

        host_domain = self.rt.domains[0]
        


if __name__ == '__main__':
    tc = Traceroute("wsu-sdn01-be.osris.org")
    hops = tc.trace(tc.host)
    print(hops)
        
