from huggingface_hub import snapshot_download
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

mistral_models_path = BASE_DIR.joinpath("hub_model", "briaai", "RMBG-1.4")
mistral_models_path.mkdir(parents=True, exist_ok=True)

snapshot_download(
    repo_id="briaai/RMBG-1.4",
    allow_patterns=["MyConfig.py", "briarmbg.py", "config.json", "model.safetensors"],
    local_dir=mistral_models_path,
)

print(mistral_models_path)
