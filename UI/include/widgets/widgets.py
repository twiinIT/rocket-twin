import ipywidgets as widgets
import json
import matplotlib.pyplot as plt
import numpy as np
from include.init_rocket.CustomRocket import CustomRocket

plt.close() # To avoid the code from plotting residual figures

materials = {"custom": 0,
             "blue_xps": 32,
             "acier": 7850,
             "acrylique": 1190,
             "aluminium": 2700,
             "balsa": 170, 
             "blue_tube": 1300,
             "bouleau": 670,
             "carton": 680,
             "contre_plaque": 630, 
             "delrin": 1420, 
             "depron (XPS)": 40, 
             "erable": 755,
             "fibre_carbon": 1780,
             "fibre_verre": 1850, 
             "kraft_phenolique": 950, 
             "laiton": 8600, 
             "liege": 240, 
             "nylon": 1150, 
             "pvc": 1390, 
             "papier": 820,
             "pin": 530, 
             "polycarbonate": 1200, 
             "polystyrene": 1050, 
             "polystyrene_eps": 20, 
             "sapin": 450, 
             "tilleul": 500,
             "titane": 4500, 
             "tube_quantum": 1050}

textures = {"Customized":"custom",
             "Acier": "acier",
             "Acrylique": "acrylique",
             "Aluminium": "aluminium",
             "Balsa": "balsa", 
             "Blue tube": "blue_tube",
             "Bouleau": "bouleau",
             "Carton": "carton",
             "Contre-plaqué (bouleau)": "contre_plaque", 
             "Delrin": "delrin", 
             "Depron (XPS)": "depron_xps", 
             "Erable": "erable", 
             "Fibre de carbone": "fibre_carbon",
             "Fibre de verre": "fibre_verre", 
             "Kraft phénolique": "kraft_phenolique", 
             "Laiton": "laiton", 
             "Liège": "liege", 
             "Mousse Bleue de polystyrène (XPS)": "blue_xps",
             "Nylon": "nylon", 
             "Papier (bureau)": "papier",
             "Pin": "pin", 
             "Polycarbonate (Lexan)": "polycarbonate", 
             "Polystyrène": "polystyrene", 
             "Polystyrène (générique EPS)": "polystyrene_eps", 
             "PVC": "pvc", 
             "Sapin": "sapin", 
             "Tilleul": "tilleul",
             "Titane": "titane", 
             "Tube Quantum": "tube_quantum"}

nose_options = [('Ellipse','ellipse'),
                ('Cone','cone'),
                ('Haack','haack_series'),
                ('Parabole','parabole'),
                ('Tangent Ogive','tangent_ogive'),
                ('Power Series', 'power_series')]

impulse_options = [("[1.26 - 2.50]",'A'),
                   ("[2.51 - 5.00]",'B'),
                   ("[5.01 - 10.0]",'C'),
                   ("[10.01 - 20.0]",'D'),
                   ("[20.01 - 40.0]",'E'),
                   ("[40.01 - 80.0]",'F'),
                   ("[80.01 - 160]",'G'),
                   ("[160.01 - 320]",'H'),
                   ("[320.01 - 640]",'I'),
                   ("[640.01 - 1280]",'J'),
                   ("[1,280.01 - 2,560]",'K'),
                   ("[2,560.01 - 5,120]",'L'),
                   ("[5,120.01 - 10,240]",'M'),
                   ("[10,240.01 - 20,480]",'N'),
                   ("[20,480.01 - 40,960]",'O')]


####################################################

# Creation of widgets for rocket properties

####################################################


# Tube properties
tube_length = widgets.BoundedFloatText(value=2,min=0,max=500.0,step=0.1,description='Tube length ($m$):',style={'description_width': 'initial'},disabled=False)
tube_radius = widgets.BoundedFloatText(value=.1,min=0,max=50.0,step=0.1,description='Tube radius ($m$):',style={'description_width': 'initial'},disabled=False)
tube_thickness = widgets.BoundedFloatText(value=.01,min=0,max=.1,step=0.001,description='Tube thickness ($m$):',style={'description_width': 'initial'},disabled=False)
tube_material = widgets.Dropdown(layout={'width': 'strech'}, description = 'Tube material',value = "fibre_carbon",options = textures.items(),style={'description_width': 'initial'},disabled=False)
tube_density = widgets.BoundedFloatText(value=0.,min=0,max=100000,step=1,description='Tube density ($kg/m^3$):',style={'description_width': 'initial'},disabled=False)

