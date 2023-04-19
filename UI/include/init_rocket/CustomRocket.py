import numpy as np
import include.init_rocket.mesh.mesh_creation as mc
from include.init_rocket.mesh.Solid import Solid

class CustomRocket:
    '''
    Class representing the physical rocket.

    Attributes:
        nose (Solid): Nose mesh and the density of its material.
        body (Solid): Body mesh and the density of its material.
        fins (Solid): Fins mesh and the density of their material.
        booster (Solid): The booster of the rocket.
        additional_mass (list(Solid)): List of dict containing mesh for additional masses and their density.
        textures (list): List of string giving the texture of each component of the rocket.
        component_number (int): The number of individual component.
    '''
    def __init__(self, nose, body, fins, booster, additional_mass=[], textures=[None for _ in range(5)]) -> None:
        self.nose = nose
        self.body = body
        self.fins = fins
        self.booster = booster
        self.additional_mass = additional_mass
        self.textures = textures
        self.component_number = 5 + len(additional_mass)
    
    @classmethod
    def fromDict(cls, dict):
        '''
        Create MyRocket from a dict containing the informations for the desired rocket.
        THE DICT MUST BE OF THE RIGHT FORMAT AND CONTAIN ALL KEYS.
        (see the user_interface for more informations about the format of the dict.)
        '''
        nose = mc.nose(shape_function = dict['nose_type'],
                       radius=dict['nose_radius'],
                       length = dict['nose_length'],
                       curve_param = dict['nose_parameter'],
                       thick = dict['nose_thickness'],
                       pos=dict['tube_length'],
                       density = dict['nose_density'])
        body = mc.empty_cylinder(outer_radius = dict['tube_radius'],
                                 inner_radius = dict['tube_radius']-dict['tube_thickness'],
                                 height = dict['tube_length'],
                                 density= dict['tube_density'])
        fins = mc.fins(Cr=dict['fins_Cr'],
                       Ct=dict['fins_Ct'],
                       Xt=dict['fins_Xt'],
                       s=dict['fins_s'],
                       thick=dict['fins_thickness'],
                       fnum=dict['fins_number'],
                       radius=dict['tube_radius'],
                       pos=dict['fins_position'],
                       density = dict['fins_density'])
        motor = dict['motor']
        mass = motor['propWeightG']*1e-3 #conversion of g in kg
        volume = np.pi*(motor['diameter']*1e-3/2)**2*(motor['length']*1e-3) #conversion of mm^3 in m^3
        density = mass/volume
        booster = mc.cylinder(radius = motor['diameter']*1e-3/2,
                              height = motor['length']*1e-3,
                              pos = dict['motor_position'],
                              density=density)
        
        textures = [dict['nose_material'], dict['tube_material'], dict['fins_material'], 'motor']

        if dict['motor_ring']:
            motor_ring = mc.empty_cylinder(outer_radius = dict['tube_radius'] - dict['tube_thickness'],
                                           inner_radius = motor['diameter']*1e-3/2,
                                           height = motor['length']*1e-3,
                                           pos = dict['motor_position'],
                                           density = dict['motor_ring_density'])
            additional_mass = [motor_ring]
            textures.append(dict['motor_ring_material'])
        else:
            additional_mass = []
        mass_list = dict['additional_masses']
        for i in range(len(mass_list)):
            current_mass = mass_list[i]
            if current_mass['type'] == 'cylinder':
                mass = mc.cylinder(radius = current_mass['outer_radius'],
                                   height = current_mass['length'],
                                   pos = current_mass['position'],
                                   density = current_mass['density'])
            else:
                mass = mc.empty_cylinder(outer_radius = current_mass['outer_radius'],
                                         inner_radius = current_mass['inner_radius'],
                                         height = current_mass['length'],
                                         pos = current_mass['position'],
                                         density = current_mass['density'])
            additional_mass.append(mass)
            textures.append(current_mass['material'])

        return cls(nose,body,fins,booster,additional_mass,textures)


    def set_textures(self,textures):
        '''
        Textures setter.
        '''
        assert len(textures) == len(self.component_number), "Textures list must be the same length as the number of component of your rocket. Enter None for unknown textures."
        self.textures = textures


    def show(self, method = 'mpl', opened=True, only_ext = True):
        '''
        Plot the plotting mesh of the rocket and return the rocket.
        Args:
            all (boolean): Specifies if only the plotting part (opened rocket)is plotted or not.
        '''
        valid_methods = ['mpl', 'go']  # predefined list of valid strings
        assert method in valid_methods, f"Invalid shape function. Valid options are: {', '.join(valid_methods)}"

        rocket = self.build(only_ext = only_ext)
        rocket.show(method=method, opened=opened)


    def asList(self, only_ext = False):
        '''
        Return the rocket as a list of its solid components.
        '''
        ls = [self.nose, self.body, self.fins, self.booster]
        ls += self.additional_mass
        return ls[:3] if only_ext else ls


    def build(self, only_ext=True):
        '''
        Build the rocket into a unique solid. Only build the exterior of the rocket if only_ext is True.
        '''
        return Solid.combine(self.asList(only_ext))


    def get_cog(self):
        '''
        Return the center of gravity (cog) of the rocket.
        '''
        rocket = self.asList()
        cog, mass = np.zeros(3), 0.
        for component in rocket:
            _, vmass, vcog, __ = component.stl_mesh.get_mass_properties_with_density(component.density)
            cog += vmass*vcog
            mass += vmass
        cog/=mass
        cog[cog<1e-6]=0. # micrometric precision on the cog
        return cog


    def get_mass_properties(self):
        '''
        Get mass properties of the rocket (volume, mass, cog, inertia).
        '''
        cog = self.get_cog()
        inertia = np.zeros((3,3))
        mass = 0.
        volume = 0.
        rocket = self.asList()

        for component in rocket:
            tvolume, tmass, tinertia = component.get_inertia_wrt(cog)

            volume += tvolume
            mass += tmass
            inertia += tinertia

        inertia[inertia<1e-6]=0.

        return volume, mass, cog, inertia
    
    def print_mass_properties(self):
        '''
        Print and return mass properties.
        '''
        volume, mass, cog, inertia = self.get_mass_properties()
        print("Volume (m^3)                                 = {0}".format(volume))
        print("Mass   (kg)                                  = {0}".format(mass))
        print("\n")
        print("Position of the center of gravity (COG)      = {0}".format(cog))
        print("\n")
        print("Inertia matrix expressed at the COG (kg*m^2) = {0}".format(inertia[0,:]))
        print("                                               {0}".format(inertia[1,:]))
        print("                                               {0}".format(inertia[2,:]))

        return volume, mass, cog, inertia