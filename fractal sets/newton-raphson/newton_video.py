#!/home/masterdesky/miniconda3/envs/main/python
import os
import sys
import imageio
from datetime import datetime

def create_anim():
  fold = 'frames-N{}-ns{}'.format(N,ns)
  name = 'NR_fractal-N{}-ns{}'.format(N,ns)

  path = '/home/masterdesky/data/GADGET4/Simulations/Masses-{}/{}/output/frames/'.format(MBINS, fold)
  out = '/home/masterdesky/data/GADGET4/Simulations/Masses-{}/{}/output/'.format(MBINS, fold)

  # Gather path to appropriate images to concatenate
  print('[{0}] Reading in list of images to concatenate'.format(datetime.now().isoformat()), file=sys.stderr)
  file_list = []
  for file in os.listdir(path):
  	complete_path = path + file
  	file_list.append(complete_path)
  # Sort filenames
  file_list.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

  # Define writer and create video
  writer = imageio.get_writer(out + '{}.mp4'.format(name), fps=30)

  for i, im in enumerate(file_list):
    text = '[{0}] Appending image {1}...'.format(datetime.now().isoformat(), i)
    print(text, file=sys.stderr)
    writer.append_data(imageio.imread(im))
  writer.close()

if __name__ == '__main__':
  
  if len(sys.argv) != 6:
    print("ERROR! Usage : ./newton_video.py <N> <ns>")
    exit()

  N = int(sys.argv[1])
  ns = int(sys.argv[2])

  create_anim()
