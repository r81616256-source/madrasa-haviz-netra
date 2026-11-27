#!/usr/bin/env python3
"""
Generator Materi Audio Pondok Hafidz Netra v7.0 (Suara Media Teknologi)
Menggunakan edge-tts (id-ID-ArdiNeural) dengan fungsi permanen render_mp3.
Menghasilkan 106 berkas MP3 variatif untuk seluruh alur v7.0.
"""
import asyncio
import os
import edge_tts

VOICE = "id-ID-ArdiNeural"
OUT_DIR = "audio_ustadz"

AUDIO_SCRIPTS = {
    # 1. Salam & Penjaga Waktu Otomatis (12)
    "salam_pembuka.mp3": "Assalamu'alaikum warahmatullahi wabarakatuh. Selamat datang di Santri Digital Pondok Hafidz Netra.",
    "salam_penutup.mp3": "Alhamdulillahi rabbil 'alamin. Sesi hari ini selesai dengan baik. Sampai jumpa di majelis berikutnya.",
    "doa_pagi_pembuka.mp3": "Assalamu'alaikum! Selamat pagi. Mari awali hari dengan doa pagi, niat ikhlas, dan semangat menghafal Al-Qur'an.",
    "pengingat_bel_kelas.mp3": "Kang Ridho menyapa: Lima menit lagi bel masuk kelas berbunyi. Yuk menuju Gedung Kelas untuk presensi.",
    "pengingat_susulan.mp3": "Ustadzah Nur menyapa: Hari ini kamu belum presensi di kelas. Yuk ikut kelas susulan atau ajukan izin resmi di Kantor TU.",
    "pengingat_antilupa.mp3": "Ustadz Yeni menyapa: Yuk sempatkan murajaah satu ayat dan cek tugas rumahmu di Kamar Pribadi.",
    "wirid_sore_pengantar.mp3": "Corong Masjid Agung: Waktunya Wirid Sore dan enam surat pendek penenang hati.",
    "majelis_malam_jumat_panggilan.mp3": "Corong Masjid Agung: Malam Jumat telah tiba. Mari berkumpul di Masjid Agung untuk Doa Arwah, Yasin, dan Tahlil.",
    "ucapan_milad_santri.mp3": "Barakallahu fii umrik! Ustadz Yeni Setiawan, Ustadzah Nur, dan seluruh keluarga pondok mendoakan keberkahan umurmu.",
    "bel_masuk_kelas.mp3": "Bel masuk kelas telah berbunyi. Mari duduk tenang, rapikan niat, dan mulai presensi.",
    "bel_pulang_kelas.mp3": "Bel pulang berbunyi. Simpan catatan PR rumahmu dan jaga adab selama di perjalanan pulang.",
    "sekolah_tutup_malam.mp3": "Gedung kelas sudah tutup malam. Kamu tetap bebas belajar dua puluh empat jam di Kamar Pribadi Rumah Santri.",

    # 2. Masa Ta'aruf & Adab 4 Pos (10)
    "taaruf_gerbang.mp3": "Kang Ridho: Assalamu'alaikum! Selamat datang di Gerbang Utama Pondok Hafidz Netra. Mari mulai Pos Satu Ta'aruf dan Adab Salam.",
    "taaruf_tu.mp3": "Ustadzah Nur: Assalamu'alaikum! Silakan duduk di depan loket Kantor TU untuk wawancara pendaftaran dan layanan administrasi.",
    "taaruf_asrama.mp3": "Ustadzah Khadijah Rahmawati: Mari mengenal empat adab inti penghafal Al-Qur'an, ruang rumah, dan sarana digital pondok.",
    "taaruf_pelantikan.mp3": "Ustadz Yeni Setiawan: Selamat atas pelantikan resmimu sebagai santri Pondok Hafidz Netra. Semoga istiqamah menjaga Al-Qur'an.",
    "adab_masuk_masjid.mp3": "Mari melangkah masuk Masjid Agung dengan kaki kanan, membaca doa masuk masjid, dan menjaga ketenangan.",
    "adab_izin_keluar.mp3": "Adab santri yang baik adalah selalu meminta izin kepada guru bila perlu keluar di tengah jam kelas.",
    "adab_sapa_ortu.mp3": "Berbakti kepada orang tua dan memohon doa restu di Ruang Tamu adalah kunci keberkahan hafalan.",
    "adab_rawat_sarana.mp3": "Merawat perangkat digital pondok melalui Koperasi adalah wujud syukur dan tanggung jawab bersama.",
    "sapaan_luar_kota.mp3": "MasyaAllah, walau berasal dari jauh, di Pondok Hafidz Netra kita adalah satu keluarga besar yang hangat.",
    "motivasi_hari_ahad.mp3": "Selamat Hari Ahad! Sekolah libur resmi, waktunya sambangan keluarga di Ruang Tamu dan murajaah santai di Teras Rumah.",

    # 3. Orientasi Mobilitas Usap 2 Jari (8)
    "orientasi_pembuka.mp3": "Mode Orientasi Mobilitas Usap Dua Jari aktif. Usap dua jari ke atas untuk Utara, bawah Selatan, kanan Timur, kiri Barat.",
    "orientasi_utara.mp3": "Kamu melangkah ke arah Utara.",
    "orientasi_selatan.mp3": "Kamu melangkah ke arah Selatan.",
    "orientasi_timur.mp3": "Kamu melangkah ke arah Timur.",
    "orientasi_barat.mp3": "Kamu melangkah ke arah Barat.",
    "orientasi_salah_arah.mp3": "Belum tepat, arah itu bukan jalur tujuanmu. Simak kembali petunjuk arah kompas berikutnya.",
    "orientasi_tiba_pintu.mp3": "Alhamdulillah kamu tiba tepat di depan pintu ruangan tujuan. Ketuk tombol Masuk Pintu sekarang.",
    "orientasi_latihan_lulus.mp3": "MasyaAllah, keempat arah kompas usap dua jari sudah kamu kuasai dengan baik.",

    # 4. Gedung Kelas 4 Babak & Pendidikan Formal (14)
    "kelas_babak1.mp3": "Babak Satu: Bel masuk dan presensi melalui Mesin Presensi Digital kelas.",
    "kelas_babak2.mp3": "Babak Dua: Mengecek PR rumah dan murajaah memori lanjutan belajar kemarin.",
    "kelas_babak3.mp3": "Babak Tiga: Menyimak materi utama hari ini dan blok hafalan terarah bersama pembimbing.",
    "kelas_babak4.mp3": "Babak Empat: Evaluasi singkat, penetapan PR rumah, dan persiapan bel pulang.",
    "kelas_sinkron_rumah.mp3": "MasyaAllah! Pembimbing menerima pemberitahuan surat yang sudah kamu matangkan tujuh puluh lima persen dari Rumah.",
    "kelas_auto_lanjut.mp3": "Alhamdulillah seratus persen hijau! Otomatis berlanjut ke ayat berikutnya.",
    "kelas_tuntas_surat.mp3": "Barakallahu fiik! Seluruh ayat dalam surat ini telah mencapai seratus persen hijau dan tercatat di Mutaba'ah.",
    "kelas_idad_iqra.mp3": "Kelas I'dad aktif. Mari fokus melancarkan makhraj dan harakat Iqra' jilid aktifmu.",
    "formal_pembuka.mp3": "Selamat datang di Gedung Sekolah Formal Pondok Hafidz Netra untuk jenjang MI, MTs, MA, dan Ma'had Aly.",
    "formal_bindo.mp3": "Pelajaran Bahasa Indonesia: Mari belajar menemukan gagasan pokok secara lisan.",
    "formal_matematika.mp3": "Pelajaran Matematika Audio: Mari melatih berhitung cepat dengan memecah puluhan dan satuan.",
    "formal_ipa.mp3": "Pelajaran IPA Sains Alam: Mari mengenal rambatan bunyi dan cara menjaga kesehatan pita suara.",
    "formal_ppkn.mp3": "Pelajaran PPKn: Mari memahami hak aksesibilitas dan semangat gotong royong inklusif.",
    "formal_bahasa.mp3": "Pelajaran Bahasa Arab dan Inggris: Mari menghafal kosakata ruang kelas dan perpustakaan.",

    # 5. Rumah Santri 4 Ruangan (8)
    "rumah_kamar_pribadi.mp3": "Kamu berada di Kamar Pribadi. Meja belajar bebas dua puluh empat jam dan Buku Catatan Digital siap digunakan.",
    "rumah_ruang_tamu.mp3": "Kamu berada di Ruang Tamu Rumah. Yuk menyapa orang tua dan membacakan Buku Penghubung Keluarga.",
    "rumah_dapur.mp3": "Kamu berada di Dapur Rumah. Nikmati sarapan sehat dan air hangat madu jahe penjaga suara.",
    "rumah_teras_taman.mp3": "Kamu berada di Teras dan Taman Rumah. Kamu bisa menyiram tanaman atau berangkat ke pondok lewat Usap Dua Jari.",
    "rumah_jurnal_terkirim.mp3": "Catatan dan laporan PR rumahmu telah terkirim ke Komputer Server TU Ustadzah Nur.",
    "rumah_istirahat.mp3": "Alhamdulillah, istirahat sejenak memulihkan stamina belajar dan kejernihan suaramu.",
    "rumah_siram_tanaman.mp3": "Tanaman di taman rumah tampak segar kembali. Nilai adab peduli lingkungan bertambah.",
    "rumah_matang_75.mp3": "MasyaAllah, surat latihan rumahmu sudah mencapai tujuh puluh lima persen dan siap disetorkan di Sekolah.",

    # 6. Kantor TU, Ujian Anti-Klik, Cetak & Sarana Digital (14)
    "tu_antrean.mp3": "Mesin Antrean Kantor TU memanggil giliranmu. Silakan menuju loket Ustadzah Nur.",
    "tu_server_buka.mp3": "Komputer Server TU menyala. Memuat catatan rumah santri dan data induk verifikasi NIS.",
    "tu_tanggapan_nur.mp3": "Ustadzah Nur sudah membaca catatan rumahmu dan memberikan tanggapan penyemangat.",
    "tu_printer_cetak.mp3": "Printer Dokumen Resmi sedang mencetak berkas ber-kop resmi dalam format foto PNG dan teks.",
    "tu_corong_siar.mp3": "Mikrofon Corong Pondok aktif. Pengumumanmu telah disiarkan ke seluruh santri melalui Firebase.",
    "tu_verifikasi_nis.mp3": "Sedang memverifikasi Nomor Induk Santri secara langsung ke server Firebase Pondok.",
    "ujian_pembuka.mp3": "Selamat datang di Sistem Ujian Anti-Klik-Sembarangan. Simak setiap soal minimal tiga detik sebelum menjawab.",
    "ujian_kunci_kilat.mp3": "Kunci anti-klik-kilat aktif. Mohon simak soal dengan tenang minimal tiga detik sebelum memilih jawaban.",
    "ujian_tahap2_susun.mp3": "Lanjut ke Tahap Dua: Susun potongan ayat secara berurutan untuk membuktikan hafalan nyata.",
    "ujian_lulus.mp3": "Alhamdulillah, kamu lulus ujian dua tahap dengan jujur! Nilai resmi tercatat di Rapor.",
    "ujian_remidi_wajib.mp3": "Nilai belum mencapai tujuh puluh lima persen. Yuk selesaikan Sesi Remidi Nyata terlebih dahulu sebelum mengulang.",
    "ujian_remidi_selesai.mp3": "Alhamdulillah Sesi Remidi Nyata tuntas. Sekarang izin mengulang ujian sudah terbuka kembali.",
    "koperasi_rawat_satu.mp3": "Perangkat digital pondok selesai diservis di Koperasi dan kembali seratus persen prima.",
    "koperasi_rawat_semua.mp3": "Seluruh dua belas sarana digital pondok telah dirawat lewat Koperasi. Semua kembali prima.",

    # 7. Majelis Malam Jumat, Firebase & Ekonomi Kemandirian (14)
    "majelis_pembuka.mp3": "Ustadz Yeni Setiawan membuka Majelis Malam Jumat di Masjid Agung. Mari niatkan doa terbaik untuk keluarga kita.",
    "majelis_arwah_intro.mp3": "Mari menyimak daftar nama almarhum dan almarhumah satu per satu dari Firebase lalu ucapkan Aamiin bersama.",
    "majelis_aamiin.mp3": "Aamiin ya Rabbal 'alamin. Semoga Allah melapangkan kubur dan mengampuni dosa beliau.",
    "majelis_yasin_intro.mp3": "Sound System Masjid Agung memutar lantunan Surat Yasin dan wirid Qari asli. Mari menyimak dengan khusyuk.",
    "majelis_penutup.mp3": "Rabbana atina fid-dunya hasanah wa fil-akhirati hasanah. Majelis Malam Jumat tuntas dan tercatat di Mutaba'ah.",
    "firebase_doa_terkirim.mp3": "Doa Semangatmu telah terkirim ke papan halaqah online seluruh santri Pondok Hafidz Netra.",
    "ekonomi_pusat.mp3": "Selamat datang di Pusat Ekonomi Kemandirian Pondok, Asrama, Kebun, dan Pasar Pondok.",
    "ekonomi_cair_pasif.mp3": "Alhamdulillah, penghasilan pasif dari gedung usaha dan toko pondok berhasil dicairkan ke Kas Pondok.",
    "ekonomi_bangun_gedung.mp3": "Alhamdulillah, gedung usaha baru pondok selesai dibangun dan mulai menghasilkan pemasukan pasif.",
    "ekonomi_upgrade_gedung.mp3": "Gedung usaha pondok naik level! Kapasitas penghasilan pasif menuju lima ratus juta semakin meningkat.",
    "ekonomi_panen_kebun.mp3": "Alhamdulillah, panen pasif Kebun Sayur, Jahe, dan Kolam Ikan Asrama berhasil terkumpul.",
    "ekonomi_dapur_asrama.mp3": "Dapur Asrama memasak hidangan bergizi dari hasil panen kebun dan kolam sendiri. Stamina santri pulih.",
    "ekonomi_pasar_jual.mp3": "Hasil panen kebun dan kolam laku terjual di Pasar Pondok. Saldo Kas Pondok bertambah.",
    "ekonomi_pasar_belanja.mp3": "Belanja grosir bahan segar di Pasar Pondok selesai. Persediaan Dapur Asrama kembali penuh.",

    # 8. 20 Metode Hafalan & Respon Emosional Guru (26)
    "metode_talaqqi.mp3": "Memulai metode Talaqqi Per Ayat. Dengarkan Qari dengan tenang lalu tirukan perlahan.",
    "metode_tikrar_berantai.mp3": "Memulai metode Tikrar Berantai untuk mengikat sambungan antar ayat.",
    "metode_tikrar_intensif.mp3": "Memulai metode Tikrar Intensif berulang agar bacaan tertanam kuat di ingatan.",
    "metode_sabak_sabqi.mp3": "Memulai metode Sabak dan Sabqi untuk menggabungkan hafalan baru dan murajaah dekat.",
    "metode_dengar_santai.mp3": "Memulai metode Dengar Santai agar irama ayat meresap tenang ke hati.",
    "metode_shadowing.mp3": "Memulai metode Shadowing tiga tahap untuk menyamakan makhraj dan irama Qari.",
    "metode_per_kata.mp3": "Memulai metode Pecah Per Kata agar lafaz sulit mudah ditirukan.",
    "metode_waqaf.mp3": "Memulai metode Potong Waqaf untuk membantu napas pada ayat panjang.",
    "metode_buka_tutup.mp3": "Memulai metode Audio Buka Tutup untuk menguji ketajaman ingatan mandiri.",
    "metode_rantai_mundur.mp3": "Memulai metode Rantai Mundur dari ayat akhir ke awal blok.",
    "metode_tautan_engsel.mp3": "Memulai metode Tautan Engsel untuk menguatkan perpindahan akhir ayat ke awal ayat berikutnya.",
    "metode_tempo.mp3": "Memulai metode Pelatih Tempo dari kecepatan pelan menuju kecepatan normal.",
    "metode_estafet.mp3": "Memulai metode Estafet Gantian satu ayat Qari dan satu ayat giliran santri.",
    "metode_rescue_lupa.mp3": "Memulai metode Penyelamat Lupa dengan pengulangan pendek yang ramah.",
    "metode_blok3.mp3": "Memulai metode Blok Tiga Ayat secara bertahap dan terukur.",
    "metode_tasmi.mp3": "Memulai metode Tasmi satu surat penuh tanpa terputus.",
    "metode_tadabbur.mp3": "Memulai metode Tadabbur Makna untuk memahami pesan indah ayat Al-Qur'an.",
    "metode_mutasyabihat.mp3": "Memulai metode Peringatan Ayat Mutasyabihat agar tidak tertukar dengan surat lain.",
    "metode_maqamat.mp3": "Memulai metode Irama Maqamat agar bacaan semakin merdu dan menyentuh.",
    "metode_murajaah_cepat.mp3": "Memulai Murajaah Cepat untuk menjaga kelancaran hafalan yang sudah hijau.",
    "emosi_futur.mp3": "Tidak apa-apa kalau kemarin sempat lelah atau sibuk. Hari ini kita mulai pelan-pelan lagi dari satu ayat saja ya.",
    "emosi_lelah.mp3": "Staminamu tampak agak lelah. Mari baca pelan saja, atau istirahat sebentar dan minum air hangat di Dapur Rumah.",
    "emosi_sabar_sulit.mp3": "MasyaAllah kamu sangat sabar mengulang bagian sulit ini. Setiap huruf yang diulang dengan susah payah berpahala ganda.",
    "emosi_semangat_rumah.mp3": "MasyaAllah, semangat belajarmu dari Rumah luar biasa! Pembimbing sangat bangga padamu.",
    "emosi_kembali_izin.mp3": "Alhamdulillah kamu sudah kembali sehat dan siap belajar. Kita mulai dengan pemanasan ringan dulu.",
    "emosi_istiqamah.mp3": "Senang melihatmu hadir tenang dan istiqamah hari ini. Semoga Allah memudahkan setiap huruf hafalanmu.",
}


async def render_mp3(filename: str, text: str) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, filename)
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate="-4%")
    await communicate.save(out_path)
    print(f"[OK] {out_path}")


async def main() -> None:
    print(f"Memulai render_mp3 untuk {len(AUDIO_SCRIPTS)} berkas suara Ustadz Ardi...")
    for filename, text in AUDIO_SCRIPTS.items():
        await render_mp3(filename, text)
    print(f"Selesai! Total {len(AUDIO_SCRIPTS)} MP3 berhasil dibuat di folder '{OUT_DIR}/'.")


if __name__ == "__main__":
    asyncio.run(main())
