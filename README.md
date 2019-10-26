# data_management
Scripts for Data Collection, Annotation and Processing

## Notes:
as you sort through data make note of things that call your attention that could be useful and suggest meta data that could be collected

### real_w_tensors_2500/Falling_all/
* Allistair's videos seem to be "faster" which imply they were captured at a slower frame rate. Could we use DSP to      interpolate?
* Some videos might not generate full joint mappings because certain bodyparts get occluded
* Meta Data Suggestions:
    * % of joints generated per frame 

### real_w_tensors_2500/Still_On_Bed_all/
* There are some files that do not have tensor data along with them.
   * All of them are from Ji's Data. It's easily identifiable by their file type (.mp4)
 
### real_w_tensors_2500
* Hard time distinguishing between rolling bed & still on bed. 
* Review data to draw a clear line between these actions and reclassify them
* Data from Ji's room is more zoomed in. Frame covers the length of the bed
