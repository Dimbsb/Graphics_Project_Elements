
import os
import numpy as np
import Elements.pyECSS.math_utilities as util
from Elements.pyECSS.Entity import Entity
from Elements.pyECSS.Component import BasicTransform, Camera, RenderMesh
from Elements.pyECSS.System import TransformSystem, CameraSystem
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyGLV.GUI.Viewer import RenderGLStateSystem
from Elements.pyGLV.GUI.ImguiDecorator import ImGUIecssDecorator2
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.pyGLV.GL.VertexArray import VertexArray
from OpenGL.GL import GL_LINES
import OpenGL.GL as gl
import Elements.utils.normals as norm
from Elements.utils.terrain import generateTerrain
from Elements.utils.obj_to_mesh import obj_to_mesh

from Elements.utils.Shortcuts import displayGUI_text
example_description = \
"This is a sphere." 

#Light
Lposition = util.vec(2.0, 5.5, 2.0) #uniform lightpos
Lambientcolor = util.vec(1.0, 1.0, 1.0) #uniform ambient color
Lambientstr = 0.3 #uniform ambientStr
LviewPos = util.vec(2.5, 2.8, 5.0) #uniform viewpos
Lcolor = util.vec(1.0,1.0,1.0)
Lintensity = 0.8
#Material
Mshininess = 0.4 
Mcolor = util.vec(0.8, 0.0, 0.8)

winWidth = 1200
winHeight = 800
scene = Scene()  

# Scenegraph with Entities, Components
rootEntity = scene.world.createEntity(Entity(name="RooT"))
entityCam1 = scene.world.createEntity(Entity(name="Entity1"))
scene.world.addEntityChild(rootEntity, entityCam1)
trans1 = scene.world.addComponent(entityCam1, BasicTransform(name="Entity1_TRS", trs=util.translate(0,0,-8)))

eye = util.vec(1, 0.54, 1.0)
target = util.vec(0.02, 0.14, 0.217)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 1.0, 10.0)   

m = np.linalg.inv(projMat @ view)

entityCam2 = scene.world.createEntity(Entity(name="Entity_Camera"))
scene.world.addEntityChild(entityCam1, entityCam2)
trans2 = scene.world.addComponent(entityCam2, BasicTransform(name="Camera_TRS", trs=util.identity()))
orthoCam = scene.world.addComponent(entityCam2, Camera(m, "orthoCam","Camera","500"))

#first cube from here
node4 = scene.world.createEntity(Entity(name="FirstCube"))
scene.world.addEntityChild(rootEntity, node4)
trans4 = scene.world.addComponent(node4, BasicTransform(name="Object_TRS", trs=util.scale(0.3)@util.translate(0,0.5,0) ))
mesh4 = scene.world.addComponent(node4, RenderMesh(name="Object_mesh"))
#first cube from here

#second cube from here
node5 = scene.world.createEntity(Entity(name="SecondCube"))
scene.world.addEntityChild(rootEntity, node5)
trans5 = scene.world.addComponent(node5, BasicTransform(name="SecondCube_TRS", trs=util.scale(0.3) @ util.translate(2.0, 0.5, 0)))
mesh5 = scene.world.addComponent(node5, RenderMesh(name="SecondCube_mesh"))
#second cube till here

#Pyramid from here
nodePyramid = scene.world.createEntity(Entity(name="Pyramid"))
scene.world.addEntityChild(rootEntity, nodePyramid)  # Make Pyramid a child of the cube
transPyramid = scene.world.addComponent(nodePyramid, BasicTransform(name="Pyramid_TRS", trs=util.scale(0.3) @ util.translate(0,0.8,0)))  # Position it on top of the cube
meshPyramid = scene.world.addComponent(nodePyramid, RenderMesh(name="Pyramid_mesh"))
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
    [1.0, 1.0, 0.0, 1.0],  
    [1.0, 1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0, 1.0],
], dtype=np.float32)

indexAxes = np.array((0,1,2,3,4,5), np.uint32) 
indexCube = np.array((1,0,3, 1,3,2, 
                  2,3,7, 2,7,6,
                  3,0,4, 3,4,7,
                  6,5,1, 6,1,2,
                  4,5,6, 4,6,7,
                  5,4,0, 5,0,1), np.uint32) 

#Simple Cube till here


# A simple Pyramid from here 
vertexPyramid = np.array([
    [0.0, 1, 0.0, 1.0],   
    [-0.6, 0.0, -0.5, 1.0], 
    [0.6, 0.0, -0.5, 1.0],  
    [0.6, 0.0, 0.5, 1.0],   
    [-0.6, 0.0, 0.5, 1.0], 
], dtype=np.float32)

indexPyramid = np.array([
    0, 1, 2, 
    0, 2, 3,  
    0, 3, 4,  
    0, 4, 1,  
], dtype=np.uint32)

colorPyramid = np.array([
    [0.5, 0.4, 1.0, 1.0],  
    [0.5, 0.4, 1.0, 1.0],  
    [0.5, 0.4, 1.0, 1.0],  
    [0.5, 0.4, 1.0, 1.0],  
    [0.5, 0.4, 1.0, 1.0],  
], dtype=np.float32)
# A simple Pyramid till here 


# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())

vertices, indices, colors, normals = norm.generateSmoothNormalsMesh(vertexCube , indexCube, colorCube)

#first cube from here
mesh4.vertex_attributes.append(vertices)
mesh4.vertex_attributes.append(colors)
mesh4.vertex_attributes.append(normals)
mesh4.vertex_index.append(indices)
vArray4 = scene.world.addComponent(node4, VertexArray())
shaderDec4 = scene.world.addComponent(node4, ShaderGLDecorator(Shader(vertex_source = Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG)))
#first cube till here

