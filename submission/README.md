# COM31006 Assignment
This project contains the source code for the COM31006 assignment. It is a Flask web application called Stegasaurus that contains a number of tools for image-to-image steganography and watermarking.

## Setup
A custom conda environment is included in the file `environment.yml`, and the environment is called `stegasaurus`.

```
conda create -f environment.yml
conda activate stegasaurus
```

## Running the code
The project runs using Flask. Activate the conda environment, then run the app.

```
conda activate stegasaurus
cd ./app/
flask run
```

Then visit http://127.0.0.1:5000 to access the application.

## Images

A set of testing images can be found in the `images` folder. This contains the unmodified image `original.png`, a watermark `watermark.png`, the image embedded with the watermark `original_watermarked.png`, and a set of images with various tampering techniques applied `cropped.png`, `resize.png`, `rotated.png`, `squish.png`, and `tampered.png`. `tampered.png` is an image made of half of the watermarked image overlayed with the original, so the tampering is imperceptible to the human eye but will be detected by the application. The application works with any image you want, as long as it is not too large.

## Video demo
A short video demo of the application: https://youtu.be/MhpaLAekoRo

## Acknowledgements
Author: Lucy Lau \
Images from my personal camera. \
Icons from [Figma Simple Design System.](https://www.figma.com/community/file/1380235722331273046) \
HTML styling using [Bootstrap.](https://getbootstrap.com/)