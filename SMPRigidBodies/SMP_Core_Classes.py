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
from mathutils import Vector
from SMPRigidBodies.SMPMath import rotate_vector_blender_to_opengl

class SMPCollisionShape():
    collision_mesh_type = "vertex"
    collision_mesh_privacy = "private"
    no_collide_with_tags = ["hair", "head", "hands", "body", "collision_mesh"]
    collide_with_tags = []
    name = "UNNAMED"
    tag = "collision_mesh"
    margin = 0.1
    penetration = 0.1

    def __init__(self, obj):
        rb_obj = obj.rigid_body
        self.name = obj.name
        self.margin = rb_obj.collision_margin

        if obj.smp_props:
            self.no_collide_with_tags = [x.name for x in obj.smp_props]
        if obj.smp_col_type:
            self.collision_mesh_type = obj.smp_col_type
        if obj.smp_tag:
            self.tag = obj.smp_tag

    def generate_string(self):
        output_string = f"""    <per-{self.collision_mesh_type}-shape name="{self.name}">
        <margin>{self.margin}</margin>
        <shared>{self.collision_mesh_privacy}</shared>
        <penetration>{self.penetration}</penetration>
        <tag>{self.tag}</tag>\n"""
        if self.no_collide_with_tags:
            for no_collide_tag in self.no_collide_with_tags:
                output_string += f"""        <no-collide-with-tag>{no_collide_tag}</no-collide-with-tag>\n"""
        if self.collide_with_tags:
            for collide_tag in self.collide_with_tags:
                output_string += f"""        <collide-with-tag>{no_collide_tag}</collide-with-tag>\n"""
        output_string += f"""    </per-{self.collision_mesh_type}-shape>\n\n"""

        return output_string


class SMPStaticBones():
    """This a container for multiple static bones, very primitive.
       It's just a 'header' and a list of bones"""

    header = """    <bone-default>
        <mass>0</mass>
        <inertia x="0" y="0" z="0"/>
        <centerOfMassTransform>
            <basis x="0" y="0" z="0" w="1"/>
            <origin x="0" y="0" z="0"/>
        </centerOfMassTransform>
        <linearDamping>0.0</linearDamping>
        <angularDamping>0.0</angularDamping>
            <friction>0.0</friction>
        <rollingFriction>0.0</rollingFriction>
        <restitution>0.0</restitution>
        <gravity-factor>0.000</gravity-factor>
    </bone-default>\n\n"""

    bone_list = []

    def __init__(self):
        pass

    def push(self, bone):
        # Should probably raise on encountering '[Active]'
        self.bone_list.append(bone.name.replace(" [Passive]", "").replace(" [Active]", ""))

    def generate_string(self):
        if not self.bone_list:
            raise "No static bones"
        output_string = self.header
        for bone in self.bone_list:
            output_string += f"""    <bone name="{bone}"/>\n"""
        output_string += "\n"
        return output_string


class SMPKinematicBone():
    """
    Class for holding a kinematic bones and it's SMP definitions
    """
    rollingFriction = 0.0
    gravityFactor = 1.0
    inertia_x = inertia_y = inertia_z = 1.0
    bone_name = "Unset bone"
    mass = 1.0
    linearDamping = 0.2
    angularDamping = 0.1
    friction = 0.0
    rollingFriction = 0.0
    margin = 1.0

    def __init__(self, bone):
        rb_obj = bone.rigid_body
        assert rb_obj.type == "ACTIVE"
        self.bone_name = bone.name.replace(" [Active]", "")
        self.mass = rb_obj.mass

        self.linearDamping = rb_obj.linear_damping
        self.angularDamping = rb_obj.angular_damping

        self.friction = rb_obj.friction
        self.restitution = rb_obj.restitution

    def generate_string(self):
        output_string = f"""    <bone name="{self.bone_name}">
        <mass>{self.mass}</mass>
        <inertia x="{self.inertia_x}" y="{self.inertia_y}" z="{self.inertia_z}"/>
        <centerOfMassTransform>
            <basis x="0" y="0" z="0" w="1"/>
            <origin x="0" y="0" z="0"/>
        </centerOfMassTransform>
        <linearDamping>{self.linearDamping}</linearDamping>
        <angularDamping>{self.angularDamping}</angularDamping>
        <friction>{self.friction}</friction> 
        <rollingFriction>{self.rollingFriction}</rollingFriction>
        <restitution>{self.restitution}</restitution>
        <margin-multiplier>{self.margin}</margin-multiplier>
        <gravity-factor>{self.gravityFactor}</gravity-factor>
    </bone>\n\n"""
        return output_string


