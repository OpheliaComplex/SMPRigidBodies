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
        row.operator("no_collide_with_tags.clear_list", icon="X")
        row.operator("no_collide_with_tags.remove_duplicates", icon="GHOST_ENABLED")

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
        row.operator("collide_with_tags.clear_list", icon="X")
        row.operator("collide_with_tags.remove_duplicates", icon="GHOST_ENABLED")

# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class SMP_objectCollection(PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    obj_type: StringProperty()
    obj_id: IntProperty()


class SMP_OT_tagCollection(PropertyGroup):
    tag: bpy.props.StringProperty(default="collision_mesh", name="tag")