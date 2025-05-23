import json
import os

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")

def load_config(library_name="seoul_library"):
    """
    Load a JSON config for the given library. If not found, fallback to default.json.
    """
    primary_path = os.path.join(CONFIG_DIR, f"{library_name}.json")
    default_path = os.path.join(CONFIG_DIR, "default.json")

    try:
        with open(primary_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Config for '{library_name}' not found. Falling back to default.json.")

    try:
        with open(default_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("❌ Both specific and default config files are missing.")
