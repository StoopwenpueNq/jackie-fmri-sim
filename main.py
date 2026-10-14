from neural_core import JackieCore
from scan_data import RAW_SESSIONS
import sys

core = JackieCore()

def banner():
    print("jackie-brain-twin  |  core online")
    print("commands: <stimulus> | replay [SID] | mem | reg | social | q")

def run():
    banner()
    for s in RAW_SESSIONS:
        r = core.process(s.stimulus, 1.15 if s.intensity == "high" else 0.9)
        print(f"{s.sid} | {s.stimulus:32s} | {r['dom']:10s} | HR={r['hr']:5.1f} | {r['vec']['joy']:.2f}/{r['vec']['anxiety']:.2f}")

    print("-" * 90)

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line in ("q", "quit", "exit"):
            break
        if line == "mem":
            for m in list(core.memory)[-12:]:
                print(m)
            continue
        if line == "reg":
            print(core.regions.top(10))
            continue
        if line == "social":
            for label in ["random street dog", "best friend dog", "neighbor dog"]:
                r = core.process(label, 1.1)
                print(f"{label:25s} → {r['dom']:10s} HR={r['hr']}  fMRI={r['fMRI']}")
            continue
        if line.startswith("replay"):
            parts = line.split()
            sid = parts[1] if len(parts) > 1 else None
            print(core.replay(sid))
            continue
        inten = 1.0
        tokens = line.split()
        if len(tokens) > 1 and tokens[0] == "i":
            try:
                inten = float(tokens[1])
                line = " ".join(tokens[2:])
            except:
                pass
        r = core.process(line, inten)
        print(f"#{r['id']} {r['stim']} → {r['dom']}  HR={r['hr']}  arousal={r['arousal']}  {r['vec']}")

if __name__ == "__main__":
    run()
