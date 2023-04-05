# Mesh creation
import numpy as np
from include.init_rocket.Solid import Solid
import include.init_rocket.nose_creation as nc
from stl import mesh
from scipy.spatial.transform import Rotation as R

# Function used to translate vertices of a mesh
def translate(vertices, trans_vect  = np.zeros(3)):
    return vertices + trans_vect

# Functions to manually create meshes for cylinder, fins and nose of the rocket given its caracteristics

def half_cylinder(outer_radius = .5, inner_radius = .49, height = 2, pnum = 25, pos = 0.):
    '''
    Create plotting part of the empty body of the rocket (i.e. a half cylinder).

    Args:
        outer_radius (float): Outer radius of the rocket.
        inner_radius (float): Inner radius of the rocket.
        height (float): The height of the rocket.
        pnum (int): number of points around the cylinder.
        pos (float): position of cylinder's bottom.

    Returns:
        The plotting mesh for the rocket's body.
    '''
    theta = np.linspace(0, np.pi, pnum, endpoint=True)

    cos, sin = np.cos(theta), np.sin(theta)

    y_out = outer_radius * cos
    z_out = outer_radius * sin
    y_in = inner_radius * cos
    z_in = inner_radius * sin

    x_bottom = pos + np.zeros(pnum)
    x_top = (height+pos) * np.ones(pnum)

    vertices = np.concatenate((np.array([x_bottom, y_out, z_out]).T,
                               np.array([x_top, y_out, z_out]).T,
                               np.array([x_bottom, y_in, z_in]).T,
                               np.array([x_top, y_in, z_in]).T))

    faces = []
    
    # Cylinder
    for i in range(pnum-1):
        # Outer one
        faces.append([i, i+1, pnum+i+1])
        faces.append([pnum+i+1, pnum+i, i])
        # Inner one
        faces.append([3*pnum+i+1, 2*pnum+i+1, 2*pnum+i])
        faces.append([2*pnum+i, 3*pnum+i, 3*pnum+i+1])

    # Bottom face
    for i in range(pnum-1):
        faces.append([i,2*pnum+i,i+1])
        faces.append([i+1, 2*pnum+i, 2*pnum+i+1])
    # Top face
    for i in range(pnum-1):
        faces.append([pnum+i, pnum+i+1, 3*pnum+i])
        faces.append([pnum+i+1, 3*pnum+i+1, 3*pnum+i])

    faces.append([0, pnum, 3*pnum])
    faces.append([0, 3*pnum, 2*pnum])
    faces.append([3*pnum-1, 4*pnum-1, 2*pnum-1])
    faces.append([3*pnum-1, 2*pnum-1, pnum-1])

    faces = np.array(faces)

    rot = R.from_euler('xyz', [-np.pi/2,0.,0.], degrees=False)
    vertices = rot.apply(vertices)

    brute_mesh = Solid.BruteMesh(vertices=vertices, faces=faces)

    cylinder_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cylinder_mesh.vectors[i][j] = vertices[f[j], :]

    return brute_mesh, cylinder_mesh


