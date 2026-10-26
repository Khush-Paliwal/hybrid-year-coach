"""Fetch start/end photos for plan exercises from free-exercise-db (public domain, The Unlicense).

Writes small JPEGs to demos/ and the matching rules to src/demos.json. The app flips between the two
photos so they play like a short GIF. Rules are tried in order against the exercise name; a rule with
no image means "no good match: show only the Watch how link".

Usage: python fetch_demos.py <scratch dir for raw downloads>
"""
import io
import json
import sys
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
RAW = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"

RULES = [
    ("straight-bar|pike push-up|wall walk|dead hang|hollow|kip swing|high pull|copenhagen|handstand hold|toe-pull", None),
    ("^paused bench|^bench press", "Barbell_Bench_Press_-_Medium_Grip"),
    ("^close-grip bench", "Close-Grip_Barbell_Bench_Press"),
    ("^(paused )?back squat", "Barbell_Full_Squat"),
    ("^goblet squat", "Goblet_Squat"),
    ("^romanian deadlift", "Romanian_Deadlift"),
    ("^deadlift", "Barbell_Deadlift"),
    ("^overhead press", "Standing_Military_Press"),
    ("^barbell row", "Bent_Over_Barbell_Row"),
    ("^chest-supported db row", "Dumbbell_Incline_Row"),
    ("^incline db press", "Incline_Dumbbell_Press"),
    ("^face pull", "Face_Pull"),
    ("^barbell hip thrust", "Barbell_Hip_Thrust"),
    ("^bulgarian split squat", "Split_Squat_with_Dumbbells"),
    ("^walking lunge", "Dumbbell_Lunges"),
    ("^seated leg curl", "Seated_Leg_Curl"),
    ("^standing calf raise", "Standing_Calf_Raises"),
    ("^side plank", "Side_Bridge"),
    ("^ab wheel", "Ab_Roller"),
    ("^hanging leg raise", "Hanging_Leg_Raise"),
    ("^lat pulldown", "Wide-Grip_Lat_Pulldown"),
    ("^incline db curl", "Incline_Dumbbell_Curl"),
    ("^hammer curl", "Hammer_Curls"),
    ("scap pull-up", "Scapular_Pull-Up"),
    ("muscle-up", "Muscle_Up"),
    ("hspu|handstand push", "Handstand_Push-Ups"),
    ("dip", "Dips_-_Triceps_Version"),
    ("pull-up", "Pullups"),
    ("push-up", "Pushups"),
]


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read()


def main(scratch):
    out = ROOT / "demos"
    out.mkdir(exist_ok=True)
    raw_dir = Path(scratch)
    raw_dir.mkdir(parents=True, exist_ok=True)
    ids = sorted({img for _, img in RULES if img})
    for ex_id in ids:
        for frame in (0, 1):
            raw_path = raw_dir / f"{ex_id}-{frame}.jpg"
            if not raw_path.exists():
                raw_path.write_bytes(fetch(f"{RAW}{ex_id}/{frame}.jpg"))
            img = Image.open(io.BytesIO(raw_path.read_bytes())).convert("RGB")
            img.thumbnail((360, 360))
            img.save(out / f"{ex_id}-{frame}.jpg", "JPEG", quality=72, optimize=True, progressive=True)
        print("ok", ex_id)
    (ROOT / "src" / "demos.json").write_text(json.dumps([[p, i] for p, i in RULES]), encoding="utf-8")
    total = sum(f.stat().st_size for f in out.glob("*.jpg"))
    print(f"{len(ids)} demos, {total // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1])
