# Atmospheric Threads

An exploration of **`community.lexicon.thread.*`**, a draft AT Protocol lexicon for threads: forum threads, chat channels and comments. It comes with a frontend-only demo website.

To see the demo, open [`demo/threads-lexicon-website.html`](demo/threads-lexicon-website.html) in a browser. It's a single self-contained file, so it needs no server and no network.

## What this exploration is about

[standard.site](https://standard.site) gives long-form writing on atproto a shared shape. A `site.standard.publication` is a blog, and a `site.standard.document` is a post, so any reader app can show posts from Leaflet and other blogging apps. Its maintainers want it to stay focused on blog-like writing, and not fill reader and discovery apps with forum and chat threads ([Basic Metadata for Modality Spaces](https://discourse.atmosphere.community/t/basic-metadata-for-modality-spaces/1333), post #5).

So threads get their own lexicon. `community.lexicon.thread` is a fork of standard.site that keeps its shape and field names and adds what threads need:

| standard.site | community.lexicon.thread |
|---|---|
| `publication` (a blog) | **`group`**: a group (space), such as a forum or a community. Same fields. |
| `document` (a post) | **`thread`**: same field names, plus `parent`, so threads nest. A channel is a top-level thread. |
| `graph.subscription` | **`subscription`**: join a whole group, or follow one channel or thread, with a `notify` level. |
| `graph.recommend` | **`recommend`**: an upvote on a thread or a post. |
| (none) | **`post`**: a reply, a chat message or a comment on an article. |
| (none) | **`channel`**: the group features a thread in its sidebar. |
| (none) | **`override`**: the group moderates records it doesn't own (lock, move, hide, pin). |

Because the two share a baseline, one piece of writing can be published as both. A Leaflet post can also be a thread, which gives it a comment section in any threads app. A long forum post can also be an article, so it reaches reader apps. The two records point at each other from the same repo.

The lexicon would live under `community.lexicon.*`, run by Lexicon Community, as a proposal from a Threads working group. It's a draft, and none of these records exist on the network yet. The full draft, with its rules and open questions, is in [`SPEC.md`](SPEC.md).

## What the demo shows

The demo reads records the way an app would and renders them as a website. The four sites are:

- **our.atmosphere.community**: Atmosphere Community's own site. It's simulated from the forum's public Discourse JSON: 30 topics as `thread` records in their channels, with every reply as a `post`. Four articles are published as `site.standard.document`, and one of them is also a thread. The board is a dense grid.
- **mu.social/space/@atmosphere.community**: the same community, read by a different client (mu.social's Group Spaces). It uses the same records, so threads, replies and follows are shared. The board is cards.
- **lab.leaflet.pub** and **notes.erlend.sh**: real standard.site snapshots of two blogs, taken 27 Oct 2026.

Controls at the top:

- **Article lens / Thread lens** switch which lexicon the page reads. In the article lens it's a standard.site reader. In the thread lens it reads `community.lexicon.thread.*`, and any blog post can be shown as a thread with comments.
- **Show record fields** labels every element with the record field it comes from. Hovering a label highlights what it labels. Counts, posters and latest activity are marked *derived*: an indexer computes them from posts, so they aren't stored in any record.
- **Render app formats**: standard.site keeps plain text in `textContent` and an app's own rich format in `content`. When this is on, the demo renders the formats it knows (Leaflet's blocks, markdown). When it's off, you see only what a plain standard.site reader sees. For Leaflet that's nothing, because Leaflet writes no `textContent`.
- **Load live** fetches a real publication by handle, DID or URL. This is the only part of the demo that uses the network.

Other things to try: click a channel chip to narrow the board to it, follow a group, channel or thread to see the subscription records it would write, and open "Notes from the October meetup" to switch between its article and thread versions.

A thread with no written `description` shows the start of its opening post on the board: up to 300 characters and at most 3 paragraphs.

## Building it

The demo is built from `demo/src/`:

```
cd demo/src
python3 build.py          # writes ../threads-lexicon-website.html
```

- `template.html` is the whole app: HTML, CSS and plain JavaScript, with no framework.
- `build.py` loads the blog snapshots (`snapshot.json`) and the Discourse data (`discourse-sim.json`). It converts the Discourse data into `community.lexicon.thread.*` records, adds the articles from `mu.py`, and inlines everything into the template.
- `fetch-inline.py` refreshes the inlined assets: marked and DOMPurify, the fonts (IBM Plex Mono, Newsreader and Public Sans) and the blogs' images. It's the only step that needs the network. Run it again after changing `snapshot.json`.

## What's in this repo

- [`SPEC.md`](SPEC.md): the lexicon draft (draft 6). It covers the fork, subscriptions, publishing both, the rules for indexers, validation and open questions.
- [`lexicons/`](lexicons/): the `community.lexicon.thread.*` schemas: `group`, `thread`, `post`, `channel`, `override`, `subscription`, `recommend` and `defs`.
- [`examples/`](examples/): 19 example records, all valid against the schemas.
- [`demo/`](demo/): the website export and its source.
- [`standard-site-remit.md`](standard-site-remit.md): what standard.site covers, and what it leaves out.
- [`apps/atmobb/`](apps/atmobb/): an example of app-native content (atmoBB) carried in the `content` union of threads and posts.
- [`archive/`](archive/): earlier drafts. Draft 4 tried to put threads under `site.standard.thread.*`, and draft 0 was the first baseline.

## Credits

The Atmosphere Community content comes from public posts on [discourse.atmosphere.community](https://discourse.atmosphere.community). The blog content belongs to [Leaflet](https://lab.leaflet.pub) and [notes.erlend.sh](https://notes.erlend.sh). Fonts are under the SIL Open Font License. marked is MIT-licensed, and DOMPurify is under Apache 2.0 or MPL 2.0.
