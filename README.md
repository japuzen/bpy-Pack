# 3D Pack - Blender Addon
![Image of Full Pack](images/Addon%20Doc%20-%20Full%20Pack.png)

## Installation
1. Right click [**this link**](https://raw.githubusercontent.com/japuzen/bpy-pack/master/PackingAddon.py) and click *Save Link As* to download the Python file.
2. In Blender, go to *Edit > Preferences*.

![Image of Full Pack](images/Addon%20Doc%20-%20Edit>Preferences.png)

3. In *Addons* click *Install* and find the *PackingAddon.py* file.

![Image of Full Pack](images/Addon%20Doc%20-%20Addon%20Install.png)

4. Click the checkbox to the left of the addon to enable it.

## Usage
<img align="right" src="images/Addon%20Doc%20-%20Pack%20Panel%20Image.png">

1. Locate the ***3D Pack Panel*** in the Sidebar.
    - Press 'N' while your mouse is in the 3D Viewport to open/close the Sidebar.
2. Click ***Generate Pack Area*** to generate the Pack Area Outline in the 3D Viewport.
3. Set the ***Pack Area Dimensions***.
4. Set the ***Gap*** between objects.
5. Set the ***Allow Object Rotation*** parameter.
    - Enabling it will allow the rotation of objects to achieve a tighter pack. Disabling it will preserve the objects’ original orientation.
6. Select all the objects to pack.
7. Click ***Pack Selected Objects***.
<br><br><br>

&nbsp;&nbsp;&nbsp;&nbsp;Fully packed areas will be placed next to the Pack Area Outline in the +X direction. Objects that do not fit in the Pack Area Outline will stay in their original positions.


![Image of Packing Results](images/Addon%20Doc%20-%20Result%20Image.png)
>Objects that were too large to pack on the left, Pack Area Outline in the center, packed objects on the right

## Info
&nbsp;&nbsp;&nbsp;&nbsp;The 3D Pack add-on provides tools to pack objects into a defined 3-dimensional area in Blender. Users can set the size of the area and the minimum gap between packed objects. Users can also specify whether their objects can be rotated to try to achieve a tighter pack.

&nbsp;&nbsp;&nbsp;&nbsp;The script uses the bounding box of an object when orienting and placing it, rather than the object’s geometry. This means that empty spaces within an object’s bounding box won’t be utilized, so objects may not be packed as tightly as possible. On the upside, using bounding boxes allows the script to pack objects fairly quickly. Also, high poly count objects and low poly count objects are packed with around the same speed.

&nbsp;&nbsp;&nbsp;&nbsp;The objects in the images come from this [Thingiverse post](https://www.thingiverse.com/thing:239105)

### Minimizing Bounding Box Volume
&nbsp;&nbsp;&nbsp;&nbsp;Since the 3D Pack add-on uses the bounding box of objects, it would be a good idea to minimize the volume of objects' bounding boxes before packing. This is an optional step, but it will provide the best packing results. Changing an object’s bounding box can be done manually in Blender by rotating the object and then applying its rotation. You can display an object’s bounding box by selecting an object, going to the *Properties* panel and checking *Object > Viewport Display > Bounds*.

&nbsp;&nbsp;&nbsp;&nbsp;**To automatically minimize an object’s bounding box volume, you can use this [Blender add-on](https://github.com/japuzen/bpy-minboundbox)**

<img src="images/Addon%20Doc%20-%20Bound%20Box%20Difference%20Image.png" height="75%" width="75%" align="center"></img>
>The same object with different bounding boxes, with its minimum volume bounding box on the right.

### Setting Up Units
&nbsp;&nbsp;&nbsp;&nbsp;The units for the *Pack Area Dimensions* and *Gap* correspond to the current Scene’s units. You can set this in the *Properties* panel under *Scene > Units*.
    
### Removing the Pack Area Outline
&nbsp;&nbsp;&nbsp;&nbsp;You can hide the Pack Area Outline in the 3D Viewport by toggling the ***Show Pack Area parameter*** in the 3D Pack Panel. You can also hide the Pack Area Outline by toggling its visibility in the Outliner, but changing its dimensions will make it visible again. 

&nbsp;&nbsp;&nbsp;&nbsp;Upon disabling the add-on, the Pack Area Outline should be automatically deleted.  If it was not deleted, you can manually delete it by right-clicking on the Pack Area Outline object in the Outliner.
