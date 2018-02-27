# These tests run a demand-driven simulation with both WNTR and Epanet and compare the results for the example networks
import unittest
from os.path import abspath, dirname, join
import pandas as pd
import pickle

testdir = dirname(abspath(str(__file__)))
test_datadir = join(testdir,'networks_for_testing')
ex_datadir = join(testdir,'..','..','examples','networks')

class TestResetInitialValues(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        import wntr
        self.wntr = wntr

        inp_file = join(ex_datadir, 'Net3.inp')
        self.wn = self.wntr.network.WaterNetworkModel(inp_file)
        self.wn.options.time.hydraulic_timestep = 3600
        self.wn.options.time.duration = 24*3600

        sim = self.wntr.sim.WNTRSimulator(self.wn)
        self.res1 = sim.run_sim(solver_options={'TOL':1e-8})

        self.wn.reset_initial_values()
        self.res2 = sim.run_sim(solver_options={'TOL':1e-8})

    @classmethod
    def tearDownClass(self):
        pass

    def test_link_flowrate(self):
        for link_name, link in self.wn.links():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.link['flowrate'].loc[t,link_name], self.res2.link['flowrate'].loc[t,link_name], 7)

    def test_link_velocity(self):
        for link_name, link in self.wn.links():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.link['velocity'].loc[t,link_name], self.res2.link['velocity'].loc[t,link_name], 7)

    def test_node_demand(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['demand'].loc[t,node_name], self.res2.node['demand'].loc[t,node_name], 7)

    def test_node_expected_demand(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['expected_demand'].loc[t,node_name], self.res2.node['expected_demand'].loc[t,node_name], 7)

    def test_node_head(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['head'].loc[t,node_name], self.res2.node['head'].loc[t,node_name], 7)

    def test_node_pressure(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['pressure'].loc[t,node_name], self.res2.node['pressure'].loc[t,node_name], 7)

class TestStopStartSim(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        import wntr
        self.wntr = wntr

        inp_file = join(ex_datadir, 'Net3.inp')

        parser = self.wntr.epanet.InpFile()
        self.wn = parser.read(inp_file)
        self.wn.options.time.hydraulic_timestep = 3600
        self.wn.options.time.duration = 24*3600
        sim = self.wntr.sim.WNTRSimulator(self.wn)
        self.res1 = sim.run_sim(solver_options={'TOL':1e-8})

        parser = self.wntr.epanet.InpFile()
        self.wn = parser.read(inp_file)
        self.wn.options.time.hydraulic_timestep = 3600
        self.wn.options.time.duration = 10*3600
        sim = self.wntr.sim.WNTRSimulator(self.wn)
        self.res2 = sim.run_sim(solver_options={'TOL':1e-8})
        self.wn.options.time.duration = 24*3600
        self.res3 = sim.run_sim(solver_options={'TOL':1e-8})

        node_res = pd.concat([self.res2.node,self.res3.node],axis=1)
        link_res = pd.concat([self.res2.link,self.res3.link],axis=1)
        self.res2.node = node_res
        self.res2.link = link_res

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_link_flowrate(self):
        for link_name, link in self.wn.links():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.link['flowrate'].loc[t,link_name], self.res2.link['flowrate'].loc[t,link_name], 7)

    def test_link_velocity(self):
        for link_name, link in self.wn.links():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.link['velocity'].loc[t,link_name], self.res2.link['velocity'].loc[t,link_name], 7)

    def test_node_demand(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['demand'].loc[t,node_name], self.res2.node['demand'].loc[t,node_name], 7)

    @unittest.SkipTest
    def test_node_expected_demand(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['expected_demand'].loc[t,node_name], self.res2.node['expected_demand'].loc[t,node_name], 7)

    def test_node_head(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['head'].loc[t,node_name], self.res2.node['head'].loc[t,node_name], 7)

    def test_node_pressure(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['pressure'].loc[t,node_name], self.res2.node['pressure'].loc[t,node_name], 7)

class TestPickle(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        import wntr
        self.wntr = wntr

        inp_file = join(ex_datadir, 'Net3.inp')

        parser = self.wntr.epanet.InpFile()
        self.wn = parser.read(inp_file)
        self.wn.options.time.hydraulic_timestep = 3600
        self.wn.options.time.duration = 24*3600
        sim = self.wntr.sim.WNTRSimulator(self.wn)
        self.res1 = sim.run_sim(solver_options={'TOL':1e-8})

        parser = self.wntr.epanet.InpFile()
        self.wn = parser.read(inp_file)
        self.wn.options.time.hydraulic_timestep = 3600
        self.wn.options.time.duration = 10*3600
        sim = self.wntr.sim.WNTRSimulator(self.wn)
        self.res2 = sim.run_sim(solver_options={'TOL':1e-8})
        f=open('pickle_test.pickle','wb')
        pickle.dump(self.wn,f)
        f.close()
        f=open('pickle_test.pickle','rb')
        wn2 = pickle.load(f)
        f.close()
        wn2.options.time.duration = 24*3600
        sim = self.wntr.sim.WNTRSimulator(wn2)
        self.res3 = sim.run_sim(solver_options={'TOL':1e-8})

        node_res = pd.concat([self.res2.node,self.res3.node],axis=1)
        link_res = pd.concat([self.res2.link,self.res3.link],axis=1)
        self.res2.node = node_res
        self.res2.link = link_res

    @classmethod
    def tearDownClass(self):
        pass

        
    def test_link_flowrate(self):
        for link_name, link in self.wn.links():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.link['flowrate'].loc[t,link_name], self.res2.link['flowrate'].loc[t,link_name], 7)

    def test_link_velocity(self):
        for link_name, link in self.wn.links():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.link['velocity'].loc[t,link_name], self.res2.link['velocity'].loc[t,link_name], 7)

    def test_node_demand(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['demand'].loc[t,node_name], self.res2.node['demand'].loc[t,node_name], 7)

    @unittest.SkipTest
    def test_node_expected_demand(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['expected_demand'].loc[t,node_name], self.res2.node['expected_demand'].loc[t,node_name], 7)

    def test_node_head(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['head'].loc[t,node_name], self.res2.node['head'].loc[t,node_name], 7)

    def test_node_pressure(self):
        for node_name, node in self.wn.nodes():
            for t in self.res1.time:
                self.assertAlmostEqual(self.res1.node['pressure'].loc[t,node_name], self.res2.node['pressure'].loc[t,node_name], 7)

if __name__ == '__main__':
    unittest.main()
