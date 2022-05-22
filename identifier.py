import base64, io
import numpy as np
from PIL import Image


def rgb_to_hex(r, g, b):
  return ('#{:X}{:X}{:X}').format(r, g, b)

def get_colors(img):
    colors, count = np.unique(img.reshape(-1, img.shape[-1]), axis=0, return_counts=True) 
    # -1 in reshape (at least in this case) means that we want numpy to reshape the image based on it's current dimesion
    # that means if the original shape is (3, 4, 3), we'd want something like (12, 3)
    # so it basically flattens the image to one long array of rgb values

    ind = np.argpartition(-count, kth=5)[:5] # get the five most dominant colors of an image
    frequent = colors[ind]

    """
    this loop iterates over each element in "frequent" array. For each iteration, compare the current element's color value with the next and 
    ensure the RGB differences are at least 21, if it's more remove that next element.

    Move to the next element and do same. Note that already similar color values are removed on each inner iteration (while loop), hence there is a 
    probability that the array reduces on each outer iteration (for loop)
    """
    
    #print(frequent)
    threshold = np.array([20, 20, 20])
    for i in range(len(frequent)-1):
        next = i+1
        while (1):
            try:
                distance = np.abs(frequent[i] - frequent[next])
                if ((distance[0] < threshold[0]) or (distance[1] < threshold[1]) or (distance[2] < threshold[2])) :
                    frequent = np.delete(frequent, next, axis=0)
                else:
                    next = next + 1
            except Exception as e:
                break
    
    all_colors = []
    rgbs = []
    hex = []

    for color in frequent:
        new_img = np.full((300, 300, 3), fill_value=color[:3], dtype=np.uint8)
        new_img = Image.fromarray(new_img.astype(np.uint8))
        data = io.BytesIO()
        new_img.save(data, 'JPEG')
        encoded = base64.b64encode(data.getvalue())
        decoded_img = encoded.decode('utf-8')
        mime = "image/jpeg"
        img_data = "data:%s;base64,%s" % (mime, decoded_img)
        hex.append(rgb_to_hex(int(color[0]), int(color[1]), int(color[2])))
        rgb_tuple = ( int(color[0]), int(color[1]), int(color[2]) )
        rgbs.append(rgb_tuple)
        all_colors.append(img_data)
    
    return {"images": all_colors, "hex": hex, "rgb": rgbs}
