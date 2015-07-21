#!/usr/bin/env python
import sys,random
consonants=['142','144','147','153','154','155','156','162','172']
vowels=['063','100','105','111','117','125','141','145']
with open(sys.argv[1]) as source: verse=map(lambda x: x.rstrip().split(' '), source.readlines())
origin=' '.join([' '.join(s) for s in verse]).split(' ')
octals=[[o[i:i+3] for i in range(0,len(o),3)] for o in origin]
syllables=list(enumerate(origin,start=1))
match=False
lit=[]
while True:
  phonemes='\\null\\vfill'
  n=[]
  count=1
  for ln in range(len(verse)):
    phonemes+=''
    for sn in range(len(verse[ln])):
      if sn>0: phonemes+='\ipa\char"2E'
      syll=[]
      phon=''
      source=[verse[ln][sn][i:i+3] for i in range(0,len(verse[ln][sn]),3)]
      while len(syll)<len(source):
        if source[len(syll)] in consonants:
          if len(syll)==0: pre=[ph[0] for ph in octals if ph[0] in consonants]
          elif phon!='': pre=[ph[ph.index(phon)+1] for ph in octals if phon in ph and len(ph)-1>ph.index(phon) and ph[ph.index(phon)+1] in consonants] if len(syll)+1!=len(source) else [ph[ph.index(phon)+1] for ph in octals if phon in ph and ph.index(phon)+1==len(ph)-1 and ph[ph.index(phon)+1] in consonants]
        elif source[len(syll)] in vowels:
          if len(syll)==0: pre=[ph[0] for ph in octals if ph[0] in vowels]
          elif phon!='': pre=[ph[ph.index(phon)+1] for ph in octals if phon in ph and len(ph)-1>ph.index(phon) and ph[ph.index(phon)+1] in vowels] if len(syll)+1!=len(source) else [ph[ph.index(phon)+1] for ph in octals if phon in ph and ph.index(phon)+1==len(ph)-1 and ph[ph.index(phon)+1] in vowels]
        try:
          phon=random.choice(pre)
          syll.append(phon)
        except IndexError:
          phon=''
          syll=[]
        if len(syll)==len(source):
          sb=''.join(syll)
          if sb in [s[1] for s in syllables] and len([s for s in syllables if s[0]==count and s[1]==sb])==0: syll=[]
      if sb not in [s[1] for s in syllables] and sb in origin or sb in [s[1] for s in syllables] and match==True: syll=[]
      if sb in [s[1] for s in syllables] and match==False: phonemes+='\pdfcolorstack\match push{1 0 0 rg}'
      if len(syll)>0:
        for s in syll: phonemes+="\ipa\char'"+s
      else: phonemes+='\enskip'*len(sb)
      if sb in [s[1] for s in syllables] and match==False:
        phonemes+='\pdfcolorstack\match pop{}'
        n.append(syllables.pop(syllables.index((count,sb)))[0])
        match=True
      count+=1
    phonemes+='\\bigskip'
  if match==True:
    match=False
    lit.append(phonemes+'\\vfill\\footline={\hfill\\tenrm\it '+','.join(map(str,n))+' / '+str(len(origin))+'}\eject')
  elif len(syllables)==0: break
with open(sys.argv[1]+'.tex','w') as temp: temp.write('\pdfcompresslevel=0\chardef\match=\pdfcolorstackinit page direct{0 g}\\nopagenumbers\\font\ipa=tipa17\pdfpagewidth 216 true mm\pdfpageheight 356 true mm\pdfhorigin 25.4 true mm\pdfvorigin 25.4 true mm\hsize 165.2 true mm\\vsize 305.2 true mm\n'+'\n'.join(lit)+'\\bye')