class SMPGenericConstraint():
    bodyA = "UNSET_bodyA"
    bodyB = "UNSET_bodyB"
    useLinearReferenceFrameA = False
    limit_lin_x_lower = 0.0
    limit_lin_x_upper = 0.0
    limit_lin_y_lower = 0.0
    limit_lin_y_upper = 0.0
    limit_lin_z_lower = 0.0
    limit_lin_z_upper = 0.0
    limit_ang_x_lower = 0.0
    limit_ang_x_upper = 0.0
    limit_ang_y_lower = 0.0
    limit_ang_y_upper = 0.0
    limit_ang_z_lower = 0.0
    limit_ang_z_upper = 0.0
    spring_stiffness_x = 0.0
    spring_damping_x = 0.0
    spring_stiffness_y = 0.0
    spring_stiffness_z = 0.0
    spring_damping_y = 0.0
    spring_damping_z = 0.0
    spring_stiffness_ang_x = 0.0
    spring_stiffness_ang_y = 0.0
    spring_stiffness_ang_z = 0.0
    spring_damping_ang_x = 0.0
    spring_damping_ang_y = 0.0
    spring_damping_ang_z = 0.0

    # This class takes a rigid body constraint and sets all variables, with defaults settings for disabled translation/rotation limits

    def __init__(self, b_rb_constraint):
        self.bodyA = b_rb_constraint.object1.name.replace(" [Passive]", "").replace(" [Active]", "")
        self.bodyB = b_rb_constraint.object2.name.replace(" [Passive]", "").replace(" [Active]", "")
        self.useLinearReferenceFrameA = False

        self.set_lin_limits(b_rb_constraint)
        self.set_ang_limits(b_rb_constraint)
        self.set_spring_lin_limits(b_rb_constraint)
        self.set_spring_ang_limits(b_rb_constraint)

    def set_lin_limits(self, b_rb_constraint):
        # Parse the linear limits into two vectors, for the lower and upper limits
        # If the limit is disabled, set it to 0.0
        vec_LO = Vector((0.0, 0.0, 0.0))
        vec_HI = Vector((0.0, 0.0, 0.0))
        if b_rb_constraint.use_limit_lin_x:
            vec_LO.x = b_rb_constraint.limit_lin_x_lower
            vec_HI.x = b_rb_constraint.limit_lin_x_upper
        else:
            vec_LO.x = 0.0
            vec_HI.x = 0.0

        if b_rb_constraint.use_limit_lin_y:
            vec_LO.y = b_rb_constraint.limit_lin_y_lower
            vec_HI.y = b_rb_constraint.limit_lin_y_upper
        else:
            vec_LO.y = 0.0
            vec_HI.y = 0.0

        if b_rb_constraint.use_limit_lin_z:
            vec_LO.z = b_rb_constraint.limit_lin_z_lower
            vec_HI.z = b_rb_constraint.limit_lin_z_upper
        else:
            vec_LO.z = 0.0
            vec_HI.z = 0.0

        # Transform the vectors into correct coordinates
        vec_LO = rotate_vector_blender_to_opengl(vec_LO)
        vec_HI = rotate_vector_blender_to_opengl(vec_HI)

        # Set the limits
        self.limit_lin_x_lower = str(vec_LO.x)
        self.limit_lin_x_upper = str(vec_HI.x)
        self.limit_lin_y_lower = str(vec_LO.y)
        self.limit_lin_y_upper = str(vec_HI.y)
        self.limit_lin_z_lower = str(vec_LO.z)
        self.limit_lin_z_upper = str(vec_HI.z)


    def set_ang_limits(self, b_rb_constraint):
        # Parse the angular limits into two vectors, for the lower and upper limits
        # If the limit is disabled, set it to 0.0
        vec_LO = Vector((0.0, 0.0, 0.0))
        vec_HI = Vector((0.0, 0.0, 0.0))
        if b_rb_constraint.use_limit_ang_x:
            vec_LO.x = b_rb_constraint.limit_ang_x_lower
            vec_HI.x = b_rb_constraint.limit_ang_x_upper
        else:
            vec_LO.x = 0.0
            vec_HI.x = 0.0
        if b_rb_constraint.use_limit_ang_y:
            vec_LO.y = b_rb_constraint.limit_ang_y_lower
            vec_HI.y = b_rb_constraint.limit_ang_y_upper
        else:
            vec_LO.y = 0.0
            vec_HI.y = 0.0
        if b_rb_constraint.use_limit_ang_z:
            vec_LO.z = b_rb_constraint.limit_ang_z_lower
            vec_HI.z = b_rb_constraint.limit_ang_z_upper
        else:
            vec_LO.z = 0.0
            vec_HI.z = 0.0

        # Transform the vectors into correct coordinates
        vec_LO = rotate_vector_blender_to_opengl(vec_LO)
        vec_HI = rotate_vector_blender_to_opengl(vec_HI)

        # Set the limits
        self.limit_ang_x_lower = str(vec_LO.x)
        self.limit_ang_x_upper = str(vec_HI.x)
        self.limit_ang_y_lower = str(vec_LO.y)
        self.limit_ang_y_upper = str(vec_HI.y)
        self.limit_ang_z_lower = str(vec_LO.z)
        self.limit_ang_z_upper = str(vec_HI.z)



    def set_spring_ang_limits(self, b_rb_constraint):

        # Parse the spring angular limits into two vectors, for the stiffness and damping
        # If the limit is disabled, set it to 0.0
        vec_stiffness = Vector((0.0, 0.0, 0.0))
        vec_damping = Vector((0.0, 0.0, 0.0))
        if b_rb_constraint.use_spring_ang_x:
            vec_stiffness.x = b_rb_constraint.spring_stiffness_ang_x
            vec_damping.x = b_rb_constraint.spring_damping_ang_x
        else:
            vec_stiffness.x = 0.0
            vec_damping.x = 0.0
        if b_rb_constraint.use_spring_ang_y:
            vec_stiffness.y = b_rb_constraint.spring_stiffness_ang_y
            vec_damping.y = b_rb_constraint.spring_damping_ang_y
        else:
            vec_stiffness.y = 0.0
            vec_damping.y = 0.0
        if b_rb_constraint.use_spring_ang_z:
            vec_stiffness.z = b_rb_constraint.spring_stiffness_ang_z
            vec_damping.z = b_rb_constraint.spring_damping_ang_z
        else:
            vec_stiffness.z = 0.0
            vec_damping.z = 0.0

        # Transform the vectors into correct coordinates
        vec_stiffness = rotate_vector_blender_to_opengl(vec_stiffness)
        vec_damping = rotate_vector_blender_to_opengl(vec_damping)

        # Make the values positive (absolute)
        vec_stiffness.x = abs(vec_stiffness.x)
        vec_stiffness.y = abs(vec_stiffness.y)
        vec_stiffness.z = abs(vec_stiffness.z)
        vec_damping.x = abs(vec_damping.x)
        vec_damping.y = abs(vec_damping.y)
        vec_damping.z = abs(vec_damping.z)

        # Set the limits
        self.spring_stiffness_ang_x = str(vec_stiffness.x)
        self.spring_stiffness_ang_y = str(vec_stiffness.y)
        self.spring_stiffness_ang_z = str(vec_stiffness.z)
        self.spring_damping_ang_x = str(vec_damping.x)
        self.spring_damping_ang_y = str(vec_damping.y)
        self.spring_damping_ang_z = str(vec_damping.z)



    def set_spring_lin_limits(self, b_rb_constraint):
        # Parse the spring linear limits into two vectors, for the stiffness and damping
        # If the limit is disabled, set it to 0.0
        # The stiffness and damping values should always be positive

        vec_stiffness = Vector((0.0, 0.0, 0.0))
        vec_damping = Vector((0.0, 0.0, 0.0))
        if b_rb_constraint.use_spring_x:
            vec_stiffness.x = b_rb_constraint.spring_stiffness_x
            vec_damping.x = b_rb_constraint.spring_damping_x
        else:
            vec_stiffness.x = 0.0
            vec_damping.x = 0.0
        if b_rb_constraint.use_spring_y:
            vec_stiffness.y = b_rb_constraint.spring_stiffness_y
            vec_damping.y = b_rb_constraint.spring_damping_y
        else:
            vec_stiffness.y = 0.0
            vec_damping.y = 0.0
        if b_rb_constraint.use_spring_z:
            vec_stiffness.z = b_rb_constraint.spring_stiffness_z
            vec_damping.z = b_rb_constraint.spring_damping_z
        else:
            vec_stiffness.z = 0.0
            vec_damping.z = 0.0

        # Transform the vectors into correct coordinates
        vec_stiffness = rotate_vector_blender_to_opengl(vec_stiffness)
        vec_damping = rotate_vector_blender_to_opengl(vec_damping)

        # Make the values positive (absolute)
        vec_stiffness.x = abs(vec_stiffness.x)
        vec_stiffness.y = abs(vec_stiffness.y)
        vec_stiffness.z = abs(vec_stiffness.z)
        vec_damping.x = abs(vec_damping.x)
        vec_damping.y = abs(vec_damping.y)
        vec_damping.z = abs(vec_damping.z)

        # Set the limits
        self.spring_stiffness_x = str(vec_stiffness.x)
        self.spring_stiffness_y = str(vec_stiffness.y)
        self.spring_stiffness_z = str(vec_stiffness.z)
        self.spring_damping_x = str(vec_damping.x)
        self.spring_damping_y = str(vec_damping.y)
        self.spring_damping_z = str(vec_damping.z)


    def update(self, b_rb_constraint):
        # Might be needed at some point I dunno
        self.set_lin_limits(b_rb_constraint)
        self.set_ang_limits(b_rb_constraint)
        self.set_spring_lin_limits(b_rb_constraint)
        self.set_spring_ang_limits(b_rb_constraint)

    def generate_string(self):
        constraintStr = """    <generic-constraint bodyA="{bodyA}" bodyB="{bodyB}">
        <useLinearReferenceFrameA>{useLinearReferenceFrameA}</useLinearReferenceFrameA>
        <linearLowerLimit x="{limit_lin_x_lower}" y="{limit_lin_y_lower}" z="{limit_lin_z_lower}" />
        <linearUpperLimit x="{limit_lin_x_upper}" y="{limit_lin_y_upper}" z="{limit_lin_z_upper}" />
        <angularLowerLimit x="{limit_ang_x_lower}" y="{limit_ang_y_lower}" z="{limit_ang_z_lower}" />
        <angularUpperLimit x="{limit_ang_x_upper}" y="{limit_ang_y_upper}" z="{limit_ang_z_upper}" />
        <linearStiffness x="{spring_stiffness_x}" y="{spring_stiffness_y}" z="{spring_stiffness_z}" />
        <angularStiffness x="{spring_stiffness_ang_x}" y="{spring_stiffness_ang_y}" z="{spring_stiffness_ang_z}" />
        <linearDamping x="{spring_damping_x}" y="{spring_damping_y}" z="{spring_damping_z}" />
        <angularDamping x="{spring_damping_ang_x}" y="{spring_damping_ang_y}" z="{spring_damping_ang_z}" />
        <linearEquilibrium x="0" y="0" z="0" />
        <angularEquilibrium x="0" y="0" z="0" />
        <linearBounce x="0" y="0" z="0" />
        <angularBounce x="0" y="0" z="0" />
    </generic-constraint>\n\n""".format(bodyA=self.bodyA,
                                        bodyB=self.bodyB,
                                        useLinearReferenceFrameA=str(self.useLinearReferenceFrameA).lower(),
                                        limit_lin_x_lower=str(self.limit_lin_x_upper),
                                        limit_lin_y_lower=str(self.limit_lin_y_upper),
                                        limit_lin_z_lower=str(self.limit_lin_z_upper),
                                        limit_lin_x_upper=str(self.limit_lin_x_upper),
                                        limit_lin_y_upper=str(self.limit_lin_y_upper),
                                        limit_lin_z_upper=str(self.limit_lin_z_upper),
                                        limit_ang_x_lower=str(self.limit_ang_x_lower),
                                        limit_ang_y_lower=str(self.limit_ang_y_lower),
                                        limit_ang_z_lower=str(self.limit_ang_z_lower),
                                        limit_ang_x_upper=str(self.limit_ang_x_upper),
                                        limit_ang_y_upper=str(self.limit_ang_y_upper),
                                        limit_ang_z_upper=str(self.limit_ang_z_upper),
                                        spring_stiffness_x=str(self.spring_stiffness_x),
                                        spring_stiffness_y=str(self.spring_stiffness_y),
                                        spring_stiffness_z=str(self.spring_stiffness_z),
                                        spring_damping_x=str(self.spring_damping_x),
                                        spring_damping_y=str(self.spring_damping_y),
                                        spring_damping_z=str(self.spring_damping_z),
                                        spring_stiffness_ang_x=str(self.spring_stiffness_ang_x),
                                        spring_stiffness_ang_y=str(self.spring_stiffness_ang_y),
                                        spring_stiffness_ang_z=str(self.spring_stiffness_ang_z),
                                        spring_damping_ang_x=str(self.spring_damping_ang_x),
                                        spring_damping_ang_y=str(self.spring_damping_ang_y),
                                        spring_damping_ang_z=str(self.spring_damping_ang_z))
        return constraintStr
