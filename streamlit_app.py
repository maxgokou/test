import os

os.system('git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y -u -p $PWD')
os.system('git clone --depth 1 https://github.com/neologd/mecab-unidic-neologd.git && cd mecab-unidic-neologd && ./bin/install-mecab-unidic-neologd -n -y -u -p $PWD')

import streamlit as st

import MeCab

st.set_page_config(page_title="NEologd demo")
st.title('NEologd demo')


"""
Input the text you'd like to analyze. See the [NEologd][] docs for more details.
[NEologd]: https://github.com/neologd
"""

if st.button('Update NEologd', help='It may take some time'):
    os.system('cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y -u -p $PWD')
    os.system('cd mecab-unidic-neologd && ./bin/install-mecab-unidic-neologd -n -y -u -p $PWD')

text = st.text_area("input", "麩菓子は、麩を主材料とした日本の菓子。")

def make_row(word, kana_index=7, lemma_index=6):
    # https://stackoverflow.com/a/49774255/5602117
    ff = dict(enumerate(word.feature.split(",")))
    return dict(surface=word.surface, kana=ff.get(kana_index), lemma=ff.get(lemma_index), 
            pos1=ff.get(0), pos2=ff.get(1), pos3=ff.get(2), pos4=ff.get(3))

"""
#### [mecab-ipadic-NEologd : Neologism dictionary for MeCab](https://github.com/neologd/mecab-ipadic-neologd)
"""

data = []

tagger = MeCab.Tagger('-r /etc/mecabrc -d /home/user/app/mecab-ipadic-neologd')
node = tagger.parseToNode(text)
while node:
    if node.feature.startswith('BOS/EOS'):
        pass
    else:
        data.append(make_row(node))
    node = node.next

st.table(data)

"""
#### [mecab-unidic-NEologd : Neologism dictionary for unidic-mecab](https://github.com/neologd/mecab-unidic-neologd)
"""

data = []

tagger = MeCab.Tagger('-r /etc/mecabrc -d /home/user/app/mecab-unidic-neologd')
node = tagger.parseToNode(text)
while node:
    if node.feature.startswith('BOS/EOS'):
        pass
    else:
        data.append(make_row(node, kana_index=9, lemma_index=7))
    node = node.next

st.table(data)

"""
#### [MeCab](https://taku910.github.io/mecab/)
"""

data = []

tagger = MeCab.Tagger('-r /etc/mecabrc')
node = tagger.parseToNode(text)
while node:
    if node.feature.startswith('BOS/EOS'):
        pass
    else:
        data.append(make_row(node))
    node = node.next

st.table(data)
