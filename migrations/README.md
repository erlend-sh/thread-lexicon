# Migrating to garden.msg

These plans show how five existing atproto discussion apps could move their threads, posts, votes and reactions onto `garden.msg.*`. Each plan maps the app's records to garden.msg, lists what stays in the app's own namespace, and gives a rollout order. They're proposals to discuss with each project, not commitments.

| App | Lexicons today | Plan |
|---|---|---|
| atmoBB | `app.atmobb.*` | [atmobb.md](atmobb.md) |
| Colibri | `social.colibri.beta.*` (on Spaces) | [colibri.md](colibri.md) |
| Barazo | `forum.barazo.*` | [barazo.md](barazo.md) |
| UserInput | `app.userinput.*` | [userinput.md](userinput.md) |
| Coves | `social.coves.*` | [coves.md](coves.md) |

## The common path

Every app follows the same four steps.

1. **Read both.** The app's indexer reads garden.msg records alongside its own, so threads written by other garden.msg apps show up. Nothing changes for existing users.
2. **Write garden.msg.** New threads, posts, votes and reactions are written as garden.msg records. App-specific extras go in sidecar records in the app's own namespace that point at the garden.msg record (see each plan).
3. **Backfill.** Group-owned records, such as the forum or community profile, boards and moderation, live in the group's repo, so the app can rewrite them in one pass. Member-owned records live in members' repos, and only a session for that member can rewrite them. So the app migrates each member's records the next time they sign in, with an OAuth scope that covers both namespaces. Members who never come back keep their legacy records, and the indexer keeps reading those.
4. **Stop writing legacy records.** Once most active members are migrated, the app stops writing its old post records. It can keep reading them indefinitely.

Backfilled records get new URIs. The indexer keeps a map from legacy URI to new URI, so old links, votes and replies still resolve. Votes and reactions that point at a legacy record are migrated along with their author, and their `subject` is rewritten through the map.

## Spec gaps the migrations hit

These come up in more than one plan. Each needs a decision in garden.msg before the affected migration can be lossless.

| # | Gap | Apps | Suggested change |
|---|---|---|---|
| G1 | **Strong refs.** All five apps point at records with `com.atproto.repo.strongRef` (URI and CID). garden.msg uses plain at-uris, so migrated references lose version pinning. | all | Accept it. A post being edited shouldn't break replies, which is why garden.msg chose plain URIs. `.reaction` keeps an optional `cid`. |
| G2 | **Media.** Posts can't carry images, attachments or embeds. | all | Add an optional `embed` open union to `.post`, with a shared `#images` def (blob plus alt text) and room for app formats. |
| G3 | **Rich text.** Apps use facets (Coves, Barazo, Colibri) or block arrays (atmoBB). garden.msg has only `#markdown`. | all but UserInput | The `content` union is already open, so apps can keep their native format there. Also write `textContent`, and `#markdown` when the native format converts cleanly. Optionally add a shared facets def later. |
| G4 | **Custom reactions.** `.reaction.emoji` is one grapheme, which rules out Colibri's custom shortcodes and Barazo's typed reactions. | Colibri, Barazo | Allow a shortcode (`:name:`) with an optional reference to the emoji record, like Colibri's `customEmoji`. |
| G5 | **Untitled threads.** Coves posts can have no title, for media-only posts. | Coves | Keep titles required, and have Coves derive a title (for example the first line, or the link title). Or make `title` optional. Open question 4 in the README. |
| G6 | **Moderation actions.** `.override` covers move, rename, hide, lock and pin. Apps also ban, warn, close, and set statuses such as "planned" or "duplicate". | atmoBB, Colibri, UserInput | Account-level actions (ban, warn) stay in the app's namespace. `close` and a generic `status` could be added to `.override`. |
| G7 | **Spaces.** Colibri's records live in permissioned spaces and point at each other with space refs. | Colibri | Covered by open questions 1 and 2 in the README (public spaces and space-qualified URIs). Colibri can't migrate until those settle. |
| G8 | **Polls.** atmoBB threads can carry a poll. | atmoBB | Keep polls app-specific, as a sidecar record. |
