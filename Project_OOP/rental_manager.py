from abc import ABC, abstractmethod
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json


# Abstraction
class Kendaraan(ABC):
    def __init__(self, nopol, merk, harga_harian, is_listrik):
        # Encapsulation
        self.__nopol = nopol
        self.__merk = merk
        self.__harga_harian = harga_harian
        self.__is_listrik = is_listrik

    def get_nopol(self):
        return self.__nopol

    def get_merk(self):
        return self.__merk

    def get_is_listrik(self):
        return self.__is_listrik

    def get_harga_harian(self):
        return self.__harga_harian

    @abstractmethod
    def get_jenis(self):
        pass

    def hitung_total_sewa(self, hari):
        total = self.__harga_harian * hari
        if self.__is_listrik:
            total *= 0.9
        return total


# Inheritance
class Mobil(Kendaraan):
    # Polymorphism
    def get_jenis(self):
        return "Mobil"


# Inheritance
class Motor(Kendaraan):
    # Polymorphism
    def get_jenis(self):
        return "Motor"


class RentalWebApp:
    def __init__(self):
        self.daftar_kendaraan = [
            Mobil("B 1234 ABC", "Toyota Avanza", 300000, False),
            Mobil("B 2024 MPV", "Mitsubishi Xpander", 325000, False),
            Mobil("D 7711 SUV", "Honda CR-V", 550000, False),
            Mobil("N 8818 DLS", "Toyota Fortuner", 700000, False),
            Mobil("AB 1456 HZ", "Suzuki Ertiga", 280000, False),
            Mobil("F 9090 HEV", "Toyota Kijang Innova Zenix Hybrid", 650000, True),
            Mobil("L 9999 EV", "Hyundai Ioniq 5 (Listrik)", 800000, True),
            Mobil("B 7777 TES", "Tesla Model 3", 1200000, True),
            Mobil("DB 1741 KN", "BMW M8", 5000000, True),
            Mobil("DK 4545 BYD", "BYD Dolphin", 680000, True),
            Motor("D 5678 XY", "Honda Vario", 75000, False),
            Motor("B 8899 NMX", "Yamaha NMAX", 120000, False),
            Motor("L 4545 SCO", "Honda Scoopy", 80000, False),
            Motor("W 2121 SPT", "Yamaha Aerox", 110000, False),
            Motor("AE 6767 TRA", "Honda PCX", 135000, False),
            Motor("B 3333 ELF", "Gesits (Listrik)", 100000, True),
            Motor("H 7878 ECO", "Alva One", 145000, True),
            Motor("B 1616 ZMT", "Yadea E8S Pro", 115000, True),
        ]
        self.addons = [
            {
                "id": "insurance",
                "label": "Proteksi perjalanan",
                "description": "Perlindungan ringan untuk risiko kecil selama masa sewa.",
                "price_per_day": 25000,
            },
            {
                "id": "driver",
                "label": "Supir profesional",
                "description": "Tambahan supir harian untuk perjalanan dalam kota.",
                "price_per_day": 150000,
            },
            {
                "id": "priority",
                "label": "Prioritas siap jalan",
                "description": "Unit diprioritaskan untuk pengecekan dan pengantaran awal.",
                "price_per_day": 40000,
            },
        ]

    def format_rupiah(self, nominal):
        return f"Rp {nominal:,.0f}".replace(",", ".")

    def get_vehicle_profile(self, kendaraan):
        merk = kendaraan.get_merk().lower()
        is_mobil = kendaraan.get_jenis() == "Mobil"
        if "tesla" in merk or "bmw" in merk or "ioniq" in merk:
            kelas = "Premium"
            rating = 4.9
        elif "fortuner" in merk or "cr-v" in merk or "zenix" in merk:
            kelas = "Executive"
            rating = 4.8
        elif is_mobil:
            kelas = "Family"
            rating = 4.7
        else:
            kelas = "Urban"
            rating = 4.6

        kapasitas = "5-7 kursi" if is_mobil else "2 orang"
        transmisi = "Otomatis" if is_mobil else "Matic"
        cocok_untuk = "Keluarga dan perjalanan bisnis" if is_mobil else "Mobilitas cepat dalam kota"
        fitur = ["AC", "Bluetooth", "Bagasi lega"] if is_mobil else ["Helm", "Bagasi jok", "Irit harian"]
        if kendaraan.get_is_listrik():
            fitur = ["Eco mode", "Charging ready", "Diskon 10%"]

        return {
            "kelas": kelas,
            "rating": rating,
            "kapasitas": kapasitas,
            "transmisi": transmisi,
            "cocok_untuk": cocok_untuk,
            "fitur": fitur,
        }

    def get_vehicle_art(self, vehicle):
        is_mobil = vehicle["jenis"] == "Mobil"
        if vehicle["is_listrik"]:
            primary = "#2563eb"
            secondary = "#ffffff"
            glow = "rgba(37, 99, 235, 0.18)"
        elif vehicle["kelas"] == "Premium":
            primary = "#f3f4f6"
            secondary = "#9ca3af"
            glow = "rgba(255, 255, 255, 0.25)"
        else:
            primary = "#6b7280"
            secondary = "#d1d5db"
            glow = "rgba(156, 163, 175, 0.25)"

        if is_mobil:
            body_shape = f"""
                <path d="M36 112 C47 82 73 68 112 68 L166 68 C196 68 222 86 235 112 L252 118 C263 122 270 132 270 144 L270 154 L30 154 L30 142 C30 128 31 119 36 112 Z" fill="{primary}"/>
                <path d="M82 78 L116 48 L166 48 L202 78 Z" fill="{secondary}" opacity="0.9"/>
                <path d="M91 75 L119 55 L139 55 L139 75 Z" fill="#0a1728" opacity="0.75"/>
                <path d="M146 55 L166 55 L193 75 L146 75 Z" fill="#0a1728" opacity="0.75"/>
                <circle cx="82" cy="154" r="22" fill="#050505"/>
                <circle cx="82" cy="154" r="10" fill="#f5f5f5"/>
                <circle cx="220" cy="154" r="22" fill="#050505"/>
                <circle cx="220" cy="154" r="10" fill="#f5f5f5"/>
            """
        else:
            body_shape = f"""
                <path d="M74 134 C86 108 111 96 144 103 C160 84 179 75 205 78" fill="none" stroke="{primary}" stroke-width="18" stroke-linecap="round"/>
                <path d="M128 101 L158 72 L184 83 L151 112 Z" fill="{secondary}" opacity="0.9"/>
                <path d="M197 79 L231 68" stroke="{secondary}" stroke-width="10" stroke-linecap="round"/>
                <path d="M226 69 L250 83" stroke="{primary}" stroke-width="8" stroke-linecap="round"/>
                <circle cx="82" cy="150" r="29" fill="#050505"/>
                <circle cx="82" cy="150" r="13" fill="#f5f5f5"/>
                <circle cx="220" cy="150" r="29" fill="#050505"/>
                <circle cx="220" cy="150" r="13" fill="#f5f5f5"/>
            """

        return f"""
            <svg class="vehicle-art" viewBox="0 0 300 190" role="img" aria-label="Gambar {escape(vehicle["merk"])}">
                <defs>
                    <linearGradient id="showroom-bg-{vehicle["id"]}" x1="0" x2="1" y1="0" y2="1">
                        <stop offset="0%" stop-color="#f8fafc"/>
                        <stop offset="100%" stop-color="#e5e7eb"/>
                    </linearGradient>
                </defs>
                <rect width="300" height="190" rx="22" fill="url(#showroom-bg-{vehicle["id"]})"/>
                <ellipse cx="150" cy="157" rx="112" ry="20" fill="{glow}"/>
                {body_shape}
                <path d="M42 176 L258 176" stroke="rgba(17,24,39,0.18)" stroke-width="3" stroke-linecap="round"/>
            </svg>
        """

    def get_vehicle_payload(self):
        payload = []
        for idx, kendaraan in enumerate(self.daftar_kendaraan):
            profile = self.get_vehicle_profile(kendaraan)
            payload.append(
                {
                    "id": idx,
                    "jenis": kendaraan.get_jenis(),
                    "merk": kendaraan.get_merk(),
                    "nopol": kendaraan.get_nopol(),
                    "harga_harian": kendaraan.get_harga_harian(),
                    "harga_harian_label": self.format_rupiah(kendaraan.get_harga_harian()),
                    "is_listrik": kendaraan.get_is_listrik(),
                    "diskon_label": "Diskon 10%" if kendaraan.get_is_listrik() else "Tarif Normal",
                    "mesin_label": "Listrik" if kendaraan.get_is_listrik() else "Bensin",
                    "kelas": profile["kelas"],
                    "rating": profile["rating"],
                    "kapasitas": profile["kapasitas"],
                    "transmisi": profile["transmisi"],
                    "cocok_untuk": profile["cocok_untuk"],
                    "fitur": profile["fitur"],
                }
            )
        return payload

    def get_addon_payload(self):
        return [
            {
                **addon,
                "price_label": self.format_rupiah(addon["price_per_day"]),
            }
            for addon in self.addons
        ]

    def get_selected_addons(self, addon_ids):
        selected = set(addon_ids or [])
        return [addon for addon in self.addons if addon["id"] in selected]

    def calculate_total(self, kendaraan, hari, addon_ids=None):
        base_total = kendaraan.hitung_total_sewa(hari)
        selected_addons = self.get_selected_addons(addon_ids)
        addon_total = sum(addon["price_per_day"] * hari for addon in selected_addons)
        return base_total, selected_addons, addon_total, base_total + addon_total

    def get_filtered_vehicles(self, vehicles, selected_category, selected_energy, search_query):
        normalized_search = search_query.strip().lower()
        return [
            vehicle for vehicle in vehicles
            if (
                (selected_category == "Semua" or vehicle["jenis"] == selected_category)
                and (
                    selected_energy == "Semua"
                    or (selected_energy == "Listrik" and vehicle["is_listrik"])
                    or (selected_energy == "Non-Listrik" and not vehicle["is_listrik"])
                )
                and (not normalized_search or normalized_search in vehicle["merk"].lower())
            )
        ]

    def render_preview_kendaraan(self):
        return """
                    <div class="vehicle-card">
                        <div class="vehicle-head">
                            <div>
                                <p class="eyebrow">Preview Kendaraan</p>
                                <h3 id="vehicle-name"></h3>
                            </div>
                            <span id="vehicle-badge" class="badge"></span>
                        </div>

        <div class="meta">
            <div class="meta-box">
                <span>Jenis</span>
                <strong id="vehicle-type"></strong>
            </div>
                            <div class="meta-box">
                                <span>No. Polisi</span>
                                <strong id="vehicle-nopol"></strong>
                            </div>
                            <div class="meta-box">
                                <span>Harga per Hari</span>
                                <strong id="vehicle-price"></strong>
                            </div>
                            <div class="meta-box">
                <span>Status Tarif</span>
                <strong id="vehicle-discount"></strong>
            </div>
            <div class="meta-box">
                <span>Kapasitas</span>
                <strong id="vehicle-capacity"></strong>
            </div>
            <div class="meta-box">
                <span>Rating</span>
                <strong id="vehicle-rating"></strong>
            </div>
        </div>
        <div class="feature-tags" id="vehicle-features"></div>
    </div>
        """

    def render_rincian_sewa(self, hasil=None, error=None):
        if error:
            return f"""
            <div class="notice error">
                <span class="notice-title">Input belum valid</span>
                <p>{escape(error)}</p>
            </div>
            """

        if not hasil:
            return ""

        badge_class = "eco" if hasil["is_listrik"] else "fuel"
        return f"""
            <div class="result-card">
                <div class="result-head">
                    <div>
                        <p class="eyebrow">Rincian Sewa</p>
                        <h3>{escape(hasil["merk"])}</h3>
                    </div>
                    <span class="badge {badge_class}">{escape(hasil["tipe_mesin"])}</span>
                </div>
                <div class="result-grid">
                    <div><span>Jenis</span><strong>{escape(hasil["jenis"])}</strong></div>
                    <div><span>No. Polisi</span><strong>{escape(hasil["nopol"])}</strong></div>
                    <div><span>Harga / Hari</span><strong>{escape(hasil["harga_harian"])}</strong></div>
                    <div><span>Lama Sewa</span><strong>{escape(str(hasil["lama_sewa"]))} hari</strong></div>
                    <div><span>Subtotal Kendaraan</span><strong>{escape(hasil["subtotal_kendaraan"])}</strong></div>
                    <div><span>Paket Tambahan</span><strong>{escape(hasil["total_addon"])}</strong></div>
                </div>
                <div class="addon-summary">
                    {hasil["addons_html"]}
                </div>
                <div class="total-strip">
                    <span>Total Bayar</span>
                    <strong>{escape(hasil["total_bayar"])}</strong>
                </div>
            </div>
        """

    def proses_sewa(self, kendaraan_idx_raw, hari_raw, addon_ids=None):
        try:
            kendaraan_idx = int(kendaraan_idx_raw)
            hari = int(hari_raw)
            if kendaraan_idx < 0 or kendaraan_idx >= len(self.daftar_kendaraan):
                raise ValueError
            if hari <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return None, "Masukkan kendaraan dan jumlah hari yang valid."

        kendaraan = self.daftar_kendaraan[kendaraan_idx]
        base_total, selected_addons, addon_total, total = self.calculate_total(
            kendaraan, hari, addon_ids
        )
        if selected_addons:
            addons_html = "".join(
                f"""
                <span>
                    {escape(addon["label"])}
                    <strong>{escape(self.format_rupiah(addon["price_per_day"] * hari))}</strong>
                </span>
                """
                for addon in selected_addons
            )
        else:
            addons_html = "<span>Tidak ada paket tambahan <strong>Rp 0</strong></span>"

        return {
            "merk": kendaraan.get_merk(),
            "nopol": kendaraan.get_nopol(),
            "jenis": kendaraan.get_jenis(),
            "tipe_mesin": "Listrik (Diskon 10%)" if kendaraan.get_is_listrik() else "Bensin",
            "lama_sewa": hari,
            "harga_harian": self.format_rupiah(kendaraan.get_harga_harian()),
            "subtotal_kendaraan": self.format_rupiah(base_total),
            "total_addon": self.format_rupiah(addon_total),
            "total_bayar": self.format_rupiah(total),
            "is_listrik": kendaraan.get_is_listrik(),
            "addons_html": addons_html,
        }, None

    def render_page(
        self,
        selected_idx=0,
        hari_value="",
        hasil=None,
        error=None,
        selected_category="Semua",
        selected_energy="Semua",
        search_query="",
        selected_addons=None,
    ):
        vehicles = self.get_vehicle_payload()
        categories = ["Semua", "Mobil", "Motor"]
        energy_filters = ["Semua", "Listrik", "Non-Listrik"]
        try:
            selected_idx = int(selected_idx)
        except (TypeError, ValueError):
            selected_idx = 0
        if selected_category not in categories:
            selected_category = "Semua"
        if selected_energy not in energy_filters:
            selected_energy = "Semua"
        selected_addons = selected_addons or []
        selected_addons = [
            addon_id for addon_id in selected_addons
            if addon_id in {addon["id"] for addon in self.addons}
        ]
        if selected_idx < 0 or selected_idx >= len(vehicles):
            selected_idx = 0

        filtered_vehicles = self.get_filtered_vehicles(
            vehicles, selected_category, selected_energy, search_query
        )

        if filtered_vehicles:
            filtered_ids = {vehicle["id"] for vehicle in filtered_vehicles}
            if selected_idx not in filtered_ids:
                selected_idx = filtered_vehicles[0]["id"]

        options_html = []
        for vehicle in filtered_vehicles:
            selected_attr = " selected" if vehicle["id"] == selected_idx else ""
            label = f'{vehicle["merk"]} | {vehicle["harga_harian_label"]}/hari'
            options_html.append(
                f'<option value="{vehicle["id"]}"{selected_attr}>{escape(label)}</option>'
            )

        category_buttons = []
        for category in categories:
            checked_attr = " checked" if category == selected_category else ""
            category_buttons.append(
                f"""
                <label class="filter-pill">
                    <input type="radio" name="kategori" value="{escape(category)}"{checked_attr}>
                    <span>{escape(category)}</span>
                </label>
                """
            )

        energy_buttons = []
        for energy in energy_filters:
            checked_attr = " checked" if energy == selected_energy else ""
            energy_buttons.append(
                f"""
                <label class="filter-pill">
                    <input type="radio" name="mesin" value="{escape(energy)}"{checked_attr}>
                    <span>{escape(energy)}</span>
                </label>
                """
            )

        jumlah_mobil = sum(1 for vehicle in vehicles if vehicle["jenis"] == "Mobil")
        jumlah_motor = sum(1 for vehicle in vehicles if vehicle["jenis"] == "Motor")
        jumlah_listrik = sum(1 for vehicle in vehicles if vehicle["is_listrik"])
        addon_payload = self.get_addon_payload()
        addon_cards = []
        for addon in addon_payload:
            checked_attr = " checked" if addon["id"] in selected_addons else ""
            addon_cards.append(
                f"""
                <label class="addon-card">
                    <input type="checkbox" name="addons" value="{escape(addon["id"])}"{checked_attr}>
                    <span>
                        <strong>{escape(addon["label"])}</strong>
                        <small>{escape(addon["description"])}</small>
                        <em>{escape(addon["price_label"])}/hari</em>
                    </span>
                </label>
                """
            )
        fleet_cards = []
        for vehicle in vehicles[:8]:
            badge_class = "eco" if vehicle["is_listrik"] else "fuel"
            fleet_cards.append(
                f"""
                <button class="fleet-card" type="button" data-vehicle-id="{vehicle["id"]}">
                    <span class="fleet-top">
                        <strong>{escape(vehicle["merk"])}</strong>
                        <em class="badge {badge_class}">{escape(vehicle["mesin_label"])}</em>
                    </span>
                    <span>{escape(vehicle["kelas"])} - {escape(vehicle["harga_harian_label"])}/hari</span>
                </button>
                """
            )
        result_html = self.render_rincian_sewa(hasil=hasil, error=error)
        preview_html = self.render_preview_kendaraan()

        return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rental Kendaraan OOP</title>
    <style>
        :root {{
            --bg: #f5f5f5;
            --panel: #ffffff;
            --panel-border: #e5e5e5;
            --text: #111111;
            --muted: #666666;
            --accent: #2563eb;
            --accent-2: #1d4ed8;
            --danger: #dc2626;
            --shadow: 0 18px 50px rgba(17, 17, 17, 0.10);
            --radius: 28px;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            min-height: 100vh;
            font-family: "Segoe UI", "Trebuchet MS", sans-serif;
            color: var(--text);
            background: #ffffff;
        }}

        .app-shell {{
            width: min(1500px, calc(100% - 32px));
            margin: 16px auto;
            display: grid;
            grid-template-columns: 340px minmax(0, 1fr);
            gap: 16px;
            align-items: start;
        }}

        .main-area {{
            display: grid;
            gap: 16px;
        }}

        .panel {{
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: 20px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            overflow: hidden;
        }}

        .sidebar {{
            position: sticky;
            top: 16px;
            height: calc(100vh - 32px);
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}

        .brand {{
            display: flex;
            gap: 12px;
            align-items: center;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .brand-mark {{
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: inline-grid;
            place-items: center;
            color: #04101f;
            font-weight: 900;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 14px 28px rgba(0, 194, 168, 0.25);
        }}

        .brand strong {{
            display: block;
            font-size: 1rem;
        }}

        .brand span {{
            color: var(--muted);
            font-size: 0.86rem;
        }}

        .sidebar-cta {{
            padding: 18px;
            border-radius: 18px;
            background: linear-gradient(145deg, rgba(0, 194, 168, 0.15), rgba(255, 184, 77, 0.11));
            border: 1px solid rgba(255, 255, 255, 0.10);
        }}

        .sidebar-cta h2 {{
            font-size: 1.35rem;
            margin-bottom: 10px;
        }}

        .sidebar-cta p:not(.eyebrow) {{
            color: var(--muted);
            line-height: 1.6;
            margin-bottom: 16px;
        }}

        .showroom-link {{
            display: inline-flex;
            justify-content: center;
            width: 100%;
            padding: 13px 16px;
            border-radius: 999px;
            color: #04101f;
            background: linear-gradient(135deg, var(--accent), #8af7c1);
            font-weight: 900;
            text-decoration: none;
            box-shadow: 0 16px 35px rgba(0, 194, 168, 0.26);
        }}

        .sidebar-stats {{
            display: grid;
            gap: 10px;
        }}

        .mini-stat {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            padding: 14px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .mini-stat span {{
            color: var(--muted);
            font-size: 0.86rem;
        }}

        .mini-stat strong {{
            font-size: 1.05rem;
        }}

        .showroom-panel {{
            min-height: 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .showroom-title {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: end;
        }}

        .showroom-title h2 {{
            margin-bottom: 0;
            font-size: 1.1rem;
        }}

        .showroom-count {{
            color: #fff2c9;
            font-weight: 800;
            font-size: 0.88rem;
        }}

        .showroom-list {{
            min-height: 0;
            overflow: auto;
            display: grid;
            gap: 12px;
            padding-right: 4px;
        }}

        .showroom-list::-webkit-scrollbar {{
            width: 8px;
        }}

        .showroom-list::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.14);
            border-radius: 999px;
        }}

        .showroom-card {{
            width: 100%;
            display: grid;
            grid-template-columns: 118px minmax(0, 1fr);
            gap: 12px;
            align-items: center;
            text-align: left;
            padding: 10px;
            border-radius: 16px;
            color: #eff6ff;
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid rgba(255, 255, 255, 0.09);
            box-shadow: none;
        }}

        .showroom-card:hover,
        .showroom-card.active {{
            transform: translateY(-1px);
            border-color: rgba(0, 194, 168, 0.55);
            background: rgba(0, 194, 168, 0.10);
            box-shadow: 0 16px 30px rgba(0, 194, 168, 0.14);
        }}

        .showroom-photo {{
            display: block;
            aspect-ratio: 1.32;
            border-radius: 14px;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.05);
        }}

        .vehicle-art {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        .showroom-info {{
            min-width: 0;
            display: grid;
            gap: 7px;
        }}

        .showroom-info strong {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-size: 0.94rem;
        }}

        .showroom-info > span {{
            color: var(--muted);
            font-size: 0.82rem;
            line-height: 1.35;
        }}

        .hero {{
            padding: 28px;
            position: relative;
            display: grid;
            grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.65fr);
            gap: 24px;
            align-items: center;
        }}

        .hero::after {{
            content: none;
        }}

        .eyebrow {{
            margin: 0 0 10px;
            font-size: 0.85rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--accent);
        }}

        h1, h2, h3, p {{
            margin-top: 0;
        }}

        h1 {{
            font-size: clamp(2rem, 4vw, 3.6rem);
            line-height: 1.05;
            margin-bottom: 18px;
        }}

        .lead {{
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.7;
            max-width: 620px;
        }}

        .highlights {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px;
        }}

        .highlight {{
            padding: 16px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .highlight strong {{
            display: block;
            font-size: 1.2rem;
            margin-bottom: 6px;
        }}

        .highlight span {{
            color: var(--muted);
            font-size: 0.92rem;
        }}

        .form-wrap {{
            padding: 28px;
        }}

        .workspace {{
            display: grid;
            grid-template-columns: minmax(0, 1.03fr) minmax(360px, 0.97fr);
            gap: 22px;
            align-items: start;
        }}

        .controls-column,
        .insight-column {{
            display: grid;
            gap: 20px;
            align-content: start;
        }}

        .control-card {{
            padding: 24px;
            border-radius: 26px;
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        form {{
            display: grid;
            gap: 18px;
        }}

        label {{
            display: block;
            margin-bottom: 8px;
            color: #d8e4f8;
            font-weight: 600;
        }}

        select, input {{
            width: 100%;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(4, 12, 24, 0.92);
            color: var(--text);
            padding: 15px 16px;
            border-radius: 16px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
        }}

        select:focus, input:focus {{
            border-color: rgba(0, 194, 168, 0.8);
            box-shadow: 0 0 0 4px rgba(0, 194, 168, 0.12);
            transform: translateY(-1px);
        }}

        .button-row {{
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .filter-stack {{
            display: grid;
            gap: 18px;
        }}

        .filter-group {{
            display: grid;
            gap: 10px;
        }}

        .filter-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .filter-pill {{
            position: relative;
            display: inline-flex;
        }}

        .filter-pill input {{
            position: absolute;
            opacity: 0;
            pointer-events: none;
        }}

        .filter-pill span {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 12px 18px;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(255, 255, 255, 0.04);
            color: #dfeaff;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
        }}

        .filter-pill span:hover {{
            transform: translateY(-1px);
        }}

        .filter-pill input:checked + span {{
            background: linear-gradient(135deg, rgba(0, 194, 168, 0.22), rgba(138, 247, 193, 0.16));
            border-color: rgba(0, 194, 168, 0.55);
            color: #eafff8;
            box-shadow: 0 12px 28px rgba(0, 194, 168, 0.16);
        }}

        .search-wrap {{
            display: grid;
            gap: 10px;
        }}

        .quick-days {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}

        .day-chip {{
            min-width: 54px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 9px 11px;
            background: rgba(255, 255, 255, 0.045);
            color: #dfeaff;
            font-weight: 800;
            cursor: pointer;
        }}

        .day-chip:hover {{
            border-color: rgba(0, 194, 168, 0.50);
            color: #eafff8;
        }}

        button {{
            border: none;
            border-radius: 999px;
            padding: 15px 24px;
            font-size: 0.98rem;
            font-weight: 700;
            cursor: pointer;
            color: #04101f;
            background: linear-gradient(135deg, var(--accent) 0%, #8af7c1 100%);
            box-shadow: 0 16px 35px rgba(0, 194, 168, 0.32);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 22px 40px rgba(0, 194, 168, 0.38);
        }}

        .ghost-info {{
            color: var(--muted);
            font-size: 0.95rem;
        }}

        .section-title {{
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
        }}

        .section-title h2,
        .section-title h3 {{
            margin-bottom: 0;
        }}

        .addon-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 12px;
        }}

        .addon-card {{
            position: relative;
            display: block;
            margin: 0;
        }}

        .addon-card input {{
            position: absolute;
            opacity: 0;
            pointer-events: none;
        }}

        .addon-card span {{
            min-height: 142px;
            display: grid;
            gap: 8px;
            align-content: start;
            padding: 16px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.10);
            background: rgba(255, 255, 255, 0.04);
            cursor: pointer;
            transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
        }}

        .addon-card input:checked + span {{
            border-color: rgba(0, 194, 168, 0.58);
            background: rgba(0, 194, 168, 0.12);
            box-shadow: 0 16px 28px rgba(0, 194, 168, 0.12);
        }}

        .addon-card span:hover {{
            transform: translateY(-1px);
        }}

        .addon-card small {{
            color: var(--muted);
            line-height: 1.45;
        }}

        .addon-card em {{
            align-self: end;
            color: #fff2c9;
            font-style: normal;
            font-weight: 800;
        }}

        .fleet-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
        }}

        .fleet-card {{
            width: 100%;
            display: grid;
            gap: 10px;
            text-align: left;
            padding: 15px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.10);
            background: rgba(255, 255, 255, 0.04);
            color: #dfeaff;
            box-shadow: none;
        }}

        .fleet-card:hover,
        .fleet-card.active {{
            border-color: rgba(0, 194, 168, 0.48);
            background: rgba(0, 194, 168, 0.10);
            box-shadow: 0 16px 28px rgba(0, 194, 168, 0.12);
        }}

        .fleet-top {{
            display: flex;
            justify-content: space-between;
            gap: 10px;
            align-items: start;
        }}

        .fleet-card > span:last-child {{
            color: var(--muted);
            font-size: 0.9rem;
        }}

        .vehicle-card {{
            padding: 22px;
            border-radius: 24px;
            background:
                linear-gradient(145deg, rgba(0, 194, 168, 0.10), rgba(255, 184, 77, 0.08)),
                rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .landscape-note {{
            padding: 20px 22px;
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .landscape-note p:last-child {{
            margin-bottom: 0;
        }}

        .vehicle-head {{
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: start;
        }}

        .vehicle-head h3 {{
            margin-bottom: 6px;
            font-size: 1.45rem;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 14px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 700;
            white-space: nowrap;
        }}

        .badge.eco {{
            background: rgba(0, 194, 168, 0.14);
            color: #8af7c1;
        }}

        .badge.fuel {{
            background: rgba(255, 184, 77, 0.14);
            color: #ffd18a;
        }}

        .meta {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            margin-top: 18px;
        }}

        .meta-box {{
            padding: 14px 16px;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.04);
        }}

        .meta-box span {{
            display: block;
            color: var(--muted);
            font-size: 0.82rem;
            margin-bottom: 8px;
        }}

        .meta-box strong {{
            font-size: 1rem;
        }}

        .feature-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 16px;
        }}

        .feature-tags span {{
            padding: 8px 10px;
            border-radius: 999px;
            color: #dfeaff;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 0.85rem;
            font-weight: 700;
        }}

        .live-estimate {{
            padding: 20px;
            border-radius: 18px;
            background: linear-gradient(145deg, rgba(255, 184, 77, 0.12), rgba(0, 194, 168, 0.10));
            border: 1px solid rgba(255, 255, 255, 0.09);
        }}

        .estimate-line {{
            display: flex;
            justify-content: space-between;
            gap: 16px;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--muted);
        }}

        .estimate-line strong {{
            color: #eff6ff;
        }}

        .estimate-total {{
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: end;
            padding-top: 14px;
        }}

        .estimate-total strong {{
            font-size: 1.5rem;
            color: #8af7c1;
        }}

        .notice {{
            margin-top: 20px;
            padding: 18px 20px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .notice.error {{
            background: rgba(255, 107, 107, 0.12);
            border-color: rgba(255, 107, 107, 0.28);
        }}

        .notice-title {{
            display: block;
            margin-bottom: 8px;
            font-weight: 700;
        }}

        .result-card {{
            margin-top: 20px;
            padding: 22px;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .result-head {{
            display: flex;
            justify-content: space-between;
            gap: 14px;
            align-items: start;
            margin-bottom: 18px;
        }}

        .result-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
        }}

        .result-grid div {{
            padding: 14px 16px;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.04);
        }}

        .result-grid span {{
            display: block;
            color: var(--muted);
            font-size: 0.82rem;
            margin-bottom: 8px;
        }}

        .total-strip {{
            margin-top: 18px;
            padding: 18px 20px;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(0, 194, 168, 0.22), rgba(255, 184, 77, 0.16));
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }}

        .total-strip span {{
            color: #dbfff9;
        }}

        .total-strip strong {{
            font-size: 1.4rem;
        }}

        .addon-summary {{
            display: grid;
            gap: 8px;
            margin-top: 14px;
        }}

        .addon-summary span {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 14px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.04);
            color: var(--muted);
        }}

        .addon-summary strong {{
            color: #eff6ff;
        }}

        body .panel,
        body .control-card,
        body .vehicle-card,
        body .result-card,
        body .landscape-note,
        body .live-estimate,
        body .highlight,
        body .mini-stat,
        body .addon-card span,
        body .fleet-card {{
            background: #ffffff;
            border-color: #e5e5e5;
            box-shadow: 0 12px 34px rgba(17, 17, 17, 0.08);
        }}

        body .sidebar-cta {{
            background: #ffffff;
            border-color: #e5e5e5;
        }}

        body .brand {{
            border-bottom-color: #e5e5e5;
        }}

        body .brand-mark,
        body button,
        body .showroom-link {{
            color: #ffffff;
            background: #2563eb;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.18);
        }}

        body button:hover,
        body .showroom-link:hover {{
            box-shadow: 0 16px 32px rgba(37, 99, 235, 0.22);
        }}

        body .eyebrow {{
            color: #2563eb;
        }}

        body .lead,
        body .ghost-info,
        body .highlight span,
        body .brand span,
        body .mini-stat span,
        body .meta-box span,
        body .result-grid span,
        body .estimate-line,
        body .addon-card small,
        body .fleet-card > span:last-child,
        body .sidebar-cta p:not(.eyebrow) {{
            color: #666666;
        }}

        body label,
        body .fleet-card,
        body .filter-pill span {{
            color: #111111;
        }}

        body select,
        body input {{
            background: #ffffff;
            color: #111111;
            border-color: #d8d8d8;
        }}

        body select:focus,
        body input:focus {{
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.10);
        }}

        body .filter-pill span,
        body .meta-box,
        body .result-grid div,
        body .addon-summary span,
        body .estimate-line,
        body .feature-tags span {{
            background: #f7f7f7;
            border-color: #e5e5e5;
            color: #111111;
        }}

        body .filter-pill input:checked + span,
        body .fleet-card:hover,
        body .fleet-card.active,
        body .addon-card input:checked + span {{
            background: #eff6ff;
            border-color: #2563eb;
            color: #111111;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.12);
        }}

        body .badge.eco,
        body .badge.fuel {{
            background: #111111;
            color: #ffffff;
        }}

        body .total-strip,
        body .live-estimate {{
            background: #ffffff;
            border: 1px solid #e5e5e5;
        }}

        body .total-strip span,
        body .estimate-total strong,
        body .addon-summary strong {{
            color: #111111;
        }}

        body .total-strip strong {{
            color: #2563eb;
        }}

        body {{
            background: #ffffff;
            color: #111111;
        }}

        body .panel,
        body .control-card,
        body .vehicle-card,
        body .result-card,
        body .landscape-note,
        body .live-estimate,
        body .highlight,
        body .mini-stat,
        body .sidebar-cta,
        body .addon-card span,
        body .fleet-card,
        body .showroom-card {{
            background: #ffffff;
            border-color: #e5e7eb;
            box-shadow: 0 12px 30px rgba(17, 24, 39, 0.07);
        }}

        body .brand {{
            border-bottom-color: #e5e7eb;
        }}

        body .brand-mark,
        body button,
        body .showroom-link {{
            background: #2563eb;
            color: #ffffff;
            box-shadow: 0 12px 26px rgba(37, 99, 235, 0.22);
        }}

        body button:hover,
        body .showroom-link:hover {{
            box-shadow: 0 16px 32px rgba(37, 99, 235, 0.24);
        }}

        body .eyebrow,
        body .total-strip strong {{
            color: #2563eb;
        }}

        body h1,
        body h2,
        body h3,
        body strong,
        body label,
        body .fleet-card,
        body .showroom-card,
        body .filter-pill span {{
            color: #111111;
        }}

        body .lead,
        body .ghost-info,
        body .highlight span,
        body .brand span,
        body .mini-stat span,
        body .meta-box span,
        body .result-grid span,
        body .estimate-line,
        body .addon-card small,
        body .fleet-card > span:last-child,
        body .showroom-info > span,
        body .sidebar-cta p:not(.eyebrow) {{
            color: #666666;
        }}

        body select,
        body input {{
            background: #ffffff;
            color: #111111;
            border-color: #d1d5db;
        }}

        body select:focus,
        body input:focus {{
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
        }}

        body .filter-pill span,
        body .day-chip,
        body .meta-box,
        body .result-grid div,
        body .addon-summary span,
        body .estimate-line,
        body .feature-tags span {{
            background: #f8fafc;
            border-color: #e5e7eb;
            color: #111111;
        }}

        body .filter-pill input:checked + span,
        body .fleet-card:hover,
        body .fleet-card.active,
        body .showroom-card:hover,
        body .showroom-card.active,
        body .day-chip:hover,
        body .addon-card input:checked + span {{
            background: #eff6ff;
            border-color: #2563eb;
            color: #111111;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.14);
        }}

        body .badge.eco,
        body .badge.fuel {{
            background: #eff6ff;
            color: #1d4ed8;
        }}

        body .total-strip,
        body .live-estimate {{
            background: #ffffff;
            border-color: #e5e7eb;
        }}

        body .total-strip span,
        body .estimate-total strong,
        body .addon-summary strong {{
            color: #111111;
        }}

        body .showroom-count,
        body .addon-card em {{
            color: #2563eb;
        }}

        @media (max-width: 1260px) {{
            .app-shell {{
                grid-template-columns: 1fr;
            }}

            .sidebar {{
                position: static;
                height: auto;
                min-height: auto;
            }}

            .showroom-list {{
                max-height: 460px;
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            .hero {{
                grid-template-columns: 1fr;
            }}

            .workspace {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 640px) {{
            .hero, .form-wrap {{
                padding: 24px;
            }}

            .highlights,
            .meta,
            .result-grid,
            .fleet-grid {{
                grid-template-columns: 1fr;
            }}

            .control-card {{
                padding: 20px;
            }}

            .vehicle-head,
            .result-head,
            .total-strip {{
                flex-direction: column;
                align-items: start;
            }}

            .showroom-list {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="app-shell">
        <aside class="panel sidebar">
            <div class="brand">
                <span class="brand-mark">RK</span>
                <div>
                    <strong>RentalKita</strong>
                    <span>Fleet booking dashboard</span>
                </div>
            </div>

            <div class="sidebar-cta">
                <p class="eyebrow">Showroom</p>
                <h2>Galeri kendaraan terpisah</h2>
                <p>Lihat foto-foto kendaraan dalam tampilan carousel sebelum memilih unit untuk disewa.</p>
                <a class="showroom-link" href="/showroom">Buka Showroom</a>
            </div>

            <div class="sidebar-stats">
                <div class="mini-stat"><span>Total unit</span><strong>{len(vehicles)}</strong></div>
                <div class="mini-stat"><span>Mobil</span><strong>{jumlah_mobil}</strong></div>
                <div class="mini-stat"><span>Motor</span><strong>{jumlah_motor}</strong></div>
                <div class="mini-stat"><span>Unit listrik</span><strong>{jumlah_listrik}</strong></div>
            </div>
        </aside>

        <main class="main-area">
            <section class="panel hero" id="dashboard">
                <div>
                    <p class="eyebrow">Rental Dashboard</p>
                    <h1>Sistem Rental Kendaraan berbasis Web</h1>
                    <p class="lead">
                        Dashboard pemesanan dengan filter armada, estimasi biaya langsung, paket tambahan,
                        dan rincian pembayaran yang tetap memakai konsep OOP Python.
                    </p>
                </div>

                <div class="highlights">
                    <div class="highlight">
                        <strong>{len(vehicles)} Unit</strong>
                        <span>Mobil dan motor siap disewa.</span>
                    </div>
                    <div class="highlight">
                        <strong>{jumlah_mobil} Mobil</strong>
                        <span>Family, executive, dan premium.</span>
                    </div>
                    <div class="highlight">
                        <strong>{jumlah_motor} Motor</strong>
                        <span>Skuter harian dan listrik.</span>
                    </div>
                    <div class="highlight">
                        <strong>{jumlah_listrik} EV</strong>
                        <span>Diskon otomatis 10%.</span>
                    </div>
                </div>
            </section>

            <section class="panel form-wrap" id="booking">
                <div class="section-title">
                    <div>
                        <p class="eyebrow">Booking Studio</p>
                        <h2>Atur sewa kendaraan</h2>
                    </div>
                    <span class="ghost-info">Preview dan estimasi akan berubah saat pilihan diubah.</span>
                </div>

                <div class="workspace">
                    <div class="controls-column">
                        <div class="control-card">
                            <form method="post" action="/hitung" id="booking-form">
                                <div class="filter-stack">
                                    <div class="filter-group">
                                        <label>Pilih Kategori</label>
                                        <div class="filter-pills">
                                            {"".join(category_buttons)}
                                        </div>
                                    </div>

                                    <div class="filter-group">
                                        <label>Filter Mesin</label>
                                        <div class="filter-pills">
                                            {"".join(energy_buttons)}
                                        </div>
                                    </div>

                                    <div class="search-wrap">
                                        <label for="search">Cari Nama Kendaraan</label>
                                        <input id="search" name="search" type="text" placeholder="Contoh: avanza, nmax, tesla" value="{escape(search_query)}">
                                    </div>
                                </div>

                                <div>
                                    <label for="kendaraan">Pilih Kendaraan</label>
                                    <select id="kendaraan" name="kendaraan">
                                        {"".join(options_html)}
                                    </select>
                                </div>

                                <div>
                                    <label for="hari">Durasi Sewa (hari)</label>
                                    <input id="hari" name="hari" type="number" min="1" placeholder="Contoh: 3" value="{escape(str(hari_value))}">
                                    <div class="quick-days" aria-label="Pilihan durasi cepat">
                                        <button class="day-chip" type="button" data-days="1">1H</button>
                                        <button class="day-chip" type="button" data-days="3">3H</button>
                                        <button class="day-chip" type="button" data-days="7">7H</button>
                                        <button class="day-chip" type="button" data-days="14">14H</button>
                                    </div>
                                </div>

                                <div>
                                    <label>Paket Tambahan</label>
                                    <div class="addon-grid">
                                        {"".join(addon_cards)}
                                    </div>
                                </div>

                                <div class="button-row">
                                    <button type="submit">Hitung Total Sewa</button>
                                </div>
                            </form>
                        </div>

                        {result_html}
                    </div>

                    <div class="insight-column">
                        {preview_html}

                        <div class="live-estimate" id="estimate">
                            <div class="section-title">
                                <div>
                                    <p class="eyebrow">Estimasi Live</p>
                                    <h3>Ringkasan cepat</h3>
                                </div>
                            </div>
                            <div class="estimate-line">
                                <span>Subtotal kendaraan</span>
                                <strong id="estimate-base">Rp 0</strong>
                            </div>
                            <div class="estimate-line">
                                <span>Paket tambahan</span>
                                <strong id="estimate-addons">Rp 0</strong>
                            </div>
                            <div class="estimate-total">
                                <span>Total perkiraan</span>
                                <strong id="estimate-total">Rp 0</strong>
                            </div>
                        </div>

                        <div class="control-card" id="fleet">
                            <div class="section-title">
                                <div>
                                    <p class="eyebrow">Armada Populer</p>
                                    <h3>Pilih cepat</h3>
                                </div>
                            </div>
                            <div class="fleet-grid">
                                {"".join(fleet_cards)}
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script>
        const vehicles = {json.dumps(vehicles)};
        const addons = {json.dumps(addon_payload)};
        const initialCategory = {json.dumps(selected_category)};
        const initialEnergy = {json.dumps(selected_energy)};

        const vehicleSelect = document.getElementById("kendaraan");
        const dayInput = document.getElementById("hari");
        const searchInput = document.getElementById("search");
        const categoryInputs = Array.from(document.querySelectorAll('input[name="kategori"]'));
        const energyInputs = Array.from(document.querySelectorAll('input[name="mesin"]'));
        const addonInputs = Array.from(document.querySelectorAll('input[name="addons"]'));
        const fleetCards = Array.from(document.querySelectorAll(".fleet-card"));
        const dayChips = Array.from(document.querySelectorAll(".day-chip"));
        const nameEl = document.getElementById("vehicle-name");
        const badgeEl = document.getElementById("vehicle-badge");
        const typeEl = document.getElementById("vehicle-type");
        const nopolEl = document.getElementById("vehicle-nopol");
        const priceEl = document.getElementById("vehicle-price");
        const discountEl = document.getElementById("vehicle-discount");
        const capacityEl = document.getElementById("vehicle-capacity");
        const ratingEl = document.getElementById("vehicle-rating");
        const featuresEl = document.getElementById("vehicle-features");
        const estimateBaseEl = document.getElementById("estimate-base");
        const estimateAddonsEl = document.getElementById("estimate-addons");
        const estimateTotalEl = document.getElementById("estimate-total");
        const rupiah = new Intl.NumberFormat("id-ID", {{
            style: "currency",
            currency: "IDR",
            maximumFractionDigits: 0,
        }});

        function getSelectedCategory() {{
            const active = categoryInputs.find((input) => input.checked);
            return active ? active.value : "Semua";
        }}

        function getSelectedEnergy() {{
            const active = energyInputs.find((input) => input.checked);
            return active ? active.value : "Semua";
        }}

        function getFilteredVehicles() {{
            const category = getSelectedCategory();
            const energy = getSelectedEnergy();
            const keyword = (searchInput.value || "").trim().toLowerCase();

            return vehicles.filter((vehicle) => {{
                const categoryOk = category === "Semua" || vehicle.jenis === category;
                const energyOk =
                    energy === "Semua"
                    || (energy === "Listrik" && vehicle.is_listrik)
                    || (energy === "Non-Listrik" && !vehicle.is_listrik);
                const searchOk = !keyword || vehicle.merk.toLowerCase().includes(keyword);
                return categoryOk && energyOk && searchOk;
            }});
        }}

        function rebuildVehicleOptions(preferredId) {{
            const filtered = getFilteredVehicles();
            const currentPreferred = Number(preferredId);
            vehicleSelect.innerHTML = "";

            filtered.forEach((vehicle, idx) => {{
                const option = document.createElement("option");
                option.value = String(vehicle.id);
                option.textContent = `${{vehicle.merk}} | ${{vehicle.harga_harian_label}}/hari`;
                if (vehicle.id === currentPreferred || (Number.isNaN(currentPreferred) && idx === 0)) {{
                    option.selected = true;
                }}
                vehicleSelect.appendChild(option);
            }});

            if (!filtered.length) {{
                const option = document.createElement("option");
                option.value = "";
                option.textContent = "Tidak ada kendaraan yang cocok";
                option.disabled = true;
                option.selected = true;
                vehicleSelect.appendChild(option);
            }}

            if (vehicleSelect.options.length && vehicleSelect.selectedIndex === -1) {{
                vehicleSelect.selectedIndex = 0;
            }}
        }}

        function clearVehiclePreview() {{
            nameEl.textContent = "Tidak ada kendaraan";
            typeEl.textContent = "-";
            nopolEl.textContent = "-";
            priceEl.textContent = "-";
            discountEl.textContent = "-";
            capacityEl.textContent = "-";
            ratingEl.textContent = "-";
            featuresEl.innerHTML = "";
            badgeEl.textContent = "Kosong";
            badgeEl.className = "badge fuel";
            estimateBaseEl.textContent = "Rp 0";
            estimateAddonsEl.textContent = "Rp 0";
            estimateTotalEl.textContent = "Rp 0";
        }}

        function renderVehiclePreview(vehicle) {{
            nameEl.textContent = vehicle.merk;
            typeEl.textContent = vehicle.jenis;
            nopolEl.textContent = vehicle.nopol;
            priceEl.textContent = vehicle.harga_harian_label + "/hari";
            discountEl.textContent = vehicle.diskon_label;
            capacityEl.textContent = vehicle.kapasitas;
            ratingEl.textContent = vehicle.rating.toFixed(1) + " / 5";
            featuresEl.innerHTML = "";
            vehicle.fitur.forEach((feature) => {{
                const tag = document.createElement("span");
                tag.textContent = feature;
                featuresEl.appendChild(tag);
            }});
            badgeEl.textContent = vehicle.is_listrik ? "Listrik" : "Bensin";
            badgeEl.className = "badge " + (vehicle.is_listrik ? "eco" : "fuel");
        }}

        function getSelectedAddonTotal(days) {{
            return addonInputs
                .filter((input) => input.checked)
                .reduce((total, input) => {{
                    const addon = addons.find((item) => item.id === input.value);
                    return total + (addon ? addon.price_per_day * days : 0);
                }}, 0);
        }}

        function updateEstimate(vehicle) {{
            const days = Math.max(Number(dayInput.value || 0), 0);
            if (!vehicle || days <= 0) {{
                estimateBaseEl.textContent = "Rp 0";
                estimateAddonsEl.textContent = "Rp 0";
                estimateTotalEl.textContent = "Rp 0";
                return;
            }}

            const base = vehicle.harga_harian * days * (vehicle.is_listrik ? 0.9 : 1);
            const addonTotal = getSelectedAddonTotal(days);
            estimateBaseEl.textContent = rupiah.format(base);
            estimateAddonsEl.textContent = rupiah.format(addonTotal);
            estimateTotalEl.textContent = rupiah.format(base + addonTotal);
        }}

        function markActiveFleet(vehicleId) {{
            fleetCards.forEach((card) => {{
                card.classList.toggle("active", Number(card.dataset.vehicleId) === vehicleId);
            }});
        }}

        function chooseVehicleFromCard(vehicleId) {{
            categoryInputs.forEach((input) => {{
                input.checked = input.value === "Semua";
            }});
            energyInputs.forEach((input) => {{
                input.checked = input.value === "Semua";
            }});
            searchInput.value = "";
            rebuildVehicleOptions(vehicleId);
            vehicleSelect.value = vehicleId;
            updatePreview();
            document.getElementById("booking").scrollIntoView({{ behavior: "smooth", block: "start" }});
        }}

        function updatePreview() {{
            const selectedValue = vehicleSelect.value;
            const selectedId = selectedValue === "" ? null : Number(selectedValue);
            const vehicle = vehicles.find((item) => item.id === selectedId);

            if (!vehicle) {{
                clearVehiclePreview();
                return;
            }}

            renderVehiclePreview(vehicle);
            updateEstimate(vehicle);
            markActiveFleet(selectedId);
        }}

        categoryInputs.forEach((input) => {{
            input.addEventListener("change", () => {{
                rebuildVehicleOptions(vehicleSelect.value);
                updatePreview();
            }});
        }});

        energyInputs.forEach((input) => {{
            input.addEventListener("change", () => {{
                rebuildVehicleOptions(vehicleSelect.value);
                updatePreview();
            }});
        }});

        searchInput.addEventListener("input", () => {{
            rebuildVehicleOptions(vehicleSelect.value);
            updatePreview();
        }});

        addonInputs.forEach((input) => {{
            input.addEventListener("change", updatePreview);
        }});

        dayInput.addEventListener("input", updatePreview);

        dayChips.forEach((chip) => {{
            chip.addEventListener("click", () => {{
                dayInput.value = chip.dataset.days;
                updatePreview();
            }});
        }});

        fleetCards.forEach((card) => {{
            card.addEventListener("click", () => {{
                chooseVehicleFromCard(card.dataset.vehicleId);
            }});
        }});

        vehicleSelect.addEventListener("change", updatePreview);
        categoryInputs.forEach((input) => {{
            input.checked = input.value === initialCategory;
        }});
        energyInputs.forEach((input) => {{
            input.checked = input.value === initialEnergy;
        }});
        rebuildVehicleOptions({json.dumps(selected_idx)});
        updatePreview();
    </script>
</body>
</html>"""

    def render_showroom_page(self):
        vehicles = self.get_vehicle_payload()
        gallery_cards = []
        for vehicle in vehicles:
            badge_class = "eco" if vehicle["is_listrik"] else "fuel"
            gallery_cards.append(
                f"""
                <article class="gallery-card" data-vehicle-id="{vehicle["id"]}">
                    <div class="photo-frame">
                        {self.get_vehicle_art(vehicle)}
                    </div>
                    <div class="gallery-info">
                        <span class="badge {badge_class}">{escape(vehicle["mesin_label"])}</span>
                        <h2>{escape(vehicle["merk"])}</h2>
                        <p>{escape(vehicle["kelas"])} - {escape(vehicle["kapasitas"])} - {escape(vehicle["transmisi"])}</p>
                        <div class="gallery-meta">
                            <span>{escape(vehicle["harga_harian_label"])}/hari</span>
                            <span>Rating {vehicle["rating"]:.1f}/5</span>
                        </div>
                        <button class="select-link" type="button" data-vehicle-id="{vehicle["id"]}">Pilih kendaraan ini</button>
                    </div>
                </article>
                """
            )

        return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Showroom Kendaraan</title>
    <style>
        :root {{
            --bg: #ffffff;
            --panel: #ffffff;
            --panel-border: #e5e7eb;
            --text: #111111;
            --muted: #666666;
            --accent: #2563eb;
            --accent-2: #1d4ed8;
            --shadow: 0 12px 30px rgba(17, 24, 39, 0.08);
        }}

        * {{
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            margin: 0;
            min-height: 100vh;
            font-family: "Segoe UI", "Trebuchet MS", sans-serif;
            color: var(--text);
            background: #ffffff;
        }}

        a {{
            color: inherit;
        }}

        .showroom-shell {{
            min-height: 100vh;
            display: grid;
            grid-template-rows: auto minmax(0, 1fr);
            gap: 18px;
            width: min(1480px, calc(100% - 32px));
            margin: 0 auto;
            padding: 18px 0 26px;
        }}

        .showroom-top {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            gap: 18px;
            align-items: center;
            padding: 22px;
            border-radius: 22px;
            background: var(--panel);
            border: 1px solid var(--panel-border);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
        }}

        .eyebrow {{
            margin: 0 0 8px;
            font-size: 0.82rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--accent);
        }}

        h1, h2, p {{
            margin-top: 0;
        }}

        h1 {{
            margin-bottom: 10px;
            font-size: clamp(2rem, 4vw, 4rem);
            line-height: 1;
        }}

        .showroom-top p:not(.eyebrow) {{
            max-width: 720px;
            margin-bottom: 0;
            color: var(--muted);
            line-height: 1.65;
        }}

        .top-actions {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: end;
        }}

        .nav-link,
        .select-link {{
            border: 0;
            border-radius: 999px;
            font-weight: 900;
            cursor: pointer;
            text-decoration: none;
        }}

        .nav-link {{
            display: inline-flex;
            padding: 13px 18px;
            background: #ffffff;
            border: 1px solid #d1d5db;
            color: #111111;
        }}

        .nav-link.primary {{
            color: #ffffff;
            background: #2563eb;
            box-shadow: 0 12px 26px rgba(37, 99, 235, 0.22);
        }}

        .showroom-stage {{
            min-height: 0;
            display: grid;
            grid-template-columns: minmax(0, 1fr);
            gap: 14px;
            align-items: center;
        }}

        .gallery-track {{
            min-height: 620px;
            display: grid;
            grid-auto-flow: column;
            grid-auto-columns: minmax(320px, 420px);
            gap: 24px;
            align-items: center;
            overflow-x: auto;
            padding: 38px max(24px, calc((100vw - 520px) / 2));
            scroll-snap-type: x proximity;
            scrollbar-width: none;
        }}

        .gallery-track::-webkit-scrollbar {{
            display: none;
        }}

        .gallery-card {{
            scroll-snap-align: center;
            min-height: 540px;
            display: grid;
            grid-template-rows: minmax(240px, 1fr) auto;
            overflow: hidden;
            border-radius: 28px;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            box-shadow: 0 12px 30px rgba(17, 24, 39, 0.08);
            transform: rotate(-3deg) scale(0.92);
            opacity: 0.72;
            transition: transform 0.35s ease, opacity 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
        }}

        .gallery-card.is-active {{
            transform: rotate(0deg) scale(1);
            opacity: 1;
            border-color: #2563eb;
            box-shadow: 0 16px 36px rgba(37, 99, 235, 0.16);
        }}

        .gallery-card.is-right {{
            transform: rotate(3deg) scale(0.92);
        }}

        .photo-frame {{
            min-height: 260px;
            display: grid;
            place-items: center;
            padding: 0;
            overflow: hidden;
            background: #f8fafc;
        }}

        .vehicle-art {{
            width: 100%;
            height: 100%;
            display: block;
            transition: transform 0.35s ease;
        }}

        .gallery-card.is-active .vehicle-art {{
            transform: scale(1.04);
        }}

        .gallery-info {{
            display: grid;
            gap: 12px;
            padding: 22px;
        }}

        .gallery-info h2 {{
            margin-bottom: 0;
            font-size: 1.45rem;
            line-height: 1.12;
        }}

        .gallery-info p {{
            margin-bottom: 0;
            color: var(--muted);
            line-height: 1.5;
        }}

        .gallery-meta {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
        }}

        .gallery-meta span {{
            padding: 12px;
            border-radius: 14px;
            background: #f8fafc;
            color: #111111;
            font-weight: 800;
            font-size: 0.92rem;
        }}

        .badge {{
            width: fit-content;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 9px 12px;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 900;
        }}

        .badge.eco {{
            background: #eff6ff;
            color: #1d4ed8;
        }}

        .badge.fuel {{
            background: #eff6ff;
            color: #1d4ed8;
        }}

        .select-link {{
            display: inline-flex;
            justify-content: center;
            padding: 14px 16px;
            color: #ffffff;
            background: #2563eb;
            box-shadow: 0 12px 26px rgba(37, 99, 235, 0.22);
            font-size: 0.98rem;
        }}

        .modal-backdrop {{
            position: fixed;
            inset: 0;
            z-index: 20;
            display: none;
            place-items: center;
            padding: 22px;
            background: rgba(17, 24, 39, 0.35);
            backdrop-filter: blur(12px);
        }}

        .modal-backdrop.is-open {{
            display: grid;
        }}

        .vehicle-modal {{
            width: min(760px, 100%);
            max-height: min(86vh, 760px);
            overflow: auto;
            border-radius: 26px;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            box-shadow: 0 24px 70px rgba(17, 24, 39, 0.24);
        }}

        .modal-hero {{
            display: grid;
            grid-template-columns: minmax(240px, 0.9fr) minmax(0, 1.1fr);
            gap: 18px;
            align-items: center;
            padding: 20px;
            background: #f8fafc;
        }}

        .modal-hero .vehicle-art {{
            min-height: 260px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
        }}

        .modal-copy {{
            min-width: 0;
            display: grid;
            gap: 12px;
        }}

        .modal-copy h2 {{
            margin-bottom: 0;
            font-size: clamp(1.55rem, 4vw, 2.35rem);
            line-height: 1.05;
        }}

        .modal-copy p {{
            margin-bottom: 0;
            color: var(--muted);
            line-height: 1.55;
        }}

        .modal-body {{
            display: grid;
            gap: 16px;
            padding: 20px;
        }}

        .modal-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
        }}

        .modal-grid div {{
            padding: 14px;
            border-radius: 16px;
            background: #f8fafc;
            border: 1px solid #e5e7eb;
        }}

        .modal-grid span {{
            display: block;
            margin-bottom: 7px;
            color: var(--muted);
            font-size: 0.82rem;
        }}

        .modal-grid strong {{
            color: #111111;
        }}

        .modal-features {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .modal-features span {{
            padding: 9px 11px;
            border-radius: 999px;
            color: #111111;
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            font-size: 0.86rem;
            font-weight: 800;
        }}

        .modal-actions {{
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .modal-close,
        .modal-book {{
            display: inline-flex;
            justify-content: center;
            border: 0;
            border-radius: 999px;
            padding: 13px 17px;
            font-weight: 900;
            cursor: pointer;
            text-decoration: none;
        }}

        .modal-close {{
            color: #111111;
            background: #ffffff;
            border: 1px solid #d1d5db;
        }}

        .modal-book {{
            color: #ffffff;
            background: #2563eb;
            box-shadow: 0 12px 26px rgba(37, 99, 235, 0.22);
        }}

        @media (max-width: 900px) {{
            .showroom-top {{
                grid-template-columns: 1fr;
            }}

            .top-actions {{
                justify-content: start;
            }}

            .showroom-stage {{
                grid-template-columns: 1fr;
            }}

            .gallery-track {{
                min-height: auto;
                grid-auto-columns: minmax(280px, 84vw);
                padding: 20px 4px 28px;
            }}

            .modal-hero {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 560px) {{
            .showroom-shell {{
                width: min(100% - 20px, 1480px);
            }}

            .showroom-top {{
                padding: 18px;
            }}

            .gallery-card {{
                min-height: 500px;
            }}

            .gallery-meta {{
                grid-template-columns: 1fr;
            }}

            .modal-grid {{
                grid-template-columns: 1fr;
            }}

            .modal-actions {{
                justify-content: stretch;
            }}

            .modal-close,
            .modal-book {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <main class="showroom-shell">
        <header class="showroom-top">
            <div>
                <p class="eyebrow">Showroom Kendaraan</p>
                <h1>Galeri unit rental</h1>
                <p>Lihat kendaraan satu per satu seperti display showroom. Geser ke kiri atau kanan, lalu pilih unit yang ingin dipakai untuk booking.</p>
            </div>
            <div class="top-actions">
                <a class="nav-link" href="/">Kembali ke Dashboard</a>
                <a class="nav-link primary" href="/#booking">Ke Form Booking</a>
            </div>
        </header>

        <section class="showroom-stage" aria-label="Carousel showroom kendaraan">
            <div class="gallery-track" id="gallery-track">
                {"".join(gallery_cards)}
            </div>
        </section>
    </main>

    <div class="modal-backdrop" id="vehicle-modal" aria-hidden="true">
        <section class="vehicle-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
            <div class="modal-hero">
                <div id="modal-art"></div>
                <div class="modal-copy">
                    <span class="badge" id="modal-badge"></span>
                    <h2 id="modal-title"></h2>
                    <p id="modal-description"></p>
                </div>
            </div>
            <div class="modal-body">
                <div class="modal-grid">
                    <div><span>Harga per Hari</span><strong id="modal-price"></strong></div>
                    <div><span>No. Polisi</span><strong id="modal-nopol"></strong></div>
                    <div><span>Kapasitas</span><strong id="modal-capacity"></strong></div>
                    <div><span>Rating</span><strong id="modal-rating"></strong></div>
                </div>
                <div class="modal-features" id="modal-features"></div>
                <div class="modal-actions">
                    <button class="modal-close" type="button" id="modal-close">Tutup</button>
                    <a class="modal-book" id="modal-book" href="/#booking">Lanjut Booking</a>
                </div>
            </div>
        </section>
    </div>

    <script>
        const vehicles = {json.dumps(vehicles)};
        const track = document.getElementById("gallery-track");
        const modal = document.getElementById("vehicle-modal");
        const modalArt = document.getElementById("modal-art");
        const modalBadge = document.getElementById("modal-badge");
        const modalTitle = document.getElementById("modal-title");
        const modalDescription = document.getElementById("modal-description");
        const modalPrice = document.getElementById("modal-price");
        const modalNopol = document.getElementById("modal-nopol");
        const modalCapacity = document.getElementById("modal-capacity");
        const modalRating = document.getElementById("modal-rating");
        const modalFeatures = document.getElementById("modal-features");
        const modalBook = document.getElementById("modal-book");
        const modalClose = document.getElementById("modal-close");
        const originalCards = Array.from(document.querySelectorAll(".gallery-card"));
        originalCards.forEach((card) => {{
            const clone = card.cloneNode(true);
            track.appendChild(clone);
        }});

        const cards = Array.from(document.querySelectorAll(".gallery-card"));
        const originalCardCount = originalCards.length;
        let activeIndex = 0;
        let loopWidth = 0;
        let isPaused = false;
        let resumeTimer = null;
        const autoSpeed = 1.15;

        function calculateLoopWidth() {{
            if (cards.length <= originalCardCount) {{
                loopWidth = track.scrollWidth;
                return;
            }}
            loopWidth = cards[originalCardCount].offsetLeft - cards[0].offsetLeft;
        }}

        function normalizeIndex(index) {{
            return (index + originalCardCount) % originalCardCount;
        }}

        function paintCards() {{
            cards.forEach((card, index) => {{
                const displayIndex = index % originalCardCount;
                card.classList.toggle("is-active", displayIndex === activeIndex);
                card.classList.toggle("is-right", displayIndex > activeIndex);
            }});
        }}

        function pauseBriefly(duration = 2400) {{
            isPaused = true;
            window.clearTimeout(resumeTimer);
            resumeTimer = window.setTimeout(() => {{
                isPaused = false;
            }}, duration);
        }}

        function normalizeScrollPosition() {{
            if (!loopWidth) {{
                return;
            }}
            if (track.scrollLeft >= loopWidth) {{
                track.scrollLeft -= loopWidth;
            }}
            if (track.scrollLeft < 0) {{
                track.scrollLeft += loopWidth;
            }}
        }}

        function getNearestVisibleCard(targetIndex) {{
            const center = track.scrollLeft + track.clientWidth / 2;
            let nearestCard = cards[targetIndex];
            let nearestDistance = Infinity;
            cards.forEach((card, index) => {{
                if (index % originalCardCount !== targetIndex) {{
                    return;
                }}
                const cardCenter = card.offsetLeft + card.clientWidth / 2;
                const distance = Math.abs(center - cardCenter);
                if (distance < nearestDistance) {{
                    nearestDistance = distance;
                    nearestCard = card;
                }}
            }});
            return nearestCard;
        }}

        function goToCard(index, shouldPause = true) {{
            activeIndex = normalizeIndex(index);
            paintCards();
            if (shouldPause) {{
                pauseBriefly();
            }}
            getNearestVisibleCard(activeIndex).scrollIntoView({{
                behavior: "smooth",
                inline: "center",
                block: "nearest",
            }});
        }}

        function openVehicleModal(vehicleId) {{
            const vehicle = vehicles.find((item) => item.id === Number(vehicleId));
            if (!vehicle) {{
                return;
            }}

            const sourceCard = originalCards.find((card) => Number(card.dataset.vehicleId) === vehicle.id);
            const sourceArt = sourceCard ? sourceCard.querySelector(".vehicle-art") : null;
            modalArt.innerHTML = sourceArt ? sourceArt.outerHTML : "";
            modalBadge.textContent = vehicle.mesin_label;
            modalBadge.className = "badge " + (vehicle.is_listrik ? "eco" : "fuel");
            modalTitle.textContent = vehicle.merk;
            modalDescription.textContent = vehicle.cocok_untuk + " dengan kelas " + vehicle.kelas + ".";
            modalPrice.textContent = vehicle.harga_harian_label + "/hari";
            modalNopol.textContent = vehicle.nopol;
            modalCapacity.textContent = vehicle.kapasitas + " - " + vehicle.transmisi;
            modalRating.textContent = vehicle.rating.toFixed(1) + " / 5";
            modalFeatures.innerHTML = "";
            vehicle.fitur.forEach((feature) => {{
                const tag = document.createElement("span");
                tag.textContent = feature;
                modalFeatures.appendChild(tag);
            }});
            modalBook.href = "/?kendaraan=" + vehicle.id + "#booking";
            modal.classList.add("is-open");
            modal.setAttribute("aria-hidden", "false");
            isPaused = true;
            window.clearTimeout(resumeTimer);
        }}

        function closeVehicleModal() {{
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");
            pauseBriefly(900);
        }}

        cards.forEach((card, index) => {{
            card.addEventListener("click", (event) => {{
                const selectButton = event.target.closest(".select-link");
                if (selectButton) {{
                    openVehicleModal(selectButton.dataset.vehicleId);
                    return;
                }}
                if (event.target.closest("a, button")) {{
                    return;
                }}
                goToCard(index % originalCardCount);
            }});
        }});

        modalClose.addEventListener("click", closeVehicleModal);
        modal.addEventListener("click", (event) => {{
            if (event.target === modal) {{
                closeVehicleModal();
            }}
        }});

        track.addEventListener("mouseenter", () => {{
            isPaused = true;
            window.clearTimeout(resumeTimer);
        }});

        track.addEventListener("mouseleave", () => {{
            isPaused = false;
        }});

        track.addEventListener("focusin", () => {{
            isPaused = true;
            window.clearTimeout(resumeTimer);
        }});

        track.addEventListener("focusout", () => {{
            isPaused = false;
        }});

        track.addEventListener("wheel", (event) => {{
            if (Math.abs(event.deltaY) > Math.abs(event.deltaX)) {{
                event.preventDefault();
                track.scrollLeft += event.deltaY * 2.8;
                normalizeScrollPosition();
                pauseBriefly(850);
            }}
        }}, {{ passive: false }});

        track.addEventListener("scroll", () => {{
            normalizeScrollPosition();
            const center = track.scrollLeft + track.clientWidth / 2;
            let nearestIndex = activeIndex;
            let nearestDistance = Infinity;
            cards.forEach((card, index) => {{
                const cardCenter = card.offsetLeft + card.clientWidth / 2;
                const distance = Math.abs(center - cardCenter);
                if (distance < nearestDistance) {{
                    nearestDistance = distance;
                    nearestIndex = index % originalCardCount;
                }}
            }});
            if (nearestIndex !== activeIndex) {{
                activeIndex = nearestIndex;
                paintCards();
            }}
        }}, {{ passive: true }});

        document.addEventListener("keydown", (event) => {{
            if (event.key === "Escape" && modal.classList.contains("is-open")) {{
                closeVehicleModal();
                return;
            }}
            if (event.key === "ArrowLeft") {{
                goToCard(activeIndex - 1);
            }}
            if (event.key === "ArrowRight") {{
                goToCard(activeIndex + 1);
            }}
        }});

        function animateLoop() {{
            if (!isPaused && !document.hidden) {{
                track.scrollLeft += autoSpeed;
                normalizeScrollPosition();
            }}
            window.requestAnimationFrame(animateLoop);
        }}

        window.addEventListener("resize", () => {{
            calculateLoopWidth();
            normalizeScrollPosition();
        }});

        calculateLoopWidth();
        paintCards();
        animateLoop();
    </script>
</body>
</html>"""

    def make_handler(self):
        app = self

        class RentalRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed_url = urlparse(self.path)
                if parsed_url.path == "/showroom":
                    page = app.render_showroom_page()
                    self._send_html(page)
                    return

                if parsed_url.path not in ("/", "/index.html"):
                    self.send_error(404, "Halaman tidak ditemukan.")
                    return

                query_data = parse_qs(parsed_url.query)
                selected_idx = query_data.get("kendaraan", ["0"])[0]
                page = app.render_page(selected_idx=selected_idx)
                self._send_html(page)

            def do_POST(self):
                if self.path != "/hitung":
                    self.send_error(404, "Endpoint tidak ditemukan.")
                    return

                content_length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(content_length).decode("utf-8")
                form_data = parse_qs(body)
                kendaraan_idx = form_data.get("kendaraan", ["0"])[0]
                hari = form_data.get("hari", [""])[0]
                kategori = form_data.get("kategori", ["Semua"])[0]
                mesin = form_data.get("mesin", ["Semua"])[0]
                search = form_data.get("search", [""])[0]
                addons = form_data.get("addons", [])
                hasil, error = app.proses_sewa(kendaraan_idx, hari, addons)
                page = app.render_page(
                    selected_idx=kendaraan_idx,
                    hari_value=hari,
                    hasil=hasil,
                    error=error,
                    selected_category=kategori,
                    selected_energy=mesin,
                    search_query=search,
                    selected_addons=addons,
                )
                self._send_html(page)

            def _send_html(self, page):
                encoded = page.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, format, *args):
                return

        return RentalRequestHandler

    def run(self, host="127.0.0.1", port=8000):
        server = HTTPServer((host, port), self.make_handler())
        print(f"Rental web app berjalan di http://{host}:{port}")
        print("Tekan Ctrl+C untuk menghentikan server.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
            print("\nServer dihentikan.")


if __name__ == "__main__":
    RentalWebApp().run()
