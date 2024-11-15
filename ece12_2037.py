
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
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.utils.Shortcuts import displayGUI_text
example_description = \
"Cubes, Pyramid and House."  

#Light
Lposition = util.vec(2.0, 5.5, 2.0) 
Lambientcolor = util.vec(1.0, 1.0, 1.0) 
Lambientstr = 0.3 
LviewPos = util.vec(2.5, 2.8, 5.0) 
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
FirstCube = scene.world.createEntity(Entity(name="FirstCube"))
scene.world.addEntityChild(rootEntity, FirstCube)
transFirstCube = scene.world.addComponent(FirstCube, BasicTransform(name="Object_TRS"))
meshFirstCube = scene.world.addComponent(FirstCube, RenderMesh(name="Object_mesh"))
#first cube from here

#second cube from here
SecondCube = scene.world.createEntity(Entity(name="SecondCube"))
scene.world.addEntityChild(rootEntity, SecondCube)
transSecondCube = scene.world.addComponent(SecondCube, BasicTransform(name="SecondCube_TRS"))
meshSecondCube = scene.world.addComponent(SecondCube, RenderMesh(name="SecondCube_mesh"))
#second cube till here

#Pyramid from here
Pyramid = scene.world.createEntity(Entity(name="Pyramid"))
scene.world.addEntityChild(rootEntity, Pyramid)  # Make Pyramid a child of the cube
transPyramid = scene.world.addComponent(Pyramid, BasicTransform(name="Pyramid_TRS"))  # Position it on top of the cube
meshPyramid = scene.world.addComponent(Pyramid, RenderMesh(name="Pyramid_mesh"))
#Pyramid till here

# Home from here
# Create an Entity home as child of the root.
nodehome = scene.world.createEntity(Entity(name="Home"))
scene.world.addEntityChild(rootEntity, nodehome)
# Set the cube and the pyramid as Entity child of entity home.
scene.world.addEntityChild(nodehome, SecondCube)
scene.world.addEntityChild(nodehome, Pyramid)
transhome = scene.world.addComponent(nodehome, BasicTransform(name="Object_TRS"))
meshhome = scene.world.addComponent(nodehome, RenderMesh(name="Object_mesh"))
# Home till here

#new imgui from here
#initiallizations
FirstCube_imgui_trans =  [2.0 , 0.0 , 0.0]
SecondCube_imgui_trans = [0.0, 0.0, 0.0]
Pyramid_imgui_trans = [0.0, 0.28, 0.0]  
Home_imgui_trans = [0.0, 0.0, 0.0]
Pyramid_imgui_scale = [1.0, 3.0, 1.0]
FirstCube_imgui_rotation = SecondCube_imgui_rotation = Pyramid_imgui_rotation = Home_imgui_rotation = [0.0, 0.0, 0.0] 
FirstCube_imgui_scale = SecondCube_imgui_scale =  Home_imgui_scale = [1.0, 1.0, 1.0]

showAxes = True
showTerrain = True
cube1_visibility = True
cube2_visibility = True
Pyramid_visibility = True
Home_visibility = True

