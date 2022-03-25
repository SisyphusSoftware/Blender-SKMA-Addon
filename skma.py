bl_info = {
        "name": "Shape Key Modifiers Applicator (SKMA)",
        "author": "Sisyphus Software",
        "version": (1,0),
        "blender": (3,0,1)
    }

import bpy
#import bpy.data
import bpy.ops
from bpy.types import Menu, Operator

class SKMA(bpy.types.Operator):
    bl_idname = "mesh.skma"
    bl_label = "SKMA"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        so = bpy.context.active_object
        if so.data.shape_keys != None:
            variants = []
            main_shape_keys = []
            shape_key_lists = []
            #make one copy of the mesh for each shape key
            for i in range(len(so.data.shape_keys.key_blocks)):
                if i != 0:
                    bpy.ops.object.duplicate_move()
                so = bpy.context.active_object
                variants.append(so)
                main_shape_keys.append(variants[i].data.shape_keys.key_blocks[i])
            for i in range(len(so.data.shape_keys.key_blocks)):
                #rename the copies as their corresponding shape keys
                if i != 0:
                    variants[i].name = variants[i].data.shape_keys.key_blocks[i].name
                variants[i].active_shape_key_index = 0
                shape_key_lists.append(variants[i].data.shape_keys.key_blocks)
                #delete all the shape keys in the correct order 
                if len(shape_key_lists[i]) > 1:
                    main_shape_key_found = 0
                    for j in range(len(shape_key_lists[i])):
                        if variants[i].data.shape_keys.key_blocks[0] == main_shape_keys[i] and main_shape_key_found == 0:
                            main_shape_key_found = 1
                        if main_shape_key_found == 0:
                            variants[i].shape_key_remove(variants[i].data.shape_keys.key_blocks[0])
                        elif main_shape_key_found == 1 and len(variants[i].data.shape_keys.key_blocks) > 1:
                            variants[i].shape_key_remove(variants[i].data.shape_keys.key_blocks[1])
                variants[i].shape_key_remove(variants[i].data.shape_keys.key_blocks[0])
            #apply all the modifiers
            for i in range(len(variants)):
                bpy.data.objects[variants[i].name].select_set(True)
                bpy.ops.object.convert(target='MESH')
                for j in range(len(variants[i].modifiers)):
                    bpy.ops.object.modifier_apply(modifier=variants[i].modifiers[0].name)
                bpy.data.objects[variants[i].name].select_set(False)
                if i != 0:
                    bpy.data.objects[variants[i].name].select_set(True)
            #apply the copies back as shape keys to the original
            bpy.context.view_layer.objects.active = bpy.data.objects[variants[0].name]
            bpy.ops.object.join_shapes()
            #delete all the copies
            bpy.ops.object.delete()
        return{'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SKMA.bl_idname)

def register():
    bpy.utils.register_class(SKMA)
   # bpy.types.TOPBAR_MT_app_system.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SKMA)

if __name__ == '__main__':
    register()