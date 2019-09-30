bl_info = {
    "name": "3D Pack Objects",
    "description": "Packs objects into a defined space using their bounding boxes.",
    "author": "Johnathan Apuzen",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Sidebar > 3D Pack Panel",
    "category": "Object",
}

import bpy
from math import radians
from bpy.props import (FloatProperty,
                       BoolProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

#variable that holds pack area object
packArea = None

'''****************************************
PACK AREA OUTLINE
****************************************'''
#Update/generate pack area outline       
def updatePackArea(self, context):
    scene = context.scene
    global packArea
    
    #Check if packArea is a valid object, if not it was probably deleted
    try:
        packArea.name
    except:
        packArea = None
    
    if packArea == None:
        #Checks if object with same name exists
        if 'Pack Area Outline' in bpy.data.objects:
            packArea = bpy.data.objects.get('Pack Area Outline')
        #Create new packArea
        else:
            #save previous active object to revert back to it after outline is created
            #prevents the outline from being selected and packed
            
            
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, location=(0,0,0))
            packArea = context.active_object
            packArea.display_type = 'WIRE'
            packArea.name = "Pack Area Outline"
    
    #Set dimensions based on user input
    packArea.dimensions = scene.pack_tool.areaX, scene.pack_tool.areaY, scene.pack_tool.areaZ
    #Move packArea, allign bottom left corner to origin
    packArea.location.x = scene.pack_tool.areaX / 2
    packArea.location.y = scene.pack_tool.areaY / 2
    packArea.location.z = scene.pack_tool.areaZ / 2

    #Make unselectable in 3D view and deselect
    packArea.hide_select = True
    bpy.ops.object.select_all(action='DESELECT')
    
    #Set visibility based on user setting
    packArea.hide_set(not(scene.pack_tool.showAreaBool))
    
    return

#Create operator, used for button in panel
class UpdatePackArea(bpy.types.Operator):
    """Update Pack Area Outline"""
    bl_idname = "object.update"
    bl_label = "Generate Pack Area"      
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        updatePackArea(self,context)
        return{'FINISHED'}


'''****************************************
INITIALIZE PROPERTIES
****************************************'''
class PackingAddonSettings(PropertyGroup):    
    areaX: FloatProperty(
        name = "X",
        description = "X dimension of packing area",
        default = 5,
        min = 0,
        max = 1e39,
        unit = 'LENGTH',
        update = updatePackArea
        )
    
    areaY: FloatProperty(
        name = "Y",
        description = "Y dimension of packing area",
        default = 5,
        min = 0,
        max = 1e39,
        unit = 'LENGTH',
        update = updatePackArea
        )
        
    areaZ: FloatProperty(
        name = "Z",
        description = "Z dimension of packing area",
        default = 5,
        min = 0,
        max = 1e39,
        unit = 'LENGTH',
        update = updatePackArea
        )
    
    showAreaBool: BoolProperty(
        name = "Show Pack Area",
        description = "Set visibility of packing area outline",
        default = True,
        update = updatePackArea
        )
        
    objectGap: FloatProperty(
        name = "Gap",
        description = "Minimum gap between packed objects",
        default = 0.1,
        min = 0.001, #A gap of 0 causes a crash
        max = 1e39, 
        unit = 'LENGTH',
        )
    
    allowRotation: BoolProperty(
        name = "Allow Object Rotation",
        description = "Set whether objects can be rotated while packing",
        default = True,
        update = updatePackArea
        )


'''****************************************
3D PACK HELPER FUNCTIONS
****************************************'''

class ListWrapper:
    def __init__(self, list):
        self.list = list

def retDimY(obj):
    return obj.dimensions.y

def retMaxZ(obj):
    return obj.location.z + obj.dimensions.z/2

