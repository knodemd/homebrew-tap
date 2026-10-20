# The knode command: the CLI, the MCP server (`knode mcp`) and Knode Service.
#
# Each release sets the version in every `url` and every `sha256` from the release's
# SHA256SUMS (scripts/bump.py); until the first release they are placeholders (zeros).
# Homebrew reads the version from the URLs. See the release process in the handbook:
# https://github.com/knodemd/handbook/blob/main/07-releasing.md
class Knode < Formula
  desc "Second brain for AI agents: CLI, MCP server and Knode Service"
  homepage "https://knode.md"
  license "Apache-2.0"

  livecheck do
    url :stable
    strategy :github_latest
  end

  on_macos do
    on_arm do
      url "https://github.com/knodemd/knode/releases/download/v0.1.0/knode-v0.1.0-aarch64-apple-darwin.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
    on_intel do
      url "https://github.com/knodemd/knode/releases/download/v0.1.0/knode-v0.1.0-x86_64-apple-darwin.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  # Homebrew on Linux runs on glibc, so the formula uses the gnu builds. The static musl
  # builds in the same release are for Alpine and older glibc, through install.sh.
  on_linux do
    on_arm do
      url "https://github.com/knodemd/knode/releases/download/v0.1.0/knode-v0.1.0-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
    on_intel do
      url "https://github.com/knodemd/knode/releases/download/v0.1.0/knode-v0.1.0-x86_64-unknown-linux-gnu.tar.gz"
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
