#!/usr/bin/env python3
"""
Thender Icon Generator v2.0
ينشئ جميع أيقونات SVG المطلوبة تلقائياً في مجلد public/icons/
يتضمن: أيقونات البحث، الشعار، المميزات، الوسائط، والوجه الأسطوري
"""

import os
from pathlib import Path

# ==================== الألوان الأساسية ====================
COLORS = {
    'primary': '#4caf50',
    'primary_light': '#a8e6a3',
    'primary_lighter': '#c8f0c4',
    'primary_dark': '#2e7d32',
    'primary_darker': '#1b5e20',
    'white': '#ffffff',
    'bg': '#f1f8f1',
    'text': '#1a3a1a',
}

# مسار مجلد الأيقونات
ICONS_DIR = Path(__file__).parent / 'public' / 'icons'


# ==================== دوال مساعدة ====================

def ensure_dir():
    """إنشاء المجلد إذا لم يكن موجوداً"""
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ تم إنشاء/التحقق من المجلد: {ICONS_DIR}")


def save_svg(name: str, content: str):
    """حفظ ملف SVG"""
    path = ICONS_DIR / f"{name}.svg"
    path.write_text(content, encoding='utf-8')
    print(f"  ✓ {name}.svg")


# ==================== أيقونات البحث والواجهة ====================

def icon_search():
    """أيقونة البحث (عدسة مكبرة)"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="11" cy="11" r="7"/>
  <line x1="16.5" y1="16.5" x2="22" y2="22"/>
</svg>"""


def icon_arrow():
    """أيقونة السهم الأبيض (زر الإرسال)"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <line x1="5" y1="12" x2="19" y2="12"/>
  <polyline points="12 5 19 12 12 19"/>
</svg>"""


def icon_arrow_green():
    """أيقونة السهم الأخضر"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <line x1="5" y1="12" x2="19" y2="12"/>
  <polyline points="12 5 19 12 12 19"/>
</svg>"""


def icon_clear():
    """أيقونة مسح/إغلاق (X)"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round">
  <line x1="18" y1="6" x2="6" y2="18"/>
  <line x1="6" y1="6" x2="18" y2="18"/>
</svg>"""


def icon_external():
    """أيقونة رابط خارجي"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
  <polyline points="15 3 21 3 21 9"/>
  <line x1="10" y1="14" x2="21" y2="3"/>
</svg>"""


def icon_keyboard():
    """أيقونة لوحة المفاتيح"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="4" width="20" height="16" rx="2"/>
  <line x1="6" y1="8" x2="6.01" y2="8"/>
  <line x1="10" y1="8" x2="10.01" y2="8"/>
  <line x1="14" y1="8" x2="14.01" y2="8"/>
  <line x1="18" y1="8" x2="18.01" y2="8"/>
  <line x1="6" y1="12" x2="6.01" y2="12"/>
  <line x1="10" y1="12" x2="10.01" y2="12"/>
  <line x1="14" y1="12" x2="14.01" y2="12"/>
  <line x1="18" y1="12" x2="18.01" y2="12"/>
  <line x1="8" y1="16" x2="16" y2="16"/>
</svg>"""


# ==================== أيقونات المميزات ====================

def icon_shield_enhanced():
    """أيقونة الدرع المحسّنة مع حرف T وعلامة صح"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c8f0c4"/>
      <stop offset="100%" stop-color="#a8e6a3"/>
    </linearGradient>
  </defs>
  <path d="M32 4 L56 14 L56 32 Q56 52 32 60 Q8 52 8 32 L8 14 Z" 
        fill="url(#shieldGrad)" stroke="#4caf50" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M22 32 L29 39 L42 24" fill="none" stroke="#2e7d32" stroke-width="3.5" 
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def icon_globe():
    """أيقونة الكرة الأرضية"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#4caf50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="26"/>
  <line x1="6" y1="32" x2="58" y2="32"/>
  <path d="M32 6 C42 6 48 18 48 32 C48 46 42 58 32 58 C22 58 16 46 16 32 C16 18 22 6 32 6 Z"/>
  <line x1="14" y1="20" x2="50" y2="20"/>
  <line x1="14" y1="44" x2="50" y2="44"/>
</svg>"""


def icon_lightning():
    """أيقونة البرق (السرعة)"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#4caf50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="34 4 14 34 28 34 24 60 50 28 34 28 38 4"/>
</svg>"""


# ==================== أيقونات الوسائط (جديدة) ====================

def icon_image():
    """أيقونة الصور"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#4caf50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <rect x="8" y="8" width="48" height="48" rx="4"/>
  <circle cx="22" cy="22" r="5"/>
  <polyline points="52 44 38 30 16 52"/>
  <polyline points="44 44 34 34 24 44"/>
