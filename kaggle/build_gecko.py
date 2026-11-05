"""Kaggle kernel: configure (and optionally build) Gecko esr115 for Android API 19.

The GitHub workflow replaces STAGE below before pushing this script to Kaggle.
Everything useful is written to /kaggle/working (logs, ccache, outputs); the
source and object directories live under /tmp to keep the saved output small.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import time
import traceback

STAGE = "__STAGE__"  # configure | build

REPO = "https://github.com/unisocsu/kitkat-browser"
BRANCH = "gecko-esr115-import"

WORK = pathlib.Path("/kaggle/working")
LOGS = WORK / "logs"
OUT = WORK / "out"
SRC = pathlib.Path("/tmp/kitkat-browser")
GECKO = SRC / "gecko"
OBJDIR = pathlib.Path("/tmp/objdir")
STATE = pathlib.Path("/tmp/mozbuild")
CCACHE = WORK / "ccache"

for d in (LOGS, OUT, CCACHE):
    d.mkdir(parents=True, exist_ok=True)

ENV = dict(os.environ)
ENV.update(
    {
        "MOZBUILD_STATE_PATH": str(STATE),
        "CCACHE_DIR": str(CCACHE),
        "CCACHE_MAXSIZE": "8G",
        "MOZ_NOSPAM": "1",
    }
)


def run(name, cmd, cwd=None, env=None, check=True):
    """Run a command, stream everything to logs/<name>.log, print a heartbeat."""
    log_path = LOGS / f"{name}.log"
    print(f"[{time.strftime('%H:%M:%S')}] START {name}: {' '.join(cmd)}", flush=True)
    start = time.time()
    count = 0
    with open(log_path, "w") as log:
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env or ENV,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        )
        for line in proc.stdout:
            log.write(line)
            count += 1
            if count % 500 == 0:
                print(
                    f"[{time.strftime('%H:%M:%S')}] {name}: {count} log lines, "
                    f"{int(time.time() - start)}s",
                    flush=True,
                )
        rc = proc.wait()
    print(f"[{time.strftime('%H:%M:%S')}] END {name}: rc={rc}", flush=True)
    if rc != 0:
        print(f"--- last lines of {name}.log ---", flush=True)
        print("".join(open(log_path, errors="replace").readlines()[-40:]), flush=True)
        if check:
            raise RuntimeError(f"{name} failed with exit code {rc}")
    return rc


def main():
    run(
        "00-environment",
        ["bash", "-c", "uname -a; nproc; free -g; df -h /tmp /kaggle/working; id; python3 --version; git --version"],
        check=False,
    )

    run("01-clone", ["git", "clone", "--depth", "1", "--branch", BRANCH, REPO, str(SRC)])
    run(
        "02-submodule",
        ["git", "submodule", "update", "--init", "--depth", "1", "gecko"],
        cwd=SRC,
    )
    run("03-gecko-version", ["bash", "-c", "cat browser/config/version.txt; git log -1 --format=%H"], cwd=GECKO, check=False)

    # Derived mozconfig: the repo's API 19 config plus ccache and an object dir in /tmp.
    mozconfig = WORK / "mozconfig.kaggle"
    mozconfig.write_text(
        f'. "{SRC}/gecko-api19/mozconfig.api19-arm"\n'
        f"ac_add_options --with-ccache\n"
        f"mk_add_options MOZ_OBJDIR={OBJDIR}\n"
    )
    ENV["MOZCONFIG"] = str(mozconfig)

    run(
        "04-bootstrap",
        ["python3", "./mach", "bootstrap", "--application-choice", "mobile_android"],
        cwd=GECKO,
    )
    run("05-configure", ["python3", "./mach", "configure"], cwd=GECKO)

    if STAGE == "build":
        run("06-build", ["python3", "./mach", "build"], cwd=GECKO)
        run("07-ccache-stats", ["bash", "-c", "ccache -s || true"], check=False)
        # Collect any Android archives the build produced (best effort).
        for aar in OBJDIR.rglob("*.aar"):
            if aar.stat().st_size < 400 * 1024 * 1024:
                shutil.copy2(aar, OUT / aar.name)
        for apk in OBJDIR.rglob("*.apk"):
            if apk.stat().st_size < 400 * 1024 * 1024:
                shutil.copy2(apk, OUT / apk.name)


if __name__ == "__main__":
    status = "OK"
    try:
        main()
    except Exception:
        status = "FAILED"
        traceback.print_exc()
    (WORK / "summary.txt").write_text(
        f"stage={STAGE}\nstatus={status}\nfinished={time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    print(f"RESULT: stage={STAGE} status={status}", flush=True)
    sys.exit(0 if status == "OK" else 1)
