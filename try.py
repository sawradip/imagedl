from googleimage import GoogleImage
from googlereverseimage import GoogleReverseImage


#block 1
#dl = GoogleImage(headless= True)
#dl.download(search_text = 'cute_babies', n_images= 5, save_folder = "babies")

#block 2
dl = GoogleReverseImage(headless= True)
dl.download(search_image= r'cute_baby.jpg', n_images= 5, save_folder = "babies")