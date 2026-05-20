"""Script to generate a premium PDF User Guide for the FX & IHSG Dashboard."""
import sys
from fpdf import FPDF

class PDFGuide(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # No header on the first page (Cover Page)
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(156, 163, 175) # #9ca3af (gray)
            self.cell(0, 10, 'Panduan Penggunaan & Interpretasi Nilai Dashboard FX & IHSG', 0, 0, 'L')
            self.cell(0, 10, f'Halaman {self.page_no()}', 0, 1, 'R')
            self.ln(1)
            # Thin gray line separator
            self.set_draw_color(229, 231, 235) # #e5e7eb
            self.set_line_width(0.2)
            self.line(15, 23, 195, 23)
            self.ln(4)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(156, 163, 175)
            self.cell(0, 10, 'Mata Kuliah: Visualisasi Data - Universitas Airlangga', 0, 0, 'L')
            self.cell(0, 10, 'Mei 2026 - Versi 1.1 (Final)', 0, 1, 'R')

    # Helper methods for structured layouts
    def cover_page(self):
        self.add_page()
        # Top banner background
        self.set_fill_color(30, 27, 75) # Indigo #1e1b4b
        self.rect(0, 0, 210, 85, 'F')
        
        # Bottom accent strip
        self.set_fill_color(79, 70, 229) # Purple #4f46e5
        self.rect(0, 85, 210, 4, 'F')
        
        # Header inside banner
        self.set_y(25)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(199, 210, 254) # Light indigo #c7d2fe
        self.cell(0, 6, 'DOKUMEN PANDUAN PENGGUNAAN & ANALISIS DATA', 0, 1, 'C')
        
        self.ln(4)
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, 'DASHBOARD NILAI TUKAR RUPIAH', 0, 1, 'C')
        self.cell(0, 12, '& IHSG SEKTORAL', 0, 1, 'C')
        
        # Subtitle
        self.ln(12)
        self.set_y(105)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(30, 27, 75)
        self.cell(0, 8, 'Panduan Membaca, Mengeksplorasi, dan Menafsirkan', 0, 1, 'L')
        self.cell(0, 8, 'Indikator Keuangan Makro Indonesia', 0, 1, 'L')
        
        # Decorative separator line
        self.ln(4)
        self.set_draw_color(79, 70, 229)
        self.set_line_width(1)
        self.line(15, self.get_y(), 100, self.get_y())
        
        # Context description
        self.ln(8)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(75, 85, 99) # Gray #4b5563
        desc = (
            "Dashboard ini merupakan aplikasi analisis interaktif yang dirancang untuk memantau "
            "dan menganalisis pergerakan nilai tukar mata uang asing (Foreign Exchange) terhadap Rupiah (IDR) "
            "serta performa Indeks Harga Saham Gabungan (IHSG) sektoral. Panduan ini disusun untuk membantu "
            "pengguna memahami fungsi-fungsi kontrol, alur data, serta makna ekonomis di balik setiap visualisasi."
        )
        self.multi_cell(180, 5.5, desc)
        
        # Meta info at the bottom
        self.set_y(220)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(30, 27, 75)
        self.cell(0, 6, 'INFORMASI DOKUMEN:', 0, 1, 'L')
        
        # Draw a table-like meta info
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(55, 65, 81)
        
        # Row 1
        self.cell(40, 6, 'Mata Kuliah', 0, 0, 'L')
        self.set_font('Helvetica', 'B', 9.5)
        self.cell(140, 6, ': Visualisasi Data (Visdat)', 0, 1, 'L')
        
        # Row 2
        self.set_font('Helvetica', '', 9.5)
        self.cell(40, 6, 'Semester / Kelas', 0, 0, 'L')
        self.set_font('Helvetica', 'B', 9.5)
        self.cell(140, 6, ': 4 (Empat)', 0, 1, 'L')
        
        # Row 3
        self.set_font('Helvetica', '', 9.5)
        self.cell(40, 6, 'Target Resolusi Layar', 0, 0, 'L')
        self.set_font('Helvetica', 'B', 9.5)
        self.cell(140, 6, ': 1280 x 585 piksel (Bebas Scroll / Fit Satu Layar)', 0, 1, 'L')
        
        # Row 4
        self.set_font('Helvetica', '', 9.5)
        self.cell(40, 6, 'Teknologi Dashboard', 0, 0, 'L')
        self.set_font('Helvetica', 'B', 9.5)
        self.cell(140, 6, ': Streamlit (Python), Plotly, Pandas, Openpyxl', 0, 1, 'L')
        
        # Row 5
        self.set_font('Helvetica', '', 9.5)
        self.cell(40, 6, 'Tanggal Pembaruan', 0, 0, 'L')
        self.set_font('Helvetica', 'B', 9.5)
        self.cell(140, 6, ': 20 Mei 2026', 0, 1, 'L')
        
        # Decorative page border
        self.set_draw_color(229, 231, 235)
        self.set_line_width(0.5)
        self.rect(5, 5, 200, 287)

    def print_section_header(self, num, title):
        self.ln(6)
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(30, 27, 75) # Indigo
        # Solid prefix background
        self.cell(8, 7, f"{num}", 0, 0, 'C', fill=False)
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 7, f" {title}", 0, 1, 'L')
        self.set_draw_color(79, 70, 229)
        self.set_line_width(0.6)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)

    def print_subsection_header(self, title):
        self.set_font('Helvetica', 'B', 10.5)
        self.set_text_color(79, 70, 229) # Purple
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(1)

    def print_paragraph(self, text):
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(55, 65, 81) # Dark gray #374151
        self.multi_cell(180, 5, text)
        self.ln(2.5)
        
    def print_bullet(self, title, desc):
        self.set_font('Helvetica', 'B', 9.5)
        self.set_text_color(30, 27, 75)
        self.cell(6, 5, '-', 0, 0, 'C') # Bullet character
        self.cell(50, 5, title, 0, 0, 'L')
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(55, 65, 81)
        self.cell(2, 5, ':', 0, 0, 'C')
        self.multi_cell(122, 5, desc)
        self.ln(1.5)

    def print_callout(self, text, style='info'):
        colors = {
            'info': (243, 244, 246, 79, 70, 229), # bg: gray, border: purple
            'warning': (254, 242, 242, 239, 68, 68), # bg: light red, border: red
            'success': (240, 253, 250, 16, 185, 129), # bg: light green, border: green
        }
        bg_r, bg_g, bg_b, border_r, border_g, border_b = colors.get(style, colors['info'])
        
        # Set colors for content
        self.set_fill_color(bg_r, bg_g, bg_b)
        self.set_draw_color(border_r, border_g, border_b)
        self.set_line_width(0.5)
        
        # Calculate cell lines to draw background properly
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(31, 41, 55)
        
        self.multi_cell(180, 4.5, text, border='L', fill=True)
        self.ln(3)

