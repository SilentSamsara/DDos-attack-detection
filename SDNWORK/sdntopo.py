from mininet.topo import Topo
class MyTopo(Topo):

    def __init__(self):

        # initilaize topology
        Topo.__init__(self)

        # add hosts and switches
        h1 = self.addHost('h1',ip='10.1.1.1')
        h2 = self.addHost('h2',ip='10.1.1.2')
        h3 = self.addHost('h3',ip='10.1.1.3')
        h4 = self.addHost('h4',ip='10.1.2.1')
        h5 = self.addHost('h5',ip='10.1.2.2')
        h6 = self.addHost('h6',ip='10.1.2.3')
	h7 = self.addHost('h7',ip='10.10.10.1')
        h8 = self.addHost('h8',ip='10.10.10.2')
        h9 = self.addHost('h9',ip='10.10.10.3')
        h10 = self.addHost('h10',ip='10.10.20.1')
        h11 = self.addHost('h11',ip='10.10.20.2')
        h12 = self.addHost('h12',ip='10.10.20.3')
        s1 = self.addSwitch('s1')
	s11 = self.addSwitch('s11')
	s12 = self.addSwitch('s12')
        s2 = self.addSwitch('s2')
	s21 = self.addSwitch('s21')
	s22 = self.addSwitch('s22')

        # add links
        self.addLink(s1,s2,3,1)
	self.addLink(s1,s11,1,3)
	self.addLink(s1,s12,2,3)
	self.addLink(s11,h1,1,1)	
	self.addLink(s11,h2,2,1)
	self.addLink(s11,h3,4,1)
	self.addLink(s12,h4,1,1)
	self.addLink(s12,h5,2,1)	
	self.addLink(s12,h6,4,1)
	self.addLink(s2,s21,2,3)
	self.addLink(s2,s22,3,3)
        self.addLink(s21,h7,1,1)
        self.addLink(s21,h8,2,1)
        self.addLink(s21,h9,4,1)
        self.addLink(s22,h10,1,1)
        self.addLink(s22,h11,2,1)
        self.addLink(s22,h12,4,1)
        
topos = {'mytopo': (lambda: MyTopo())}
