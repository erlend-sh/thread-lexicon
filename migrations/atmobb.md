# atmoBB → garden.msg

atmoBB (github.com/keithk/atmoBB) is a classic bulletin board. The forum account owns its profile, boards, categories, staff grants and moderation log. Members own their threads, replies, memberships and board watches. Its model is close to garden.msg's, so most records map one-to-one.

## Record mapping

| atmoBB | garden.msg | Notes |
|---|---|---|
| `forum.profile` (forum repo, `self`) | `.group` | `name`, `description`, `avatar`→`icon`. The forum's URL becomes `url`. Theming, custom CSS, ranks, rules and the homepage stay in `app.atmobb.forum.profile`. |
| `forum.board` (forum repo) | `.thread`, plus `.channel` for top-level boards | A board is a container thread written by the forum. `name`→`title`, `description`→`description`, `parent`→`parent`. A top-level board gets a `.channel` with `position` from `order`, `icon` from `emoji` and `section` from its category's name. `color`, topic federation and `access` stay app-specific. |
| `forum.category` (forum repo) | `.channel.section` | Categories become section names on `.channel` records. There's no separate record. |
| `discussion.thread` (member repo) | `.thread` + opening `.post` | `board`→`parent` (the board's new thread URI), with `group` set to the forum's `.group`. `title`→`title`, `tags`→`tags`, `createdAt`→`publishedAt`, `editedAt`→`updatedAt`. `body` moves to the opening post. Both are written in one `applyWrites`. |
| `discussion.reply` (member repo) | `.post` | `thread`→`thread`, `parent`→`replyTo` (absent stays absent), `editedAt`→`updatedAt`. |
| `body` (block array) | `.post.textContent` + `content` | `textContent` is the blocks' plain text. Text, quote and code blocks convert to `#markdown`. Image blocks need gap G2, and meanwhile can stay as `app.atmobb.richtext.block` inside `content`. |
| `moderation.action` (forum repo) | `.override` for thread and post actions | `hide`/`unhide`/`lock`/`unlock`/`pin`/`unpin` on a thread or reply map directly, with `actor`, `reason` and `expiresAt`→`until`. Account actions (ban, warn, block, access and membership decisions) and stamps stay in `app.atmobb.moderation.action` (G6). |
| `forum.membership` (member repo) | `.subscription` with `group` only | Joining the forum. `wearing`, `pinned` and the guestbook settings stay on `app.atmobb.forum.membership`. |
| `forum.watch` (member repo) | `.subscription` with `thread` = the board, `notify: threads` | Watching a board for new threads. |
| `poll.vote`, `discussion.thread#poll` | stays app-specific | A sidecar `app.atmobb.discussion.poll` whose subject is the garden.msg thread (G8). |
| `actor.*`, `forum.stamp`, `forum.moderator`, `forum.accessRequest`, `extension.*` | stays app-specific | Not part of garden.msg. |

atmoBB has no likes or reactions today. If it adds them, it should use `.recommend` and `.reaction`.

## Rollout

1. **Forum records.** For each forum, write a `.group`, a `.thread` per board and a `.channel` per top-level board. These are in the forum's own repo, so this is one pass per forum.
2. **Read both.** Board and thread pages read `garden.msg.post` alongside `app.atmobb.discussion.reply`. `getBoardThreads` and `getThreadPage` merge the two.
3. **Write garden.msg.** `createThread` and `createReply` write garden.msg records. Polls are written as a sidecar.
4. **Backfill members** when they sign in: threads, replies, memberships and watches.
5. **Moderation.** Thread and post actions are written as `.override`. Earlier `moderation.action` records stay as the audit log.

## Blockers

G2 for image blocks. Everything else migrates without loss. atmoBB's strongRefs become plain URIs (G1).
