import os
import sys
import imageio
from datetime import datetime

path = './output/'
out = './'

# Gather path to appropriate images to concatenate
print('[{0}] Reading in list of images to concatenate'.format(datetime.now().isoformat()), file=sys.stderr)
file_list = []
for file in os.listdir(path):
    if "frame" in file:
        complete_path = path + file
        file_list.append(complete_path)
# Sort filenames
file_list.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

# Define writer and create video
writer = imageio.get_writer(out + 'hypercube_rotate.mp4', fps=60)

for i, im in enumerate(file_list):
    text = '[{0}] Appending image #{1}...'.format(datetime.now().isoformat(), i)
    print(text, file=sys.stderr)
    writer.append_data(imageio.imread(im))
writer.close()