def generate_guide():
    pdf = PDFGuide()
    
    # 1. Cover Page
    pdf.cover_page()
    
    # 2. Page 2: Pendahuluan & Struktur
    pdf.add_page()
    pdf.print_section_header(1, "Pendahuluan & Tujuan Dashboard")
    pdf.print_paragraph(
        "Keterkaitan antara pergerakan nilai tukar mata uang asing (khususnya USD/IDR) dengan pasar modal "
        "(IHSG Composite) merupakan indikator makroekonomi yang sangat krusial bagi investor, analis pasar, "
        "maupun pengambil kebijakan. Secara teori ekonomi, depresiasi nilai tukar Rupiah terhadap Dolar AS sering kali "
        "menjadi sinyal terjadinya capital outflow (aliran modal keluar) dari pasar modal domestik, yang "
        "pada akhirnya menekan pergerakan IHSG. Sebaliknya, penguatan Rupiah biasanya didorong oleh sentimen "
        "investasi asing masuk (capital inflow) yang mendorong IHSG ke zona hijau."
    )
    pdf.print_paragraph(
        "Dashboard ini dirancang untuk memvisualisasikan hubungan dinamis tersebut secara interaktif, real-time, "
        "dan komprehensif. Melalui dashboard ini, pengguna dapat mengamati performa nilai tukar secara bersamaan "
        "dengan performa sektoral saham di bawah IHSG, mendeteksi korelasi historis, mengukur risiko volatilitas, "
        "serta melihat respons masing-masing sektor industri terhadap fluktuasi nilai tukar Rupiah."
    )
    
    pdf.print_subsection_header("Struktur Data Dashboard")
    pdf.print_bullet("Data Kurs (FX)", "Mengandung data historis nilai tukar harian Rupiah (IDR) terhadap mata uang asing utama, meliputi USD (Dolar AS), EUR (Euro), GBP (Poundsterling Inggris), HKD (Dolar Hong Kong), CNH (Yuan Tiongkok Luar Negeri), CAD (Dolar Kanada), dan JPY (Yen Jepang).")
    pdf.print_bullet("Data IHSG Sektoral", "Mengandung data harian indeks sektoral di Bursa Efek Indonesia (BEI) berdasarkan klasifikasi industri baru (IDX-IC), termasuk Sektor Keuangan (Finance), Infrastruktur (Infra), Energi (Energy), Material Dasar (Basic Materials), Kesehatan (Healthcare), Properti (Property), Teknologi (Technology), Industri (Industrial), Transportasi & Logistik (Trans), Konsumer Siklikal (Cyclical), Konsumer Non-Siklikal (Non-Cyclical), serta IHSG Composite itu sendiri.")

    pdf.print_callout(
        "PENTING: Seluruh komponen dashboard ini telah dioptimalkan secara tata letak (visual layout) untuk resolusi "
        "layar 1280x585 piksel. Semua visualisasi, KPI, dan tabel dapat termuat penuh dalam 1 halaman web tanpa "
        "perlu melakukan vertical scrolling (gulir ke bawah), sehingga sangat ideal untuk presentasi satu layar.",
        style='success'
    )

    # 3. Page 3: Tab 1 - Overview
    pdf.add_page()
    pdf.print_section_header(2, "Panduan Eksplorasi: Tab 1 - Overview")
    pdf.print_paragraph(
        "Tab pertama ('Overview') menyajikan rangkuman cepat (executive summary) mengenai kondisi makro dan "
        "kinerja instrumen keuangan dalam periode tahun berjalan (Year-to-Date / YTD) serta tren jangka panjang."
    )
    
    pdf.print_subsection_header("A. Ringkasan Kartu KPI (Key Performance Indicator)")
    pdf.print_paragraph(
        "Tepat di bawah judul dashboard, terdapat baris berisi 5 kartu KPI berlatar gradien yang memberikan gambaran ringkas:"
    )
    pdf.print_bullet("IHSG Return (YTD)", "Mengukur persentase performa Indeks Harga Saham Gabungan sejak awal tahun kalender terbaru hingga hari ini. Menunjukkan apakah pasar saham domestik sedang bullish (positif) atau bearish (negatif) sepanjang tahun berjalan.")
    pdf.print_bullet("Sektor Terbaik (YTD)", "Menampilkan nama sektor saham yang mencatatkan pertumbuhan tertinggi di BEI sepanjang tahun, beserta persentase kenaikannya. Berguna untuk mengidentifikasi sektor industri yang memimpin pertumbuhan pasar.")
    pdf.print_bullet("Sektor Terburuk (YTD)", "Menampilkan nama sektor dengan kinerja paling negatif sepanjang tahun berjalan. Membantu analis mendeteksi sektor yang mengalami tekanan atau siklus penurunan industri.")
    pdf.print_bullet("USD/IDR Max (YTD)", "Menampilkan nilai nominal kurs Rupiah tertinggi terhadap Dolar AS pada tahun berjalan. Nilai ini menggambarkan titik terlemah Rupiah (puncak pelemahan Rupiah).")
    pdf.print_bullet("USD/IDR Min (YTD)", "Menampilkan nilai nominal kurs Rupiah terendah terhadap Dolar AS sepanjang tahun. Nilai ini menggambarkan titik terkuat Rupiah (puncak apresiasi Rupiah).")
    
    pdf.ln(1)
    pdf.print_subsection_header("B. Analisis Grafik dan Tabel Overview")
    pdf.print_bullet("Grafik USD/IDR vs IHSG", "Grafik dual-sumbu (dua y-axis). Sumbu kiri (biru) menampilkan pergerakan kurs USD/IDR, sementara sumbu kanan (pink) menampilkan IHSG Composite. Perhatikan ketika garis biru naik (Rupiah melemah), apakah garis pink cenderung turun (IHSG tertekan). Pola ini mendeteksi korelasi negatif antara kurs dan pasar saham.")
    pdf.print_bullet("Tren 3 Mata Uang Utama", "Area chart yang menumpuk pergerakan kurs 3 mata uang acuan utama dunia (USD, EUR, GBP) terhadap Rupiah. Berguna untuk melihat apakah pelemahan/penguatan Rupiah terjadi secara sistemik terhadap seluruh mata uang kuat dunia atau hanya spesifik terhadap Dolar AS.")
    pdf.print_bullet("Performa Mata Uang", "Bar chart horizontal yang mengurutkan kinerja persentase perubahan nilai tukar dari yang terlemah hingga terkuat terhadap Rupiah. Batang berwarna hijau menunjukkan mata uang tersebut menguat terhadap Rupiah (Rupiah melemah), sementara batang merah menunjukkan mata uang tersebut melemah (Rupiah menguat).")
    pdf.print_bullet("Tabel Return Sektoral", "Tabel ringkas bergradien ungu-biru yang mencantumkan return harian/YTD seluruh sektor saham di Bursa Efek Indonesia secara real-time. Memudahkan komparasi performa antar industri dalam satu pandangan mata.")

    # 4. Page 4: Tab 2 - Exchange Rates
    pdf.add_page()
    pdf.print_section_header(3, "Panduan Eksplorasi: Tab 2 - Exchange Rates")
    pdf.print_paragraph(
        "Tab kedua fokus pada analisis mendalam mengenai pergerakan nilai tukar mata uang asing (valas/forex) "
        "dan keterkaitan pergerakan antar mata uang tersebut."
    )
    
    pdf.print_subsection_header("A. Metrik Kurs Utama")
    pdf.print_paragraph(
        "KPI khusus pada tab ini menampilkan detail kurs acuan (default: USD/IDR), meliputi harga penutupan terakhir, "
        "persentase perubahan YTD (dengan indikator warna hijau jika terapresiasi, merah jika terdepresiasi), "
        "serta nilai tertinggi dan terendah sepanjang periode filter lengkap dengan tanggal pencapaiannya."
    )
    
    pdf.print_subsection_header("B. Kontrol Filter Dinamis")
    pdf.print_bullet("Multi-select Mata Uang", "Memungkinkan pengguna memilih satu atau beberapa mata uang sekaligus (misal USDIDR, EURIDR, GBPIDR) untuk diplot bersamaan dalam grafik garis historis. Fitur ini sangat fleksibel untuk membandingkan volatilitas relatif antar mata uang valas.")
    pdf.print_bullet("Filter Periode Analisis", "Dropdown pilihan rentang tanggal analisis: 'Semua' (seluruh data historis dari tahun 2021 hingga 2026), 'YTD' (sejak 1 Januari tahun berjalan), '1 Tahun' (12 bulan ke belakang dari data terakhir), dan '6 Bulan'. Seluruh grafik dan korelasi di Tab 2 akan langsung menyesuaikan secara dinamis.")
    
    pdf.ln(1)
    pdf.print_subsection_header("C. Visualisasi Khusus Nilai Tukar")
    pdf.print_bullet("Pergerakan Historis Kurs", "Line chart multi-warna yang menampilkan tren pergerakan nilai tukar mata uang yang dipilih di filter. Membantu melihat deviasi jangka panjang.")
    pdf.print_bullet("Detail Tren (Area Chart)", "Area chart monokrom yang menyoroti pergerakan mata uang pertama yang dipilih. Area di bawah garis diberi arsiran warna transparan ungu pudar untuk memperjelas wilayah fluktuasi harga.")
    pdf.print_bullet("Tabel Nilai & Harian (%)", "Menampilkan nilai absolut kurs terbaru beserta persentase perubahan dibandingkan dengan harga penutupan hari sebelumnya. Teks berwarna merah menandakan depresiasi harian, sedangkan hijau menandakan apresiasi.")
    pdf.print_bullet("Matriks Korelasi Kurs (Heatmap)", "Visualisasi heatmap interaktif yang mengukur kekuatan hubungan linier antar pergerakan mata uang pilihan. Skala korelasi berkisar antara -1 (korelasi negatif sempurna) hingga +1 (korelasi positif sempurna). Nilai 0 menunjukkan tidak adanya hubungan pergerakan.")
    
    pdf.print_callout(
        "CARA MEMBACA HEATMAP KURS: Jika korelasi EURIDR vs GBPIDR bernilai 0.85, hal ini menunjukkan adanya "
        "hubungan searah yang sangat kuat. Artinya, jika mata uang Euro menguat terhadap Rupiah, kemungkinan besar "
        "Poundsterling Inggris juga akan ikut menguat terhadap Rupiah karena faktor eksternal kawasan Eropa yang serupa.",
        style='info'
    )

    # 5. Page 5: Tab 3 - IHSG Sektoral
    pdf.add_page()
    pdf.print_section_header(4, "Panduan Eksplorasi: Tab 3 - IHSG Sektoral")
    pdf.print_paragraph(
        "Tab ketiga dirancang khusus untuk membedah kinerja pasar saham domestik secara sektoral, mengukur risiko "
        "fluktuasi masing-masing sektor, serta mendeteksi sensitivitas sektor tersebut terhadap pergerakan Dolar AS."
    )
    
    pdf.print_subsection_header("A. Fitur dan Visualisasi Unggulan Sektoral")
    pdf.print_bullet("KPI IHSG Composite", "Menyajikan posisi indeks gabungan terakhir, persentase return YTD, serta level tertinggi/terendah historis beserta tanggal terjadinya. Berguna sebagai tolok ukur (benchmark) pasar modal nasional.")
    pdf.print_bullet("Multi-select Sektor", "Memilih sektor-sektor industri tertentu (misal idxfinance, idxenergy) untuk membandingkan kinerjanya. Sektor 'composite' (IHSG keseluruhan) dimasukkan secara default sebagai benchmark perbandingan.")
    pdf.print_bullet("Performa Sektor Pilihan", "Bar chart persentase return sektor terpilih selama periode analisis yang aktif. Memudahkan melihat sektor mana yang outperform (mengalahkan pasar) dan mana yang underperform (tertinggal dari pasar).")
    
    pdf.ln(1)
    pdf.print_subsection_header("B. Analisis Risiko dan Statistik Hubungan")
    pdf.print_bullet("Volatilitas 30 Hari", "Line chart merah yang menunjukkan standar deviasi pergerakan harga harian sektor terpilih dalam jendela waktu 30 hari bergulir. Puncak grafik menandakan periode ketidakpastian pasar yang tinggi (high risk), sedangkan lembah grafik menandakan periode pergerakan harga yang stabil dan tenang (low risk).")
    pdf.print_bullet("Scatter Plot Hubungan USD/IDR vs IHSG", "Menampilkan titik-titik persebaran data harian koordinat nilai tukar USD/IDR (sumbu X) dan nilai indeks sektor terpilih (sumbu Y). Dilengkapi dengan garis tren regresi linier putus-putus berwarna oranye. Jika garis tren miring ke bawah, hubungan keduanya adalah korelasi negatif (pelemah Rupiah dibarengi penurunan nilai saham sektor tersebut).")
    pdf.print_bullet("Matriks Korelasi Sektor", "Heatmap yang menunjukkan korelasi statistik antar pergerakan sektor saham pilihan. Membantu strategi diversifikasi portofolio investasi (misal jika dua sektor memiliki korelasi sangat rendah, menggabungkan keduanya dalam portofolio akan meminimalkan risiko kerugian sistemik).")

    # 6. Page 6: Interpretasi Finansial & Makna Ekonomi
    pdf.add_page()
    pdf.print_section_header(5, "Interpretasi Finansial & Makna Ekonomi (Panduan Analisis)")
    pdf.print_paragraph(
        "Untuk menghasilkan analisis data yang berkualitas dari dashboard ini, pengguna perlu memahami teori "
        "dan logika keuangan makro yang melatarbelakangi indikator-indikator yang divisualisasikan:"
    )
    
    pdf.print_subsection_header("1. Hubungan Nilai Tukar (USD/IDR) dengan IHSG")
    pdf.print_paragraph(
        "Di negara berkembang seperti Indonesia, pergerakan nilai tukar Dolar terhadap Rupiah sering kali memiliki korelasi "
        "negatif dengan indeks saham gabungan (IHSG). Logikanya sebagai berikut:\n"
        "a. Aliran Modal Asing (Capital Flow): Saat perekonomian global tidak menentu, investor asing cenderung menarik modalnya "
        "dari pasar keuangan Indonesia (Jual Saham di IHSG) dan menukarnya kembali ke mata uang aman seperti Dolar AS (Beli USD). "
        "Tindakan ini menyebabkan harga saham turun (IHSG melemah) dan permintaan USD melonjak (Rupiah melemah).\n"
        "b. Beban Utang dan Impor: Banyak emiten di BEI (terutama sektor infrastruktur, manufaktur, dan farmasi) memiliki utang "
        "dalam denominasi Dolar AS atau mengimpor bahan baku dalam USD. Ketika Rupiah melemah, biaya operasional dan cicilan utang "
        "mereka membengkak, menurunkan laba bersih perusahaan, yang akhirnya menekan harga saham mereka."
    )
    
    pdf.print_subsection_header("2. Klasifikasi Sensitivitas Sektoral terhadap Nilai Tukar")
    pdf.print_paragraph(
        "Tidak semua sektor merespons pergerakan Rupiah dengan cara yang sama. Melalui Scatter Plot dan Matriks Korelasi, "
        "Anda dapat membuktikan karakteristik sektor berikut:\n"
        "a. Sektor Sensitif Negatif (Financial & Property): Sektor keuangan (Finance) sangat sensitif terhadap kurs. "
        "Pelemahan Rupiah biasanya memicu Bank Indonesia menaikkan suku bunga untuk menstabilkan kurs. Kenaikan suku bunga "
        "ini menekan penyaluran kredit perbankan dan menurunkan penjualan sektor properti karena bunga KPR meningkat.\n"
        "b. Sektor Berdampak Positif/Netral (Energy & Basic Materials): Sektor energi (batubara, minyak) dan komoditas tambang "
        "sering kali diuntungkan saat USD menguat. Karena komoditas dunia dihargai dalam USD, emiten sektor ini menerima pendapatan "
        "dalam USD sementara biaya operasionalnya dalam Rupiah, menghasilkan keuntungan kurs yang signifikan."
    )
    
    pdf.print_subsection_header("3. Interpretasi Koefisien Korelasi Heatmap")
    pdf.print_paragraph(
        "Nilai korelasi yang tertera pada heatmap diinterpretasikan sebagai berikut:\n"
        "- Nilai +0.70 s.d +1.00: Hubungan positif kuat (bergerak searah secara konsisten).\n"
        "- Nilai -0.70 s.d -1.00: Hubungan negatif kuat (jika variabel A naik, variabel B pasti turun).\n"
        "- Nilai -0.30 s.d +0.30: Hubungan sangat lemah atau acak (pergerakan tidak saling memengaruhi)."
    )

    # 7. Page 7: Panduan Teknis & Penggunaan Kontrol
    pdf.add_page()
    pdf.print_section_header(6, "Panduan Teknis Pengoperasian Dashboard")
    pdf.print_paragraph(
        "Aplikasi dashboard ini dibangun dengan prinsip 'user-friendly' dan interaktif penuh. Berikut langkah-langkah "
        "teknis untuk memaksimalkan eksplorasi data Anda:"
    )
    
    pdf.print_subsection_header("Langkah 1: Mengatur Periode Waktu Analisis")
    pdf.print_paragraph(
        "Gunakan dropdown 'Periode Analisis' yang tersedia di setiap tab untuk memotong rentang data historis. "
        "Jika Anda ingin melihat respons jangka pendek terhadap rilis kebijakan suku bunga terbaru, pilih opsi '6 Bulan'. "
        "Jika ingin melihat tren siklus jangka panjang yang melewati masa pandemi hingga pemulihan ekonomi, gunakan opsi 'Semua'."
    )
    
    pdf.print_subsection_header("Langkah 2: Melakukan Komparasi Variabel Spesifik")
    pdf.print_paragraph(
        "Di Tab 2 dan 3, gunakan kotak 'Multi-select' untuk menambahkan atau menghapus mata uang / sektor industri dari grafik. "
        "Hindari memilih terlalu banyak variabel sekaligus (disarankan maksimal 3-4 variabel) agar legenda dan garis grafik "
        "tidak tumpang tindih dan tetap mudah dibaca dalam resolusi 1280x585."
    )
    
    pdf.print_subsection_header("Langkah 3: Menggunakan Fitur Interaktif Plotly")
    pdf.print_paragraph(
        "Setiap grafik di dashboard ini menggunakan library Plotly, yang berarti Anda dapat:\n"
        "1. Hovering: Arahkan kursor ke atas garis grafik untuk memunculkan tooltip info nilai nominal presisi dan tanggal data tersebut.\n"
        "2. Zooming: Klik kiri dan seret (drag) area tertentu di dalam grafik untuk memperbesar tampilan detail per tanggal.\n"
        "3. Pan / Reset: Klik dua kali (double click) di dalam grafik untuk mengembalikan skala grafik ke ukuran semula."
    )
    
    pdf.ln(5)
    # Contact/Footer Callout block on last page
    pdf.set_fill_color(243, 244, 246)
    pdf.rect(15, pdf.get_y(), 180, 32, 'F')
    
    pdf.set_y(pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(30, 27, 75)
    pdf.cell(0, 5, '   KONTAK & TIM PENGEMBANG:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 5, '   Aplikasi Visualisasi Data - Semester 4, Universitas Airlangga', 0, 1, 'L')
    pdf.cell(0, 5, '   Pengembang Utama: Tim Asisten Praktikum Visdat', 0, 1, 'L')
    pdf.cell(0, 5, '   Dokumentasi Resmi & Kode Sumber: GitHub Repository Proyek Visdat 2026', 0, 1, 'L')

    # Save PDF
    output_filename = "Panduan_Dashboard_FX_IHSG.pdf"
    pdf.output(output_filename)
    print(f"PDF successfully generated: {output_filename}")

if __name__ == '__main__':
    generate_guide()
