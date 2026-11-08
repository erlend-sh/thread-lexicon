# UserInput → garden.msg

UserInput (`app.userinput.*`) is a feedback board. A space owner creates a space, people post discussions into it, others reply and vote, and the owner sets statuses such as "planned" or "implemented". It's a forum with voting and a roadmap on top, so the thread core maps directly and the roadmap stays app-specific.

## Record mapping

| UserInput | garden.msg | Notes |
|---|---|---|
| `space` (owner repo) | `.group` | `name`→`name`, `icon`→`icon`. The space's tag list stays on `app.userinput.space`. The group's `url` is the space's page. |
| `discussion` | `.thread` + opening `.post` | `space`→`group`, `title`→`title`, `tags`→`tags`, `createdAt`→`publishedAt`. `body` moves to the opening post. `images` need G2. |
| `reply` | `.post` | `subject`→`thread`, `parent`→`replyTo`, `body`→`textContent`. |
| `upvote` / `downvote` | `.recommend` with `direction` | Two record types become one with `up` or `down`. UserInput keys these by `any` to keep one vote per subject. garden.msg gets the same result with "the newest counts". |
| `edit` | update the record in place, setting `updatedAt` | garden.msg records are edited in place, and the edit record isn't needed. If UserInput wants an edit history, the indexer keeps it. |
| `hide`, `pin` | `.override` `hide` / `pin` | Written by the space owner. |
| `lock` (with `lockedAt` cutoff) | `.override` `lock` | garden.msg locks stop new posts. UserInput's cutoff also hides later replies, which an indexer can do by comparing `createdAt` with the override's `createdAt`. |
| `status` | stays app-specific (G6) | `app.userinput.status` keeps pointing at the discussion, now the garden.msg thread. `duplicate` could also write an `.override` `move` or `lock`. |
| `member`, `ban` | stays app-specific (G6) | Staff roles and bans aren't part of garden.msg. |
| `visited`, `checkedNotifications` | stays app-specific | Read state and private preferences. |

## Rollout

1. Space owners' spaces get a `.group`, written on the owner's next sign-in.
2. Read both: the board reads garden.msg threads alongside discussions in each space.
3. Write garden.msg for new discussions, replies and votes. Statuses keep their own records, now pointing at garden.msg threads.
4. Backfill members on sign-in, rewriting status and moderation subjects through the URI map.

## Blockers

G2 for images. Statuses stay app-specific, and UserInput is the case for a shared `status` override if other apps want one (G6).
