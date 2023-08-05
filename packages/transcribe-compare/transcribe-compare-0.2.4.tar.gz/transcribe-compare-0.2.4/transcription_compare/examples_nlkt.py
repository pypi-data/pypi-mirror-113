#import nltk
# # nltk.download('wordnet')
# # nltk.download('averaged_perceptron_tagger')
# from nltk.corpus import wordnet
# from nltk.stem import WordNetLemmatizer
# def get_wordnet_pos(word):
#     """Map POS tag to first character lemmatize() accepts"""
#     tag = nltk.pos_tag([word])[0][1][0].upper()
#     tag_dict = {"J": wordnet.ADJ,
#                 "N": wordnet.NOUN,
#                 "V": wordnet.VERB,
#                 "R": wordnet.ADV}
#
#     return tag_dict.get(tag, wordnet.NOUN)
#
#
# # 1. Init Lemmatizer
# lemmatizer = WordNetLemmatizer()
#
# # 2. Lemmatize Single Word with the appropriate POS tag
# word = 'working'
# print(get_wordnet_pos(word))
# print(lemmatizer.lemmatize(word, get_wordnet_pos(word)))

default_rule_tuple = (
    "ai*2.",  # -ia > -   if intact
    "a*1.",  # -a > -    if intact
    "bb1.",  # -bb > -b
    "city3s.",  # -ytic > -ys
    "ci2>",  # -ic > -
    "cn1t>",  # -nc > -nt
    "dd1.",  # -dd > -d
    "dei3y>",  # -ied > -y
    "deec2ss.",  # -ceed >", -cess
    "dee1.",  # -eed > -ee
    "de2>",  # -ed > -
    "dooh4>",  # -hood > -
    "e1>",  # -e > -
    "feil1v.",  # -lief > -liev
    "fi2>",  # -if > -
    "gni3>",  # -ing > -
    "gai3y.",  # -iag > -y
    "ga2>",  # -ag > -
    "gg1.",  # -gg > -g
    "ht*2.",  # -th > -   if intact
    "hsiug5ct.",  # -guish > -ct
    "hsi3>",  # -ish > -
    "i*1.",  # -i > -    if intact
    "i1y>",  # -i > -y
    "ji1d.",  # -ij > -id   --  see nois4j> & vis3j>
    "juf1s.",  # -fuj > -fus
    "ju1d.",  # -uj > -ud
    "jo1d.",  # -oj > -od
    "jeh1r.",  # -hej > -her
    "jrev1t.",  # -verj > -vert
    "jsim2t.",  # -misj > -mit
    "jn1d.",  # -nj > -nd
    "j1s.",  # -j > -s
    "lbaifi6.",  # -ifiabl > -
    "lbai4y.",  # -iabl > -y
    "lba3>",  # -abl > -
    "lbi3.",  # -ibl > -
    "lib2l>",  # -bil > -bl
    "lc1.",  # -cl > c
    "lufi4y.",  # -iful > -y
    "luf3>",  # -ful > -
    "lu2.",  # -ul > -
    "lai3>",  # -ial > -
    "lau3>",  # -ual > -
    "la2>",  # -al > -
    "ll1.",  # -ll > -l
    "mui3.",  # -ium > -
    "mu*2.",  # -um > -   if intact
    "msi3>",  # -ism > -
    "mm1.",  # -mm > -m
    "nois4j>",  # -sion > -j
    "noix4ct.",  # -xion > -ct
    "noi3>",  # -ion > -
    "nai3>",  # -ian > -
    "na2>",  # -an > -
    "nee0.",  # protect  -een
    "ne2>",  # -en > -
    "nn1.",  # -nn > -n
    "pihs4>",  # -ship > -
    "pp1.",  # -pp > -p
    "re2>",  # -er > -
    "rae0.",  # protect  -ear
    "ra2.",  # -ar > -
    "ro2>",  # -or > -
    "ru2>",  # -ur > -
    "rr1.",  # -rr > -r
    "rt1>",  # -tr > -t
    "rei3y>",  # -ier > -y
    "sei3y>",  # -ies > -y
    "sis2.",  # -sis > -s
    "si2>",  # -is > -
    "ssen4>",  # -ness > -
    "ss0.",  # protect  -ss
    "suo3>",  # -ous > -
    "su*2.",  # -us > -   if intact
    "s*1>",  # -s > -    if intact
    "s0.",  # -s > -s
    "tacilp4y.",  # -plicat > -ply
    "ta2>",  # -at > -
    "tnem4>",  # -ment > -
    "tne3>",  # -ent > -
    "tna3>",  # -ant > -
    "tpir2b.",  # -ript > -rib
    "tpro2b.",  # -orpt > -orb
    "tcud1.",  # -duct > -duc
    "tpmus2.",  # -sumpt > -sum
    "tpec2iv.",  # -cept > -ceiv
    "tulo2v.",  # -olut > -olv
    "tsis0.",  # protect  -sist
    "tsi3>",  # -ist > -
    "tt1.",  # -tt > -t
    "uqi3.",  # -iqu > -
    "ugo1.",  # -ogu > -og
    "vis3j>",  # -siv > -j
    "vie0.",  # protect  -eiv
    "vi2>",  # -iv > -
    "ylb1>",  # -bly > -bl
    "yli3y>",  # -ily > -y
    "ylp0.",  # protect  -ply
    "yl2>",  # -ly > -
    "ygo1.",  # -ogy > -og
    "yhp1.",  # -phy > -ph
    "ymo1.",  # -omy > -om
    "ypo1.",  # -opy > -op
    "yti3>",  # -ity > -
    "yte3>",  # -ety > -
    "ytl2.",  # -lty > -l
    "yrtsi5.",  # -istry > -
    "yra3>",  # -ary > -
    "yro3>",  # -ory > -
    "yfi3.",  # -ify > -
    "ycn2t>",  # -ncy > -nt
    "yca3>",  # -acy > -
    "zi2>",  # -iz > -
    "zy1s.",  # -yz > -ys
)
print(len(default_rule_tuple))