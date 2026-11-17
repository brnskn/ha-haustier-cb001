"""Tests for kedi_kumu, run inside the Home Assistant container.

    docker exec -it homeassistant python3 /path/to/tests/ha_container_check.py /path/to/repo
"""

import asyncio
import base64
import json
import sys
import tempfile
from types import SimpleNamespace

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")

from homeassistant.core import HomeAssistant  # noqa: E402
from homeassistant.helpers import device_registry as dr, entity_registry as er  # noqa: E402
from homeassistant.util import dt as dt_util  # noqa: E402

from custom_components.kedi_kumu import classifier, protocol  # noqa: E402
from custom_components.kedi_kumu.const import ST_AUTO, ST_MANUAL, ST_NOT_CAT, ST_PENDING  # noqa: E402
from custom_components.kedi_kumu.tracker import LitterTracker  # noqa: E402

FAILS = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        FAILS.append(label)


def rec(kind, value, hh=19, mi=21, ss=55):
    raw = bytes([26, 11, 17, hh, mi, ss, kind]) + value.to_bytes(2, "big")
    return base64.b64encode(raw).decode()


# ---------------------------------------------------------------- protocol
r = protocol.parse_record("GgsRExU3Aw7E")
check(r.kind == 3 and r.value == 3780 and r.device_time == "2026-11-17 19:21:55", "decode weight record")
r = protocol.parse_record("GgsRExYlAgAq")
check(r.kind == 2 and r.value == 42, "decode duration record")
check(protocol.parse_record("standby") is None, "non-record string ignored")
check(protocol.parse_record(123) is None, "non-string ignored")


# ---------------------------------------------------------------- classifier
def cat(cid, weights=(), manual=0, hint=None):
    return {"id": cid, "name": cid, "samples": [{"w": w, "src": "manual"} for w in weights], "manual_count": manual, "hint": hint}


cats = [cat("a"), cat("b"), cat("c")]
res = classifier.classify(3780, cats, 3)
check(res.status == ST_PENDING and res.reason == "untrained", "no data -> pending")
res = classifier.classify(200, cats, 3)
check(res.status == ST_NOT_CAT, "200 g -> not a cat")

cats = [cat("a", [3780, 3800], 2), cat("b", hint=4600), cat("c", hint=5500)]
res = classifier.classify(3790, cats, 3)
check(res.status == ST_PENDING and res.suggestion == "a", "learning phase suggests nearest cat")

cats = [cat("a", [3780, 3800, 3760], 3), cat("b", [4600, 4650, 4580], 3), cat("c", [5500, 5450, 5520], 3)]
res = classifier.classify(3820, cats, 3)
check(res.status == ST_AUTO and res.cat_id == "a" and res.confidence > 0.5, f"trained -> auto a ({res.confidence})")
res = classifier.classify(4630, cats, 3)
check(res.status == ST_AUTO and res.cat_id == "b", "trained -> auto b")
res = classifier.classify(4200, cats, 3)
check(res.status == ST_PENDING, f"between two cats -> pending ({res.reason})")
res = classifier.classify(7800, cats, 3)
check(res.status == ST_PENDING and res.anomaly, "far from every cat -> anomaly")

close = [cat("a", [4000, 4020, 3990], 3), cat("b", [4100, 4080, 4120], 3)]
res = classifier.classify(4050, close, 3)
check(res.status == ST_PENDING and res.reason == "ambiguous", "two cats with near weights -> ambiguous")
check(not classifier.should_learn(6000, cats[0], 3), "trained cat does not learn outlier weight")
check(classifier.should_learn(3900, cats[0], 3), "trained cat learns normal weight")