#Checks if the bounding box of two objects are colliding
def isColliding(obj1, obj2):
    xBool = (obj1.location.x + obj1.dimensions.x/2 < obj2.location.x - obj2.dimensions.x/2) or (obj1.location.x - obj1.dimensions.x/2 > obj2.location.x + obj2.dimensions.x/2)
    
    yBool = (obj1.location.y + obj1.dimensions.y/2 < obj2.location.y - obj2.dimensions.y/2) or (obj1.location.y - obj1.dimensions.y/2 > obj2.location.y + obj2.dimensions.y/2)
    
    zBool = (obj1.location.z + obj1.dimensions.z/2 < obj2.location.z - obj2.dimensions.z/2) or (obj1.location.z - obj1.dimensions.z/2 > obj2.location.z + obj2.dimensions.z/2)
    
    return not (xBool or yBool or zBool)

#Checks that bounding boxes of objects are separated by gap
def hasGap(obj1, obj2, gap):
    gap = gap*0.99
    
    obj1X = [obj1.location.x - obj1.dimensions.x/2, obj1.location.x + obj1.dimensions.x/2]
    obj1Y = [obj1.location.y - obj1.dimensions.y/2, obj1.location.y + obj1.dimensions.y/2]
    obj1Z = [obj1.location.z - obj1.dimensions.z/2, obj1.location.z + obj1.dimensions.z/2]
    
    obj2X = [obj2.location.x - obj2.dimensions.x/2, obj2.location.x + obj2.dimensions.x/2]
    obj2Y = [obj2.location.y - obj2.dimensions.y/2, obj2.location.y + obj2.dimensions.y/2]
    obj2Z = [obj2.location.z - obj2.dimensions.z/2, obj2.location.z + obj2.dimensions.z/2]
    
    xBool = not((obj1X[1] > obj2X[0]) and (obj2X[1] > obj1X[0])) and (abs(obj1X[1] - obj2X[0]) >= gap) and (abs(obj2X[1] - obj1X[0]) >= gap)
    
    yBool = not((obj1Y[1] > obj2Y[0]) and (obj2Y[1] > obj1Y[0])) and (abs(obj1Y[1] - obj2Y[0]) >= gap) and (abs(obj2Y[1] - obj1Y[0]) >= gap)
    
    zBool = not((obj1Z[1] > obj2Z[0]) and (obj2Z[1] > obj1Z[0])) and (abs(obj1Z[1] - obj2Z[0]) >= gap) and (abs(obj2Z[1] - obj1Z[0]) >= gap)
            
    return xBool or yBool or zBool

#Checks if checkingObj is colliding with any object in objList
#returns True when it detects collision or no gap
def checkCollisionAndGap(checkingObj, objList, gap):
    for obj in objList:
        
        if isColliding(checkingObj, obj):
            return True
        
        elif not(hasGap(checkingObj, obj, gap)):
            return True
        
    return False

#orients objects so Y > X > Z using 90 degree rotations
def orientObjects(objectList):
    for obj in objectList:
        
        if obj.dimensions.x > obj.dimensions.z > obj.dimensions.y:
            obj.rotation_euler.x = radians(90)
            obj.rotation_euler.z = radians(90)
            
        elif obj.dimensions.x > obj.dimensions.y > obj.dimensions.z:
            obj.rotation_euler.z = radians(90)

        elif obj.dimensions.z > obj.dimensions.y > obj.dimensions.x:
            obj.rotation_euler.x = radians(90)
            obj.rotation_euler.y = radians(90)

        elif obj.dimensions.z > obj.dimensions.x > obj.dimensions.y:
            obj.rotation_euler.x = radians(90)

        
        elif obj.dimensions.y > obj.dimensions.z > obj.dimensions.x:
            obj.rotation_euler.y = radians(90)
        
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


'''****************************************
3D PACKING FUNCTIONS
****************************************'''

