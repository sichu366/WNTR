from nose.tools import *
from os.path import abspath, dirname, join
import numpy as np
import wntr

testdir = dirname(abspath(str(__file__)))
datadir = join(testdir,'networks_for_testing')
net1dir = join(testdir,'..','..','examples','networks')

def test_terminal_nodes():
    inp_file = join(net1dir,'Net1.inp')
    parser = wntr.epanet.InpFile()
    wn = parser.read(inp_file)

    G = wn.get_graph()
    terminal_nodes = G.terminal_nodes()
    expected_nodes = set(['2', '9'])
    assert_set_equal(set(terminal_nodes), expected_nodes)

def test_Net1_MultiDiGraph():
    inp_file = join(net1dir,'Net1.inp')
    parser = wntr.epanet.InpFile()
    wn = parser.read(inp_file)
    G = wn.get_graph()

    node = {'11': {'pos': (30.0, 70.0),'type': 'Junction'},
            '10': {'pos': (20.0, 70.0),'type': 'Junction'},
            '13': {'pos': (70.0, 70.0),'type': 'Junction'},
            '12': {'pos': (50.0, 70.0),'type': 'Junction'},
            '21': {'pos': (30.0, 40.0),'type': 'Junction'},
            '22': {'pos': (50.0, 40.0),'type': 'Junction'},
            '23': {'pos': (70.0, 40.0),'type': 'Junction'},
            '32': {'pos': (50.0, 10.0),'type': 'Junction'},
            '31': {'pos': (30.0, 10.0),'type': 'Junction'},
            '2':  {'pos': (50.0, 90.0),'type': 'Tank'},
            '9':  {'pos': (10.0, 70.0),'type': 'Reservoir'}}

    edge = {'11': {'12': {'11':  {'type': 'Pipe'}},
                   '21': {'111': {'type': 'Pipe'}}},
            '10': {'11': {'10':  {'type': 'Pipe'}}},
            '13': {'23': {'113': {'type': 'Pipe'}}},
            '12': {'13': {'12':  {'type': 'Pipe'}},
                   '22': {'112': {'type': 'Pipe'}}},
            '21': {'31': {'121': {'type': 'Pipe'}},
                   '22': {'21':  {'type': 'Pipe'}}},
            '22': {'32': {'122': {'type': 'Pipe'}},
                   '23': {'22':  {'type': 'Pipe'}}},
            '23': {},
            '32': {},
            '31': {'32': {'31':  {'type': 'Pipe'}}},
            '2':  {'12': {'110': {'type': 'Pipe'}}},
            '9':  {'10': {'9':   {'type': 'Pump'}}}}

    assert_dict_contains_subset(node, G.node)
    assert_dict_contains_subset(edge, G.adj)

if __name__ == '__main__':
    test_Net1()
