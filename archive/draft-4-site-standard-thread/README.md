# Atmospheric Threads: `site.standard.thread.*` (draft 3)

**Premise.** standard.site describes itself as being for "long-form publishing", but its schema is a *website* lexicon. A publication is a `url` and a `name`. A document is a `title` at a `path` on that site, with an open `content` union. Verification ties records to web pages. Long-form articles are one kind of website and discussion threads are another, so **a thread is a `site.standard.document`**.

**One domain.** Everything lives under `site.standard.*`, in a `thread` group that sits beside the existing `graph` and `theme` groups. There's no second namespace. `garden.msg` from drafts 0–2 is retired.

**The catch: only standard.site can publish these.** An NSID resolves through DNS on its domain (`_lexicon.thread.standard.site`), and that domain points at the standard.site account. So these four lexicons are an **upstream proposal**, to be filed at tangled.org/standard.site/lexicons, and they're only official once the maintainers publish them. Until then, records using them validate locally but lexicon resolution fails for anyone else. That's the same position as the unofficial `site.standard.document.comment`. Upstream decides by "consensus among builders who are actively implementing the standard", so atmo-board shipping against the draft is the strongest argument for it.

**Derived from atmo-board.** Following `comms-api/research-notes.md` and requirement 8 ("design the API first, then derive the lexicons"), this draft takes atmo-board's own records (`dev.atmoboard.thread`, `post`, `channel`, `override`) and re-expresses them on standard.site. It keeps the field names and drops what is atmo-board-specific (trust levels, bans). The shared standard covers **records only**. Views and queries (`getThread`, `listPosts` and so on) stay in each app's namespace, following Bluesky's split between `app.bsky.*` views and records (research notes §4.6).

## The model

