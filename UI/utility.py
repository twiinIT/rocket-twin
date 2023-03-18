from pythreejs import *
from IPython.display import display


###3D
def show3DRocket(rocket_geometry):
    d = rocket_geometry["d"]
    L = rocket_geometry["L"]

    ###TUBE
    cylinder = CylinderGeometry(
        radiusTop=d/2, radiusBottom=d/2, height=L, radialSegments=15
    )
    myCylinder = Mesh(
        geometry = cylinder,
        material=MeshLambertMaterial(vertexColors='VertexColors'),
        position=[0, 0, 0],  
    )

    t = rocket_geometry["t"]
    Cr = rocket_geometry["Cr"]
    Ct = rocket_geometry["Ct"]
    Xt = rocket_geometry["Xt"]
    s = rocket_geometry["s"]

    ###FINS
    vertices = [
        [-t/2, 0, 0],
        [-t/2, Cr-Ct-Xt, s],
        [-t/2, Cr, 0],
        [-t/2, Cr-Xt, s],
        [t/2, 0, 0],
        [t/2, Cr-Ct-Xt, s],
        [t/2, Cr, 0],
        [t/2, Cr-Xt, s]
    ]
    faces = [
        [0, 1, 3],
        [0, 3, 2],
        [0, 2, 4],
        [2, 6, 4],
        [0, 4, 1],
        [1, 4, 5],
        [2, 3, 6],
        [3, 7, 6],
        [1, 5, 3],
        [3, 5, 7],
        [4, 6, 5],
        [5, 6, 7]
    ]
    vertexcolors = ['#ffffff', '#ffffff', '#ffffff', '#ffffff',
                    '#ffffff', '#ffffff', '#ffffff', '#ffffff']

    # Map the vertex colors into the 'color' slot of the faces
    faces = [f + [None, [vertexcolors[i] for i in f], None] for f in faces]

    # Create the geometry:
    cubeGeometry = Geometry(vertices=vertices,
        faces=faces,
        colors=vertexcolors)
    # Calculate normals per face, for nice crisp edges:
    cubeGeometry.exec_three_obj_method('computeFaceNormals')

    nb_fins = rocket_geometry['nb_fins']
    d = rocket_geometry['d']
    L = rocket_geometry['L']

    children = []

    for i in range(nb_fins):
        globals()[f"myFin{i}"] = Mesh(
        geometry=cubeGeometry,
        material=MeshLambertMaterial(vertexColors='VertexColors'),
        position=[d/2 * np.sin(np.pi/(nb_fins/2) * i), -L/2, d/2 * np.cos(np.pi/(nb_fins/2) * i)],   
    )
        children.append(globals()[f"myFin{i}"])
        globals()[f"myFin{i}"].rotateY(np.pi/(nb_fins/2) * i)


    ###NOSE

    def nose_tangent_ogive(x, R, L):
        rho = (R**2 + L**2)/(2*R)
        return np.sqrt(rho**2 - (L-x)**2) + R - rho 

    def nose_ellipse(x,R,L):
        return R*np.sqrt(1-x**2/L**2)

    def nose_parabole(x, R, L, K):
        #K entre 0 et 1 compris
        return R*((2*(x/L)-K*(x/L)**2)/(2-K))

    def nose_power_series(x,R,L,n):
        #n entre 0 et 1
        return R*(x/L)**n 

    def nose_hack_series(x,R,L,C):
        #si C=1/3, serie LV-Haack, minimum drag, si C=2/3, tangent to the body at the base
        theta = np.arccos(1-2*x/L)
        return R/np.sqrt(np.pi) * np.sqrt(theta- np.sin(2*theta)/2 + C*np.sin(theta)**3)

    def nose_cone(x,R,L):
        return x*R/L

    l=rocket_geometry["l"]
    x=np.linspace(0,l,20)
    nosetype = rocket_geometry["nose_type"]



    nose_points = []
    for i in range(len(x)):
        if nosetype == "Ellipse":
            nose_points.append([nose_ellipse(x[i],d/2,l), x[i], 0])
        elif nosetype == "Parabole":
            nose_points.append([nose_parabole(x[i],d/2,l, .5), x[i], 0])
        elif nosetype == "Cone":
            nose_points.append([nose_cone(x[i],d/2,l), x[i]],0)
        elif nosetype == "Haack":
            nose_points.append([nose_hack_series(x[i],d/2,l,1/3), x[i], 0])
        else:
            nose_points.append([nose_tangent_ogive(x[i],d/2,l), x[i], 0])

    nose = LatheGeometry(
        points=nose_points,
        segments=16,
        phiStart=0.0,
        phiLength=2.0*pi, _flat=True)

    myNose = Mesh(
        geometry = nose,
        material=MeshLambertMaterial(vertexColors='VertexColors'),
        position=[0, L/2 + l if nosetype!="Ellipse" else L/2, 0],   
    )
    if nosetype!="Ellipse":
        myNose.rotateZ(np.pi)


    fins = Group(children=children)
    corps= Group(children=[myCylinder,myNose,fins])

    l = LightShadow(camera=UninitializedSentinel)

    axeshelper = AxesHelper(3)

    # Set up a scene and render it:
    cCube = PerspectiveCamera(position=[10, 5, 10], fov=10,
                        children=[DirectionalLight(color='#ffffff', position=[-3, 5, 1], intensity=0.5, target=corps, shadow=l)])
    sceneCube = Scene(children=[corps, axeshelper, AmbientLight(color='#dddddd')], background=None)


    rendererCube = Renderer(camera=cCube, background='red', background_opacity=1,
                            scene=sceneCube, controls=[OrbitControls(controlling=cCube, autoRotate=True)], width = 500, height = 500)

    display(rendererCube)


