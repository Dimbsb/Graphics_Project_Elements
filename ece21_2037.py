
import os
import numpy as np
import OpenGL.GL as gl
from OpenGL.GL import GL_LINES
import Elements.utils.normals as norm
from Elements.pyECSS.Entity import Entity
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyGLV.GUI.Viewer import imgui
import Elements.pyECSS.math_utilities as util
from Elements.utils.terrain import generateTerrain
from Elements.utils.obj_to_mesh import obj_to_mesh
from Elements.pyGLV.GUI.ImguiDecorator import imgui 
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.pyGLV.GUI.Viewer import RenderGLStateSystem
from Elements.pyECSS.System import TransformSystem, CameraSystem
from Elements.pyGLV.GUI.ImguiDecorator import ImGUIecssDecorator2
from Elements.pyECSS.Component import BasicTransform, Camera, RenderMesh
from Elements.pyGLV.GL.Textures import Texture
from Elements.definitions import TEXTURE_DIR
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.utils.Shortcuts import displayGUI_text
example_description = \
"Cubes, Pyramid and House."  

#Light
Lposition = util.vec(2.0, 2.0, 2.0) 
Lambientcolor = util.vec(1.0, 1.0, 1.0) 
LviewPos = util.vec(2.5, 2.8, 5.0) 
Lcolor = util.vec(1.0,1.0,1.0)
Lambientstr = 0.2
Lintensity = 1.0
#Material
MshininessFirstcube = 0.0
MshininessSecondcube = 0.0
MshininessPyramid = 0.0
Mcolor = util.vec(1, 1, 1)

#Scene
winWidth = 1200
winHeight = 800
scene = Scene()   

# Scenegraph with Entities, Components
rootEntity = scene.world.createEntity(Entity(name="RooT"))

#first cube from here
FirstCube = scene.world.createEntity(Entity(name="FirstCube"))
scene.world.addEntityChild(rootEntity, FirstCube)
transFirstCube = scene.world.addComponent(FirstCube, BasicTransform(name="FirstCube_TRS",trs=util.translate(0.0, 0.3, 3.0)))
meshFirstCube = scene.world.addComponent(FirstCube, RenderMesh(name="FirstCube_mesh"))
#first cube from here

#second cube from here
SecondCube = scene.world.createEntity(Entity(name="SecondCube"))
scene.world.addEntityChild(rootEntity, SecondCube)
transSecondCube = scene.world.addComponent(SecondCube, BasicTransform(name="SecondCube_TRS",trs=util.translate(3.0, 0.3, 0.0)))  
meshSecondCube = scene.world.addComponent(SecondCube, RenderMesh(name="SecondCube_mesh"))
#second cube till here

#Pyramid from here
Pyramid = scene.world.createEntity(Entity(name="Pyramid"))
scene.world.addEntityChild(rootEntity, Pyramid)  
transPyramid = scene.world.addComponent(Pyramid, BasicTransform(name="Pyramid_TRS",trs=util.translate(1.0, 0.3, 1.5)))  
meshPyramid = scene.world.addComponent(Pyramid, RenderMesh(name="Pyramid_mesh"))
#Pyramid till here

#Simple Cube from here
vertexCube = np.array([
    [-0.6, -0.3, 0.5, 1.0],  
    [-0.6,  0.3, 0.5, 1.0],  
    [ 0.6,  0.3, 0.5, 1.0],  
    [ 0.6, -0.3, 0.5, 1.0],  
    [-0.6, -0.3, -0.5, 1.0], 
    [-0.6,  0.3, -0.5, 1.0], 
    [ 0.6,  0.3, -0.5, 1.0], 
    [ 0.6, -0.3, -0.5, 1.0], 
], dtype=np.float32)

colorCube = np.array([
    [0.2, 0.8, 0.1, 1.0],  
    [0.2, 0.8, 0.1, 1.0],
    [0.2, 0.8, 0.1, 1.0],
    [0.2, 0.8, 0.1, 1.0],
    [0.2, 0.8, 0.1, 1.0],
    [0.2, 0.8, 0.1, 1.0],
    [0.2, 0.8, 0.1, 1.0],
    [0.2, 0.8, 0.1, 1.0],
], dtype=np.float32)