def show_tube_density(change):
    if change['new'] == "custom":
        tube_density.value = 0.
        tube_density.layout.display = ''
    else:
        tube_density.layout.display = 'none'
        tube_density.value = materials[change['new']]

show_tube_density({'new':tube_material.value})
tube_material.observe(show_tube_density, names='value')

# Nose properties
nose_type = widgets.Dropdown(layout={'width': 'strech'},options=nose_options,style={'description_width': 'initial'},value='ellipse',description='Nose type:',disabled=False)
nose_parameter = widgets.BoundedFloatText(value=0.,min=0.,max=1.,step=0.1,description='Nose parameter C*:',style={'description_width': 'initial'},disabled=False)
nose_parameter_desc = widgets.Label( value='')
nose_length = widgets.BoundedFloatText(value=.5,min=0,max=50.0,step=0.1,description='Nose length ($m$):',style={'description_width': 'initial'},disabled=False)
nose_radius = widgets.BoundedFloatText(value=.1,min=0,max=50.0,step=0.1,description='Nose radius ($m$):',style={'description_width': 'initial'},disabled=False)
nose_thickness = widgets.BoundedFloatText(value=.01,min=0,max=.1,step=0.001,description='Nose thickness ($m$):',style={'description_width': 'initial'},disabled=False)
nose_material = widgets.Dropdown(layout={'width': 'strech'}, description = 'Nose material',value = "acier",options = textures.items(),style={'description_width': 'initial'},disabled=False)
nose_density = widgets.BoundedFloatText(value=0,min=0,max=100000,step=1,description='Nose density ($kg/m^3$):',style={'description_width': 'initial'},disabled=False)

def show_nose_density(change):
    if change['new'] == "custom":
        nose_density.value = 0.
        nose_density.layout.display = ''
    else:
        nose_density.layout.display = 'none'
        nose_density.value = materials[change['new']]

def show_nose_parameter(change):
    nose_parameter.min = 0.
    nose_parameter.max = 1.
    if change['new'] in ['haack_series','power_series','parabole']:
        if change['new'] == 'haack_series':
            nose_parameter_desc.value = '(*) C=0 : LD-Haack - C=1/3 : LV-Haack (min drag) - C=2/3 : tangent to the body'
            nose_parameter.value = 0.
        elif change['new'] == 'power_series':
            nose_parameter_desc.value = '(*) Curve parameter C in (0,1)'
            nose_parameter.value = 0.1
            nose_parameter.min = 0.001
            nose_parameter.max = 0.999
        elif change['new'] == 'parabole':
            nose_parameter_desc.value = '(*) Parabola parameter C in [0,1]'
            nose_parameter.value = 0.
        nose_parameter.layout.display = ''
        nose_parameter_desc.layout.display = ''
    else:
        nose_parameter.layout.display = 'none'
        nose_parameter_desc.layout.display = 'none'
        nose_parameter.value = 0.


show_nose_density({'new':nose_material.value})
nose_material.observe(show_nose_density, names='value')
show_nose_parameter({'new':nose_type.value})
nose_type.observe(show_nose_parameter, names='value')

