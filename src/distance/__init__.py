bl_info = {
    "name": "My Blender Addon",
    "blender": (4, 2, 1),  # Ваша версія Blender
    "category": "Object",
    "description": "Допоможе отримати дистанцію між двома вершинами",
    "author": "Сергій Ходак",
    "version": (1, 0),
    "support": "COMMUNITY",
}

import bpy # Бібліотека для праці з blender
from .distance import Distance
from bpy.props import PointerProperty
import bmesh
import bpy_extras.view3d_utils

bpy.types.Scene.x1 = bpy.props.FloatProperty(name="X1", default=0.0)
bpy.types.Scene.y1 = bpy.props.FloatProperty(name="Y1", default=0.0)
bpy.types.Scene.z1 = bpy.props.FloatProperty(name="Z1", default=0.0)
bpy.types.Scene.x2 = bpy.props.FloatProperty(name="X2", default=0.0)
bpy.types.Scene.y2 = bpy.props.FloatProperty(name="Y2", default=0.0)
bpy.types.Scene.z2 = bpy.props.FloatProperty(name="Z2", default=0.0)
bpy.types.Scene.distance_result = bpy.props.FloatProperty(name="Відстань", default=0.0)


def get_vertex_coordinates(context, event):
    # Отримання об'єкта та його даних
    obj = context.active_object
    
    if obj is None or obj.type != 'MESH':
        print("Об'єкт не обрано або це не меш.")
        return

    # Переключення в режим об'єкта
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = obj.data

    # Створення bmesh для роботи з вершинами
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Отримання координат вершини під курсором
    region = context.region
    rv3d = context.space_data.region_3d
    coord = (event.mouse_region_x, event.mouse_region_y)
    #depth_location = bpy_extras.view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    location = bpy_extras.view3d_utils.region_2d_to_location_3d(region, rv3d, coord, (0, 0, 0))

    # Пошук найближчої вершини
    closest_vertex = None
    min_distance = float('inf') # плюс безкінечність
    for v in bm.verts:
        distance = (v.co - location).length
        if distance < min_distance:
            closest_vertex = v
            min_distance = distance

    # Виведення координат найближчої вершини
    if closest_vertex:
        print("Координати вершини:", closest_vertex.co)
        
    # Звільнення bmesh
    bm.free()
    
    # Повернення в режим редагування
    bpy.ops.object.mode_set(mode='EDIT')

class SimpleOperator(bpy.types.Operator):
    bl_idname = "view3d.simple_operator"
    bl_label = "Simple Operator"

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if context.area.type == 'VIEW_3D':
                get_vertex_coordinates(context, event)
                return {'FINISHED'}
        elif event.type == 'ESC':
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':  # Працюємо тільки в 3D View
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Будь ласка, натисніть у 3D View")
            return {'CANCELLED'}

class GetDistanceOperator(bpy.types.Operator):
    bl_idname = "object.get_2d_distance"
    bl_label = "Обчислити"

    def execute(self, context):
        x1 = context.scene.x1
        y1 = context.scene.y1
        x2 = context.scene.x2
        y2 = context.scene.y2
        distance_2d = Distance()
        distance_2d.get_2d_distance(x1, y1, x2, y2)
        context.scene.distance_result = distance_2d.distance_result
        return {'FINISHED'}

class CopyDistanceOperator(bpy.types.Operator):
    bl_idname = "object.copy_distance"
    bl_label = "Копіювати"

    def execute(self, context):
        bpy.context.window_manager.clipboard = str(context.scene.distance_result)
        self.report({'INFO'}, "Відстань скопійовано!")
        return {'FINISHED'}

