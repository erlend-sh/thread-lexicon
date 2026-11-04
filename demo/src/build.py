import json
sim=json.loads(open('discourse-sim.json').read().replace('did:web:discourse.atmosphere.community','did:web:atmosphere.community'))
# the forum publishes community.lexicon.thread.* records, the fork of standard.site for threads
T='community.lexicon.thread'
ren=lambda x: json.loads(json.dumps(x).replace('site.standard.publication/',f'{T}.group/').replace('site.standard.document/',f'{T}.thread/')
  .replace('site.standard.thread.post',f'{T}.post').replace('site.standard.thread.channel',f'{T}.channel'))
def as_thread(d):
  d=ren(d); v=d['value']; v['$type']=f'{T}.thread'
  parent=(v.pop('links',None) or {}).get('parent')
  if parent: v['parent']=parent
  if 'site' in v: v['group']=v.pop('site')  # a thread names its group, where a document names its site
  return d
# one community, one set of records: a .group for its threads and a site.standard.publication for its articles, both at our.atmosphere.community
URL='https://our.atmosphere.community'
sim['handle']='atmosphere.community'
std=sim['publication']; std['value']['url']=URL
sim['threadSite']=ren(std); sim['threadSite']['value']['$type']=f'{T}.group'
sim['publication']={'uri':std['uri'],'value':{**std['value']}}
sim['threads']=[as_thread(d) for d in sim['documents']]
# Discourse's excerpts are generated, not written, so these threads have no description and the board derives one from textContent
for d in sim['threads']: d['value'].pop('description',None)
sim['channels']=[{**c,**as_thread({'uri':c['uri'],'value':c['value']})} for c in sim['channels']]
for c in sim['channels']: c['channel']=ren(c['channel'])
from mu import articles
lexch=next(c['uri'] for c in sim['channels'] if c['value']['title']=='Lexicon Community')
sim['documents'],mirror=articles(sim['publication']['uri'],sim['threadSite']['uri'],lexch)
sim['threads'].append(mirror)
SIM=f"Records for Atmosphere Community, built from its Discourse forum's public JSON: the community as a {T}.group, each topic as a {T}.thread whose parent is its channel, channels as {T}.channel records and every reply as a {T}.post. Its articles are site.standard.document records, and Lars's meetup notes are published both ways. None of this exists on the network yet."
sim['simulated']=f"{SIM} This is the community's own site, which shows its board as a dense grid. mu.social shows the same records as cards."
sim['layout']='grid'
# the same records, read by another client: mu.social shows the community as a group space
sim['views']=[{'url':'https://mu.social/space/@atmosphere.community','client':'mu.social','simulated':f"{SIM} This is mu.social showing the same community as a group space. It reads the same records as our.atmosphere.community, so threads, replies and follows are shared, in its card layout.",'layout':'cards'}]
s=[sim]  # the demo is one community, shown by its own site and by mu.social
json.dump(s,open('snapshot.json','w'),separators=(',',':'))
t=open('template.html').read(); sj=open('snapshot.json').read().replace('</','<\\/')
# everything the page needs goes inside it, so it works offline: the fonts (see fetch-inline.py)
inl=lambda f: open(f).read().replace('</script','<\\/script')
for k,f in [('__FONTS__','fonts-inline.css')]: t=t.replace(k,inl(f))
open('../threads-lexicon-website.html','w').write(t.replace('__SNAPSHOT__',sj).replace('__SNAPDATE__','27 Oct 2026'))
print(len(sj))