#second cube from here
mesh5.vertex_attributes.append(vertices)
mesh5.vertex_attributes.append(colors)
mesh5.vertex_attributes.append(normals)
mesh5.vertex_index.append(indices)
vArray5 = scene.world.addComponent(node5, VertexArray())
shaderDec5 = scene.world.addComponent(node5, ShaderGLDecorator(Shader(vertex_source=Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG)))
#second cube till here

#pyramid from here
meshPyramid.vertex_attributes.append(vertexPyramid)
meshPyramid.vertex_attributes.append(colorPyramid)
meshPyramid.vertex_index.append(indexPyramid)
vArrayPyramid = scene.world.addComponent(nodePyramid, VertexArray())
shaderDecPyramid = scene.world.addComponent(nodePyramid, ShaderGLDecorator(Shader(vertex_source=Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG)))
#pyramid till here

# Generate terrain
vertexTerrain, indexTerrain, colorTerrain= generateTerrain(size=4,N=20)
# Add terrain
terrain = scene.world.createEntity(Entity(name="terrain"))
scene.world.addEntityChild(rootEntity, terrain)
terrain_trans = scene.world.addComponent(terrain, BasicTransform(name="terrain_trans", trs=util.identity()))
terrain_mesh = scene.world.addComponent(terrain, RenderMesh(name="terrain_mesh"))
terrain_mesh.vertex_attributes.append(vertexTerrain) 
terrain_mesh.vertex_attributes.append(colorTerrain)
terrain_mesh.vertex_index.append(indexTerrain)
terrain_vArray = scene.world.addComponent(terrain, VertexArray(primitive=GL_LINES))
terrain_shader = scene.world.addComponent(terrain, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))

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
eye = util.vec(2.5, 2.5, 2.5)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)  
projMat = util.perspective(50.0, winWidth/winHeight, 0.01, 100.0)   
gWindow._myCamera = view # otherwise, an imgui slider must be moved to properly update
model_terrain_axes = util.translate(0.0,0.0,0.0)
model_cube = util.scale(1.0) @ util.translate(0.0,0.5,0.0)



while running:
    running = scene.render()
    displayGUI_text(example_description)
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.world.traverse_visit_pre_camera(camUpdate, orthoCam)
    scene.world.traverse_visit(camUpdate, scene.world.root)
    scene.world.traverse_visit(transUpdate, scene.world.root)
    view =  gWindow._myCamera # updates view via the imgui
    mvp_terrain = projMat @ view @ terrain_trans.trs

    #first cube from here
    mvp_cube = projMat @ view @ trans4.l2world
    terrain_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain, mat4=True)
    shaderDec4.setUniformVariable(key='modelViewProj', value=mvp_cube, mat4=True)
    shaderDec4.setUniformVariable(key='model',value=trans4.l2world,mat4=True)
    shaderDec4.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
    shaderDec4.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
    shaderDec4.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
    shaderDec4.setUniformVariable(key='lightPos',value=Lposition,float3=True)
    shaderDec4.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
    shaderDec4.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
    shaderDec4.setUniformVariable(key='shininess',value=Mshininess,float1=True)
    shaderDec4.setUniformVariable(key='matColor',value=Mcolor,float3=True)
    #first cube till here

    #second cube from here
    mvp_cube2 = projMat @ view @ trans5.l2world
    shaderDec5.setUniformVariable(key='modelViewProj', value=mvp_cube2, mat4=True)
    shaderDec5.setUniformVariable(key='model', value=trans5.l2world, mat4=True)
    shaderDec5.setUniformVariable(key='ambientColor', value=Lambientcolor, float3=True)
    shaderDec5.setUniformVariable(key='ambientStr', value=Lambientstr, float1=True)
    shaderDec5.setUniformVariable(key='viewPos', value=LviewPos, float3=True)
    shaderDec5.setUniformVariable(key='lightPos', value=Lposition, float3=True)
    shaderDec5.setUniformVariable(key='lightColor', value=Lcolor, float3=True)
    shaderDec5.setUniformVariable(key='lightIntensity', value=Lintensity, float1=True)
    shaderDec5.setUniformVariable(key='shininess', value=Mshininess, float1=True)
    shaderDec5.setUniformVariable(key='matColor', value=Mcolor, float3=True)
    #second cube till here

    #pyramid from here
    mvp_pyramid = projMat @ view @ transPyramid.l2world
    shaderDecPyramid.setUniformVariable(key='modelViewProj', value=mvp_pyramid, mat4=True)
    shaderDecPyramid.setUniformVariable(key='model', value=transPyramid.l2world, mat4=True)
    shaderDecPyramid.setUniformVariable(key='ambientColor', value=Lambientcolor, float3=True)
    shaderDecPyramid.setUniformVariable(key='ambientStr', value=Lambientstr, float1=True)
    shaderDecPyramid.setUniformVariable(key='viewPos', value=LviewPos, float3=True)
    shaderDecPyramid.setUniformVariable(key='lightPos', value=Lposition, float3=True)
    shaderDecPyramid.setUniformVariable(key='lightColor', value=Lcolor, float3=True)
    shaderDecPyramid.setUniformVariable(key='lightIntensity', value=Lintensity, float1=True)
    shaderDecPyramid.setUniformVariable(key='shininess', value=Mshininess, float1=True)
    shaderDecPyramid.setUniformVariable(key='matColor', value=Mcolor, float3=True)
    #pyramid till here

    scene.render_post()
    
scene.shutdown()
