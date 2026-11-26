"""Constants for Kedi Kumu."""

DOMAIN = "kedi_kumu"
VERSION = "1.0.0"

CONF_TUYA_DEVICE_ID = "tuya_device_id"
CONF_NOTIFY = "notify_services"
# Phones whose fault alerts ring through silent mode; the others get time-sensitive ones.
# Missing option = every notify phone (behaviour before the option existed).
CONF_CRITICAL = "critical_services"
CONF_MIN_MANUAL = "min_manual"
DEFAULT_MIN_MANUAL = 3

SIGNAL_UPDATE = "kedi_kumu_update"
SIGNAL_CAT_ADDED = "kedi_kumu_cat_added"
SIGNAL_CAT_REMOVED = "kedi_kumu_cat_removed"

EVENT_VISIT = "kedi_kumu_visit"
EVENT_ANOMALY = "kedi_kumu_anomaly"
NOTIFY_ACTION_PREFIX = "KEDIKUMU"

NOT_CAT = "none"

URL_BASE = "/kedi_kumu"
URL_CARD = f"{URL_BASE}/kedi-kumu-card.js"
URL_PHOTOS = f"{URL_BASE}/photos"

# Tuya data points of the Haustier CB001 (product key nietgqxmysgyf988)
DP_TIMES_DAY = 7
DP_DURATION_DAY = 8
DP_MANUAL_CLEAN = 9
DP_LIGHT = 16
DP_FAULT = 22
DP_STATUS = 24
DP_RECORD = 104
SCHEMA_DPS = {1, 4, 5, 6, 7, 8, 9, 16, 22, 23, 24}

# DP 22 bitmap, in bit order
FAULT_LABELS = ["motor_fault", "g_sensor_fault", "full_fault", "box_out", "filter_fault"]
# A fault must last this long (seconds) before it is shown or notified. The
# box briefly raises "motor fault" when it pauses the drum because a cat came
# near during cleaning; that resolves by itself within a minute or two.
FAULT_GRACE = {
    "motor_fault": 180,
    "g_sensor_fault": 180,
    "box_out": 60,
    "filter_fault": 60,
    "full_fault": 30,
}
# Push notification texts, picked by the Home Assistant language (Turkish or English)
FAULT_MESSAGES = {
    "en": {
        "motor_fault": "The litter box reports a motor fault.",
        "g_sensor_fault": "The litter box weight sensor reports a fault.",
        "full_fault": "The waste bag is full, time to change it.",
        "box_out": "The waste drawer cover is not closed.",
        "filter_fault": "The deodorizer filter has expired, time to replace it.",
    },
    "tr": {
        "motor_fault": "Kum kabında motor arızası var.",
        "g_sensor_fault": "Kum kabının ağırlık sensöründe arıza var.",
        "full_fault": "Atık poşeti doldu, değiştirme zamanı.",
        "box_out": "Atık haznesinin kapağı kapalı değil.",
        "filter_fault": "Koku giderici filtrenin süresi doldu, değiştirme zamanı.",
    },
}
NOTIFY_TEXT = {
    "en": {
        "fault_title": "🐾 Litter box",
        "question_title": "🐾 Who used the litter box?",
        "guess": "My guess: {name}",
        "anomaly": "This weight matches no cat; the scale may have drifted.",
        "not_cat": "Not a cat",
        "sec": "{n} s",
    },
    "tr": {
        "fault_title": "🐾 Kum kabı",
        "question_title": "🐾 Kumu kim kullandı?",
        "guess": "Tahminim: {name}",
        "anomaly": "Bu ağırlık hiçbir kediye uymuyor; tartı kaymış olabilir.",
        "not_cat": "Kedi değil",
        "sec": "{n} sn",
    },
}

# Box states reported on DP 24 (plus a few the Tuya integration filters out)
BOX_STATES = [
    "standby",
    "cat_near",
    "cat_in",
    "cat_out",
    "clean",
    "smooth",
    "clear_sand",
    "sleep",
    "uv",
    "other",
]

# Visit statuses
ST_AUTO = "auto"
ST_MANUAL = "manual"
ST_PENDING = "pending"
ST_NOT_CAT = "not_cat"

MAX_VISITS = 3000
MAX_SAMPLES = 30
VISIT_TIMEOUT = 20 * 60  # seconds before an unfinished visit is closed
IDLE_CLOSE_DELAY = 120  # seconds in standby (no cat_out) before an open visit is closed
