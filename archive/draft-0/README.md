# Atmospheric Threads: `garden.msg` baseline (draft 0)

This is a standard.site-style baseline for threads. It takes the common ground of **Colibri** (`social.colibri.beta.thread`, group chat) and **atmoBB** (`app.atmobb.discussion.thread` / `reply`, forum). Its namespace is `garden.msg`. Both NSIDs resolve through a single DNS record, `_lexicon.msg.garden`.

## The approach, borrowed from standard.site
`site.standard.document` is metadata that a platform writes next to its own content: `site`, `title`, `textContent`, an open-union `content`, `tags`, `publishedAt` and `updatedAt`. `garden.msg.thread` does the same for threads. An app keeps its native thread record, and it either writes a baseline record too or makes its native record conform to it. Every app can read `textContent` as plain text. `content` is an open union, where each app puts its own rich format under its own `$type`.

## `garden.msg.thread` (key `any`)

| Baseline field | Colibri `beta.thread` | atmoBB `discussion.thread` | Notes |
|---|---|---|---|
| **title** (req) | `name` (1–128 chars) | `title` (300 graphemes) | Uses the looser limit, so both apps' titles fit |
| **container** (req, uri) | `channel` (space-ref) | `board` (at-uri) | A generic uri, so it accepts an at-uri, a space ref or an https URL |
| **createdAt** (req) | `createdAt` | `createdAt` | |
| author (did) | `createdBy` (written by the community) | the repo owner | Needed when someone else writes the record |
| origin (uri) | `anchor` (spaceRecordRef) | none | A chat thread branched from a message |
| textContent / content | none (the anchor message holds the text) | `body` (rich blocks) | Same pattern as standard.site |
| tags | none | `tags` (max 8) | |
| locked | `locked` | moderation action `lock` | In atmoBB, a lock is a forum-side moderation record |
| closedAt | `closedAt` | none | |
| updatedAt | none | `editedAt` | |
| url | none | none | Matches standard.site's canonical link |
| labels | none (Colibri uses labels) | none | selfLabels, as in standard.site |

**Deliberately left out:** visibility (`visibleToRoles` and `visibleToMembers`), bridge attribution, polls and pins. These are app-specific, or they are access control, which belongs to the container or space and not to the shared metadata.

## `garden.msg.post` (optional module, key `tid`)
A reply or a message in a thread. It requires `thread` (uri), `textContent` and `createdAt`. It can also take `parent` (uri), `author`, `content` (open union) and `updatedAt`. It covers atmoBB `reply` (thread, plus an optional parent) and Colibri `beta.message` (an optional `parent` recordRef, where the thread is implicit in the space).

## Open questions
1. **References.** atmoBB pins versions with strongRefs. Colibri uses `{did, rkey}` and `space-ref`, a permissioned-spaces format that the lexicon spec doesn't define yet. The draft uses plain `uri` strings so that both fit. Should we define a typed ref union instead?
2. **Record key `any`.** atmoBB uses `tid` in the author's repo, and Colibri uses `literal:self` inside the thread's own space. `any` allows both, at the cost of some guarantees.
3. **Mirror or conform?** Should apps write a separate `garden.msg.thread` record, or adopt it as their native thread record and add their own fields to it?
4. **Is `garden.msg.post` in scope for v0,** or should the baseline be thread metadata only, the way standard.site has no comment record?
5. **Locked vs. closed.** Is having both right? Colibri has both. atmoBB only has lock, and it records that as a moderation action.

Validated with `@atproto/lexicon`: both lexicons load, three example records pass, and a post without `thread` is rejected.
