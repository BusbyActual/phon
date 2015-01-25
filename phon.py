#
# Define lists of hexdecimal values referencing certain tipa glyphs
# Separate lists into consonants and vowels, and use these to
# populate the verse, writing a concoction of
# \def\syllable{\ipa\char"hex} statements to the temp.tex file.
#
#!/usr/bin/env python
import sys,os,random

consonants=['70','74','FA','63','KB','71','50','62','64','E3','E9','67','E5','6D','4D','6E','EF','F1','4E','F0','E0','72','F6','52','F3','46','66','54','73','53','F9','E7','78','58','E8','68','42','76','44','7A','5A','4A','47','43','51','48','EC','D0','56','F4','F5','6A','EE','6C','ED','4C','CF']
            
vowels=['69','79','31','30','57','75','49','59','55','65','F8','39','38','37','6F','40','45','F7','33','C5','32','4F','35','E6','D7','61','41','36']
            
syllables=['cv','cvc']

verse=['----A',
       '----B',
       '----A',
       '--B---A',
       '--A---B']
       
rhymes={}

composition=[]

with open('temp.tex','w') as temp:
  temp.write('\\nopagenumbers\n\\font\ipa=tipa17\n')
  
  for ln in range(len(verse)):
    composition.append([])
    for lt in verse[ln]:
      if lt!='-':
        if lt not in rhymes.keys():
          rhymes[lt]='\ipa\char"'+random.choice(consonants+vowels)
        composition[ln].append(rhymes[lt])
      else: composition[ln].append('\ipa\char"'+random.choice(consonants+vowels))
  
  composition[0]=['\ipa\char"5B']+composition[0]
  for c in composition:
    temp.write('\n\n'+''.join(c))
    
  temp.write('\ipa\char"5D\\bye')

os.system('pdftex temp.tex')
