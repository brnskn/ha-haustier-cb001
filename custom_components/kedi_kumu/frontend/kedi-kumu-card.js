/* Kedi Kumu card — cat profiles, visit labelling and litter box controls (English / Türkçe). */
const KK_VERSION = "1.1.0";

const KK_I18N = {
  en: {
    title: "Litter Box", loading: "Loading…", unreachable: "Can't reach the Kedi Kumu integration", failed: "Failed: {err}",
    photo_read: "Couldn't read the photo",
    s_standby: "Idle", s_cat_near: "Cat nearby", s_cat_in: "Cat inside", s_cat_out: "Cat left", s_clean: "Cleaning",
    s_smooth: "Leveling litter", s_clear_sand: "Emptying litter", s_sleep: "Sleeping", s_uv: "Sterilizing", s_other: "Unknown",
    f_full_fault: "Waste bag is full, time to change it", f_box_out: "Waste drawer cover is not closed",
    f_motor_fault: "Motor fault", f_g_sensor_fault: "Weight sensor fault", f_filter_fault: "Deodorizer filter has expired",
    r_learning: "Still learning", r_ambiguous: "Two cats are very close in weight", r_no_match: "This weight matches no cat",
    r_no_cats: "Add a cat first", r_no_weight: "No weight received", r_out_of_range: "Implausible weight for a cat",
    just_now: "just now", min_ago: "{n} min ago", h_ago: "{n} h ago", yesterday_l: "yesterday {t}",
    days_ago: "{n} days ago", days_ago_one: "{n} day ago", today_at: "Today {t}", yesterday_at: "Yesterday {t}",
    sec: "{n} s", min_short: "{n} min",
    auto_recognized: "Recognized automatically", picked_manually: "Picked manually", not_cat: "Not a cat", unknown: "Unknown",
    today_visits: "<b>{n}</b> visits today", today_visits_one: "<b>{n}</b> visit today", last_by: " · last: {name}, {ago}",
    in_box: "{name} in the box", cat_in_box: "A cat is in the box", add_cat: "Add cat",
    waiting_link: "Waiting for the litter box connection (Tuya)",
    scale_suspect: "The scale may have drifted: the last weight matched no cat. Unplugging and replugging fixes it.", ok: "OK",
    ob_title: "Let's meet your cats",
    ob_text: "Add a name, photo and rough weight for each cat. For the first few visits I'll ask \"Who's this?\"; after that I'll recognize them by weight.",
    who: "Who's this?", my_guess: "my guess", more_pending: "{n} more questions waiting", more_pending_one: "{n} more question waiting",
    steady: "steady", knows: "Recognizes", learning: "Learning", no_weight: "no weight", today_n: "Today {n}", none_today: "None today",
    last_clean: "Last cleaned {ago}", no_visits_yet: "No visits yet. They'll show up here when a cat uses the box.",
    recent: "Recent visits", all: "All", clean: "Clean", leveling: "Leveling", level: "Level litter", stop_ster: "Stop sterilizing",
    sterilize: "Sterilize", drum_light: "Drum light", auto_clean: "Auto clean", settings: "Settings",
    saved_as: "Saved as {name}", del_visit_q: "Delete this visit?", visit_deleted: "Visit deleted", clean_started: "Cleaning started",
    bin_q: "Did you change the waste bag? The counter will reset.", bin_reset: "Waste bin counter reset",
    filter_q: "Did you replace the deodorizer filter? The timer resets to 30 days.", filter_done: "Deodorizer timer reset",
    pour_q1: "ALL litter in the drum will be dumped into the waste bag (the app's \"add litter\" action). Continue only if you want to change the litter.",
    pour_q2: "Are you sure? This can't be undone; you'll need to refill the litter afterwards.",
    leveling_toast: "Leveling litter", ster_stopped: "Sterilization stopped", lock_on: "Child lock on", lock_off: "Child lock off",
    dnd_saved: "Do Not Disturb saved", clean_sched_saved: "Cleaning schedule saved", ster_sched_saved: "Sterilization schedule saved",
    delay_range: "Delay must be 0–600 s", delay_saved: "Cleaning delay saved",
    ster_q: "Start UV sterilization? No cat should be in the box.", ster_started: "Sterilization started",
    del_cat_q: "Delete {name}? Their visits will become unlabeled.", cat_deleted: "{name} deleted",
    dnd: "Do Not Disturb", child_lock: "Child lock", chip_clean: "Cleaning {t}", chip_ster: "Sterilization {t}",
    waste_bin: "Waste bin", full: "Full", pct: "~{n}%", cleans: "{n} cleans", cleans_one: "{n} clean", since: " · since {d}",
    estimated: " · estimated", bag_changed: "I changed the bag", deodorizer: "Deodorizer", days: "{n} days", days_one: "{n} day",
    days_unit: "days", days_unit_one: "day", time_left: "time left", time_left_cap: "Time left", renewed: "Replaced",
    settings_title: "Litter box settings", lock_desc: "Locks the buttons on the device", delay: "Cleaning delay",
    delay_desc: "After the cat leaves (s)", save: "Save", dnd_desc: "Only manual cleaning runs during this time",
    start: "Start", end: "End", sched_clean: "Scheduled cleaning", sched_ster: "Scheduled sterilization", add_time: "+ Add time",
    pour: "Empty litter", pour_desc: "Dumps all litter from the drum into the bag, for a litter change", pour_btn: "Empty",
    local_err: "Couldn't reach the litter box on the local network: {err}", delete: "Delete",
    no_sched_clean: "No scheduled cleaning", no_sched_ster: "No scheduled sterilization", min: "min", close: "Close",
    st_last_weight: "Last weight", st_average: "Average", st_change: "Change", st_today: "Today", visits_n: "{n} visits",
    visits_n_one: "{n} visit", st_daily: "Daily avg.", st_dur: "Avg. time",
    learn_ok: "I recognize this cat by weight ({n} readings, ±{s} g)",
    learn_wip: "Learning: {n}/{m} labels. I learn each time you answer \"Who's this?\".",
    edit: "Edit", weight: "Weight", last14: "Last 14 days", visits: "Visits", no_visits: "No visits yet",
    chart_more: "A few more readings are needed for the chart", vs_auto: "Recognized automatically · {p}% confidence",
    vs_pending: "Waiting for a label", vs_not_cat_range: "Not a cat (implausible weight)", visit: "Visit",
    not_learned: "This weight was far from the cat's normal, so it wasn't used for learning.",
    still_in: "The cat is still inside; you can label the visit after it leaves.", who_was: "Who was it?", del_visit: "Delete visit",
    pending_n: "Pending ({n})", history: "History", no_records: "No records", color: "Color", edit_cat: "Edit cat", new_cat: "New cat",
    name: "Name", name_ph: "e.g. Luna", hint: "Approx. weight", hint_sub: "(optional, speeds up learning)", hint_ph: "e.g. 4.2",
    cancel: "Cancel", tap_photo: "Tap to pick a photo", remove_photo: "Remove photo", name_req: "Name is required",
    hint_range: "Weight must be 0–20 kg", saving: "Saving…", saved: "{name} saved",
  },
  tr: {
    title: "Kedi Kumu", loading: "Yükleniyor…", unreachable: "Kedi Kumu eklentisine ulaşılamadı", failed: "Olmadı: {err}",
    photo_read: "Fotoğraf okunamadı",
    s_standby: "Boşta", s_cat_near: "Kedi yaklaştı", s_cat_in: "Kedi içeride", s_cat_out: "Kedi çıktı", s_clean: "Temizleniyor",
    s_smooth: "Kum düzleniyor", s_clear_sand: "Kum boşaltılıyor", s_sleep: "Uyku", s_uv: "Sterilize ediliyor", s_other: "Bilinmiyor",
    f_full_fault: "Atık poşeti dolu, değiştirme zamanı", f_box_out: "Atık haznesinin kapağı kapalı değil",
    f_motor_fault: "Motor arızası", f_g_sensor_fault: "Ağırlık sensörü arızası", f_filter_fault: "Koku giderici filtrenin süresi doldu",
    r_learning: "Henüz öğreniyorum", r_ambiguous: "İki kedi birbirine çok yakın", r_no_match: "Bu ağırlık hiçbir kediye uymuyor",
    r_no_cats: "Önce kedi ekle", r_no_weight: "Ağırlık gelmedi", r_out_of_range: "Ağırlık kedi için mantıksız",
    just_now: "az önce", min_ago: "{n} dk önce", h_ago: "{n} sa önce", yesterday_l: "dün {t}",
    days_ago: "{n} gün önce", today_at: "Bugün {t}", yesterday_at: "Dün {t}", sec: "{n} sn", min_short: "{n} dk",
    auto_recognized: "Otomatik tanındı", picked_manually: "Elle seçildi", not_cat: "Kedi değil", unknown: "Bilinmiyor",
    today_visits: "Bugün <b>{n}</b> ziyaret", last_by: " · son: {name}, {ago}",
    in_box: "{name} kumda", cat_in_box: "Bir kedi kumda", add_cat: "Kedi ekle",
    waiting_link: "Kum kabıyla bağlantı bekleniyor (Tuya)",
    scale_suspect: "Tartı kaymış olabilir: son ağırlık hiçbir kediye uymadı. Fişi çekip takmak düzeltir.", ok: "Tamam",
    ob_title: "Kedilerini tanıtalım",
    ob_text: "Her kedi için isim, fotoğraf ve yaklaşık kilosunu ekle. İlk birkaç ziyarette \"Bu kim?\" diye soracağım; sonra ağırlıklarından kendim tanıyacağım.",
    who: "Bu kim?", my_guess: "tahminim", more_pending: "{n} soru daha bekliyor",
    steady: "sabit", knows: "Tanıyor", learning: "Öğreniyor", no_weight: "kilo yok", today_n: "Bugün {n}", none_today: "Bugün yok",
    last_clean: "Son temizlik {ago}", no_visits_yet: "Henüz ziyaret yok. Bir kedi kumu kullandığında burada görünecek.",
    recent: "Son ziyaretler", all: "Tümü", clean: "Temizle", leveling: "Düzleniyor", level: "Kumu düzelt", stop_ster: "Sterilizasyonu durdur",
    sterilize: "Sterilize", drum_light: "Tambur ışığı", auto_clean: "Oto temizlik", settings: "Ayarlar",
    saved_as: "{name} olarak kaydedildi", del_visit_q: "Bu ziyaret silinsin mi?", visit_deleted: "Ziyaret silindi", clean_started: "Temizlik başlatıldı",
    bin_q: "Atık poşetini değiştirdin mi? Sayaç sıfırlanacak.", bin_reset: "Atık haznesi sayacı sıfırlandı",
    filter_q: "Koku giderici filtreyi yeniledin mi? Süre 30 güne sıfırlanacak.", filter_done: "Koku giderici süresi sıfırlandı",
    pour_q1: "Tamburdaki BÜTÜN kum atık poşetine boşaltılacak (uygulamadaki \"Kum Ekle\"). Kum değiştirmek istiyorsan devam et.",
    pour_q2: "Emin misin? Bu işlem geri alınamaz; boşalttıktan sonra yeni kum doldurman gerekecek.",
    leveling_toast: "Kum düzeltiliyor", ster_stopped: "Sterilizasyon durduruldu", lock_on: "Çocuk kilidi açıldı", lock_off: "Çocuk kilidi kapandı",
    dnd_saved: "Rahatsız etme kaydedildi", clean_sched_saved: "Planlı temizlik kaydedildi", ster_sched_saved: "Planlı sterilizasyon kaydedildi",
    delay_range: "Gecikme 0–600 sn olmalı", delay_saved: "Temizlik gecikmesi kaydedildi",
    ster_q: "UV sterilizasyon başlatılsın mı? Bu sırada kum kabında kedi olmamalı.", ster_started: "Sterilizasyon başlatıldı",
    del_cat_q: "{name} silinsin mi? Ziyaretleri etiketsiz kalır.", cat_deleted: "{name} silindi",
    dnd: "Rahatsız etme", child_lock: "Çocuk kilidi", chip_clean: "Temizlik {t}", chip_ster: "Sterilizasyon {t}",
    waste_bin: "Atık haznesi", full: "Dolu", pct: "~%{n}", cleans: "{n} temizlik", since: " · {d} beri",
    estimated: " · tahmini", bag_changed: "Poşeti değiştirdim", deodorizer: "Koku giderici", days: "{n} gün",
    days_unit: "gün", time_left: "kalan süre", time_left_cap: "Kalan süre", renewed: "Yeniledim",
    settings_title: "Kum kabı ayarları", lock_desc: "Cihazdaki tuşları kilitler", delay: "Temizlik gecikmesi",
    delay_desc: "Kedi çıktıktan sonra (sn)", save: "Kaydet", dnd_desc: "Bu sürede yalnızca elle temizlik yapılır",
    start: "Başlangıç", end: "Bitiş", sched_clean: "Planlı temizlik", sched_ster: "Planlı sterilizasyon", add_time: "+ Saat ekle",
    pour: "Kumu boşalt", pour_desc: "Kum değiştirmek için tamburdaki tüm kumu poşete boşaltır", pour_btn: "Boşalt",
    local_err: "Kum kabına yerel ağdan ulaşılamadı: {err}", delete: "Sil",
    no_sched_clean: "Planlı temizlik yok", no_sched_ster: "Planlı sterilizasyon yok", min: "dk", close: "Kapat",
    st_last_weight: "Son kilo", st_average: "Ortalama", st_change: "Değişim", st_today: "Bugün", visits_n: "{n} ziyaret",
    st_daily: "Günlük ort.", st_dur: "Ort. süre",
    learn_ok: "Ağırlığından tanıyorum ({n} ölçüm, ±{s} g)",
    learn_wip: "Öğreniyorum: {n}/{m} etiket. \"Bu kim?\" sorularında seçtikçe öğrenirim.",
    edit: "Düzenle", weight: "Kilo", last14: "Son 14 gün", visits: "Ziyaretler", no_visits: "Henüz ziyaret yok",
    chart_more: "Grafik için birkaç ölçüm daha lazım", vs_auto: "Otomatik tanındı · güven %{p}",
    vs_pending: "Etiket bekliyor", vs_not_cat_range: "Kedi değil (ağırlık mantıksız)", visit: "Ziyaret",
    not_learned: "Bu ağırlık kedinin normalinden çok farklı olduğu için öğrenmeye katılmadı.",
    still_in: "Kedi hâlâ içeride; çıkınca etiketleyebilirsin.", who_was: "Bu kimdi?", del_visit: "Ziyareti sil",
    pending_n: "Bekleyen ({n})", history: "Geçmiş", no_records: "Kayıt yok", color: "Renk", edit_cat: "Kediyi düzenle", new_cat: "Yeni kedi",
    name: "İsim", name_ph: "ör. Pamuk", hint: "Yaklaşık kilo", hint_sub: "(isteğe bağlı, öğrenmeyi hızlandırır)", hint_ph: "ör. 4,2",
    cancel: "Vazgeç", tap_photo: "Fotoğrafa dokunup seç", remove_photo: "Fotoğrafı kaldır", name_req: "İsim gerekli",
    hint_range: "Kilo 0–20 kg arası olmalı", saving: "Kaydediliyor…", saved: "{name} kaydedildi",
  },
};

