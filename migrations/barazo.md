# Barazo → garden.msg

Barazo (`forum.barazo.*`, github.com/singi-labs/barazo-lexicons) is the closest prior art. It already uses root and parent, markdown content and directional votes, so the migration is mostly renaming.

## Record mapping

| Barazo | garden.msg | Notes |
|---|---|---|
| community DID | `.group` (community repo) | Barazo identifies a community by its DID alone. Each community writes one `.group` record, and its at-uri replaces the bare DID wherever a record names the community. |
| category (record-key slug) | `.thread` + `.channel` (community repo) | Each category becomes a top-level container thread and a `.channel`. Topics point at it through `parent`. |
| `topic.post` | `.thread` + opening `.post` | `title`→`title`, `community`→`group`, `category`→`parent` (the category's thread URI), `tags`→`tags`, `labels`→`labels`, `publishedAt`→`publishedAt`. `content` moves to the opening post. `site` matches garden.msg's article pairing: the opening post's `document` field and a `defs#link` on the article. |
| `topic.reply` | `.post` | `root`→`thread`. `parent`→`replyTo`, except when `parent == root`, where `replyTo` is left out. `content`, `labels` and `createdAt` carry over. |
| `richtext#markdown {value}` | `defs#markdown {text}` | A field rename. `textContent` is the markdown stripped to plain text. |
| `facets`, `langs` | `content` / sidecar | `langs` has no garden.msg field yet. Facets stay alongside the markdown (G3). |
| `interaction.vote` | `.recommend` | `direction: up` carries over, and Barazo can add `down` later as it planned. `community` is dropped, since the subject's thread names its group. |
| `interaction.reaction` | `.reaction` | `#heart`→❤️ and `#thumbsup`→👍. `#like` becomes ❤️ or stays a vote, as Barazo prefers. Community-defined types need G4. |
| `actor.preferences`, `actor.signature` | stays app-specific | Not part of garden.msg. |

## Rollout

1. Each community writes its `.group`, plus a `.thread` and `.channel` per category.
2. The AppView reads garden.msg records alongside `forum.barazo.topic.*`.
3. New topics, replies, votes and reactions are written as garden.msg.
4. Members are backfilled on sign-in. Since Barazo replies already carry root and parent, the conversion is mechanical.

## Blockers

G4 for custom reaction types. `langs` would need a field on `.post`, which is worth adding upstream. G1 means strongRefs become plain URIs.
