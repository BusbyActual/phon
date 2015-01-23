# 1)  Open source file, and create variables for document prep.
#     First line is a tuple with variables, remaining lines are a rhyme scheme
#
#     Example:    (language,font-size,etc..)
#                 ----A
#                 ----B
#                 ----A
#                 --B-B
#
# 2)  readline() and then readlines() on source file to separate first-line tuple vars
#
# 3)  compose TeX flags using document prep variables, introduce standard flags:
#
#     \usepackage{tipa}
#     \nopagenumbers
#
# 4)  source language defenitions from language file referenced by doc. prep. vars
#
# 5)  language files will contain a dictionary which separates IPA symbols into consonants and vowels,
#     and defines rules for their usage. The language definitions will also contain a list of
#     possible syllable structures = [ 'CV', 'CVC', ... ]
#
#     phonemes = { '\IPA' : ('C',[*a],[*b], ...) , ...}
#
#     each '\IPA' declaration is paired with a tuple which defines rules for its usage.
#     the tuple will begin with either 'C' or 'V' to indicate either consonant or vowel,
#     followed by two lists, which define which symbols are permitted to preceed and follow that symbol.
#     (it this results in a conflct where no symbols 'fit', the sound will be replaced by a stop, or comprable
#
# 6)  scan verse for alpha characters, and assign each instance a phoneme -
#     this will 'seed' the verse with an initial phonemic structure
#
# 7)  Then all that remains to be done is randomly select syllables in the verse, assigning each a phoneme
#     according to the language defenitions.
#
# 8)  This process is done once to assign each syllable a phoneme, then again to 'fill' each syllable with
#     additional phonemes until each matches either 'CV' or 'CVC' structure (or however this is defined.)
#
#     Note that consonants may be composed of multiple consonant phonemes, same with vowels - this all
#     depends on how the language defines the potential syllabic structures.
#
# 9)  Once the verse has been composed, write enclose strings in textIPA flags and write to the TeX file.
#     Close the TeX file with '\bye'
#
# 10) close the tex file and issue commands:
#
#     os.system('pdftex file.tex')
#
#
#!/usr/bin/env python
import sys
import os

with open('temp.tex','w') as temp:
  temp.write('\\nopagenumbers\n\\usepackage{tipa}\n')
  temp.write('\\textipa{Z}')
  temp.write('\\bye')

os.system('pdftex temp.tex')