from cosapp.base import System, Port, BaseConnector

import numpy as np

from Utility import thrust, aeroCoefs

##########################################################################
# Below is the Earth system composed of the Dynamic and the Rocket systems


class Earth(System):
    
    def setup(self):

        self.add_child(Rocket('Rocket'), pulling = ["v", "m", 
                                                    #"Fp", "Fa"
                                                    ]) 
        
        self.add_child(Dynamics('Dyn'), pulling = {"a" : "a", "aw" : "aw", 
                                                #    "Fp" : "Fp_Earth", 
                                                #    "Fa" : "Fa_Earth"
                                                   })

        # self.add_child(Atmosphere('Atm'), pulling = ["rhosol", "Psol", "Hp", "Hd"])

        self.connect(self.Dyn, self.Rocket, ["m", "I", "Mp", "Ma", "Fa", "Fp"]) # Output in Rocket and input in Dynamics

        self.add_transient('vEarth', der = 'a', desc = "Rocket velocity")
        self.add_transient('r', der = 'vEarth', desc = "Rocket Position")
        self.add_transient('w', der = 'aw', desc = "Rocket Angular velocity")
        self.add_transient('theta', der = 'w', desc = "Rocket Angular Position")

        self.exec_order = ['Rocket', 'Dyn']

        # self.exec_order = ['Atmo', 'Rocket', 'Dyn']
    
    def compute(self):
        # We need v to be an inward in order to be a transient, thus we add a variable vEarth
        self.v.vector = self.vEarth
        # self.Fp_Earth.vector = self.Fp.vector
        # self.Fa_Earth.vector = self.Fa.vector



##########


class Dynamics(System):
    
    def setup(self):
        
        #Thrust inputs
        self.add_input(ReferentialPort, 'Fp') # desc = "Thrust Force"
        self.add_inward('Mp', np.zeros(2), desc = "Thrust Moment")

        #Aerodynamic inputs
        self.add_input(ReferentialPort, 'Fa') # desc = "Aerodynamic Force"
        self.add_inward('Ma', 0., desc = "Aerodynamic Moment")

        #Mass inputs
        self.add_inward('m', 1., desc = "Rocket Mass")
        self.add_inward('I', 1.475e-3, desc = "Moment of Inertia")

        #Gravity inputs
        self.add_inward('g', np.array([0, -9.8]), desc = "Gravity")

        #Trajectory Outputs
        self.add_outward('a', np.zeros(2), desc = "Rocket Acceleration")
        self.add_outward('aw', 0., desc = "Rocket Angular Acceleration")
    
        
    def compute(self):

        self.a = (self.Fp.vector + self.Fa.vector) / self.m + self.g
        self.aw = (self.Ma + self.Mp) / self.I

        print(f'{self.Fp=}')
        print(f'{self.Fa=}')
        print(f'{self.a=}')
        print(f'{self.m=}')


##########################################################################################
# Below is the rocket system composed of the Aerodynamics, the Thrust and the Mass systems


class Rocket(System):
    
    def setup(self):
        self.add_input(ReferentialPort, 'v')
        self.add_output(ReferentialPort, 'Fa')
        self.add_output(ReferentialPort, 'Fp')

        self.add_child(Aerodynamics('Aero'), pulling = ["v", "Fa", "Ma"])
        self.add_child(Thrust('Thrust'), pulling= ["Fp", "Mp"])
        self.add_child(Mass('Mass'), pulling = ["m", "I"])

        self.exec_order = ['Mass', 'Aero', 'Thrust']


##########


class Aerodynamics(System):
    
    def setup(self):
        
        #Rocket inputsèè
        self.add_inward('Sref', 1.767e-2, desc = "Aerodynamic Surface of Reference")

        # self.add_inward('Cd', 1., desc = "Drag Coefficient")
        # self.add_inward('Cl', 1., desc = "Lift Coefficient")
        # self.add_inward('gf', 1., desc = "GF Distance")

        #Trajectory inputs
        self.add_input(ReferentialPort, 'v') # desc = "Rocket velocity"

        #Atmosphere inputs
        self.add_inward('rho', 1.225, desc = "Air density")

        #Aerodynamics outputs
        self.add_output(ReferentialPort, 'Fa') # desc = "Aerodynamic Force"
        self.add_outward('Ma', 0., desc = "Aerodynamic Moment")
        
    def compute(self):
        incidence = self.parent.parent.theta - np.arctan2(self.parent.parent.v.vector[1],self.parent.parent.v.vector[0]) # The y axis is the axis of the rocket and the x axis is perpendicular 
        incidence = incidence%(2*np.pi) - np.pi

        Cx, Cn, Z_CPA = aeroCoefs(incidence) # !!!!!!!!!!! The tables are supposed to be in degree
        
        self.Fa.vector = 0.5*self.rho*np.linalg.norm(self.v.vector)**2*self.Sref*np.array([Cn, Cx]) # Selon l'axe de la fusée

        G = .300
        self.Ma = self.Fa.vector[0]*(G - Z_CPA) # Bras de levier entre Le centre de masse et le centre de poussée aérodynamique


