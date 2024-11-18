Provides batch processing of image sets, generating composites of said sets. 

* Uses the alpha channel to determine crop boundaries.
* Builds the composite by placing images along the x-axis.
* Centers images along the y-axis. 
* Option to apply a caption derived from the filename to composites. 
* Does not change images in the raw directory. 

Sets are separating by appending tags to the end of the filename. See images in raw for an example of this, noting that more sets could be added (i.e., umbrella Front.png, umbrella 3Q.png, etc) and processed in the same batch.

Note that tags are matched in the order of the list they're contained in. As such, "3Q Above" can be misidentified as "Above", if the "Above" is placed ahead of "3Q Above" in the `tags` list. This can be entirely circumvented by using unique tags, such as camera1, camera2, etc.