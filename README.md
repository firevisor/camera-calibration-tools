# Camera Calibration Tools

Tools to manually mark the cell corners in the module and using those corner coordinates to undistort the modules.
The process of marking the cell corners if very labor-intensive. For example, you will have to make 91 markings for a 
72-cell module (i.e. there are 91 corners for a 72 cell-module).


## To Manually Mark Corners

`python cam_calib.py label -p dir/with/images -d <dimension_of_module>`

* `<dimension_of_module>`: If the module is 72 cells (12 cols, 6 rows), the dimension that has to be provided is "13x7".
Specify the dimension in "`<col+1>`x`<row+1>`" format.

Click corners of every cell and once you are done with the module image, press <Spacebar>.

## Workflow

A typical workflow will contain the following:

  * Put all the images into one directory 
  * Run the label tool, which will open up a window 
  * Click the corners from left to right and top to bottom (Press "backspace" to undo)
  * Pass the resulting CSV file into undistort

The available options for label are as follows:

    -p - The directory of images to label (e.g. images)
    -f - The format of the images (e.g. jpg, png)
    -o - The output file (e.g. labels.csv)
    -d - The dimensions of the board (e.g. 8x8)

The available options for undistort are as follows:

    -p - The directory of images to label (e.g. images)
    -f - The format of the images (e.g. jpg, png)
    -l - The file containing the labels (e.g. labels.csv)
    -d - The dimensions of the board (e.g. 8x8)
    -r - Whether to crop or letterbox the undistorted images

"Crop" means that the extra pixels (due to the curves) will be discarded, while "Letterbox" means that black pixels will be inserted.