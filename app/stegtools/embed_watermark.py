import cv2
import numpy as np
from .utils import *
    
def embed(region, watermark):
    """
    Embed a single watermark over a region of an image, given that they are the same shape.
    """

    assert region.shape == watermark.shape

    # Modify lsb
    region = region // 2
    region *= 2
    region += watermark

    return region

def embed_watermark(cover_img, watermark, N=100):
    """
    Embeds watermark into cover image.

    params
    cover_img: image to embed the watermark in
    watermark: watermark image to embed into the cover image
    N: number of keypoints to embed the watermark in

    returns
    embedded_img [[int]]: new image with embedded watermark
    keypoints_embedded [cv2.KeyPoint]: list of keypoints that were embedded. Used for debugging
    """

    # Only modify blue channel
    embedded_img = cover_img.copy()
    img_b = embedded_img[:, :, 0]
    
    # Process watermark
    watermark = process_watermark(watermark)
    w_x, w_y = watermark.shape

    keypoints = get_keypoints(cover_img)
    i = 0
    count = 0
    keypoints_embedded = []
    used_px = np.zeros(img_b.shape, dtype=np.uint8) # mask to keep track of overlapping key points

    while i < len(keypoints) and count < N:
        y, x = keypoints[i].pt
        x = int(round(x))
        y = int(round(y))

        # Extract region from cover image to embed watermark
        x_min = x - (w_x // 2)
        x_max = x + (w_x // 2) + 1

        y_min = y - (w_y // 2)
        y_max = y + (w_y // 2) + 1

        # If region lies outside the image, skip
        if x_min < 0 or x_max > img_b.shape[0] \
            or y_min < 0 or y_max > img_b.shape[1]:
            i += 1
            continue

        # If region overlaps with a previous key point, skip
        if used_px[x_min:x_max, y_min:y_max].any():
            i += 1
            continue

        region = img_b[x_min : x_max, y_min : y_max]
        
        # Embed
        img_b[x_min : x_max, y_min : y_max] = embed(region, watermark)

        # Update mask
        used_px[x_min:x_max, y_min:y_max] = 1

        keypoints_embedded.append(keypoints[i])
        count += 1
        i += 1

    embedded_img[:, :, 0] = img_b
    return embedded_img, keypoints_embedded
        

if __name__ == '__main__':

    img_name = 'tori'
    img_path = f'images/{img_name}.png'
    
    test_img = cv2.imread(img_path)
    # test_img = cv2.resize(test_img, None, fx=0.2, fy=0.2)
    print(test_img.shape)

    # test_watermark = np.array([
    #     [1, 0, 1, 0, 1],
    #     [0, 1, 0, 1, 0],
    #     [1, 0, 1, 0, 1],
    #     [0, 1, 0, 1, 0],
    #     [1, 0, 1, 0, 1]
    # ], dtype=np.uint8)
    test_watermark = cv2.imread('images/watermark.png')

    new_img, _ = embed_watermark(test_img, test_watermark)
    # cv2.imwrite(f'images/{img_name}_marked.png', new_img)

    # cv2.imshow('test image', test_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # cv2.imshow('new image', new_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()