def XPack(startCoords, maxCoords, unplacedListWrapper, gap, checkCollisionsBool, checkCollisionSet = set()):
    currX = startCoords[0]
    placedRowSet = set() #used to quickly subtract placed items from unplaced list
    placedRowList = [] #used in XYPack to place more objects in row
    rowMaxY = rowMaxZ = 0

    #Place objects starting from min X coord to max X coord (left to right)
    for obj in unplacedListWrapper.list:
        
        fitBool = False
        
        #Check if object is within x and y bounds of packing space when placed
        #Check current orientation
        if (currX + obj.dimensions.x) < maxCoords[0] and (startCoords[1] + obj.dimensions.y) <= maxCoords[1] and (startCoords[2] + obj.dimensions.z) <= maxCoords[2]:
            fitBool = True
            
            
            #Save object's current location
            oldLocation = [obj.location.x, obj.location.y, obj.location.z]
            
            #Place object in potential spot
            obj.location.x = currX + obj.dimensions.x/2
            obj.location.y = startCoords[1] + obj.dimensions.y/2
            obj.location.z = startCoords[2] + obj.dimensions.z/2
            
            #Check collision of first obj placed in row if checkCollisionsBool is set
            #Also check if objects have proper gaps            
            if checkCollisionsBool:
                if checkCollisionAndGap(obj, checkCollisionSet, gap):
                    obj.location.x, obj.location.y, obj.location.z = oldLocation
                    fitBool = False
                else:
                    fitBool = True
            
            
            
        #Check if object fits if rotated 90 degrees on Z (X and Y dimensions switch)
        #Only happens if user allows rotation
        #Added check for fitBool so if check with current orientation fails, it will check object with rotation
        if (not fitBool) and bpy.context.scene.pack_tool.allowRotation and (currX + obj.dimensions.y) < maxCoords[0] and (startCoords[1] + obj.dimensions.x) <= maxCoords[1] and (startCoords[2] + obj.dimensions.z) <= maxCoords[2]:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            obj.rotation_euler.z = radians(90)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            fitBool = True
            
            
            #Save object's current location
            oldLocation = [obj.location.x, obj.location.y, obj.location.z]
            
            #Place object in potential spot
            obj.location.x = currX + obj.dimensions.x/2
            obj.location.y = startCoords[1] + obj.dimensions.y/2
            obj.location.z = startCoords[2] + obj.dimensions.z/2
            
            #Check collision of first obj placed in row if checkCollisionsBool is set
            #Also check if objects have proper gaps            
            if checkCollisionsBool:
                if checkCollisionAndGap(obj, checkCollisionSet, gap):
                    obj.location.x, obj.location.y, obj.location.z = oldLocation
                    fitBool = False
                else:
                    fitBool = True
        
        
        if fitBool:
            #Update current X location and add gap between objects
            currX += (obj.dimensions.x + gap)

            #Add object to placed set & list
            placedRowSet.add(obj)
            placedRowList.append(obj)

            #Update max dimensions
            rowMaxY = max(rowMaxY, obj.dimensions.y)
            rowMaxZ = max(rowMaxZ, obj.dimensions.z)

            if currX > maxCoords[0]:
                break

        else:
            #Continue if object didn't fit
            continue
        
    #Remove placed objects from unplaced list and sort
    tempUnplacedSet = set(unplacedListWrapper.list)
    tempUnplacedSet.difference_update(placedRowSet)
    unplacedListWrapper.list = list(tempUnplacedSet)
    unplacedListWrapper.list.sort(reverse=True, key=retDimY)
        
    return placedRowList, placedRowSet, rowMaxY, rowMaxZ


