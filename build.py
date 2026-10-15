import re,json,html,urllib.request
B="https://eldiarioabierto.sites.tab.bot/newsletter/"
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"curl/8"}),timeout=30).read().decode()
def parse(h):
  out={}
  for a in re.findall(r'<article class="card[^"]*" id="no-(\d+)">(.*?)</article>',h,re.S):
    n,b=int(a[0]),a[1]
    t=lambda p: html.unescape(re.sub('<[^>]+>','',re.search(p,b,re.S).group(1))).strip()
    out[n]=dict(fecha=re.search(r'datetime="([^"]+)"',b).group(1),fecha_texto=t(r'<time[^>]*>(.*?)</time>'),
      titulo=t(r'<h3>(.*?)</h3>'),resumen=t(r'<p class="sum">(.*?)</p>'),
      temas=[html.unescape(x).strip() for x in re.findall(r'<li>(.*?)</li>',b)],
      id=(re.search(r'/file/d/([^/]+)/',b) or [None,None])[1],
      pdf=(lambda h: None if "drive.google.com" in h else h)(re.search(r'class="btn pdf" href="([^"]+)"',b).group(1)))
  return out
es,en=parse(get(B)),parse(get(B+"en/"))
eds=[]
for n in sorted(set(es)|set(en),reverse=True):
  e,g=es.get(n,{}),en.get(n,{})
  eds.append({"numero":n,"fecha":e.get("fecha") or g.get("fecha"),
   "titulo":{"es":e.get("titulo"),"en":g.get("titulo")},"resumen":{"es":e.get("resumen"),"en":g.get("resumen")},
   "temas":{"es":e.get("temas",[]),"en":g.get("temas",[])},"fecha_texto":{"es":e.get("fecha_texto"),"en":g.get("fecha_texto")},
   "es":e.get("id"),"en":g.get("id")})
  pu={k:v for k,v in (("es",e.get("pdf")),("en",g.get("pdf"))) if v}
  if pu: eds[-1]["pdf_url"]=pu
json.dump({"newsletter":"El Diario Abierto","archivo":B,"ediciones":eds},open("newsletter.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(eds),[ (x["numero"],x["fecha"],x["es"],x["en"]) for x in eds])
