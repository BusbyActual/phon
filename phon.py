#!/usr/bin/env python
import sys,random
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'EC','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF','w':'77'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
with open(sys.argv[1]) as source: verse=map(lambda x: x.rstrip().split(' '), source.readlines())
syllables=' '.join([' '.join(s) for s in verse]).split(' ')
t=str(len(syllables))
match=False
lit=[]
while True:
  phonemes='\\null\\vfill'
  n=[]
  count=0
  for ln in range(len(verse)):
    phonemes+=''
    for sn in range(len(verse[ln])):
      if sn>0: phonemes+='\ipa\char"2E'
      syll=[]
      phon=''
      while len(syll)<len(verse[ln][sn]):
        if verse[ln][sn][len(syll)] in consonants.keys():
          if len(syll)==0: pre=[ph[0] for ph in ' '.join([' '.join(s) for s in verse]).split(' ') if ph[0] in consonants.keys()]
          elif phon!='': pre=[ph[ph.index(phon)+1] for ph in ' '.join([' '.join(s) for s in verse]).split(' ') if phon in ph and ph.index(phon)+1<len(ph)-1 and ph[ph.index(phon)+1] in consonants.keys()] if len(syll)+1!=len(verse[ln][sn]) else [ph[ph.index(phon)+1] for ph in ' '.join([' '.join(s) for s in verse]).split(' ') if phon in ph and ph.index(phon)+1==len(ph)-1 and ph[ph.index(phon)+1] in consonants.keys()]
        elif verse[ln][sn][len(syll)] in vowels.keys():
          if len(syll)==0: pre=[ph[0] for ph in ' '.join([' '.join(s) for s in verse]).split(' ') if ph[0] in vowels.keys()]
          elif phon!='': pre=[ph[ph.index(phon)+1] for ph in ' '.join([' '.join(s) for s in verse]).split(' ') if phon in ph and ph.index(phon)+1<len(ph)-1 and ph[ph.index(phon)+1] in vowels.keys()] if len(syll)+1!=len(verse[ln][sn]) else [ph[ph.index(phon)+1] for ph in ' '.join([' '.join(s) for s in verse]).split(' ') if phon in ph and ph.index(phon)+1==len(ph)-1 and ph[ph.index(phon)+1] in vowels.keys()]
        try:
          phon=random.choice(pre)
          syll.append(phon)
        except IndexError:
          phon=''
          syll=[]
        sb=''.join(syll)
        if sb in syllables and count!=' '.join([' '.join(s) for s in verse]).split(' ').index(sb): syll=[]
      count+=1
      if sb not in syllables and sb in ' '.join([' '.join(s) for s in verse]).split(' '): syll=[]
      if len(syllables)>0 and sb in syllables: phonemes+='\pdfcolorstack\match push{1 0 0 rg}'
      if len(syll)>0:
        for s in syll: phonemes+='\ipa\char"'+dict(consonants.items()+vowels.items())[s]
      else: phonemes+='\ipa\char"5B'+'\quad'*len(sb)+'\ipa\char"5D'
      if len(syllables)>0 and sb in syllables:
        phonemes+='\pdfcolorstack\match pop{}'
        n.append(str(' '.join([' '.join(s) for s in verse]).split(' ').index(syllables.pop(syllables.index(sb)))+1))
        match=True
    phonemes+='\\bigskip'
  if match==True:
    match=False
    lit.append(phonemes+'\\vfill\\footline={\hfill\\tenrm\it '+','.join(n)+' / '+t+'}')
  elif len(syllables)==0: break
with open(sys.argv[1]+'.tex','w') as temp: temp.write('\pdfcompresslevel=0\chardef\match=\pdfcolorstackinit page direct{0 g}\\nopagenumbers\\font\ipa=tipa17\pdfpagewidth 216 true mm\pdfpageheight 356 true mm\pdfhorigin 25.4 true mm\pdfvorigin 25.4 true mm\hsize 165.2 true mm\\vsize 305.2 true mm\n'+'\eject'.join(lit)+'\\bye')