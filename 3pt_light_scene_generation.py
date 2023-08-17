import maya.cmds as cmds

'''
    Creates a plane with 1x1 subdivision called backdrop for a polyPlane transform node
    Sets the scale and Z transform
    Applies an arnold shader
    Returns the plane
'''
def create_plane():
    plane = cmds.polyPlane(sx=1, sy=1, name='backdrop')[0]
    cmds.scale(10,10,8, plane)

    apply_arnold_shader(plane, 'planeShader')

    return plane

'''
    Selects the edge[3] of the plane
    Extrudes the edge and sets its localTranslateZ to 10
    Bevels the edge and sets its segments and offset
'''
def plane_curve(plane):
    edge = f'{plane}.e[3]'
    extrude = cmds.polyExtrudeEdge(edge)[0]
    cmds.setAttr(extrude + '.localTranslateZ', 5)

    bevel = cmds.polyBevel3(edge)[0]
    cmds.setAttr(bevel + '.segments', 10)
    cmds.setAttr(bevel + '.offset', 0.15)

'''
    creates a new arnold shader with the name objectShader
    gets the name of the object created, selects it, and applies the shader
'''
def apply_arnold_shader(object, name=str):
    arnold_shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=name)
    cmds.select(object)
    cmds.hyperShade(assign=arnold_shader)

# creates the key light and sets it's transform and rotation
def create_key_light():
    area_light = cmds.shadingNode('aiAreaLight', asLight=True)
    area_light = cmds.rename(area_light, 'keyLight')

    cmds.setAttr(f'{area_light}.translate', -2.5, 2.5, 2.5)
    cmds.setAttr(f'{area_light}.rotate', -15, -45, 0)
    cmds.setAttr(f'{area_light}.aiExposure', 5)
    return area_light

# creates the rim light and sets it's transform and rotation
def create_rim_light():
    area_light = cmds.shadingNode('aiAreaLight', asLight=True)
    area_light = cmds.rename(area_light, 'rimLight')

    cmds.setAttr(f'{area_light}.translate', 2.5, 2.5, -2.5)
    cmds.setAttr(f'{area_light}.rotate', -15, 135 , 0)
    cmds.setAttr(f'{area_light}.aiExposure', 2.5)
    return area_light

# creates the fill light and sets it's transform and rotation
def create_fill_light():
    area_light = cmds.shadingNode('aiAreaLight', asLight=True)
    area_light = cmds.rename(area_light, 'fillLight')

    cmds.setAttr(f'{area_light}.translate', 2.5, 2.5, 2.5)
    cmds.setAttr(f'{area_light}.rotate', -15, 45, 0)
    cmds.setAttr(f'{area_light}.aiExposure', 3)
    return area_light

# calls the 3 lighting functions to create 3pt lighting
def create_3pt_lighting():
    light_group = cmds.group(em=True, name='Lights')
    key = create_key_light()
    rim = create_rim_light()
    fill = create_fill_light()

    cmds.parent(key, rim, fill, light_group)

    return light_group

# creates a camera and sets it's transform and rotation
def create_camera():
    camera = cmds.camera(name='potraitCamera')[0]

    cmds.setAttr(f'{camera}.translate', 0,2,4)
    cmds.setAttr(f'{camera}.rotate', -10, 0, 0)
    return camera

'''
    Creates a nurbsCircle named setup_controller
    Scales, moves and rotates the controller so that it floats above the objects
    Selects the controller
    Freezes the transform, rotate and scale values
'''
def create_controller():
    controller = cmds.circle(name='setup_controller')[0]
    cmds.scale(2,2,2, controller)
    cmds.move(0,5,0, controller)
    cmds.rotate(-90,0,0, controller)

    cmds.select(controller)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, rotate=True)
    return controller

'''
    Creates a group for the camera, plane, and lights, named Cam_Lights_BG
    Constrains the group to the controller
'''
def parent_controller(controller, camera, plane, lights):
    group = cmds.group(camera, plane, lights, name='Cam_Lights_BG')
    cmds.parentConstraint(controller, group, maintainOffset=True)

if __name__ == '__main__':
    plane = create_plane()
    plane_curve(plane)
    
    lights = create_3pt_lighting()

    camera = create_camera()

    controller = create_controller()
    parent_controller(controller, camera, plane, lights)