from .models import Fayl


def disk_statistika(request):
    if not request.user.is_authenticated:
        return {}
    fayllar = Fayl.objects.filter(foydalanuvchi=request.user)
    jami = sum(f.hajm for f in fayllar)
    
    for birlik in ["B", "KB", "MB", "GB"]:
        if jami < 1024:
            hajm_str = f"{jami:.1f} {birlik}"
            break
        jami /= 1024
    else:
        hajm_str = f"{jami:.1f} TB"
    
    return {
        "jami_hajm": hajm_str,
        "fayllar_soni": fayllar.count(),
    }
