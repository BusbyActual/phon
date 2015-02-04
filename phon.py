#!/usr/bin/env python
import sys,os,random
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'EC','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF','w':'77'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
suprasegmentals={':':'3A',';':'3B','rh':'7E'}
accents={'u':'08','thh':'05','th':'01','tm':'09','tl':'00','tll':'0D'}
morphing={'l','r','m','n','N'}
glides={'h','j','w'}
rhymes={}
C=set()
V=set()
with open(sys.argv[1]) as source: lines=map(lambda x: x.rstrip(), source.readlines())
cypher=' . '.join(lines).split(' ')
verse=map(lambda x: ''.join([y for y in x if y!=' ']).split('.'), lines)
rules=''
for p in cypher:
  if p in consonants.keys():
    C.add(p)
    rules+='c'
  elif p=='.': rules+=p
  else:
    V.add(p)
    rules+='v'
phonemes=''
for ln in range(len(verse)):
  if verse[ln][0]!=' ': phonemes+='\centerline{'
  else:
    phonemes+='\\vskip 1.4em\n'
    break
  for lt in range(len(verse[ln])):
    core=''.join([cr for cr in verse[ln][lt] if cr not in C])
    if core in rhymes.keys(): rule=random.choice([rl for rl in set(rules.split('.')) if len(rhymes[core])==len([syl for syl in rl if syl=='v'])])
    else: rule=random.sample(set(rules.split('.')),1)[0]
    ct=set(C)
    vt=set(V)
    pr=''
    for d in range(len(rule)):
      if rule[d]=='c':
        if d+1<len(rule) and rule[d+1]=='c':
          pre=[ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in ct and cypher[ph[0]+1] in ct]
          if d==0:
            con=random.choice([pc for pc in pre if pc not in morphing])
          else:
            con=random.choice([pc for pc in pre if pc not in glides])
        elif pr in C:
          try:
            pre=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in ct]
            if d<len(rule)-1: con=random.choice(pre)
            else: con=random.choice([pc for pc in pre if pc not in morphing])
          except IndexError: con=''
        elif d!=0:
          try:
            pre=[ph[1] for ph in enumerate(cypher) if ph[1] in ct-glides and cypher[ph[0]-1]==pr]
            con=random.choice(pre)
          except IndexError: con=random.choice([pc for pc in ct if pc not in glides])
        else: con=random.choice([pc for pc in ct if pc not in morphing])
        pr=con
        if con in ct: ct.remove(con)
      else:
        if d+1<len(rule) and rule[d+1]=='v':
          pre=[ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in vt and cypher[ph[0]+1] in vt]
          if core not in rhymes.keys(): rhymes[core]=[random.choice(pre)]
          vow=rhymes[core][0]
        elif pr in V:
          try:
            pre=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in vt]
            if len(rhymes[core])==1: rhymes[core].append(random.choice(pre))
            vow=rhymes[core][1]
          except IndexError: vow=''
        else:
          if core not in rhymes.keys():
            try: rhymes[core]=[random.choice([cc[1] for cc in enumerate(cypher) if cc[1] in vt and cypher[cc[0]-1]==pr])]
            except IndexError: rhymes[core]=[random.choice(list(vt))]
          vow=rhymes[core][0]
        pr=vow
        if vow in vt: vt.remove(vow)
      if pr!='':
        if '/' not in pr: phonemes+='\ipa\char"'+dict(consonants.items()+vowels.items())[pr]
        else:
          va=pr.split('/')
          if va[1] in suprasegmentals.keys(): phonemes+='\ipa\char"'+vowels[va[0]]+'\ipa\char"'+suprasegmentals[va[1]]
          elif va[1] in accents.keys(): phonemes+='\\'+va[1]+'{\ipa\char"'+vowels[va[0]]+'}'
    if lt<len(verse[ln])-1: phonemes+='\ipa\char"2E'
    elif ln<len(verse)-1: phonemes+='}\\vskip 1.4em\n'
with open(sys.argv[1]+'.tex','w') as temp:
  temp.write('\\font\ipa=tipa17 scaled \magstep3 \\font\\acc=tipa17\n')
  for u,h in accents.items(): temp.write('\def\\'+u+'#1{{\\acc\\accent"'+h+' #1}}'+'\n')
  temp.write('\\null\\vfill\n'+phonemes+'}\\bye')
os.system('pdftex '+sys.argv[1]+'.tex')