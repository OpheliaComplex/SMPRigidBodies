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
from SMPRigidBodies.SMP_Core_Classes import SMPCollisionShape, SMPKinematicBone, SMPStaticBones, SMPGenericConstraint

def traverse_tree(t):
    # Func to traverse trees of blender collections
    yield t
    for child in t.children:
        yield from traverse_tree(child)

def parse_scene(scene):
    # Collect hard coded top scene-level collection (the "Scene Collection")
    top_collection = scene.collection

    statics = SMPStaticBones()
    kinematics = []
    hkx_constraints_list = []
    collision_meshes = []

    for collection in top_collection.children:
        # Find the RigidBodyBones collection
        if collection.name == "RigidBodyBones":
            for armature_collections in collection.children:
                arma_name = armature_collections.name.replace(" [Container]" ,"")
                for armature_collection_child in armature_collections.children:
                    if " [Passives]" in armature_collection_child.name:
                        for obj in armature_collection_child.objects:
                            bone_name = obj.name.replace(" [Passive]" ,"")
                            statics.push(obj)

                    if " [Actives]" in armature_collection_child.name:
                        for obj in armature_collection_child.objects:
                            bone_name = obj.name.replace(" [Active]" ,"")
                            kinematics.append(SMPKinematicBone(obj))

                    if " [Joints]" in armature_collection_child.name:
                        for obj in armature_collection_child.objects:
                            if obj.rigid_body_constraint is not None:
                                constr = obj.rigid_body_constraint
                                constraint_name = obj.name.replace(" [Head]" ,"")
                                constr_trgt1 = constr.object1.name.replace(" [Passive]" ,"").replace(" [Active]" ,"")
                                constr_trgt2 = constr.object2.name.replace(" [Passive]" ,"").replace(" [Active]" ,"")

                                hkx_constr = SMPGenericConstraint(constr)
                                hkx_constraints_list.append(hkx_constr)

        else:
            # All other collections
            # Find rigid bodies that are not part of rigidbodybones collection but is in some other high level collection

            # Traverse these and find all objs
            for c in traverse_tree(collection):
                for obj in c.objects:
                    if obj.rigid_body is not None:
                        if obj.rigid_body.type == "PASSIVE":
                            collision_meshes.append(SMPCollisionShape(obj))
                        else:
                            # Warn the user that it found a rigid body that could be intended to be a collision mesh
                            # But is defined as 'ACTIVE' and thus will be ignored
                            print(f"WARNING: Found a passive rigid body {obj.name}, set to 'ACTIVE' to export as a "
                                  f"collision mesh.")

    for obj in top_collection.objects:
        # All objects in the top-level scene collection
        if obj.rigid_body is not None:
            if obj.rigid_body.type == "PASSIVE":
                collision_meshes.append(SMPCollisionShape(obj))
            else:
                # Warn the user that it found a rigid body that could be intended to be a collision mesh
                # But is defined as 'ACTIVE' and thus will be ignored
                print(f"WARNING: Found a passive rigid body {obj.name}, set to 'ACTIVE' to export as a "
                      f"collision mesh.")
    return statics, kinematics, hkx_constraints_list, collision_meshes


def generate_xml(scene):

    statics, kinematics, hkx_constraints, collision_meshes = parse_scene(scene)
    header = """<?xml version="1.0" encoding="UTF-8"?>
<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="description.xsd">\n\n"""
    footer = """\n\n</system>
</xml>"""
    # Add header, statics, kinematics, collision meshes, constraints, footer
    full_xml_string = header
    full_xml_string += statics.generate_string()
    if kinematics:
        for kinematic_bone in kinematics:
            full_xml_string += kinematic_bone.generate_string()
    if collision_meshes:
        for collision_mesh in collision_meshes:
            full_xml_string += collision_mesh.generate_string()
    if hkx_constraints:
        for hkx_constraint in hkx_constraints:
            full_xml_string += hkx_constraint.generate_string()

    full_xml_string += footer

    return full_xml_string