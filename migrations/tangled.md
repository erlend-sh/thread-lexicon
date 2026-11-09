# Tangled → garden.msg

Tangled (`org.tangled.*`) is a git forge on atproto. Its issue tracker is the part that overlaps with garden.msg. A `track.ticket` is an issue, or a pull request when `targetBranch` is set. `feed.comment` holds the discussion, `feed.reaction` holds the reactions, and `feed.subscription` holds the follows.

## Where Tangled's records live

Tangled is the one app here where discussion records don't live in their authors' repos. Every repository has its own DID and atproto account on its knot. Tickets, comments and reactions are written into that repository account through the knot. The knot checks permissions, stamps each record with the editor's DID (`x-tngl-editor`), and mints the record key. Authors can confirm a record is theirs with a `graph.attestation` in their own PDS.

garden.msg assumes the opposite: authors write threads and posts in their own repos, and the group acts only through overrides. That's gap G9 below, and it decides which of two paths Tangled takes.

## Record mapping

| Tangled | garden.msg | Notes |
|---|---|---|
| repository (its DID account) | `.group` | Each repository account writes one `.group`. `name` and `description` come from the repo, and `url` is its tangled.org page. Tangled doesn't use channels, so a repo's tickets sit directly in the group, with no `parent`. |
| `track.ticket` | `.thread` + opening `.post` | `title.text`→`title` (inline markdown flattened to plain text), `createdAt`→`publishedAt`. `body` (`markup.markdown`) moves to the opening post as `defs#markdown`. Its `blobs` (images, video) need G2. `labels` carries over. |
| `ticket.state` | `.override` | `closed` and `completed` become a `lock` override written by the repository account. The difference between them (and reopening) needs a status or `close` action (G6). |
| `ticket.tangledLabels` | `.thread.tags` | Label definitions are per repo, so a tag is the label's name. Colours and the label catalogue stay in `org.tangled.label.*`. |
| `ticket.assignees`, `targetBranch`, `review.patch` | stays app-specific | Assignment and pull requests are forge features. A pull request is still a thread, with its patches as Tangled sidecars. |
| `feed.comment` | `.post` | `subject`→`thread` (the ticket's thread), `replyTo`→`replyTo`, `body`→`textContent` and `#markdown`. `embed` (`embed.commit`) stays in `content` as a Tangled format. Comments on patches point at the pull request's thread. Comments on strings stay app-specific. |
| `feed.reaction` | `.reaction` | `subject`→`subject`, `reaction`→`emoji`. Tangled's eight fixed emoji all fit garden.msg's single-grapheme `emoji`. |
| `feed.subscription` (user PDS) | `.subscription` | `subject#repo`→`group`. `subject#record`→`group` + `thread`. `ignore` (mute) has no public equivalent: garden.msg keeps muting private, so it stays a Tangled preference. |
| `feed.star` | stays app-specific | Starring a repository isn't a vote on a post. Starring a ticket could become a `.recommend`. |

## Two paths

**A. The repository writes garden.msg records (recommended).** Tangled keeps its storage model. The knot writes `garden.msg.thread`, `.post` and `.reaction` into the repository account, exactly as it writes tickets and comments today, and keeps the editor stamp and attestations. This needs garden.msg to accept records written by a host on someone's behalf (G9). In exchange, Tangled keeps knot-side permission checks, and other garden.msg clients can read a repo's issues as a group's threads.

**B. Comment on tickets as they are.** Tangled keeps `track.ticket`, and garden.msg clients reply to a ticket directly with a `.post` whose `thread` is the ticket's URI. This is open question 3 ("other roots"). It needs no change on Tangled's side, but those posts live in authors' PDSes, outside the knot's permission checks, and Tangled would have to choose whether to show them.

## Rollout (path A)

1. Each repository account writes a `.group`.
2. Tangled's appview reads garden.msg threads, posts and reactions alongside tickets and comments.
3. The knot writes garden.msg records for new issues, comments and reactions. State changes are written as overrides.
4. Backfill is easy compared with the other apps: every ticket, comment and reaction lives in a repository account the knot controls, so it can migrate a whole repository in one pass, with no member sign-ins.

## Blockers

G9 (host-written records) for path A. G2 for markdown blobs, and G6 for closed versus completed.
