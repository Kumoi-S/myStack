"""Print the models and reasoning levels reported by Magpie."""

import json
import shutil
import subprocess
import sys
from http.client import HTTPException
from urllib.request import urlopen


def main() -> int:
    magpie = shutil.which("magpie")
    if magpie is None:
        print("Error: magpie was not found on PATH.", file=sys.stderr)
        return 1

    try:
        result = subprocess.run(
            [magpie, "status", "--json"],
            stdout=subprocess.PIPE,
            check=True,
            timeout=10,
        )
        status = json.loads(result.stdout)
        url = status.get("url") if isinstance(status, dict) else None
        if not isinstance(url, str) or not url.strip():
            raise ValueError("magpie status did not report a service URL")

        with urlopen(f"{url.strip().rstrip('/')}/v1/models", timeout=10) as response:
            models = json.load(response)["data"]

        rows = []
        for model in models:
            model_id = model["id"]
            levels = model.get("reasoning_levels")
            rows.append((model_id, "/".join(levels) if levels else "none"))
        width = max((len(model_id) for model_id, _ in rows), default=0)
    except (subprocess.SubprocessError, OSError, HTTPException, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    for model_id, levels in rows:
        print(f"{model_id:<{width}}  {levels}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