colorCube2 = np.array([
    [0.8, 0.0, 0.8, 1.0],  
    [0.8, 0.0, 0.8, 1.0],
    [0.8, 0.0, 0.8, 1.0],
    [0.8, 0.0, 0.8, 1.0],
    [0.8, 0.0, 0.8, 1.0],
    [0.8, 0.0, 0.8, 1.0],
    [0.8, 0.0, 0.8, 1.0],
    [0.8, 0.0, 0.8, 1.0],
], dtype=np.float32)

indexCube = np.array([
    1, 0, 3,  1, 3, 2, 
    2, 3, 7,  2, 7, 6,
    3, 0, 4,  3, 4, 7,
    6, 5, 1,  6, 1, 2,
    4, 5, 6,  4, 6, 7,
    5, 4, 0,  5, 0, 1
], dtype=np.uint32)
#Simple Cube till here

# A simple Pyramid from here 
vertexPyramid = np.array([
    [0.0, 0.6, 0.0, 1.0],  
    [-0.6, 0.0, -0.5, 1.0], 
    [0.6, 0.0, -0.5, 1.0],  
    [0.6, 0.0, 0.5, 1.0],   
    [-0.6, 0.0, 0.5, 1.0], 
], dtype=np.float32)

indexPyramid = np.array([
    0, 4, 1,
    0, 3, 4,  
    0, 2, 3,  
    0, 1, 2,   
], dtype=np.uint32)

colorPyramid = np.array([
    [0.0, 0.2, 0.8, 1.0],  
    [0.0, 0.2, 0.8, 1.0],  
    [0.0, 0.2, 0.8, 1.0],  
    [0.0, 0.2, 0.8, 1.0],  
    [0.0, 0.2, 0.8, 1.0],  
], dtype=np.float32)

# A simple Pyramid till here 

# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())

#Vertices from here
verticesFirstcube, indicesFirstcube, colorsFirstcube, normalsFirstcube = norm.generateSmoothNormalsMesh(vertexCube , indexCube, colorCube)
verticesSecondcube, indicesSecondcube, colorsSecondcube, normalsSecondcube = norm.generateSmoothNormalsMesh(vertexCube , indexCube, colorCube2)
verticesPyramid, indicesPyramid, colorsPyramid, normalsPyramid = norm.generateSmoothNormalsMesh(vertexPyramid , indexPyramid, colorPyramid)
#Vertices till here

#first cube from here
meshFirstCube.vertex_attributes.append(verticesFirstcube)
meshFirstCube.vertex_attributes.append(colorsFirstcube)
meshFirstCube.vertex_attributes.append(normalsFirstcube)
meshFirstCube.vertex_index.append(indicesFirstcube)
vArrayFirstCube = scene.world.addComponent(FirstCube, VertexArray())
shaderDecFirstCube = scene.world.addComponent(FirstCube, ShaderGLDecorator(Shader(vertex_source = Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG_MATERIAL)))
#first cube till here

#second cube from here
meshSecondCube.vertex_attributes.append(verticesSecondcube)
meshSecondCube.vertex_attributes.append(colorsSecondcube)
meshSecondCube.vertex_attributes.append(normalsSecondcube)
meshSecondCube.vertex_index.append(indicesSecondcube)
vArraySecondCube = scene.world.addComponent(SecondCube, VertexArray())
shaderDecSecondCube = scene.world.addComponent(SecondCube, ShaderGLDecorator(Shader(vertex_source = Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG_MATERIAL)))
#second cube till here

#pyramid from here
meshPyramid.vertex_attributes.append(verticesPyramid)
meshPyramid.vertex_attributes.append(colorsPyramid)
meshPyramid.vertex_attributes.append(-normalsPyramid)
meshPyramid.vertex_index.append(indicesPyramid)
vArrayPyramid = scene.world.addComponent(Pyramid, VertexArray())
shaderDecPyramid = scene.world.addComponent(Pyramid, ShaderGLDecorator(Shader(vertex_source = Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG_MATERIAL)))
#pyramid till here

