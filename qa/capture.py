from pathlib import Path
import os, subprocess, json, re

root = Path.cwd().resolve()
bundle = root / "work/graphics-pilot-20261006"
qa = bundle / "qa/runtime"
results = []
for room in [9, 22]:
    out = qa / f"room{room:03d}-final-hd"
    out.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        SDL_AUDIODRIVER="dummy",
        SDL_VIDEODRIVER="wayland" if env.get("WAYLAND_DISPLAY") else "x11",
        DIGHD_MOD=str(bundle / "mod"),
        DIGHD_SKIP_VIDEO="1", DIGHD_TEST_ROOM=str(room), DIGHD_TEST_AT="240",
        DIGHD_DUMP_DIR=str(out), DIGHD_DUMP_EVERY="240", DIGHD_QUIT_AT="480",
    )
    env.pop("DIGHD_VERIFY", None)
    args = [
        str(root / "engine/scummvm/scummvm"), f"--path={root}/game",
        f"--config={out}/scummvm.ini", "--debuglevel=1", "--no-fullscreen",
        "--aspect-ratio", "--gfx-mode=opengl",
        "--music-volume=0", "--sfx-volume=0", "--speech-volume=0", "dig",
    ]
    print(f"Kjører rom {room} i vindu", flush=True)
    process = subprocess.run(args, env=env, capture_output=True, text=True, timeout=45)
    log = process.stdout + process.stderr
    (out / "scummvm.log").write_text(log)
    print("\n".join(line for line in log.splitlines() if "DigHD:" in line)[-1700:], flush=True)
    result = {
        "room": room, "exit_code": process.returncode,
        "images": sorted(path.name for path in out.glob(f"frame_*_room{room:03d}.png")),
        "loaded": f"room {room} loaded (1280x800)" in log,
        "screen": re.findall(r"screen (\d+)x(\d+), (\d+) bytes per pixel", log),
    }
    result["pass"] = (
        result["exit_code"] == 0 and result["loaded"]
        and f"frame_000480_room{room:03d}.png" in result["images"]
        and ["1280", "800", "4"] in [list(mode) for mode in result["screen"]]
    )
    results.append(result)
(qa / "final-results.json").write_text(json.dumps(results, indent=2) + "\n")
if not all(result["pass"] for result in results):
    raise SystemExit("En romkjøring feilet. Se final-results.json og scummvm.log.")
print("PASS: Begge HD-bakgrunnene er lastet i 1280x800 med 32-bits farger.")
