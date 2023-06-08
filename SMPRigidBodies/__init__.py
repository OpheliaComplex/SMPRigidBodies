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
from bpy.props import (StringProperty, CollectionProperty, IntProperty, EnumProperty)

from SMPRigidBodies.SMP_UI import SMP_OT_actions_ncwt, SMP_OT_actions_cwt, SMP_OT_defaultTags_ncwt, \
    SMP_OT_defaultTags_cwt,SMP_OT_tagCollection, SMP_UL_items, SMP_PT_CollisionPropertiesPanel,  SMP_objectCollection
from SMPRigidBodies.SMPExport import SMPExport

bl_info = {
    "name": "SMPRigidBodies",
    "description": "Export Rigid Body Bones and collision rigid bodies to SMP .xmls",
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "category": "Import-Export",
}

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    SMP_OT_actions_ncwt,
    SMP_OT_defaultTags_ncwt,
    SMP_OT_actions_cwt,
    SMP_OT_defaultTags_cwt,
    SMP_OT_tagCollection,
    SMP_UL_items,
    SMP_PT_CollisionPropertiesPanel,
    SMP_objectCollection,
    SMPExport,
)


def SMP_menu_export(self, context):
    self.layout.operator(SMPExport.bl_idname, text="Skinned mesh physics (SMP) .xml")

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # SMP properties
    bpy.types.Object.no_collide_with_tags = CollectionProperty(type=SMP_objectCollection)
    bpy.types.Object.no_collide_with_tags_index = IntProperty()
    bpy.types.Object.collide_with_tags = CollectionProperty(type=SMP_objectCollection)
    bpy.types.Object.collide_with_tags_index = IntProperty()
    bpy.types.Object.smp_tag = StringProperty(default="collision_mesh")
    bpy.types.Object.smp_col_type = EnumProperty(items=(
        ('vertex', "per-vertex-shape", ""),
        ('triangle', "per-triangle-shape", "")))
    bpy.types.Object.smp_col_privacy = EnumProperty(items=(
        ('public', "public", ""),
        ('private', "private", ""),
        ('internal', "internal", ""),
        ('external', "external", "")))
    # Insert into export menu
    bpy.types.TOPBAR_MT_file_export.append(SMP_menu_export)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Object.no_collide_with_tags
    del bpy.types.Object.no_collide_with_tags_index
    del bpy.types.Object.collide_with_tags
    del bpy.types.Object.collide_with_tags_index
    del bpy.types.Object.smp_tag
    del bpy.types.Object.smp_col_type
    del bpy.types.Object.smp_col_privacy
    # Remove from export menu
    bpy.types.TOPBAR_MT_file_export.remove(SMP_menu_export)


if __name__ == "__main__":
    register()