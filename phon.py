#!/usr/bin/env python
import sys,os,random,ast
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'EC','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF','w':'77'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
suprasegmentals={':':'3A',';':'3B','rh':'7E'}
accents={'u':'08','thh':'05','th':'01','tm':'09','tl':'00','tll':'0D'}
morphing={'l','r','m','n','N'}
glides={'h','j','w'}
C=[]
V=[]
with open(sys.argv[1]) as source: phrase,verse=ast.literal_eval(source.readline())
cypher=phrase.split(' ')
rules=''
for p in cypher:
  if p in consonants.keys():
    C.append(p)
    rules+='c'
  elif p=='.': rules+=p
  else:
    V.append(p)
    rules+='v'
if len([rl for rl in rules.split('.') if 'vvv' in rl or 'ccc' in rl])>0: sys.exit("ERROR: vvv or ccc")
rhymes={}
composition=[]
for ln in range(len(verse)):
  phonemes=''
  for lt in range(len(verse[ln])):
    rule=random.choice(rules.split('.'))
    ct=list(C)
    vt=list(V)
    pr=''
    for d in range(len(rule)):
      if rule[d]=='c': # consonant
        if d+1<len(rule) and rule[d+1]=='c': # c follows
          dc=[cc[1] for cc in enumerate(cypher) if cc[0]+1<len(cypher) and cc[1] in ct and cypher[cc[0]+1] in ct] # identify potential cc pairs
          if d==0: con=random.choice([pc for pc in dc if pc not in morphing]) # cannot begin with liquid or nasal
          else: con=random.choice([pc for pc in dc if pc not in glides]) # glides can only occur at onset
        elif pr in C: # previous is c
          try:
            tc=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in ct] # identify pr-c pairs
            if rule.endswith(rule[d]): con=random.choice([pc for pc in tc if pc not in morphing]) # syllable cannot end in c + liquid/nasal
            else: con=random.choice(tc)
          except IndexError: con='' # no possible c+c pairs, drop consonant
        elif d!=0: con=random.choice([pc for pc in ct if pc not in glides]) # glides can only occur at onset
        else: con=random.choice([pc for pc in ct if pc not in morphing]) # cannot begin with liquid or nasal
        pr=con
        if pr!='':
          phonemes+='\ipa\char"'+consonants[con]
          for x,t in enumerate(ct):
            if t==pr:
              ct.pop(x)
              break
      else:
        if verse[ln][lt]!='-':
          if verse[ln][lt] not in rhymes.keys(): rhymes[verse[ln][lt]]=vow
          vow=rhymes[verse[ln][lt]]
        elif d+1<len(rule) and rule[d+1]=='v':
          vow=random.choice([vv[1] for vv in enumerate(cypher) if vv[0]+1<len(cypher) and vv[1] in vt and cypher[vv[0]+1] in vt and vv[1]!=pr])
        else:
          try: vow=random.choice([cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in vt])
          except IndexError: vow=random.choice(vt)
        if '/' not in vow: phonemes+='\ipa\char"'+vowels[vow]
        else:
          va=vow.split('/')
          if va[1] in suprasegmentals.keys(): phonemes+='\ipa\char"'+vowels[va[0]]+'\ipa\char"'+suprasegmentals[va[1]]
          elif va[1] in accents.keys(): phonemes+='\\'+va[1]+'{\ipa\char"'+vowels[va[0]]+'}'
        pr=vow
        for x,t in enumerate(vt):
          if t==pr:
            vt.pop(x)
            break
    if lt<len(verse[ln])-1: phonemes+='\ipa\char"2E'
    elif ln<len(verse)-1: phonemes+='\\vskip 0.4em\n'
  composition.append(phonemes)
with open('temp.tex','w') as temp:
  temp.write('\\font\ipa=tipa17 scaled \magstep3 \\font\\acc=tipa17\n')
  for u,h in accents.items(): temp.write('\def\\'+u+'#1{{\\acc\\accent"'+h+' #1}}'+'\n')
  temp.write('\\null\\vfill\n')
  for syllables in composition: temp.write(syllables)
  temp.write('\\bye')
os.system('pdftex temp.tex')