# Fins properties
fin_file = open("./include/widgets/fin.png", "rb")
fin_image = fin_file.read()
fin_wimg = widgets.Image(value=fin_image,format='png',height=100,width=200,)
Cr = widgets.BoundedFloatText(value=.2,min=0,max=1,step=0.01,description='Cr ($m$):',style={'description_width': 'initial'},disabled=False)
Ct = widgets.BoundedFloatText(value=.1,min=0,max=1,step=0.01,description='Ct ($m$):',style={'description_width': 'initial'},disabled=False)
Xt = widgets.BoundedFloatText(value=.1,min=0,max=1,step=0.01,description='Xt ($m$):',style={'description_width': 'initial'},disabled=False)
s = widgets.BoundedFloatText(value=.15,min=0,max=1,step=0.01,description='s ($m$):',style={'description_width': 'initial'},disabled=False)
fins_thickness = widgets.BoundedFloatText(value=.01,min=0,max=.1,step=0.001,description='thickness ($m$):',style={'description_width': 'initial'},disabled=False)
fins_cant = widgets.BoundedFloatText(value=0.,min=-180,max=180,step=1.,description='Cant angle (deg):',style={'description_width': 'initial'},disabled=False)
fins_number = widgets.IntText(value=4,description='Number of fins:',style={'description_width': 'initial'},disabled=False)
fins_material = widgets.Dropdown(layout={'width': 'strech',}, description = 'Fins material',value = "fibre_carbon",options = textures.items(),style={'description_width': 'initial'},disabled=False)
fins_density = widgets.BoundedFloatText(value=0,min=0,max=100000,step=1,description='Fins density ($kg/m^3$):',style={'description_width': 'initial'},disabled=False)
fins_position = widgets.BoundedFloatText(value=0,min=0,max=500,step=0.01,description='Fins position from tube bottom ($m$):',style={'description_width': 'initial'},disabled=False)

def show_fins_density(change):
    if change['new'] == "custom":
        fins_density.value = 0.
        fins_density.layout.display = ''
    else:
        fins_density.layout.display = 'none'
        fins_density.value = materials[change['new']]

show_fins_density({'new':fins_material.value})
fins_material.observe(show_fins_density, names='value')

# Combining everithing for geometry and mass
tube = widgets.VBox([tube_length,tube_radius,tube_thickness,tube_material,tube_density])
nose = widgets.VBox([nose_type,nose_parameter,nose_parameter_desc,nose_length,nose_radius,nose_thickness,nose_material,nose_density])
fins_fields = widgets.VBox([Cr,Ct,Xt,s,fins_thickness,fins_cant,fins_number,fins_material,fins_density,fins_position])
fins = widgets.HBox([fins_fields,fin_wimg])
children = [tube,nose,fins]
rocket_properties_widget = widgets.Tab(children = children, titles = ['Tube prop.', 'Nose prop.', 'Fins prop.'])

# Motor Properties
f = open('./include/widgets/motor_data.json')
data = json.load(f)

impulse_class = widgets.Dropdown(options=impulse_options,description='Impulse Class (N.s):',style={'description_width': 'initial'},disabled=False)
motor_diameter = widgets.FloatRangeSlider(value=[6, 161],min=6,max=161,step=1,description='Diameter ($mm$):',disabled=False,continuous_update=False,
                                          orientation='horizontal',readout=True,readout_format='.1f',style={'description_width': 'initial'})
motor_position = widgets.BoundedFloatText(value=0,min=0,max=500,step=0.1,description='Motor position from tube bottom ($m$):',style={'description_width': 'initial'},disabled=False)
motor_geometry = widgets.VBox([motor_diameter,motor_position])
selected_motor = widgets.Dropdown(options = [], description = 'Designation:', style={'description_width': 'initial'}, disabled=False)
motor_select_text = widgets.Label( value='(Keep this tab opened to ensure you have selected the right motor)', style={'description_width':'initial'})
motor_ring = widgets.Checkbox(value=True,description='Automatic fixation ring around the motor',disabled=False,indent=True,style={'description_width':'initial'})
ring_material = widgets.Dropdown(layout={'width': 'strech',}, description = 'Fixation ring material',value = "acier",options = textures.items(),style={'description_width': 'initial'},disabled=False)
ring_density = widgets.BoundedFloatText(value=0,min=0,max=100000,step=1,description='Fixation ring density ($kg/m^3$):',style={'description_width': 'initial'},disabled=False)
ring_box = widgets.VBox([ring_material,ring_density])
motor_file = open("./include/widgets/thrustcurve.png", "rb")
motor_image = motor_file.read()
motor_wimg = widgets.Image(value=motor_image,format='png', height = 300, width=600)
motorBox = widgets.VBox([selected_motor,motor_select_text,motor_ring,ring_box,motor_wimg])

