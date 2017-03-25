import os
import math
import sys
import pickle
term_index = pickle.loads(open('./term_index.pkl', 'rb').read())

index_term = {index:term for term, index in term_index.items()}
with open('./head.svm.model') as f:
  next(f)
  next(f)
  next(f)
  next(f)
  next(f)
  next(f)
  term_weight = {}
  for i, line in enumerate(f):
    line = line.strip()
    term_weight[index_term[i]] = float(line.strip())

  for term, weight in sorted(term_weight.items(), key=lambda x:x[1]*-1):
    print(term, weight)
