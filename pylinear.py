import os
import math
import os
import sys


def _make_svm(Ys:list, Xs:list) -> str:
  res = [] 
  for y,x in zip(Ys, Xs):
    y = "{}".format(y)
    x = " ".join(["{}:{}".format(i+1,x) for i,x in enumerate(x)])
    res.append("{} {}\n".format(y,x))
  train, test = res[:int(len(res)/0.8)], [int(len(res)/0.8):]
  return train, test

def test(inputs="", y_index=None):
  Xs = []
  Ys = []
  with open(inputs) as f:
    for line in f:
      line = line.strip()
      ents = list(map(float, line.split()))
      if y_index is None:
        y    = ents.pop()
      else:
        y    = ents.pop(y_index)
      x    = ents
      Ys.append(y)
      Xs.append(x)
  train, test = _make_svm(Ys, Xs)
  open('{}.train.svm'.format(inputs), 'w').write(train)
  open('{}.test.svm'.format(inputs), 'w').write(test)
  os.system('./train {}.train.svm'.format(inputs))

def init():
  os.system('git clone https://github.com/cjlin1/liblinear.git')
  os.system('cd liblinear && make -j4')
  os.system('mv ./liblinear/train ./liblinear/predict ./')

if __name__ == '__main__':
  print("here is test mode...")
  init()
  test(inputs="./sample.txt")
