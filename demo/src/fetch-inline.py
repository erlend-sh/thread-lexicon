# Fetches what build.py inlines: the two libraries, the latin font files and the snapshot's images (resized, as data URLs).
# Run once after snapshot.json changes; build.py then needs no network.
import json, re, urllib.request, io, base64
from PIL import Image
get = lambda u, ua=None: urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': ua} if ua else {}), timeout=30).read()
open('marked.min.js', 'wb').write(get('https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js'))
open('purify.min.js', 'wb').write(get('https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js'))
css = get('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Public+Sans:wght@400;500;600;700&display=swap',
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36').decode()
faces, cache = [], {}
for sub, blk in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
  if sub not in ('latin', 'latin-ext'): continue
  url = re.search(r'url\((https://[^)]+)\)', blk).group(1)
  cache.setdefault(url, 'data:font/woff2;base64,' + base64.b64encode(get(url)).decode())
  faces.append(blk.replace(url, cache[url]))
open('fonts-inline.css', 'w').write('\n'.join(faces))
blobs = {}
for s in json.load(open('snapshot.json')):
  if not s.get('pds'): continue
  for cid in sorted(set(re.findall(r'"\$link":\s*"(baf[a-z0-9]+)"', json.dumps(s)))):
    try: im = Image.open(io.BytesIO(get(f"{s['pds']}/xrpc/com.atproto.sync.getBlob?did={s['did']}&cid={cid}"))); im.load()
    except Exception: continue
    if im.width > 1200: im = im.resize((1200, round(im.height * 1200 / im.width)))
    b = io.BytesIO()
    if im.mode in ('RGBA', 'LA', 'P'): im.save(b, 'WEBP', quality=82); mime = 'image/webp'
    else: im.convert('RGB').save(b, 'JPEG', quality=80, optimize=True); mime = 'image/jpeg'
    blobs[cid] = f'data:{mime};base64,' + base64.b64encode(b.getvalue()).decode()
json.dump(blobs, open('blobs.json', 'w'))
print(len(faces), 'font faces,', len(blobs), 'images')
