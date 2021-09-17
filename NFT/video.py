#!/home/masterdesky/miniconda3/envs/gadget4/python
import os
import re
import sys
import imageio
from datetime import datetime

# Gather path to appropriate images to concatenate
def read_files(path):
  print('[{0}] Reading in list of images to concatenate'.format(datetime.now().isoformat()), file=sys.stderr)
  file_list = []
  for file in os.listdir(path):
    complete_path = path + file
    file_list.append(complete_path)

  # Sort filenames
  # lambda x: int(''.join(filter(str.isdigit, x.split())))
  def atoi(text):
    return int(text) if text.isdigit() else text

  def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

  file_list.sort(key=natural_keys)

  return file_list


def create_video(file_list, out_file):
  # Define writer and create video
  writer = imageio.get_writer(out_file, fps=30)

  for i, im in enumerate(file_list):
    text = '[{0}] Appending image #{1}...'.format(datetime.now().isoformat(), i)
    print(text, file=sys.stderr)
    writer.append_data(imageio.imread(im))
  writer.close()


if __name__ == '__main__':
  att = sys.argv[1]
  path = '/home/masterdesky/GitHub/Aesthetic_Function_Graphposting/NFT/out/{0}/frames/'.format(att)
  out_dir = '/home/masterdesky/GitHub/Aesthetic_Function_Graphposting/NFT/out/{0}/animation/'.format(att)
  out_file = out_dir + '{0}.mp4'.format(att)
  
  if not os.path.exists(out_dir):
    os.makedirs(out_dir)

  file_list = read_files(path)
  create_video(file_list, out_file)