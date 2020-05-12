# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import matplotlib.pyplot as plt
import bibtexparser

fn = "mcmechan.bib"
with open(fn) as bibtex_file:
    bibtex_str = bibtex_file.read()
bdb = bibtexparser.loads(bibtex_str)

year_pubs = {}
for entry in bdb.entries:
    year = entry['year']
    if year not in year_pubs:
        year_pubs[year] = 1
    else:
        year_pubs[year] += 1

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 6)
ax.grid(zorder=0)
ax.bar(year_pubs.keys(), year_pubs.values(), color='g', zorder=3)
ax.set_ylabel('Number of Papers')
plt.xticks(rotation='vertical')
# plt.show()

fn = "year_pubs.png"
plt.savefig(fn)
plt.close()