motor_selection_widget = widgets.Accordion(children=[impulse_class, motor_geometry, motorBox], titles=('Impulse class', 'Geometric parameters', 'Motor selection'), style={'description_width': 'initial'})

def show_ring(change):
    if change['new']:
        ring_box.layout.display = ''
    else:
        ring_box.layout.display = 'none'

motor_ring.observe(show_ring, names='value')

def show_ring_density(change):
    if change['new'] == "custom":
        ring_density.value = 0.
        ring_density.layout.display = ''
    else:
        ring_density.layout.display = 'none'
        ring_density.value = materials[change['new']]

show_ring_density({'new':ring_material.value})
ring_material.observe(show_ring_density, names='value')

def thrustcurve(motor_name):
    d=[]
    for elem in data:
        if elem['designation'] == motor_name:
            d = elem['samples']
    x = [d[i][0] for i in range(len(d))]
    y = [d[i][1] for i in range(len(d))]

    plt.plot(x,y)
    plt.xlabel('time (s)')
    plt.ylabel('impulse (N)')
    plt.title(f'{motor_name} thrust curve')
    plt.savefig('./include/widgets/thrustcurve.png')
    plt.close()

def set_motor_options(change):
    if change['new'] == 2:
        motors = []
        for motor in data:
            if motor['impulseClass']==impulse_class.value and motor['diameter']>motor_diameter.value[0] and motor['diameter']<motor_diameter.value[1]:
                motors.append(motor['designation'])

        selected_motor.options = motors
        if len(motors)!=0:
            selected_motor.value = motors[0]

def change_thrustcurve(change):
    thrustcurve(change['new'])
    motor_file = open("./include/widgets/thrustcurve.png", "rb")
    motor_image = motor_file.read()
    motor_wimg.value = motor_image

selected_motor.observe(change_thrustcurve, names='value')
motor_selection_widget.observe(set_motor_options, names='selected_index')


# Parachute settings
rope_rest_length = widgets.BoundedFloatText(value=1.,min=0.,max=1000.,step=.1,description='Rope rest length ($m$):',style={'description_width': 'initial'},disabled=False)
parachute_weight = widgets.BoundedFloatText(value=.5,min=0.,max=1000.,step=.1,description='Parachute weight ($kg$):',style={'description_width': 'initial'},disabled=False)
s_ref = widgets.BoundedFloatText(value=.29,min=0.,max=1000.,step=.1,description='Reference surface of parachute ($m^2$):',style={'description_width': 'initial'},disabled=False)
parachute_cd = widgets.BoundedFloatText(value=1.75,min=0.,max=100.,step=.1,description='Drag coefficient of parachute:',style={'description_width': 'initial'},disabled=False)
deploy_method = widgets.Dropdown(options=[('timer','timer'), ('negative vertical velocity','velocity')],value='timer',description='Parachute deployment method:',style={'description_width': 'initial'},disabled=False)
parachute_timer = widgets.BoundedFloatText(value=60.,min=0.,max=3600.,step=1,description='(*)Deployment time ($s$):',style={'description_width': 'initial'},disabled=False)
timer_text = widgets.Label(value="(*)Time before parachute deployment in seconds.", style={'description_width':'initial'})

parachute_widget = widgets.VBox([rope_rest_length, parachute_weight, s_ref, parachute_cd, deploy_method, parachute_timer])

def show_timer(change):
    if change['new'] == 'timer':
        parachute_timer.layout.display = ''
        timer_text.layout.display = ''
    else:
        parachute_timer.layout.display = 'none'
        timer_text.layout.display = 'none'
        parachute_timer.value = 60.

deploy_method.observe(show_timer, names='value')

# Additional masses
number_int = widgets.BoundedIntText(value=0,min=0,max=100,description='Number of additional masses',style={'description_width': 'initial'},disabled=False)
number_text = widgets.Label(value="- Please ensure that you have entered the desired number of additional masses. If you reduce the number of masses, the last mass you specified will be lost.", style={'description_width':'initial'})
masses_number = widgets.VBox([number_int,number_text])
mass_text = widgets.Label(value="- You must specify each mass' properties in order to move to the next step.", style={'description_width':'initial'})
masses_properties = widgets.Tab()
mass_box = widgets.VBox([mass_text,masses_properties])
additional_masses_widget = widgets.Accordion(children=[masses_number,mass_box], titles=('Mass Number', 'Mass properties'), style={'description_width': 'initial'})

