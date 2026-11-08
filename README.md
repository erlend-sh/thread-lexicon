# Atmospheric Threads: `garden.msg` (draft 9)

A shared lexicon for threaded discussion on atproto, covering forum threads, chat channels and comments on articles. Any app that speaks it can read and write the same discussions, whether it shows them as a forum, a chat or a comment section.

It's a spiritual fork of [standard.site](https://standard.site) that keeps standard.site's shape and field names but lives in its own namespace. The lexicon lives under `garden.msg.*`, on the msg.garden domain.

Schemas are in `lexicons/`, and example records are in `examples/`.

## Model

- A **group** is a community, such as a forum or a team. It plays the part of a standard.site publication.
- A **thread** is the container of a discussion: a title and a position in its group, with no text of its own. Threads nest through `parent`, so a group's threads form a tree: top-level threads (can be featured as **channels** in the group's sidebar), threads inside them, and sub-threads below those, as deep as needed. The record is `garden.msg.thread`: the thread at the heart of the thread lexicon.
- A **post** is every message: an opening post, a reply, a chat message or a comment.
- **Authors own their words.** Threads, posts, votes, reactions and subscriptions live in their authors' repos. The group acts on them only through `.channel` and `.override` records in its own repo.
- **Records only.** Counts, lists and latest activity are computed by indexers and served as views (see Views), never stored in records.

## Records

| Record | Written by | Fields (**required**) | Forked from |
|---|---|---|---|
| `.group` | the group | **`url`**, **`name`**, `description`, `icon`, `basicTheme` (`site.standard.theme.basic`), `labels`, `preferences.showInDiscover` | `site.standard.publication` |
| `.thread` | its author | **`group`**, **`title`**, **`publishedAt`**, `parent`, `path`, `description`, `tags`, `labels`, `updatedAt` | `site.standard.document`, with no body |
| `.post` | its author | **`thread`**, **`textContent`**, **`createdAt`**, `replyTo`, `content`, `document`, `labels`, `updatedAt` | (new) |
| `.channel` | the group | **`thread`**, **`position`**, **`createdAt`**, `section`, `icon`, `description` | (new) |
| `.override` | the group | **`subject`**, **`action`**, **`createdAt`**, `toThread`, `title`, `until`, `actor`, `reason` | (new) |
| `.subscription` | the subscriber | **`group`**, **`createdAt`**, `thread`, `notify` | `site.standard.graph.subscription` |
| `.recommend` | the voter | **`subject`**, **`createdAt`**, `direction` | `site.standard.graph.recommend` |
| `.reaction` | the reactor | **`subject`**, **`emoji`**, **`createdAt`**, `cid` | (new) |

Pointers are plain at-uris, not strongRefs, because posts get edited. `defs` holds `#link`, `#markdown` and the view types. `textContent` and `#markdown` allow up to 100,000 graphemes, enough for long forum posts.

Groups and threads are verified the same way as in standard.site, at `/.well-known/garden.msg.group` and with `<link rel="garden.msg.thread">`.

## Smallest possible thread

A thread needs only two record types and six required fields:

```json
// garden.msg.thread
{ "group": "at://did:plc:forum/garden.msg.group/self", "title": "FOSDEM planning", "publishedAt": "2026-11-08T12:00:00Z" }

// garden.msg.post, one per message, the opening post included
{ "thread": "at://did:plc:alice/garden.msg.thread/3m4abc", "textContent": "Who's going?", "createdAt": "2026-11-08T12:00:00Z" }
```

A minimal reader fetches a thread and the posts whose `thread` points at it. It sorts them by `createdAt` and shows the title, then each post's `textContent` with its author's handle. It can ignore `replyTo`, `content`, votes, reactions, subscriptions, channels and the group record. The one thing it should still read is `.override` with `action: hide`, so it doesn't show what the group has hidden.

## Threads and posts

**The opening post is a `.post` record, not part of the thread.** The thread record holds only the title, and the text that starts the discussion is a separate `.post`: the opening post (OP), which is the thread author's first post in it that answers no other post. That way the OP is edited, voted on, moderated and rendered like every other post. Clients write the thread and its OP together in one `applyWrites`. Records only point at records that already exist, so the post names the thread and never the other way round. A thread can have no OP: a channel's chat is just its posts.

**Root and parent.** `thread` is the root and `replyTo` is the parent, in Bluesky, Barazo and Coves terms. A top-level post has no `replyTo`, where those lexicons set `parent == root`. Linear apps such as forums and chat read `thread` and ignore `replyTo`. Nested or vote-sorted apps rebuild the tree from both fields.

**Descriptions.** A thread's `description` is optional. When it's absent, apps show the start of the OP's `textContent`, up to 300 characters.

**Rich text.** `textContent` is required, so every reader can show every post. It holds plain text, with no markdown. `content` is an open union for formatting, and `defs#markdown` (`{ text }`, CommonMark) is the shared format that every threads app should read and write. Apps may add their own formats too. Raw HTML in markdown isn't rendered.

## Moderation

A group can't edit its members' records, so it applies `.override` records on top of them. Each one names a `subject` (a thread or a post) and an `action`:

- `move`: a thread gets a new parent, or a post a new thread (`toThread`).
- `rename`: a thread gets a new title (`title`).
- `hide` / `unhide`: readers stop seeing the subject (staff still can).
- `lock` / `unlock`: only staff can post in the thread.
- `pin` / `unpin`: the thread is shown first in its parent.

