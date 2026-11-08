# Atmospheric Threads: `community.lexicon.thread.*` (draft 8)

**Draft 8** renames the thread record to `.container` and adds reactions, vote direction, a shared markdown format and indexer views.

**Premise.** `community.lexicon.thread` is a fork of standard.site that goes on to fully cover threads: forums, chat channels and comments.

standard.site's schema could hold threads, but its maintainers want it to stay focused on long-form, blog-like writing. In "Basic Metadata for Modality Spaces" (discourse.atmosphere.community/t/1333, post #5), schlage.town said forum and chat threads should be a different lexicon, so reader and discovery apps don't fill up with them. Barazo ran into the same feed-pollution problem in its forum lexicon thread (/t/624). So this draft keeps standard.site's shape and field names, and moves everything into its own namespace.

**Why Lexicon Community.** `community.lexicon.*` is a neutral namespace run by an open working group. bnewbold suggested it for shared space metadata in /t/1333. It keeps the one-domain rule: everything lives under a single domain, and no product owns it. Proposals go through the Lexicon Community category on discourse.atmosphere.community, and the schemas live at tangled.org/lexicon.community/lexicons. New lexicons are developed by a working group, so this would start as a "Threads" working group.

## The fork

| standard.site | community.lexicon.thread | What changes |
|---|---|---|
| `site.standard.publication` | **`.group`** | A group (space): in threads, the group is what a publication is to articles. Same fields (`url`, `name`, `description`, `icon`, `basicTheme`, `labels`, `preferences.showInDiscover`). `basicTheme` reuses `site.standard.theme.basic` by reference. |
| `site.standard.document` | **`.container`** | A container with no body: the document's `path`, `title`, `description`, `tags`, `labels`, `publishedAt` and `updatedAt`, plus **`parent`** for nesting. Its `group` field replaces `site`. Drops `textContent` and `content` (the opening post carries the text), and `coverImage`, `bskyPostRef`, `contributors` and `links`. |
| `site.standard.graph.subscription` | **`.subscription`** | Its `group` field replaces `publication`. Adds optional `thread` and `notify`, so you can join a whole group, or follow one channel or one thread (see Subscriptions). |
| `site.standard.graph.recommend` | **`.recommend`** | Its `subject` field replaces `document`, and can be a thread or a post. Works like an upvote. Adds optional `direction` (`up` or `down`, absent means `up`), so it doubles as a vote (see Votes and reactions). |
| (none) | **`.post`** | Every message: a thread's opening post, a reply, a chat message or a comment. `thread`, `replyTo`, `document`, `textContent` (**required**), `content`, `labels`, `createdAt`, `updatedAt`. `content` lists `defs#markdown` as the shared rich format. `thread` can be a `.container` or any `site.standard.document`, so it doubles as a comment record for articles. |
| (none) | **`.reaction`** | An emoji reaction: `subject` (any record), optional `cid`, `emoji`, `createdAt`. A like is ❤️. |
| (none) | **`.channel`** | Written by the group. Features a top-level thread in the sidebar: `thread`, `section`, `position`, `icon`, `description`. |
| (none) | **`.override`** | Written by the group. Applies moderation to records it can't edit (move, rename, hide, unhide, lock, unlock, pin, unpin): `subject`, `action`, `toThread`, `title`, `until`, `actor`, `reason`. |
| verification: `/.well-known/site.standard.publication`, `<link rel="site.standard.document">` | `/.well-known/community.lexicon.thread.group`, `<link rel="community.lexicon.thread.container">` | Same mechanism, renamed. |

**The opening post is a post.** A `.container` holds no text, only its title, its group and where it sits. Everything said in it is a `.post`, the opening post (OP) included, so the OP is edited, recommended, moderated and rendered the same way as every reply. The OP is the thread author's first post in the thread that answers no other post. Clients write the thread and its OP together, in one `applyWrites` call. The thread never names its OP: a record only points at records that already exist, so the post points at the thread and never the other way round. A thread can also have no OP: a channel is a thread whose chat is just its posts (examples 4 and 20).

