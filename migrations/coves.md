# Coves → garden.msg

Coves (`social.coves.*`) is an aggregator in the style of Reddit or Lemmy. People submit posts to communities, comment in nested trees, and vote up and down. It's the furthest from a classic forum, but its core still maps: community to group, post to thread, comment to post, vote to recommend.

## Record mapping

| Coves | garden.msg | Notes |
|---|---|---|
| community (DID) | `.group` | Each community writes a `.group`, and its at-uri replaces the bare `community` DID. |
| `community.postv2` | `.thread` + opening `.post` | `community`→`group`, `title`→`title` (G5), `tags`→`tags`, `labels`→`labels`, `createdAt`→`publishedAt`. `content` with `facets` moves to the opening post's `textContent` and `content` (G3). `embed` needs G2. |
| `community.comment` | `.post` | `reply.root`→`thread`, where the root is the post's new thread. `reply.parent`→`replyTo`, left out when the parent is the root post. That's the case `parent == root` in garden.msg's README. |
| `feed.vote` | `.recommend` | `subject` and `direction` (`up`/`down`) carry over unchanged. Coves is where `direction` came from. |
| `crosspostOf`, `crosspostChain` | stays app-specific | A sidecar pointing at the garden.msg thread, or a field in a Coves `content` format. |
| `federatedFrom`, `originalAuthor`, `bridgedStats` | stays app-specific | Bridge metadata. Counts in particular are a view in garden.msg, not a record field. |
| `location`, `langs` | `content` / sidecar | No garden.msg field yet. |

## The root post

A Coves comment's root is the submitted post, while a garden.msg post's `thread` is the container. In garden.msg the submitted post becomes a container thread plus an opening post, so a comment's `thread` is the container and comments on the submission itself have no `replyTo`. An importer has to handle three cases:

- root = parent = the post: `thread` is set, `replyTo` is absent
- parent is a comment: `replyTo` is that comment's new URI
- votes on the post: `subject` becomes the opening post (or the thread, if Coves wants votes to rank threads; garden.msg allows both)

## Rollout

1. Each community writes its `.group`.
2. The AppView reads garden.msg threads alongside `postv2` in feeds and comment trees.
3. New posts, comments and votes are written as garden.msg, with Coves extras as sidecars.
4. Users are backfilled on sign-in. Bridged content is written by the bridge's own account, so it migrates in one pass.

## Blockers

G2 for embeds is the main one, since many Coves posts are links or media. Then G5 (untitled posts) and G3 (facets).
