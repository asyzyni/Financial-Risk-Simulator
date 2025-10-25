// === Update mode pinjaman ===
function updatePinjamanMode() {
  const jenis = document.getElementById("jenis_pinjaman").value;
  const label = document.getElementById("label_bunga");
  const tenorInput = document.getElementById("tenorValueInput");
  const tenorHint = document.getElementById("tenorHint");
  if (jenis === "cicilan") {
    label.textContent = "Bunga Cicilan (% per bulan)";
    tenorInput.max = 24;
    if (parseInt(tenorInput.value) > 24) tenorInput.value = 24;
    tenorHint.textContent = "bulan (maks 24 untuk cicilan barang)";
  } else {
    label.textContent = "Bunga Pinjaman (% per tahun)";
    tenorInput.max = 360;
    tenorHint.textContent = "bulan (maks 360 bulan untuk pinjaman bank)";
  }
}

// === Format Rupiah ===
function formatRupiah(angka) {
  const numberString = angka.replace(/[^,\d]/g, "").toString();
  const split = numberString.split(",");
  const sisa = split[0].length % 3;
  let rupiah = split[0].substr(0, sisa);
  const ribuan = split[0].substr(sisa).match(/\d{3}/gi);
  if (ribuan) {
    const separator = sisa ? "." : "";
    rupiah += separator + ribuan.join(".");
  }
  return "Rp " + rupiah;
}

function unformatRupiah(value) {
  return value.replace(/[^0-9]/g, "");
}

["gaji", "biaya_tetap", "jumlah_pengajuan"].forEach((id) => {
  const input = document.getElementById(id);
  input.addEventListener("input", function () {
    const val = unformatRupiah(this.value);
    this.value = formatRupiah(val);
  });
});

function prepareValues() {
  ["gaji", "biaya_tetap", "jumlah_pengajuan"].forEach((id) => {
    const input = document.getElementById(id);
    input.value = unformatRupiah(input.value);
  });
}

// === Modal ===

function openModal() {
  document.getElementById("pengeluaranModal").style.display = "block";
}
function closeModal() {
  document.getElementById("pengeluaranModal").style.display = "none";
}
function resetModal() {
  document.getElementById("bulan_lalu").value = "";
  document.getElementById("tabungan").value = "";
  document.getElementById("totalPengeluaran").textContent = "Rp 0";
}

function handleEnter(e) {
  if (e.key === "Enter") {
    e.preventDefault();
    document.getElementById("tabungan").focus();
  }
}

function formatDanHitung(el) {
  const val = unformatRupiah(el.value);
  el.value = formatRupiah(val);
  hitungTotal();
}

function hitungTotal() {
  const a = parseInt(
    unformatRupiah(document.getElementById("bulan_lalu").value) || 0
  );
  const b = parseInt(
    unformatRupiah(document.getElementById("tabungan").value) || 0
  );
  const total = a + b;
  document.getElementById("totalPengeluaran").textContent = formatRupiah(
    total.toString()
  );
}

function gunakanTotal() {
  const total = document.getElementById("totalPengeluaran").textContent;
  document.getElementById("biaya_tetap").value = total;
  closeModal();
}
