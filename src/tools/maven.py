import subprocess
from pathlib import Path

from src.models.build import BuildResult


MAVEN_IMAGE = "maven:3.9-eclipse-temurin-21"
BUILD_TIMEOUT_SECONDS = 300


def run_maven_tests(project_dir: Path) -> BuildResult:
    project_path = project_dir.resolve()

    if not project_path.is_dir():
        raise ValueError(f"Project directory not found: {project_path}")

    if not (project_path / "pom.xml").is_file():
        return BuildResult(
            success=False,
            exit_code=-1,
            stdout="",
            stderr="pom.xml not found in the generated project.",
        )

    command = [
        "docker", "run",
        "--rm",
        "--network", "none",
        "--read-only",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--memory", "2g",
        "--cpus", "2",
        "--pids-limit", "256",

        # Temporary writable directories
        "--tmpfs", "/tmp:rw,exec,nosuid,size=256m",
        "--tmpfs", "/root/.m2:rw,nosuid,size=512m",
        "--tmpfs", "/workspace:rw,nosuid,size=512m",

        # Generated source code mounted as read-only
        "--mount",
        f"type=bind,source={project_path},target=/source,readonly",

        MAVEN_IMAGE,

        "sh", "-c",
        "cp -a /source/. /workspace/ && "
        "cd /workspace && "
        "mvn -B -ntp -o test",
    ]

    print("[MAVEN] Starting isolated build...")

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=BUILD_TIMEOUT_SECONDS,
            check=False,
        )

        result = BuildResult(
            success=process.returncode == 0,
            exit_code=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr,
        )

    except subprocess.TimeoutExpired as exc:
        result = BuildResult(
            success=False,
            exit_code=-1,
            stdout=(
                exc.stdout.decode(errors="replace")
                if isinstance(exc.stdout, bytes)
                else exc.stdout or ""
            ),
            stderr="Maven execution timed out.",
        )

    except FileNotFoundError:
        result = BuildResult(
            success=False,
            exit_code=-1,
            stdout="",
            stderr="Docker executable was not found.",
        )

    print(
        f"[MAVEN] Build completed. "
        f"success={result.success}, exit_code={result.exit_code}"
    )

    return result