# SMPRigidBodies
Export SMP xmls from blender defined using Rigid Body Bones (github.com/Pauan/blender-rigid-body-bones)

Set up and test your physics using Rigid Body Bones, define collision meshes in your scene by making them rigid bodies and passive. 
There's additional settings for these in the physics sidepanel like 'per-vertex-shape' or 'per-triangle-shape' which doesn't make sense on the blender side.

Some useful notes:
- Margins are currently exported as 1:1 which is clearly not correct.
- In blender "bounciness" is what's called "restitution" in SMP and bullet
- Inertia is not exposed and set to 1.0, which is generally sane and what you should do, however many SMP .xml builders use different settings for this. I might add this.

