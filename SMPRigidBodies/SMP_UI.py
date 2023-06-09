# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####
# Copyright © 2023, OpheliaComplex.

import bpy
from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       EnumProperty)
from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)


class SMP_OT_actions_ncwt(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "no_collide_with_tags.list_action"
    bl_label = "No Collide With Tags list actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        obj = context.active_object
        idx = obj.no_collide_with_tags_index

        try:
            item = obj.no_collide_with_tags[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(obj.no_collide_with_tags) - 1:
                item_next = obj.no_collide_with_tags[idx + 1].name
                obj.no_collide_with_tags.move(idx, idx + 1)
                obj.no_collide_with_tags_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.no_collide_with_tags_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = obj.no_collide_with_tags[idx - 1].name
                obj.no_collide_with_tags.move(idx, idx - 1)
                obj.no_collide_with_tags_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.no_collide_with_tags_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (obj.no_collide_with_tags[idx].name)
                obj.no_collide_with_tags_index -= 1
                obj.no_collide_with_tags.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            item = obj.no_collide_with_tags.add()
            item.name = "tag"
            item.obj_id = len(obj.no_collide_with_tags)
            obj.no_collide_with_tags_index = len(obj.no_collide_with_tags) - 1

        return {"FINISHED"}


class SMP_OT_defaultTags_ncwt(Operator):
    """Fill with default no collide with tags"""
    bl_idname = "no_collide_with_tags.default_tags"
    bl_label = "Fill default tags"
    bl_description = "Fill with default collision tags"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        for tag in ["body", "hair", "hands", "head"]:
            item = context.active_object.no_collide_with_tags.add()
            item.name = tag
            item.obj_id = len(context.active_object.no_collide_with_tags)
            context.active_object.no_collide_with_tags_index = len(context.active_object.no_collide_with_tags) - 1
        return {'FINISHED'}

class SMP_OT_actions_cwt(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "collide_with_tags.list_action"
    bl_label = "Collide With Tags list actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        obj = context.active_object
        idx = obj.collide_with_tags_index

        try:
            item = obj.collide_with_tags[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(obj.collide_with_tags) - 1:
                item_next = obj.collide_with_tags[idx + 1].name
                obj.collide_with_tags.move(idx, idx + 1)
                obj.collide_with_tags_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.collide_with_tags_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = obj.collide_with_tags[idx - 1].name
                obj.collide_with_tags.move(idx, idx - 1)
                obj.collide_with_tags_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.collide_with_tags_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (obj.collide_with_tags[idx].name)
                obj.collide_with_tags_index -= 1
                obj.collide_with_tags.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            item = obj.collide_with_tags.add()
            item.name = "tag"
            item.obj_id = len(obj.collide_with_tags)
            obj.collide_with_tags_index = len(obj.collide_with_tags) - 1

        return {"FINISHED"}


class SMP_OT_defaultTags_cwt(Operator):
    """Fill with default no collide with tags"""
    bl_idname = "collide_with_tags.default_tags"
    bl_label = "Fill default tags"
    bl_description = "Fill with default collision tags"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        for tag in ["body", "hair", "hands", "head"]:
            item = context.active_object.collide_with_tags.add()
            item.name = tag
            item.obj_id = len(context.active_object.collide_with_tags)
            context.active_object.collide_with_tags_index = len(context.active_object.collide_with_tags) - 1
        return {'FINISHED'}

class SMP_UL_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, "name", text="", emboss=False)

    def invoke(self, context, event):
        pass


class SMP_PT_CollisionPropertiesPanel(Panel):
    """Custom panel in the rigid body physics properties area
    Containing a list of tags to not collide with"""

    bl_idname = "SMPRIGIDBODIES_PT_CollisionPropertiesPanel"
    bl_label = "SMPRigidBodies_CollisionPropertiesPanel"

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"

    @classmethod
    def poll(cls, context):
        # Only show this panel if an object is selected and it has a rigid body
        return (context.object is not None) and (context.object.rigid_body is not None)

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        type_row = layout.row()
        type_row.prop(obj, "smp_col_type", text="collision type")
        row = layout.row()
        row.prop(obj, "smp_col_privacy", text="shared")
        tag_row = layout.row()
        tag_row.prop(obj, "smp_tag", text="tag")

        # ************* NO COLLIDE WITH TAGS *************

        desc_row = layout.row()
        desc_row.label(text="no-collide-with-tags")

        rows = 2
        row = layout.row()
        row.template_list("SMP_UL_items", "", obj, "no_collide_with_tags", obj, "no_collide_with_tags_index", rows=rows)

        col = row.column(align=True)
        col.operator("no_collide_with_tags.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("no_collide_with_tags.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("no_collide_with_tags.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("no_collide_with_tags.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("no_collide_with_tags.default_tags", icon="ADD")

        # ************ COLLIDE WITH TAGS ************

        desc_row = layout.row()
        desc_row.label(text="no-collide-with-tags")

        rows = 2
        row = layout.row()
        row.template_list("SMP_UL_items", "", obj, "collide_with_tags", obj, "collide_with_tags_index", rows=rows)

        col = row.column(align=True)
        col.operator("collide_with_tags.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("collide_with_tags.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("collide_with_tags.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("collide_with_tags.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("collide_with_tags.default_tags", icon="ADD")
# -------------------------------------------------------------------
#   Injection in Rigid Body Bones panel
# -------------------------------------------------------------------
def rigid_body_menu(self, context):
    self.layout.menu("VIEW3D_MT_pose_rigid_body_extras")

class SMP_Props_that_dont_exist_in_blender(bpy.types.PropertyGroup):

    inertia: bpy.props.FloatProperty(
        name="inertia",
        description="The (x,y,z) inertia of the bone, final inertia is computed as 1/<this inertia value>. Using the "
                    "default value is strongly recommended, default: 1.0.",
        default=1.0,
        min=0.0,
        max=100.0,
        precision=1,
        step=0.1,
        unit='NONE',
    )

    gravity_factor: bpy.props.FloatProperty(
        name="gravity factor",
        description="Will be applied to the gravity of the bone, default: 1.0.",
        default=1.0,
        min=0.0,
        max=10.0,
        precision=2,
        step=0.1,
        unit='NONE',
    )

    rolling_friction: bpy.props.FloatProperty(
        name="rolling friction",
        description="Unknown, default: 0.0.",
        default=0.0,
        min=0.0,
        max=1.0,
        precision=2,
        step=0.1,
        unit='NONE',
    )

    margin_multiplier: bpy.props.FloatProperty(
        name="margin multiplier",
        description="Unknown, default: 1.0.",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=2,
        step=0.1,
        unit='NONE',
    )

    @classmethod
    def register(cls):
        bpy.types.Bone.rigid_body_bones_extra_props = bpy.props.PointerProperty(type=cls)

    @classmethod
    def unregister(cls):
        del bpy.types.Bone.rigid_body_bones_extra_props

class RBBExtraProps(bpy.types.Panel):
    bl_idname = "DATA_PT_rigid_body_bones_extra_properties"
    bl_label = "EXTRA SMP Rigid Bodies properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigid Body Bones"
    bl_parent_id = "DATA_PT_rigid_body_bones_bone"
    bl_options = set()
    bl_order = 6

    def draw(self, context):
        data = context.active_object.data.bones.active.rigid_body_bones_extra_props
        layout = self.layout
        row = layout.row()
        # add some text describing these properties
        row.label(text="These properties have no effect in Blender, but will be exported and included in the SMP .xml file")
        row = layout.row()
        row.prop(data, "inertia")
        row = layout.row()
        row.prop(data, "gravity_factor")
        row = layout.row()
        row.prop(data, "rolling_friction")
        row = layout.row()
        row.prop(data, "margin_multiplier")

# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class SMP_objectCollection(PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    obj_type: StringProperty()
    obj_id: IntProperty()


class SMP_OT_tagCollection(PropertyGroup):
    tag: bpy.props.StringProperty(default="collision_mesh", name="tag")