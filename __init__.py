import bpy
import mathutils
import bgl
from . import utils


bl_info = {
    "name": "Axis Measure",
    "author": "MehmetHY",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "3D View -> N Panel -> View -> Axis Measure",
    "description": "Draws the distance between the two vertices of an edge.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/MehmetHY/BlenderEasyGridResizer",
    "category": "3D View"
}


global_vars = {'Active': False, 'Handler2D': None, 'Handler3D': None}

def draw_edge_lines_callback(self, context):
    bgl.glEnable(bgl.GL_BLEND)
    for coord in self._edge_coords:
        if bpy.context.scene.axis_measure_props.show_x_line:
            self.draw_x_line(coord[0], coord[1])
        if bpy.context.scene.axis_measure_props.show_y_line:
            self.draw_y_line(coord[0], coord[1])
        if bpy.context.scene.axis_measure_props.show_z_line:
            self.draw_z_line(coord[0], coord[1])
    bgl.glDisable(bgl.GL_BLEND)

def draw_edge_length_callback(self, context):
    for coord in self._edge_coords:
        if bpy.context.scene.axis_measure_props.show_length:
            self.draw_edge_length(coord[0], coord[1])
        if bpy.context.scene.axis_measure_props.show_x_length:
            self.draw_x_length(coord[0], coord[1])
        if bpy.context.scene.axis_measure_props.show_y_length:
            self.draw_y_length(coord[0], coord[1])
        if bpy.context.scene.axis_measure_props.show_z_length:
            self.draw_z_length(coord[0], coord[1])
    

class axis_measurement_props(bpy.types.PropertyGroup):
    show_length: bpy.props.BoolProperty(name='Show Length', description='Show Length', default=True)
    show_x_length: bpy.props.BoolProperty(name='Show X Value', description='Show X Value', default=True)
    show_x_line: bpy.props.BoolProperty(name='Show X Line', description='Show X Line', default=True)
    show_y_length: bpy.props.BoolProperty(name='Show Y Value', description='Show Y Value', default=True)
    show_y_line: bpy.props.BoolProperty(name='Show Y Line', description='Show Y Line', default=True)
    show_z_length: bpy.props.BoolProperty(name='Show Z Value', description='Show Z Value', default=True)
    show_z_line: bpy.props.BoolProperty(name='Show Z Line', description='Show Z Line', default=True)

    precision: bpy.props.IntProperty(name='Precision', description='Precision of the float value', default=2, min=0, max=15)

    length_font_size: bpy.props.IntProperty(name='Length Font Size', description='Length Font Size', default=36, min=12, max=64)
    length_font_color: bpy.props.FloatVectorProperty(name='Length Font Color', description='Length Font Color', size=4, subtype='COLOR', default=(1, 1, 1, 1), min=0, max=1)
    
    x_font_size: bpy.props.IntProperty(name='X Font Size', description='X Font Size', default=24, min=8, max=64)
    x_font_color: bpy.props.FloatVectorProperty(name='X Font Color', description='X Font Color', size=4, subtype='COLOR', default=(1, 0, 0, 1), min=0, max=1)
    x_line_width: bpy.props.IntProperty(name='X-Axis Line Width', description='X-Axis Line Width', default=1, min=1, max=12)
    x_line_color: bpy.props.FloatVectorProperty(name='X-Axis Line Color', description='X-Axis Line Color', size=4, subtype='COLOR', default=(1, 0, 0, 1), min=0, max=1)
    
    y_font_size: bpy.props.IntProperty(name='Y Font Size', description='Y Font Size', default=24, min=8, max=64)
    y_font_color: bpy.props.FloatVectorProperty(name='Y Font Color', description='Y Font Color', size=4, subtype='COLOR', default=(0, 1, 0, 1), min=0, max=1)
    y_line_width: bpy.props.IntProperty(name='Y-Axis Line Width', description='Y-Axis Line Width', default=1, min=1, max=12)
    y_line_color: bpy.props.FloatVectorProperty(name='Y-Axis Line Color', description='Y-Axis Line Color', size=4, subtype='COLOR', default=(0, 1, 0, 1), min=0, max=1)
    
    z_font_size: bpy.props.IntProperty(name='Z Font Size', description='Z Font Size', default=24, min=8, max=64)
    z_font_color: bpy.props.FloatVectorProperty(name='Z Font Color', description='Z Font Color', size=4, subtype='COLOR', default=(0, 0, 1, 1), min=0, max=1)
    z_line_width: bpy.props.IntProperty(name='Z-Axis Line Width', description='Z-Axis Line Width', default=1, min=1, max=12)
    z_line_color: bpy.props.FloatVectorProperty(name='Z-Axis Line Color', description='Z-Axis Line Color', size=4, subtype='COLOR', default=(0, 0, 1, 1), min=0, max=1)


