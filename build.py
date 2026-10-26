"""Build index.html: wrap src/template.html in a document head and inline the plan from src/plan.json
and the study plan from src/study.json.

Regenerate the plan first if it changed:  python ../tools/build_plan.py <xlsx out> src/plan.json
Regenerate the study plan if it changed:  python ../tools/build_study.py <study_tracker.xlsx> src/study.json
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
plan = (ROOT / "src" / "plan.json").read_text(encoding="utf-8").replace("</", "<\\/")
demos = (ROOT / "src" / "demos.json").read_text(encoding="utf-8").replace("</", "<\\/")
study = (ROOT / "src" / "study.json").read_text(encoding="utf-8").replace("</", "<\\/")
body = template.replace("__PLAN_JSON__", plan).replace("__DEMO_JSON__", demos).replace("__STUDY_JSON__", study)
assert "__PLAN_JSON__" not in body and "__DEMO_JSON__" not in body and "__STUDY_JSON__" not in body

head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Hybrid Year Coach</title>
<meta name="theme-color" content="#0f1317">
<meta name="description" content="Daily workout, food and progress log for a 52-week hybrid training plan, plus a day-by-day study checklist.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<style>[hidden]{display:none!important}html,body{margin:0}img{max-width:100%}</style>
</head>
<body>
"""
tail = """
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () { /* offline cache is optional */ }); });
}
</script>
</body>
</html>
"""
(ROOT / "index.html").write_text(head + body + tail, encoding="utf-8")
print("index.html", len((head + body + tail).encode("utf-8")), "bytes")
