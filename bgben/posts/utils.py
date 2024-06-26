import os
import secrets
from PIL import Image, ImageOps
from flask import current_app

def save_picture(form_picture, pic_folder, width, height):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(current_app.root_path, pic_folder, picture_fn)

  output_size = (width, height)
  i = Image.open(form_picture)
  i = ImageOps.contain(i, output_size)
  i.save(picture_path)

  return picture_fn


def delete_picture(pic_folder, picture_fn):
  os.remove(os.path.join(current_app.root_path, pic_folder, picture_fn))
