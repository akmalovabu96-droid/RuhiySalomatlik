import json
import os
import tkinter as tk
from tkinter import messagebox
import random

# --- OFFLAYN BAZANING MA'LUMOTLARI ---
DB_FILE = "shield_stats.json"

def load_stats():
    """Mahalliy fayldan qalqon nechchi marta ishlatilganini saqlaydi."""
    if not os.path.exists(DB_FILE):
        return {"shield_raised_count": 0}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return {"shield_raised_count": 0}

def save_stats(data):
    """Yangilangan ko'rsatkichlarni qattiq diskka saqlaydi."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Ko'rsatkichlarni saqlashdagi muammo: {e}")

# --- THE CURATED COMFORT DATASET ---
SHIELD_DATA = [
    {
        "arabic": "إِنَّا نَحْنُ نَزَّلْنَا عَلَيْكَ الْقُرْآنَ تَنزِيلًا",
        "text": "“Albatta, Biz senga Qur'onni bo'lak-bo'lak qilib (ma'lum muddatlarda) tushirdik.”",
        "source": "Qur'an 76:23 (Surah Al-Insan)",
        "lesson": "Hayotni bosqichma-bosqich qabul qiling. Shifo va yengillik asta-sekinlik bilan keladi. Butun dunyo tashvishini birdaniga yelkangizga olishingiz shart emas."
    },
    {
        "arabic": "وَأَنَّ سَعۡیَهُۥ سَوۡفَ یُرَىٰ",
        "text": "“Va, albatta, u(inson)ning sa'y-harakati tezda ko'rinur.”",
        "source": "Quran 53:40 (Surah An-Najm)",
        "lesson": "Alloh sizni natijalaringizga qarab emas, harakatingiz va samimiyatingizga qarab baholaydi. Yashirincha ko‘rsatgan har zarracha matonatingiz to‘la-to‘kis ko‘rib turiladi va qadrlanadi."
    },
    {
        "arabic": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ",
        "text": "“Shak-shubhasizki, Allohni zikr qilish bilan qalblar orom topadi.”",
        "source": "Quran 13:28 (Surah Ar-Ra'd)",
        "lesson": "Jismoniy qulayliklar (taom, boshpana) tanani yashnatadi, biroq och qolgan qalbni faqat sokinlik va iliqlik to‘ydira oladi. O‘z qalbingizga yuzlaning."
    },
    {
        "arabic": "وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ ۖ أُجِيبُ دَعْوَةَ الدَّاعِ إِذَا دَعَانِ",
        "text": "“Ey Rasulim, bandalarim sizdan Men haqimda so‘rasalar shuni bilsinlarki, albatta, Men ularga juda yaqinman. Menga duo qilgan payt, duo qiluvchining duosini ijobat qilaman.”",
        "source": "Quran 2:186 (Surah Al-Baqarah) ",
        "lesson": "Har qachon o‘zingizni butkul yolg‘iz his qilsangiz, iltimos, aynan shu oyatni yodga oling. Zero, sizning ma’naviy holatingiz Alloh nazdida muhim ahamiyatga egadir."
    },
    {
        "arabic": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ",
        "text": "“Allohning mukammal kalimalari bilan U yaratgan narsalarning yomonligidan panoh so‘rayman.”",
        "source": "Prophetic Supplication (Hisn al-Muslim 97)",
        "lesson": "Payg‘ambarimiz ruhiy qiyinchilikni tabiiy hol deb bilganlar. Xavotir hissi yoki o‘zini chorasiz sezish noshukurlik yoxud zaiflik belgisi emas, balki insonga xos ojizlikdir. Buni inobatga olish esa juda muhim."
    },
    {
        "arabic": "اللَّهُمَّ رَحْمَتَكَ أَرْجُو فَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ وَأَصْلِحْ لِي شَأْنِي كُلَّهُ لَا إِلَهَ إِلَّا أَنْتَ",
        "text": "“Allohim! Sening rahmatingdan umidvorman. Meni ko‘z ochib yumgunchalik muddatga ham o‘z nafsimga tashlab qo‘yma. Mening barcha ishlarimni o‘ngla. Sendan o‘zga iloh yo‘qdir.”",
        "source": "Prophetic Supplication (Sunan Abi Dawud)",
        "lesson": "Ushbu duoning fazilati shundaki, inson o‘z ojizligini bo‘yniga olib, butun borligini Allohga topshirishini anglatadi. Bu esa qalbga tinchlik yetkazuvchi muhim omillardan biridir."
    },
    {
        "arabic": "أَنِّي مَسَّنِيَ الضُّرُّ وَأَنْتَ أَرْحَمُ الرَّاحِمِينَ",
        "text": "“(Robbim), menga musibat yetdi, va O‘zing rahmlilarning eng rahmlisisan!”",
        "source": "Supplication of the Prophet Ayyub a.s | Quran 21:83 (Surah Al-Anbiya)",
        "lesson": "Sabr - bu shunchaki chidash emas, balki boshga tushgan sinovni Allohning taqdiri deb bilib, tushkunlikka tushmaslik va Uning rahmatidan umid uzmaslikdir. Musibatlar yuki haddan ziyod og‘irlashdi deb o‘ylagan paytingizda, Allohga chin qalbdan iltijo qiling."
    },
    {
        "arabic": "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
        "text": "“Allohdan o'zga quvvat va kuch egasi yo'qdir.”",
        "source": "Prophetic Supplications (Sahih al-Bukhari)",
        "lesson": "Payg‘ambarimiz (Solallohu alayhi vassallam) Abu Muso al-Ash’ariyga: 'Senga jannat xazinalaridan birini aytaymi? U – 'Lā havla va lā quvvata illā billāh' dir', deganlar (Sahihi Buxoriy)."
    },
    {
        "arabic": "يَا حَنْظَلَةُ سَاعَةً وَسَاعَةً",
        "text": "“Ey Hanzalah, bir soat unday, bir soat bunday.”",
        "source": "Prophetic Hadith (Sahih Muslim)",
        "lesson": "Yuragingiz robot emas. Uning gohida ezilishi, gohida hissizlanib qolishi tabiiy. O‘zingizga shunchaki dam olish va nafas rostlash uchun izn bering."
    },
    {
        "arabic": "مَا وَدَّعَكَ رَبُّكَ وَمَا قَلَىٰ",
        "text": "“Robbing sendan voz kechgani ham yoʻq, g‘azab ham qilgani yo‘q!”",
        "source": "Quran 93:3 (Surah Ad-Duha)",
        "lesson": "O‘zingizni chorasiz, duolaringiz ijobat bo‘lmayotgandek yoki hayotda qiyinchiliklar ichingizda qolgandek his qilsangiz, bilishingiz kerakki — Alloh sizni tark etgani yo‘q. Payg'ambarimizga vahiy to'xtab qolgan paytda taskin bergan Alloh, sizga taskin beradigan ham Alloh bo'ladi."
    },
    {
        "arabic": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا إِنَّ مَعَ الْعُسْرِ يُسْرًا",
        "text": "“Bas, albatta, har qiyinchilik bilan osonchilik bordir. Albatta, har bir qiyinchilik bilan osonchilik bordir.”",
        "source": "Quran 94:5-6 (Surah Ash-Sharh)",
        "lesson": "Yengillik qiyinchilikdan KEYIN kelmaydi, u aynan qiyinchilikning ICHIGA joylangan bo‘ladi. Og‘ir kunlarda yashiringan ne’matlarni sinchiklab izlash kerak. Har qanday vaziyatda qadrli narsalar kam emas."
    },
    {
        "arabic": "إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنْكَرِ",
        "text": "“Albatta, namoz fahsh va yomonlikdan qaytaradi.”",
        "source": "Quran 29:45 (Surah Al-Ankabut)",
        "lesson": "Namozini shunchaki o'qimaydigan, balki TO'KIS ado etadigan insonning hayoti ham, ishlari ham tartibga tushadi."
    },
    {
        "arabic": "اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ",
        "text": "“Allohim! Sening zikringni qilishda, Senga shukr keltirishda va Senga go‘zal suratda ibodat qilishda menga yordam bergin.”",
        "source": "Prophetic Advice to Mu'adh (Sunan Abi Dawud)",
        "lesson": "Ruhiy lazzatni o‘z kuchingiz bilan topishingiz shart emas. Mutlaq hissiy kamtarlik bilan Allohdan duolaringizda yordam so‘rang."
    },
    {
        "arabic": "يَا ابْنَ آدَمَ، إِنَّكَ مَا دَعَوْتَنِي وَرَجَوْتَنِي غَفَرْتُ لَكَ عَلَى مَا كَانَ فِيكَ وَلَا أُبَالِيَ",
        "text": "“Ey Odam bolasi! Modomiki sen Menga duo qilib, Mendan umidvor bo‘lar ekansan, sendan nima sodir bo‘lganidan qat’iy nazar, seni kechiraman va bu(qilgan ishing)nga parvo qilmayman.”",
        "source": "34 Hadith (40 Hadith Qudsi)",
        "lesson": "Bir qarang. “Va bunga parvo qilmayman” iborasi biror gunohning Alloh kechirib yuborishi uchun og‘ir yoki ulkan bo‘lmasligini hamda bu Unga zarracha ham malol kelmasligini ta’kidlaydi. Umidsizlikka tushmang!"
    },
    {
        "arabic": "يَا ابْنَ آدَمَ، لَوْ بَلَغَتْ ذُنُوبُكَ عَنَانَ السَّمَاءِ ثُمَّ اسْتَغْفَرْتَنِي غَفَرْتُ لَكَ",
        "text": "“Ey Odam bolasi, agar gunohlaring osmon barobariga (bulutlarigacha) yetsa-yu, so‘ngra Mendan mag‘firat so‘rasang, Men seni kechiraman.”",
        "source": "34 Hadith (40 Hadith Qudsi)",
        "lesson": "Bu holat mukammallikka intilishdek ezuvchi yukni yelkangizdan oladi. Alloh sizning inson ekaningizni, kurashlarga to'la hayotni kechirishingizni biladi va sizga nisbatan doimiy munosabati aslida rahmah(aql bovar qilmaydigan marhamat) ekanini ochiq-oydin bayon qiladi."
    },
    {
        "arabic": "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا",
        "text": "“Alloh hech bir jonga uning toqatidan tashqari narsani taklif etmas (yuklamas).”",
        "source": "Quran 2:286 (Surah Al-Baqarah)",
        "lesson": "Siz o‘ylaganingizdan ancha kuchliroqsiz. Agar hozirda bir sinovga yuzma-yuz kelayotgan bo‘lsangiz, demak, ichingizda undan omon qolish va yengib o‘tish uchun yetarli kuch mavjud!"
    },
    {
        "arabic": "رَبَّنَا آتِنَا مِن لَّدُنكَ رَحْمَةً وَهَيِّئْ لَنَا مِنْ أَمْرِنَا رَشَدًا",
        "text": "“Ey Robbimiz, bizga O‘z huzuringdan rahmat ato etgin va ishimizni to‘g‘ri yo‘lga solishni (najot berishni) oson qilgin!”",
        "source": "Quran 18:10 (Surah Al-Kahf)",
        "lesson": "Fitna zulmatiga g‘arq bo‘lgan yosh yigitlarning duosi. Muhit toksik kayfiyatida bo'lganda, xayolan mana shu qalqon ortiga chekining. Ayniqsa yoshlar ham bunga loyiqdir."
    }
]

is_dark_mode = False
active_card = None


# --- INTERFACE FUNCTIONS ---

def hold_the_shield():

    global active_card

    # Agar ro'yxatda faqat bittasi bo'lsa, uni shunchaki chiqaramiz (tuganmas tsikldan himoya)
    if len(SHIELD_DATA) <= 1:
        active_card = SHIELD_DATA[0]
    else:
        # Eskisi bilan to'g'ri kelmagunicha yangisini chiqaraveramiz
        new_card = random.choice(SHIELD_DATA)
        while new_card == active_card:
            new_card = random.choice(SHIELD_DATA)
        active_card = new_card

    # Interfeysni yangilaymiz
    arabic_text.config(text=active_card["arabic"])
    verse_text.config(text=active_card["text"])
    source_text.config(text=active_card["source"])
    lesson_text.config(text=active_card["lesson"])

    stats_data["shield_raised_count"] += 1
    save_stats(stats_data)
    counter_label.config(text=f"🛡️ QALQON: {stats_data['shield_raised_count']} MARTA KO'TARILGAN")


def copy_to_clipboard():
    """Copies the active card data directly to the operating system clipboard."""
    text_to_copy = f"{arabic_text.cget('text')}\n{verse_text.cget('text')}\n— {source_text.cget('text')}"

    if "Press the button" in text_to_copy:
        text_to_copy = "Qalqon Ilovasi: Ichki sukunatga intiling."

    root.clipboard_clear()
    root.clipboard_append(text_to_copy)
    root.update()
    messagebox.showinfo("Qalqon", "Vaqtinchalik xotiraga nusxalandi!")


def toggle_theme():
    """Dynamically shifts color values across all window widgets."""
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    if is_dark_mode:
        bg = "#121820"
        card = "#1E2631"
        text_main = "#E2E8F0"
        text_muted = "#94A3B8"
        accent_gold = "#F59E0B"  # Slightly brighter gold for dark mode contrast
        btn_bg = "#38BDF8"
        btn_fg = "#0F172A"
        mode_label = "KUNDUZGI REJIM ☀️"
    else:
        bg = "#F0F4F8"
        card = "#FFFFFF"
        text_main = "#1A2E40"
        text_muted = "#526E8C"
        accent_gold = "#D4AF37"
        btn_bg = "#1A2E40"
        btn_fg = "#FFFFFF"
        mode_label = "TUNGI REJIM 🌙"

    root.configure(bg=bg)
    header.configure(bg=bg, fg=text_muted)
    top_bar.configure(bg=bg)
    theme_button.configure(text=mode_label, bg=bg, fg=text_muted, activebackground=bg, activeforeground=text_main)
    control_frame.configure(bg=bg)
    counter_label.configure(bg=bg, fg=text_muted)
    card_frame.configure(bg=card, highlightbackground="#334155" if is_dark_mode else "#E1E8ED")
    arabic_text.configure(bg=card, fg=accent_gold)
    verse_text.configure(bg=card, fg=text_main)
    source_text.configure(bg=card)
    lesson_text.configure(bg=card, fg=text_muted)

    shield_button.configure(bg=btn_bg, fg=btn_fg, activebackground=text_muted)
    copy_button.configure(bg=card, fg=text_muted, activebackground=bg, activeforeground=text_main)

stats_data = load_stats()

# --- USER INTERFACE DESIGN ---
root = tk.Tk()
root.title("Qalqon: Qalb uchun panoh")
root.geometry("700x600")  # Expanded dimensions slightly to comfortably house Arabic lines
root.configure(bg="#F0F4F8")

# 1. Top Utility Header Bar
top_bar = tk.Frame(root, bg="#F0F4F8")
top_bar.pack(fill="x", padx=40, pady=(20, 5))

header = tk.Label(top_bar, text="Q A L Q O N", font=("Segoe UI", 14, "bold"), fg="#526E8C", bg="#F0F4F8")
header.pack(side="left")

theme_button = tk.Button(
    top_bar, text="TUNGI REJIM 🌙", font=("Segoe UI", 9, "bold"), fg="#526E8C", bg="#F0F4F8",
    bd=0, activebackground="#F0F4F8", activeforeground="#1A2E40", cursor="hand2", command=toggle_theme
)
theme_button.pack(side="right")

# 2. Main Center Display Quote Card
card_frame = tk.Frame(root, bg="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#E1E8ED")
card_frame.pack(pady=10, padx=40, fill="both", expand=True)

# Brand New Label: Original Arabic Text (Using a larger font and classical layout styling)
arabic_text = tk.Label(
    card_frame, text="",
    font=("Traditional Arabic", 22, "bold"), fg="#D4AF37", bg="#FFFFFF", wraplength=550, justify="center"
)
arabic_text.pack(pady=(30, 5), padx=30, expand=True)

# English Translation Label
verse_text = tk.Label(
    card_frame, text="“Tinchlik qalqoningizni tortib olish uchun quyidagi tugmani bosing.”",
    font=("Georgia", 14, "italic"), fg="#1A2E40", bg="#FFFFFF", wraplength=550, justify="center"
)
verse_text.pack(pady=(5, 5), padx=30, expand=True)

# Reference Source Label
source_text = tk.Label(card_frame, text="", font=("Segoe UI", 10, "bold"), fg="#526E8C", bg="#FFFFFF")
source_text.pack(pady=(0, 10))

# Contextual Explanation Label
lesson_text = tk.Label(
    card_frame, text="Zulm yoki bohsqa turdagi bosimlarga yuragingiz dosh berolmaydigan paytlarda ushbu ilovadan foydalaning!",
    font=("Segoe UI", 11), fg="#526E8C", bg="#FFFFFF", wraplength=530, justify="center"
)
lesson_text.pack(pady=(0, 30), padx=30, expand=True)

# New Element: Text indicator
counter_label = tk.Label(
    root, text=f"🛡️ QALQON: {stats_data['shield_raised_count']} MARTA KO'TARILGAN",
    font=("Segoe UI", 10, "bold"), fg="#526E8C", bg="#F0F4F8"
)
counter_label.pack(pady=(5, 5))

# 3. Action Layer Controls
control_frame = tk.Frame(root, bg="#F0F4F8")
control_frame.pack(pady=(10, 30))

shield_button = tk.Button(
    control_frame, text="QALQONNI KO'TARISH", font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#1A2E40",
    activebackground="#526E8C", activeforeground="#FFFFFF", bd=0, padx=30, pady=12, cursor="hand2",
    command=hold_the_shield
)
shield_button.pack(side="left", padx=10)

copy_button = tk.Button(
    control_frame, text="📋 NUSXALASH", font=("Segoe UI", 10, "bold"), fg="#526E8C", bg="#FFFFFF",
    activebackground="#F0F4F8", activeforeground="#1A2E40", bd=1, relief="solid", padx=15, pady=10, cursor="hand2",
    command=copy_to_clipboard
)
copy_button.pack(side="left", padx=10)

root.mainloop()