def empty_cylinder(outer_radius = .5, inner_radius = .49, height = 2, pnum = 50, pos = 0., density = 1e3):
    '''
    Create a Solid object representing the empty body of the rocket.

    Args:
        outer_radius (float): Outer radius of the rocket.
        inner_radius (float): Inner radius of the rocket.
        height (float): The height of the rocket.
        pnum (int): number of points around the cylinder.
        pos (float): position of cylinder's bottom.
        density (float): density of the cylinder in kg/m^3.

    Returns:
        A Solid object containing all data necessary to manipulate, plot and calculate properties of the cylinder.
    '''
    theta = np.linspace(0, 2*np.pi, pnum, endpoint=False)

    cos, sin = np.cos(theta), np.sin(theta)

    y_out = outer_radius * cos
    z_out = outer_radius * sin
    y_in = inner_radius * cos
    z_in = inner_radius * sin

    x_bottom = pos + np.zeros(pnum)
    x_top = (height+pos) * np.ones(pnum)

    vertices = np.concatenate((np.array([x_bottom, y_out, z_out]).T,
                               np.array([x_top, y_out, z_out]).T,
                               np.array([x_bottom, y_in, z_in]).T,
                               np.array([x_top, y_in, z_in]).T))

    faces = []
    
    # Cylinder
    for i in range(pnum-1):
        # Outer one
        faces.append([i, i+1, pnum+i+1])
        faces.append([pnum+i+1, pnum+i, i])
        # Inner one
        faces.append([3*pnum+i+1, 2*pnum+i+1, 2*pnum+i])
        faces.append([2*pnum+i, 3*pnum+i, 3*pnum+i+1])
    # Last outer triangles
    faces.append([pnum-1, 0, pnum])
    faces.append([pnum, 2*pnum-1, pnum-1])
    # Last inner triangles
    faces.append([3*pnum, 2*pnum, 3*pnum-1])
    faces.append([3*pnum-1, 4*pnum-1, 3*pnum])

    # Bottom face
    for i in range(pnum-1):
        faces.append([i,2*pnum+i,i+1])
        faces.append([i+1, 2*pnum+i, 2*pnum+i+1])
    faces.append([pnum-1, 3*pnum-1, 0])
    faces.append([0, 3*pnum-1, 2*pnum])
    # Top face
    for i in range(pnum-1):
        faces.append([pnum+i, pnum+i+1, 3*pnum+i])
        faces.append([pnum+i+1, 3*pnum+i+1, 3*pnum+i])
    faces.append([2*pnum-1, pnum, 4*pnum-1])
    faces.append([pnum, 3*pnum, 4*pnum-1])
   
    faces = np.array(faces)

    brute_mesh = Solid.BruteMesh(vertices=vertices, faces=faces)

    cylinder_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cylinder_mesh.vectors[i][j] = vertices[f[j], :]

    plot_brute_mesh, plot_stl_mesh = half_cylinder(outer_radius=outer_radius, inner_radius=inner_radius, height=height, pnum=pnum//2, pos=pos)

    return Solid(brute_mesh=brute_mesh, stl_mesh=cylinder_mesh, plot_brute_mesh=plot_brute_mesh, plot_stl_mesh=plot_stl_mesh, density = density)


def cylinder(radius = .5, height = 2, pnum = 50, pos = 0., density = 1e3):
    '''
    Create a Solid object representing a cylindric distribution of mass in the rocket.

    Args:
        radius (float): Outer radius of the cylinder.
        height (float): The height of the cylinder.
        pnum (int): number of points around the cylinder.
        pos (float): position of cylinder's bottom.
        density (float): density of the cylinder in kg/m^3.

    Returns:
        A Solid object containing all data necessary to manipulate, plot and calculate properties of the cylinder.
    '''
    theta = np.linspace(0, 2*np.pi, pnum, endpoint=False)
    y = radius * np.cos(theta)
    z = radius * np.sin(theta)

    x_bottom = pos + np.zeros(pnum)
    x_top = (height+pos) * np.ones(pnum)

    vertices = np.concatenate((np.array([x_bottom, y, z]).T, np.array([x_top, y, z]).T, np.array([[pos,0,0]]), np.array([[height+pos,0,0]])))

    faces = []

    end = len(vertices)
    
    # Bottom face
    for i in range(pnum-1):
        faces.append([end-2,i+1,i])
    faces.append([end-2,0,pnum-1])
    # Top face
    for i in range(pnum-1):
        faces.append([end-1,pnum+i,pnum+i+1])
    faces.append([end-1,2*pnum-1,pnum])
    # Cylinder
    for i in range(pnum-1):
        faces.append([i, i+1, pnum+i+1])
        faces.append([pnum+i+1, pnum+i, i])
    faces.append([pnum-1, 0, pnum])
    faces.append([pnum, 2*pnum-1, pnum-1])

    faces = np.array(faces)

    brute_mesh = Solid.BruteMesh(vertices=vertices, faces=faces)

    cylinder_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cylinder_mesh.vectors[i][j] = vertices[f[j], :]

    return Solid(brute_mesh=brute_mesh, stl_mesh=cylinder_mesh, plot_brute_mesh=brute_mesh, plot_stl_mesh=cylinder_mesh, density = density)


def fins(Cr=.2,Ct=.1, Xt=.1, s=.15, thick=.01,fnum=4, radius=.5, pos=0., density = 1e3):
    '''
    Create a Solid object containing the mesh for the fins of the rocket and their various properties (see class Solid).
    See fin.png for the definition of Cr,...,s.

    Args:
        thick (float): Thickness of the fin.
        fnum (int): The number of fins.
        radius (float): The radius of the rocket.
        pos (float): the position of the bottom of the fins (0 is the position of the bottom of the rocket).
        density (float): density of fins in kg/m^3.

    Returns:
        A Solid object containing all data necessary to manipulate, plot and calculate properties of the fins.
    '''
    # Mesh for one fin
    vertices = np.array([[Cr, 0, -thick/2],
                         [Cr, 0, thick/2],
                         [Cr-Xt, s, thick/2],
                         [Cr-Xt, s, -thick/2],
                         [0, 0, -thick/2],
                         [0, 0, thick/2],
                         [Cr-Xt-Ct, s, thick/2],
                         [Cr-Xt-Ct, s, -thick/2]])
    faces = np.array([[0, 3, 1],
                      [2, 1, 3],
                      [0, 1, 4],
                      [1, 5, 4],
                      [4, 5, 6],
                      [4, 6, 7],
                      [2, 3, 6],
                      [3, 7, 6],
                      [1, 2, 5],
                      [2, 6, 5],
                      [0, 4, 3],
                      [3, 4, 7]])
    
    vertices = translate(vertices=vertices, trans_vect=np.array([pos, radius, 0]))

    total_vertices = vertices
    total_faces = faces

    n_vertice = len(vertices)
    n_face = len(faces)

    # Total mesh
    for n in range(1,fnum):
        # rotation and translation of the fin according to its position
        angle = 2*np.pi*n/fnum
        rotation = R.from_euler('xyz', angles=[angle,0,0], degrees=False)

        new_vertices = rotation.apply(vertices)
        new_faces = faces + len(total_vertices)

        total_vertices = np.concatenate((total_vertices, new_vertices))
        total_faces = np.concatenate((total_faces, new_faces))

    # Plotting mesh consisting in the half of the toal mesh
    num = int(np.ceil((fnum+1)/2))

    plot_total_vertices = total_vertices[:n_vertice*num]
    plot_total_faces = total_faces[:n_face*num]

    # Rotation of plot vertices
    rot = R.from_euler('xyz', [-np.pi/2,0.,0.],degrees=False)
    plot_total_vertices = rot.apply(plot_total_vertices)
    
    brute_mesh = Solid.BruteMesh(vertices=total_vertices, faces=total_faces)
    plot_brute_mesh = Solid.BruteMesh(vertices=plot_total_vertices, faces=plot_total_faces)

    fins = mesh.Mesh(np.zeros(total_faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(total_faces):
        for j in range(3):
            fins.vectors[i][j] = total_vertices[f[j],:]

    data = np.zeros(plot_total_faces.shape[0], dtype=mesh.Mesh.dtype)
    data['vectors'] = fins.vectors[:n_face*num,:]

    plot_fins = mesh.Mesh(data)

    plot_fins.rotate([0.5, 0., 0.], np.pi/2)

    return Solid(brute_mesh=brute_mesh, stl_mesh=fins, plot_brute_mesh=plot_brute_mesh, plot_stl_mesh=plot_fins, density = density)


def half_nose(nose_obj, Cpnum=10):
    '''
    Create plotting part of the nose of the rocket.

    Args:
        shape_function (string): The function giving the nose's shape (see code for available functions).
        radius (float): The radius of the nose (typically similar to rocket's radius).
        length (float): The length of the nose.
        curve_param (number): Curve parameter used in the shape_function (see the definition of each shape_function for more detail).
        thick (float): Thickness of the nose.
        pos (float): Position of nose bottom with respect to rocket's bottom.
        Vpnum (int): Number of points on the curve.
        Cpnum (int): Number of points around the nose.
        
    Returns:
        The plotting mesh for the nose.
    '''
    out_vertices = nose_obj.out_points
    in_vertices = nose_obj.in_points
    out_vertices_to_rotate = out_vertices[1:]
    in_vertices_to_rotate = in_vertices[1:]

    OVpnum = len(out_vertices)
    IVpnum = len(in_vertices)

    out_faces = []
    in_faces = []

    for j in range(1,Cpnum):
        # Rotation and translation of the fin according to its position
        angle = np.pi*j/(Cpnum-1)
        rotation = R.from_euler('xyz', angles=[angle,0,0], degrees=False)

        # Rotate and concatenate
        out_vertices = np.concatenate((out_vertices, rotation.apply(out_vertices_to_rotate)))
        in_vertices = np.concatenate((in_vertices, rotation.apply(in_vertices_to_rotate)))

        # Making the triangles on the tip of the nose
        if j == 1:
            # Outer first column of triangles
            out_faces.append([OVpnum,1,0])
            for i in range(1,OVpnum-1):
                out_faces.append([OVpnum+i-1, OVpnum+i, i])
                out_faces.append([OVpnum+i,i+1,i])
            
            # Inner first column of trianges
            in_faces.append([0,1,IVpnum])
            for i in range(1,IVpnum-1):
                in_faces.append([i,IVpnum+i,IVpnum+i-1])
                in_faces.append([i,i+1,IVpnum+i])

        else:
            # Remaining faces on the outer side
            for i in range(OVpnum-2):
                if (i==0):
                    # Single top triangle
                    out_faces.append([OVpnum + (OVpnum-1)*(j-1),OVpnum + (OVpnum-1)*(j-2),0])
                    # first rectangle
                    left = OVpnum + (OVpnum-1)*(j-2)
                    right = OVpnum + (OVpnum-1)*(j-1)
                    out_faces.append([right, right+1 ,left])
                    out_faces.append([right+1, left+1 ,left])
                else:
                    # other rectangles
                    left = i + OVpnum + (OVpnum-1)*(j-2)
                    right = i + OVpnum + (OVpnum-1)*(j-1)
                    out_faces.append([right, right+1 ,left])
                    out_faces.append([right+1, left+1 ,left])
            # Remaining faces on the inner side
            for i in range(IVpnum-2):
                if (i==0):
                    # Single top triangle
                    in_faces.append([0,IVpnum + (IVpnum-1)*(j-2),IVpnum + (IVpnum-1)*(j-1)])
                    # first rectangle
                    left = IVpnum + (IVpnum-1)*(j-2)
                    right = IVpnum + (IVpnum-1)*(j-1)
                    in_faces.append([left,right+1,right])
                    in_faces.append([left,left+1,right+1])
                else:
                    # other rectangles
                    left = i + IVpnum + (IVpnum-1)*(j-2)
                    right = i + IVpnum + (IVpnum-1)*(j-1)
                    in_faces.append([left,right+1,right])
                    in_faces.append([left,left+1,right+1])

    nout = len(out_vertices)

    out_faces = np.array(out_faces)
    in_faces = np.array(in_faces) + nout

    # Closing the nose
    close_faces = []
    for i in range(1,Cpnum):
        top_r, top_l = i*(OVpnum-1), (i+1)*(OVpnum-1)
        bot_r, bot_l = i*(IVpnum-1)+nout, (i+1)*(IVpnum-1)+nout
        close_faces.append([top_r, top_l, bot_r])
        close_faces.append([top_l, bot_l, bot_r])

    # Closing the lateral side
    out_end = (Cpnum-2)*(OVpnum-1)+OVpnum
    in_end = nout + (Cpnum-2)*(IVpnum-1)+IVpnum
    # Top first triangles
    close_faces.append([1,nout,0])
    close_faces.append([nout,out_end,0])
    n_tri = OVpnum-IVpnum
    for i in range(1,n_tri):
        close_faces.append([i,i+1,nout])
        close_faces.append([out_end+1,out_end,nout])
        out_end+=1
    # First rectangle
    close_faces.append([n_tri,nout+1,nout])
    close_faces.append([n_tri,n_tri+1,nout+1])
    close_faces.append([out_end+1,out_end,nout])
    close_faces.append([nout,in_end,out_end+1])
    # Remaining rectangles
    out_end-=1
    for i in range(1,IVpnum-1):
        close_faces.append([n_tri+i,nout+i+1,nout+i])
        close_faces.append([n_tri+i,n_tri+i+1,nout+i+1])
        close_faces.append([out_end+i+1, out_end+i, in_end+i-1])
        close_faces.append([in_end+i-1, in_end+i ,out_end+i+1])

    close_faces = np.array(close_faces)
    
    vertices = np.concatenate((out_vertices, in_vertices))
    faces = np.concatenate((out_faces, in_faces, close_faces))

    # Rotate plot vertices
    rot = R.from_euler('xyz',[-np.pi/2,0.,0.],degrees=False)
    vertices = rot.apply(vertices)

    brute_mesh = Solid.BruteMesh(vertices=vertices, faces=faces)

    stl_nose = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            stl_nose.vectors[i][j] = vertices[f[j],:]

    return brute_mesh, stl_nose


def nose(shape_function = 'cone', radius=.5, length = .5, curve_param = 0, thick = .1, pos=0, OVpnum = 20, Cpnum=20, density = 1e3):
    '''
    Create a Solid representing the nose of the rocket.

    Args:
        shape_function (string): The function giving the nose's shape (see code for available functions).
        radius (float): The radius of the nose (typically similar to rocket's radius).
        length (float): The length of the nose.
        curve_param (number): Curve parameter used in the shape_function (see the definition of each shape_function for more detail).
        thick (float): Thickness of the nose.
        pos (float): Position of nose bottom with respect to rocket's bottom.
        Vpnum (int): Number of points on the curve.
        Cpnum (int): Number of points around the nose.
        density (float): density of the nose in kg/m^3.
        
    Returns:
        A Solid object containing all data necessary to manipulate, plot and calculate properties of the nose.
    '''

    valid_functions = ['tangent_ogive','ellipse','parabole','power_series','haack_series','cone']  # predefined list of valid strings
    assert shape_function in valid_functions, f"Invalid shape function. Valid options are: {', '.join(valid_functions)}"

    # function = getattr(__main__<<the module in which the function is defined, shape_function) Use theses lines for futur code
    # function(x, radius, length, C=curve_param, thick=thick)

    x = np.linspace(0, length, OVpnum, endpoint=True)
    nose_points = eval("nc." + shape_function + "(x, radius, length, C=curve_param, thick=thick)")

    out_vertices = nose_points.out_points
    in_vertices = nose_points.in_points

    rotation_xz = R.from_euler('xyz',angles=[np.pi,0,np.pi], degrees=False)
    transvect = np.array([pos+length, 0, 0])
    out_vertices = translate(rotation_xz.apply(out_vertices), trans_vect  = transvect)
    in_vertices = translate(rotation_xz.apply(in_vertices), trans_vect  = transvect)

    nose_points = nc.Nose(out_vertices,in_vertices)

    out_vertices_to_rotate = out_vertices[1:]
    in_vertices_to_rotate = in_vertices[1:]

    OVpnum = len(out_vertices)
    IVpnum = len(in_vertices)

    out_faces = []
    in_faces = []

    for j in range(1,Cpnum):
        # Rotation and translation of the fin according to its position
        angle = 2*np.pi*j/Cpnum
        rotation = R.from_euler('xyz', angles=[angle,0,0], degrees=False)

        # Rotate and concatenate
        out_vertices = np.concatenate((out_vertices, rotation.apply(out_vertices_to_rotate)))
        in_vertices = np.concatenate((in_vertices, rotation.apply(in_vertices_to_rotate)))

        # Making the triangles on the tip of the nose
        if j == 1:
            # Outer first column of triangles
            out_faces.append([0,1,OVpnum])
            for i in range(1,OVpnum-1):
                out_faces.append([i, OVpnum+i, OVpnum+i-1])
                out_faces.append([i,i+1,OVpnum+i])
            
            # Inner first column of trianges
            in_faces.append([IVpnum,1,0])
            for i in range(1,IVpnum-1):
                in_faces.append([IVpnum+i-1,IVpnum+i,i])
                in_faces.append([IVpnum+i,i+1,i])

        else:
            # Remaining faces on the outer side
            for i in range(OVpnum-2):
                if (i==0):
                    # Single top triangle
                    out_faces.append([0,OVpnum + (OVpnum-1)*(j-2),OVpnum + (OVpnum-1)*(j-1)])
                    # first rectangle
                    left = OVpnum + (OVpnum-1)*(j-2)
                    right = OVpnum + (OVpnum-1)*(j-1)
                    out_faces.append([left, right+1 ,right])
                    out_faces.append([left, left+1 ,right+1])
                else:
                    # other rectangles
                    left = i + OVpnum + (OVpnum-1)*(j-2)
                    right = i + OVpnum + (OVpnum-1)*(j-1)
                    out_faces.append([left, right+1 ,right])
                    out_faces.append([left, left+1 ,right+1])
            # Remaining faces on the inner side
            for i in range(IVpnum-2):
                if (i==0):
                    # Single top triangle
                    in_faces.append([IVpnum + (IVpnum-1)*(j-1),IVpnum + (IVpnum-1)*(j-2),0])
                    # first rectangle
                    left = IVpnum + (IVpnum-1)*(j-2)
                    right = IVpnum + (IVpnum-1)*(j-1)
                    in_faces.append([right,right+1,left])
                    in_faces.append([right+1,left+1,left])
                else:
                    # other rectangles
                    left = i + IVpnum + (IVpnum-1)*(j-2)
                    right = i + IVpnum + (IVpnum-1)*(j-1)
                    in_faces.append([right,right+1,left])
                    in_faces.append([right+1,left+1,left])

    # Last column of outer side
    for i in range(OVpnum-1):
        end = OVpnum + (OVpnum-1)*(Cpnum-2)
        if i == 0:
            out_faces.append([end,1,0])
        else:
            out_faces.append([end+i-1,end+i,i+1])
            out_faces.append([end+i-1,i+1,i])
    # Last column of inner side
    for i in range(IVpnum-1):
        end = IVpnum + (IVpnum-1)*(Cpnum-2)
        if i == 0:
            in_faces.append([0,1,end])
        else:
            in_faces.append([i+1,end+i,end+i-1])
            in_faces.append([i,i+1,end+i-1])

    nout = len(out_vertices)
    nin = len(in_vertices)

    out_faces = np.array(out_faces)
    in_faces = np.array(in_faces) + nout

    # Closing the nose
    close_faces = []
    for i in range(1,Cpnum):
        top_r, top_l = i*(OVpnum-1), (i+1)*(OVpnum-1)
        bot_r, bot_l = i*(IVpnum-1)+nout, (i+1)*(IVpnum-1)+nout
        close_faces.append([top_r, top_l, bot_r])
        close_faces.append([top_l, bot_l, bot_r])
    top_r, top_l = nout-1, OVpnum-1
    bot_r, bot_l = nin-1+nout, (IVpnum-1)+nout
    close_faces.append([top_r, top_l, bot_r])
    close_faces.append([top_l, bot_l, bot_r])

    close_faces = np.array(close_faces)

    vertices = np.concatenate((out_vertices, in_vertices))
    faces = np.concatenate((out_faces, in_faces, close_faces))

    brute_mesh = Solid.BruteMesh(vertices=vertices, faces=faces)

    nose = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            nose.vectors[i][j] = vertices[f[j],:]

    plot_brute_mesh, plot_nose = half_nose(nose_points, Cpnum = Cpnum//2)

    return Solid(brute_mesh=brute_mesh, stl_mesh=nose, plot_brute_mesh=plot_brute_mesh, plot_stl_mesh=plot_nose, density = density)