</svg>"""


def icon_video():
    """أيقونة الفيديو"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#4caf50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <rect x="6" y="14" width="38" height="36" rx="4"/>
  <polygon points="48 22 60 14 60 50 48 42"/>
  <line x1="16" y1="26" x2="34" y2="26"/>
  <line x1="16" y1="38" x2="28" y2="38"/>
</svg>"""


def icon_news():
    """أيقونة الأخبار/الجريدة"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#4caf50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <rect x="8" y="6" width="48" height="52" rx="3"/>
  <line x1="8" y1="18" x2="56" y2="18"/>
  <line x1="20" y1="6" x2="20" y2="18"/>
  <line x1="16" y1="26" x2="48" y2="26"/>
  <line x1="16" y1="34" x2="48" y2="34"/>
  <line x1="16" y1="42" x2="40" y2="42"/>
  <line x1="16" y1="50" x2="32" y2="50"/>
</svg>"""


def icon_play():
    """أيقونة التشغيل (مثلث أبيض)"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff">
  <polygon points="6 3 20 12 6 21 6 3"/>
</svg>"""


def icon_play_green():
    """أيقونة التشغيل خضراء"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#4caf50">
  <polygon points="6 3 20 12 6 21 6 3"/>
</svg>"""


# ==================== أيقونات الشعار ====================

def icon_logo_t():
    """شعار T للإنجليزية - دائري بتدرج"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <defs>
    <radialGradient id="gradT" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#c8f0c4"/>
      <stop offset="100%" stop-color="#a8e6a3"/>
    </radialGradient>
    <filter id="shadowT" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#4caf50" flood-opacity="0.3"/>
    </filter>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#gradT)" stroke="#4caf50" stroke-width="3" filter="url(#shadowT)"/>
  <text x="100" y="145" font-size="150" font-family="Arial, sans-serif" 
        font-weight="bold" fill="#2e7d32" text-anchor="middle">T</text>
</svg>"""


def icon_logo_th():
    """شعار ث للعربية - دائري بتدرج"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <defs>
    <radialGradient id="gradTH" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#c8f0c4"/>
      <stop offset="100%" stop-color="#a8e6a3"/>
    </radialGradient>
    <filter id="shadowTH" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#4caf50" flood-opacity="0.3"/>
    </filter>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#gradTH)" stroke="#4caf50" stroke-width="3" filter="url(#shadowTH)"/>
  <text x="100" y="140" font-size="140" font-family="Arial, sans-serif" 
        font-weight="bold" fill="#2e7d32" text-anchor="middle">ث</text>
</svg>"""


def icon_logo_small_t():
    """شعار T صغير للهيدر"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
  <defs>
    <radialGradient id="gradST" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#c8f0c4"/>
      <stop offset="100%" stop-color="#a8e6a3"/>
    </radialGradient>
  </defs>
  <circle cx="20" cy="20" r="18" fill="url(#gradST)" stroke="#4caf50" stroke-width="2"/>
  <text x="20" y="28" font-size="26" font-family="Arial, sans-serif" 
        font-weight="bold" fill="#2e7d32" text-anchor="middle">T</text>
</svg>"""


def icon_logo_small_th():
    """شعار ث صغير للهيدر"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
  <defs>
    <radialGradient id="gradSTH" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#c8f0c4"/>
      <stop offset="100%" stop-color="#a8e6a3"/>
    </radialGradient>
  </defs>
  <circle cx="20" cy="20" r="18" fill="url(#gradSTH)" stroke="#4caf50" stroke-width="2"/>
  <text x="20" y="28" font-size="24" font-family="Arial, sans-serif" 
        font-weight="bold" fill="#2e7d32" text-anchor="middle">ث</text>
</svg>"""


# ==================== أيقونات الحالة ====================

def icon_sad_face():
    """الوجه الأسطوري - لا توجد نتائج (محايد)"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <defs>
    <radialGradient id="sadGrad" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#f1f8f1"/>
      <stop offset="100%" stop-color="#e8f5e9"/>
    </radialGradient>
  </defs>
  <circle cx="60" cy="60" r="50" fill="url(#sadGrad)" stroke="#4caf50" stroke-width="4"/>
  <circle cx="42" cy="50" r="5" fill="#2e7d32"/>
  <circle cx="78" cy="50" r="5" fill="#2e7d32"/>
  <line x1="45" y1="75" x2="75" y2="75" stroke="#4caf50" stroke-width="4" stroke-linecap="round"/>
