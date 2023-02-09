import glob
import contextlib
from PIL import Image

# filepaths
fp_in = "../../Figure/iteration_*.png"
fp_out = "../../Figure/animation.gif"

# use exit stack to automatically close opened images
with contextlib.ExitStack() as stack:
    # lazily load images
    images = (stack.enter_context(Image.open(f))
              for f in sorted(glob.glob(fp_in)))

    # extract  first image from iterator
    img = next(images)

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img.save(fp=fp_out, format='GIF', append_images=images,
             save_all=True, duration=500, loop=0)
