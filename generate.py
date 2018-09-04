#!/usr/bin/env python

import numpy
import pandas as pd
from random import (
    choice,
    randint
)
from string import ascii_lowercase

d_min = 2
d_max = 20
n = 100

domains = pd.read_csv('top_level_domains.txt',
        comment='#',
        names=[ 'name' ])

domains_usage = pd.read_csv('top_level_domains_usage.txt',
        sep='\s+',
        comment='#',
        names=[ 'name', 'p' ],
        converters={ 'p': lambda x : float(x.strip('%')) / 100 })

# merge
domains = pd.merge(domains, domains_usage, how='left', on='name')

# replace NaN
sum_p = domains.p.sum()
if sum_p > 1.0:
    raise Exception('invalid prob > 1')
min_p = (1.0 - sum_p) / domains.p.isna().sum()
domains = domains.fillna(min_p)

def random_top_level():
    return numpy.random.choice(domains.name, p=domains.p) # non-uniform random

for i in range(0, 100):
    top = random_top_level()
    p = (''.join(choice(ascii_lowercase) for i in range(randint(d_min, d_max+1))))
    print(p + '.' + top)