masses_children = []
masses_titles = []

def on_number_change(change):
    global masses_children,masses_titles
    number = change['new']
    nchild = len(masses_children)
    if number > nchild:
        for i in range(number-nchild):
            masses_children.append(create_mass_form())
            masses_titles.append(f'Mass-{len(masses_children)+i}')
    elif number < nchild:
        masses_children = masses_children[:number]
        masses_titles = masses_titles[:number]

def on_number_selected(change):
    global masses_children,masses_titles
    if change['new'] == 1:
        masses_properties.children = masses_children
        masses_properties.titles = masses_titles

number_int.observe(on_number_change,names='value')
additional_masses_widget.observe(on_number_selected,names='selected_index')

def create_mass_form():
    mass_type = widgets.Dropdown(value = 'cylinder', options=[('Cylinder','cylinder'), ('Empty cylinder','empty_cylinder')], description='Shape of mass',style={'description_width': 'initial'},disabled=False)
    mass_length= widgets.BoundedFloatText(value=0.,min=0.,max=1000.,step=.1,description='Mass length ($m$):',style={'description_width': 'initial'},disabled=False)
    mass_outer_radius= widgets.BoundedFloatText(value=0.,min=0.,max=100.,step=.1,description='Mass outer radius ($m$):',style={'description_width': 'initial'},disabled=False)
    mass_inner_radius= widgets.BoundedFloatText(value=0.,min=0.,max=100.,step=.1,description='Mass inner radius ($m$):',style={'description_width': 'initial'},layout={'display':'none'},disabled=False)
    mass_material = widgets.Dropdown(description = 'Mass material',value = "custom",options = textures.items(),style={'description_width': 'initial'},disabled=False)
    mass_density = widgets.BoundedFloatText(value=0,min=0,max=100000,step=1,description='Mass density ($kg/m^3$):',style={'description_width': 'initial'},disabled=False)
    mass_position= widgets.BoundedFloatText(value=0.,min=0.,max=1000.,step=0.1,description='Mass position form rocket bottom ($m$):',style={'description_width': 'initial'},disabled=False)

    form = widgets.VBox([mass_type,mass_length,mass_outer_radius,mass_inner_radius,mass_material,mass_density,mass_position])

    def on_type_selected(change):
        if change['new'] == 'empty_cylinder':
            mass_inner_radius.layout.display = ''
        else:
            mass_inner_radius.layout.display = 'none'
            mass_inner_radius.value = 0.

    def update_max(change):
        mass_inner_radius.max = change['new']
    
    def show_mass_density(change):
        if change['new'] == "custom":
            mass_density.value = 0.
            mass_density.layout.display = ''
        else:
            mass_density.layout.display = 'none'
            mass_density.value = materials[change['new']]

    mass_type.observe(on_type_selected,names='value')
    mass_outer_radius.observe(update_max,names='value')
    mass_material.observe(show_mass_density,names='value')

    return form

def mass_dict_list():
    '''
    Return a list of dict representing additinal masses.
    '''
    dict_list = []
    for i in range(number_int.value):
        parent = masses_properties.children[i]
        dict = {'type':parent.children[0].value,
                'length':parent.children[1].value,
                'outer_radius':parent.children[2].value,
                'inner_radius':parent.children[3].value,
                'material':parent.children[4].value,
                'density':parent.children[5].value,
                'position':parent.children[6].value}
        dict_list.append(dict)

    return dict_list