def XYPack(startCoords, maxCoords, unplacedListWrapper, gap, checkCollisionsBool, checkCollisionSet = set()):
    currY = startCoords[1]
    layerMaxZ = 0
    placedLayerSet = set()

    #Use X Pack to fill rows
    while True:
        #Run XPack
        placedRowList, placedRowSet, rowMaxY , rowMaxZ = XPack([startCoords[0], currY, startCoords[2]], maxCoords, unplacedListWrapper, gap, checkCollisionsBool, checkCollisionSet)

        #Check if row was placed
        if placedRowList:
            #Update currY to next row
            currY += rowMaxY + gap

            #Update maxZ
            layerMaxZ = max(layerMaxZ, rowMaxZ)
            
            #Update placed set
            placedLayerSet = placedLayerSet.union(placedRowSet)
            
            
            #attempt to place more in row
            #try to xpack above (on Y) of placed objects
            
            #objects to check collision with
            rowCheckCollisionSet = set()
            rowCheckCollisionSet = rowCheckCollisionSet.union(placedRowSet)
            #used to update new placed objects to try placing objects on
            newPlacedRowList = []
            
            while True:
                for placedObject in placedRowList:
                    #Set start coords to be above (on Y) of placed object, alligned on left of object (-X)
                    newStartCoords = [placedObject.location.x - placedObject.dimensions.x/2, placedObject.location.y + placedObject.dimensions.y/2 + gap, startCoords[2]]
                    #Set new max coords, currY was shifted up (on Y) to the next row + gap
                    newMaxCoords = [maxCoords[0], currY - gap, startCoords[2] + layerMaxZ]
                    
                    #Run XPack, checking for collisions with all placed objects in the layer
                    #Check for collisions with row set and with checkCollisionSet argument passed in
                    placedRowList2, placedRowSet2, temp, temp = XPack(newStartCoords, newMaxCoords, unplacedListWrapper, gap, True, checkCollisionSet.union(rowCheckCollisionSet))
                    
                    #Add placed objects to placed layer set
                    placedLayerSet = placedLayerSet.union(placedRowSet2)
                    #Add newly placed objects to check collision
                    rowCheckCollisionSet = rowCheckCollisionSet.union(placedRowSet2)
                    
                    #Keep track of newly placed objects
                    if placedRowList2:
                        newPlacedRowList = newPlacedRowList + placedRowList2
                
                #Update placedRowList to be newly placed objects
                if newPlacedRowList:
                    placedRowList.clear()
                    for i in newPlacedRowList:
                        placedRowList.append(i)
                    newPlacedRowList.clear()
                else:
                    #Finish if nothing was placed
                    break
            
        else:
            #Finish if nothing was placed
            break

    return placedLayerSet, layerMaxZ


def XYZPack(startCoords, maxCoords, unplacedListWrapper, gap):
    currZ = startCoords[2]
    placedAreaSet = set() #stores all objects placed in current area
    placedAreasList = [] #list of sets, each set is a packed area and holds all objects placed in the area

    #Use XY Pack to fill layers
    while True:
        placedLayerSet, layerMaxZ = XYPack([startCoords[0], startCoords[1], currZ], maxCoords, unplacedListWrapper, gap, False)

        #Check if layer was placed
        if placedLayerSet:
            #Update currZ
            currZ += layerMaxZ + gap
            
            #attempt to place more in layer
            #try to XYpack above (on Z) of placed objects
            #start on objects lower down (on Z)
            layerCheckCollisionSet = placedLayerSet
            placedLayerList = list(placedLayerSet)
            
            #Attempt to pack more on top (on the Z) of placed objects
            while True:
                newPlacedLayerList = [] #newly placed objects
                checkedPlacedObjects = set() #placed objects that script attempted to place an object on
                placedLayerList.sort(key=retMaxZ) #sort list by top Z coordinate
                
                for placedObject in placedLayerList:
                    #Set start coords to be on lower left corner (least X and Y) and on top (on Z) of placed object
                    newStartCoords = [placedObject.location.x - placedObject.dimensions.x/2, placedObject.location.y - placedObject.dimensions.y/2, placedObject.location.z + placedObject.dimensions.z/2 + gap]
                    #Set max coords, currZ was shifted up to next layer + gap
                    newMaxCoords = [maxCoords[0], maxCoords[1], currZ - gap]
                    
                    #Run XY pack, checking for collisions
                    placedLayerSet2 , temp = XYPack(newStartCoords, newMaxCoords, unplacedListWrapper, gap, True, layerCheckCollisionSet)
                    
                    #Add placed items to check collisions
                    layerCheckCollisionSet = layerCheckCollisionSet.union(placedLayerSet2)
                    #Record that object has been checked
                    checkedPlacedObjects.add(placedObject)
                    
                    #If objects were placed, record objects and break
                    if placedLayerSet2:
                        newPlacedLayerList = list(placedLayerSet2)
                        break
                
                #If objects were placed
                if newPlacedLayerList:
                    #Remove checked objects
                    placedLayerList = list(set(placedLayerList) - checkedPlacedObjects)
                    #Add newly placed objects
                    placedLayerList = placedLayerList + newPlacedLayerList
                    newPlacedLayerList.clear()
                else:
                    #Finish if nothing was placed
                    break
            
            #Add placed objects to placedAreaSet
            #layerCheckCollisionSet records all placed objects in layer
            placedAreaSet = placedAreaSet.union(layerCheckCollisionSet)
        
        
        #No objects were placed
        else:
            #Check if there are unplaced objects
            #AND if objects were previously placed to avoid infinite loop
            if len(unplacedListWrapper.list) != 0 and len(placedAreaSet) != 0:
                
                #Add placedAreaSet to placedAreasList
                tempSet = set(placedAreaSet)
                placedAreasList.append(tempSet)
                
                #Move all objects in placed areas on X a specific interval
                for areaSet in placedAreasList:
                    for object in areaSet:
                        object.location.x = object.location.x + (maxCoords[0] * 1.5)
                
                #Reset pack area
                placedAreaSet.clear()
                currZ = startCoords[2]
                
            else:
                break