| atmo-board today | On standard.site | Who writes it |
|---|---|---|
| The forum (one install, req. 16) | `site.standard.publication`, `url` = the forum's address | the forum (group DID) |
| `dev.atmoboard.thread` | `site.standard.document` with `site` = the forum publication, `path` = `/t/{key}/{slug}`, and **`links: { $type: "site.standard.thread.link", parent }`** | the author |
| thread `parent` | the `parent` field of `site.standard.thread.link`, inside the document's `links` | the author |
| thread `createdAt` | `publishedAt` | |
| `title`, `textContent`, `content`, `tags`, `updatedAt` | same names (standard.site's own fields) | |
| `dev.atmoboard.channel` (sidebar entry) | **`site.standard.thread.channel`**: `thread`, `section`, `position`, `icon`, `description` | the forum |
| `dev.atmoboard.post` | **`site.standard.thread.post`**: `thread`, `replyTo`, `textContent` (required), `content`, `labels`, `createdAt`, `updatedAt` | the author |
| `dev.atmoboard.override` | **`site.standard.thread.override`**: `subject`, `action` (move, rename, hide, unhide, lock, unlock, pin, unpin), `toThread`, `title`, `until`, `actor`, `reason` | the forum |
| `setTrustLevel`, `ban` overrides | stay in `dev.atmoboard.override` | the forum |
| Follow the forum, upvote a thread | `site.standard.graph.subscription`, `site.standard.graph.recommend` | the member |

This keeps every rule from `docs/all-threads.md` intact:
- **Threads all the way down.** A channel is a top-level thread document. A `site.standard.thread.channel` record from the forum features it in the sidebar, and deleting that record demotes it.
- **Untitled chat.** A channel's chat is the `site.standard.thread.post` records whose `thread` is the channel's own document.
- **One post model for chat and forum.** `site.standard.thread.post` is used for both (requirement 9), and it settles draft-0 finding 2.
- **Authors' records are never rewritten.** Moves, renames, locks, pins and hides are forum-signed overrides (research notes §4.1: the author decides *what you write*, the forum decides *whether it counts*). An override only counts when it's written by the repo that owns the publication its subject belongs to.

**Why `thread.link`?** The thread group can't also have a record named `thread`, so the object that marks a document as a thread is `site.standard.thread.link`, named after the `links` field it lives in.

**Why `links`?** standard.site's FAQ allows extra properties, but `links` is the field it defines for "relationships between this document and external resources", and it's an open union. A `site.standard.thread.link` object there is a sanctioned extension point. It marks the document as a thread, so readers can tell threads from articles, and it says where the thread sits. Vanilla standard.site readers ignore it and still list the thread as a document on the forum's site.

**Free side effect.** `site.standard.thread.post` works on *any* `site.standard.document`, so it doubles as a comment record for Leaflet, pckt and other blogs (see `examples/8-article-comment.json`). That fills the gap people currently patch with `bskyPostRef` or the unofficial `site.standard.document.comment`.

## Files
- `lexicons/site.standard.thread.link.json`: an object, not a record, carried in a document's `links`.
- `lexicons/site.standard.thread.post.json`, `site.standard.thread.channel.json`, `site.standard.thread.override.json`: records.
- `examples/1–10`: the forum publication, a channel document and its sidebar entry, a thread document, a chat post, a reply, a reply to a reply, a comment on a real Leaflet article, a lock override and a move override.
- `demo/standard-site-website.html`: the standard.site website demo, a frontend-only reader that renders real publications using only `site.standard.*` fields.
- `standard-site-remit.md`: what standard.site covers today.
- `archive/draft-0/`: the first baseline (a separate thread record, then named garden.msg.thread) and the Colibri and atmoBB explorations.

**Validation.** Checked with `@atproto/lexicon` against the live `site.standard.*` schemas. All 10 examples pass. A post without `thread` or `textContent`, a channel without `position`, an override without `action`, and a thread document without `title` are all rejected. One caveat: validators don't look inside open unions, so a malformed `site.standard.thread.link` in `links` passes standard.site validation, and apps have to validate it themselves.

## Lessons from the demo (real data, 27 Oct 2026)
- **`textContent` isn't reliable upstream.** Leaflet writes none, standard.site's own docs put MDX source in it, and stevedylan.dev fills it in only sometimes. That's why `site.standard.thread.post` *requires* `textContent`, and threads should always write it too.
- **Leaflet has its own comments**, so `showComments` appears in its publication preferences. That's worth comparing before proposing `site.standard.thread.post` upstream as a comment record.

## Open questions
1. **Public repos or public spaces?** standard.site's reach comes from public repo records: Bluesky link cards, docs.surf and the search indexes all read the firehose. atmo-board plans to keep forum content in the group's spaces, with public channels in a public space (`atmospheric-group.md`, "What this changes" §1). Records in a space may never reach those indexes. Options: write public threads to authors' repos, mirror them out of the space, or give up the discovery benefit.
2. **`links` is a single union, not an array** (standard.site issue #17). If upstream turns it into an array, existing thread records change shape. If it stays single, threads take the only slot. Proposing the array fix upstream would make `links` the right home for relationships like this. The fallback is a top-level `parent` property, which the FAQ allows.
3. **Titles are required.** `dev.atmoboard.thread` allows untitled threads, but `site.standard.document` doesn't. Channels have names and named threads have titles, so only a hypothetical untitled thread is lost. Is that acceptable?
4. **`publishedAt` vs `createdAt`.** For a thread they're the same moment, so this is a rename only.
5. **Which forum owns a thread?** The document's `site` names the forum. A thread can't be cross-posted into two forums, and that matches requirement 16 (one install is one forum).
6. **What to propose first.** `site.standard.thread.post` is generic enough to stand as standard.site's comment record on its own, so it's the easiest first proposal. `thread` comes next. `channel` and `override` are forum-specific and are the ones upstream is most likely to question.
7. **Who is the author?** standard.site has no author or profile lexicon (an author-lexicon PR was closed and a byline issue is open). A record's author is the repo DID in its at-uri, and the name shown is that DID resolved to a handle. Display names and avatars come from outside standard.site (for example `app.bsky.actor.profile`). Forum threads need both, so either standard.site gains a small profile record or threads depend on another lexicon for them.