// Active language/locale. Set by each card right before it renders (cards may differ via `language:`).
let KK_LANG = "en";
let KK_LOCALE = "en-US";
const T = (key, vars = {}) => {
  const s = KK_I18N[KK_LANG]?.[key] ?? KK_I18N.en[key] ?? key;
  return String(s).replace(/\{(\w+)\}/g, (_, k) => (vars[k] ?? ""));
};
// Plural-aware lookup: uses `<key>_one` when n === 1 and the language has it.
const P = (key, n, vars = {}) => T(n === 1 && KK_I18N[KK_LANG]?.[`${key}_one`] ? `${key}_one` : key, { n, ...vars });

const KK_STATUS = {
  standby: { icon: "mdi:check-circle-outline", tone: "ok" },
  cat_near: { icon: "mdi:paw", tone: "warn" },
  cat_in: { icon: "mdi:cat", tone: "busy" },
  cat_out: { icon: "mdi:exit-run", tone: "warn" },
  clean: { icon: "mdi:rotate-3d-variant", tone: "info" },
  smooth: { icon: "mdi:wave", tone: "info" },
  clear_sand: { icon: "mdi:delete-sweep", tone: "info" },
  sleep: { icon: "mdi:sleep", tone: "muted" },
  uv: { icon: "mdi:shield-sun-outline", tone: "info" },
  other: { icon: "mdi:help-circle-outline", tone: "muted" },
};

const KK_FAULTS = {
  full_fault: "mdi:delete-alert",
  box_out: "mdi:archive-alert",
  motor_fault: "mdi:engine-off",
  g_sensor_fault: "mdi:scale-off",
  filter_fault: "mdi:air-filter",
};

const KK_COLORS = ["#f4a261", "#2a9d8f", "#e76f51", "#8e7dbe", "#e9c46a", "#4ea8de", "#d16ba5", "#7a8b99"];
const KK_REASONS = ["learning", "ambiguous", "no_match", "no_cats", "untrained", "no_weight", "out_of_range"];
const reason = (r) => (KK_REASONS.includes(r) ? T(r === "untrained" ? "r_learning" : `r_${r}`) : "");

