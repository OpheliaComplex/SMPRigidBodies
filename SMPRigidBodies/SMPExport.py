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
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from SMPRigidBodies.SMPUtils import generate_xml

class SMPExport(bpy.types.Operator, ExportHelper):
    """Exporting rigid body bones setups to bullet SMP .xmls"""
    bl_idname = "object.armature_to_hkx"
    bl_label = "Export SMP .xml"

    # ExportHelper mixin class uses this
    filename_ext = ".xml"

    filter_glob: StringProperty(
        default="*.xml",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):

        scene = context.scene

        if self.filepath == "" or self.filepath[-4:]!=".xml":
            reportStr="Output filepath must end with .xml Cancelling export.."
            self.report({"ERROR"},reportStr)
            return {"CANCELLED"}

        # Collect the xml
        xml = generate_xml(scene)
        # Write the xml to file
        with open(self.filepath, "w") as f:
            f.write(xml)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

    def invoke(self, context, event):
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}