</svg>"""


def icon_loading():
    """أيقونة التحميل الدوارة"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
  <circle cx="25" cy="25" r="20" fill="none" stroke="#a8e6a3" stroke-width="4"/>
  <path d="M25 5 A 20 20 0 0 1 45 25" fill="none" stroke="#4caf50" stroke-width="4" stroke-linecap="round"/>
</svg>"""


def icon_success():
    """أيقونة نجاح/تم"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <polyline points="8 12 11 15 16 9"/>
</svg>"""


def icon_warning():
    """أيقونة تحذير"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
  <line x1="12" y1="9" x2="12" y2="13"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>"""


# ==================== أيقونات إضافية ====================

def icon_settings():
    """أيقونة الإعدادات"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="3"/>
  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
</svg>"""


def icon_user():
    """أيقونة المستخدم"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
  <circle cx="12" cy="7" r="4"/>
</svg>"""


def icon_home():
    """أيقونة المنزل/الرئيسية"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
  <polyline points="9 22 9 12 15 12 15 22"/>
</svg>"""


def icon_filter():
    """أيقونة الفلتر"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
</svg>"""


def icon_clock():
    """أيقونة الساعة/السجل"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <polyline points="12 6 12 12 16 14"/>
</svg>"""


def icon_star():
    """أيقونة النجمة/المفضلة"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
</svg>"""


def icon_download():
    """أيقونة التحميل"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="7 10 12 15 17 10"/>
  <line x1="12" y1="15" x2="12" y2="3"/>
</svg>"""


def icon_share():
    """أيقونة المشاركة"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="18" cy="5" r="3"/>
  <circle cx="6" cy="12" r="3"/>
  <circle cx="18" cy="19" r="3"/>
  <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
  <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
</svg>"""


# ==================== قائمة جميع الأيقونات ====================

def get_all_icons():
    """إرجاع قاموس بجميع الأيقونات"""
    return {
        # أيقونات البحث والواجهة
        'search': icon_search(),
        'arrow': icon_arrow(),
        'arrow-green': icon_arrow_green(),
        'clear': icon_clear(),
        'external': icon_external(),
        'keyboard': icon_keyboard(),
        
        # أيقونات المميزات
        'shield': icon_shield_enhanced(),
        'globe': icon_globe(),
        'lightning': icon_lightning(),
        
        # أيقونات الوسائط (جديدة)
        'image': icon_image(),
        'video': icon_video(),
        'news': icon_news(),
        'play': icon_play(),
        'play-green': icon_play_green(),
        
        # أيقونات الشعار
        'logo-t': icon_logo_t(),
        'logo-th': icon_logo_th(),
        'logo-small-t': icon_logo_small_t(),
        'logo-small-th': icon_logo_small_th(),
        
        # أيقونات الحالة
        'sad-face': icon_sad_face(),
        'loading': icon_loading(),
        'success': icon_success(),
        'warning': icon_warning(),
        
        # أيقونات إضافية
        'settings': icon_settings(),
        'user': icon_user(),
        'home': icon_home(),
        'filter': icon_filter(),
        'clock': icon_clock(),
        'star': icon_star(),
        'download': icon_download(),
        'share': icon_share(),
    }


# ==================== التنفيذ الرئيسي ====================

def main():
    """الدالة الرئيسية لإنشاء جميع الأيقونات"""
    print("=" * 60)
    print("  Thender Icon Generator v2.0")
    print(" 🚀 Generating all SVG icons...")
    print("=" * 60)
    
    # إنشاء المجلد
    ensure_dir()
    
    # الحصول على جميع الأيقونات
    icons = get_all_icons()
    
    print(f"\n جاري إنشاء {len(icons)} أيقونة...\n")
    
    # إنشاء كل أيقونة
    for name, content in icons.items():
        save_svg(name, content)
    
    # ملخص
    print(f"\n{'=' * 60}")
    print(f"✅ تم إنشاء {len(icons)} أيقونة بنجاح!")
    print(f"📁 الموقع: {ICONS_DIR}")
    print(f"\n📋 الأيقونات المُنشأة:")
    print(f"   • البحث والواجهة: search, arrow, clear, external, keyboard")
    print(f"   • المميزات: shield (مع T), globe, lightning")
    print(f"   • الوسائط: image, video, news, play")
    print(f"   • الشعار: logo-t, logo-th, logo-small-t, logo-small-th")
    print(f"   • الحالة: sad-face, loading, success, warning")
    print(f"   • إضافية: settings, user, home, filter, clock, star, download, share")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()