class axis_measurement_panel(bpy.types.Panel):
    bl_idname = 'AXISMEASUREMENT_PT_main_panel'
    bl_label = 'Axis Measure'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'
    bl_category = 'View'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (bpy.context.object != None and bpy.context.object.mode == 'EDIT')
    
    def draw(self, context):
        measure_props = bpy.context.scene.axis_measure_props
        layout = self.layout

class axis_measurement_panel_show(bpy.types.Panel):
    bl_idname = 'AXISMEASUREMENT_PT_show_panel'
    bl_label = 'Show / Hide'
    bl_parent_id = 'AXISMEASUREMENT_PT_main_panel'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        measure_props = bpy.context.scene.axis_measure_props
        layout = self.layout

        box = layout.box()
        box.operator('view3d.axis_measurement', text='Start / Stop')
        box.separator()
        box.prop(measure_props, 'precision')
        box.separator()
        box.prop(measure_props, 'show_length')
        box.separator()
        box.prop(measure_props, 'show_x_length')
        box.prop(measure_props, 'show_x_line')
        box.separator()
        box.prop(measure_props, 'show_y_length')
        box.prop(measure_props, 'show_y_line')
        box.separator()
        box.prop(measure_props, 'show_z_length')
        box.prop(measure_props, 'show_z_line')

class axis_measurement_panel_size(bpy.types.Panel):
    bl_idname = 'AXISMEASUREMENT_PT_size_panel'
    bl_label = 'Size'
    bl_parent_id = 'AXISMEASUREMENT_PT_main_panel'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        measure_props = bpy.context.scene.axis_measure_props
        layout = self.layout

        box = layout.box()
        box.prop(measure_props, 'length_font_size')
        box.separator()
        box.prop(measure_props, 'x_font_size')
        box.prop(measure_props, 'y_font_size')
        box.prop(measure_props, 'z_font_size')
        box.separator()
        box.prop(measure_props, 'x_line_width')
        box.prop(measure_props, 'y_line_width')
        box.prop(measure_props, 'z_line_width')

class axis_measurement_panel_color(bpy.types.Panel):
    bl_idname = 'AXISMEASUREMENT_PT_color_panel'
    bl_label = 'Color'
    bl_parent_id = 'AXISMEASUREMENT_PT_main_panel'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        measure_props = bpy.context.scene.axis_measure_props
        layout = self.layout

        box = layout.box()
        box.prop(measure_props, 'length_font_color')
        box.separator()
        box.prop(measure_props, 'x_font_color')
        box.prop(measure_props, 'y_font_color')
        box.prop(measure_props, 'z_font_color')
        box.separator()
        box.prop(measure_props, 'x_line_color')
        box.prop(measure_props, 'y_line_color')
        box.prop(measure_props, 'z_line_color')


