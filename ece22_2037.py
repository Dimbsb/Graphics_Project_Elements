
import os
import numpy as np
import Elements.utils.normals as norm
from Elements.pyECSS.Entity import Entity
from Elements.pyGLV.GL.Scene import Scene
from Elements.definitions import TEXTURE_DIR
import Elements.pyECSS.math_utilities as util
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.pyGLV.GL.Textures import get_texture_faces
from Elements.pyGLV.GUI.Viewer import RenderGLStateSystem
from Elements.pyGLV.GL.Textures import get_single_texture_faces
from Elements.pyECSS.System import TransformSystem, CameraSystem
from Elements.pyGLV.GUI.ImguiDecorator import ImGUIecssDecorator2
from Elements.pyECSS.Component import BasicTransform, Camera, RenderMesh
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.utils.Shortcuts import displayGUI_text
example_description = """This is earth."""

#Light
Lposition = util.vec(-1, 1.5, 1.2) #uniform lightpos
Lambientcolor = util.vec(1.0, 1.0, 1.0) #uniform ambient color
Lcolor = util.vec(1.0,1.0,1.0)
Lintensity = 40.0

# Scene
winWidth = 1024
winHeight = 768
scene = Scene()

#Root
rootEntity = scene.world.createEntity(Entity(name="RooT"))

#Skybox
skybox = scene.world.createEntity(Entity(name="Skybox"))
scene.world.addEntityChild(rootEntity, skybox)
transSkybox = scene.world.addComponent(skybox, BasicTransform(name="transSkybox", trs=util.identity())) 
meshSkybox = scene.world.addComponent(skybox, RenderMesh(name="meshSkybox"))

#Sphere
sphere = scene.world.createEntity(Entity(name="sphere"))
scene.world.addEntityChild(rootEntity, sphere)
transSphere = scene.world.addComponent(sphere, BasicTransform(name="transSphere", trs=util.identity())) 
meshSphere = scene.world.addComponent(sphere, RenderMesh(name="meshSphere"))

# Skybox from here
minbox = -30
maxbox = 30
vertexSkybox = np.array([
    [minbox, minbox, maxbox, 1.0],
    [minbox, maxbox, maxbox, 1.0],
    [maxbox, maxbox, maxbox, 1.0],
    [maxbox, minbox, maxbox, 1.0], 
    [minbox, minbox, minbox, 1.0], 
    [minbox, maxbox, minbox, 1.0], 
    [maxbox, maxbox, minbox, 1.0], 
    [maxbox, minbox, minbox, 1.0]
], dtype=np.float32)

indexSkybox = np.array((1, 0, 3, 1, 3, 2, 
                  2, 3, 7, 2, 7, 6,
                  3, 0, 4, 3, 4, 7,
                  6, 5, 1, 6, 1, 2,
                  4, 5, 6, 4, 6, 7,
                  5, 4, 0, 5, 0, 1), np.uint32)
# Skybox till here

# Cube vertex and UV generation
VerticesSphere = []
IndicesSphere = []
NormalsSpheres = []
uvs = []

k = 30
radius = 1  # Adjust radius if needed
for i in range(k):
    for j in range(k):
        x = radius * np.cos(2 * np.pi * j / k) * np.sin(np.pi * i / k)
        y = radius * np.cos(np.pi * i / k)
        z = radius * np.sin(2 * np.pi * j / k) * np.sin(np.pi * i / k)
        VerticesSphere.append([x, y, z, 1.0])
        IndicesSphere.append(i * k + j)
        IndicesSphere.append((i + 1) * k + j)
        IndicesSphere.append((i + 1) * k + (j + 1) % k)
        IndicesSphere.append(i * k + j)
        IndicesSphere.append((i + 1) * k + (j + 1) % k)
        IndicesSphere.append(i * k + (j + 1) % k)
        NormalsSpheres.append([x, y, z, 1.0])
        u = j / k
        v = i / k
        uvs.append([u, v])


# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())

vertexSkybox, indexSkybox, _ = norm.generateUniqueVertices(vertexSkybox, indexSkybox)


