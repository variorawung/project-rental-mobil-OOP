from abc import ABC, abstractmethod
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json


class Kendaraan(ABC):
    def __init__(self, nopol, merk, harga_harian, is_listrik):
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


class Mobil(Kendaraan):
    def get_jenis(self):
        return "Mobil"


class Motor(Kendaraan):
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

    def format_rupiah(self, nominal):
        return f"Rp {nominal:,.0f}".replace(",", ".")

    def get_vehicle_payload(self):
        payload = []
        for idx, kendaraan in enumerate(self.daftar_kendaraan):
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
                }
            )
        return payload

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
                        </div>
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
                </div>
                <div class="total-strip">
                    <span>Total Bayar</span>
                    <strong>{escape(hasil["total_bayar"])}</strong>
                </div>
            </div>
        """

    def proses_sewa(self, kendaraan_idx_raw, hari_raw):
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
        total = kendaraan.hitung_total_sewa(hari)
        return {
            "merk": kendaraan.get_merk(),
            "nopol": kendaraan.get_nopol(),
            "jenis": kendaraan.get_jenis(),
            "tipe_mesin": "Listrik (Diskon 10%)" if kendaraan.get_is_listrik() else "Bensin",
            "lama_sewa": hari,
            "harga_harian": self.format_rupiah(kendaraan.get_harga_harian()),
            "total_bayar": self.format_rupiah(total),
            "is_listrik": kendaraan.get_is_listrik(),
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
            --bg: #07111f;
            --panel: rgba(9, 20, 36, 0.72);
            --panel-border: rgba(255, 255, 255, 0.12);
            --text: #eff6ff;
            --muted: #96a7c2;
            --accent: #00c2a8;
            --accent-2: #ffb84d;
            --danger: #ff6b6b;
            --shadow: 0 30px 80px rgba(0, 0, 0, 0.35);
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
            background:
                radial-gradient(circle at top left, rgba(0, 194, 168, 0.18), transparent 30%),
                radial-gradient(circle at right, rgba(255, 184, 77, 0.18), transparent 25%),
                linear-gradient(145deg, #030816 0%, #07111f 45%, #10213c 100%);
        }}

        .shell {{
            width: min(1460px, calc(100% - 40px));
            margin: 24px auto;
            display: grid;
            grid-template-columns: minmax(320px, 0.76fr) minmax(760px, 1.24fr);
            gap: 24px;
            align-items: stretch;
        }}

        .panel {{
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            overflow: hidden;
            height: 100%;
        }}

        .hero {{
            padding: 36px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: calc(100vh - 48px);
        }}

        .hero::after {{
            content: "";
            position: absolute;
            inset: auto -60px -90px auto;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255, 184, 77, 0.25), transparent 65%);
            pointer-events: none;
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
            margin-top: 28px;
        }}

        .highlight {{
            padding: 18px;
            border-radius: 22px;
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
            grid-template-columns: minmax(0, 1.1fr) minmax(350px, 0.9fr);
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

        @media (max-width: 1260px) {{
            .shell {{
                grid-template-columns: 1fr;
            }}

            .hero {{
                min-height: auto;
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
            .result-grid {{
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
        }}
    </style>
</head>
<body>
    <main class="shell">
        <section class="panel hero">
            <p class="eyebrow">Rental Dashboard</p>
            <h1>Sistem Rental Kendaraan berbasis Web</h1>
            <p class="lead">
                Aplikasi ini mempertahankan konsep OOP Python sambil memindahkan antarmuka dari desktop ke browser.
                Pilih kendaraan, tentukan durasi, lalu lihat estimasi harga dan total pembayaran dengan tampilan yang lebih modern.
            </p>

            <div class="highlights">
                <div class="highlight">
                    <strong>{len(vehicles)} Unit</strong>
                    <span>Siap dipilih langsung dari dashboard.</span>
                </div>
                <div class="highlight">
                    <strong>{jumlah_mobil} Mobil</strong>
                    <span>Mulai dari city car sampai EV premium.</span>
                </div>
                <div class="highlight">
                    <strong>{jumlah_motor} Motor</strong>
                    <span>Skuter harian, premium, dan motor listrik.</span>
                </div>
                <div class="highlight">
                    <strong>{jumlah_listrik} EV</strong>
                    <span>Bisa difilter khusus kendaraan listrik.</span>
                </div>
            </div>
        </section>

        <section class="panel form-wrap">
            <div class="workspace">
                <div class="controls-column">
                    <div class="control-card">
                        <form method="post" action="/hitung">
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
                            </div>

                            <div class="button-row">
                                <button type="submit">Hitung Total Sewa</button>
                                <span class="ghost-info">Kategori, pencarian, dan status mesin langsung memfilter daftar kendaraan.</span>
                            </div>
                        </form>
                    </div>

                    {result_html}
                </div>

                <div class="insight-column">
                    {preview_html}

                    <div class="landscape-note">
                        <p class="eyebrow">Layout Landscape</p>
                        <p class="ghost-info">
                            Panel kiri menampilkan ringkasan sistem, sedangkan sisi kanan difokuskan untuk filter, preview,
                            dan hasil perhitungan agar lebih nyaman dipakai di layar lebar.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        const vehicles = {json.dumps(vehicles)};
        const initialCategory = {json.dumps(selected_category)};
        const initialEnergy = {json.dumps(selected_energy)};

        const vehicleSelect = document.getElementById("kendaraan");
        const dayInput = document.getElementById("hari");
        const searchInput = document.getElementById("search");
        const categoryInputs = Array.from(document.querySelectorAll('input[name="kategori"]'));
        const energyInputs = Array.from(document.querySelectorAll('input[name="mesin"]'));
        const nameEl = document.getElementById("vehicle-name");
        const badgeEl = document.getElementById("vehicle-badge");
        const typeEl = document.getElementById("vehicle-type");
        const nopolEl = document.getElementById("vehicle-nopol");
        const priceEl = document.getElementById("vehicle-price");
        const discountEl = document.getElementById("vehicle-discount");

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
            badgeEl.textContent = "Kosong";
            badgeEl.className = "badge fuel";
        }}

        function renderVehiclePreview(vehicle) {{
            nameEl.textContent = vehicle.merk;
            typeEl.textContent = vehicle.jenis;
            nopolEl.textContent = vehicle.nopol;
            priceEl.textContent = vehicle.harga_harian_label + "/hari";
            discountEl.textContent = vehicle.diskon_label;
            badgeEl.textContent = vehicle.is_listrik ? "Listrik" : "Bensin";
            badgeEl.className = "badge " + (vehicle.is_listrik ? "eco" : "fuel");
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

    def make_handler(self):
        app = self

        class RentalRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path not in ("/", "/index.html"):
                    self.send_error(404, "Halaman tidak ditemukan.")
                    return
                page = app.render_page()
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
                hasil, error = app.proses_sewa(kendaraan_idx, hari)
                page = app.render_page(
                    selected_idx=kendaraan_idx,
                    hari_value=hari,
                    hasil=hasil,
                    error=error,
                    selected_category=kategori,
                    selected_energy=mesin,
                    search_query=search,
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