`until` makes a pin, lock or hide lapse. `actor` names the staff member, and `reason` is shown to readers. An override only counts when it's written by the repo that owns the subject's group. For each subject and action, the newest override wins.

A `.channel` record features a thread in the group's sidebar, under a `section` and at a `position`. Deleting the record demotes the thread but leaves it in place.

## Votes and reactions

These are separate records, because they count differently.

- **`.recommend` is a vote.** Each person has one per subject, and the newest counts. `direction` is `up` or `down`, and absent means `up`, so a plain recommend reads like standard.site's. Aggregator-style apps sort by score, and forum and chat apps can ignore down votes. `direction` is on trial: if it doesn't fit, it can move to its own `.vote` record.
- **`.reaction` is an emoji.** A person can leave several on one subject, one per emoji, and a like is ❤️. `subject` can be any record, not only a thread or a post. The optional `cid` pins the reaction to one version of its subject.

## Subscriptions

A subscription with only `group` means joining the group, and only these count toward membership. Adding `thread` narrows the subscription to that thread and everything under it, at any depth. To follow a channel, point at its thread, not at its `.channel` record.

`notify` sets what reaches you: `posts`, `threads` (new threads only) or `none` (follow quietly). When it's absent, the default is `threads` for a group and `posts` for a thread.

Indexers apply these rules:
- The most specific subscription wins.
- There's one record per (`group`, `thread`) pair, and the newest counts. Apps update a subscription in place and unsubscribe by deleting it.
- A subscription whose `thread` isn't in its `group` is ignored.

Subscriptions are public, so `none` means following quietly, not muting. Muting is a private preference and doesn't belong in a public record.

## Articles

Threads and standard.site articles connect in two ways:

- **Comments.** A `.post` whose `thread` is a `site.standard.document` is a comment on that article. To follow the comments, write a subscription with `group` set to the publication and `thread` set to the document.
- **Publishing both.** The same writing can be both a `.post` and a `site.standard.document`. That lets a blog post open a thread and get replies, or a long forum post reach reader apps. The post's `document` field names the article, and the article's `links` union carries a `defs#link` naming the post. A pair only counts when both records are in the same repo and each points at the other. Validators don't look inside open unions, so apps have to check `defs#link` themselves.

## Views

Reply counts, posters and activity are aggregates over other people's repos, so indexers serve them in shared view shapes:

- **`defs#threadView`**: the record, the effective title and parent after overrides, the OP, an excerpt, `postCount`, `posters` (up to 5), `lastPostAt`, `score` and `state` (`#moderationState`).
- **`defs#postView`**: the record, `replyCount`, `score`, `reactions` (`#reactionCount`) and `state`.
- Both carry an optional `viewer` (`#viewerState`) with the signed-in viewer's own recommend and its direction, their reactions, and, for a thread, their subscription and effective `notify`, so clients can show and undo them.

Four queries serve them:

| Query | Parameters | Returns |
|---|---|---|
| `getGroup` | `group` | the group record, its channels in section and position order (each with its `threadView` and thread count), member count, staff and viewer state |
| `listThreads` | `parent` or `group`, `sort` (`latest`, `new`, `top`), `tag`, `limit`, `cursor` | `threadView[]`, pinned first under a parent. With `group` alone, every thread that isn't a channel. Hidden threads only for staff. |
| `getThread` | `thread`, `order` (`oldest`, `newest`), `limit`, `cursor` | the `threadView` and its `postView[]`. `thread` can be a `site.standard.document`, for its comments. |
| `listReactions` | `subject`, `emoji`, `limit`, `cursor` | who reacted with what, newest first |

`updatedAt` keeps standard.site's meaning, the author's last edit. A thread's activity is its newest post's `createdAt`. An author is a repo DID, and display names and avatars come from elsewhere, such as `app.bsky.actor.profile`.

## Open questions

1. **Public spaces.** We lean towards keeping a group's threads and posts in its atproto Spaces, including public ones, with the `.group` record in a public repo as the public announcement. Spaces aren't relayed: apps sync them through a Spaces-mode Jetstream on their backend, so browser clients need a read API in front of it. Article comments can stay in public repos.
2. **Space-qualified URIs.** One author can write the same collection and record key into two spaces, so `thread`, `replyTo` and `subject` may need a space qualifier. This depends on how Spaces addresses records.
3. **Other roots.** Should `thread` accept any record, such as a calendar event, a Bluesky post or a wiki note? If it does, the root's owner would moderate and `.subscription.group` would become optional. The alternative is that those apps write a `.thread` that points at the record.
4. **Required titles.** Every thread needs a title. Untitled chat lives in a channel's posts, and `topic` is reserved for later.

## Prior art

- Thread lexicons on atproto:
  - Colibri: `social.colibri.beta.thread`
  - atmoBB: `app.atmobb.discussion.*`
  - Barazo: `forum.barazo.topic.*`
  - UserInput: `app.userinput.discussion`
  - Coves: `social.coves.community.postv2`, `social.coves.community.comment`, `social.coves.feed.vote`
  - Roomy: a planned move to atproto Spaces
- [SIOC](https://rdfs.org/sioc/spec) has the same model: a Site holds Containers of Posts, with `has_reply`, `has_subscriber` and `has_creator`, and access is set at the container.
