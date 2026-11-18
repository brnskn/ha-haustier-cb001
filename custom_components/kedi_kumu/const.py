"""Constants for Kedi Kumu."""

DOMAIN = "kedi_kumu"
VERSION = "1.0.0"

CONF_TUYA_DEVICE_ID = "tuya_device_id"
CONF_NOTIFY = "notify_services"
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
FAULT_MESSAGES = {
    "motor_fault": "Kum kabında motor arızası var.",
    "g_sensor_fault": "Kum kabının ağırlık sensöründe arıza var.",
    "full_fault": "Atık poşeti doldu, değiştirme zamanı.",
    "box_out": "Atık haznesi yerinde değil.",
    "filter_fault": "Kum kabının filtresinde sorun var.",
}

# Box states reported on DP 24 (plus a few the Tuya integration filters out)
BOX_STATES = [
    "standby",
    "cat_near",
    "cat_in",
    "cat_out",
    "clean",
    "smooth",
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