def display(FirstCube_imgui_trans, SecondCube_imgui_trans, Pyramid_imgui_trans, Home_imgui_trans, 
            FirstCube_imgui_rotation, SecondCube_imgui_rotation, Pyramid_imgui_rotation, Home_imgui_rotation, 
            FirstCube_imgui_scale, SecondCube_imgui_scale, Pyramid_imgui_scale, Home_imgui_scale, cube1_visibility, cube2_visibility, Pyramid_visibility, Home_visibility, showAxes, showTerrain):

    imgui.begin("TRS")

    #changed_c1, c1_trans = imgui.drag_float3("Cube1 translation", c1_trans, change_speed=0.1)
    changed_FirstCube, new_FirstCube_imgui_trans = imgui.drag_float3("Cube1 Translation", *FirstCube_imgui_trans, change_speed=0.1)
    changed_FirstCube_rotation, new_FirstCube_imgui_rotation = imgui.drag_float3("Cube1 Rotation", *FirstCube_imgui_rotation, change_speed=0.1)
    changed_FirstCube_scale, new_FirstCube_imgui_scale = imgui.drag_float3("Cube1 Scale", *FirstCube_imgui_scale, change_speed=0.1)
    changed_SecondCube, new_SecondCube_imgui_trans = imgui.drag_float3("Cube2 Translation", *SecondCube_imgui_trans, change_speed=0.1)
    changed_SecondCube_rotation, new_SecondCube_imgui_rotation = imgui.drag_float3("Cube2 Rotation", *SecondCube_imgui_rotation, change_speed=0.1)
    changed_SecondCube_scale, new_SecondCube_imgui_scale = imgui.drag_float3("Cube2 Scale", *SecondCube_imgui_scale, change_speed=0.1)
    changed_Pyramid, new_Pyramid_imgui_trans = imgui.drag_float3("Pyramid Translation", *Pyramid_imgui_trans, change_speed=0.1)
    changed_Pyramid_rotation, new_Pyramid_imgui_rotation = imgui.drag_float3("Pyramid Rotation", *Pyramid_imgui_rotation, change_speed=0.1)
    changed_Pyramid_scale, new_Pyramid_imgui_scale = imgui.drag_float3("Pyramid Scale", *Pyramid_imgui_scale, change_speed=0.1)
    changed_home, new_home_imgui_trans = imgui.drag_float3("Home Translation", *Home_imgui_trans, change_speed=0.1)
    changed_Home_rotation, new_Home_imgui_rotation = imgui.drag_float3("Home Rotation", *Home_imgui_rotation, change_speed=0.1)
    changed_Home_scale, new_Home_imgui_scale = imgui.drag_float3("Home Scale", *Home_imgui_scale, change_speed=0.1)
    #clicked, showAxes = imgui.checkbox("Show Axes", showAxes)
    changed_cube1_visibility, cube1_visibility = imgui.checkbox("Show Cube 1",cube1_visibility)
    changed_cube2_visibility, cube2_visibility = imgui.checkbox("Show Cube 2",cube2_visibility)
    changed_Pyramid_visibility, Pyramid_visibility = imgui.checkbox("Show Pyramid",Pyramid_visibility)
    changed_Home_visibility, Home_visibility = imgui.checkbox("Show Home",Home_visibility)
    changed_showAxes, showAxes = imgui.checkbox("Show Axes",showAxes)
    changed_showTerrain, showTerrain = imgui.checkbox("Show Terrain",showTerrain)

    #Visibility
    #We can make this with all shapes in order to see (True-False) about Checkbox
    #if changed_cube1_visibility:
       # print({cube1_visibility})

    #if changed_c1:
    #Translation
    if changed_FirstCube:
        FirstCube_imgui_trans = list(new_FirstCube_imgui_trans)

    if changed_SecondCube:
        SecondCube_imgui_trans = list(new_SecondCube_imgui_trans)

    if  changed_Pyramid:
        Pyramid_imgui_trans = list(new_Pyramid_imgui_trans)

    if changed_home:
        Home_imgui_trans = list(new_home_imgui_trans)

    #Rotation
    if changed_FirstCube_rotation:
        FirstCube_imgui_rotation = list(new_FirstCube_imgui_rotation)

    if changed_SecondCube_rotation:
        SecondCube_imgui_rotation = list(new_SecondCube_imgui_rotation)

    if changed_Pyramid_rotation:
        Pyramid_imgui_rotation = list(new_Pyramid_imgui_rotation)

    if changed_Home_rotation:
        Home_imgui_rotation = list(new_Home_imgui_rotation)

    #Scale
    if changed_FirstCube_scale:
        FirstCube_imgui_scale = list(new_FirstCube_imgui_scale)

    if changed_SecondCube_scale:
        SecondCube_imgui_scale = list(new_SecondCube_imgui_scale)

    if changed_Pyramid_scale:
        Pyramid_imgui_scale = list(new_Pyramid_imgui_scale)

    if changed_Home_scale:
        Home_imgui_scale = list(new_Home_imgui_scale)

    imgui.end()
    return (FirstCube_imgui_trans, SecondCube_imgui_trans, Pyramid_imgui_trans, Home_imgui_trans, 
FirstCube_imgui_rotation,SecondCube_imgui_rotation, Pyramid_imgui_rotation, Home_imgui_rotation, 
FirstCube_imgui_scale, SecondCube_imgui_scale, Pyramid_imgui_scale, Home_imgui_scale, cube1_visibility, cube2_visibility, Pyramid_visibility, Home_visibility, showAxes, showTerrain)
#new imgui till here

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
    [1.0, 0.4, 0.1, 1.0],  
    [1.0, 0.4, 0.1, 1.0],
    [1.0, 0.4, 0.1, 1.0],
    [1.0, 0.4, 0.1, 1.0],
    [1.0, 0.4, 0.1, 1.0],
    [1.0, 0.4, 0.1, 1.0],
    [1.0, 0.4, 0.1, 1.0],
    [1.0, 0.4, 0.1, 1.0],
], dtype=np.float32)

