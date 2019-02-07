
import flickr_api
from flickr_api import Photo
import os


def save_images_by_tag(tag):
    """
    Saves all the images of a specific tag by flickr search.
    :param tag: Tag to search for
    :return:
    """
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', tag)
    if not os.path.isdir(path):
        os.chdir('images')
        os.mkdir(tag)
    for photo in Photo.search(tags=tag):
        photo.save(os.path.join(path, photo.id), size_label='Medium 640')


if __name__ == '__main__':
    save_images_by_tag('jungle')
