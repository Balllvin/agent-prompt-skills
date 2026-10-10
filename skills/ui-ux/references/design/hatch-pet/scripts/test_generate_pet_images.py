import importlib.util
from pathlib import Path
import subprocess


def test_api_key_stays_out_of_curl_argv(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("generate_pet_images", Path(__file__).with_name("generate_pet_images.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        Path(command[command.index("-o") + 1]).write_text("{}")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("pet")
    base = tmp_path / "base.png"
    base.write_bytes(b"image")
    module.run_image_generation(model="m", prompt_file=prompt, output_json=tmp_path / "g.json", size="1024x1024", api_key="sk-test-secret")
    module.run_image_edit(model="m", prompt_file=prompt, image_paths=[base], output_json=tmp_path / "e.json", size="1024x1024", api_key="sk-test-secret")
    assert len(calls) == 2
    for command, kwargs in calls:
        assert all("sk-test-secret" not in arg for arg in command)
        assert kwargs["input"] == "Authorization: Bearer sk-test-secret\n"
