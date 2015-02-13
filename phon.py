#!/usr/bin/env python
import sys,os,random,time
consonants={'p':'70','t':'74',':t':'FA','c':'63','k':'6B','q':'71','P':'50','b':'62','d':'64',':d':'E3','textbardotlessj':'E9','g':'67',';G':'E5','m':'6D','M':'4D','n':'6E',':n':'EF','textltailn':'F1','N':'4E',';N':'F0',';B':'E0','r':'72',';R':'F6','R':'52',':r':'F3','F':'46','f':'66','T':'54','s':'73','S':'53',':s':'F9',':c':'E7','x':'78','X':'58','textcrh':'E8','h':'68','B':'42','v':'76','D':'44','z':'7A','Z':'5A','J':'4A','G':'47','K':'43','Q':'51','H':'48','textbeltl':'Eself.C','textlyoghlig':'D0','V':'56','*r':'F4',':R':'F5','j':'6A','textturnmrleg':'EE','l':'6C',':l':'ED','L':'4C',';L':'CF','w':'77'}
vowels={'i':'69','y':'79','1':'31','O':'30','W':'57','u':'75','I':'49','Y':'59','U':'55','e':'65',':o':'F8','9':'39','8':'38','7':'37','o':'6F','@':'40','E':'45','oe':'F7','3':'33','textcloseepsilon':'C5','2':'32','0':'4F','5':'35','ae':'E6','OE':'D7','a':'61','A':'41','6':'36'}
suprasegmentals={':':'3A',';':'3B','rh':'7E'}
morphing={'l','r','m','n','N'}
glides={'h','j','w'}

class page:
  
  def __init__(self):
    with open(sys.argv[1]) as source:
      lines=map(lambda x: x.rstrip(), source.readlines())
      self.cypher=' . '.join(lines).split(' ')
      self.sylbs=set(''.join(self.cypher).split('.'))
      self.verse=map(lambda x: ''.join([y for y in x if y!=' ']).split('.'), lines)

    
    self.rules=''
    self.C=set()
    self.V=set()
    self.matching=set()
    
    for c in self.cypher:
      if c in consonants.keys():
        self.C.add(c)
        self.rules+='c'
      elif c=='.': self.rules+=c
      else:
        self.V.add(c)
        self.rules+='v'
    
  
  def compose(self):

    syllables=[]
    rhymes={}
    phonemes='\\null\\vfill\n'
    f=0
    
    for ln in range(len(self.verse)):
      
      phonemes+='\centerline{'
      
      for lt in range(len(self.verse[ln])):
        
        if lt>0: phonemes+='\ipa\char"2E'
        
        nucleus=''.join([ph for ph in self.verse[ln][lt] if ph not in self.C])
        if nucleus in rhymes.keys(): rule=random.choice([rl for rl in set(self.rules.split('.')) if len(rhymes[nucleus])==len([pt for pt in rl if pt=='v'])])
        else: rule=random.sample(set(self.rules.split('.')),1)[0]
        
        pr=''
        syll=[]
        
        while len(syll)<len(rule):
          
          if rule[len(syll)]=='c':
            
            if len(syll)+1<len(rule) and rule[len(syll)+1]=='c':
              pre=[ph[1] for ph in enumerate(self.cypher) if ph[0]+1<len(self.cypher) and ph[1] in self.C and self.cypher[ph[0]+1] in self.C]
              if len(syll)>0: con=randpm.choice([ph for ph in pre if ph not in glides])
              else: con=random.choice(pre)
              
            elif pr in self.C:
              try:
                pre=[self.cypher[ph[0]+1] for ph in enumerate(self.cypher) if ph[1]==pr and ph[0]+1<len(self.cypher) and self.cypher[ph[0]+1] in self.C]
                con=random.choice(pre) if len(syll)<len(rule)-1 else random.choice([ph for ph in pre if ph not in morphing])
              except IndexError: con=''
              
            elif len(syll)!=0:
              try:
                pre=[ph[1] for ph in enumerate(self.cypher) if ph[1] in self.C-glides and self.cypher[ph[0]-1]==pr]
                con=random.choice([p for p in pre if p not in syll])
              except IndexError: con=random.choice([ph for ph in self.C if ph not in glides and ph not in syll])
              
            else: con=random.choice([ph for ph in self.C if ph not in morphing and ph not in syll])
            
            pr=con
            
          else:
            
            if len(syll)+1<len(rule) and rule[len(syll)+1]=='v':
              pre=[ph[1] for ph in enumerate(self.cypher) if ph[0]+1<len(self.cypher) and ph[1] in self.V and self.cypher[ph[0]+1] in self.V]
              if nucleus not in rhymes.keys(): rhymes[nucleus]=[random.choice([p for p in pre if p not in syll])]
              vow=rhymes[nucleus][0]
              
            elif pr in self.V:
              try:
                pre=[self.cypher[ph[0]+1] for ph in enumerate(self.cypher) if ph[1]==pr and ph[0]+1<len(self.cypher) and self.cypher[ph[0]+1] in self.V]
                if len(rhymes[nucleus])==1: rhymes[nucleus].append(random.choice([p for p in pre if p not in syll]))
                vow=rhymes[nucleus][1]
              except IndexError: vow=''
              
            else:
              if nucleus not in rhymes.keys():
                try: rhymes[nucleus]=[random.choice([cc[1] for cc in enumerate(self.cypher) if cc[1] in self.V and self.cypher[cc[0]-1]==pr])]
                except IndexError: rhymes[nucleus]=random.sample(self.V,1)[0]
              vow=rhymes[nucleus][0]
              
            pr=vow

          if pr!='': syll.append(pr)
            
        sb=''.join(syll)
        syllables.append(sb)

        if sb in self.sylbs:
          phonemes+='\pdfcolorstack\match push{1 0 0 rg}'
          self.matching.add(sb)
        
        for s in range(len(syll)):
          if '/' not in syll[s]: phonemes+='\ipa\char"'+dict(consonants.items()+vowels.items())[syll[s]]
          else:
            va=syll[s].split('/')
            if va[1] in suprasegmentals.keys(): phonemes+='\ipa\char"'+vowels[va[0]]+'\ipa\char"'+suprasegmentals[va[1]]
        
        if sb in self.sylbs: phonemes+='\pdfcolorstack\match pop{}'
        
      if ln<len(self.verse)-1: phonemes+='}\\bigskip\n'
        
    if len([s for s in syllables if s in self.sylbs])>0: return phonemes+'}\n\\vfill\eject\n'
    else: return ''

pg=page()

def main():
  
  temp=open(sys.argv[1]+'.tex','w')
  temp.write('\\footline={\\tenrm\it '+time.strftime("%d.%m.%y")+'\hfill\\folio\hfill'+time.strftime("%H.%M.%S")+'}\chardef\match=\pdfcolorstackinit page direct{0 g} \\font\ipa=tipa17 \pdfpagewidth 5.5in \pdfpageheight 8.5in \hsize 4.5in \\vsize 7in \hoffset -0.5in \\voffset -0.375in\n')
  
  while pg.matching!=pg.sylbs:
    temp.write(pg.compose())
  
  temp.write('\\bye')
  temp.close()
  os.system('pdftex '+sys.argv[1]+'.tex')

main()