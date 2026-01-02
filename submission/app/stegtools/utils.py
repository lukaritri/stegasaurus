import numpy as np
import cv2

def get_keypoints(cover_img, is_sort=True):
    """
    Returns all keypoints from cover image. Optionally sorts the keypoints.
    """
    gray = cv2.cvtColor(cover_img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    kp = sift.detect(gray, None)

    if is_sort:
        kp = sorted(kp, key=lambda k:k.response, reverse=True)

    return kp

def draw_keypoints(img, keypoints):
    """
    Draws keypoints onto an image.
    """
    new_img = img.copy()
    cv2.drawKeypoints(new_img, keypoints, new_img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    return new_img

def draw_strong_keypoints(img, keypoints, N=10, howsort='response'):
    """
    Draws the N strongest keypoints.
    """
    new_img = img.copy()

    if howsort == 'response':
        keypoints = sorted(keypoints, key=lambda kp:kp.response, reverse=True)
    elif howsort == 'size':
        keypoints = sorted(keypoints, key=lambda kp:kp.size, reverse=True)
    else:
        print('Invalid howsort. Must be one of {"response", "size"}')

    keypoints = keypoints[:N]

    cv2.drawKeypoints(new_img, keypoints, new_img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return new_img


def process_watermark(watermark, size=(15, 15)):
    """
    Converts a greyscale watermark into binary data and resizes.
    Default size is (15, 15)
    """
    grey = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
    watermark_resized = cv2.resize(grey, size)
    processed = cv2.threshold(watermark_resized, 127, 1, cv2.THRESH_BINARY)
    return processed[1]

def filestorage_to_img(file):
    """
    Converts a FileStorage object into an image to be used with OpenCV.
    """
    file_str = file.read()
    file_bytes = np.fromstring(file_str, np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR_BGR)