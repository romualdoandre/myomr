#myomr
=====

An [Optical Mark Recognizer Software](https://en.wikipedia.org/wiki/Optical_mark_recognition "OMR") made by me using OpenCV and Python.

This software has two parts: a GUI configurer and a CLI OMR.

## Requirements:
* Python 2.7.x
* OpenCV 2.4.x
* Numpy
* PIL and ImageTk
* Tix 

## License:
* [GPL V2](LICENSE)

Preprocessing
-----

You might preprocessing the image to ensure that there is not problems with the sheet image alignment. 

First you might use scripts to ensure the image alignment. Enter the _/omr/src/cropped_ folder and use the *align.py* script as follow:

> python align.py x1 y1 x2 y2 regex

Where *x1* and *y1* is the beginning of the rightest superior mark, *x2* and *y2* is the beginning of the rightest inferior mark and *regex* is a regular expression refering the image files. All the result files will have a *rot_* prefix.

After you might crop the image with the _/omr/src/cropped/crop.py_ script as follow:

> python crop.py x1 y1 x2 y2 regex

Where *x1* and *y1* is the beginning of the rightest superior mark, *x2* and *y2* is the beginning of the rightest inferior mark and *regex* is a regular expression refering the image files. All the result files will have a *crop_* prefix.

GUI configurer tool
-----

Open the configurer tool (folder _/configurer/src/_) using the command line:

> python configurer.py

##Open a background image

Before you start creating a configuration file, now called *application*, it is necessary to define a background image to the canvas. This is necessary for the user to have idea how to define each field. The keyboard shortcut for the command to open the background image is *Ctrl + i* or from the *File* menu, *Open background Image*.

##Creating a new application

When a new *application* is created, all fields already set are deleted and remains only the background image. The keyboard shortcut for the new application command is *Ctrl + n* or from the *File* menu, *New*.

##Save

Applications are saved to disk with the extension .csv (Comma Separated Values) compatible with the OMR. The *application* contains all configured fields. The keyboard shortcut to save an application is *Ctrl + s* or from the *File* menu, *Save*.

##Open

*Applications* are saved to disk with the extension .csv (Comma Separated Values - Comma Separated Values). When opening the *application* file, the fields configured are shown on the screen in the order they were created. An application can only be opened if there is a *background image* set. If there are any previously configured field, it will be deleted and only the fields of the application file will appear. The keyboard shortcut for the command to open the application is *Ctrl + a* or from the *File* menu, *Open*.

##New field

To create a new field for the correction, select the *Field* menu, *New*, click the left mouse button over the background image by selecting the beginning of the field. A dialog for the field configuration. In this dialog set the amount of the field cells (1 to 10), the field direction (horizontal or vertical), the field type (character or numeral), if the field is part of the answer sheet identifier, the dimensions of each cell of the field pixels and the spacing between each cell. If you want to quit the process by clicking the Cancel button. To save the field, click OK. After the selection of the field will be updated to the specified dimensions. To field an identifier that will be close to the field will be assigned.

##Moving a field

To select a field and move it, use the mouse middle button or select the *Field* menu , *Move* and use the left button. Click on the boundary line of the field, it will change to the color red, indicating it has been selected. After selection, you can hold the center button and move the field to another area, the release operation is finished.

##Delete a field

Select the field using the mouse middle button or select the *Field* menu, *Move* and use the left button. Once selected, delete the field using the *Delete* key.

##Changing a field

Select the field using the right click of the mouse. The boundary line of the field will change to blue, indicating that the field is selected. Change the field information in the same way in the field setting operation. If you want to quit the process by clicking the *Cancel* button. To save the field, click *OK*.

Processing
-----

After angle correction and image cropping, processing can occur using the command line in the following format:

> python omr.py -i regex -o output -a config.csv

Where *regex* is a regular expression refering the image files already corrected for processing. *Output* is the file where the responses of each sheet will be saved, one in each row. *Config.csv* is the configuration file generated in __Configurer__. The processed images will be renamed according to the identifier determined in the configuration.
**Attention: Each field is processed in the order in which it appears in the configuration file.**
