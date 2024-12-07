
import os
import numpy as np
from OpenGL.GL import GL_LINES
import Elements.utils.normals as norm
from Elements.pyECSS.Entity import Entity
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyGLV.GUI.Viewer import imgui
from Elements.definitions import TEXTURE_DIR
import Elements.pyECSS.math_utilities as util
from Elements.pyGLV.GL.Textures import Texture
from Elements.utils.terrain import generateTerrain
from Elements.utils.obj_to_mesh import obj_to_mesh
from Elements.pyGLV.GUI.ImguiDecorator import imgui
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.pyGLV.GL.Textures import get_texture_faces
from Elements.pyGLV.GUI.Viewer import RenderGLStateSystem
from Elements.pyGLV.GL.Textures import get_single_texture_faces
from Elements.pyECSS.System import TransformSystem, CameraSystem
from Elements.pyGLV.GUI.ImguiDecorator import ImGUIecssDecorator2
from Elements.pyECSS.Component import BasicTransform, Camera, RenderMesh
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
import Elements.pyECSS.math_utilities as util
from Elements.utils.Shortcuts import displayGUI_text
example_description = """This is planet Earth."""

# Scene
winWidth = 1024
winHeight = 768
scene = Scene()

eye = util.vec(2.5, 2.5, 10)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 0.01, 100.0) 
m = np.linalg.inv(projMat @ view)  

#Light
Lposition = util.vec(2.5, 2.5, 2.5) 
Lambientcolor = util.vec(1.0, 1.0, 1.0) 
LviewPos = util.vec(2.5, 2.8, 5.0) 
Lcolor = util.vec(1.0,1.0,1.0)
Lambientstr = 0.3
Lintensity = 0.5
Mshininess = 0.1

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
transSphere = scene.world.addComponent(sphere, BasicTransform(name="sphere", trs=util.translate(0.0, 0.0, 0.0))) 
meshSphere = scene.world.addComponent(sphere, RenderMesh(name="meshSphere"))

# Moon
Moon = scene.world.createEntity(Entity(name="Moon"))
scene.world.addEntityChild(rootEntity, Moon)
transMoon = scene.world.addComponent(Moon, BasicTransform(name="Moon", trs=util.translate(2.5, 2.5, 2.5))) 
meshMoon = scene.world.addComponent(Moon, RenderMesh(name="meshMoon"))

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

# Sphere from here
VerticesSphere = []
IndicesSphere = []
normals = []
uvs = []

k = 30
radius = 1 
for i in range(0, k+1):
    for j in range(0, k+1):
        x = radius* np.cos(2 * np.pi * j / k) * np.sin(np.pi * i / k)
        y = radius* np.cos(np.pi * i / k)
        z = radius* np.sin(2 * np.pi * j / k) * np.sin(np.pi * i / k) 
        VerticesSphere.append([x, y, z, 1.0])
        IndicesSphere.append(i * k + j)
        IndicesSphere.append((i + 1) * k + j)
        IndicesSphere.append((i + 1) * k + (j + 1) % k)
        IndicesSphere.append(i * k + j)
        IndicesSphere.append(i * k + (j + 1) % k)
        IndicesSphere.append((i + 1) * k + (j + 1) % k) 
        normals.append([x, y, z, 1.0])  
        u = j / k            
        v = i / k              
        uvs.append([u, v])         
# Sphere till here

# Set up Earth
meshSphere.vertex_attributes.append(VerticesSphere)
meshSphere.vertex_attributes.append(uvs)
meshSphere.vertex_attributes.append(normals)
meshSphere.vertex_index.append(IndicesSphere)
vArraySphere = scene.world.addComponent(sphere, VertexArray())
shaderDecSphere = scene.world.addComponent(sphere, ShaderGLDecorator(Shader(vertex_source = Shader.SIMPLE_TEXTURE_PHONG_VERT, fragment_source=Shader.SIMPLE_TEXTURE_PHONG_FRAG)))

# Moon from here
VerticesSphere2 = []
IndicesSphere2 = []
Color = []
radius2 = 0.1  
for i in range(k):
    for j in range(k):
        x = radius2 * np.cos(2 * np.pi * j / k) * np.sin(np.pi * i / k)
        y = -(radius2 * np.cos(np.pi * i / k))
        z = radius2 * np.sin(2 * np.pi * j / k) * np.sin(np.pi * i / k)
        VerticesSphere2.append([x, y, z, 1.0])
        IndicesSphere2.append(i * k + j)
        IndicesSphere2.append((i + 1) * k + j)
        IndicesSphere2.append((i + 1) * k + (j + 1) % k)
        IndicesSphere2.append(i * k + j)
        IndicesSphere2.append((i + 1) * k + (j + 1) % k)
        IndicesSphere2.append(i * k + (j + 1) % k)
        Color.append([1.0, 1.0, 1.0, 1.0])
