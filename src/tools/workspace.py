from pathlib import Path
import shutil

from src.models.implementation import Implementation


WORKSPACE_ROOT = Path("generated/application")


def materialize_implementation(implementation: Implementation) -> Path:
    root = WORKSPACE_ROOT.resolve()

    if root.exists():
        shutil.rmtree(root)

    root.mkdir(parents=True, exist_ok=True)

    for source_file in implementation.files:
        target = (root / source_file.path).resolve()

        if not target.is_relative_to(root):
            raise ValueError(
                f"Invalid generated file path: {source_file.path}"
            )

        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(
            source_file.content,
            encoding="utf-8",
        )

    print(
        f"[WORKSPACE] Materialized {len(implementation.files)} files "
        f"at {root}"
    )

    return root