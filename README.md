# SMPRigidBodies
Export SMP xmls from blender defined using Rigid Body Bones (github.com/Pauan/blender-rigid-body-bones)

Set up and test your physics using Rigid Body Bones, define collision meshes in your scene by making them rigid bodies and passive. 
There's additional settings for these in the physics sidepanel like 'per-vertex-shape' or 'per-triangle-shape' which doesn't make sense on the blender side.

Some useful notes:
- Margins are currently exported as 1:1 which is clearly not correct.
- In blender "bounciness" is what's called "restitution" in SMP and bullet
- Inertia is not exposed and set to 1.0, which is generally sane and what you should do, however many SMP .xml builders use different settings for this. I might add this.

Pauans Rigid Body Bones can be used to create physics setups similarly to those created with SMP in skyrim:

[physics test.webm](https://github.com/OpheliaComplex/SMPRigidBodies/assets/92117876/a9210f4c-0fb1-4218-9020-5b071f2956ad)

Create the physics setup with that addon. 
Additionally you can define SMP collisison meshes by making them passive rigid bodies and tweaking their settings in the rigid body physics side panel under SMPRigidBodies

![1](https://github.com/OpheliaComplex/SMPRigidBodies/assets/92117876/e47459c3-b69a-4b46-8b03-b8a23efcb987)

When you are satisfied, export it all under file->export->Skinned Mesh Physics (SMP) .xml

![export](https://github.com/OpheliaComplex/SMPRigidBodies/assets/92117876/83487e7b-8312-4cca-927a-9990c0fee3fc)
