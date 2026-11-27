"""The skill's offline links must match the Tekyous server's byte for byte.

`doc_link_fixtures.json` holds specs and the `v1.…` value the server's own encoder (tekyous-backend
`app/mcp/diagram.py`, `encode_doc`) made for each. Run: `python3 -m unittest discover tests`.
"""

import base64
import json
import subprocess
import sys
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "tekyous" / "skills" / "tech-stack-diagram" / "scripts" / "doc_link.py"
FIXTURES = json.loads((Path(__file__).with_name("doc_link_fixtures.json")).read_text(encoding="utf-8"))

sys.path.insert(0, str(SCRIPT.parent))
import doc_link  # noqa: E402


def decode(value: str):
    version, _, body = value.partition(".")
    assert version == "v1"
    raw = base64.urlsafe_b64decode(body + "=" * (-len(body) % 4))
    return json.loads(zlib.decompress(raw, -15).decode())


class DocLinkTest(unittest.TestCase):
    def test_matches_server_encoder(self):
        for f in FIXTURES:
            with self.subTest(title=f["spec"].get("title")):
                self.assertEqual(doc_link.encode(f["spec"]), f["doc"])

    def test_round_trip(self):
        for f in FIXTURES:
            self.assertEqual(decode(doc_link.encode(f["spec"])), f["spec"])

    def test_cli_prints_builder_link(self):
        spec = FIXTURES[0]
        out = subprocess.run([sys.executable, str(SCRIPT), "-"], input=json.dumps(spec["spec"]),
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()
        self.assertEqual(out, f"{doc_link.BUILDER}#doc={spec['doc']}")

    def test_cli_rejects_other_json(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "-"], input='{"groups": []}', capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("tekyous-diagram", r.stderr)


if __name__ == "__main__":
    unittest.main()