##########


class Thrust(System):
    
    def setup(self):
        
        self.add_inward('m', 1., desc = "Rocket's mass")

        #Pushing outputs
        self.add_output(ReferentialPort, 'Fp') # desc = "Thrust Force"
        self.add_outward('Mp', 0, desc = "Thrust Moment")

        self.add_transient('edfzsrqgt', der='m') # Sinon on n'a pas assez d'appels à compute... Etrange

    def compute(self):
        #the data used comes from the experimental values measured on the engine used by X20
        #Fp is a dim2 np.array
        self.Fp.vector = np.array([0, - thrust(self.time)])


##########


class Mass(System):
    
    def setup(self):
        
        #Rocket inputs
        self.add_inward('m0', 1., desc = "Rocket's Initial Mass")
        self.add_inward('I0', 1.475e-3, desc = "Rocket's Initial Inertia Moment")
        self.add_inward('m', 1., desc = "Rocket Mass")

        #Mass outputs
        self.add_outward('I', self.I0, desc = "Rocket's Inertia Moment")
        self.add_outward('Dm', 1, desc = "Rocket Mass' Rate of Change")

        #Events
        self.add_event('noMoreEngine', trigger="time >= 3.6") #voir thrust.txt

        #Transients
        self.add_transient('m', der='-Dm')
        
    def transition(self):
        if self.noMoreEngine.present:
            self.Dm = 0
        
    def compute(self):
        self.I = self.I0 * self.m/self.m0




################################################################################################
# Below is the custom Port designed to switch the vectors between earth and rocket's referential

class ReferentialPort(Port):
    """Referential Port """
    def setup(self):
        self.add_variable('vector', np.zeros(2, dtype=float))

    class Connector(BaseConnector):
        """Custom connector for `ReferentialPort` objects
        """
        def __init__(self, name: str, sink: Port, source: Port, *args, **kwargs):
            super().__init__(name, sink, source)

        def transfer(self) -> None:
            sink = self.sink # sink = destination
            source = self.source 

            ##########
            #Going from earth referential to rocket referential 

            if isinstance(source.owner, Earth) and isinstance(sink.owner, Rocket): 
                theta = source.owner.theta
                sink.vector = np.array([source.vector[1]*np.cos(theta) - source.vector[0]*np.sin(theta),
                                        - source.vector[0]*np.cos(theta) - source.vector[1]*np.sin(theta)])
                return
                                        
            if isinstance(source.owner, Dynamics) and isinstance(sink.owner, Rocket): 
                theta = source.owner.parent.theta #Earth's theta
                sink.vector = np.array([source.vector[1]*np.cos(theta) - source.vector[0]*np.sin(theta),
                                        - source.vector[0]*np.cos(theta) - source.vector[1]*np.sin(theta)])
                return

            ##########
            # Going from rocket referential to earth referential

            if isinstance(sink.owner, Earth) and isinstance(source.owner, Rocket): 
                theta = sink.owner.theta
                sink.vector = np.array([ - source.vector[1]*np.cos(theta) - source.vector[0]*np.sin(theta),
                                        source.vector[0]*np.cos(theta) - source.vector[1]*np.sin(theta)])
                return

            if isinstance(sink.owner, Dynamics) and isinstance(source.owner, Rocket): 
                theta = sink.owner.parent.theta #Earth's theta
                sink.vector = np.array([ - source.vector[1]*np.cos(theta) - source.vector[0]*np.sin(theta),
                                        source.vector[0]*np.cos(theta) - source.vector[1]*np.sin(theta)])
                return
            
            
            sink.vector = source.vector

            