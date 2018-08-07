from scapy.all import *
from unis import Runtime
from unis.models import *

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

        if host_rt == None:
            self.host_rt = Runtime("http://iu-ps01.osris.org:8888", name = "host")
        else:
            self.host_rt = host_rt

        if remote_rt == None:
            self.remote_rt = Runtime("http://iu-ps01.osris.org:8888", name = "remote")
        else:
            self.host_rt = remote_rt

        self.tc = Traceroute()
        
        return
    
    '''
        @param:pattern:string - string of a node name search pattern you are looking for in each domain.

        The nodes retrieved from this setup phase will be used as targets for traceroute and pathing.
    '''
    def _setup(self, pattern):
        # get the local domain, this is the 'source'
        host_domain = self.host_rt.domains[0]
        
        target_domains = self.remote_rt.topologies[0].domains
        target_nodes   = []
        
        #
        # This mess is to handle when a resource can't be resolved. 
        # Only an issue because we are navigating resources in multiple
        # Runtimes on the fly. 
        #
        for d in range(len(target_domains)):
            try:
                current_domain = target_domains[d]    
            except:
                continue
            for n in range(len(current_domain.nodes)):
                try:
                    current_node = current_domain.nodes[n]
                    if pattern in current_node.name:
                        target_nodes.append(current_node)
                except:
                    continue

        return target_nodes

    ''' 
        @param:node:UNISNode

        takes a valid Node retrieved in self._setup method and uses traceroute to get the hops to it.
    '''
    def trace_path(self, node):
        try:
            hops = self.tc.trace(node.properties.mgmtaddr)
        except Exception as e:
            print("Exception: ", e.__traceback__)
            print("Unable to reach IP address of node: " + node.name + " - " + node.properties.mgmtaddr)
        return hops

if __name__ == '__main__':
       tcm = Traceroute_Manager()
       target_nodes = tcm._setup("virt")
       for node in target_nodes:
           print(node.to_JSON())
           hops = tcm.trace_path(node)
           print(hops)