What the fork gains over draft 4:
- **`parent` is a real field.** Draft 4 hid it inside standard.site's `links` union, and validators don't look inside open unions. Now a bad `parent` is rejected (see the validation below), and standard.site issue #17 doesn't matter here any more.
- **Discovery is opt-in by type.** Thread indexers read `.container` records, and reader apps never see them unless they choose to.
- **Comments still reach articles.** A `.post` whose `thread` is a `site.standard.document` is a comment on that article. Nobody has to approve anything, and it fills the gap people currently patch with `bskyPostRef` or the unofficial `site.standard.document.comment`.

## Root and parent
Bluesky, Barazo and Coves give every reply a `root` and a `parent`. A `.post` has the same two pointers under different names:

| Bluesky, Barazo, Coves | `.post` | Notes |
|---|---|---|
| `root` | `thread` | The container: a `.container`, or a `site.standard.document` for article comments. Always set. |
| `parent` | `replyTo` | The post being answered. |
| `parent == root` (top-level reply) | `replyTo` absent | A post that answers no other post is top level. An importer maps `parent == root` to no `replyTo`, and an exporter does the reverse. |

So linear apps (forums, chat) read `thread` and ignore `replyTo`, while nesting or vote-sorted apps rebuild the tree from both. Unlike Bluesky's strongRefs, both are plain at-uris with no CID, because posts are expected to be edited. A reaction can still pin a CID (below).