const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const _nf = {};
const kg = (g) => {
  if (g == null) return "–";
  _nf[KK_LOCALE] ||= new Intl.NumberFormat(KK_LOCALE, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  return _nf[KK_LOCALE].format(g / 1000);
};
const median = (a) => {
  if (!a.length) return null;
  const s = [...a].sort((x, y) => x - y);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};
const sameDay = (a, b) => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
const hm = (d) => d.toLocaleTimeString(KK_LOCALE, { hour: "2-digit", minute: "2-digit" });
const dm = (d) => d.toLocaleDateString(KK_LOCALE, { day: "numeric", month: "short" });

function ago(iso) {
  if (!iso) return "–";
  const d = new Date(iso);
  const s = (Date.now() - d.getTime()) / 1000;
  if (s < 60) return T("just_now");
  if (s < 3600) return T("min_ago", { n: Math.floor(s / 60) });
  const now = new Date();
  if (sameDay(d, now)) return T("h_ago", { n: Math.floor(s / 3600) });
  const y = new Date(now);
  y.setDate(now.getDate() - 1);
  if (sameDay(d, y)) return T("yesterday_l", { t: hm(d) });
  if (s < 7 * 86400) return P("days_ago", Math.floor(s / 86400));
  return dm(d);
}

function when(iso) {
  const d = new Date(iso);
  const now = new Date();
  const y = new Date(now);
  y.setDate(now.getDate() - 1);
  if (sameDay(d, now)) return T("today_at", { t: hm(d) });
  if (sameDay(d, y)) return T("yesterday_at", { t: hm(d) });
  return `${dm(d)} ${hm(d)}`;
}

function dur(s) {
  if (s == null) return "";
  if (s < 60) return T("sec", { n: s });
  return `${T("min_short", { n: Math.floor(s / 60) })} ${s % 60 ? T("sec", { n: s % 60 }) : ""}`.trim();
}

async function squarePhoto(file, size = 512) {
  const url = URL.createObjectURL(file);
  try {
    const img = await new Promise((res, rej) => {
      const i = new Image();
      i.onload = () => res(i);
      i.onerror = () => rej(new Error(T("photo_read")));
      i.src = url;
    });
    const side = Math.min(img.naturalWidth, img.naturalHeight);
    const c = document.createElement("canvas");
    c.width = c.height = size;
    c.getContext("2d").drawImage(img, (img.naturalWidth - side) / 2, (img.naturalHeight - side) / 2, side, side, 0, 0, size, size);
    return c.toDataURL("image/jpeg", 0.86);
  } finally {
    URL.revokeObjectURL(url);
  }
}

class KediKumuCard extends HTMLElement {
  static getStubConfig() {
    return { type: "custom:kedi-kumu-card" };
  }

  setConfig(config) {
    this._config = { show_controls: true, recent: 6, ...config };
    this.toggleAttribute("compact", !!this._config.compact);
    if (this._root) this._render();
  }

  _useLang() {
    const want = String(this._config?.language || this._hass?.locale?.language || this._hass?.language || "en").toLowerCase();
    KK_LANG = want.startsWith("tr") ? "tr" : "en";
    KK_LOCALE = KK_LANG === "tr" ? "tr-TR" : want.startsWith("en") ? want : "en-US";
  }

  set hass(hass) {
    const first = !this._hass;
    this._hass = hass;
    this._useLang();
    if (first) {
      this._setup();
      return;
    }
    const sig = this._entitySig();
    if (sig !== this._sig) {
      this._sig = sig;
      this._render();
    }
  }

  getCardSize() {
    return 9;
  }

  getGridOptions() {
    return { columns: 12, min_columns: 6, rows: "auto" };
  }

  connectedCallback() {
    if (this._hass && !this._unsub) this._subscribe();
    if (!this._tick) this._tick = setInterval(() => this._render(), 30000);
  }

  disconnectedCallback() {
    clearInterval(this._tick);
    this._tick = null;
    if (this._unsub) {
      this._unsub.then((u) => u && u()).catch(() => {});
      this._unsub = null;
    }
  }

  // ------------------------------------------------------------ data
  _setup() {
    this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `<style>${KK_CSS}</style><ha-card><div id="root"></div></ha-card><dialog id="dlg"></dialog>`;
    this._root = this.shadowRoot.getElementById("root");
    this._dlg = this.shadowRoot.getElementById("dlg");
    this._root.addEventListener("click", (e) => this._onClick(e));
    this._dlg.addEventListener("click", (e) => {
      if (e.target === this._dlg) return this._closeDialog();
      this._onClick(e);
    });
    this._dlg.addEventListener("close", () => (this._view = null));
    this._root.innerHTML = `<div class="loading"><ha-icon icon="mdi:cat"></ha-icon> ${T("loading")}</div>`;
    this._load();
    this._subscribe();
    if (!this._tick) this._tick = setInterval(() => this._render(), 30000);
  }

  _subscribe() {
    if (!this._hass || this._unsub) return;
    this._unsub = this._hass.connection
      .subscribeMessage(() => this._scheduleLoad(), { type: "kedi_kumu/subscribe" })
      .catch((err) => {
        this._unsub = null;
        this._error = err.message || String(err);
        this._render();
      });
  }

  _scheduleLoad() {
    clearTimeout(this._loadTimer);
    this._loadTimer = setTimeout(() => this._load(), 250);
  }

  async _load() {
    try {
      this._data = await this._hass.callWS({ type: "kedi_kumu/data" });
      this._error = null;
    } catch (err) {
      this._error = err.message || String(err);
    }
    this._sig = this._entitySig();
    this._render();
    this._refreshDialog();
  }

  _entitySig() {
    const c = this._data?.controls || {};
    return ["light", "bag_full", "lid", "auto_clean", "clean"]
      .map((k) => (c[k] && this._hass.states[c[k]] ? this._hass.states[c[k]].state : ""))
      .join("|");
  }

  _cat(id) {
    return this._data?.cats.find((c) => c.id === id);
  }

  _visit(id) {
    return this._data?.visits.find((v) => v.id === id) || (this._data?.current?.id === id ? this._data.current : null);
  }

  async _ws(msg, okText) {
    try {
      const r = await this._hass.callWS(msg);
      if (okText) this._toast(okText);
      return r;
    } catch (err) {
      this._toast(T("failed", { err: err.message || err }), true);
      throw err;
    }
  }

  _toast(text, bad = false) {
    let t = this._toastEl;
    if (!t) {
      t = this._toastEl = document.createElement("div");
      t.className = "toast";
    }
    const host = this._dlg?.open ? this._dlg : this.shadowRoot;
    if (t.parentNode !== host) host.appendChild(t);
    t.textContent = text;
    t.classList.toggle("bad", bad);
    t.classList.add("show");
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => t.classList.remove("show"), 2600);
  }

  // ------------------------------------------------------------ helpers
  _avatar(cat, size = "") {
    if (!cat) return `<div class="av ${size} unknown"><ha-icon icon="mdi:help"></ha-icon></div>`;
    const inner = cat.photo
      ? `<img src="${esc(cat.photo)}" alt="" loading="lazy">`
      : `<span>${esc(cat.name.trim().charAt(0).toLocaleUpperCase(KK_LOCALE))}</span>`;
    return `<div class="av ${size}" style="--c:${esc(cat.color || "#999")}">${inner}</div>`;
  }

  _catVisits(id) {
    return (this._data?.visits || []).filter((v) => v.cat_id === id && (v.status === "auto" || v.status === "manual"));
  }

  _trend(cat) {
    const vs = this._catVisits(cat.id).filter((v) => v.weight && v.learned !== false);
    if (vs.length < 4) return null;
    const now = Date.now();
    const recent = vs.filter((v) => now - new Date(v.start) < 7 * 864e5).map((v) => v.weight);
    let old = vs.filter((v) => {
      const a = now - new Date(v.start);
      return a > 23 * 864e5 && a < 37 * 864e5;
    });
    if (!old.length) old = vs.slice(0, Math.min(5, Math.floor(vs.length / 2)));
    if (!recent.length || !old.length) return null;
    const diff = Math.round(median(recent) - median(old.map((v) => v.weight)));
    return Math.abs(diff) < 30 ? 0 : diff;
  }

  _spark(cat) {
    const ws = this._catVisits(cat.id)
      .filter((v) => v.weight && v.learned !== false)
      .slice(-15)
      .map((v) => v.weight);
    if (ws.length < 3) return "";
    const min = Math.min(...ws) - 20;
    const max = Math.max(...ws) + 20;
    const pts = ws.map((w, i) => `${((i / (ws.length - 1)) * 64).toFixed(1)},${(18 - ((w - min) / (max - min)) * 16 - 1).toFixed(1)}`);
    return `<svg class="spark" viewBox="0 0 64 18" preserveAspectRatio="none"><polyline points="${pts.join(" ")}" style="stroke:${esc(cat.color)}"/></svg>`;
  }

  _statusBadge(v) {
    if (v.status === "auto") return `<span class="badge auto" title="${T("auto_recognized")}">${Math.round((v.confidence || 0) * 100)}%</span>`;
    if (v.status === "manual") return `<span class="badge manual" title="${T("picked_manually")}"><ha-icon icon="mdi:hand-back-right"></ha-icon></span>`;
    if (v.status === "pending") return `<span class="badge pending">?</span>`;
    return `<span class="badge none"><ha-icon icon="mdi:close"></ha-icon></span>`;
  }

  _visitName(v) {
    if (v.status === "not_cat") return T("not_cat");
    const cat = this._cat(v.cat_id);
    if (cat) return cat.name;
    const s = this._cat(v.suggestion);
    return s ? `${s.name}?` : T("unknown");
  }

  // ------------------------------------------------------------ render
  _render() {
    if (!this._root) return;
    this._useLang();
    if (this._error && !this._data) {
      this._root.innerHTML = `<div class="empty"><ha-icon icon="mdi:alert-circle-outline"></ha-icon><div><b>${T("unreachable")}</b><br><small>${esc(this._error)}</small></div></div>`;
      return;
    }
    if (!this._data) return;
    const d = this._data;
    const pending = d.visits.filter((v) => v.status === "pending").reverse();
    this._root.innerHTML = `
      ${this._renderHead(d)}
      ${this._renderAlerts(d)}
      ${d.cats.length ? "" : this._renderOnboarding()}
      ${pending.length ? this._renderPending(pending) : ""}
      ${d.cats.length ? this._renderCats(d) : ""}
      ${this._config.compact ? this._renderCompactFoot(d) : `
      ${this._renderToday(d)}
      ${this._renderGauges(d)}
      ${this._renderInfo(d)}
      ${this._renderRecent(d)}
      ${this._config.show_controls ? this._renderControls(d) : ""}`}`;
  }

  _renderCompactFoot(d) {
    const now = new Date();
    const today = d.visits.filter((v) => sameDay(new Date(v.start), now) && v.status !== "not_cat").length;
    const last = [...d.visits].reverse().find((v) => v.status !== "not_cat");
    return `<button class="compact-foot" data-action="history">
      <span>${P("today_visits", today)}${last ? T("last_by", { name: esc(this._visitName(last)), ago: ago(last.start) }) : ""}</span>
      <ha-icon icon="mdi:chevron-right"></ha-icon></button>`;
  }

  _renderHead(d) {
    const cur = d.current;
    let st = KK_STATUS[d.status] || KK_STATUS.other;
    if (d.settings?.sterilizing && d.status === "standby") st = KK_STATUS.uv;
    let label = T(`s_${KK_STATUS[d.status] ? d.status : "other"}`);
    if (st === KK_STATUS.uv) label = T("s_uv");
    let av = "";
    if (cur) {
      const cat = this._cat(cur.cat_id) || this._cat(cur.suggestion);
      st = KK_STATUS.cat_in;
      label = cat ? T("in_box", { name: `${esc(cat.name)}${cur.cat_id ? "" : "?"}` }) : T("cat_in_box");
      av = this._avatar(cat, "xs");
    }
    return `
      <div class="head">
        <div class="title"><ha-icon icon="mdi:cat"></ha-icon><span>${esc(this._config.title || T("title"))}</span></div>
        <div class="head-r">
          <div class="status ${st.tone}">${av || `<ha-icon icon="${st.icon}"></ha-icon>`}<span>${label}</span>${
            cur ? `<small>${kg(cur.weight)} kg</small>` : ""
          }</div>
          ${d.cats.length ? `<button class="icon add-cat" data-action="add-cat" title="${T("add_cat")}" aria-label="${T("add_cat")}"><ha-icon icon="mdi:plus"></ha-icon></button>` : ""}
        </div>
      </div>`;
  }

  _renderAlerts(d) {
    const c = d.controls || {};
    const st = (id) => (id && this._hass.states[id] ? this._hass.states[id].state : null);
    const out = [];
    if (!d.hooked) out.push(`<div class="alert warn"><ha-icon icon="mdi:link-variant-off"></ha-icon><span>${T("waiting_link")}</span></div>`);
    const faults = new Set(d.faults || []);
    if (st(c.bag_full) === "on") faults.add("full_fault");
    if (st(c.lid) === "on") faults.add("box_out");
    for (const f of faults) {
      const text = KK_FAULTS[f] ? T(`f_${f}`) : esc(f);
      out.push(`<div class="alert bad"><ha-icon icon="${KK_FAULTS[f] || "mdi:alert"}"></ha-icon><span>${text}</span></div>`);
    }
    if (d.scale_suspect)
      out.push(`<div class="alert warn"><ha-icon icon="mdi:scale-unbalanced"></ha-icon><span>${T("scale_suspect")}</span><button class="link" data-action="reset-scale">${T("ok")}</button></div>`);
    return out.length ? `<div class="alerts">${out.join("")}</div>` : "";
  }

  _renderOnboarding() {
    return `
      <div class="onboard">
        <div class="ob-icon"><ha-icon icon="mdi:cat"></ha-icon></div>
        <div class="ob-text">
          <b>${T("ob_title")}</b>
          <span>${esc(T("ob_text"))}</span>
        </div>
        <button class="primary" data-action="add-cat"><ha-icon icon="mdi:plus"></ha-icon>${T("add_cat")}</button>
      </div>`;
  }

  _renderPending(pending) {
    const d = this._data;
    if (!d.cats.length) return "";
    const shown = pending.slice(0, 3);
    const cards = shown
      .map((v) => {
        const picks = d.cats
          .map(
            (c) => `<button class="pick ${v.suggestion === c.id ? "sugg" : ""}" data-action="assign" data-visit="${v.id}" data-cat="${c.id}" style="--c:${esc(c.color)}">
              ${this._avatar(c, "sm")}<span>${esc(c.name)}</span></button>`
          )
          .join("");
        return `
        <div class="ask">
          <div class="ask-head">
            <div><b>${T("who")}</b> <span class="muted">${when(v.start)}</span></div>
            <div class="ask-meta"><span class="w">${kg(v.weight)} kg</span>${v.duration != null ? ` · ${dur(v.duration)}` : ""}</div>
          </div>
          ${reason(v.reason) ? `<div class="ask-reason">${reason(v.reason)}${v.suggestion ? ` · ${T("my_guess")} <b>${esc(this._cat(v.suggestion)?.name || "")}</b>` : ""}</div>` : ""}
          <div class="picks">${picks}
            <button class="pick none" data-action="assign" data-visit="${v.id}" data-cat="none"><div class="av sm unknown"><ha-icon icon="mdi:close"></ha-icon></div><span>${T("not_cat")}</span></button>
          </div>
        </div>`;
      })
      .join("");
    const more = pending.length > shown.length ? `<button class="link more" data-action="history" data-filter="pending">${P("more_pending", pending.length - shown.length)}</button>` : "";
    return `<div class="section asks">${cards}${more}</div>`;
  }

  _renderCats(d) {
    const tiles = d.cats
      .map((c) => {
        const t = this._trend(c);
        const trend =
          t == null ? "" : t === 0 ? `<span class="trend flat">${T("steady")}</span>` : `<span class="trend ${t > 0 ? "up" : "down"}">${t > 0 ? "▲" : "▼"} ${Math.abs(t)} g</span>`;
        const w = c.last_weight ?? c.center ?? c.hint;
        const learn = c.trained
          ? `<span class="learn ok"><ha-icon icon="mdi:check-decagram"></ha-icon>${T("knows")}</span>`
          : `<span class="learn" title="${T("learning")}"><span class="bar"><i style="width:${Math.min(100, (c.manual_count / d.min_manual) * 100)}%"></i></span>${this._config.compact ? "" : `${T("learning")} `}${c.manual_count}/${d.min_manual}</span>`;
        return `
        <button class="cat" data-action="cat" data-id="${c.id}" style="--c:${esc(c.color)}">
          ${this._avatar(c, "lg")}
          <div class="cat-name">${esc(c.name)}</div>
          <div class="cat-w">${w ? `${kg(w)}<small> kg</small>` : `<small>${T("no_weight")}</small>`} ${trend}</div>
          ${this._spark(c)}
          <div class="cat-meta">${c.today ? T("today_n", { n: c.today }) : T("none_today")}${this._config.compact ? "" : ` · ${ago(c.last_visit)}`}</div>
          ${learn}
        </button>`;
      })
      .join("");
    return `<div class="section cats" style="--cols:${Math.min(4, d.cats.length)}">${tiles}</div>`;
  }

  _renderToday(d) {
    const now = new Date();
    const today = d.visits.filter((v) => sameDay(new Date(v.start), now) && v.status !== "not_cat");
    const nowPct = ((now.getHours() * 60 + now.getMinutes()) / 1440) * 100;
    const dots = today
      .map((v) => {
        const t = new Date(v.start);
        const pct = ((t.getHours() * 60 + t.getMinutes()) / 1440) * 100;
        const cat = this._cat(v.cat_id);
        return `<button class="dot ${cat ? "" : "unk"}" style="left:${pct.toFixed(2)}%;--c:${esc(cat?.color || "#9e9e9e")}" data-action="visit" data-id="${v.id}" title="${esc(this._visitName(v))} · ${hm(t)} · ${kg(v.weight)} kg"></button>`;
      })
      .join("");
    const lastClean = d.last_clean ? T("last_clean", { ago: ago(d.last_clean) }) : "";
    return `
      <div class="section today">
        <div class="sec-title"><span>${P("today_visits", today.length)}</span><span class="muted">${lastClean}</span></div>
        <div class="tl"><div class="tl-track"></div><div class="tl-now" style="left:${nowPct.toFixed(2)}%"></div>${dots}
          <div class="tl-ticks"><span>00</span><span>06</span><span>12</span><span>18</span><span>24</span></div></div>
      </div>`;
  }

  _renderRecent(d) {
    const rows = d.visits.slice(-this._config.recent).reverse();
    if (!rows.length) return `<div class="section"><div class="muted center">${T("no_visits_yet")}</div></div>`;
    return `
      <div class="section recent">
        <div class="sec-title"><span>${T("recent")}</span><button class="link" data-action="history">${T("all")}</button></div>
        ${rows.map((v) => this._row(v)).join("")}
      </div>`;
  }

  _row(v) {
    const cat = this._cat(v.cat_id);
    return `
      <button class="row ${v.status}" data-action="visit" data-id="${v.id}">
        ${this._avatar(cat || (v.status === "pending" ? this._cat(v.suggestion) : null), "sm")}
        <div class="row-main"><div class="row-name">${esc(this._visitName(v))} ${this._statusBadge(v)}</div><div class="muted">${when(v.start)}</div></div>
        <div class="row-w">${kg(v.weight)} <small>kg</small><div class="muted">${dur(v.duration)}</div></div>
      </button>`;
  }

  _renderControls(d) {
    const c = d.controls || {};
    const s = (id) => (id ? this._hass.states[id] : null);
    const busy = !!d.current || ["cat_in", "cat_near", "clean", "smooth", "clear_sand"].includes(d.status);
    const light = s(c.light);
    const auto = s(c.auto_clean);
    const ster = !!d.settings?.sterilizing || d.status === "uv";
    const btn = (action, icon, label, on, disabled) =>
      `<button class="ctl ${on ? "on" : ""}" data-action="${action}" ${disabled ? "disabled" : ""}><ha-icon icon="${icon}"></ha-icon><span>${label}</span></button>`;
    return `
      <div class="controls">
        ${c.clean ? btn("clean", "mdi:broom", d.status === "clean" ? T("s_clean") : T("clean"), d.status === "clean", busy) : ""}
        ${d.hooked ? btn("level", "mdi:wave", d.status === "smooth" ? T("leveling") : T("level"), d.status === "smooth", busy) : ""}
        ${d.hooked ? btn(ster ? "stop-sterilize" : "sterilize", "mdi:shield-sun-outline", ster ? T("stop_ster") : T("sterilize"), ster, !ster && busy) : ""}
        ${light ? btn("light", "mdi:lightbulb", T("drum_light"), light.state === "on", false) : ""}
        ${auto ? btn("auto", "mdi:autorenew", T("auto_clean"), auto.state === "on", false) : ""}
        <button class="ctl" data-action="settings"><ha-icon icon="mdi:cog"></ha-icon><span>${T("settings")}</span></button>
      </div>`;
  }

  // ------------------------------------------------------------ actions
  async _onClick(e) {
    const el = e.target.closest("[data-action]");
    if (!el || el.disabled) return;
    this._useLang();
    const a = el.dataset.action;
    const c = this._data?.controls || {};
    switch (a) {
      case "add-cat":
        return this._openEditor(null);
      case "cat":
        return this._openCat(el.dataset.id);
      case "edit-cat":
        return this._openEditor(el.dataset.id);
      case "visit":
        return this._openVisit(el.dataset.id);
      case "history":
        return this._openHistory(el.dataset.filter || "all");
      case "filter":
        return this._openHistory(el.dataset.filter);
      case "close":
        return this._closeDialog();
      case "assign": {
        el.classList.add("chosen");
        const catId = el.dataset.cat === "none" ? null : el.dataset.cat;
        const name = catId ? this._cat(catId)?.name : T("not_cat");
        await this._ws({ type: "kedi_kumu/visit/assign", visit_id: el.dataset.visit, cat_id: catId }, T("saved_as", { name }));
        if (this._view?.type === "visit") this._closeDialog();
        return;
      }
      case "delete-visit":
        if (!confirm(T("del_visit_q"))) return;
        await this._ws({ type: "kedi_kumu/visit/delete", visit_id: el.dataset.id }, T("visit_deleted"));
        return this._closeDialog();
      case "reset-scale":
        return this._ws({ type: "kedi_kumu/reset_scale" });
      case "clean":
        if (!c.clean) return;
        await this._hass.callService("button", "press", { entity_id: c.clean });
        return this._toast(T("clean_started"));
      case "light":
        return this._hass.callService("light", "toggle", { entity_id: c.light });
      case "reset-bin":
        if (!confirm(T("bin_q"))) return;
        return this._ws({ type: "kedi_kumu/command", action: "reset_bin" }, T("bin_reset"));
      case "filter-reset":
        e.stopPropagation();
        if (!confirm(T("filter_q"))) return;
        return this._ws({ type: "kedi_kumu/command", action: "filter_reset" }, T("filter_done"));
      case "pour-sand":
        if (!confirm(T("pour_q1"))) return;
        if (!confirm(T("pour_q2"))) return;
        this._closeDialog();
        return this._ws({ type: "kedi_kumu/command", action: "pour_sand" }, T("s_clear_sand"));
      case "level":
        return this._ws({ type: "kedi_kumu/command", action: "level" }, T("leveling_toast"));
      case "stop-sterilize":
        return this._ws({ type: "kedi_kumu/command", action: "stop_sterilize" }, T("ster_stopped"));
      case "settings":
        return this._openSettings();
      case "toggle-lock":
        return this._ws({ type: "kedi_kumu/command", action: "child_lock", value: el.checked }, el.checked ? T("lock_on") : T("lock_off"));
      case "save-dnd": {
        const q = (sel) => this._dlg.querySelector(sel);
        return this._ws({ type: "kedi_kumu/command", action: "dnd", value: { enabled: q("#dnd-on").checked, start: q("#dnd-start").value, end: q("#dnd-end").value } }, T("dnd_saved"));
      }
      case "add-clean":
        this._readSchedules();
        this._sched.clean.push({ time: "04:00", enabled: true });
        return this._renderSchedules();
      case "del-clean":
        this._readSchedules();
        this._sched.clean.splice(+el.dataset.i, 1);
        return this._renderSchedules();
      case "save-clean":
        this._readSchedules();
        return this._ws({ type: "kedi_kumu/command", action: "clean_schedule", value: this._sched.clean }, T("clean_sched_saved"));
      case "add-ster":
        this._readSchedules();
        this._sched.ster.push({ time: "02:00", minutes: 5, enabled: true });
        return this._renderSchedules();
      case "del-ster":
        this._readSchedules();
        this._sched.ster.splice(+el.dataset.i, 1);
        return this._renderSchedules();
      case "save-ster":
        this._readSchedules();
        return this._ws({ type: "kedi_kumu/command", action: "sterilize_schedule", value: this._sched.ster }, T("ster_sched_saved"));
      case "save-delay": {
        const v = parseInt(this._dlg.querySelector("#delay").value, 10);
        if (!isFinite(v) || v < 0 || v > 600) return this._toast(T("delay_range"), true);
        await this._hass.callService("number", "set_value", { entity_id: c.clean_delay, value: v });
        return this._toast(T("delay_saved"));
      }
      case "sterilize":
        if (!confirm(T("ster_q"))) return;
        return this._ws({ type: "kedi_kumu/command", action: "sterilize" }, T("ster_started"));
      case "auto":
        return this._hass.callService("switch", "toggle", { entity_id: c.auto_clean });
      case "pick-color": {
        this._dlg.querySelectorAll(".swatch").forEach((s) => s.classList.toggle("sel", s === el));
        this._edit.color = el.dataset.color;
        const av = this._dlg.querySelector(".editor .av");
        if (av) av.style.setProperty("--c", el.dataset.color);
        return;
      }
      case "remove-photo":
        this._edit.photo = null;
        this._edit.removePhoto = true;
        return this._renderEditorPhoto();
      case "save-cat":
        return this._saveCat();
      case "delete-cat": {
        const cat = this._cat(el.dataset.id);
        if (!cat || !confirm(T("del_cat_q", { name: cat.name }))) return;
        await this._ws({ type: "kedi_kumu/cat/delete", cat_id: cat.id }, T("cat_deleted", { name: cat.name }));
        return this._closeDialog();
      }
    }
  }

  // ------------------------------------------------------------ settings
  _renderInfo(d) {
    const st = d.settings || {};
    const chips = [];
    if (st.dnd?.enabled) chips.push(`<span class="chip-i"><ha-icon icon="mdi:sleep"></ha-icon>${T("dnd")} ${st.dnd.start}–${st.dnd.end}</span>`);
    if (st.child_lock) chips.push(`<span class="chip-i"><ha-icon icon="mdi:lock"></ha-icon>${T("child_lock")}</span>`);
    const on = (st.clean_schedule || []).filter((e) => e.enabled).map((e) => e.time);
    if (on.length) chips.push(`<span class="chip-i"><ha-icon icon="mdi:calendar-clock"></ha-icon>${T("chip_clean", { t: on.join(", ") })}</span>`);
    const ster = (st.sterilize_schedule || []).filter((e) => e.enabled).map((e) => e.time);
    if (ster.length) chips.push(`<span class="chip-i"><ha-icon icon="mdi:shield-sun-outline"></ha-icon>${T("chip_ster", { t: ster.join(", ") })}</span>`);
    return chips.length ? `<button class="info-row" data-action="settings">${chips.join("")}</button>` : "";
  }

  _renderGauges(d) {
    const w = d.waste;
    const days = d.settings?.deodorizer_days;
    if (!w && days == null) return "";
    const out = [];
    if (w) {
      const tone = w.percent >= 90 ? "bad" : w.percent >= 75 ? "warn" : "ok";
      const since = w.since ? dm(new Date(w.since)) : null;
      out.push(`<div class="gauge">
        <div class="g-top"><ha-icon icon="mdi:delete-variant"></ha-icon><span>${T("waste_bin")}</span><b>${w.full ? T("full") : T("pct", { n: w.percent })}</b></div>
        <div class="g-bar ${tone}"><i style="width:${Math.min(100, w.percent)}%"></i></div>
        <div class="g-foot"><span class="muted">${P("cleans", w.count)}${since ? T("since", { d: since }) : ""}${w.learned ? "" : T("estimated")}</span>
          <button class="link" data-action="reset-bin">${T("bag_changed")}</button></div>
      </div>`);
    }
    if (days != null) {
      const pct = Math.max(0, Math.min(100, (days / 30) * 100));
      out.push(`<button class="gauge" data-action="settings">
        <div class="g-top"><ha-icon icon="mdi:spray"></ha-icon><span>${T("deodorizer")}</span><b>${P("days", days)}</b></div>
        <div class="g-bar ${days <= 3 ? "warn" : "ok"}"><i style="width:${pct}%"></i></div>
        <div class="g-foot"><span class="muted">${T("time_left")}</span><span class="link" data-action="filter-reset">${T("renewed")}</span></div>
      </button>`);
    }
    return `<div class="gauges">${out.join("")}</div>`;
  }

  _openSettings() {
    const d = this._data;
    const st = d.settings || {};
    const c = d.controls || {};
    const delay = c.clean_delay && this._hass.states[c.clean_delay] ? parseInt(this._hass.states[c.clean_delay].state, 10) : null;
    const dnd = st.dnd || { start: "22:00", end: "07:00", enabled: false };
    this._sched = {
      clean: (st.clean_schedule || []).map((e) => ({ ...e })),
      ster: (st.sterilize_schedule || []).map((e) => ({ ...e })),
    };
    const sw = (id, checked, action = "") => `<label class="sw"><input type="checkbox" id="${id}" ${checked ? "checked" : ""} ${action ? `data-action="${action}"` : ""}><span></span></label>`;
    this._showDialog(
      `${this._dlgHead(T("settings_title"))}
      <div class="set-sec">
        <div class="set-row"><ha-icon icon="mdi:spray"></ha-icon><div class="grow"><b>${T("deodorizer")}</b><div class="muted">${T("time_left_cap")}</div></div>
          <div class="big ${st.deodorizer_days != null && st.deodorizer_days <= 3 ? "warn" : ""}">${st.deodorizer_days ?? "–"} <small>${P("days_unit", st.deodorizer_days)}</small></div></div>
        <div class="set-row"><ha-icon icon="mdi:lock"></ha-icon><div class="grow"><b>${T("child_lock")}</b><div class="muted">${T("lock_desc")}</div></div>${sw("lock", st.child_lock, "toggle-lock")}</div>
        ${delay != null ? `<div class="set-row"><ha-icon icon="mdi:timer-sand"></ha-icon><div class="grow"><b>${T("delay")}</b><div class="muted">${T("delay_desc")}</div></div>
          <input id="delay" class="num" type="number" min="0" max="600" value="${delay}"><button class="mini" data-action="save-delay">${T("save")}</button></div>` : ""}
      </div>
      <div class="set-sec">
        <div class="set-row"><ha-icon icon="mdi:sleep"></ha-icon><div class="grow"><b>${T("dnd")}</b><div class="muted">${T("dnd_desc")}</div></div>${sw("dnd-on", dnd.enabled)}</div>
        <div class="set-row times"><span>${T("start")}</span><input id="dnd-start" type="time" value="${esc(dnd.start)}"><span>${T("end")}</span><input id="dnd-end" type="time" value="${esc(dnd.end)}">
          <button class="mini" data-action="save-dnd">${T("save")}</button></div>
      </div>
      <div class="set-sec"><div class="set-title"><ha-icon icon="mdi:calendar-clock"></ha-icon><b>${T("sched_clean")}</b></div><div id="sched-clean"></div>
        <div class="set-actions"><button class="mini ghost" data-action="add-clean">${T("add_time")}</button><button class="mini" data-action="save-clean">${T("save")}</button></div></div>
      <div class="set-sec"><div class="set-title"><ha-icon icon="mdi:shield-sun-outline"></ha-icon><b>${T("sched_ster")}</b></div><div id="sched-ster"></div>
        <div class="set-actions"><button class="mini ghost" data-action="add-ster">${T("add_time")}</button><button class="mini" data-action="save-ster">${T("save")}</button></div></div>
      <div class="set-sec">
        <div class="set-row"><ha-icon icon="mdi:delete-sweep"></ha-icon><div class="grow"><b>${T("pour")}</b><div class="muted">${T("pour_desc")}</div></div>
          <button class="mini danger" data-action="pour-sand" ${["cat_in", "cat_near", "clean", "smooth", "clear_sand"].includes(d.status) || d.current ? "disabled" : ""}>${T("pour_btn")}</button></div>
      </div>
      ${d.local?.error ? `<div class="note">${T("local_err", { err: esc(d.local.error) })}</div>` : ""}`,
      { type: "settings" }
    );
    this._renderSchedules();
  }

  _renderSchedules() {
    const sw = (cls, i, checked) => `<label class="sw"><input type="checkbox" class="${cls}" data-i="${i}" ${checked ? "checked" : ""}><span></span></label>`;
    const clean = this._dlg.querySelector("#sched-clean");
    if (clean)
      clean.innerHTML = this._sched.clean.length
        ? this._sched.clean.map((e, i) => `<div class="set-row sched"><input type="time" class="c-time" data-i="${i}" value="${esc(e.time)}"><span class="grow"></span>${sw("c-on", i, e.enabled)}<button class="icon sm" data-action="del-clean" data-i="${i}" aria-label="${T("delete")}"><ha-icon icon="mdi:delete-outline"></ha-icon></button></div>`).join("")
        : `<div class="muted pad">${T("no_sched_clean")}</div>`;
    const ster = this._dlg.querySelector("#sched-ster");
    if (ster)
      ster.innerHTML = this._sched.ster.length
        ? this._sched.ster.map((e, i) => `<div class="set-row sched"><input type="time" class="s-time" data-i="${i}" value="${esc(e.time)}"><input type="number" class="s-min num" data-i="${i}" min="1" max="120" value="${e.minutes}"><span class="muted">${T("min")}</span><span class="grow"></span>${sw("s-on", i, e.enabled)}<button class="icon sm" data-action="del-ster" data-i="${i}" aria-label="${T("delete")}"><ha-icon icon="mdi:delete-outline"></ha-icon></button></div>`).join("")
        : `<div class="muted pad">${T("no_sched_ster")}</div>`;
  }

  _readSchedules() {
    const all = (sel) => [...this._dlg.querySelectorAll(sel)];
    all(".c-time").forEach((el) => (this._sched.clean[+el.dataset.i].time = el.value || "00:00"));
    all(".c-on").forEach((el) => (this._sched.clean[+el.dataset.i].enabled = el.checked));
    all(".s-time").forEach((el) => (this._sched.ster[+el.dataset.i].time = el.value || "00:00"));
    all(".s-min").forEach((el) => (this._sched.ster[+el.dataset.i].minutes = Math.min(120, Math.max(1, parseInt(el.value, 10) || 5))));
    all(".s-on").forEach((el) => (this._sched.ster[+el.dataset.i].enabled = el.checked));
  }

  // ------------------------------------------------------------ dialogs
  _showDialog(html, view) {
    this._view = view;
    this._dlg.innerHTML = `<div class="dlg">${html}</div>`;
    if (!this._dlg.open) this._dlg.showModal();
  }

  _closeDialog() {
    if (this._dlg.open) this._dlg.close();
    this._view = null;
  }

  _refreshDialog() {
    const v = this._view;
    if (!v || !this._dlg.open) return;
    this._useLang();
    const scroll = this._dlg.querySelector(".dlg")?.scrollTop || 0;
    if (v.type === "cat") {
      if (!this._cat(v.id)) return this._closeDialog();
      this._openCat(v.id);
    } else if (v.type === "history") this._openHistory(v.filter);
    else if (v.type === "visit") {
      if (!this._visit(v.id)) return this._closeDialog();
      this._openVisit(v.id);
    } else return;
    const box = this._dlg.querySelector(".dlg");
    if (box) box.scrollTop = scroll;
  }

  _dlgHead(title, extra = "") {
    return `<div class="dlg-head"><div class="dlg-title">${title}</div>${extra}<button class="icon" data-action="close" aria-label="${T("close")}"><ha-icon icon="mdi:close"></ha-icon></button></div>`;
  }

  _openCat(id) {
    const cat = this._cat(id);
    if (!cat) return;
    const vs = this._catVisits(id);
    const learned = vs.filter((v) => v.weight && v.learned !== false);
    const now = Date.now();
    const last7 = vs.filter((v) => now - new Date(v.start) < 7 * 864e5);
    const durs = last7.map((v) => v.duration).filter((x) => x != null);
    const t = this._trend(cat);
    const stats = [
      [T("st_last_weight"), cat.last_weight ? `${kg(cat.last_weight)} kg` : "–"],
      [T("st_average"), cat.center ? `${kg(cat.center)} kg` : "–"],
      [T("st_change"), t == null ? "–" : t === 0 ? T("steady") : `${t > 0 ? "+" : "−"}${Math.abs(t)} g`],
      [T("st_today"), P("visits_n", cat.today)],
      [T("st_daily"), last7.length ? T("visits_n", { n: (last7.length / 7).toLocaleString(KK_LOCALE, { maximumFractionDigits: 1 }) }) : "–"],
      [T("st_dur"), durs.length ? dur(Math.round(durs.reduce((a, b) => a + b, 0) / durs.length)) : "–"],
    ];
    const learnText = cat.trained
      ? T("learn_ok", { n: cat.samples, s: cat.spread })
      : esc(T("learn_wip", { n: cat.manual_count, m: this._data.min_manual }));
    this._showDialog(
      `${this._dlgHead("", `<button class="icon" data-action="edit-cat" data-id="${id}" aria-label="${T("edit")}"><ha-icon icon="mdi:pencil"></ha-icon></button>`)}
      <div class="profile" style="--c:${esc(cat.color)}">
        ${this._avatar(cat, "xl")}
        <div class="p-name">${esc(cat.name)}</div>
        <div class="p-learn ${cat.trained ? "ok" : ""}">${learnText}</div>
      </div>
      <div class="stats">${stats.map(([k, v]) => `<div class="stat"><div class="muted">${k}</div><div class="sv">${v}</div></div>`).join("")}</div>
      <div class="chart-title">${T("weight")}</div>
      ${this._weightChart(learned, cat)}
      <div class="chart-title">${T("last14")}</div>
      ${this._barChart(vs, cat.color)}
      <div class="chart-title">${T("visits")}</div>
      <div class="list">${vs.slice(-12).reverse().map((v) => this._row(v)).join("") || `<div class="muted center">${T("no_visits")}</div>`}</div>`,
      { type: "cat", id }
    );
  }

  _weightChart(visits, cat) {
    const pts = visits.map((v) => ({ t: new Date(v.start).getTime(), w: v.weight })).filter((p) => now90(p.t));
    function now90(t) {
      return Date.now() - t < 90 * 864e5;
    }
    if (pts.length < 2) return `<div class="chart-empty muted">${T("chart_more")}</div>`;
    const W = 480, H = 170, L = 44, R = 10, T = 12, B = 24;
    const tmin = pts[0].t, tmax = Math.max(pts[pts.length - 1].t, tmin + 864e5);
    let wmin = Math.min(...pts.map((p) => p.w)), wmax = Math.max(...pts.map((p) => p.w));
    const pad = Math.max(40, (wmax - wmin) * 0.15);
    wmin -= pad;
    wmax += pad;
    const x = (t) => L + ((t - tmin) / (tmax - tmin)) * (W - L - R);
    const y = (w) => T + (1 - (w - wmin) / (wmax - wmin)) * (H - T - B);
    const smooth = pts.map((p, i) => ({ t: p.t, w: median(pts.slice(Math.max(0, i - 2), i + 3).map((q) => q.w)) }));
    const line = smooth.map((p) => `${x(p.t).toFixed(1)},${y(p.w).toFixed(1)}`).join(" ");
    const area = `${L},${H - B} ${line} ${x(smooth[smooth.length - 1].t).toFixed(1)},${H - B}`;
    const grid = [0, 0.5, 1]
      .map((f) => {
        const w = wmin + f * (wmax - wmin);
        return `<line x1="${L}" x2="${W - R}" y1="${y(w)}" y2="${y(w)}" class="grid"/><text x="${L - 6}" y="${y(w) + 4}" text-anchor="end">${kg(w)}</text>`;
      })
      .join("");
    const fmt = (t) => dm(new Date(t));
    return `<svg class="chart" viewBox="0 0 ${W} ${H}" style="--c:${esc(cat.color)}">
      <defs><linearGradient id="g${cat.id}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="${esc(cat.color)}" stop-opacity=".28"/><stop offset="1" stop-color="${esc(cat.color)}" stop-opacity="0"/></linearGradient></defs>
      ${grid}
      <polygon points="${area}" fill="url(#g${cat.id})"/>
      <polyline points="${line}" class="line"/>
      ${pts.map((p) => `<circle cx="${x(p.t).toFixed(1)}" cy="${y(p.w).toFixed(1)}" r="2.6" class="pt"><title>${fmt(p.t)} · ${kg(p.w)} kg</title></circle>`).join("")}
      <text x="${L}" y="${H - 6}">${fmt(tmin)}</text><text x="${W - R}" y="${H - 6}" text-anchor="end">${fmt(tmax)}</text>
    </svg>`;
  }

  _barChart(visits, color) {
    const days = [];
    const now = new Date();
    for (let i = 13; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(now.getDate() - i);
      days.push({ d, n: visits.filter((v) => sameDay(new Date(v.start), d)).length });
    }
    const max = Math.max(3, ...days.map((x) => x.n));
    const W = 480, H = 90, B = 18, bw = W / 14;
    const bars = days
      .map((x, i) => {
        const h = ((H - B - 14) * x.n) / max;
        return `<rect x="${(i * bw + 4).toFixed(1)}" y="${(H - B - h).toFixed(1)}" width="${(bw - 8).toFixed(1)}" height="${Math.max(h, 1.5).toFixed(1)}" rx="4" class="${x.n ? "bar" : "bar zero"}"/>
          ${x.n ? `<text x="${(i * bw + bw / 2).toFixed(1)}" y="${(H - B - h - 3).toFixed(1)}" text-anchor="middle">${x.n}</text>` : ""}
          <text x="${(i * bw + bw / 2).toFixed(1)}" y="${H - 4}" text-anchor="middle" class="${i === 13 ? "strong" : ""}">${x.d.getDate()}</text>`;
      })
      .join("");
    return `<svg class="chart bars" viewBox="0 0 ${W} ${H}" style="--c:${esc(color)}">${bars}</svg>`;
  }

  _openVisit(id) {
    const v = this._visit(id);
    if (!v) return;
    const d = this._data;
    const cat = this._cat(v.cat_id);
    const statusText = {
      auto: T("vs_auto", { p: Math.round((v.confidence || 0) * 100) }),
      manual: T("picked_manually"),
      pending: `${T("vs_pending")}${reason(v.reason) ? ` · ${reason(v.reason)}` : ""}`,
      not_cat: v.reason === "out_of_range" ? T("vs_not_cat_range") : T("not_cat"),
    }[v.status] || "";
    const isCurrent = d.current?.id === id;
    const picks = d.cats
      .map(
        (c) => `<button class="pick ${v.cat_id === c.id ? "sel" : ""} ${!v.cat_id && v.suggestion === c.id ? "sugg" : ""}" data-action="assign" data-visit="${v.id}" data-cat="${c.id}" style="--c:${esc(c.color)}" ${isCurrent ? "disabled" : ""}>
          ${this._avatar(c, "sm")}<span>${esc(c.name)}</span></button>`
      )
      .join("");
    this._showDialog(
      `${this._dlgHead(T("visit"))}
      <div class="visit-hero">
        ${this._avatar(cat || this._cat(v.suggestion), "lg")}
        <div>
          <div class="vh-name">${esc(this._visitName(v))}</div>
          <div class="muted">${when(v.start)}${v.duration != null ? ` · ${dur(v.duration)}` : ""}</div>
          <div class="vh-status">${statusText}</div>
        </div>
        <div class="vh-w">${kg(v.weight)}<small> kg</small></div>
      </div>
      ${v.status === "manual" && v.learned === false ? `<div class="note">${T("not_learned")}</div>` : ""}
      ${isCurrent ? `<div class="note">${T("still_in")}</div>` : `
      <div class="chart-title">${T("who_was")}</div>
      <div class="picks wrap">${picks}
        <button class="pick none ${v.status === "not_cat" ? "sel" : ""}" data-action="assign" data-visit="${v.id}" data-cat="none"><div class="av sm unknown"><ha-icon icon="mdi:close"></ha-icon></div><span>${T("not_cat")}</span></button>
      </div>
      <div class="dlg-foot"><button class="danger-link" data-action="delete-visit" data-id="${v.id}"><ha-icon icon="mdi:delete-outline"></ha-icon>${T("del_visit")}</button></div>`}`,
      { type: "visit", id }
    );
  }

  _openHistory(filter = "all") {
    const d = this._data;
    let vs = [...d.visits].reverse();
    if (filter === "pending") vs = vs.filter((v) => v.status === "pending");
    else if (filter === "not_cat") vs = vs.filter((v) => v.status === "not_cat");
    else if (filter !== "all") vs = vs.filter((v) => v.cat_id === filter);
    const chips = [
      ["all", T("all")],
      ["pending", T("pending_n", { n: d.visits.filter((v) => v.status === "pending").length })],
      ...d.cats.map((c) => [c.id, c.name]),
      ["not_cat", T("not_cat")],
    ]
      .map(([k, l]) => `<button class="chip ${filter === k ? "sel" : ""}" data-action="filter" data-filter="${esc(k)}">${esc(l)}</button>`)
      .join("");
    let lastDay = "";
    const rows = vs
      .slice(0, 300)
      .map((v) => {
        const day = new Date(v.start).toLocaleDateString(KK_LOCALE, { weekday: "long", day: "numeric", month: "long" });
        const head = day !== lastDay ? `<div class="day">${day}</div>` : "";
        lastDay = day;
        return head + this._row(v);
      })
      .join("");
    this._showDialog(
      `${this._dlgHead(T("history"))}<div class="chips">${chips}</div><div class="list">${rows || `<div class="muted center">${T("no_records")}</div>`}</div>`,
      { type: "history", filter }
    );
  }

  _openEditor(id) {
    const cat = id ? this._cat(id) : null;
    const used = new Set(this._data.cats.map((c) => c.color));
    const color = cat?.color || KK_COLORS.find((c) => !used.has(c)) || KK_COLORS[0];
    this._edit = { id, color, photo: undefined, removePhoto: false, preview: cat?.photo || null, name: cat?.name || "" };
    const swatches = KK_COLORS.map(
      (c) => `<button type="button" class="swatch ${c === color ? "sel" : ""}" style="--c:${c}" data-action="pick-color" data-color="${c}" aria-label="${T("color")}"></button>`
    ).join("");
    this._showDialog(
      `${this._dlgHead(cat ? T("edit_cat") : T("new_cat"))}
      <div class="editor">
        <div class="photo-pick"></div>
        <label class="field"><span>${T("name")}</span><input id="kk-name" maxlength="40" value="${esc(cat?.name || "")}" placeholder="${T("name_ph")}" autocomplete="off"></label>
        <label class="field"><span>${T("hint")} <small>${T("hint_sub")}</small></span>
          <input id="kk-hint" type="number" inputmode="decimal" step="0.1" min="0" max="20" value="${cat?.hint ? (cat.hint / 1000).toFixed(1) : ""}" placeholder="${T("hint_ph")}"></label>
        <div class="field"><span>${T("color")}</span><div class="swatches">${swatches}</div></div>
        <div class="dlg-foot">
          ${cat ? `<button class="danger-link" data-action="delete-cat" data-id="${cat.id}"><ha-icon icon="mdi:delete-outline"></ha-icon>${T("delete")}</button>` : "<span></span>"}
          <div class="gap"><button class="ghost" data-action="close">${T("cancel")}</button><button class="primary" data-action="save-cat">${T("save")}</button></div>
        </div>
      </div>`,
      { type: "editor", id }
    );
    this._renderEditorPhoto();
    const name = this._dlg.querySelector("#kk-name");
    name.addEventListener("input", () => {
      const e = this._edit;
      if (e.photo || (!e.removePhoto && e.preview)) return;
      const span = this._dlg.querySelector(".photo-pick .av span");
      if (span) span.textContent = (name.value.trim().charAt(0) || "?").toLocaleUpperCase(KK_LOCALE);
    });
    if (!cat) setTimeout(() => name.focus(), 50);
  }

  _renderEditorPhoto() {
    const box = this._dlg.querySelector(".photo-pick");
    if (!box) return;
    const e = this._edit;
    const src = e.photo || (e.removePhoto ? null : e.preview);
    const letter = (this._dlg.querySelector("#kk-name")?.value || e.name || "?").trim().charAt(0).toLocaleUpperCase(KK_LOCALE) || "?";
    box.innerHTML = `
      <label class="av xl pickable" style="--c:${esc(e.color)}">
        ${src ? `<img src="${esc(src)}" alt="">` : `<span>${esc(letter)}</span>`}
        <div class="cam"><ha-icon icon="mdi:camera"></ha-icon></div>
        <input type="file" accept="image/*" hidden>
      </label>
      <div class="pp-actions"><span class="muted">${T("tap_photo")}</span>${src ? `<button class="link" data-action="remove-photo">${T("remove_photo")}</button>` : ""}</div>`;
    box.querySelector("input").addEventListener("change", async (ev) => {
      const file = ev.target.files?.[0];
      if (!file) return;
      try {
        e.photo = await squarePhoto(file);
        e.removePhoto = false;
        this._renderEditorPhoto();
      } catch (err) {
        this._toast(err.message, true);
      }
    });
  }

  async _saveCat() {
    const e = this._edit;
    const name = this._dlg.querySelector("#kk-name").value.trim();
    const hintRaw = this._dlg.querySelector("#kk-hint").value.replace(",", ".").trim();
    if (!name) {
      this._dlg.querySelector("#kk-name").focus();
      return this._toast(T("name_req"), true);
    }
    const msg = { type: "kedi_kumu/cat/save", name, color: e.color };
    if (e.id) msg.cat_id = e.id;
    if (hintRaw !== "") {
      const h = parseFloat(hintRaw);
      if (!isFinite(h) || h < 0 || h > 20) return this._toast(T("hint_range"), true);
      msg.hint_kg = h;
    } else if (e.id && this._cat(e.id)?.hint) msg.hint_kg = 0;
    if (e.photo) msg.photo = e.photo;
    if (e.removePhoto && !e.photo) msg.remove_photo = true;
    const btn = this._dlg.querySelector('[data-action="save-cat"]');
    btn.disabled = true;
    btn.textContent = T("saving");
    try {
      const saved = await this._ws(msg, T("saved", { name }));
      this._closeDialog();
      await this._load();
      if (!e.id && saved?.id) this._openCat(saved.id);
    } catch (_) {
      btn.disabled = false;
      btn.textContent = T("save");
    }
  }
}

