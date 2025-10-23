from flask import Flask, render_template, request
import math

app = Flask(__name__)

def format_currency(value):
    """Format angka ke format akuntansi Rp"""
    try:
        return f"Rp {round(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "Rp 0"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hasil', methods=['POST'])
def hasil():
    try:
        # Ambil data form
        jenis_pinjaman = request.form.get('jenis_pinjaman', 'bank')
        gaji = float(request.form.get('gaji', 0) or 0)
        biaya_tetap = float(request.form.get('biaya_tetap', 0) or 0)
        jumlah_pengajuan = float(request.form.get('jumlah_pengajuan', 0) or 0)
        bunga_tahunan = float(request.form.get('bunga_tahunan', 0) or 0)
        tenor = int(request.form.get('tenor', 0) or 0)
        tujuan = request.form.get('tujuan', '').strip()

        if gaji <= 0 or jumlah_pengajuan <= 0 or tenor <= 0:
            return render_template('result.html', error="⚠️ Mohon isi semua kolom dengan benar.")

        # Konversi bunga
        if jenis_pinjaman == 'bank':
            bunga_bulanan = bunga_tahunan / 100 / 12
        else:
            bunga_bulanan = bunga_tahunan / 100

        # Rumus cicilan (anuitas)
        if bunga_bulanan > 0:
            cicilan_perbulan = jumlah_pengajuan * (
                (bunga_bulanan * math.pow(1 + bunga_bulanan, tenor)) /
                (math.pow(1 + bunga_bulanan, tenor) - 1)
            )
        else:
            cicilan_perbulan = jumlah_pengajuan / tenor

        total_bunga = (cicilan_perbulan * tenor) - jumlah_pengajuan
        total_pembayaran = cicilan_perbulan * tenor
        sisa_uang = gaji - biaya_tetap

        rasio_gaji = (cicilan_perbulan / gaji) * 100 if gaji > 0 else 0
        rasio_sisa = (cicilan_perbulan / sisa_uang) * 100 if sisa_uang > 0 else 0

        if rasio_sisa > 80:
            risiko = "Tinggi"
            warna = "#ef4444"
            icon = "⚠️"
        elif rasio_sisa > 50:
            risiko = "Sedang"
            warna = "#f59e0b"
            icon = "🟠"
        else:
            risiko = "Rendah"
            warna = "#10b981"
            icon = "✅"

        return render_template(
            'result.html',
            jenis_pinjaman=jenis_pinjaman,
            gaji=format_currency(gaji),
            biaya_tetap=format_currency(biaya_tetap),
            jumlah_pengajuan=format_currency(jumlah_pengajuan),
            bunga_tahunan=bunga_tahunan,
            tenor=tenor,
            tujuan=tujuan,
            cicilan=format_currency(cicilan_perbulan),
            total_bunga=format_currency(total_bunga),
            total_pembayaran=format_currency(total_pembayaran),
            sisa_uang=format_currency(sisa_uang),
            rasio_gaji=round(rasio_gaji, 1),
            rasio_sisa=round(rasio_sisa, 1),
            risiko=risiko,
            warna=warna,
            icon=icon
        )

    except Exception as e:
        return render_template('result.html', error=f"⚠️ Terjadi kesalahan: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)