# Launching parameters
rocket_mass = widgets.BoundedFloatText(value=2.,min=0.,max=1000000.,step=1.,description="Rocket's total mass ($kg$):",style={'description_width': 'initial'},disabled=False)
prop_weight = widgets.BoundedFloatText(value=.2,min=0.,max=1000000.,step=1.,description="Propellant mass ($kg$):",style={'description_width': 'initial'},disabled=False)
nose_mass = widgets.BoundedFloatText(value=.5,min=0.,max=1000000.,step=1.,description="(*)Nose mass ($kg$):",style={'description_width': 'initial'},disabled=False)
nose_mass_text = widgets.Label( value="(*) The mass of the ejected part of the nose when the parachute is deployed.", style={'description_width':'initial'})
rocket_launch_angle = widgets.BoundedFloatText(value=80.,min=0.,max=180,step=1,description="Rocket's launch angle (deg):",style={'description_width': 'initial'},disabled=False)
wind_on = widgets.Checkbox(value=True,description='Generate random wind profile at launch time.',disabled=False,indent=True,style={'description_width':'initial'})
wind_average_speed = widgets.BoundedFloatText(value=5.,min=0.,max=1000.,step=1.,description="Wind average speed ($m/s$):",style={'description_width': 'initial'},disabled=False)

launching_parameters_widget = widgets.VBox([rocket_mass, prop_weight, nose_mass, nose_mass_text, rocket_launch_angle, wind_on, wind_average_speed])

def show_wind(change):
    if change['new']:
        wind_average_speed.layout.display = ''
    else:
        wind_average_speed.layout.display = 'none'

wind_on.observe(show_wind, names='value')

####################################################

####################################################

def find_motor(designation):
    '''
    Return the motor dictionary corresponding to the motor designation.
    '''
    for motor in data:
        if motor['designation'] == designation:
            return motor
    raise ValueError('Motor not found : wrong motor designation.')

def rocket_dictionary():
    '''
    Return a dictionary representing the rocket.
    '''
    rocket = {'tube_length':tube_length.value,
              'tube_radius':tube_radius.value,
              'tube_thickness':tube_thickness.value,
              'tube_material':tube_material.value,
              'tube_density':tube_density.value,
              'nose_type':nose_type.value,
              'nose_parameter':nose_parameter.value,
              'nose_length':nose_length.value,
              'nose_radius':nose_radius.value,
              'nose_thickness':nose_thickness.value,
              'nose_material':nose_material.value,
              'nose_density':nose_density.value,
              'fins_Cr':Cr.value,
              'fins_Ct':Ct.value,
              'fins_Xt':Xt.value,
              'fins_s':s.value,
              'fins_thickness':fins_thickness.value,
              'delta':fins_cant.value*np.pi/180, # conversion to radians
              'fins_number':fins_number.value,
              'fins_material':fins_material.value,
              'fins_density':fins_density.value,
              'fins_position':fins_position.value,
              'motor':find_motor(selected_motor.value),
              'motor_position':motor_position.value,
              'motor_ring':motor_ring.value,
              'motor_ring_material':ring_material.value,
              'motor_ring_density':ring_density.value,
              'parachute_l0':rope_rest_length.value,
              'parachute_weight':parachute_weight.value,
              'parachute_sref':s_ref.value,
              'parachute_Cd':parachute_cd.value,
              'parachute_deploy_method':deploy_method.value,
              'parachute_deploy_timer':parachute_timer.value,
              'additional_masses':mass_dict_list(),
              'rocket_mass':rocket_mass.value,
              'rocket_prop_weight':prop_weight.value,
              'ejected_nose_mass':nose_mass.value,
              'rocket_launch_angle':rocket_launch_angle.value*np.pi/180, # conversion to radians
              'wind_on':wind_on.value,
              'wind_average_speed':wind_average_speed.value}

    return rocket

def rocket_from_widgets():
    '''
    Create a CustomRocket object representing the rocket from its dict, and write it content in 'rocket_dict.json'.
    '''
    rocket_dict = rocket_dictionary()
    rocket = CustomRocket.fromDict(rocket_dict)

    volume, mass, cog, inertia = rocket.get_mass_properties()

    rocket_dict['rocket_volume'] = volume
    # rocket_dict['rocket_mass'] = mass ### For now the mass is passed as the mass entered by the user
    rocket_dict['rocket_cog'] = cog.tolist()
    rocket_dict['rocket_inertia'] = inertia.tolist()

    # Write the content of the dict in a file that will be passed to the model
    with open("include/init_rocket/rocket_dict.json", "w") as f:
        json.dump(rocket_dict, f)
    
    return rocket