class axis_measurement(bpy.types.Operator):
    bl_idname = 'view3d.axis_measurement'
    bl_label = 'Draw Edge Length'
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        if not bpy.context.object.mode == 'EDIT' or not global_vars['Active']:
            self.deactivate()
            context.area.tag_redraw()
            return {'FINISHED'}
        self._edge_coords = utils.mesh_get_selected_edges_coords()
        context.area.tag_redraw()
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        global_vars['Active'] = not global_vars['Active']
        self._args = (self, context)
        if global_vars['Active']:
            self._edge_coords = []
            bpy.context.window_manager.modal_handler_add(self)
            global_vars['Handler2D'] = bpy.types.SpaceView3D.draw_handler_add(draw_edge_length_callback, self._args, 'WINDOW', 'POST_PIXEL')
            global_vars['Handler3D'] = bpy.types.SpaceView3D.draw_handler_add(draw_edge_lines_callback, self._args, 'WINDOW', 'POST_VIEW')
            return {'RUNNING_MODAL'}
        self.deactivate()
        context.area.tag_redraw()
        return {'FINISHED'}
    
    def deactivate(self):
        if global_vars['Handler2D'] != None:
            bpy.types.SpaceView3D.draw_handler_remove(global_vars['Handler2D'], 'WINDOW')
            global_vars['Handler2D'] = None
        if global_vars['Handler3D'] != None:
            bpy.types.SpaceView3D.draw_handler_remove(global_vars['Handler3D'], 'WINDOW')
            global_vars['Handler3D'] = None
        global_vars['Active'] = False


    def draw_edge_length(self, start: mathutils.Vector, end: mathutils.Vector):
        vector = mathutils.Vector(end - start)
        mid = mathutils.Vector((end + start) / 2.0)
        utils.draw_text_3d(format(vector.length, f'.{bpy.context.scene.axis_measure_props.precision}f'), mid, bpy.context.scene.axis_measure_props.length_font_size, bpy.context.scene.axis_measure_props.length_font_color)
    
    def draw_x_length(self, start: mathutils.Vector, end: mathutils.Vector):
        dist = end[0] - start[0]
        if dist == 0:
            return
        if dist < 0:
            dist = -dist
        pos = (end[0], start[1], start[2])
        mid = (((start[0] + pos[0]) / 2.0), ((start[1] + pos[1]) / 2.0), ((start[2] + pos[2]) / 2.0))
        utils.draw_text_3d(format(dist, f'.{bpy.context.scene.axis_measure_props.precision}f'), mid, bpy.context.scene.axis_measure_props.x_font_size, bpy.context.scene.axis_measure_props.x_font_color)
    
    def draw_x_line(self, start: mathutils.Vector, end: mathutils.Vector):
        dist = end[0] - start[0]
        if dist == 0:
            return
        pos = (end[0], start[1], start[2])
        utils.draw_line_3d(start, pos, bpy.context.scene.axis_measure_props.x_line_width, bpy.context.scene.axis_measure_props.x_line_color)
    
    def draw_y_length(self, start: mathutils.Vector, end: mathutils.Vector):
        dist = end[1] - start[1]
        if dist == 0:
            return
        if dist < 0:
            dist = -dist
        pos1 = (end[0], start[1], start[2])
        pos2 = (end[0], end[1], pos1[2])
        mid = (((pos1[0] + pos2[0]) / 2.0), ((pos1[1] + pos2[1]) / 2.0), ((pos1[2] + pos2[2]) / 2.0))
        utils.draw_text_3d(format(dist, f'.{bpy.context.scene.axis_measure_props.precision}f'), mid, bpy.context.scene.axis_measure_props.y_font_size, bpy.context.scene.axis_measure_props.y_font_color)
    
    def draw_y_line(self, start: mathutils.Vector, end: mathutils.Vector):
        dist = end[1] - start[1]
        if dist == 0:
            return
        pos1 = (end[0], start[1], start[2])
        pos2 = (end[0], end[1], pos1[2])
        utils.draw_line_3d(pos1, pos2, bpy.context.scene.axis_measure_props.y_line_width, bpy.context.scene.axis_measure_props.y_line_color)
    
    def draw_z_length(self, start: mathutils.Vector, end: mathutils.Vector):
        dist = end[2] - start[2]
        if dist == 0:
            return
        if dist < 0:
            dist = -dist
        pos1 = (end[0], end[1], start[2])
        pos2 = (end[0], end[1], end[2])
        mid = (((pos1[0] + pos2[0]) / 2.0), ((pos1[1] + pos2[1]) / 2.0), ((pos1[2] + pos2[2]) / 2.0))
        utils.draw_text_3d(format(dist, f'.{bpy.context.scene.axis_measure_props.precision}f'), mid, bpy.context.scene.axis_measure_props.z_font_size, bpy.context.scene.axis_measure_props.z_font_color)
    
    def draw_z_line(self, start: mathutils.Vector, end: mathutils.Vector):
        dist = end[2] - start[2]
        if dist == 0:
            return
        pos1 = (end[0], end[1], start[2])
        pos2 = (end[0], end[1], end[2])
        utils.draw_line_3d(pos1, pos2, bpy.context.scene.axis_measure_props.z_line_width, bpy.context.scene.axis_measure_props.z_line_color)

classes_to_register = (axis_measurement_props, axis_measurement, axis_measurement_panel, axis_measurement_panel_show, axis_measurement_panel_size, axis_measurement_panel_color)

def register():
    for cls in classes_to_register:
        bpy.utils.register_class(cls)
    bpy.types.Scene.axis_measure_props = bpy.props.PointerProperty(type=axis_measurement_props)

def unregister():
    for cls in classes_to_register:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.axis_measure_props

if __name__ == '__main__':
    register()
    global_vars['Active'] = False