#def get_active_vertex_coords():
#    # Перевіряємо, чи об'єкт в режимі редагування
#    if bpy.context.object.mode == 'EDIT':
#        # Отримуємо меш
#        mesh = bmesh.from_edit_mesh(bpy.context.object.data)
#
#        # Знаходимо активну вершину
#        active_verts = [v for v in mesh.verts if v.select]
#
#        # Якщо є активна вершина, повертаємо її координати
#        if active_verts:
#            active_vertex = active_verts[0]
#            return active_vertex.co
#        else:
#            print("Немає активних вершин")
#            return None
#    else:
#        print("Об'єкт не в режимі редагування")
#        return None
#
#def modal_operator(self, context, event):
#    if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
#        # Викликаємо оператор для вибору вершини
#        bpy.ops.view3d.select('INVOKE_DEFAULT', extend=False)
#
#        # Отримуємо координати активної вершини після вибору
#        coords = get_active_vertex_coords()
#        if coords:
#            print(f"Координати активної вершини: {coords}")
#        return {'FINISHED'}
#    return {'PASS_THROUGH'}
#
#class SimpleOperator(bpy.types.Operator):
#    bl_idname = "object.select_and_get_vertex_coords"
#    bl_label = "Вибрати та отримати координати вершини"
#    bl_options = {'REGISTER', 'UNDO'}
#
#    def modal(self, context, event):
#        return modal_operator(self, context, event)
#
#    def invoke(self, context, event):
#        if context.object:
#            context.window_manager.modal_handler_add(self)
#            return {'RUNNING_MODAL'}
#        else:
#            self.report({'WARNING'}, "Немає об'єкта")
#            return {'CANCELLED'}

# малює панель в самому блендері
class DistancePanel(bpy.types.Panel):
    bl_label = "Distance Calculator"
    bl_idname = "OBJECT_PT_distance_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Distance"

    # що саме малювати в панелі
    def draw(self, context):
        layout = self.layout

        # Розділ для розрахунку відстані
        layout.label(text="Введіть координати:")
        row = layout.row()
        row.prop(context.scene, "x1", text="X1")
        row.prop(context.scene, "y1", text="Y1")
        row = layout.row()
        row.prop(context.scene, "x2", text="X2")
        row.prop(context.scene, "y2", text="Y2")
        layout.operator("object.get_2d_distance", text="Обчислити")
        layout.label(text="Відстань:")
        layout.label(text=str(context.scene.distance_result))
        layout.operator("object.copy_distance", text="Копіювати")

        # Розділ для властивостей об'єкта
        layout.separator()
        layout.label(text="Властивості об'єкта:")
        col = layout.column()
        col.prop(context.scene, "prop")

#        # спроби створити піпетку для вершин
#        layout.separator()
#        layout.label(text="Піпетка координат вершини:")
#        row = layout.row()
#        row.prop(context.scene, "x1", text="X1")
#        row.prop(context.scene, "y1", text="Y1")
#        #row.prop(context.scene, "z1", text="Z1")
#        row = layout.row()
#        row.prop(context.scene, "x2", text="X2")
#        row.prop(context.scene, "y2", text="Y2")
#        #row.prop(context.scene, "z2", text="Z2")
#        layout.operator("object.select_and_get_vertex_coords",
#                        text="SimpleOperator")
        layout.separator()
        layout.label(text="Піпетка:")
        col = layout.column()
        col.prop(context.scene, "x1", text="X1")
        col.prop(context.scene, "y1", text="Y1")
        col.prop(context.scene, "z1", text="Z1")
        layout.operator("view3d.simple_operator",
                                text="ЛКМ")


class TEST_PT_layoyt_panel(bpy.types.Panel):
    bl_label = "Prop Panels"
    bl_category = "Test Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = layout.column()
        col.prop_search(scene, "prop", context.scene, "objects")
        #or
        col.prop(scene, "prop")


# Реєстрація класів
classes = (
    SimpleOperator,
    GetDistanceOperator,
#    SimpleOperator,
    DistancePanel,
    CopyDistanceOperator,
    TEST_PT_layoyt_panel
)



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
    bpy.types.Scene.prop = PointerProperty(type=bpy.types.Object)
    bpy.ops.view3d.simple_operator('INVOKE_DEFAULT')
