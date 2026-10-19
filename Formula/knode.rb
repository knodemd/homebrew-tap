# The knode command: the CLI, the MCP server (`knode mcp`) and Knode Service.
#
# Template until the first release: `version` and every `sha256` below are placeholders
# (0.1.0 and zeros). Each release replaces them with the tag's version and the checksums
# from the release's SHA256SUMS. See the release process in the handbook:
# https://github.com/knodemd/handbook/blob/main/07-releasing.md
class Knode < Formula
  desc "Second brain for AI agents: CLI, MCP server and Knode Service"
  homepage "https://knode.md"
  version "0.1.0"
  license "Apache-2.0"

  livecheck do
    url :stable
    strategy :github_latest
  end

  on_macos do
    on_arm do
      url "https://github.com/knodemd/knode/releases/download/v#{version}/knode-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
    on_intel do
      url "https://github.com/knodemd/knode/releases/download/v#{version}/knode-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/knodemd/knode/releases/download/v#{version}/knode-v#{version}-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
    on_intel do
      url "https://github.com/knodemd/knode/releases/download/v#{version}/knode-v#{version}-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  def install
    bin.install "knode"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/knode --version")
  end
end
