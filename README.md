# data_management
Scripts for Data Collection, Annotation and Processing

## DataSets Summary:
* real_w_joints
    * Falling
        * RRuedaLiving w others (03/2019)
        * RRuedaLiving w RRueda (04/2019)
        * RRuedaBed w VBaena (07/2019)
        * ATamGarage w ATam (07/2019)
        * ATwomblyMaster w ATwombly (08/2019)
    * Rolling_Bed
        * JLeeBed w JLee, RRueda (04/2019)
        * RRuedaBed w RRueda,JLee,DBerry (06/2019)
        * RRuedaBed w VBaena (07/2019)
        * ATamGarage w ATam (07/2019)
        * ATwomblyMaster w ATwombly (08/2019)
        * NMousaBed w MMercurio (08/2019)
        * unlabled data
    * Rolling_Ground
        * RRuedaBed w VBaena (07/2019)
        * ATamGarage w ATam (07/2019)
        * ATwomblyMaster w ATwombly (08/2019)
        * NMousaBed w MMercurio (08/2019)
    * Sitting_Up
        * JLeeBed w JLee, RRueda (04/2019)
        * RRuedaBed w VBaena (07/2019)
        * ATamGarage w ATam (07/2019)
        * ATwomblyMaster w ATwombly (08/2019)
        * NMousaBed w MMercurio (08/2019)
        * unlabeled data
    * Standing
        * RRuedaLiving w others (03/2019)
        * JLeeBed w JLee (04/2019)
        * RRuedaBed w VBaena (07/2019)
        * ATamGarage w ATam (07/2019)
        * ATwomblyMaster w ATwombly (08/2019)
    * Still_On_Bed
        * JLeeBed w JLee, RRueda (04/2019)
        * RRuedaBed w RRueda,JLee,DBerry (06/2019)
        * RRuedaBed w VBaena (07/2019)
        * ATamGarage w ATam (07/2019)
        * ATwomblyMaster w ATwombly (08/2019)
        * NMousaBed w MMercurio (08/2019)
        * unlabeled data
    * Still_On_Ground
        * RRuedaLiving w others (03/2019)
        * RRuedaLiving w RRueda (04/2019)
        * RRuedaBed w VBaena (07/2019)
        * ATamGarage w ATam (07/2019)
        * ATwomblyMaster w ATwombly (08/2019)
        * NMousaBed w MMercurio (08/2019)

* liveset_w_joints
    * RRuedaBed w RRueda (09-10/2019) 
        * Rolling_Bed
        * Sitting_Up
        * Standing
        * Still_On_Bed
* Test_Set_fisheye_undistorted
    * collected in Tandem with Test_Set_Original
    * processed fisheye 
* test_8_27_19
    * NMousaBed w MMercurio 
        * 08/2019 All Actions
    * Fisheye Distortion


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
