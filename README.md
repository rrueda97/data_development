# data_management
Scripts for Data Collection, Annotation and Processing

## DataSets Summary:
* real_w_joints (n = 21, 750)
    * Falling (n = 1,520)
        * RRuedaLiving w others (03/2019)       (n = 217)
        * RRuedaLiving w RRueda (04/2019)       (n = 88)
        * RRuedaBed w VBaena (07/2019)          (n = 399)
        * ATamGarage w ATam (07/2019)           (n = 252)
        * ATwomblyMaster w ATwombly (08/2019)   (n = 564)
        
    * Rolling_Bed (n = 4233)
        * JLeeBed w JLee, RRueda (04/2019)          (n = 481) 
        * RRuedaBed w RRueda,JLee,DBerry (06/2019)  (n = 979)
        * RRuedaBed w VBaena (07/2019)              (n = 818)
        * ATamGarage w ATam (07/2019)               (n = 594)
        * ATwomblyMaster w ATwombly (08/2019)       (n = 791)
        * NMousaBed w MMercurio (08/2019)           (n = 570)
        
    * Rolling_Ground (n = 2,057)
        * RRuedaBed w VBaena (07/2019)          (n = 402)
        * ATamGarage w ATam (07/2019)           (n = 274)
        * ATwomblyMaster w ATwombly (08/2019)   (n = 763)
        * NMousaBed w MMercurio (08/2019)       (n = 618)
        
    * Sitting_Up (n = 3,820)
        * RRuedaBed w JLee, RRueda (04/2019)     (n = 600)
        * JLeeBed w JLee (04/2019)                (n = 350)
        * RRuedaBed w VBaena (07/2019)          (n = 804)
        * ATamGarage w ATam (07/2019)           (n = 764)
        * ATwomblyMaster w ATwombly (08/2019)   (n = 767)
        * NMousaBed w MMercurio (08/2019)       (n = 535)

    * Standing (n = 4713)
        * RRuedaLiving w others (03/2019)       (n = 3,585)
        * RRuedaBed w VBaena (07/2019)          (n = 415)
        * JLeeBed w JLee (04/2019)              (n = 39)
        * ATamGarage w ATam (07/2019)           (n = 126)
        * ATwomblyMaster w ATwombly (08/2019)   (n = 548)
        
    * Still_On_Bed (n = 3,292)
        * JLeeBed w JLee, RRueda (04/2019)          (n = 63)
        * RRuedaBed w RRueda,JLee,DBerry (06/2019)  (n = 620)
        * RRuedaBed w VBaena (07/2019)              (n = 829)
        * ATamGarage w ATam (07/2019)               (n = 569)
        * ATwomblyMaster w ATwombly (08/2019)       (n = 794)
        * NMousaBed w MMercurio (08/2019)           (n = 417)

    * Still_On_Ground (n = 2,115)
        * RRuedaLiving w others (03/2019)           (n = 461)
        * RRuedaLiving w RRueda (04/2019)           (n = 51)
        * RRuedaBed w VBaena (07/2019)              (n = 411)
        * ATamGarage w ATam (07/2019)               (n = 274)
        * ATwomblyMaster w ATwombly (08/2019)       (n = 383)
        * NMousaBed w MMercurio (08/2019)           (n = 535)
        
* liveset_w_joints (n = 1,500)
    * RRuedaBed w RRueda (09-10/2019) 
        * Rolling_Bed   (n = 400)
        * Sitting_Up    (n = 400)
        * Standing      (n = 300)
        * Still_On_Bed  (n = 400)
        
* NMousaBed_processed_fisheye (n = 2,851)
    * processed fisheye, no joints
    * NMousaBed w MMercurio (08/2019) 
        * Rolling_Bed       (n = 595)
        * Rolling_Ground    (n = 633)
        * Sitting_Up        (n = 580)
        * Still_On_Bed      (n = 479)
        * Still_On_Ground   (n = 564)
* NMousaBed_fisheye (n = 3,387)
    * fisheye distortion, no joints
    * NMousaBed w MMercurio (08/2019) 
        * Falling           (n = 348)
        * Standing          (n = 404)
        * Rolling_Bed       (n = 767)
        * Rolling_Ground    (n = 482)
        * Sitting_Up        (n = 214)
        * Still_On_Bed      (n = 619)
        * Still_On_Ground   (n = 553)

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

### data_sort.py
* Because data is all over the place, we're going to categorize most of the data to have precise categories
* Variance: How each action is seen typically. 
   * Low = Usual. (ex. a fall due to a collapse)
   * Medium = Slight off of action but still usual. (ex. a fall due to a collapse but still conscious)
   * High = Very unusual activity (ex. a fall but someone stops it with their hands)
* Zoom: 
   * Low: person is completely on frame, but way smaller
   * Medium: Person is completely on frame
   * High: Person is on frame, but parts of head, feet, or legs are slightly on edges of frame
* CamID: Think about the person's perspective of their camera and their roomset
   * CamRight: Alex's Garage (the Side)
   * CamFront: Alex's Garage (camera set on washing machine)
   * CamBack: Alex's Garage (camera set on the door)
  
* Position: How the person is located away from their center of the frame.

* splitNum: Determined if the datasets are formed from a single cut (one long 30 sec video of a fall/ sittingup) or are individual actions (like standing)
* roomInfo: How many objects are present in the surroundings aside from the bed itself.
