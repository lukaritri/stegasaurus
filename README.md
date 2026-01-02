# Stegasaurus
This project contains the source code for computer vision assignment. It is a Flask web application called Stegasaurus that contains a number of tools for image-to-image steganography and watermarking.

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

## Video demo
A short video demo of the application: https://youtu.be/MhpaLAekoRo

## Acknowledgements
Author: Lucy Lau \
Images from my personal camera. \
Icons from [Figma Simple Design System.](https://www.figma.com/community/file/1380235722331273046) \
HTML styling using [Bootstrap.](https://getbootstrap.com/)