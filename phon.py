#!/usr/bin/env python
import sys,os,random,time
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'EC','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF','w':'77'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
suprasegmentals={':':'3A',';':'3B','rh':'7E'}
morphing={'l','r','m','n','N'}
glides={'h','j','w'}
with open(sys.argv[1]) as source: lines=map(lambda x: x.rstrip(), source.readlines())
cypher=' . '.join(lines).split(' ')
sylbs=set(''.join(cypher).split('.'))
verse=map(lambda x: ''.join([y for y in x if y!=' ']).split('.'), lines)
rules=''
C=set()
V=set()
matching=set()
lit=['\pdfcompresslevel=0\chardef\match=\pdfcolorstackinit page direct{0 g}\\nopagenumbers\\font\ipa=tipa12\\font\\title=cmr17\pdfpagewidth 210mm\pdfpageheight 148mm\pdfhorigin 12mm\pdfvorigin 16mm\hsize 162mm\\vsize 100mm\n']
for c in cypher:
  if c in consonants.keys():
    C.add(c)
    rules+='c'
  elif c=='.': rules+=c
  else:
    V.add(c)
    rules+='v'
while matching!=set(''.join(cypher).split('.')):
  syllables=[]
  rhymes={}
  phonemes='\hbox to 186mm{\hsize=81mm' if len(lit)%2!=0 else ''
  phonemes+='\\vbox to 100mm{\\vfill'
  for ln in range(len(verse)):
    for lt in range(len(verse[ln])):
      if lt>0: phonemes+='\ipa\char"2E'
      nucleus=''.join([p for p in verse[ln][lt] if p not in consonants.keys()])
      if nucleus in rhymes.keys(): rule=random.choice([pt for pt in set(rules.split('.')) if 'v'*len(rhymes[nucleus]) in pt])
      else: rule=random.sample(set(rules.split('.')),1)[0]
      pr=''
      syll=[]
      ct=set(C)
      vt=set(V)
      while len(syll)<len(rule):
        if rule[len(syll)]=='c':
          if len(syll)+1<len(rule) and rule[len(syll)+1]=='c':
            if pr in C:
              try: con=random.choice([ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in ct and cypher[ph[0]+1]=='r'])
              except IndexError: con=''
            else:
              pre=[ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in ct and cypher[ph[0]+1] in ct]
              if len(syll)>0: con=random.choice([ph for ph in pre if ph not in glides])
              else: con=random.choice([ph for ph in pre if ph not in morphing])
          elif pr in C:
            try:
              pre=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1]==pr and cypher[ph[0]+1] in ct]
              if len(syll)+1!=len(rule): con=random.choice(pre)
              else: con=random.choice([ph for ph in pre if ph not in morphing])
            except IndexError: con=''
          else:
            try:
              pre=[ph[1] for ph in enumerate(cypher) if ph[1] in ct-glides and cypher[ph[0]-1]==pr]
              con=random.choice(pre)
            except IndexError: con=random.sample(ct-glides,1)[0] if len(syll)>0 else random.choice([ph for ph in ct if ph!='N'])
          pr=con
          if con in ct: ct.remove(con)
        else:
          if len(syll)+1<len(rule) and rule[len(syll)+1]=='v':
            pre=[ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in vt and cypher[ph[0]+1] in vt]
            if nucleus not in rhymes.keys(): rhymes[nucleus]=[random.choice(pre)]
            vow=rhymes[nucleus][0]
          elif pr in V:
            try:
              pre=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in vt]
              if len(rhymes[nucleus])<2: rhymes[nucleus].append(random.choice(pre))
              vow=rhymes[nucleus][1]
            except IndexError: vow=''
          else:
            if nucleus not in rhymes.keys():
              try: rhymes[nucleus]=[random.choice([ph[1] for ph in enumerate(cypher) if ph[1] in vt and cypher[ph[0]-1]==pr])]
              except IndexError: rhymes[nucleus]=[random.sample(vt,1)[0]]
            vow=rhymes[nucleus][0]
          pr=vow
          if vow in vt: vt.remove(vow)
        syll.append(pr)
      sb=''.join(syll)
      syllables.append(sb)
      if sb in sylbs and sb not in matching: phonemes+='\pdfcolorstack\match push{1 0 0 rg}'
      for s in [s for s in syll if s!='']:
        if '/' not in s: phonemes+='\ipa\char"'+dict(consonants.items()+vowels.items())[s]
        else:
          va=s.split('/')
          if va[1] in suprasegmentals.keys(): phonemes+='\ipa\char"'+vowels[va[0]]+'\ipa\char"'+suprasegmentals[va[1]]
      if sb in sylbs and sb not in matching:
        phonemes+='\pdfcolorstack\match pop{}'
        matching.add(sb)
    if ln<len(verse)-1: phonemes+='\medskip'
  if len([s for s in syllables if s in sylbs])>0:
    sylbs-=matching
    if len(lit)%2!=0: lit.append(phonemes+'\\vfill}\hfill')
    else: lit.append(phonemes+'\\vfill}}\eject\n')
if len(lit)%2==0: lit.append('}\eject\n')
with open(sys.argv[1]+'.tex','w') as temp: temp.write(''.join(lit)+'\\bye')
os.system('pdftex '+sys.argv[1]+'.tex')