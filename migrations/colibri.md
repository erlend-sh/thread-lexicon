# Colibri → garden.msg

Colibri (`social.colibri.beta.*`) is a Discord-style chat app built on atproto Spaces. Communities, channels and threads are spaces, each with a `self` record written by the community. Messages and reactions live in members' permissioned repos for the channel's space. Of the five apps, it's the closest to garden.msg's group model, but it depends most on how Spaces work.

## Record mapping

| Colibri | garden.msg | Notes |
|---|---|---|
| `community` (profile space) | `.group` | `name`, `description`, `picture`→`icon`. `managingApp` and settings stay app-specific. |
| `channel` (channel space, `self`) | `.thread` + `.channel` | A text channel is a top-level container thread. `name`→`title`, `description`→`description`. Posting and visibility rules (`allowedRoles`, `visibleToRoles` and so on) stay app-specific. They're the space's access policy, not record fields. |
| `category` | `.channel.section` and `position` | `channelOrder` becomes each channel's `position`. |
| `channel.thread` / `beta.thread` (thread space, `self`) | `.thread` | `name`→`title`, `channel`→`parent`, `createdAt`→`publishedAt`. `locked` and `closedAt` become `.override` `lock` (closing needs G6). `anchor` (the message a thread was opened from) has no field yet, and could become a post-level `document`-style link. |
| `message` | `.post` | `text`→`textContent`, `parent`/`parentUri`→`replyTo`, `updatedAt`→`updatedAt`. `thread` is the channel or thread's garden.msg URI. `facets` go in `content` (G3), `attachments` need G2, and `forward` stays app-specific. |
| `reaction` | `.reaction` | `target`/`uri`→`subject`, `emoji`→`emoji`. Custom shortcodes need G4. |
| `moderation`, `role`, `actor.*`, `bridge.*` | stays app-specific | Moderation in Colibri is enforced by the space authority, and the record is an audit log. |

## Who writes threads

In Colibri the community writes a thread's `self` record and names the opener in `createdBy`. In garden.msg the thread's author writes it in their own repo. Two options:

- The opener writes the `.thread` into the channel's space from their own repo, and the community moderates it with overrides. This matches garden.msg as it is.
- garden.msg allows a group-written `.thread` to name its opener. That's a spec change, but it would also suit forums that pre-create threads.

## Rollout

Colibri can't start until open questions 1 and 2 in the README are settled (G7). Then:

1. In each community, write a `.group` in the profile space and a `.thread` plus `.channel` per channel, all in community-owned spaces, so it's one pass.
2. Read both in `listMessages` and the channel views.
3. Write garden.msg for new messages and reactions.
4. Backfill members on sign-in. Their records are in permissioned repos, which the member's session can rewrite.

## Blockers

G7 (space-qualified URIs) comes first. Then G2, G3 and G4. Thread authorship needs a decision.
