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


class SMP_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "smp_props.list_action"
    bl_label = "List Actions"
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
        idx = obj.smp_props_index

        try:
            item = obj.smp_props[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(obj.smp_props) - 1:
                item_next = obj.smp_props[idx + 1].name
                obj.smp_props.move(idx, idx + 1)
                obj.smp_props_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.smp_props_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = obj.smp_props[idx - 1].name
                obj.smp_props.move(idx, idx - 1)
                obj.smp_props_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.smp_props_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (obj.smp_props[idx].name)
                obj.smp_props_index -= 1
                obj.smp_props.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            item = obj.smp_props.add()
            item.name = "tag"
            item.obj_id = len(obj.smp_props)
            obj.smp_props_index = len(obj.smp_props) - 1

        return {"FINISHED"}


class SMP_OT_defaultTags(Operator):
    """Fill with default tags"""
    bl_idname = "smp_props.default_tags"
    bl_label = "Fill default tags"
    bl_description = "Fill with default collision tags"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        for tag in ["body", "hair", "hands", "head"]:
            item = context.active_object.smp_props.add()
            item.name = tag
            item.obj_id = len(context.active_object.smp_props)
            context.active_object.smp_props_index = len(context.active_object.smp_props) - 1
        return {'FINISHED'}


class SMP_OT_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "smp_props.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object.smp_props)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.active_object.smp_props):
            context.active_object.smp_props.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return {'FINISHED'}


class SMP_OT_removeDuplicates(Operator):
    """Remove all duplicates"""
    bl_idname = "smp_props.remove_duplicates"
    bl_label = "Remove Duplicates"
    bl_description = "Remove all duplicates"
    bl_options = {'INTERNAL'}

    def find_duplicates(self, context):
        """find all duplicates by name"""
        name_lookup = {}
        for c, i in enumerate(context.active_object.smp_props):
            name_lookup.setdefault(i.name, []).append(c)
        duplicates = set()
        for name, indices in name_lookup.items():
            for i in indices[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))

    @classmethod
    def poll(cls, context):
        return bool(context.active_object.smp_props)

    def execute(self, context):
        obj = context.active_object
        removed_items = []
        # Reverse the list before removing the items
        for i in self.find_duplicates(context)[::-1]:
            obj.smp_props.remove(i)
            removed_items.append(i)
        if removed_items:
            obj.smp_props_index = len(obj.smp_props) - 1
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SMP_UL_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, "name", text="", emboss=False)

    def invoke(self, context, event):
        pass


class SMP_PT_objectList(Panel):
    """Custom panel in the rigid body physics properties area"""

    bl_idname = "SMPRIGIDBODIES_PT_SMPRigidBodies"
    bl_label = "SMPRigidBodies"

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
        tag_row = layout.row()
        tag_row.prop(obj, "smp_tag", text="tag")

        desc_row = layout.row()
        desc_row.label(text="no-collide-with-tags")

        rows = 2
        row = layout.row()
        row.template_list("SMP_UL_items", "", obj, "smp_props", obj, "smp_props_index", rows=rows)

        col = row.column(align=True)
        col.operator("smp_props.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("smp_props.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("smp_props.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("smp_props.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("smp_props.default_tags", icon="ADD")
        row.operator("smp_props.clear_list", icon="X")
        row.operator("smp_props.remove_duplicates", icon="GHOST_ENABLED")


# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class SMP_objectCollection(PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    obj_type: StringProperty()
    obj_id: IntProperty()


class SMP_OT_tagCollection(PropertyGroup):
    tag: bpy.props.StringProperty(default="collision_mesh", name="tag")