<img src="https://raw.githubusercontent.com/knodemd/brand/main/09%20Banners/README%20Headers/PNG/readme-homebrew-tap.png" alt="Knode Homebrew tap" width="100%">

# Knode for Homebrew

Nothing to install yet: the first release comes with
[v0.1](https://github.com/knodemd/handbook/blob/main/06-roadmap.md).

## The `knode` command

```sh
brew install knodemd/tap/knode
```

Installs the `knode` binary: the command line, the MCP server (`knode mcp`) and Knode Service.
That is enough to give every agent a memory, without the app. Works on macOS (Apple silicon and
Intel) and on Linux (x86_64 and arm64).

Then connect an agent:

```sh
knode connect claude-code
```

## Knode for Mac

```sh
brew install --cask knodemd/tap/knode
```

Installs the Mac app, signed and notarised. The app carries its own `knode` and offers to install the
command; when the formula above is installed, the app uses that one instead, so there is never a
second `knode` on your path.

## Updating

```sh
brew upgrade knode
brew upgrade --cask knode
```

## What is here

| Path | What |
|---|---|
| `Formula/knode.rb` | The `knode` command line |
| `Casks/knode.rb` | The Mac app |

Both point at the archives attached to each
[Knode release](https://github.com/knodemd/knode/releases), and every release updates their version
and checksums. How a release is made is in the
[handbook](https://github.com/knodemd/handbook/blob/main/07-releasing.md).

Licence: [Apache 2.0](LICENSE).
