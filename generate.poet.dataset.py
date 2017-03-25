import os
import sys
import glob
import math
import json
import MeCab
from pathlib import Path 
import pickle
from collections import Counter 
import random
def generate_term_index():
  term_index = {}
  m = MeCab.Tagger('-Owakati')
  m.parse("")
  files = glob.glob('./contents/*')
  num_files = len(files)
  for ni, name in enumerate(files):
    if ni%100 == 0:
      print("{} {}".format(ni, num_files))
    try:
      obj = json.loads(open(name).read())
    except json.decoder.JSONDecodeError as e:
      continue
    try:
      terms = m.parse(obj['context']).strip().split() 
    except AttributeError as e:
      continue
    for term in set( terms ):
      if term_index.get(term) is None:
        term_index[term] = len(term_index)
  open('term_index.pkl', 'wb').write( pickle.dumps(term_index) )

def make_svm():
  term_index = pickle.loads(open('./term_index.pkl', 'rb').read())
  m = MeCab.Tagger('-Owakati')
  m.parse("")
  files = glob.glob('./contents/*')
  num_files = len(files)
  f = open('dataset.svm', 'w')
  for ni, name in enumerate(files):
    if ni%100 == 0:
      print("{} {}".format(ni, num_files))
    try:
      obj = json.loads(open(name).read())
    except json.decoder.JSONDecodeError as e:
      continue
    tags  = obj['tags']
    is_poet = 'ポエム' in tags
    #print( obj['tags'] )
    if not is_poet and random.random() > 0.01:  continue
    try:
      terms = m.parse(obj['context']).strip().split() 
    except AttributeError as e:
      continue
    vec = [0.]*len(term_index)
    for term, freq in Counter(terms).items():
      vec[term_index[term]] =  freq
    f.write("%d "%int(is_poet) + " ".join(["%d:%04f"%(i+1,w) for i,w in filter(lambda x:x[1]!=0., [(i,w)for i,w in enumerate(vec)])]) + "\n")
    print(int(is_poet))
if __name__ == '__main__':
  if '--generate_term_index' in sys.argv:
    generate_term_index()
  if '--make_svm' in sys.argv:
    make_svm()
