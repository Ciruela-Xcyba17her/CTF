from PIL import Image
import numpy as np

img_orig = np.array(Image.open('sandstorm.png').convert('L'))
width, height = len(img_orig[0]), len(img_orig)

exp = 1
while True:
    space = pow(2, exp)
    if pow(2, exp) > width or pow(2, exp) > height:
        break
    
    img_adam = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            img_adam[i][j] = img_orig[space * (i // space)][space * (j // space)]
    Image.fromarray(img_adam).convert('L').save('sandstorm_adam7_' + str(space) + 'x' + str(space) + '.png')
    exp += 1

input('[END OF PROGRAM]')