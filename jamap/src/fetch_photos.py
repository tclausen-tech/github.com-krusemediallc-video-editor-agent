"""Baixa as fotos escolhidas (originais do Wikimedia Commons) e registra créditos.
uso: python3 fetch_photos.py <pasta_candidatos>"""
import json, os, sys, time, re, urllib.request, urllib.parse
UA = {"User-Agent": "jamap-video-editor/1.0 (https://github.com/tclausen-tech/github.com-krusemediallc-video-editor-agent) python-urllib"}
PICK = {  # nome -> (pasta de busca, índice)
    "escritorio": ("office", 3), "loja": ("c_shop", 0), "lojista": ("c_shop", 3),
    "papelada": ("c_paper", 10), "assinatura": ("c_paper", 11), "calculadora": ("calc2", 11),
    "martelo": ("gavel", 0), "notebook": ("meeting2", 0), "datacenter": ("dc2", 1),
    "esplanada": ("brasilia", 6), "ministerio": ("brasilia", 3)
}
cand = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "..", "assets", "photos"); credits = []
for name, (d, i) in PICK.items():
    m = json.load(open(os.path.join(cand, d, "meta.json")))[i]
    url = m["thumb"].split("?")[0].replace("thumb.wikimedia.org", "upload.wikimedia.org")
    base, last = url.rsplit("/", 1)  # miniatura padrão de 1920 px (originais caem em 429)
    url = base + "/1920px-" + last.split("px-", 1)[1]
    fn = os.path.join(out, name + ".jpg")
    if not os.path.exists(fn):
        for k in range(4):
            try:
                data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
                assert data[:2] == b"\xff\xd8", "não é JPEG"
                open(fn, "wb").write(data); break
                open(fn, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()); break
            except Exception as e:
                print("retry", name, e); time.sleep(20 * (k + 1))
        time.sleep(10)
    artist = re.sub("<[^>]+>", "", m["artist"]).strip()
    credits.append(f"- {name}.jpg: \"{m['title'][5:]}\" — {artist} — {m['lic']} — https://commons.wikimedia.org/wiki/{urllib.parse.quote(m['title'].replace(' ', '_'))}")
    print(name, os.path.getsize(fn) if os.path.exists(fn) else "FALHOU", flush=True)
open(os.path.join(out, "CREDITOS.md"), "w").write("# Créditos das fotos (Wikimedia Commons)\n\n" + "\n".join(credits) + "\n")
