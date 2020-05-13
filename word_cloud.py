# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from pdf2txt import pdf2txt
import glob

NCORE = os.cpu_count()

# This PDF is scan image, not selectable text. image to text?
# text = pdf2txt("../journals/1973_Wiggins.pdf")
# print(text)


def read1file(i, files):
    file = files[i]
    text = pdf2txt(file)
    print(file, len(text))
    return text


def read_pdfs():
    files = glob.glob("../journals/*.pdf")
    text_list = Parallel(n_jobs=NCORE)(delayed(read1file)(i, files)
        for i in range(len(files)))

    npapers = 0
    texts = ""
    for text in text_list:
        if len(text) > 200:
            texts += text
            npapers += 1
    print("Number of papers =", npapers)

    fn = "papers.txt"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(texts)

    return texts


def read_text():
    fn = "papers.txt"
    with open(fn, 'r', encoding="utf-8") as file:
        texts = file.read()
    return texts


# Create stop-word list
stopwords = set(STOPWORDS)
stopwords.update([
    "mcmechan", "et al", "figure", "seg", "license", "downloaded", "http",
    "library", "redistribution", "annual", "international", "fig", "terms",
    "et", "al", "copyright", "one", "two", "org", "seg org", "cid", "thus",
    "corresponding", "subject copyright", "see use", "result"])

# text = read_pdfs()
text = read_text()
text = text.lower()

# Getting rid of the stopwords
clean_text = [word for word in text.split() if word not in stopwords]

# Converting the list to string
text = ' '.join([str(elem) for elem in clean_text])

# for word in stopwords:
#     text = text.replace(word, "")
text = text.replace("copyright", "")
text = text.replace("see use", "")
text = text.replace("use http", "")
text = text.replace("subject see", "")
text = text.replace("subject http", "")
text = text.replace("http", "")
text = text.replace("using", "")
text = text.replace("used", "")
text = text.replace("use", "")
text = text.replace("respectively", "")
text = text.replace("will", "")
text = text.replace("texas dallas", "")
# print("subject copyright" in text)
# exit()

# Generate a word cloud image
wordcloud = WordCloud(width=1200, height=900, stopwords=stopwords,
                      background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()

wordcloud.to_file("word_cloud.png")
