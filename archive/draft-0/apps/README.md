# Colibri and atmoBB on `garden.msg` (exploration 1)

Both apps follow the standard.site pattern. They write the shared `garden.msg.thread` record as their real thread record, put their own rich content in its open `content` union, and keep their app-only settings in records under their own namespaces. Everything here validates with `@atproto/lexicon`. Colibri's space type can't be checked, because the validator doesn't know the `space` type yet.

## atmoBB

| Before | After |
|---|---|
| `app.atmobb.discussion.thread` (author repo, tid) | **`garden.msg.thread`** (author repo, tid) |
| `board` | `container` |
| `title`, `tags`, `createdAt` | same names |
| `editedAt` | `updatedAt` |
| `body` (rich blocks), `poll` | `content` = `app.atmobb.discussion.defs#threadContent`, plus a plain-text `textContent` |
| `app.atmobb.discussion.reply` | **`garden.msg.post`**: `thread` (uri), `parent` (uri), `content` = `#postContent`, `textContent` |
| lock (moderation action) | stays a forum-side `app.atmobb.moderation.action` |

New file: `atmobb/lexicons/app.atmobb.discussion.defs.json` (`threadContent`, `postContent`, `poll`). The old `discussion.thread` and `reply` stay published and readable, and stop being written. Poll votes and moderation actions now point at `garden.msg.*` URIs.

## Colibri

| Before | After |
|---|---|
| `social.colibri.beta.thread` (self, in the thread's space, written by the community) | **`garden.msg.thread`** (self, same place, same writer) |
| `name` | `title` (Colibri still enforces its 128-char limit in the app) |
| `channel` (space-ref, `at://<did>/space/<type>/<key>`) | `container` (the same string; it is a valid uri) |
| `createdBy` | `author` |
| `locked`, `closedAt`, `createdAt` | same names |
| `anchor`, `visibleToRoles`, `visibleToMembers`, `bridged` | **`social.colibri.beta.thread.settings`** (self, same space, community-written) |
| `social.colibri.beta.channel.thread` space | its `collections` list swaps `beta.thread` for `garden.msg.thread` + `beta.thread.settings` |
| `social.colibri.beta.message` | unchanged (see finding 2) |

## Findings to feed back into the baseline
1. **Who writes `locked` and `closedAt`?** In Colibri the community writes the thread record, so these work. In atmoBB the author owns the thread record, and locking is a forum-side moderation record, so atmoBB can never set them. Either move thread state into a container-side record that both apps could write, or document that it is advisory and owner-written.
2. **`garden.msg.post` doesn't suit chat.** Colibri messages in a thread are the same `beta.message` records used in channels, and the thread is implied by the space. A required `thread` field would be redundant, and switching collections only inside threads would split their message model. Options: make `thread` optional when a space implies it, or keep `post` as a forum-only module.
3. **`origin` can't hold a space record yet.** A record in a Colibri space is addressed as `{space, did, rkey}`, and it has no single URI form. Colibri keeps `anchor` structured in its settings record. The baseline needs either a URI convention for space records or a structured ref type.
4. **atmoBB loses version pinning.** Its replies used strongRefs (uri + cid), and the baseline's plain `uri` drops the cid. An optional `cid` beside each reference, or a union of strongRef and uri, would fix it.
5. **Title length.** The baseline allows 300 graphemes, but Colibri caps titles at 128 chars. A long title from atmoBB is valid baseline data that Colibri can't store natively. Should the baseline set a lower common cap, or require truncating on display?
6. **`textContent` duplicates content.** atmoBB has to flatten its blocks into plain text on every write. That's the standard.site trade-off, and it's worth confirming the apps accept it.
7. **Extra fields are accepted.** The validator passes unknown top-level fields, so an app could attach its settings directly to the baseline record instead of using a separate record. A separate namespaced record (Colibri's `settings`) avoids name clashes, and I chose that for this draft.
