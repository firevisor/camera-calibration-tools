# Camera Calibration Tools

Tools to manually mark the cell corners in the module and using those corner coordinates to undistort the modules.
The process of marking the cell corners if very labor-intensive. For example, you will have to make 91 markings for a 
72-cell module (i.e. there are 91 corners for a 72 cell-module).


## To Manually Mark Corners

`python cam_calib.py label -p dir/with/images -d <dimension_of_module>`

* `<dimension_of_module>`: If the module is 72 cells (12 cols, 6 rows), the dimension that has to be provided is "13x7".
Specify the dimension in "`<col+1>`x`<row+1>`" format.

Click corners of every cell and once you are done with the module image, press <Spacebar>.