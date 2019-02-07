import cv2
import numpy as np
import os


def similarity(des1, des2):
    """
    The similarity between two image descriptors by finding the closest
    neighbor for each vector in des1, and then averaging them. Then averaging this distance
    to find the distance between des1 and des2.
    :param des1: First list of image descriptors
    :param des2: Second list of image descriptors
    :return: Distance between the two
    """
    matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = matcher.match(des1, des2)
    distances = np.array([1 / (1 + m.distance) for m in matches])
    return np.sum(distances) / len(distances)


def closest_image(source_im, images):
    """
    Finds the closest image in images to im using SIFT similarity.
    :param source_im: source image
    :param images: images to compare against
    :return: the index in images of the most similar image
    """
    _, source_des = apply_sift(source_im)
    similarities = []
    for img in images:
        _, des = apply_sift(img)
        similarities.append(similarity(source_des, des))
    max_index = np.argmax(similarities)
    print('Similarity: {:3f}'.format(similarities[max_index]))
    return max_index


def apply_sift(img):
    """
    Apply SIFT to an image.
    :param img: Image to apply
    :return: SIFT keypoints
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(gray, None)
    return kp, des


def display_closest_image(i, images):
    closest_im_index = closest_image(images[i],
                                     images[:i] + images[i+1:])
    closest_img = images[closest_im_index]

    cv2.imwrite('img1.jpg', images[i])
    cv2.imwrite('img2.jpg', closest_img)
    
    cv2.imshow('original', images[i])
    cv2.imshow('most similar', closest_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', 'desert')
    images = []
    for fname in os.listdir(path):
        img_path = os.path.join(path, fname)
        images.append(cv2.imread(img_path, cv2.IMREAD_COLOR))
    display_closest_image(5, images)