const KK_CSS = `
:host { --kk-r: 16px; --kk-soft: color-mix(in srgb, var(--primary-text-color) 6%, transparent); --kk-line: var(--divider-color, rgba(127,127,127,.2)); }
ha-card { padding: 16px; overflow: hidden; }
button { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; -webkit-tap-highlight-color: transparent; }
button:disabled { opacity: .45; cursor: default; }
.muted { color: var(--secondary-text-color); font-size: .86em; }
.center { text-align: center; padding: 12px 0; }
.loading, .empty { display: flex; gap: 12px; align-items: center; color: var(--secondary-text-color); padding: 8px 4px; }
.head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
.head-r { display: flex; align-items: center; gap: 8px; min-width: 0; }
.add-cat { width: 34px; height: 34px; flex: none; color: var(--secondary-text-color); transition: background .15s, color .15s; }
.add-cat:hover { background: color-mix(in srgb, var(--primary-color) 16%, transparent); color: var(--primary-color); }
.title { display: flex; align-items: center; gap: 10px; font-size: 1.15em; font-weight: 600; }
.title ha-icon { color: var(--primary-color); }
.status { display: flex; align-items: center; gap: 6px; padding: 6px 12px 6px 8px; border-radius: 999px; font-size: .88em; font-weight: 500; background: var(--kk-soft); white-space: nowrap; }
.status ha-icon { --mdc-icon-size: 18px; }
.status small { opacity: .75; font-weight: 400; }
.status.ok { color: #2e9e6a; background: color-mix(in srgb, #2e9e6a 14%, transparent); }
.status.warn { color: #d08a1f; background: color-mix(in srgb, #e9a23b 16%, transparent); }
.status.busy { color: #e2683c; background: color-mix(in srgb, #e2683c 16%, transparent); animation: kkpulse 1.6s ease-in-out infinite; }
.status.info { color: #3a86d4; background: color-mix(in srgb, #3a86d4 15%, transparent); }
.status.info ha-icon { animation: kkspin 1.4s linear infinite; }
@keyframes kkpulse { 50% { box-shadow: 0 0 0 6px color-mix(in srgb, #e2683c 10%, transparent); } }
@keyframes kkspin { to { transform: rotate(360deg); } }
.alerts { display: grid; gap: 8px; margin-bottom: 12px; }
.alert { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 12px; font-size: .9em; }
.alert span { flex: 1; }
.alert.warn { background: color-mix(in srgb, #e9a23b 15%, transparent); }
.alert.warn ha-icon { color: #d08a1f; }
.alert.bad { background: color-mix(in srgb, #e5484d 14%, transparent); }
.alert.bad ha-icon { color: #e5484d; }
.link { color: var(--primary-color); font-weight: 500; font-size: .9em; }
.section { margin-top: 14px; }
.sec-title { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; font-weight: 500; }
.onboard { display: grid; grid-template-columns: auto 1fr; gap: 6px 14px; align-items: center; padding: 16px; border-radius: var(--kk-r); background: var(--kk-soft); }
.ob-icon { width: 48px; height: 48px; border-radius: 14px; display: grid; place-items: center; background: color-mix(in srgb, var(--primary-color) 18%, transparent); color: var(--primary-color); grid-row: span 2; }
.ob-text { display: grid; gap: 4px; font-size: .92em; }
.ob-text span { color: var(--secondary-text-color); }
.onboard .primary { grid-column: 2; justify-self: start; margin-top: 6px; }
.primary { display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: 999px; background: var(--primary-color); color: var(--text-primary-color, #fff); font-weight: 600; }
.primary ha-icon { --mdc-icon-size: 18px; }
.ghost { padding: 9px 14px; border-radius: 999px; background: var(--kk-soft); font-weight: 500; }
.asks { display: grid; gap: 10px; }
.ask { border-radius: var(--kk-r); padding: 12px; background: color-mix(in srgb, var(--primary-color) 9%, transparent); border: 1px solid color-mix(in srgb, var(--primary-color) 22%, transparent); }
.ask-head { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; flex-wrap: wrap; }
.ask-meta .w { font-weight: 700; font-size: 1.05em; }
.ask-reason { font-size: .82em; color: var(--secondary-text-color); margin-top: 2px; }
.more { display: block; margin: 0 auto; }
.picks { display: flex; gap: 8px; margin-top: 10px; overflow-x: auto; scrollbar-width: none; padding-bottom: 2px; }
.picks.wrap { flex-wrap: wrap; }
.pick { display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 64px; padding: 8px 6px; border-radius: 14px; background: var(--card-background-color, #fff); font-size: .8em; font-weight: 500; border: 2px solid transparent; transition: transform .12s, border-color .12s; }
.pick:active { transform: scale(.95); }
.pick.sugg { border-color: color-mix(in srgb, var(--c) 70%, transparent); box-shadow: 0 0 0 3px color-mix(in srgb, var(--c) 18%, transparent); }
.pick.sel, .pick.chosen { border-color: var(--c, var(--secondary-text-color)); background: color-mix(in srgb, var(--c, #888) 14%, var(--card-background-color, #fff)); }
.pick.none { color: var(--secondary-text-color); }
.av { --c: #999; position: relative; width: 40px; height: 40px; flex: none; border-radius: 50%; display: grid; place-items: center; overflow: hidden; background: color-mix(in srgb, var(--c) 30%, var(--card-background-color, #fff)); color: color-mix(in srgb, var(--c) 75%, #000); font-weight: 700; box-shadow: 0 0 0 2px color-mix(in srgb, var(--c) 55%, transparent); }
.av img { width: 100%; height: 100%; object-fit: cover; }
.av.xs { width: 20px; height: 20px; font-size: .7em; box-shadow: none; }
.av.sm { width: 34px; height: 34px; font-size: .9em; }
.av.lg { width: 64px; height: 64px; font-size: 1.5em; box-shadow: 0 0 0 3px color-mix(in srgb, var(--c) 55%, transparent); }
.av.xl { width: 104px; height: 104px; font-size: 2.4em; box-shadow: 0 0 0 4px color-mix(in srgb, var(--c) 60%, transparent); }
.av.unknown { --c: #9e9e9e; color: var(--secondary-text-color); box-shadow: none; background: var(--kk-soft); }
.av.unknown ha-icon { --mdc-icon-size: 18px; }
.cats { display: grid; grid-template-columns: repeat(auto-fill, minmax(118px, 1fr)); gap: 10px; }
.cat { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 14px 8px 12px; border-radius: var(--kk-r); background: linear-gradient(180deg, color-mix(in srgb, var(--c) 14%, transparent), var(--kk-soft)); text-align: center; transition: transform .12s; min-width: 0; }
.cat:active { transform: scale(.97); }
.cat-name { font-weight: 600; margin-top: 4px; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cat-w { font-size: 1.25em; font-weight: 700; display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap; justify-content: center; }
.cat-w small { font-size: .62em; font-weight: 500; color: var(--secondary-text-color); }
.trend { font-size: .55em; font-weight: 600; padding: 1px 6px; border-radius: 999px; background: var(--kk-soft); }
.trend.up { color: #d9822b; } .trend.down { color: #3a86d4; } .trend.flat { color: var(--secondary-text-color); }
.spark { width: 64px; height: 18px; } .spark polyline { fill: none; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.cat-meta { font-size: .78em; color: var(--secondary-text-color); }
.learn { display: flex; align-items: center; gap: 6px; font-size: .74em; color: var(--secondary-text-color); margin-top: 2px; }
.learn.ok { color: #2e9e6a; } .learn ha-icon { --mdc-icon-size: 14px; }
.learn .bar { width: 34px; height: 4px; border-radius: 4px; background: var(--kk-line); overflow: hidden; }
.learn .bar i { display: block; height: 100%; background: var(--c); }
.tl { position: relative; height: 46px; }
.tl-track { position: absolute; left: 0; right: 0; top: 14px; height: 8px; border-radius: 8px; background: var(--kk-soft); }
.tl-now { position: absolute; top: 9px; width: 2px; height: 18px; margin-left: -1px; border-radius: 2px; background: var(--primary-color); opacity: .6; }
.dot { position: absolute; top: 10px; width: 16px; height: 16px; margin-left: -8px; border-radius: 50%; background: var(--c); border: 2px solid var(--card-background-color, #fff); box-shadow: 0 1px 3px rgba(0,0,0,.25); }
.dot.unk { background: repeating-linear-gradient(45deg, #9e9e9e, #9e9e9e 3px, #c4c4c4 3px, #c4c4c4 6px); }
.tl-ticks { position: absolute; left: 0; right: 0; top: 28px; display: flex; justify-content: space-between; font-size: .7em; color: var(--secondary-text-color); }
.recent, .list { display: grid; gap: 2px; }
.row { display: flex; align-items: center; gap: 12px; padding: 8px 6px; border-radius: 12px; text-align: left; width: 100%; }
.row:hover { background: var(--kk-soft); }
.row-main { flex: 1; min-width: 0; }
.row-name { font-weight: 500; display: flex; align-items: center; gap: 6px; }
.row.not_cat .row-name { color: var(--secondary-text-color); }
.row-w { text-align: right; font-weight: 600; white-space: nowrap; }
.row-w small { font-weight: 400; color: var(--secondary-text-color); }
.badge { display: inline-flex; align-items: center; font-size: .68em; font-weight: 600; padding: 1px 6px; border-radius: 999px; background: var(--kk-soft); color: var(--secondary-text-color); }
.badge ha-icon { --mdc-icon-size: 12px; }
.badge.auto { color: #2e9e6a; background: color-mix(in srgb, #2e9e6a 14%, transparent); }
.badge.pending { color: #fff; background: #e9a23b; }
.compact-foot { display: flex; align-items: center; justify-content: space-between; width: 100%; margin-top: 12px; padding: 10px 12px; border-radius: 12px; background: var(--kk-soft); font-size: .88em; text-align: left; }
.compact-foot ha-icon { --mdc-icon-size: 18px; color: var(--secondary-text-color); }
.gauges { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 14px; }
.gauge { display: grid; gap: 6px; padding: 12px; border-radius: 14px; background: var(--kk-soft); text-align: left; width: 100%; box-sizing: border-box; }
.g-top { display: flex; align-items: center; gap: 8px; font-size: .88em; }
.g-top span { flex: 1; } .g-top ha-icon { --mdc-icon-size: 18px; color: var(--secondary-text-color); }
.g-bar { height: 6px; border-radius: 6px; background: var(--kk-line); overflow: hidden; }
.g-bar i { display: block; height: 100%; border-radius: 6px; background: #2e9e6a; }
.g-bar.warn i { background: #e9a23b; } .g-bar.bad i { background: #e5484d; }
.g-foot { display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; }
.g-foot .link { font-size: .8em; }
.info-row { display: flex; flex-wrap: wrap; gap: 6px; width: 100%; margin-top: 12px; text-align: left; }
.chip-i { display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; border-radius: 999px; background: var(--kk-soft); font-size: .8em; color: var(--secondary-text-color); }
.chip-i ha-icon { --mdc-icon-size: 15px; }
.chip-i.warn { color: #d08a1f; background: color-mix(in srgb, #e9a23b 16%, transparent); }
.set-sec { padding: 10px 12px; border-radius: 14px; background: var(--kk-soft); margin-top: 10px; display: grid; gap: 8px; }
.set-row { display: flex; align-items: center; gap: 10px; min-height: 40px; }
.set-row > ha-icon, .set-title ha-icon { --mdc-icon-size: 20px; color: var(--secondary-text-color); }
.set-row .grow, .grow { flex: 1; min-width: 0; }
.set-row b, .set-title b { font-weight: 600; font-size: .95em; }
.set-title { display: flex; align-items: center; gap: 10px; }
.set-row.times { flex-wrap: wrap; font-size: .88em; color: var(--secondary-text-color); }
.set-row.sched { padding: 4px 0; border-top: 1px solid var(--kk-line); }
.set-actions { display: flex; justify-content: flex-end; gap: 8px; }
.set-sec input[type=time], .set-sec .num { font: inherit; padding: 7px 9px; border-radius: 10px; border: 1px solid var(--kk-line); background: var(--card-background-color, #fff); color: var(--primary-text-color); }
.set-sec .num { width: 64px; }
.big { font-size: 1.4em; font-weight: 700; } .big small { font-size: .55em; color: var(--secondary-text-color); } .big.warn { color: #d08a1f; }
.mini { padding: 7px 14px; border-radius: 999px; background: var(--primary-color); color: var(--text-primary-color, #fff); font-weight: 600; font-size: .85em; }
.mini.danger { background: #e5484d; color: #fff; }
.mini.ghost { background: transparent; color: var(--primary-color); border: 1px solid color-mix(in srgb, var(--primary-color) 40%, transparent); }
.icon.sm { width: 32px; height: 32px; } .icon.sm ha-icon { --mdc-icon-size: 18px; }
.pad { padding: 6px 2px; }
.sw { position: relative; display: inline-block; width: 44px; height: 26px; flex: none; }
.sw input { opacity: 0; width: 0; height: 0; position: absolute; }
.sw span { position: absolute; inset: 0; border-radius: 26px; background: var(--kk-line); transition: background .15s; cursor: pointer; }
.sw span::before { content: ""; position: absolute; width: 20px; height: 20px; left: 3px; top: 3px; border-radius: 50%; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.3); transition: transform .15s; }
.sw input:checked + span { background: var(--primary-color); }
.sw input:checked + span::before { transform: translateX(18px); }
.controls { display: flex; gap: 8px; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--kk-line); flex-wrap: wrap; }
.ctl { flex: 1; min-width: 72px; display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 10px 6px; border-radius: 14px; background: var(--kk-soft); font-size: .78em; font-weight: 500; }
.ctl ha-icon { --mdc-icon-size: 22px; color: var(--secondary-text-color); }
.ctl.on { background: color-mix(in srgb, var(--primary-color) 16%, transparent); }
.ctl.on ha-icon { color: var(--primary-color); }
dialog { border: 0; padding: 0; border-radius: 22px; width: min(520px, calc(100vw - 24px)); max-height: min(88vh, 900px); background: var(--card-background-color, #fff); color: var(--primary-text-color); box-shadow: 0 20px 60px rgba(0,0,0,.35); }
dialog::backdrop { background: rgba(0,0,0,.45); backdrop-filter: blur(2px); }
.dlg { padding: 16px 18px 20px; max-height: min(88vh, 900px); overflow-y: auto; box-sizing: border-box; }
.dlg-head { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.dlg-title { flex: 1; font-size: 1.15em; font-weight: 600; }
.icon { width: 38px; height: 38px; border-radius: 50%; display: grid; place-items: center; background: var(--kk-soft); }
.icon ha-icon { --mdc-icon-size: 20px; }
.profile { display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center; margin-bottom: 14px; }
.p-name { font-size: 1.5em; font-weight: 700; }
.p-learn { font-size: .85em; color: var(--secondary-text-color); max-width: 360px; }
.p-learn.ok { color: #2e9e6a; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.stat { padding: 10px; border-radius: 12px; background: var(--kk-soft); }
.sv { font-weight: 700; margin-top: 2px; }
.chart-title { font-weight: 600; margin: 16px 0 6px; }
.chart { width: 100%; height: auto; display: block; }
.chart text { font-size: 11px; fill: var(--secondary-text-color); }
.chart text.strong { fill: var(--primary-text-color); font-weight: 600; }
.chart .grid { stroke: var(--kk-line); stroke-dasharray: 3 4; }
.chart .line { fill: none; stroke: var(--c); stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }
.chart .pt { fill: var(--card-background-color, #fff); stroke: var(--c); stroke-width: 1.6; }
.chart .bar { fill: var(--c); } .chart .bar.zero { fill: var(--kk-line); }
.chart-empty { padding: 18px; text-align: center; border-radius: 12px; background: var(--kk-soft); }
.visit-hero { display: flex; align-items: center; gap: 14px; padding: 12px; border-radius: var(--kk-r); background: var(--kk-soft); }
.visit-hero > div:nth-child(2) { flex: 1; }
.vh-name { font-size: 1.15em; font-weight: 700; }
.vh-status { font-size: .82em; margin-top: 2px; }
.vh-w { font-size: 1.5em; font-weight: 700; } .vh-w small { font-size: .55em; color: var(--secondary-text-color); }
.note { margin-top: 10px; font-size: .85em; padding: 10px 12px; border-radius: 12px; background: color-mix(in srgb, #e9a23b 14%, transparent); }
.dlg-foot { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-top: 18px; }
.gap { display: flex; gap: 8px; }
.danger-link { display: inline-flex; align-items: center; gap: 4px; color: #e5484d; font-weight: 500; font-size: .9em; }
.danger-link ha-icon { --mdc-icon-size: 18px; }
.chips { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }
.chip { padding: 6px 12px; border-radius: 999px; background: var(--kk-soft); font-size: .85em; }
.chip.sel { background: var(--primary-color); color: var(--text-primary-color, #fff); }
.day { font-size: .8em; font-weight: 600; color: var(--secondary-text-color); margin: 10px 6px 2px; text-transform: capitalize; }
.editor { display: grid; gap: 14px; }
.photo-pick { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.pickable { cursor: pointer; overflow: visible; }
.pickable img { border-radius: 50%; }
.cam { position: absolute; right: 4px; bottom: 4px; width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; background: var(--primary-color); color: var(--text-primary-color, #fff); }
.cam ha-icon { --mdc-icon-size: 16px; }
.pp-actions { display: flex; gap: 12px; align-items: center; }
.field { display: grid; gap: 6px; font-size: .9em; font-weight: 500; }
.field small { color: var(--secondary-text-color); font-weight: 400; }
.field input { font: inherit; font-size: 1.05em; padding: 11px 12px; border-radius: 12px; border: 1px solid var(--kk-line); background: var(--secondary-background-color, transparent); color: var(--primary-text-color); outline: none; }
.field input:focus { border-color: var(--primary-color); box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary-color) 18%, transparent); }
.swatches { display: flex; gap: 10px; flex-wrap: wrap; }
.swatch { width: 30px; height: 30px; border-radius: 50%; background: var(--c); border: 3px solid var(--card-background-color, #fff); box-shadow: 0 0 0 1px var(--kk-line); }
.swatch.sel { box-shadow: 0 0 0 2px var(--c); }
.toast { position: fixed; left: 50%; bottom: 24px; transform: translate(-50%, 20px); opacity: 0; pointer-events: none; padding: 10px 16px; border-radius: 999px; background: #2b2b2b; color: #fff; font-size: .9em; transition: all .2s; z-index: 10; }
.toast.show { opacity: 1; transform: translate(-50%, 0); }
.toast.bad { background: #b3261e; }
:host([compact]) .cats { grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr)); gap: 8px; }
:host([compact]) .cat { min-width: 0; }
:host([compact]) .cat-name, :host([compact]) .cat-meta, :host([compact]) .learn { max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
:host([compact]) .learn .bar { width: 22px; flex: none; }
:host([compact]) .cat { padding: 10px 4px 8px; }
:host([compact]) .cat .av.lg { width: 48px; height: 48px; font-size: 1.1em; }
:host([compact]) .cat-w { font-size: 1.05em; }
:host([compact]) .cat-meta, :host([compact]) .learn { font-size: .7em; }
:host([compact]) .spark { display: none; }
@media (max-width: 420px) { .gauges { grid-template-columns: 1fr; } .stats { grid-template-columns: repeat(2, 1fr); } .cats { grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); } }
`;

if (!customElements.get("kedi-kumu-card")) {
  customElements.define("kedi-kumu-card", KediKumuCard);
  window.customCards = window.customCards || [];
  window.customCards.push({
    type: "kedi-kumu-card",
    name: "Kedi Kumu",
    description: "Cat profiles, litter box visits and weight-based cat recognition (English / Türkçe)",
    preview: false,
  });
  console.info(`%c KEDI-KUMU-CARD %c ${KK_VERSION} `, "background:#f4a261;color:#000;border-radius:3px 0 0 3px", "background:#333;color:#fff;border-radius:0 3px 3px 0");
}
