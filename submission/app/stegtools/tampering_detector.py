import cv2
import numpy as np
from .utils import *
from .embed_watermark import *
import time

def compare_lsb(region, watermark):
    """
    Compare lsb of a region of an image with the watermark.
    """
    mask = np.ones(region.shape, dtype=np.uint8)
    region_lsb = region & mask

    return np.equal(region_lsb, watermark).all()

def draw_circles(img, matched_kps, verified_kps):
    """
    Draws circle around keypoints. Green circle where the watermark was found,
    red circle where it wasn't.
    """

    new_img = img.copy()
    radius = img.shape[1] // 50
    stroke = radius // 6

    for kp in matched_kps:
        x, y = kp.pt
        x = int(round(x))
        y = int(round(y))

        if kp in verified_kps:
            new_img = cv2.circle(new_img, (x, y), radius, (0, 255, 0), stroke)
        else:
            new_img = cv2.circle(new_img, (x, y), radius, (0, 0, 255), stroke)

    return new_img

def get_error(matched_kps, verified_kps):
    """
    Returns the proportion of kps that match.
    """
    return len(verified_kps) / len(matched_kps)

def verify_authenticity(img, watermark, N=100, threshold=0.95):
    """
    Verifies whether an image contains watermark or not.

    params
    img: image to check
    watermark: watermark to check
    N: number of keypoints
    threshold: threshold proportion of matching keypoints

    returns
    is_authentic bool: True if authentic, False otherwise
    matched_kps [cv2.KeyPoint]: set of keypoints where the watermark should be
    verified_kps [cv2.KeyPoint]: set of keypoints where the watermark was found
    """

    keypoints = get_keypoints(img)
    count = 0
    i = 0

    # Only check blue channel
    img_b = img[:, :, 0]

    # Process watermark
    watermark = process_watermark(watermark)
    w_x, w_y = watermark.shape

    matched_kps = []
    verified_kps = []
    used_px = np.zeros(img_b.shape, dtype=np.uint8)

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

        # If region has already been used, skip
        if used_px[x_min:x_max, y_min:y_max].any():
            i += 1
            continue

        matched_kps.append(keypoints[i])

        region = img_b[x_min : x_max, y_min : y_max]
        used_px[x_min:x_max, y_min:y_max] = 1

        # If region contains the watermark, then add to set of matched keypoints
        if compare_lsb(region, watermark):
            verified_kps.append(keypoints[i])

        count += 1
        i += 1

    return len(verified_kps) >= threshold * N, list(matched_kps), list(verified_kps)

if __name__ == '__main__':

    img_name = 'tori'
    img_path = f'stegtools/images/{img_name}.jpg'
    
    test_img = cv2.imread(img_path)
    test_img = cv2.resize(test_img, None, fx=0.2, fy=0.2)
    print(test_img.shape)

    # test_watermark = np.array([
    #     [1, 0, 1, 0, 1],
    #     [0, 1, 0, 1, 0],
    #     [1, 0, 1, 0, 1],
    #     [0, 1, 0, 1, 0],
    #     [1, 0, 1, 0, 1]
    # ], dtype=np.uint8)

    test_watermark = cv2.imread('stegtools/images/watermark.png', flags=cv2.IMREAD_GRAYSCALE)

    N = 10

    new_img, keypoints = embed_watermark(test_img, test_watermark, N)

    start = time.time()
    is_authentic, kps, verified_kps = verify_authenticity(new_img, test_watermark, N)
    end = time.time()

    print(f'Is authentic: {is_authentic}')
    print(f'Time taken: {end - start}')

    img_kps = draw_keypoints(new_img, list(kps))

    cv2.imshow('Keypoints', img_kps)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    test_kp = get_keypoints(test_img)
    kp_img = draw_strong_keypoints(test_img, test_kp, howsort='response')

    cv2.imshow('Strong keypoints', kp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()