import pytest
import numpy as np
import cv2
from stegtools.embed_watermark import embed
from stegtools.tampering_detector import compare_lsb

@pytest.fixture
def cover_img():
    test_img = [
        [120, 132, 140, 150, 160],
        [110, 121, 131, 141, 151],
        [100, 111, 122, 132, 142],
        [90, 101, 112, 123, 133],
        [80, 91, 102, 113, 124]
    ]
    return np.array(test_img)

@pytest.fixture
def watermark():
    test_watermark = [
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1]
    ]
    return np.array(test_watermark)

@pytest.fixture
def expected_result():
    expected_result = np.array([
        [121, 132, 141, 150, 161],
        [110, 121, 130, 141, 150],
        [101, 110, 123, 132, 143],
        [90, 101, 112, 123, 132],
        [81, 90, 103, 112, 125]
    ])
    return expected_result

def test_embed(cover_img, watermark, expected_result):
    result = embed(cover_img, watermark)

    print(result)

    assert np.equal(result, expected_result).all()

def test_compare_lsb(expected_result, watermark):
    result = compare_lsb(expected_result, watermark)
    assert result