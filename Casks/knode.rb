# Knode for Mac, signed with a Developer ID and notarised.
#
# Template until the first release: `version` and `sha256` below are placeholders
# (0.1.0 and zeros). Each release replaces them with the tag's version and the checksum
# of the release's Knode-<version>.dmg. See the release process in the handbook:
# https://github.com/knodemd/handbook/blob/main/07-releasing.md
#
# There is no `binary` stanza on purpose: the app carries its own `knode` and offers to
# install the command, and uses the formula's `knode` when it is installed, so the cask
# never links a second `knode` next to the formula's.
cask "knode" do
  version "0.1.0"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"

  url "https://github.com/knodemd/knode/releases/download/v#{version}/Knode-#{version}.dmg"
  name "Knode"
  desc "Second brain for AI agents"
  homepage "https://knode.md/"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on macos: :tahoe

  app "Knode.app"

  # The app's own settings and caches. Spaces are .knode files the user saved, never removed.
  zap trash: [
    "~/Library/Application Support/Knode",
    "~/Library/Caches/md.knode.Knode",
    "~/Library/HTTPStorages/md.knode.Knode",
    "~/Library/Preferences/md.knode.Knode.plist",
    "~/Library/Saved Application State/md.knode.Knode.savedState",
  ]

  caveats <<~EOS
    To use Knode from the terminal and from your agents, let the app install the `knode`
    command, or install it with Homebrew:
      brew install knodemd/tap/knode
  EOS
end