'''****************************************
3D PACK MAIN FUNCTION
****************************************'''
class PackObjects(bpy.types.Operator):
    """Pack selected objects into pack area"""
    bl_idname = "object.pack"
    bl_label = "Pack Selected Objects"      
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pack_tool = context.scene.pack_tool
        gap = context.scene.pack_tool.objectGap
        
        #Set origin of selected objectsto center of bounding box
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        
        #Put unplaced objects into list wrapper class
        unplacedListWrapper = ListWrapper(context.selected_objects)
        
        #Orient objects if user allows rotation
        if pack_tool.allowRotation:
            orientObjects(unplacedListWrapper.list)
            
        #Sort by Y largest to smallest
        unplacedListWrapper.list.sort(reverse=True, key=retDimY)

        #Run XYZ pack
        XYZPack([0,0,0], [pack_tool.areaX, pack_tool.areaY, pack_tool.areaZ], unplacedListWrapper, pack_tool.objectGap)
        
        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


'''****************************************
SIDEBAR PANEL
****************************************'''
#Adding panel to toolshelf
class PACK_PT_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "3D Pack"
    bl_context = "objectmode"
    bl_label = "3D Pack Panel"

    def draw(self, context):
        layout = self.layout
        
        layout.operator("object.update")
        layout.prop(context.scene.pack_tool, "showAreaBool")
        
        layout.separator()
        
        column = layout.column(align = True)
        
        column.label(text = "Pack Area Dimensions:")
        column.prop(context.scene.pack_tool, "areaX")
        column.prop(context.scene.pack_tool, "areaY")
        column.prop(context.scene.pack_tool, "areaZ")
        
        column.separator()
        column.separator()
        column.label(text = "Gap Between Objects:")
        column.prop(context.scene.pack_tool, "objectGap")
        
        column.separator()
        column.separator()
        column.prop(context.scene.pack_tool, "allowRotation")
        
        layout.separator()
        layout.operator("object.pack")


'''****************************************
REGISTER/UNREGISTER
****************************************'''
def register():
    bpy.utils.register_class(PackObjects)
    bpy.utils.register_class(UpdatePackArea)
    bpy.utils.register_class(PACK_PT_Panel)
    
    bpy.utils.register_class(PackingAddonSettings)
    bpy.types.Scene.pack_tool = PointerProperty(type=PackingAddonSettings)
    

def unregister():    
    bpy.utils.unregister_class(PackObjects)
    bpy.utils.unregister_class(UpdatePackArea)
    bpy.utils.unregister_class(PACK_PT_Panel)
    
    bpy.utils.unregister_class(PackingAddonSettings)
    del bpy.types.Scene.pack_tool
    
    #delete pack area outline
    global packArea
    #Check if packArea is a valid object, if not it was probably deleted
    try:
        packArea.name
    except:
        packArea = None
    #If the pack area was generated, delete it
    if packArea != None:
        #switch to object mode, needed to use deselect operator
        if bpy.context.mode!="OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')
        packArea.hide_select = False
        packArea.select_set(True)
        bpy.ops.object.delete()
        
        packArea = None