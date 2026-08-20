"""Kill python -m business_bookmark_sorter review processes only."""
from __future__ import annotations

import subprocess
import sys


def main() -> int:
    ps = r"""
$left = @(Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match 'python' -and $_.CommandLine -and
  ($_.CommandLine -like '*-m business_bookmark_sorter review*')
})
foreach ($p in $left) {
  Write-Output ("KILL {0}" -f $p.ProcessId)
  Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
}
if (-not $left) { Write-Output 'none-found' }
"""
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps],
        capture_output=True,
        text=True,
        check=False,
    )
    sys.stdout.write(r.stdout or "")
    if r.stderr:
        sys.stderr.write(r.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
