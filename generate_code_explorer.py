from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = REPO_ROOT / "site"
IGNORE_NAMES = {".git", ".venv", "__pycache__", "site", ".vscode", ".gitignore"}
TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".html",
    ".css",
    ".js",
    ".ini",
    ".cfg",
    ".yml",
    ".yaml",
}


def is_in_ignored_folder(path: Path) -> bool:
    return any(part in IGNORE_NAMES for part in path.parts)


def scan_repo() -> list[dict[str, str]]:
    files = []
    for path in sorted(REPO_ROOT.rglob("*")):
        if path.is_dir():
            continue
        if is_in_ignored_folder(path.relative_to(REPO_ROOT)):
            continue
        if path == OUTPUT_DIR / "files.json":
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="utf-8", errors="replace")

        files.append(
            {
                "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "content": content,
            }
        )
    return files


def write_site_files(files: list[dict[str, str]]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "files.json"
    output_path.write_text(
        json.dumps({"files": files}, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {len(files)} files to {output_path}")


if __name__ == "__main__":
    file_list = scan_repo()
    write_site_files(file_list)