# ---------------------------------------------------------------- tracker
async def tracker_tests():
    tmp = tempfile.mkdtemp()
    hass = HomeAssistant(tmp)
    await hass.config.async_set_time_zone("Europe/Istanbul")
    from homeassistant.helpers import area_registry as ar, entity, frame, translation
    from homeassistant import loader
    loader.async_setup(hass)
    entity.async_setup(hass)
    frame.async_setup(hass)
    translation.async_setup(hass)
    dr.async_setup(hass)
    from homeassistant.config_entries import ConfigEntries
    hass.config_entries = ConfigEntries(hass, {})
    await hass.config_entries.async_initialize()
    await ar.async_load(hass, load_empty=True)
    await dr.async_load(hass, load_empty=True)
    await er.async_load(hass, load_empty=True)
    sent = []

    async def fake_notify(call):
        sent.append((call.service, dict(call.data)))

    hass.services.async_register("notify", "mobile_app_test", fake_notify)
    events = []
    hass.bus.async_listen("kedi_kumu_visit", lambda e: events.append(e.data))
    entry = SimpleNamespace(
        entry_id="E1",
        data={"tuya_device_id": "dev1"},
        options={"min_manual": 3, "notify_services": ["mobile_app_test"]},
    )
    tr = LitterTracker(hass, entry)
    await tr.async_load()
    hass.bus.async_listen("mobile_app_notification_action", tr.async_handle_notification_action)

    # The real visit captured on 2026-11-17 19:21
    t0 = 1794932511000
    seq = [
        [{"dpId": 24, "t": t0, "value": "cat_near"}],
        [{"dpId": 104, "t": t0 + 11000, "value": "GgsRExU3Aw7E"}],
        [{"dpId": 24, "t": t0 + 11100, "value": "cat_in"}],
        [{"dpId": 104, "t": t0 + 41000, "value": "GgsRExYlAgAq"}],
        [{"dpId": 7, "t": t0 + 41001, "value": 1}],
        [{"dpId": 8, "t": t0 + 41002, "value": 42}],
        [{"dpId": 24, "t": t0 + 41100, "value": "cat_out"}],
        [{"dpId": 104, "t": t0 + 41200, "value": "GgsRExYlAQAA"}],
        [{"dpId": 24, "t": t0 + 71000, "value": "clean"}],
        [{"dpId": 104, "t": t0 + 177000, "value": "GgsRExg1BQAA"}],
        [{"dpId": 24, "t": t0 + 177100, "value": "standby"}],
    ]
    for i, item in enumerate(seq):
        tr._handle_report(item)
        if i == 1:
            check(tr.current is not None and tr.current["weight"] == 3780, "visit opens on weight record")
    tr._handle_report(seq[1])  # duplicate message must be ignored
    await hass.async_block_till_done()
    check(len(tr.visits) == 1, f"one visit stored ({len(tr.visits)})")
    v = tr.visits[0]
    check(v["weight"] == 3780 and v["duration"] == 42 and v["status"] == ST_PENDING, "visit weight/duration/status")
    check(tr.last_clean is not None and tr.status == "standby", "clean done + status tracked")
    check(events and events[-1]["weight_kg"] == 3.78, "visit event fired")
    check(not sent, "no question sent while there are no cats")

    a = await tr.async_save_cat(None, name="Pamuk", hint_kg=3.8)
    b = await tr.async_save_cat(None, name="Duman", hint_kg=4.6)
    c = await tr.async_save_cat(None, name="Tarçın", hint_kg=5.5)
    check(len({a["color"], b["color"], c["color"]}) == 3, "cats get distinct colors")
    check(tr.visits[0]["suggestion"] == a["id"], "pending visit re-suggested after cats were added")
    tr.assign(v["id"], a["id"])
    check(tr.visits[0]["status"] == ST_MANUAL and tr.get_cat(a["id"])["manual_count"] == 1, "manual label learned")

    def visit(weight, minute):
        tr._handle_report([{"dpId": 104, "t": t0 + minute * 60000, "value": rec(3, weight, 20, minute % 60, 0)}])
        tr._handle_report([{"dpId": 104, "t": t0 + minute * 60000 + 30000, "value": rec(2, 35, 20, minute % 60, 30)}])
        tr._handle_report([{"dpId": 104, "t": t0 + minute * 60000 + 31000, "value": rec(1, 0, 20, minute % 60, 31)}])
        return tr.visits[-1]

    sent.clear()
    x = visit(4620, 5)
    await hass.async_block_till_done()
    check(x["status"] == ST_PENDING and x["suggestion"] == b["id"], "learning: asks with suggestion")
    check(sent and sent[0][1]["data"]["actions"][0]["action"].startswith("KEDIKUMU_"), "question notification sent with actions")
    # Answer from the phone notification
    hass.bus.async_fire("mobile_app_notification_action", {"action": f"KEDIKUMU_{x['id']}_{b['id']}"})
    await hass.async_block_till_done()
    check(tr.get_visit(x["id"])["cat_id"] == b["id"], "notification action assigns the cat")
    check(any(s[1].get("message") == "clear_notification" for s in sent), "question cleared after answer")

    minute = 10
    for w_a, w_b, w_c in [(3800, 4600, 5480), (3760, 4650, 5520), (3790, 4610, 5500)]:
        for w, cid in ((w_a, a["id"]), (w_b, b["id"]), (w_c, c["id"])):
            vv = visit(w, minute)
            minute += 3
            if vv["status"] == ST_PENDING:
                tr.assign(vv["id"], cid)
    check(all(tr.get_cat(i)["manual_count"] >= 3 for i in (a["id"], b["id"], c["id"])), "all cats trained")
    sent.clear()
    vv = visit(3810, minute)
    check(vv["status"] == ST_AUTO and vv["cat_id"] == a["id"], f"auto recognised Pamuk ({vv['confidence']})")
    vv = visit(5490, minute + 3)
    check(vv["status"] == ST_AUTO and vv["cat_id"] == c["id"], "auto recognised Tarçın")
    await hass.async_block_till_done()
    check(not sent, "no question for confident visits")

    vv = visit(8200, minute + 6)
    check(vv["status"] == ST_PENDING and vv["anomaly"] and tr.scale_suspect, "litter-fill style weight flags the scale")
    tr.assign(vv["id"], None)
    check(tr.get_visit(vv["id"])["status"] == ST_NOT_CAT, "marked as not a cat")
    vv = visit(4630, minute + 9)
    check(vv["status"] == ST_AUTO and not tr.scale_suspect, "next good visit clears scale warning")

    # Reassign an auto visit: sample must move to the other cat
    before_b = len(tr.get_cat(b["id"])["samples"])
    pam = next(v for v in reversed(tr.visits) if v["cat_id"] == a["id"] and v["status"] == ST_AUTO)
    tr.assign(pam["id"], b["id"])
    check(not any(s.get("v") == pam["id"] for s in tr.get_cat(a["id"])["samples"]), "reassign removes old sample")
    check(len(tr.get_cat(b["id"])["samples"]) in (before_b, before_b + 1), "reassign handled for new cat")

    # Timeout closes an unfinished visit
    tr._handle_report([{"dpId": 104, "t": t0 + 99 * 60000, "value": rec(3, 3800, 21, 30, 0)}])
    check(tr.current is not None, "unfinished visit open")
    tr._timeout_visit(dt_util.utcnow())
    check(tr.current is None and tr.visits[-1]["weight"] == 3800, "timeout closes the visit")

    # Photo upload
    jpg = "data:image/jpeg;base64," + base64.b64encode(b"\xff\xd8\xff\xe0" + b"0" * 100).decode()
    info = await tr.async_save_cat(a["id"], photo=jpg)
    check(info["photo"] and info["photo"].startswith("/kedi_kumu/photos/"), "photo stored")
    try:
        await tr.async_save_cat(a["id"], photo="data:image/jpeg;base64," + base64.b64encode(b"<svg>").decode())
        check(False, "non-image rejected")
    except ValueError:
        check(True, "non-image rejected")

    snap = tr.snapshot()
    json.dumps(snap)
    check(len(snap["cats"]) == 3 and snap["cats"][0]["trained"], "snapshot serialisable")
    check(tr.visits_today() >= 0, "visits_today works")

    await tr.async_delete_cat(c["id"])
    check(len(tr.cats) == 2 and all(v.get("cat_id") != c["id"] for v in tr.visits), "delete cat clears its visits")

    await tr.async_flush()
    tr2 = LitterTracker(hass, entry)
    await tr2.async_load()
    check(len(tr2.cats) == 2 and len(tr2.visits) == len(tr.visits), "data persists across reload")
    await hass.async_stop(force=True)


asyncio.run(tracker_tests())
print("\nFAILED:" if FAILS else "\nALL PASSED", FAILS if FAILS else "")
sys.exit(1 if FAILS else 0)
