# Simulated articles for Atmosphere Community, the same community the forum records come from.
# mu.social's Group Spaces mock shows this community as a space; the articles are site.standard.document records,
# and Lars's meetup notes are published both ways, as an article and as a thread in the Lexicon Community channel.
import json, re
T = 'community.lexicon.thread'
PEOPLE = {
  'kai': ('Kai Lindqvist', 'kai.lindqvist.dev'), 'lars': ('Lars Haugen', 'larsh.bsky.social'), 'omar': ('Omar Haddad', 'omarh.dev'),
  'sofia': ('Sofia Reyes', 'sofiareyes.bsky.social'),
}
did = lambda k: f'did:plc:sim{k}'
author = lambda k: {'name': PEOPLE[k][0], 'handle': PEOPLE[k][1]}
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60]
ARTICLES = [
  ('kai', '2026-10-23', 'Moving a notes app to atproto, one record at a time', 'What we learned porting 40k notes to user-owned repos, writing our first lexicon, and running an AppView on a single VPS.'),
  ('sofia', '2026-10-20', "Lexicons are APIs you can't take back", "Once a record type ships, other apps start reading it. A short guide to naming, optional fields and versioning that won't strand anyone."),
  ('omar', '2026-10-14', 'Running an AppView for $12 a month', 'Jetstream, SQLite and one small box. Benchmarks, the bits that broke, and when you actually need Postgres.'),
  ('lars', '2026-10-02', 'Notes from the October meetup', 'Five talks, three demos and one long argument about whether replies should point at the root or the parent.'),
]
def post(k, n, thread, when, text):
  return {'uri': f'at://{did(k)}/{T}.post/sim{n:04d}', 'value': {'$type': f'{T}.post', 'thread': thread, 'textContent': text, 'createdAt': when}, 'author': author(k)}

def articles(pub_uri, site_uri, channel_uri):
  documents = [{'uri': f'at://{did(k)}/site.standard.document/simart{i:03d}', 'author': author(k), 'replies': [],
                'value': {'$type': 'site.standard.document', 'site': pub_uri, 'path': f'/a/{slug(title)}', 'title': title, 'description': excerpt, 'textContent': excerpt, 'publishedAt': f'{day}T09:00:00.000Z'}}
               for i, (k, day, title, excerpt) in enumerate(ARTICLES)]
  # publishing both: each record points at the other from the same repo
  art = documents[3]; th_uri = f'at://{did("lars")}/{T}.thread/simmirror'
  art['value']['links'] = {'$type': f'{T}.defs#link', 'thread': th_uri}
  replies = [post('omar', 90, th_uri, '2026-10-02T15:10:00.000Z', 'Both. Root for fetching, parent for rendering. Same as app.bsky.feed.post does.'),
             post('sofia', 91, th_uri, '2026-10-02T16:40:00.000Z', 'Thanks for writing this up. The slides from the lexicon talk would be great to link here too.')]
  mirror = {'uri': th_uri, 'author': author('lars'), 'replies': replies, 'value': {'$type': f'{T}.thread', 'group': site_uri, 'parent': channel_uri, 'document': art['uri'],
    'path': f'/t/{slug(art["value"]["title"])}', 'title': art['value']['title'], 'description': art['value']['description'], 'textContent': art['value']['textContent'], 'publishedAt': art['value']['publishedAt']}}
  return documents, mirror
