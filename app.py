from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="template")

# =========================
# 🏠 Halaman Utama
# =========================
@app.route("/")
def home():
    biaya_tetap = request.args.get("biaya_tetap", "")

    if biaya_tetap:
        try:
            biaya_tetap = f"Rp {float(biaya_tetap):,.0f}".replace(",", ".")
        except ValueError:
            pass

    return render_template("index.html", biaya_tetap=biaya_tetap)
# =========================
# 💰 Hasil Analisis Pinjaman
# =========================
@app.route("/hasil", methods=["POST"])
def hasil():
    try:
        gaji = float(request.form.get("gaji", 0))
        biaya_tetap = float(request.form.get("biaya_tetap", 0))
        jumlah_pengajuan = float(request.form.get("jumlah_pengajuan", 0))
        tenor = int(request.form.get("tenor", 0))
    except ValueError:
        return render_template("result.html", error="⚠️ Input tidak valid! Pastikan semua kolom diisi dengan angka.")

    # Validasi input
    if gaji <= 0 or biaya_tetap < 0 or jumlah_pengajuan <= 0:
        return render_template("result.html", error="⚠️ Nilai tidak boleh kosong atau negatif!")

    uang_sisa = gaji - biaya_tetap
    if uang_sisa <= 0:
        return render_template("result.html", error="⚠️ Pengeluaran Anda melebihi gaji!")

    # Tentukan bunga bulanan berdasarkan jumlah pinjaman
    if jumlah_pengajuan <= 5_000_000:
        bunga_per_bulan = 0.025
        label_bunga = "Fintech kecil (2.5%/bulan)"
    elif jumlah_pengajuan <= 20_000_000:
        bunga_per_bulan = 0.018
        label_bunga = "Pinjaman menengah (1.8%/bulan)"
    else:
        bunga_per_bulan = 0.010
        label_bunga = "Pinjaman besar (1.0%/bulan)"

    # Hitung cicilan per bulan (rumus anuitas)
    i = bunga_per_bulan
    n = tenor
    cicilan_perbulan = (jumlah_pengajuan * i) / (1 - (1 + i) ** (-n))
    rasio_cicilan = cicilan_perbulan / uang_sisa

    # Klasifikasi risiko
    if rasio_cicilan <= 0.3:
        kategori = "🟢 Aman"
        pesan = "Pinjaman ini aman dan tidak membebani cashflow bulanan Anda."
    elif rasio_cicilan <= 0.6:
        kategori = "🟡 Hampir Aman"
        pesan = "Masih bisa diajukan, tapi sebaiknya pertimbangkan kembali jumlah pinjaman Anda."
    else:
        kategori = "🔴 Risiko Tinggi"
        pesan = "Pinjaman ini berisiko tinggi dan dapat mengganggu kestabilan keuangan Anda."

    # Hitung total bunga dan rekomendasi
    total_bayar = cicilan_perbulan * tenor
    total_bunga = total_bayar - jumlah_pengajuan
    pinjaman_aman = uang_sisa * 0.3 * tenor
    pinjaman_maksimal = uang_sisa * 0.6 * tenor
    pinjaman_risiko = uang_sisa * 0.8 * tenor

    return render_template(
        "result.html",
        gaji=gaji,
        biaya_tetap=biaya_tetap,
        jumlah_pengajuan=jumlah_pengajuan,
        tenor=tenor,
        bunga_per_bulan=bunga_per_bulan,
        label_bunga=label_bunga,
        cicilan_perbulan=cicilan_perbulan,
        uang_sisa=uang_sisa,
        kategori=kategori,
        pesan=pesan,
        total_bayar=total_bayar,
        total_bunga=total_bunga,
        pinjaman_aman=pinjaman_aman,
        pinjaman_maksimal=pinjaman_maksimal,
        pinjaman_risiko=pinjaman_risiko
    )


# =========================
# 📊 Halaman Penghitungan Pengeluaran
# =========================
@app.route("/pengeluaran")
def pengeluaran():
    return render_template("hitung.html")


@app.route("/hitung_pengeluaran", methods=["POST"])
def hitung_pengeluaran():
    try:
        pengeluaran_lalu = float(request.form.get("pengeluaran_lalu", 0))
        tabungan = float(request.form.get("tabungan", 0))
    except ValueError:
        return render_template("hitung.html", total=None, error="⚠️ Masukkan angka yang valid!")

    if pengeluaran_lalu < 0 or tabungan < 0:
        return render_template("hitung.html", error="⚠️ Nilai tidak boleh negatif!")

    total_pengeluaran = pengeluaran_lalu + tabungan
    if total_pengeluaran < 0:
        return render_template(
            "hitung.html",
            error="⚠️ Data tidak logis: pengeluaran dan tabungan melebihi gaji!",
            total=None
        )

    # Redirect ke halaman utama dengan total otomatis terisi
    return redirect(url_for("home", biaya_tetap=total_pengeluaran))


# =========================
# 🚀 Jalankan Aplikasi
# =========================
if __name__ == "__main__":
    app.run(debug=True)