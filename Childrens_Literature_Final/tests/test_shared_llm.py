# tests/test_shared_llm.py
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from website.services.shared.llm import call_gpt

def test_call_gpt_returns_text():
    result = call_gpt("Write one sentence about a little girl with a cape.")
    assert isinstance(result, str)
    assert len(result) > 0
