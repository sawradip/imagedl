This small project is for downloading google tons of google images, with a few clicks.
Speciality of this project is, you can search google with both
1. Text
2. Images

Yes! Reverse image search(searching by an image) is also included here. So, lets see how this works.
 First clone this package in apropriate folder using the terminal, 

 ```git clone https://github.com/sawradip/imagedl.git ```

Open that folder in your IDE.Then install the dependencies.

```pip install -r requirements.txt```

After installation, you can open the script `try.py`.This is the simplest way to use those modules for now.

Now uncomment either of the block.
block 1 downloads the image by text search, and block 2 downloads searching by image.

### Block1
Here you can provide the text `search_text` that you want to search , number of images `n_images` to download, and the name of the folder `save_folder` you want the images to be in.

### Block 2
Here you can provide path of an image in  `search_image` that you want similar images of, number of images `n_images` to download, and the name of the folder `save_folder` you want the images to be in.

## Additional Features

If you have checked, you should have found information (Captions, width, height) of all the images, in `img_info.txt` located inside the newly created folder.
* If you want to see what is actually hapeing withing the program, you can make `headless = False` .  
* If you want the image informations in csv file , you just have to add an additional argument `to_csv = True` , with the `headless` argument.
* If you want to get the download links of the images in the terminal,you can add another argument `show_links= True`.

For now, I am not sure if it would work in colab, or other jupyter notebook. I would  prefer, you run it with an IDE , like VSCode.












