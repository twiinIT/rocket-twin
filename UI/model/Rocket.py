from cosapp.base import System

from Ports import VelPort, AclPort
from Kinematics import Kinematics
from Dynamics import Dynamics
from Thrust import Thrust
from Aerodynamics.Aerodynamics import Aerodynamics
from Mass import Mass

import numpy as np

class Rocket(System):
    
    def setup(self):
        #System orientation
        self.add_inward('Rocket_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
        
        #Gravity input
        self.add_input(AclPort, 'g')
        self.add_input(VelPort, 'v_wind')
        
        #Rocket parameters
        self.add_inward('l', 0.834664, desc='Rocket length', unit='m')
        self.add_inward('CG', self.l/2, desc='Center of Gravity', unit='m')

        #Parachute deployment
        self.add_inward_modevar('ParaDep', 0., desc = "Parachute Deployed", unit = '')
      
        #Rocket children
        self.add_child(Kinematics('Kin'), pulling = ['v_out', 'Kin_ang', 'ParaDep'])
        self.add_child(Thrust('Thrust'), pulling=['l', 'CG'])
        self.add_child(Dynamics('Dyn'), pulling = ['g', 'l', 'ParaDep', 'a_earth'])
        self.add_child(Aerodynamics('Aero'), pulling = ['l','rho', 'v_wind', 'ParaDep', 'CG'])
        self.add_child(Mass('Mass'))
        
        #Child-Child connections
        self.connect(self.Kin, self.Dyn, {'Kin_ang' : 'Dyn_ang', 'v_out' : 'v_in', 'a': 'a', 'aa' : 'aa'})
        self.connect(self.Kin, self.Aero, {'Kin_ang' : 'Aero_ang', 'v_cpa':'v_cpa', 'av_out':'av'})
        self.connect(self.Dyn, self.Aero, ['F', 'Ma'])
        self.connect(self.Thrust, self.Dyn, ['Fp', 'Mp'])
        self.connect(self.Mass, self.Dyn, {'m_out':'m', 'I':'I'})
        self.connect(self.Mass, self.Aero, {'m_out':'m'})

 
        #Execution order
        self.exec_order = ['Thrust', 'Mass', 'Aero', 'Dyn', 'Kin']
