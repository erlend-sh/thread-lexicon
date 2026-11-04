# Atmospheric Threads

An exploration of **`community.lexicon.thread.*`**, a draft AT Protocol lexicon for threads: forum threads, chat channels and comments. It comes with a frontend-only demo website.

To see the demo, open [`demo/threads-lexicon-website.html`](demo/threads-lexicon-website.html) in a browser. It's a single self-contained file, so it needs no server and no network.

## What this exploration is about

[standard.site](https://standard.site) gives long-form writing on atproto a shared shape. A `site.standard.publication` is a blog, and a `site.standard.document` is a post, so any reader app can show posts from Leaflet and other blogging apps. Its maintainers want it to stay focused on blog-like writing, and not fill reader and discovery apps with forum and chat threads ([Basic Metadata for Modality Spaces](https://discourse.atmosphere.community/t/basic-metadata-for-modality-spaces/1333), post #5).

So threads get their own lexicon. `community.lexicon.thread` is a fork of standard.site that keeps its shape and field names and adds what threads need:

| standard.site | community.lexicon.thread |
|---|---|
| `publication` (a blog) | **`group`**: a group (space), such as a forum or a community. Same fields. |
| `document` (a post) | **`thread`**: a container with the document's title and path fields, plus `parent`, so threads nest. It has no body. A channel is a top-level thread. |
| `graph.subscription` | **`subscription`**: join a whole group, or follow one channel or thread, with a `notify` level. |
| `graph.recommend` | **`recommend`**: an upvote on a thread or a post. |
| (none) | **`post`**: every message, the thread's opening post included: replies, chat messages and comments on articles. |
| (none) | **`channel`**: the group features a thread in its sidebar. |
| (none) | **`override`**: the group moderates records it doesn't own (lock, move, hide, pin). |

One piece of writing can be published as both an article and a post. A Leaflet post can also be the opening post of a thread, which gives it a comment section in any threads app. A long forum post can also be an article, so it reaches reader apps. The article and the post point at each other from the same repo.

The lexicon would live under `community.lexicon.*`, run by Lexicon Community, as a proposal from a Threads working group. It's a draft, and none of these records exist on the network yet. The full draft, with its rules and open questions, is in [`SPEC.md`](SPEC.md).

## What the demo shows

The demo is a pure threads-lexicon demo. It reads `community.lexicon.thread.*` records the way an app would and renders them as a website. It shows one community in two places:

- **our.atmosphere.community**: Atmosphere Community's own site. It's simulated from the forum's public Discourse JSON: 30 topics as `thread` records in their channels, with every reply as a `post`. Four articles are published as `site.standard.document`, and one of them is also a thread. The board is a dense grid.
- **mu.social/groupspace/@atmosphere.community**: the same community, read by a different client (mu.social's Group Spaces). It uses the same records, so threads, replies and follows are shared. The board is cards.

Controls at the top:

- **Site** switches between the two.
- **Show record fields** labels every element with the record field it comes from. Hovering a label highlights what it labels. Counts, posters and latest activity are marked *derived*: an indexer computes them from posts, so they aren't stored in any record.

Other things to try: click a channel chip to narrow the board to it, follow a group, channel or thread to see the subscription records it would write, and open "Notes from the October meetup", a thread whose opening post is also published as an article. The demo makes no network requests.

A thread with no written `description` shows the start of its opening post on the board: up to 300 characters and at most 3 paragraphs.

## Building it

The demo is built from `demo/src/`:

```
cd demo/src
python3 build.py          # writes ../threads-lexicon-website.html
```

- `template.html` is the whole app: HTML, CSS and plain JavaScript, with no framework.
- `build.py` loads the Discourse data (`discourse-sim.json`) and converts it into `community.lexicon.thread.*` records. It adds the articles from `mu.py`, writes them to `snapshot.json`, and inlines everything into the template.
- `fetch-inline.py` refreshes the inlined fonts (IBM Plex Mono, Newsreader and Public Sans). It's the only step that needs the network.

## What's in this repo

- [`SPEC.md`](SPEC.md): the lexicon draft (draft 7). It covers the fork, subscriptions, publishing both, the rules for indexers, validation and open questions.
- [`lexicons/`](lexicons/): the `community.lexicon.thread.*` schemas: `group`, `thread`, `post`, `channel`, `override`, `subscription`, `recommend` and `defs`.
- [`examples/`](examples/): 21 example records, all valid against the schemas.
- [`demo/`](demo/): the website export and its source.
- [`standard-site-remit.md`](standard-site-remit.md): what standard.site covers, and what it leaves out.
- [`apps/atmobb/`](apps/atmobb/): an example of app-native content (atmoBB) carried in the `content` union of threads and posts.
- [`archive/`](archive/): earlier drafts. Draft 4 tried to put threads under `site.standard.thread.*`, and draft 0 was the first baseline.

## Credits

The Atmosphere Community content comes from public posts on [discourse.atmosphere.community](https://discourse.atmosphere.community). Fonts are under the SIL Open Font License.
