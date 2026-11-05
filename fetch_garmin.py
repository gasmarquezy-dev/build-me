# Récupère le sommeil, la VFC et les activités Garmin, puis écrit garmin.json.
# Utilise le secret GARMIN_TOKENS créé avec cle-garmin.py.
import os, json, datetime as dt
from garminconnect import Garmin

g = Garmin()
g.login(os.environ["GARMIN_TOKENS"])

def hm(ms):
    if not ms:
        return None
    return dt.datetime.utcfromtimestamp(ms / 1000).strftime("%H:%M")

today = dt.date.today()
nights = []
for i in range(56):
    day = today - dt.timedelta(days=i)
    try:
        data = g.get_sleep_data(day.isoformat()) or {}
        s = data.get("dailySleepDTO") or {}
        score = ((s.get("sleepScores") or {}).get("overall") or {}).get("value")
        if score is None:
            continue
        hrv = None
        try:
            hrv = ((g.get_hrv_data(day.isoformat()) or {}).get("hrvSummary") or {}).get("lastNightAvg")
        except Exception:
            pass
        nights.append({
            "d": day.isoformat(),
            "score": score,
            "min": round((s.get("sleepTimeSeconds") or 0) / 60),
            "fc": data.get("restingHeartRate"),
            "vfc": hrv,
            "bed": hm(s.get("sleepStartTimestampGMT")),
            "wake": hm(s.get("sleepEndTimestampGMT")),
        })
    except Exception:
        continue
nights.sort(key=lambda n: n["d"])

acts = []
try:
    for a in g.get_activities(0, 40):
        acts.append({
            "d": (a.get("startTimeLocal") or "")[:10],
            "h": (a.get("startTimeLocal") or "")[11:16],
            "type": (a.get("activityType") or {}).get("typeKey"),
            "name": a.get("activityName"),
            "min": round((a.get("duration") or 0) / 60),
            "hr": round(a.get("averageHR") or 0) or None,
            "kcal": round(a.get("calories") or 0) or None,
        })
except Exception:
    pass

out = {
    "updatedAt": int(dt.datetime.utcnow().timestamp() * 1000),
    "date": today.isoformat(),
    "nights": nights,
    "acts": acts,
}
with open("garmin.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print(f"{len(nights)} nuits, {len(acts)} activités")
