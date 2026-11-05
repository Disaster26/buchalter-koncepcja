# python _src/kafle.py plik.png [wys_segmentu] -> plik_k.png (segmenty obok siebie)
import sys
from PIL import Image
p=sys.argv[1]; seg=int(sys.argv[2]) if len(sys.argv)>2 else 1700
im=Image.open(p); w,h=im.size; n=(h+seg-1)//seg
c=Image.new('RGB',(n*(w+20),seg),'#ff00ff')
for i in range(n):
    c.paste(im.crop((0,i*seg,w,min(h,(i+1)*seg))),(i*(w+20),0))
c.save(p.replace('.png','_k.png'))
print(n)