# MAIN RENDERING LOOP
running = True
scene.init(imgui=True, windowWidth = winWidth, windowHeight = winHeight, windowTitle = "Elements: Let There Be Light", openGLversion = 4, customImGUIdecorator = ImGUIecssDecorator2)
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
eye = util.vec(5, 5, 8)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)  
projMat = util.perspective(50.0, winWidth/winHeight, 0.01, 100.0)   
gWindow._myCamera = view 
model_cube = util.scale(1.0) @ util.translate(0.0,0.5,0.0)


#Main loop
while running:
    running = scene.render()
    displayGUI_text(example_description)

    #Imgui from here
    imgui.begin("COLOR-LIGHT-IMGUI")

    # Color controls from here
    changed_colorCube1, new_colorCube1 = imgui.drag_float3("Cube 1 Color", *colorCube[0][:3], min_value=0.0, max_value=255.0)
    if changed_colorCube1:
        colorCube[0][:3] = new_colorCube1 
        shaderDecFirstCube.setUniformVariable(key='matColor', value=colorCube[0][:3] / 255.0, float3=True)

    changed_colorCube2, new_colorCube2 = imgui.drag_float3("Cube 2 Color", *colorCube2[0][:3], min_value=0.0, max_value=255.0)
    if changed_colorCube2:
        colorCube2[0][:3] = new_colorCube2  
        shaderDecSecondCube.setUniformVariable(key='matColor', value=colorCube2[0][:3] / 255.0, float3=True)

    changed_colorPyramid, new_colorPyramid = imgui.drag_float3("Pyramid Color", *colorPyramid[0][:3], min_value=0.0, max_value=255.0)
    if changed_colorPyramid:
        colorPyramid[0][:3] = new_colorPyramid 
        shaderDecPyramid.setUniformVariable(key='matColor', value=colorPyramid[0][:3] / 255.0, float3=True)
    # Color controls till here

    # Light Position Control from here
    changed_lightPosition, new_lightPosition = imgui.drag_float3("Light Position", *Lposition, min_value=-20.0, max_value=20.0)
    if changed_lightPosition:
        Lposition = new_lightPosition
    # Light Position Control till here

    # Light Color Control from here
    changed_lightColor, new_lightColor = imgui.drag_float3("Light Color", *Lcolor, min_value=0.0, max_value=10.0)
    if changed_lightColor:
        Lcolor = new_lightColor
    # Light Color Control till here

    # Ambient Light Color Control from here
    changed_ambientColor, new_ambientColor = imgui.drag_float3("Ambient Light Color", *Lambientcolor, min_value=0.0, max_value=10.0)
    if changed_ambientColor:
        Lambientcolor = new_ambientColor
    # Ambient Light Color Control till here

    # Light Intensity Control from here
    changed_lightIntensity, new_lightIntensity = imgui.drag_float("Light Intensity", Lintensity, min_value=0.0, max_value=10.0)
    if changed_lightIntensity:
        Lintensity = new_lightIntensity
    # Light Intensity Control till here

    # Ambient Intensity Control from here
    changed_ambientIntensity, new_ambientIntensity = imgui.drag_float("Ambient Intensity", Lambientstr, min_value=0.0, max_value=10.0)
    if changed_ambientIntensity:
        Lambientstr = new_ambientIntensity
    # Ambient Intensity Control till here

    # Shininess control from here
    changed_shininess1, new_shininess1 = imgui.drag_float("Cube 1 Shininess", MshininessFirstcube, min_value=0.0, max_value=100.0)
    if changed_shininess1:
        MshininessFirstcube = new_shininess1
        shaderDecFirstCube.setUniformVariable(key='shininess', value=MshininessFirstcube, float1=True)

    changed_shininess2, new_shininess2 = imgui.drag_float("Cube 2 Shininess", MshininessSecondcube, min_value=0.0, max_value=100.0)
    if changed_shininess2:
        MshininessSecondcube = new_shininess2
        shaderDecSecondCube.setUniformVariable(key='shininess', value=MshininessSecondcube, float1=True)

    changed_shininessPyramid, new_shininessPyramid = imgui.drag_float("Pyramid Shininess", MshininessPyramid, min_value=0.0, max_value=100.0)
    if changed_shininessPyramid:
        MshininessPyramid = new_shininessPyramid
        shaderDecPyramid.setUniformVariable(key='shininess', value=MshininessPyramid, float1=True)
    # Shininess control till here

    imgui.end()
    #Imgui till here

    mvp_cube = projMat @ view @ transFirstCube.l2world
    mvp_cube2 = projMat @ view @ transSecondCube.l2world
    mvp_pyramid = projMat @ view @ transPyramid.l2world
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.world.traverse_visit(transUpdate, scene.world.root)
    view = gWindow._myCamera

    shaderDecFirstCube.setUniformVariable(key='model', value=model_cube, mat4=True)
    shaderDecFirstCube.setUniformVariable(key='modelViewProj', value=mvp_cube, mat4=True)
    shaderDecFirstCube.setUniformVariable(key='model', value=transFirstCube.l2world, mat4=True)
    shaderDecFirstCube.setUniformVariable(key='ambientColor', value=Lambientcolor, float3=True)
    shaderDecFirstCube.setUniformVariable(key='ambientStr', value=Lambientstr, float1=True)
    shaderDecFirstCube.setUniformVariable(key='viewPos', value=LviewPos, float3=True)
    shaderDecFirstCube.setUniformVariable(key='lightPos', value=Lposition, float3=True)
    shaderDecFirstCube.setUniformVariable(key='lightColor', value=Lcolor, float3=True)
    shaderDecFirstCube.setUniformVariable(key='lightIntensity', value=Lintensity, float1=True)
    shaderDecFirstCube.setUniformVariable(key='shininess', value=MshininessFirstcube, float1=True)
    shaderDecFirstCube.setUniformVariable(key='matColor', value=colorCube[0][:3], float3=True)

    shaderDecSecondCube.setUniformVariable(key='model', value=model_cube, mat4=True)
    shaderDecSecondCube.setUniformVariable(key='modelViewProj', value=mvp_cube2, mat4=True)
    shaderDecSecondCube.setUniformVariable(key='model', value=transSecondCube.l2world, mat4=True)
    shaderDecSecondCube.setUniformVariable(key='ambientColor', value=Lambientcolor, float3=True)
    shaderDecSecondCube.setUniformVariable(key='ambientStr', value=Lambientstr, float1=True)
    shaderDecSecondCube.setUniformVariable(key='viewPos', value=LviewPos, float3=True)
    shaderDecSecondCube.setUniformVariable(key='lightPos', value=Lposition, float3=True)
    shaderDecSecondCube.setUniformVariable(key='lightColor', value=Lcolor, float3=True)
    shaderDecSecondCube.setUniformVariable(key='lightIntensity', value=Lintensity, float1=True)
    shaderDecSecondCube.setUniformVariable(key='shininess', value=MshininessSecondcube, float1=True)
    shaderDecSecondCube.setUniformVariable(key='matColor', value=colorCube2[0][:3], float3=True) 

    shaderDecPyramid.setUniformVariable(key='model', value=model_cube, mat4=True)
    shaderDecPyramid.setUniformVariable(key='modelViewProj', value=mvp_pyramid, mat4=True)
    shaderDecPyramid.setUniformVariable(key='model', value=transPyramid.l2world, mat4=True)
    shaderDecPyramid.setUniformVariable(key='ambientColor', value=Lambientcolor, float3=True)
    shaderDecPyramid.setUniformVariable(key='ambientStr', value=Lambientstr, float1=True)
    shaderDecPyramid.setUniformVariable(key='viewPos', value=LviewPos, float3=True)
    shaderDecPyramid.setUniformVariable(key='lightPos', value=Lposition, float3=True)
    shaderDecPyramid.setUniformVariable(key='lightColor', value=Lcolor, float3=True)
    shaderDecPyramid.setUniformVariable(key='lightIntensity', value=Lintensity, float1=True)
    shaderDecPyramid.setUniformVariable(key='shininess', value=MshininessPyramid, float1=True)
    shaderDecPyramid.setUniformVariable(key='matColor', value=colorPyramid[0][:3], float3=True) 

    scene.render_post()

scene.shutdown()