# Set up Skybox with UVs and Mesh
meshSkybox.vertex_attributes.append(vertexSkybox)
meshSkybox.vertex_index.append(indexSkybox)
vArraySkybox = scene.world.addComponent(skybox, VertexArray())
shaderSkybox = scene.world.addComponent(skybox, ShaderGLDecorator(Shader(vertex_source=Shader.STATIC_SKYBOX_VERT, fragment_source=Shader.STATIC_SKYBOX_FRAG)))

# Set up Cube with UVs and Mesh
meshSphere.vertex_attributes.append(VerticesSphere)
meshSphere.vertex_attributes.append(uvs)
meshSphere.vertex_index.append(IndicesSphere)
vArray4 = scene.world.addComponent(sphere, VertexArray())
shaderDec4 = scene.world.addComponent(sphere, ShaderGLDecorator(Shader(vertex_source=Shader.TEXTURE_3D_VERT, fragment_source=Shader.TEXTURE_3D_FRAG)))

# MAIN RENDERING LOOP
running = True
scene.init(imgui=True, windowWidth=winWidth, windowHeight=winHeight, windowTitle="Elements: Cube Mapping Example", customImGUIdecorator=ImGUIecssDecorator2, openGLversion=4)

# Pre-pass scenegraph to initialize all GL context dependent geometry, shader classes
scene.world.traverse_visit(initUpdate, scene.world.root)

################### EVENT MANAGER ###################

eManager = scene.world.eventManager
gWindow = scene.renderWindow
gGUI = scene.gContext

renderGLEventActuator = RenderGLStateSystem()

eManager._subscribers['OnUpdateWireframe'] = gWindow
eManager._actuators['OnUpdateWireframe'] = renderGLEventActuator
eManager._subscribers['OnUpdateCamera'] = gWindow 
eManager._actuators['OnUpdateCamera'] = renderGLEventActuator

eye = util.vec(2.5, 2.5, 8)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 0.01, 100.0)   
gWindow._myCamera = view

# Load the skybox textures (cube map faces)
skybox_texture_locations = TEXTURE_DIR / "Stars"
front_img = skybox_texture_locations / "front.png"
right_img = skybox_texture_locations / "right.png"
left_img = skybox_texture_locations / "left.png"
back_img = skybox_texture_locations / "back.png"
bottom_img = skybox_texture_locations / "bottom.png"
top_img = skybox_texture_locations / "top.png"

# Load cube map textures for the skybox
face_data = get_texture_faces(front_img, back_img, top_img, bottom_img, left_img, right_img)

# Apply cube map texture to the skybox shader
shaderSkybox.setUniformVariable(key='cubemap', value=face_data, texture3D=True)


# Load Earth texture for the sphere (single texture)
mat_img = TEXTURE_DIR / "earth.jpg"
face_data_2 = get_single_texture_faces(mat_img)

# Apply Earth texture to the sphere shader
shaderDec4.setUniformVariable(key='cubemap', value=face_data_2, texture3D=False)


# MAIN RENDERING LOOP
while running:
    running = scene.render()
    displayGUI_text(example_description)
    scene.world.traverse_visit(transUpdate, scene.world.root)

    view = gWindow._myCamera

    # Apply the projection and view matrices for the sphere (Earth texture)
    shaderDec4.setUniformVariable(key='Proj', value=projMat, mat4=True)
    shaderDec4.setUniformVariable(key='View', value=view, mat4=True)
    shaderDec4.setUniformVariable(key='model', value=transSphere.l2world, mat4=True)  # Model matrix for Earth

    # Apply the projection and view matrices for the skybox (Cube map)
    shaderSkybox.setUniformVariable(key='Proj', value=projMat, mat4=True)
    shaderSkybox.setUniformVariable(key='View', value=view, mat4=True)

    # Traverse the scene graph and render the sphere with the Earth texture
    scene.world.traverse_visit(renderUpdate, scene.world.root)

    # After rendering the sphere, render the skybox (with the cube map)
    scene.render_post()
