import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

TITLES = [
    "File:Ceramic tower heater.jpg",
    "File:Halogen Heater Tube.jpg",
    "File:Elektrischer Heizofen, fahrbar.jpg",
    "File:Heater with the cable.JPG",
    "File:Heizung1.jpg",
    "File:Oil filled radiator.jpg",
]
OUT = Path("/root/video-gen/refs")
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

for i, t in enumerate(TITLES):
    q = urllib.parse.urlencode({"action": "query", "titles": t, "prop": "imageinfo",
                                "iiprop": "url", "iiurlwidth": "700", "format": "json"})
    try:
        req = urllib.request.Request(f"https://commons.wikimedia.org/w/api.php?{q}", headers=UA)
        d = json.load(urllib.request.urlopen(req, timeout=20))
        pages = d["query"]["pages"]
        info = next(iter(pages.values()))
        if "imageinfo" not in info:
            print("нет", t)
            continue
        url = info["imageinfo"][0].get("thumburl") or info["imageinfo"][0]["url"]
        raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        p = OUT / f"heater{i}.jpg"
        p.write_bytes(raw)
        print("ok", t, len(raw))
    except Exception as e:  # noqa: BLE001
        print("fail", t, e)
