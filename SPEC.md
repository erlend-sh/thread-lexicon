# Atmospheric Threads: `community.lexicon.thread.*` (draft 6)

**Premise.** `community.lexicon.thread` is a fork of standard.site that goes on to fully cover threads: forums, chat channels and comments.

standard.site's schema could hold threads, but its maintainers want it to stay focused on long-form, blog-like writing. In "Basic Metadata for Modality Spaces" (discourse.atmosphere.community/t/1333, post #5), schlage.town said forum and chat threads should be a different lexicon, so reader and discovery apps don't fill up with them. Barazo ran into the same feed-pollution problem in its forum lexicon thread (/t/624). So this draft keeps standard.site's shape and field names, and moves everything into its own namespace.

**Why Lexicon Community.** `community.lexicon.*` is a neutral namespace run by an open working group. bnewbold suggested it for shared space metadata in /t/1333. It keeps the one-domain rule: everything lives under a single domain, and no product owns it. Proposals go through the Lexicon Community category on discourse.atmosphere.community, and the schemas live at tangled.org/lexicon.community/lexicons. New lexicons are developed by a working group, so this would start as a "Threads" working group.

## The fork

| standard.site | community.lexicon.thread | What changes |
|---|---|---|
| `site.standard.publication` | **`.group`** | A group (space): in threads, the group is what a publication is to articles. Same fields (`url`, `name`, `description`, `icon`, `basicTheme`, `labels`, `preferences.showInDiscover`). `basicTheme` reuses `site.standard.theme.basic` by reference. |
| `site.standard.document` | **`.thread`** | Same field names (`path`, `title`, `description`, `textContent`, `content`, `tags`, `labels`, `publishedAt`, `updatedAt`), plus **`parent`** for nesting. Its `group` field replaces `site`. Drops `coverImage`, `bskyPostRef`, `contributors` and `links`. |
| `site.standard.graph.subscription` | **`.subscription`** | Its `group` field replaces `publication`. Adds optional `thread` and `notify`, so you can join a whole group, or follow one channel or one thread (see Subscriptions). |
| `site.standard.graph.recommend` | **`.recommend`** | Its `subject` field replaces `document`, and can be a thread or a post. Works like an upvote. |
| (none) | **`.post`** | A reply, chat message or comment: `thread`, `replyTo`, `textContent` (**required**), `content`, `labels`, `createdAt`, `updatedAt`. `thread` can be a `.thread` or any `site.standard.document`, so it doubles as a comment record for articles. |
| (none) | **`.channel`** | Written by the group. Features a top-level thread in the sidebar: `thread`, `section`, `position`, `icon`, `description`. |
| (none) | **`.override`** | Written by the group. Applies moderation to records it can't edit (move, rename, hide, unhide, lock, unlock, pin, unpin): `subject`, `action`, `toThread`, `title`, `until`, `actor`, `reason`. |
| verification: `/.well-known/site.standard.publication`, `<link rel="site.standard.document">` | `/.well-known/community.lexicon.thread.group`, `<link rel="community.lexicon.thread.thread">` | Same mechanism, renamed. |

What the fork gains over draft 4:
- **`parent` is a real field.** Draft 4 hid it inside standard.site's `links` union, and validators don't look inside open unions. Now a bad `parent` is rejected (see the validation below), and standard.site issue #17 doesn't matter here any more.
- **Discovery is opt-in by type.** Thread indexers read `.thread` records, and reader apps never see them unless they choose to.
- **Comments still reach articles.** A `.post` whose `thread` is a `site.standard.document` is a comment on that article. Nobody has to approve anything, and it fills the gap people currently patch with `bskyPostRef` or the unofficial `site.standard.document.comment`.

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
Because the fork keeps standard.site's field names, the same piece of writing can be published as both a `site.standard.document` and a `.thread`, and converting one into the other is mostly copying fields. That gives two things:
- **A blog post gets a comment section.** A Leaflet author also writes a `.thread` for their post. Any threads client can then show the post with its replies, and reader apps keep showing the article (examples 13 and 14).
- **A forum post becomes an article.** A long thread or a single long reply gets a `site.standard.document` too, so it shows up in reader and discovery apps (example 15).

