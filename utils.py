import bpy
import bmesh
import bpy_extras
import gpu
import gpu_extras
import bgl
import blf
import mathutils


# Object

def object_get_active():
    obj = bpy.context.active_object
    return obj

def object_get_selected():
    objs = bpy.context.selected_objects
    return objs


# Mesh

def mesh_create_bmesh_object_from_edit_object():
    bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    return bm

def mesh_create_bmesh_objects_from_selected_objects():
    objs = bpy.context.selected_objects
    selected_objs = [obj for obj in objs if obj.select_get()]
    bms = []
    for obj in selected_objs:
        bm = bmesh.from_edit_mesh(obj.data)
        bms.append(bm)
    return bms


def mesh_get_active_element():
    obj = object_get_active()
    if obj == None:
        print('no active object')
        return None
    bm = bmesh.from_edit_mesh(obj.data)
    elem = bm.select_history.active
    return elem

def mesh_get_selected_vertices_from_selected_objects(stay_in_edit_mode = False):
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    all_selected_verts = []
    objs = object_get_selected()
    for obj in objs:
        bm = bmesh.from_edit_mesh(obj.data)
        elems = []
        for vert in bm.verts:
            if vert.select:
                elems.append(vert)
        all_selected_verts.extend(elems)
    if not stay_in_edit_mode:
        bpy.ops.object.mode_set(mode=mode)
    return all_selected_verts

def mesh_get_selected_edges_from_selected_objects(stay_in_edit_mode = False):
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    all_selected_edges = []
    objs = object_get_selected()
    for obj in objs:
        bm = bmesh.from_edit_mesh(obj.data)
        elems = []
        for edge in bm.edges:
            if edge.select:
                elems.append(edge)
        all_selected_edges.extend(elems)
    if not stay_in_edit_mode:
        bpy.ops.object.mode_set(mode=mode)
    return all_selected_edges

def mesh_get_selected_faces_from_selected_objects(stay_in_edit_mode = False):
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    all_selected_faces = []
    objs = object_get_selected()
    for obj in objs:
        bm = bmesh.from_edit_mesh(obj.data)
        elems = []
        for face in bm.faces:
            if face.select:
                elems.append(face)
        all_selected_faces.extend(elems)
    if not stay_in_edit_mode:
        bpy.ops.object.mode_set(mode=mode)
    return all_selected_faces

def mesh_get_normals_of_selected_edges():
    normals = []
    edges = mesh_create_bmesh_object_from_edit_object().edges
    for edge in edges:
        edge.normal_update()
        normal = (edge.verts[0].normal + edge.verts[1].normal) / 2.0
        normals.append(normal)
    return normals

def mesh_get_selected_edges_coords():
    objs = [obj for obj in object_get_selected() if obj.mode == 'EDIT']
    coords = []
    for obj in objs:
        bm = bmesh.from_edit_mesh(obj.data)
        for edge in bm.edges:
            if edge.select:
                vert1 = mathutils.Vector((edge.verts[0].co[0], edge.verts[0].co[1], edge.verts[0].co[2]))
                vert2 = mathutils.Vector((edge.verts[1].co[0], edge.verts[1].co[1], edge.verts[1].co[2]))
                vert1 = obj.matrix_world @ vert1
                vert2 = obj.matrix_world @ vert2
                coords.append((vert1, vert2))

    return coords


# Draw

def draw_text_3d(text, pos, size, color):
    pos_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.region_data, pos)
    blf.position(0, pos_2d[0], pos_2d[1], 0)
    blf.color(0, color[0], color[1], color[2], color[3])
    blf.size(0, size, bpy.context.preferences.system.dpi)
    blf.draw(0, f'{text}')

def draw_line_3d(start, end, width, color):
    shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR') 
    bgl.glLineWidth(width)
    shader.bind()
    shader.uniform_float('color', color)
    batch = gpu_extras.batch.batch_for_shader(shader, 'LINES', {"pos": [start, end]})
    batch.draw(shader)