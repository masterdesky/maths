#!/home/masterdesky/.conda/envs/main/python
import os
import sys
import imageio
from datetime import datetime

def create_anim(N : int, n_steps : int):
  dir_ = 'frames-N{}-ns{}/'.format(N, n_steps)
  name = 'NR_fractal-N{}-ns{}'.format(N, n_steps)

  path = './out/' + dir_
  outdir = './out/' + dir_ + 'anim/'
  if not os.path.exists(outdir):
    os.makedirs(outdir)

  # Gather path to appropriate images to concatenate
  print('[{0}] Reading in list of images to concatenate'.format(datetime.now().isoformat()), file=sys.stderr)
  file_list = []
  for file in os.listdir(path):
    if 'nrfractal' in file:
      complete_path = path + file
      file_list.append(complete_path)
  # Sort filenames
  file_list.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

  # Define writer and create video
  writer = imageio.get_writer(outdir + '{}.mp4'.format(name),
                              codec='h264', bitrate='3500k',
                              format='mp4', fps=30)

  for i, im in enumerate(file_list):
    text = '[{0}] Appending image {1}...'.format(datetime.now().isoformat(), i)
    print(text, file=sys.stderr)
    writer.append_data(imageio.imread(im))
  writer.close()

if __name__ == '__main__':
  
  if len(sys.argv) != 3:
    print("ERROR! Usage : ./newton_video.py <N> <ns>")
    exit()

  N = int(sys.argv[1])
  n_steps = int(sys.argv[2])

  create_anim(N, n_steps)
