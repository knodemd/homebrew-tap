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

| `scripts/bump.py` | Sets the version and checksums from a release's `SHA256SUMS` |
| `.github/workflows/bump.yml` | Opens the pull request for each new release |
| `.github/workflows/tests.yml` | Checks, installs and tests the formula and the cask |

Both point at the archives attached to each
[Knode release](https://github.com/knodemd/knode/releases). How a release is made is in the
[handbook](https://github.com/knodemd/handbook/blob/main/07-releasing.md).

## How a release reaches the tap

1. When a release of `knodemd/knode` is published, it sends a `knode-release` event to this
   repository with the version.
2. The `bump` workflow downloads the release's `SHA256SUMS` and sets the version and every `sha256`
   in the formula and the cask with `scripts/bump.py`. A release without a `.dmg` leaves the cask
   as it is. Pre-releases are skipped.
3. It runs `brew style` and `brew audit`, installs and tests the formula on macOS and Linux and
   the cask on macOS, then opens a pull request. Nothing is pushed to `main`.
4. A maintainer tests the pull request on a Mac and merges it.

The workflow can also be run by hand from the Actions tab with a version. To test the script:

```sh
python3 -m unittest discover -s scripts
```

Licence: [Apache 2.0](LICENSE).
