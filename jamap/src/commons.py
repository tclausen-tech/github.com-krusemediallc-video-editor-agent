"""Busca fotos no Wikimedia Commons e gera folha de contato para escolha.
uso: python3 commons.py "<termo>" <pasta_saida> [n]"""
import json, sys, os, time, urllib.request, urllib.parse
from PIL import Image, ImageDraw
UA = {"User-Agent": "jamap-video-editor/1.0 (https://github.com/tclausen-tech/github.com-krusemediallc-video-editor-agent) python-urllib"}

def get(url, tries=5):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            time.sleep(3 * (k + 1))

def search(q, n=12):
    if q.startswith("cat:"):  # membros de uma categoria
        p = dict(action="query", format="json", generator="categorymembers", gcmtitle="Category:" + q[4:],
                 gcmtype="file", gcmlimit=n, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=960)
    else:
        p = dict(action="query", format="json", generator="search", gsrsearch=f"{q} filetype:bitmap",
                 gsrnamespace=6, gsrlimit=n, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=960)
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
    out = []
    for pg in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0)):
        ii = pg["imageinfo"][0]; md = ii.get("extmetadata", {})
        out.append(dict(title=pg["title"], thumb=ii["thumburl"], w=ii["width"], h=ii["height"],
                        lic=md.get("LicenseShortName", {}).get("value", ""),
                        artist=md.get("Artist", {}).get("value", "")))
    return out

if __name__ == "__main__":
    q, od = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    os.makedirs(od, exist_ok=True)
    res = search(q, n); sheet = Image.new("RGB", (4 * 300, 3 * 260), "white"); dr = ImageDraw.Draw(sheet)
    for i, r in enumerate(res[:12]):
        fn = os.path.join(od, f"{i:02d}.jpg")
        try:
            time.sleep(1.5)
            open(fn, "wb").write(get(r["thumb"]))
            im = Image.open(fn).convert("RGB"); im.thumbnail((290, 230))
            sheet.paste(im, ((i % 4) * 300 + 5, (i // 4) * 260 + 5))
        except Exception as e:
            r["err"] = str(e)
        dr.text(((i % 4) * 300 + 5, (i // 4) * 260 + 238), f"{i} {r['lic'][:20]} {r['w']}x{r['h']}", fill="black")
    sheet.save(os.path.join(od, "sheet.png"))
    json.dump(res, open(os.path.join(od, "meta.json"), "w"), ensure_ascii=False, indent=1)
    for i, r in enumerate(res): print(i, r["title"][:70], r["lic"], r.get("err", ""))
