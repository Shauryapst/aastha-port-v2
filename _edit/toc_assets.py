"""Cuts the seven contents-page stamps out of page 3 (img/xl/03.webp) into img/toc/.
Run from the repo root:  python3 _edit/toc_assets.py"""
import numpy as np, cv2, pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parents[1]
a = np.array(Image.open(R / "img/xl/03.webp").convert("RGB"))
boxes = [(1263,223,525,525),(2001,224,506,506),(2742,224,516,516),(3482,224,507,507),(1272,939,515,516),(2004,939,517,516),(2743,940,514,514)]
names = ["unbuilt","fables","saandra","seed","roundup","kargha","baandh"]
(R / "img/toc").mkdir(exist_ok=True)
masks = {}
for (x,y,w,h),nm in zip(boxes,names):
    p=14; c=a[y-p:y+h+p, x-p:x+w+p]
    hsv=cv2.cvtColor(c,cv2.COLOR_RGB2HSV)
    m=((hsv[...,1]>40)|(hsv[...,2]<120)).astype(np.uint8)*255
    n,lab,st,_=cv2.connectedComponentsWithStats(m); k=1+int(np.argmax(st[1:,4])); m=(lab==k).astype(np.uint8)*255
    ff=m.copy(); H,W=m.shape; cv2.floodFill(ff,np.zeros((H+2,W+2),np.uint8),(0,0),255); m=m|(~ff&255)
    m=cv2.GaussianBlur(m,(3,3),0)
    im=Image.fromarray(np.dstack([c,m])).resize((420,420),Image.LANCZOS); masks[nm]=im
for nm,im in masks.items():
    if nm=="baandh":            # cream stamp on cream paper: borrow the perforated outline of another stamp
        arr=np.array(im); arr[...,3]=np.array(masks["saandra"])[...,3]; im=Image.fromarray(arr)
    im.save(R / f"img/toc/{nm}.webp", quality=88, method=5)
print("stamps written")