indexCube = np.array((1,0,3, 1,3,2, 
                  2,3,7, 2,7,6,
                  3,0,4, 3,4,7,
                  6,5,1, 6,1,2,
                  4,5,6, 4,6,7,
                  5,4,0, 5,0,1), np.uint32) 
#Simple Cube till here

# A simple Pyramid from here 
vertexPyramid = np.array([
    [0.0, 0.3, 0.0, 1.0],   
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

#Axes from here
vertexAxes = np.array([
    [0.0, 0.0, 0.0, 1.0],
    [1.5, 0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 1.5, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 1.5, 1.0]
],dtype=np.float32) 
colorAxes = np.array([
    [1.0, 0.0, 0.0, 1.0],
    [1.0, 0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 1.0],
    [0.0, 0.0, 1.0, 1.0]
], dtype=np.float32)

indexAxes = np.array((0,1,2,3,4,5), np.uint32) 
#Axes till here

# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())
vertices, indices, colors, normals = norm.generateSmoothNormalsMesh(vertexCube , indexCube, colorCube)

#first cube from here
meshFirstCube.vertex_attributes.append(vertices)
meshFirstCube.vertex_attributes.append(colors)
meshFirstCube.vertex_attributes.append(normals)
meshFirstCube.vertex_index.append(indices)
vArrayFirstCube = scene.world.addComponent(FirstCube, VertexArray())
shaderDecFirstCube = scene.world.addComponent(FirstCube, ShaderGLDecorator(Shader(vertex_source = Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG)))
#first cube till here

#second cube from here
meshSecondCube.vertex_attributes.append(vertices)
meshSecondCube.vertex_attributes.append(colors)
meshSecondCube.vertex_attributes.append(normals)
meshSecondCube.vertex_index.append(indices)
vArraySecondCube = scene.world.addComponent(SecondCube, VertexArray())
shaderDecSecondCube = scene.world.addComponent(SecondCube, ShaderGLDecorator(Shader(vertex_source=Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG)))
#second cube till here

#pyramid from here
meshPyramid.vertex_attributes.append(vertexPyramid)
meshPyramid.vertex_attributes.append(colorPyramid)
meshPyramid.vertex_index.append(indexPyramid)
vArrayPyramid = scene.world.addComponent(Pyramid, VertexArray())
shaderDecPyramid = scene.world.addComponent(Pyramid, ShaderGLDecorator(Shader(vertex_source=Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG)))
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
# terrain_shader.setUniformVariable(key='modelViewProj', value=mvpMat, mat4=True)

## ADD AXES ##
axes = scene.world.createEntity(Entity(name="axes"))
scene.world.addEntityChild(rootEntity, axes)
axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.translate(0.0, 0.001, 0.0))) #util.identity()
axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))
axes_mesh.vertex_attributes.append(vertexAxes) 
axes_mesh.vertex_attributes.append(colorAxes)
axes_mesh.vertex_index.append(indexAxes)
axes_vArray = scene.world.addComponent(axes, VertexArray(primitive=gl.GL_LINES)) # note the primitive change
axes_shader = scene.world.addComponent(axes, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))

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

    #new imgui from here
    #display function from here
    FirstCube_imgui_trans, SecondCube_imgui_trans, Pyramid_imgui_trans, Home_imgui_trans, FirstCube_imgui_rotation, SecondCube_imgui_rotation, Pyramid_imgui_rotation, Home_imgui_rotation, FirstCube_imgui_scale, SecondCube_imgui_scale, Pyramid_imgui_scale, Home_imgui_scale, cube1_visibility, cube2_visibility, Pyramid_visibility, Home_visibility, showAxes, showTerrain = display(
        FirstCube_imgui_trans, SecondCube_imgui_trans, Pyramid_imgui_trans, Home_imgui_trans, 
        FirstCube_imgui_rotation, SecondCube_imgui_rotation, Pyramid_imgui_rotation, Home_imgui_rotation, 
        FirstCube_imgui_scale, SecondCube_imgui_scale, Pyramid_imgui_scale, Home_imgui_scale, cube1_visibility, cube2_visibility, Pyramid_visibility, Home_visibility, showAxes, showTerrain)
    #display function till here

    #Rotation calc x,y,z
    x1, y1, z1 = FirstCube_imgui_rotation
    rotation_matrix1 = (util.rotate(axis=(1.0, 0.0, 0.0), angle=x1) @ util.rotate(axis=(0.0, 1.0, 0.0), angle=y1) @ util.rotate(axis=(0.0, 0.0, 1.0), angle=z1))
    x2, y2, z2 = SecondCube_imgui_rotation
    rotation_matrix2 = (util.rotate(axis=(1.0, 0.0, 0.0), angle=x2) @ util.rotate(axis=(0.0, 1.0, 0.0), angle=y2) @ util.rotate(axis=(0.0, 0.0, 1.0), angle=z2))
    xP, yP, zP = Pyramid_imgui_rotation
    rotation_matrix3 = (util.rotate(axis=(1.0, 0.0, 0.0), angle=xP) @ util.rotate(axis=(0.0, 1.0, 0.0), angle=yP) @ util.rotate(axis=(0.0, 0.0, 1.0), angle=zP))
    xH, yH, zH = Home_imgui_rotation
    rotation_matrix4 = (util.rotate(axis=(1.0, 0.0, 0.0), angle=xH) @ util.rotate(axis=(0.0, 1.0, 0.0), angle=yH) @ util.rotate(axis=(0.0, 0.0, 1.0), angle=zH))

    #Scale calculation
    FirstCube_imgui_scale_matrix = util.scale(*FirstCube_imgui_scale)
    SecondCube_imgui_scale_matrix = util.scale(*SecondCube_imgui_scale)
    Pyramid_imgui_scale_matrix = util.scale(*Pyramid_imgui_scale)
    Home_imgui_scale_matrix = util.scale(*Home_imgui_scale)

    #TRS
    transFirstCube.trs =  util.translate(FirstCube_imgui_trans[0], FirstCube_imgui_trans[1], FirstCube_imgui_trans[2]) @ rotation_matrix1 @ FirstCube_imgui_scale_matrix
    transSecondCube.trs =  util.translate(SecondCube_imgui_trans[0], SecondCube_imgui_trans[1], SecondCube_imgui_trans[2]) @ rotation_matrix2 @ SecondCube_imgui_scale_matrix
    transPyramid.trs =  util.translate(Pyramid_imgui_trans[0], Pyramid_imgui_trans[1], Pyramid_imgui_trans[2]) @ rotation_matrix3 @ Pyramid_imgui_scale_matrix 
    transhome.trs =  util.translate(Home_imgui_trans[0], Home_imgui_trans[1],  Home_imgui_trans[2]) @ rotation_matrix4 @ Home_imgui_scale_matrix  

    #Visibility
    if cube1_visibility == True:
        mvp_cube = projMat @ view @ transFirstCube.l2world 
    else:
        mvp_cube = False

    if cube2_visibility == True:
        mvp_cube2 = projMat @ view @ transSecondCube.l2world 
    else:
        mvp_cube2 = False

    if Pyramid_visibility == True:
        mvp_pyramid = projMat @ view @ transPyramid.l2world
    else:
        mvp_pyramid = False

    #Μπορούμε να το κάνουμε με την λογική #mvp_cube2 και #mvp_pyramid ωστόσο με αυτό το τρόπο οι ξεχωριστοί έλεγχοι για το cub2 και το pyramid δεν θα είναι λειτουργικοί.
    
    #if Home_visibility == True:
        #mvp_home = ...
       #mvp_cube2 = projMat @ view @ transSecondCube.l2world
       #mvp_pyramid = projMat @ view @ transPyramid.l2world
    #else:
        #mvp_home=False
         #mvp_cube2 = False
         #mvp_pyramid = False

    if showAxes == True:
        mvp_axes = projMat @ view @ axes_trans.trs
    else:
        mvp_axes = False

    if showTerrain == True:
        mvp_terrain = projMat @ view @ terrain_trans.trs
    else:
        mvp_terrain = False

    #new imgui till here

    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.world.traverse_visit_pre_camera(camUpdate, orthoCam)
    scene.world.traverse_visit(camUpdate, scene.world.root)
    scene.world.traverse_visit(transUpdate, scene.world.root)
    view =  gWindow._myCamera 
    axes_shader.setUniformVariable(key='modelViewProj', value = mvp_axes, mat4=True)
    terrain_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain, mat4=True)
    terrain_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain, mat4=True)

    #first cube from here
    shaderDecFirstCube.setUniformVariable(key='modelViewProj', value=mvp_cube, mat4=True)
    shaderDecFirstCube.setUniformVariable(key='model',value=transFirstCube.l2world,mat4=True)
    shaderDecFirstCube.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
    shaderDecFirstCube.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
    shaderDecFirstCube.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
    shaderDecFirstCube.setUniformVariable(key='lightPos',value=Lposition,float3=True)
    shaderDecFirstCube.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
    shaderDecFirstCube.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
    shaderDecFirstCube.setUniformVariable(key='shininess',value=Mshininess,float1=True)
    shaderDecFirstCube.setUniformVariable(key='matColor',value=Mcolor,float3=True)
    #first cube till here

    #second cube from here
    shaderDecSecondCube.setUniformVariable(key='modelViewProj', value=mvp_cube2, mat4=True)
    shaderDecSecondCube.setUniformVariable(key='model', value=transSecondCube.l2world, mat4=True)
    shaderDecSecondCube.setUniformVariable(key='ambientColor', value=Lambientcolor, float3=True)
    shaderDecSecondCube.setUniformVariable(key='ambientStr', value=Lambientstr, float1=True)
    shaderDecSecondCube.setUniformVariable(key='viewPos', value=LviewPos, float3=True)
    shaderDecSecondCube.setUniformVariable(key='lightPos', value=Lposition, float3=True)
    shaderDecSecondCube.setUniformVariable(key='lightColor', value=Lcolor, float3=True)
    shaderDecSecondCube.setUniformVariable(key='lightIntensity', value=Lintensity, float1=True)
    shaderDecSecondCube.setUniformVariable(key='shininess', value=Mshininess, float1=True)
    shaderDecSecondCube.setUniformVariable(key='matColor', value=Mcolor, float3=True)
    #second cube till here

    #pyramid from here
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



