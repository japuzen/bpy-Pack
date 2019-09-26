# 3D Pack - Blender Addon
![Image of Full Pack](images/Addon%20Doc%20-%20Full%20Pack.png)
## Usage
<img align="left" src="images/Addon%20Doc%20-%20Pack%20Panel%20Image.png">

1. Install and enable the add-on.
2. Locate the ***3D Pack Panel*** in the Sidebar.
    - Press 'N' while your mouse is in the 3D Viewport to open/close the Sidebar.
3. Click ***Generate Pack Area*** to generate the Pack Area Outline in the 3D Viewport.
4. Set the ***Pack Area Dimensions***.
5. Set the ***Gap*** between objects.
6. Set the ***Allow Object Rotation*** parameter.
    - Enabling it will allow the rotation of objects to achieve a tighter pack. Disabling it will preserve the objects’ original orientation.
7. Select all the objects to pack.
8. Click ***Pack Selected Objects***.

&nbsp;&nbsp;&nbsp;&nbsp;Fully packed areas will be placed next to the Pack Area Outline in the +X direction. Objects that do not fit in the Pack Area Outline will stay in their original positions.
![Image of Packing Results](images/Addon%20Doc%20-%20Result%20Image.png)

## Info
&nbsp;&nbsp;&nbsp;&nbsp;The 3D Pack add-on provides tools to pack objects into a defined 3-dimensional area in Blender. Users can set the size of the area and the minimum gap between packed objects. Users can also specify whether their objects can be rotated to try to achieve a tighter pack.

&nbsp;&nbsp;&nbsp;&nbsp;The script uses the bounding box of an object when orienting and placing it, rather than the object’s geometry. This means that empty spaces within an object’s bounding box won’t be utilized, so objects may not be packed as tightly as possible. On the upside, using bounding boxes allows the script to pack objects fairly quickly. Also, high poly count objects and low poly count objects are packed with around the same speed.

&nbsp;&nbsp;&nbsp;&nbsp;The objects shown in the images come from the following Thingiverse post: https://www.thingiverse.com/thing:239105

### Minimizing Bounding Boxes
&nbsp;&nbsp;&nbsp;&nbsp;Since the 3D Pack add-on uses the bounding box of objects, it would be a good idea to minimize the bounding box of objects before packing. This is an optional step, but it will provide the best packing results. Changing an object’s bounding box can be done manually in Blender by rotating the object and then applying its rotation. You can display an object’s bounding box by selecting an object, going to the *Properties* panel and checking *Object > Viewport Display > Bounds*.
    
&nbsp;&nbsp;&nbsp;&nbsp;To automatically minimize an object’s bounding box, you can use the following Blender add-on: {Add link to bounding box add-on}
    
### Setting Up Units
&nbsp;&nbsp;&nbsp;&nbsp;The units for the *Pack Area Dimensions* and *Gap* correspond to the current Scene’s units. You can set this in the *Properties* panel under *Scene > Units*.
    
### Removing the Pack Area Outline
&nbsp;&nbsp;&nbsp;&nbsp;You can hide the Pack Area Outline in the 3D Viewport by toggling the ***Show Pack Area parameter*** in the 3D Pack Panel. You can also hide the Pack Area Outline by toggling its visibility in the Outliner, but changing its dimensions will make it visible again. 

&nbsp;&nbsp;&nbsp;&nbsp;Upon disabling the add-on, the Pack Area Outline should be automatically deleted.  If it was not deleted, you can manually delete it by right-clicking on the Pack Area Outline object in the Outliner.
