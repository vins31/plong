import bpy
from mathutils.geometry import distance_point_to_plane
from mathutils import Vector, Matrix

mesh = bpy.data.meshes['Icosphere']
ob = bpy.data.objects['Icosphere']
volume = 0
m100 = m010 = m001 = 0 # Geometric moments
orig = Vector((0,0,0))
eps = 1e-15

for face in mesh.faces:
    distance = distance_point_to_plane(orig, face.center, face.normal)
    # minus sign, assuming normals are directed towards the outside
    face_vol = - face.area * distance / 3
    volume += face_vol
    nb_edges = len(face.vertices)
    
    if nb_edges == 3:
        v = [mesh.vertices[face.vertices[i]].co for i in range(3)]
        m100 += face_vol * (v[0][0] + v[1][0] + v[2][0]) / 4
        m010 += face_vol * (v[0][1] + v[1][1] + v[2][1]) / 4
        m001 += face_vol * (v[0][2] + v[1][2] + v[2][2]) / 4
    elif nb_edges == 4:
        # let's cut the quad in triangles!
        v = [mesh.vertices[face.vertices[i]].co for i in range(4)]
        m100 += face_vol * (v[0][0] + v[1][0] + v[2][0] + v[3][0]) / 4
        m010 += face_vol * (v[0][1] + v[1][1] + v[2][1] + v[3][1]) / 4
        m001 += face_vol * (v[0][2] + v[1][2] + v[2][2] + v[3][2]) / 4
        
print("Volume: %s" % volume)
print("CoG: %s, %s, %s" % (m100, m010, m001))

center_of_gravity = Vector((m100, m010, m001))
point_a = mesh.faces[0].center # completely arbitrary

intersections_count = 0

# http://blenderartists.org/forum/showthread.php?195605-Detecting-if-a-point-is-inside-a-mesh-2.5-API
orig = center_of_gravity
axis = mesh.faces[0].center
while True:
    location, normal, index = ob.ray_cast(orig, orig + axis * 10000.0)
    if index == -1:
        break
    intersections_count += 1
    orig = location + axis * 0.00001

print("Number of intersections: %s" % intersections_count)

if intersections_count % 2 == 0:
    print("Center of gravity is outside the object.\n")
else:
    print("Center of gravity is inside the object.\n")