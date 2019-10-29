# data_management
Scripts for Data Collection, Annotation and Processing

## DataSets and what they inlcude:
* real_w_tensors_all
    * JLeeBed w JLee                 (04/2019) BedActions+Standing
    * RRuedaLiving w RRueda          (04/2019) Falling
    * RRuedaBed w RRueda+JLee+DBerry (06/2019) BedActions
    * RRuedaBed w VBaena             (07/2019) AllActions
    * ATamGarage w ATam              (07/2019) AllActions
    * AtwomblyMaster w Atwombly      (08/2019) AllActions

* older_data
    * RRuedaLiving w RRueda+JiLee+RBhardwaj+JAlvarenga (04??/2019) GroundActions+Standing+Falling
* test_set
    * NMousaBed w MMercurio (8/2019) AllActions
* liveset
    * RRuedaBed w RRueda (09-10/2019) BedActions+Standing


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
