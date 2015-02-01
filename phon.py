#!/usr/bin/env python
import sys,os,random,ast
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'EC','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF','w':'77'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
suprasegmentals={':':'3A',';':'3B','rh':'7E'}
accents={'u':'08','thh':'05','th':'01','tm':'09','tl':'00','tll':'0D'}
morphing={'l','r','m','n','N'}
glides={'h','j','w'}
rhymes={}
C=set()
V=set()
with open(sys.argv[1]) as source: phrase,verse=ast.literal_eval(source.readline())
cypher=phrase.split(' ')
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
log=''
for ln in range(len(verse)):
  phonemes+='\centerline{'
  for lt in range(len(verse[ln])):
    if verse[ln][lt]!='-' and verse[ln][lt] in rhymes.keys(): rule=random.choice([rl for rl in set(rules.split('.')) if str('v'*len(rhymes[verse[ln][lt]])) in rl])
    elif verse[ln][lt]==' ':
      phonemes+='}\\vskip 1em\n\n'
      break
    else: rule=random.sample(set(rules.split('.')),1)[0]
    ct=set(C)
    vt=set(V)
    pr=''
    log+='line '+str(ln)+', syllable '+str(lt)+'\nrule = '+rule+'\n'
    for d in range(len(rule)):
      if rule[d]=='c':
        if d+1<len(rule) and rule[d+1]=='c':
          pre=[ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in ct and cypher[ph[0]+1] in ct]
          if d==0:
            log+='\nfirst C & first C from C+C pairs: '+str(pre)
            con=random.choice([pc for pc in pre if pc not in morphing])
          else:
            log+='\nfirst C from C+C pairs: '+str(pre)
            con=random.choice([pc for pc in pre if pc not in glides])
        elif pr in C:
          try:
            pre=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in ct]
            log+='\nsecond C from '+pr+'+C pairs: '+str(pre)
            if d<len(rule)-1: con=random.choice(pre)
            else: con=random.choice([pc for pc in pre if pc not in morphing])
          except IndexError: con=''
        elif d!=0:
          try:
            pre=[ph[1] for ph in enumerate(cypher) if ph[1] in ct-glides and cypher[ph[0]-1]==pr]
            log+='\nC from '+pr+'+C pairs: '+str(pre)
            con=random.choice(pre)
          except IndexError: con=random.choice([pc for pc in ct if pc not in glides])
        else: con=random.choice([pc for pc in ct if pc not in morphing])
        pr=con
        if con in ct: ct.remove(con)
      else:
        if d+1<len(rule) and rule[d+1]=='v':
          pre=[ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in vt and cypher[ph[0]+1] in vt]
          if verse[ln][lt]!='-':
            if verse[ln][lt] not in rhymes.keys(): rhymes[verse[ln][lt]]=[random.choice(pre)]
            vow=rhymes[verse[ln][lt]][0]
          else:
            log+='\nfirst V from V+V pairs: '+str(pre)
            vow=random.choice(pre)
        elif pr in V:
          try:
            pre=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in vt]
            log+='\nsecond V from '+pr+'+V pairs: '+str(pre)
            if verse[ln][lt]!='-':
              if len(rhymes[verse[ln][lt]])==1: rhymes[verse[ln][lt]].append(random.choice(pre))
              vow=rhymes[verse[ln][lt]][1]
            else: vow=random.choice(pre)
          except IndexError: vow=''
        elif verse[ln][lt]!='-':
          if verse[ln][lt] not in rhymes.keys():
            try: rhymes[verse[ln][lt]]=[random.choice([cc[1] for cc in enumerate(cypher) if cc[1] in vt and cypher[cc[0]-1]==pr])]
            except IndexError: rhymes[verse[ln][lt]]=[random.choice(list(vt))]
          vow=rhymes[verse[ln][lt]][0]
        else:
          try:
            pre=[cc[1] for cc in enumerate(cypher) if cc[1] in vt and cypher[cc[0]-1]==pr]
            vow=random.choice(pre)
            log+='\nV from '+pr+'+V pairs: '+str(pre)
          except IndexError: vow=random.choice(list(vt))
        pr=vow
        if vow in vt: vt.remove(vow)
      log+='\nchoice: '+pr
      if pr!='':
        if '/' not in pr: phonemes+='\ipa\char"'+dict(consonants.items()+vowels.items())[pr]
        else:
          va=pr.split('/')
          if va[1] in suprasegmentals.keys(): phonemes+='\ipa\char"'+vowels[va[0]]+'\ipa\char"'+suprasegmentals[va[1]]
          elif va[1] in accents.keys(): phonemes+='\\'+va[1]+'{\ipa\char"'+vowels[va[0]]+'}'
    log+='\n\n'
    if lt<len(verse[ln])-1: phonemes+='\ipa\char"2E'
    elif ln<len(verse)-1: phonemes+='}\\\n\n'
with open(sys.argv[1]+'.tex','w') as temp:
  temp.write('\\font\ipa=tipa17 scaled \magstep3 \\font\\acc=tipa17\n')
  for u,h in accents.items(): temp.write('\def\\'+u+'#1{{\\acc\\accent"'+h+' #1}}'+'\n')
  temp.write('\\null\\vfill\n'+phonemes+'}\\bye')
with open('log','w') as lg: lg.write(log)
os.system('pdftex '+sys.argv[1]+'.tex')