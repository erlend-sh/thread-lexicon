# Fetches what build.py inlines: the latin font files, as data URLs.
# Run once; build.py then needs no network.
import re, urllib.request, base64
get = lambda u, ua=None: urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': ua} if ua else {}), timeout=30).read()
css = get('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Public+Sans:wght@400;500;600;700&display=swap',
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36').decode()
faces, cache = [], {}
for sub, blk in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
  if sub not in ('latin', 'latin-ext'): continue
  url = re.search(r'url\((https://[^)]+)\)', blk).group(1)
  cache.setdefault(url, 'data:font/woff2;base64,' + base64.b64encode(get(url)).decode())
  faces.append(blk.replace(url, cache[url]))
open('fonts-inline.css', 'w').write('\n'.join(faces))
print(len(faces), 'font faces')
