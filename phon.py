#!/usr/bin/env python
import sys,os,random,ast
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'EC','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
suprasegmentals={':':'3A',';':'3B'}
accents={'u':'08','thh':'05','th':'01','tm':'09','tl':'00','tll':'0D'}
C=[]
V=[]
with open(sys.argv[1]) as source: phrase,verse=ast.literal_eval(source.readline())
for p in phrase.split(' '):
  if p in consonants.keys(): C.append(p)
  else: V.append(p)
rhymes={}
composition=[]
for ln in range(len(verse)):
  phonemes=''
  for lt in range(len(verse[ln])):
    if verse[ln][lt]!='-':
      if verse[ln][lt] not in rhymes.keys(): rhymes[verse[ln][lt]]=random.choice(V)
      r=rhymes[verse[ln][lt]]
    else: r=random.choice(C+V)
    if r in C:
      phonemes+='\ipa\char"'+consonants[r]
      r=random.choice(V)
    else: phonemes+='\ipa\char"'+consonants[random.choice(C)]
    if '/' not in r: phonemes+='\ipa\char"'+vowels[r]
    else:
      a=r.split('/')
      if a[0] in suprasegmentals.keys(): phonemes+='\ipa\char"'+vowels[a[1]]+'\ipa\char"'+suprasegmentals[a[0]]
      elif a[0] in accents.keys(): phonemes+='\\'+a[0]+'{\ipa\char"'+vowels[a[1]]+'}'
    if random.getrandbits(1)==1: phonemes+='\ipa\char"'+consonants[random.choice(C)]
    if lt<len(verse[ln])-1: phonemes+='\ipa\char"2E'
    else: phonemes+='\\vskip 0.4em\n'
  composition.append(phonemes)
with open('temp.tex','w') as temp:
  temp.write('\\font\ipa=tipa17 scaled \magstep3 \\font\\acc=tipa17\n')
  for u,h in accents.items(): temp.write('\def\\'+u+'#1{{\\acc\\accent"'+h+' #1}}'+'\n')
  temp.write('\\null\\vfill\n')
  for syllables in composition: temp.write(syllables)
  temp.write('\\bye')
os.system('pdftex temp.tex')