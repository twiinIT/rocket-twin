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
    def __init__(self, nose, body, fins, booster, additional_mass=[], textures=[None for _ in range(5)], dictionnary={}) -> None:
        self.nose = nose
        self.body = body
        self.fins = fins
        self.booster = booster
        self.additional_mass = additional_mass
        self.textures = textures
        self.dictionnary = dictionnary
        self.component_number = 5 + len(additional_mass)
    
    @classmethod
    def fromDict(cls, dictio):
        '''
        Create MyRocket from a dict containing the informations for the desired rocket.
        THE dict MUST BE OF THE RIGHT FORMAT AND CONTAIN ALL KEYS.
        (see the user_interface for more informations about the format of the dict.)
        '''
        nose = mc.nose(shape_function = dictio['nose_type'],
                       radius=dictio['nose_radius'],
                       length = dictio['nose_length'],
                       curve_param = dictio['nose_parameter'],
                       thick = dictio['nose_thickness'],
                       pos=dictio['tube_length'],
                       density = dictio['nose_density'])
        body = mc.empty_cylinder(outer_radius = dictio['tube_radius'],
                                 inner_radius = dictio['tube_radius']-dictio['tube_thickness'],
                                 height = dictio['tube_length'],
                                 density= dictio['tube_density'])
        fins = mc.fins(Cr=dictio['fins_Cr'],
                       Ct=dictio['fins_Ct'],
                       Xt=dictio['fins_Xt'],
                       s=dictio['fins_s'],
                       thick=dictio['fins_thickness'],
                       fnum=dictio['fins_number'],
                       radius=dictio['tube_radius'],
                       pos=dictio['fins_position'],
                       density = dictio['fins_density'])
        motor = dictio['motor']
        mass = motor['propWeightG']*1e-3 #conversion of g in kg
        volume = np.pi*(motor['diameter']*1e-3/2)**2*(motor['length']*1e-3) #conversion of mm^3 in m^3
        density = mass/volume
        booster = mc.cylinder(radius = motor['diameter']*1e-3/2,
                              height = motor['length']*1e-3,
                              pos = dictio['motor_position'],
                              density=density)
        
        textures = [dictio['nose_material'], dictio['tube_material'], dictio['fins_material'], 'motor']

        if dictio['motor_ring']:
            motor_ring = mc.empty_cylinder(outer_radius = dictio['tube_radius'] - dictio['tube_thickness'],
                                           inner_radius = motor['diameter']*1e-3/2,
                                           height = motor['length']*1e-3,
                                           pos = dictio['motor_position'],
                                           density = dictio['motor_ring_density'])
            additional_mass = [motor_ring]
            textures.append(dictio['motor_ring_material'])
        else:
            additional_mass = []
        mass_list = dictio['additional_masses']
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

        return cls(nose,body,fins,booster,additional_mass,textures,dictio)


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
        return cog, mass


    def get_mass_properties(self):
        '''
        Get calculated mass properties of the rocket (volume, mass, cog, inertia).
        '''
        cog, mass = self.get_cog()
        inertia = np.zeros((3,3))
        volume = 0.
        rocket = self.asList()

        for component in rocket:
            tvolume, tmass, tinertia = component.get_inertia_wrt(cog)

            volume += tvolume
            inertia += tinertia

        inertia[inertia<1e-6]=0.

        return volume, mass, cog, inertia
    
    
    def get_cpa(self):
        '''
        Compute and return the position of the CPA at rest.
        The code was taken from the class Coefficients in Aerodynamics from rocket model.
        '''
        rocket_dict = self.dictionnary

        l = rocket_dict['tube_length'] + rocket_dict['nose_length']
        r = rocket_dict['tube_radius']
        ln = rocket_dict['nose_length']
        A0 = 0
        Al = np.pi*r**2
        NFins = rocket_dict['fins_number']

        l_t = l - ln
        Xt = rocket_dict['fins_Xt']
        Cr = rocket_dict['fins_Cr']
        Ct = rocket_dict['fins_Ct']
        s = rocket_dict['fins_s']

        Afin = (Cr + Ct)/2 * s
        GammaC = np.arctan2(Xt + 0.5*(Ct - Cr), s)

        Cna_one_fin = (2*np.pi*s**2/Al )/(1 + (1 + (s**2/(Afin*np.cos(GammaC)))**2)**0.5)
        Xfins = l_t + Xt/3*(Cr+2*Ct)/(Cr+Ct) + 1/6*(Cr**2 + Ct**2 +Cr*Ct)/(Cr+Ct)
        Cna_body = 2/Al*(Al - A0)
        Cna_all_fins = Cna_one_fin * NFins/2 * (1 + r/(s + r))

        V = (l - ln)*Al + 1/3*ln*np.pi*r**2

        Cna = Cna_all_fins + Cna_body
        Xbody = (l*Al - V)/(Al - A0)

        cpa = (Xbody*Cna_body + Xfins*Cna_all_fins)/Cna

        return np.array([l-cpa, 0, 0])
    
    def print_properties(self):
        '''
        Print and return mass properties.
        '''
        input_mass = self.dictionnary['rocket_mass']
        volume, mass, cog, inertia = self.get_mass_properties()

        mass = input_mass if mass==0 else mass # Change the value of the mass to the calculated one if the input is 0

        cpa = self.get_cpa()
        print("Volume (m^3)                                 = {0}".format(volume))
        print("Mass   (kg)                                  = {0}".format(mass))
        print("\n")
        print("Position of the center of gravity (COG)      = {0}".format(cog))
        print("Position of the center of pressure (CPA)     = {0}".format(cpa))
        print("\n")
        print("Inertia matrix expressed at the COG (kg*m^2) = {0}".format(inertia[0,:]))
        print("                                               {0}".format(inertia[1,:]))
        print("                                               {0}".format(inertia[2,:]))

        return volume, mass, cog, cpa, inertia