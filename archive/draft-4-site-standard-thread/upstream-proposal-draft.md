# proposal(lexicon): `site.standard.thread.*`, threads, replies and comments

_Draft 0, written for an issue at tangled.org/standard.site/lexicons. It's expected to change after more iteration on the demo._

## Summary
standard.site describes publications and documents but has nothing for conversation. Today comments are handed to Bluesky through `bskyPostRef`, or kept in each platform's own lexicon (Leaflet's comments, the unofficial `site.standard.document.comment`). This proposal adds a small `thread` group, sitting beside `graph` and `theme`, that covers two cases with the same records:

- **Comments on any document.** A reply to a Leaflet post, a pckt article or a blog entry.
- **Forums and chat built as websites.** A forum is a publication, each thread is a document, and replies are posts.

## Why this belongs in standard.site
Nothing in `site.standard.publication` or `site.standard.document` is specific to articles. A publication is a `url` and a `name`, and a document is a `title` at a `path` with an open `content` union. A forum thread fits that shape exactly. Writing threads as documents means every existing reader and index (Bluesky link cards, docs.surf, pckt and the search engines) shows forum threads without changes. Verification works too: the forum's thread page carries `rel="site.standard.document"` pointing at the author's record.

## Lexicons
| NSID | Kind | Purpose |
|---|---|---|
| `site.standard.thread.post` | record, tid, in the author's repo | A reply, comment or chat message. `thread` (at-uri of a document), optional `replyTo` (at-uri of a post), `textContent` (**required**), `content` (open union), `labels`, `createdAt`, `updatedAt`. |
| `site.standard.thread.link` | object, in a document's `links` | Marks a document as a discussion thread. Optional `parent` (at-uri of another thread document) for nesting, such as a thread inside a channel. |
| `site.standard.thread.channel` | record, written by the publication owner | Features a top-level thread in the site's navigation: `thread`, `section`, `position`, `icon`, `description`. |
| `site.standard.thread.override` | record, written by the publication owner | Moderation on records the site can't edit: move, rename, hide or unhide, lock or unlock, pin or unpin. Fields are `subject`, `action`, `toThread`, `title`, `until`, `actor` and `reason`. It only counts when written by the repo that owns the subject's publication. |

The schemas and 10 example records are in `lexicons/` and `examples/`. All of them validate against the published `site.standard.*` schemas.

## Design notes
- **Authors own their words.** Posts and thread documents live in their authors' repos. The publication owner never rewrites them and acts only through `override` records.
- **`textContent` is required on posts.** Real-world documents often leave it out (we found Leaflet writes none, for example). Requiring it on posts guarantees that any reader can show any comment.
- **Comments can be adopted on their own.** A blog platform can use `thread.post` alone. `thread.link`, `thread.channel` and `thread.override` are only needed for forum-style sites.
- **Records only.** Queries and views (listing a thread's posts, counting replies) stay with each app or indexer, as with `graph.subscription` and `graph.recommend` today.

## Related issues
- **#17, `links` is a union, not an array.** `thread.link` lives in `links`, so making it an array would let a thread carry other relationships too.
- **#19, `site.standard.series`.** That proposal also gives documents a parent and child structure, so it's worth aligning the two.

## Implementations
- **atmo-board** (a forum and chat app, Discourse-style): in progress, built against this draft.
- **A frontend-only reader demo** that renders standard.site publications from records.
