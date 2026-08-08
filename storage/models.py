import os
from django.db import models
from accounts.models import User


FAYL_TURI_IKONKALAR = {
    # Rasmlar
    ".jpg": ("rasm", "🖼️"), ".jpeg": ("rasm", "🖼️"), ".png": ("rasm", "🖼️"),
    ".gif": ("rasm", "🖼️"), ".webp": ("rasm", "🖼️"), ".svg": ("rasm", "🖼️"),
    ".bmp": ("rasm", "🖼️"), ".ico": ("rasm", "🖼️"),
    # Video
    ".mp4": ("video", "🎬"), ".avi": ("video", "🎬"), ".mkv": ("video", "🎬"),
    ".mov": ("video", "🎬"), ".webm": ("video", "🎬"), ".flv": ("video", "🎬"),
    # Audio
    ".mp3": ("audio", "🎵"), ".wav": ("audio", "🎵"), ".ogg": ("audio", "🎵"),
    ".m4a": ("audio", "🎵"), ".flac": ("audio", "🎵"), ".aac": ("audio", "🎵"),
    # Hujjat
    ".pdf": ("pdf", "📑"),
    ".doc": ("word", "📝"), ".docx": ("word", "📝"),
    ".xls": ("excel", "📊"), ".xlsx": ("excel", "📊"),
    ".ppt": ("ppt", "📋"), ".pptx": ("ppt", "📋"),
    # Arxiv
    ".zip": ("arxiv", "📦"), ".rar": ("arxiv", "📦"), ".7z": ("arxiv", "📦"),
    ".tar": ("arxiv", "📦"), ".gz": ("arxiv", "📦"),
    # Matn/Kod
    ".txt": ("matn", "📄"), ".py": ("kod", "💻"), ".js": ("kod", "💻"),
    ".ts": ("kod", "💻"), ".html": ("kod", "💻"), ".css": ("kod", "💻"),
    ".json": ("kod", "💻"), ".xml": ("kod", "💻"), ".md": ("kod", "💻"),
    ".csv": ("kod", "💻"), ".jsx": ("kod", "💻"), ".tsx": ("kod", "💻"),
    ".java": ("kod", "💻"), ".cpp": ("kod", "💻"), ".c": ("kod", "💻"),
    ".h": ("kod", "💻"), ".php": ("kod", "💻"), ".rb": ("kod", "💻"),
    ".go": ("kod", "💻"), ".rs": ("kod", "💻"), ".sh": ("kod", "💻"),
    ".yaml": ("kod", "💻"), ".yml": ("kod", "💻"), ".sql": ("kod", "💻"),
    ".vue": ("kod", "💻"), ".dart": ("kod", "💻"), ".kt": ("kod", "💻"),
    ".swift": ("kod", "💻"), ".r": ("kod", "💻"), ".m": ("kod", "💻"),
}

MATN_KENGAYTMALARI = {
    ".txt", ".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".md",
    ".csv", ".jsx", ".tsx", ".java", ".cpp", ".c", ".h", ".php", ".rb",
    ".go", ".rs", ".sh", ".yaml", ".yml", ".sql", ".vue", ".dart", ".kt",
    ".swift", ".r", ".m", ".env", ".gitignore", ".dockerfile",
}


class Papka(models.Model):
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE, related_name="papkalar")
    nom = models.CharField(max_length=255)
    ota_papka = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="ichki_papkalar"
    )
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Papka"
        verbose_name_plural = "Papkalar"

    def __str__(self):
        return self.nom

    def non_olish(self):
        """Papkaning to'liq yo'lini olish"""
        qismlar = []
        papka = self
        while papka:
            qismlar.insert(0, papka)
            papka = papka.ota_papka
        return qismlar


class Fayl(models.Model):
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fayllar")
    papka = models.ForeignKey(
        Papka, null=True, blank=True, on_delete=models.SET_NULL, related_name="fayllar"
    )
    nom = models.CharField(max_length=255)
    fayl = models.FileField(upload_to="fayllar/")
    hajm = models.BigIntegerField(default=0)
    oxirgi_pozitsiya = models.JSONField(default=dict)
    yaratilgan = models.DateTimeField(auto_now_add=True)
    yangilangan = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fayl"
        verbose_name_plural = "Fayllar"

    def __str__(self):
        return self.nom

    def kengaytma(self):
        return os.path.splitext(self.nom)[1].lower()

    def tur_va_ikonka(self):
        ext = self.kengaytma()
        return FAYL_TURI_IKONKALAR.get(ext, ("boshqa", "📎"))

    def tur(self):
        return self.tur_va_ikonka()[0]

    def ikonka(self):
        return self.tur_va_ikonka()[1]

    def rasm_mi(self):
        return self.tur() == "rasm"

    def pdf_mi(self):
        return self.tur() == "pdf"

    def matn_mi(self):
        return self.kengaytma() in MATN_KENGAYTMALARI

    def word_mi(self):
        return self.tur() == "word"

    def excel_mi(self):
        return self.tur() == "excel"

    def video_mi(self):
        return self.tur() == "video"

    def audio_mi(self):
        return self.tur() == "audio"

    def hajm_formatlangan(self):
        hajm = self.hajm
        for birlik in ["B", "KB", "MB", "GB"]:
            if hajm < 1024:
                return f"{hajm:.1f} {birlik}"
            hajm /= 1024
        return f"{hajm:.1f} TB"

    def rang_klass(self):
        """Fayl turiga ko'ra rang"""
        ranglar = {
            "rasm": "text-emerald-500",
            "video": "text-purple-500",
            "audio": "text-pink-500",
            "pdf": "text-red-500",
            "word": "text-blue-500",
            "excel": "text-green-600",
            "ppt": "text-orange-500",
            "arxiv": "text-yellow-600",
            "kod": "text-indigo-500",
            "matn": "text-slate-500",
        }
        return ranglar.get(self.tur(), "text-slate-400")