# Moon till here

# Set up Moon
meshMoon.vertex_attributes.append(VerticesSphere2)
meshMoon.vertex_index.append(IndicesSphere2)
meshMoon.vertex_attributes.append(Color)
vArrayMoon = scene.world.addComponent(Moon, VertexArray())
shaderDecMoon = scene.world.addComponent(Moon, ShaderGLDecorator(Shader(vertex_source=Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))

# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())

# Set up Skybox 
vertexSkybox, indexSkybox, _ = norm.generateUniqueVertices(vertexSkybox, indexSkybox)
meshSkybox.vertex_attributes.append(vertexSkybox)
meshSkybox.vertex_index.append(indexSkybox)
vArraySkybox = scene.world.addComponent(skybox, VertexArray())
shaderSkybox = scene.world.addComponent(skybox, ShaderGLDecorator(Shader(vertex_source=Shader.STATIC_SKYBOX_VERT, fragment_source=Shader.STATIC_SKYBOX_FRAG)))

# MAIN RENDERING LOOP
running = True
scene.init(imgui=True, windowWidth=winWidth, windowHeight=winHeight, windowTitle="Elements: Earth Example", customImGUIdecorator=ImGUIecssDecorator2, openGLversion=4)
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

# Camera
eye = util.vec(2.5, 2.5, 10)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 0.01, 100.0)  
gWindow._myCamera = view

# Load Stars textures 
skybox_texture_locations = TEXTURE_DIR / "Stars"
front_img = skybox_texture_locations / "front.png"
right_img = skybox_texture_locations / "right.png"
left_img = skybox_texture_locations / "left.png"
back_img = skybox_texture_locations / "back.png"
bottom_img = skybox_texture_locations / "bottom.png"
top_img = skybox_texture_locations / "top.png"
face_data = get_texture_faces(front_img, back_img, top_img, bottom_img, left_img, right_img)
shaderSkybox.setUniformVariable(key='cubemap', value=face_data, texture3D=True)

# Load Earth texture
texturePath = TEXTURE_DIR / "earth.jpg"
texture = Texture(texturePath) 
shaderDecSphere.setUniformVariable(key='ImageTexture', value=texture, texture=True)

# Main loop
while running:
    running = scene.render()
    displayGUI_text(example_description)
    
    scene.world.traverse_visit(transUpdate, scene.world.root)

    imgui.begin("Light")
    changed_lightPosition, new_lightPosition = imgui.drag_float3("Light Position", *Lposition, min_value=-20.0, max_value=20.0)
    if changed_lightPosition:
        Lposition = new_lightPosition

    imgui.end()

    view = gWindow._myCamera
    model_sphere = transSphere.l2world
    model_Moon = transMoon.l2world

    shaderDecSphere.setUniformVariable(key='model', value=model_sphere, mat4=True)
    shaderDecSphere.setUniformVariable(key='View', value=view, mat4=True)
    shaderDecSphere.setUniformVariable(key='Proj', value=projMat, mat4=True)
    shaderDecSphere.setUniformVariable(key='lightPos', value=Lposition, float3=True) 
    shaderDecSphere.setUniformVariable(key='viewPos', value=LviewPos, float3=True) 
    shaderDecSphere.setUniformVariable(key='lightColor', value=Lcolor, float3=True)  
    shaderDecSphere.setUniformVariable(key='ambientColor', value=Lambientcolor, float3=True)  
    shaderDecSphere.setUniformVariable(key='ambientStr', value=Lambientstr, float1=True)  
    shaderDecSphere.setUniformVariable(key='viewPos', value=eye, float3=True)  
    shaderDecSphere.setUniformVariable(key='lightIntensity', value=Lintensity, float1=True)  
    shaderDecSphere.setUniformVariable(key='shininess', value=Mshininess, float1=True)  

    mvp_Moon = projMat @ view @ model_Moon
    shaderDecMoon.setUniformVariable(key="modelViewProj", value=mvp_Moon, mat4=True)

    shaderSkybox.setUniformVariable(key='Proj', value=projMat, mat4=True)
    shaderSkybox.setUniformVariable(key='View', value=view, mat4=True)

    scene.world.traverse_visit(renderUpdate, scene.world.root)

    scene.render_post()

scene.shutdown()
