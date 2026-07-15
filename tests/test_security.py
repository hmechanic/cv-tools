import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import use_LLM  # noqa: E402


class LatexEscapingTests(unittest.TestCase):
    def test_escapes_latex_control_characters(self):
        untrusted = r"\input{.env} 100% R&D_name #1 $5 ~ ^"

        escaped = use_LLM.escape_latex_text(untrusted)

        self.assertNotIn(r"\input", escaped)
        self.assertIn(r"\textbackslash{}input\{.env\}", escaped)
        self.assertIn(r"100\%", escaped)
        self.assertIn(r"R\&D\_name", escaped)

    @patch("use_LLM.requests.post")
    @patch.dict(
        "os.environ",
        {"API_PROVIDER": "openrouter", "OPENROUTER_API_KEY": "test-key"},
        clear=False,
    )
    def test_openrouter_request_has_timeout(self, post):
        post.return_value.json.return_value = {
            "choices": [{"message": {"content": "result"}}]
        }

        result = use_LLM.get_ai_response("query")

        self.assertEqual(result, "result")
        self.assertEqual(post.call_args.kwargs["timeout"], use_LLM.REQUEST_TIMEOUT)


if __name__ == "__main__":
    unittest.main()