The two records point at each other. The thread or post has a `document` field, and the document carries `community.lexicon.thread.defs#link` in its `links` union. **A pair only counts when both records are in the same repo and each points at the other**, so nobody can attach someone else's article to their thread. Replies point at the thread. A reader showing the document finds them through the link, and older `.post` records that point straight at a document still count as comments on it.

Rules kept from atmo-board (`docs/all-threads.md`):
- **Threads all the way down.** A channel is a top-level `.thread` that the group features with a `.channel` record.
- **Chat and forum share one post model.** A channel's chat is the `.post` records that point at the channel's own thread.
- **Authors own their words.** Threads and posts live in their authors' repos. The group only acts through `.override` records, and an override only counts when the repo that owns the subject's `.group` wrote it.
- **Records only.** Lists, counts and the latest activity are views that indexers compute, not record fields (see open question 2).

## Files
- `lexicons/community.lexicon.thread.{group,thread,post,channel,override,subscription,recommend,defs}.json`
- `examples/1–19`: a forum's group, a channel thread and its sidebar entry, a thread, a chat post, a reply, a reply to a reply, a comment on a real Leaflet article, lock and move overrides, a subscription, a recommend, the publishing-both pair (a Leaflet post as a thread, the document linking back, and a forum post republished as an article), and granular subscriptions (a channel, a thread, an article's comments, and a channel followed quietly).
- `demo/threads-lexicon-website.html`: the threads-lexicon website demo, a frontend-only reader of `community.lexicon.thread.*` records. It shows Atmosphere Community (simulated from its Discourse forum) in two places with the same records: at its own site, our.atmosphere.community, as a dense grid board, and as a group space on mu.social (mu.social/groupspace/@atmosphere.community) as cards. `demo/src/` holds the build (`build.py`, `template.html`, and `mu.py` for the articles).
- `standard-site-remit.md`: what standard.site covers.
- `archive/draft-4-site-standard-thread/`: the previous draft, which tried to put threads under `site.standard.thread.*`. `archive/draft-0/` holds the first baseline.

**Validation.** Checked with `@atproto/lexicon`. All 19 examples pass. These are rejected:
- a post without `thread` or `textContent`
- a thread without `title`, or with a `parent` or `document` that isn't an at-uri
- a group without `url`
- a channel without `position`
- an override without `action`
- a subscription or recommend without its subject
- a subscription whose `thread` isn't an at-uri, or whose `notify` isn't a string

One gap: validators don't look inside open unions, so a malformed `defs#link` inside a document's `links` still passes. Apps have to check it themselves.

## Lessons from the demo
- **`textContent` isn't reliable upstream.** Leaflet writes none, and standard.site's own docs put MDX source in it. That's why `.post` requires it, and `.thread` should always write it too.
- **Descriptions fall back to the opening post.** A thread's `description` is optional. When the author didn't write one, the board shows the start of `textContent`: up to 300 characters and at most 3 paragraphs. Discourse's excerpts are generated, so the demo leaves them out and derives them this way.
- **Activity is derived.** `updatedAt` keeps standard.site's meaning (the author's last edit). The board's activity column is the newest post's `createdAt`, which an indexer computes.

## Open questions
1. **Public repos or public spaces?** Discovery comes from records in public repos, but atmo-board plans to keep forum content in a group's spaces. That's the "announcing a space publicly" question from /t/1333. The `.group` record is that public declaration, so the question is which of a group's threads live in public repos and which stay in its space.
2. **A shared view.** Reply counts, posters and latest activity are aggregates over posts in other people's repos, so they belong in a view such as `community.lexicon.thread.defs#threadView`, not in a record. A shared view would mean every indexer serves the same shape.
3. **Who is the author?** Neither standard.site nor this fork has a profile record. An author is the repo DID, shown as its handle. Display names and avatars come from elsewhere, such as `app.bsky.actor.profile`.
4. **Naming.** `community.lexicon.thread.thread` repeats itself, but `topic` is reserved for later. Alternatives are `.start` or `.root`.
5. **Titles are required.** Every thread needs one, as with documents. Untitled chat lives in a channel's posts, so nothing is lost so far.
6. **Muting.** Subscriptions are public records, so `notify: "none"` means following quietly, not muting. Muting a thread or a person is a private choice and belongs in app preferences or a private space, not a public record.
7. **Barazo.** `forum.barazo.topic.*` is the closest prior art, and it was already moving towards standard.site's shape. It's worth inviting into the working group.
