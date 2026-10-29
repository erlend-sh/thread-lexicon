# standard.site: current remit (as of 2026-10-27)

Sources: the published lexicon schemas in the `standard.site` repo (did:plc:re3ebnp5v7ffagz6rb6xfei4, `com.atproto.lexicon.schema`), standard.site docs (introduction, FAQ, verification, document), the `standard.site/lexicons` repo on Tangled (issues and pulls), and the Bluesky integration announcement (atproto discussion #4978).

## Stated scope
- "Shared lexicons for long-form publishing on AT Protocol": blogs, articles, newsletters.
- "The lexicons focus on metadata": what a publication is, what a document contains, and where it lives. **Content format is explicitly out of scope** (each platform puts its own format in an open union).
- Each lexicon is independent. Apps implement only the ones they need.
- Extension policy (FAQ, verbatim): "The standard focuses on shared metadata properties. Applications are free to add additional properties, though they may not be understood by other platforms." Nothing says how to add new *record types*.
- Governance: "community-driven", "maintained by the developers building on it", "coordination through adoption, not committee"; changes need "consensus among builders who are actively implementing the standard." Discussion happens on Bluesky and Tangled.

## What is actually published (8 lexicons)
| NSID | Kind | Key | Required | Notable optional fields |
|---|---|---|---|---|
| `site.standard.publication` | record | tid | `url`, `name` | `icon`, `description`, `basicTheme`, `labels`, `preferences.showInDiscover` |
| `site.standard.document` | record | tid | `site` (at:// publication or https URL), `title`, `publishedAt` | `path`, `description`, `coverImage`, `content` (open union), `textContent`, `bskyPostRef` (strongRef), `tags`, `links` (open union), `labels`, `contributors[]` (did, role, displayName), `updatedAt` |
| `site.standard.graph.subscription` | record | tid | `publication` (at-uri) | `createdAt` |
| `site.standard.graph.recommend` | record | tid | `document` (at-uri), `createdAt` | |
| `site.standard.theme.basic` | record | tid | background, foreground, accent, accentForeground | |
| `site.standard.theme.color` | defs | | `#rgb`, `#rgba` | |
| `site.standard.authFull` | permission set | | repo access to publication, document, subscription, recommend | |
| `site.standard.authSocial` | permission set | | repo access to subscription and recommend only | |

Plus a non-lexicon convention: **verification**. A publication serves `/.well-known/site.standard.publication` returning its AT-URI, and a document page carries `<link rel="site.standard.document" href="at://...">`. A record is only "valid" if verified.

## What it does not cover
- **No comments, replies or threads.** The only nod to conversation is `bskyPostRef`, a strongRef to a Bluesky post "to keep track of comments off-platform", so discussion is delegated to Bluesky.
- No authorship model beyond the repo owner plus `contributors` (an "author lexicon" PR was closed; a byline issue is open).
- No content format, no localisation (open issue), no series/collections (proposal opened last week, issue #19).
- No moderation, access control or community ownership. Every record lives in the author's repo.

## Ecosystem signals
- Adopters: Leaflet, pckt, Offprint, plus indexes and search (docs.surf, Read on pckt, Standard Search, pub search, potatonet) and migration tools (Sequoia, Wireservice for WordPress).
- Bluesky ingests all `site.standard.*` records (May 2026). Phase 1 renders enhanced link cards for verified documents. Later phases are unspecified.
- People already want comments: Steve Simkins built `site.standard.document.comment` (parent/root strongRefs, content, author, createdAt) and acknowledges it is "not technically a valid schema", because only standard.site's DID can publish `site.standard.*`. The Leaflet team named commenting as an early interop goal.
- The upstream repo has 16 open issues and no merged external PRs, so its scope grows slowly.