## Votes and reactions
These are two different records, because they count differently (bretton.dev in /t/1418, post #4):

- **`.recommend` is a vote.** One per person per subject, so the newest counts. `direction` is `up` or `down`, and absent means `up`, so a plain recommend still reads like standard.site's. Aggregator-style apps (Coves, Lobsters- or Reddit-like boards) sort by the score. Forum and chat apps can show only up votes, or ignore votes altogether. `direction` is a trial: if it turns out apps want a different shape, it can move to its own `.vote` record without touching `.recommend`.
- **`.reaction` is an emoji.** Someone can leave several on the same subject, one per emoji. A Discourse-style like is a ❤️ reaction. Its `subject` can be any record, not only a thread or a post, since reacting to an event or an RSVP is the same act (ngerakines.me, post #6). The optional `cid` pins the reaction to one version of the subject.

## Rich text
Every post needs plain `textContent`, so any reader can show any post. For formatting, `content` is an open union, which on its own would leave readers chasing every app's format (hyl.st, post #8). So `defs#markdown` (`{ text }`, CommonMark) is the shared starter format: every threads app should be able to read and write it, and apps can add their own formats alongside. Readers that can't render markdown fall back to `textContent`, and raw HTML in the markdown should not be rendered.

## Subscriptions
standard.site's subscription is one record per publication you follow, kept in your own repo. That still works for threads: a `.group` plays the publication's part, and subscribing to it means joining the group. But people also want to follow a single thread, so `.subscription` adds two optional fields:

- **`thread`** narrows the subscription to one thread and everything under it: its posts and its child threads, at any depth. A channel is a thread, so following a channel means pointing at the channel's thread, not its `.channel` record, which the group can delete and recreate. `thread` can also be a `site.standard.document`, with `group` set to its publication, to follow an article's comments.
- **`notify`** says what you want to hear about: `posts` (every new post), `threads` (new threads only) or `none` (follow quietly, such as keeping a channel in your sidebar). When it's absent, a whole-group subscription means `threads` and a thread subscription means `posts`. That matches standard.site, where following a publication means seeing its new documents.

| Scope | `group` | `thread` | Default `notify` | Example |
|---|---|---|---|---|
| Join a group | the `.group` | (absent) | `threads` | 11 |
| Follow a channel | the `.group` | the channel's thread | `posts` | 16, 19 |
| Follow a thread | the `.group` | the thread | `posts` | 17 |
| Follow an article's comments | the `site.standard.publication` | the `site.standard.document` | `posts` | 18 |

Rules for indexers:
- **The most specific subscription wins.** Someone who joined a group with `threads` and follows one channel with `posts` hears every post in that channel and only new threads elsewhere.
- **One record per scope.** If someone has two subscriptions with the same `group` and `thread`, the newest counts. Apps change `notify` by updating the record in place, and unsubscribe by deleting it.
- **Only a whole-group subscription means membership.** A group's member count is its subscriptions without `thread`. Following a single thread doesn't make you a member.
- **The thread has to belong to the group.** A subscription whose `thread` belongs to a different group (by its own `group` field, or its ancestors') is ignored.

## Publishing both
The same piece of writing can be published as both a `site.standard.document` and a `.post`. Since draft 7 the pair is always an article and a post, never an article and a thread. That gives two things:
- **A blog post gets a comment section.** A Leaflet author also writes a `.container` for their post, with the post's text as its opening post. Any threads client can then show the post with its replies, and reader apps keep showing the article (examples 13, 21 and 14).
- **A forum post becomes an article.** A long opening post or a single long reply gets a `site.standard.document` too, so it shows up in reader and discovery apps (example 15).

The two records point at each other. The post has a `document` field, and the document carries `community.lexicon.thread.defs#link` in its `links` union, naming the post. **A pair only counts when both records are in the same repo and each points at the other**, so nobody can attach someone else's article to their thread. Replies are the other posts in the paired post's thread. A reader showing the document finds them through the link, and `.post` records that point straight at a document still count as comments on it.

Draft 6 paired the article with the thread record itself, which carried the text. That made the thread one record and saved a copy, but it gave the OP a different shape from every other post. Draft 7 gives that up so the container and the OP are independent.

Rules kept from atmo-board (`docs/all-threads.md`):
- **Threads all the way down.** A channel is a top-level `.container` that the group features with a `.channel` record.
- **Chat and forum share one post model.** A channel's chat is the `.post` records that point at the channel's own thread.
- **Authors own their words.** Threads and posts live in their authors' repos. The group only acts through `.override` records, and an override only counts when the repo that owns the subject's `.group` wrote it.
- **Records only.** Lists, counts and the latest activity are views that indexers compute, not record fields (see open question 2).

## Files
- `lexicons/community.lexicon.thread.{group,container,post,channel,override,subscription,recommend,reaction,defs}.json`
- `examples/1–24`: a forum's group, a channel thread and its sidebar entry, a thread and its opening post (4 and 20), a chat post, a reply, a reply to a reply, a comment on a real Leaflet article, lock and move overrides, a subscription, a recommend, the publishing-both pair (a Leaflet post as a thread with its opening post, the document linking back to that post, and a forum reply republished as an article: 13, 21, 14 and 15), and granular subscriptions (a channel, a thread, an article's comments, and a channel followed quietly), plus a ❤️ reaction (22), a down vote (23) and a markdown reply to a reply (24).
- `demo/threads-lexicon-website.html`: the threads-lexicon website demo, a frontend-only reader of `community.lexicon.thread.*` records. It shows Atmosphere Community (simulated from its Discourse forum) in two places with the same records: at its own site, our.atmosphere.community, as a dense grid board, and as a group space on mu.social (mu.social/groupspace/@atmosphere.community) as cards. `demo/src/` holds the build (`build.py`, `template.html`, and `mu.py` for the articles).
- `standard-site-remit.md`: what standard.site covers.
- `archive/draft-4-site-standard-thread/`: the previous draft, which tried to put threads under `site.standard.thread.*`. `archive/draft-0/` holds the first baseline.

**Validation.** Checked with `@atproto/lexicon`. All 23 thread records in the examples pass (example 14 is a `site.standard.document`, which this lexicon set doesn't cover). These are rejected:
- a post without `thread` or `textContent`, or with a `document` that isn't an at-uri
- a thread without `title`, or with a `parent` that isn't an at-uri
- a group without `url`
- a channel without `position`
- an override without `action`
- a subscription, recommend or reaction without its subject
- a reaction without `emoji`, or with more than one grapheme in it
- a recommend whose `direction` isn't a string
- a `defs#markdown` content without `text`
- a subscription whose `thread` isn't an at-uri, or whose `notify` isn't a string

One gap: validators don't look inside open unions, so a malformed `defs#link` inside a document's `links` still passes. Apps have to check it themselves.

## Lessons from the demo
- **`textContent` isn't reliable upstream.** Leaflet writes none, and standard.site's own docs put MDX source in it. That's why `.post` requires it, and every message, the opening post included, is a `.post`.
- **Descriptions fall back to the opening post.** A thread's `description` is optional. When the author didn't write one, the board shows the start of the opening post's `textContent`: up to 300 characters and at most 3 paragraphs. Discourse's excerpts are generated, so the demo leaves them out and derives them this way.
- **Activity is derived.** `updatedAt` keeps standard.site's meaning (the author's last edit). The board's activity column is the newest post's `createdAt`, which an indexer computes.

## Open questions
1. **Public spaces, leaning yes.** A group's threads and posts live in its spaces, including public ones, rather than in public repos. That fits team comms better: the group's space defines who can read and write, and private channels are just spaces with a member list. The `.group` record stays in a public repo as the public announcement, so discovery still works (the "announcing a space publicly" question from /t/1333). What this means, per atproto's "A Jetstream for Spaces" post (6 Nov 2026):
   - **No firehose for spaces.** Space records aren't relayed. An app reads a space through its own Spaces-mode Jetstream sync service, which borrows read access from a signed-in member. A public-read space presumably lets any signed-in user lend that access, but a reader still has to sync it, so mu.social or a Bluesky client would each run (or share) a sync service.
   - **Backend, not browser.** The stream is meant for an app's backend, so a frontend-only client needs a Group Host or appview read API in front of it. The mock API stands in for that.
   - **Records still live in authors' repos.** A post stays in its author's repo and is written into the group's space, which keeps "authors own their words".
   - **URIs need their space.** The same author can write the same collection and record key into two spaces, so an at-uri alone may not name one record. `thread`, `replyTo` and `subject` may need a space qualifier, depending on how Spaces addresses records.
   - **Article comments stay public.** A `site.standard.document` lives in a public repo, so comments on it can stay public-repo posts.
2. **A shared view.** Reply counts, posters and latest activity are aggregates over posts in other people's repos, so they belong in a view, not in a record. Draft 8 adds `defs#threadView` and `defs#postView` (with `#reactionCount` and `#moderationState`) so every indexer, and the mock API, serves the same shape: the record as written, the effective title and parent after overrides, post count, posters, latest activity, score and reaction tallies. Query endpoints that return them (such as `listThreads` and `getThread`) are still to be named.
3. **Who is the author?** Neither standard.site nor this fork has a profile record. An author is the repo DID, shown as its handle. Display names and avatars come from elsewhere, such as `app.bsky.actor.profile`.
4. **Naming.** Settled in draft 8: the thread record is `community.lexicon.thread.container`, since `thread.thread` repeated itself and the record holds both posts and child threads. The family stays `community.lexicon.thread`, and fields that point at a container keep the name `thread` (on posts and subscriptions). `topic` is still reserved for later.
5. **Titles are required.** Every thread needs one, as with documents. Untitled chat lives in a channel's posts, so nothing is lost so far.
6. **Muting.** Subscriptions are public records, so `notify: "none"` means following quietly, not muting. Muting a thread or a person is a private choice and belongs in app preferences or a private space, not a public record.
7. **Other roots.** Should `thread` accept any record, such as a calendar event, a Bluesky post or a Lichen wiki note (ngerakines.me and juprodh.me in /t/1418)?

## Prior art
- **Thread lexicons on atproto**, collected in /t/1418:
  - Colibri: `social.colibri.beta.thread`
  - atmoBB: `app.atmobb.discussion.*`
  - Barazo: `forum.barazo.topic.*`
  - UserInput: `app.userinput.discussion`
  - Coves: `social.coves.community.postv2`, `social.coves.community.comment`, `social.coves.feed.vote`
  - Roomy: planned move to atproto spaces
- **SIOC** (rdfs.org/sioc/spec), used for forums, blogs and mailing lists, has the same model: a `Site` (our group) holds `Forum`s and `Container`s (our threads and channels), which are `container_of` `Post`s, with `has_reply`/`reply_of`, `has_subscriber`, `has_creator` and `dcterms:created`/`title`. Its SIOC Access module separates container access from the site, as spaces do here (cloud, post #3).
