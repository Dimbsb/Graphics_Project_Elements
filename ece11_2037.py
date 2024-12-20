import numpy as np
from OpenGL.GL import GL_LINES
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyECSS.Entity import Entity
import Elements.pyECSS.math_utilities as util
from Elements.utils.terrain import generateTerrain
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.pyGLV.GUI.Viewer import RenderGLStateSystem
from Elements.pyECSS.System import TransformSystem, CameraSystem
from Elements.pyGLV.GUI.ImguiDecorator import ImGUIecssDecorator2
from Elements.pyECSS.Component import BasicTransform, Camera, RenderMesh
from Elements.pyGLV.GL.Shader import (InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem)
from Elements.utils.Shortcuts import displayGUI_text
example_description = "This is a sphere."

winWidth = 1024
winHeight = 768
scene = Scene()

rootEntity = scene.world.createEntity(Entity(name="RooT"))
entityCam1 = scene.world.createEntity(Entity(name="entityCam1"))
scene.world.addEntityChild(rootEntity, entityCam1)
trans1 = scene.world.addComponent(entityCam1, BasicTransform(name="trans1", trs=util.identity()))

eye = util.vec(1, 0.54, 1.0)
target = util.vec(0.02, 0.14, 0.217)
up = util.vec(0.0, 1.0, 1.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 1.0, 10.0)
m = np.linalg.inv(projMat @ view)

entityCam2 = scene.world.createEntity(Entity(name="entityCam2"))
scene.world.addEntityChild(entityCam1, entityCam2)
trans2 = scene.world.addComponent(entityCam2, BasicTransform(name="trans2", trs=util.identity()))
orthoCam = scene.world.addComponent(entityCam2, Camera(m, "orthoCam", "Camera", "500"))

sphere = scene.world.createEntity(Entity(name="sphere"))
scene.world.addEntityChild(rootEntity, sphere)
transSphere = scene.world.addComponent(sphere, BasicTransform(name="transSphere", trs=util.translate(0, 0.5, 0)))  
meshSphere = scene.world.addComponent(sphere, RenderMesh(name="meshSphere"))

initiallcolor = [1.0, 1.0, 1.0, 1.0]
vertices = []
colors = []
indices = []
normals = []

k = 30
radius = 1 # Για να ρυθμίζουμε την ακτίνα.
for i in range(0, k):
    for j in range(0, k):
        x = radius* np.cos(2 * np.pi * j / k) * np.sin(np.pi * i / k)
        y = radius* np.cos(np.pi * i / k)
        z = radius* np.sin(2 * np.pi * j / k) * np.sin(np.pi * i / k)
        vertices.append([x, y, z, 1.0])
        indices.append(i * k + j)
        indices.append((i + 1) * k + j)
        indices.append((i + 1) * k + (j + 1) % k)
        indices.append(i * k + j)
        indices.append((i + 1) * k + (j + 1) % k)
        indices.append(i * k + (j + 1) % k)
        normals.append([x, y, z, 1.0])
        #Α) Να υλοποιήστε μια σκηνή που θα περιέχει μία σφαίρα. Πατώντας το wireframe checkbox θα εμφανίζονται μόνο οι ακμές/κορυφές της.
        ##########
        colors.append(initiallcolor); 
        
        # Β) Να υλοποιήστε μία σκηνή που θα περιέχει 1 σφαίρα με διαφορετική ακτίνα και διαφορετικό πλήθος κορυφών/ακμών,
        # της οποίας το χρώμα θα αλλάζει ανάλογα με το ύψος (συντεταγμένη y) κάθε κορυφής (πχ. ξεκινώντας από την κορυφή της σφαίρας με κόκκινο και καταλήγοντας στη βάση
        # της σφαίρας σε κίτρινο).
        ##########
        #colors.append([1.0,-y,0.0]);

        # Γ) Να υλοποιήστε μία σκηνή που θα περιέχει 1 σφαίρα με διαφορετική ακτίνα και διαφορετικό
        # πλήθος κορυφών/ακμών, της οποίας το χρώμα σε κάθε κορυφή να ισούται με το normal σε αυτή την κορυφή.
        ##########
        #colors = normals
      
# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())

## ADD SPHERE ##
meshSphere.vertex_attributes.append(vertices)
meshSphere.vertex_attributes.append(colors)
meshSphere.vertex_index.append(indices)
vArray4 = scene.world.addComponent(sphere, VertexArray())
shaderDec4 = scene.world.addComponent(sphere,ShaderGLDecorator(Shader(vertex_source=Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)),)

# MAIN RENDERING LOOP
running = True
scene.init(imgui=True,windowWidth=winWidth, windowHeight=winHeight, windowTitle="Elements: A Working Event Manager", customImGUIdecorator=ImGUIecssDecorator2, openGLversion=4)
scene.world.traverse_visit(initUpdate, scene.world.root)

################### EVENT MANAGER ###################
eManager = scene.world.eventManager
gWindow = scene.renderWindow
gGUI = scene.gContext
renderGLEventActuator = RenderGLStateSystem()
eManager._subscribers["OnUpdateWireframe"] = gWindow
eManager._actuators["OnUpdateWireframe"] = renderGLEventActuator
eManager._subscribers["OnUpdateCamera"] = gWindow
eManager._actuators["OnUpdateCamera"] = renderGLEventActuator

eye = util.vec(2.5, 2.5, 2.5)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 0.01, 10.0)
gWindow._myCamera = view
sphere = transSphere.trs

while running:
    running = scene.render()
    displayGUI_text(example_description)
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.world.traverse_visit_pre_camera(camUpdate, orthoCam)
    scene.world.traverse_visit(camUpdate, scene.world.root)
    view = gWindow._myCamera  
    mvp_sphere = projMat @ view @ sphere
    shaderDec4.setUniformVariable(key="modelViewProj", value=mvp_sphere, mat4=True)

    scene.render_post()

scene.shutdown()
