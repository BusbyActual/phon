#!/usr/bin/env python
import sys,os,random,time
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'Eself.C','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF','w':'77'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
suprasegmentals={':':'3A',';':'3B','rh':'7E'}
morphing={'l','r','m','n','N'}
glides={'h','j','w'}

class page:
  
  def __init__(self):
    with open(sys.argv[1]) as source: self.lines=map(lambda x: x.rstrip(), source.readlines())
  
    self.cypher=' . '.join(lines).split(' ')
    self.sylbs=set(''.join(cypher).split('.'))
    self.verse=map(lambda x: ''.join([y for y in x if y!=' ']).split('.'), lines)
    
  def setup(self):
    
    self.rhymes={}
    self.phonemes='\\null\\vfill\n'
    self.rules=''
    
    self.C=set()
    self.V=set()
    
    for c in self.cypher:
      if c in self.consonants.keys():
        self.C.add(c)
        self.rules+='c'
      elif c=='.': self.rules+=c
      else:
        self.V.add(c)
        self.rules+='v'
    
  
  def compose(self):
    
    setup()
    
    for ln in range(len(self.verse)):
      
      self.phonemes+='\centerline{'
      
      for lt in range(len(self.verse[ln])):
        
        nucleus=''.join([ph for ph in self.verse[ln][lt] if ph not in self.C])
        if nucleus in self.rhymes.keys(): rule=random.choice([rl for rl in set(self.rules.split('.')) if len(self.rhymes[nucleus])==len([pt for pt in rl if pt=='v'])])
        else: rule=random.sample(set(self.rules.split('.')),1)[0]
        
        pr=''
        syll=[]
        
        for d in range(len(rule)):
          
          if rule[d]=='c':
            if d+1<len(rule) and rule[d+1]=='c':
              
              pre=[ph[1] for ph in enumerate(self.cypher) if ph[0]+1<len(self.cypher) and ph[1] in self.C and self.cypher[ph[0]+1] in self.C]
              con = randpm.choice([ph for ph in [p for p in pre if p not in syll] and ph not in glides if d>0 else morphing])
              
              #if d==0:
              #  con=random.choice([pc for pc in pre if pc not in morphing]) # will be glides if d>0 otherwise morphing
              #else: con=random.choice([pc for pc in pre if pc not in glides])
              
            elif pr in self.C:
              try:
                pre=[cypher[ph[0]+1] for ph in enumerate(self.cypher) if ph[1]==pr and ph[0]+1<len(self.cypher) and self.cypher[ph[0]+1] in self.C]
                con=random.choice(pre) if d<len(rule)-1 else random.choice([ph for ph in [p for p in pre if p not in syll] if ph not in morphing])
              except IndexError: con=''
              
            elif d!=0:
              try:
                pre=[ph[1] for ph in enumerate(self.cypher) if ph[1] in self.C-glides and self.cypher[ph[0]-1]==pr]
                con=random.choice([p for p in pre if p not in syll])
              except IndexError: con=random.choice([ph for ph in self.C if ph not in glides and ph not in syll])
              
            else: con=random.choice([ph for ph in self.C if ph not in morphing and ph not in syll])
            
            pr=con
            
          else:
            if d+1<len(rule) and rule[d+1]=='v':
              pre=[ph[1] for ph in enumerate(cypher) if ph[0]+1<len(cypher) and ph[1] in self.V and cypher[ph[0]+1] in self.V]
              if core not in rhymes.keys(): rhymes[core]=[random.choice(pre)]
              vow=rhymes[core][0]
            elif pr in self.V:
              try:
                pre=[cypher[ph[0]+1] for ph in enumerate(cypher) if ph[1]==pr and ph[0]+1<len(cypher) and cypher[ph[0]+1] in self.V]
                if len(rhymes[core])==1: rhymes[core].append(random.choice(pre))
                vow=rhymes[core][1]
              except IndexError: vow=''
            else:
              if core not in rhymes.keys():
                try: rhymes[core]=[random.choice([cc[1] for cc in enumerate(cypher) if cc[1] in self.V and cypher[cc[0]-1]==pr])]
                except IndexError: rhymes[core]=[random.choice(list(self.V))]
              vow=rhymes[core][0]
            pr=vow
          if pr!='': syll.append(pr)
        sb=''.join(syll)
        if sb in sylbs:
          phonemes+='\pdfcolorstack\match push{1 0 0 rg}'
          matching.add(sb)
          print(str(_m))
        for phon in syll:
          if '/' not in phon: phonemes+='\ipa\char"'+dict(consonants.items()+vowels.items())[phon]
          else:
            va=phon.split('/')
            if va[1] in suprasegmentals.keys(): phonemes+='\ipa\char"'+vowels[va[0]]+'\ipa\char"'+suprasegmentals[va[1]]
        if sb in sylbs: phonemes+='\pdfcolorstack\match pop{}'
        if lt<len(verse[ln])-1: phonemes+='\ipa\char"2E'
        elif ln<len(verse)-1: phonemes+='}\\bigskip\n'
    if len(matching)>_m:
      temp.write(phonemes+'}\n\\vfill\eject\n')
      _m=len(matching)
  

pg=page()

def main():
  
  temp=open(sys.argv[1]+'.tex','w')
  temp.write('\\footline={\\tenrm\it \hfill\\folio\hfill}\chardef\match=\pdfcolorstackinit page direct{0 g} \\font\ipa=tipa17 \pdfpagewidth 5.5in \pdfpageheight 8.5in \hsize 4.5in \\vsize 7in \hoffset -0.5in \\voffset -0.375in\n')

  matching=set()
  
  print(str(len(matching))+' '+str(len(pg.sylbs)))
  
  while True:
    if len(matching-pg.sylbs)>0:
      pg.compose()
    else: break
  
  temp.write('\\bye')
  temp.close()
  os.system('pdftex '+sys.argv[1]+'.tex')

main()