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
DP_STATUS = 24
DP_RECORD = 104

# Box states reported on DP 24 (plus a few the Tuya integration filters out)
BOX_STATES = [
    "standby",
    "cat_near",
    "cat_in",
    "cat_out",
    "clean",
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
