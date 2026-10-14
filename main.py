from neural_core import JackieCore
from scan_data import RAW_SESSIONS
import sys

core = JackieCore()

def run():
    for s in RAW_SESSIONS:
        r = core.process(s.stimulus, 1.2 if s.intensity == "high" else 0.9)
        print(f"{s.sid} | {s.stimulus:30s} | dom={r['dom']:10s} | joy={r['vec']['joy']:.3f} anx={r['vec']['anxiety']:.3f} | matched={r['matched']}")

    print("-" * 80)

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line in ("q", "quit", "exit"):
            break
        if line.startswith("replay"):
            parts = line.split()
            sid = parts[1] if len(parts) > 1 else None
            r = core.replay(sid)
            print(r)
            continue
        if line == "mem":
            for m in list(core.memory)[-10:]:
                print(m)
            continue
        if line == "reg":
            print(core.regions.top(10))
            continue
        inten = 1.0
        if line.startswith("i "):
            try:
                inten = float(line.split()[1])
                line = " ".join(line.split()[2:])
            except:
                pass
        r = core.process(line, inten)
        print(f"#{r['id']} {r['stim']} → {r['dom']} {r['vec']}")

if __name__ == "__main__":
    run()
