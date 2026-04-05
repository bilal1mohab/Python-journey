import customtkinter as ctk
import re
from tkinter import messagebox, filedialog

def render(logs, success_percent, title="Bilal Dashboard"):
    # 1. إعداد النافذة
    app = ctk.CTk()
    app.title(title)
    app.geometry("750x600")
    app.attributes("-alpha", 0.90)  # سر تأثير الإزاز
    ctk.set_appearance_mode("dark")

    log_font = ctk.CTkFont(family="Consolas", size=14)

    def export_to_file():
        # تنظيف النص من أكواد الألوان قبل الحفظ
        clean_text = clean_ansi("\n".join(logs))
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(clean_text)
            messagebox.showinfo("Export Success", f"Logs saved to:\n{file_path}")

    def clean_ansi(text):
        modified = text.replace("μ","u")
        return re.sub(r'\033\[\d+m', '', modified)


    txt = ctk.CTkTextbox(app,
                         width=650,
                         height=350,
                         font=log_font,
                         border_width=2,
                         border_color="#333333",
                         wrap="none",
                         activate_scrollbars=True)
    txt.pack(pady=10, padx=10, fill="both", expand=True)
    txt.bind("<Control-c>", lambda e: app.clipboard_append(txt.get("sel.first", "sel.last")))

    tags = {
        "\033[32m": ("gr", ["#228B22", "#32CD32"]),  # ForestGreen / LimeGreen
        "\033[31m": ("rd", ["#B22222", "#FF4500"]),  # FireBrick / OrangeRed
        "\033[34m": ("bl", ["#104E8B", "#1e90ff"]),  # DeepSkyBlue / DodgerBlue
        "\033[33m": ("yl", ["#8B8B00", "#FFFF00"]),  # DarkYellow / Yellow
        "\033[0m": ("bk", ["#000000", "#FFFFFF"])  # Black / White
    }

    def apply_tags(mode=None):
        if not mode: mode = ctk.get_appearance_mode().lower()
        idx = 1 if mode == "dark" else 0

        for code, (tag_name, colors) in tags.items():
            txt.tag_config(tag_name, foreground=colors[idx])

    def toggle_mode():
        mode = "light" if ctk.get_appearance_mode().lower() == "dark" else "dark"
        ctk.set_appearance_mode(mode)
        apply_tags(mode)

    apply_tags()

    # --- لوحة التحكم (Control Panel) ---
    control_frame = ctk.CTkFrame(app, fg_color="transparent")
    control_frame.pack(side="bottom", pady=10, padx=20, fill="x")

    # 2. العنوان العلوي
    title_label = ctk.CTkLabel(control_frame,
                               text=title,
                               font=("Segoe UI", 22, "bold"),
                               text_color="#1e90ff")
    title_label.pack(side="right", padx=5)
    # زرار المود (Dark/Light)
    mode_btn = ctk.CTkButton(control_frame, text="🌓 Toggle Mode", command=toggle_mode, width=120)
    mode_btn.pack(side="left", padx=5)

    # زرار الـ Export
    export_btn = ctk.CTkButton(control_frame, text="💾 Export Logs", command=export_to_file, fg_color="#2c3e50",
                               width=120)
    export_btn.pack(side="left", padx=5)

    # زرار الـ OK (Close)
    ok_btn = ctk.CTkButton(control_frame, text="✅ OK / Close", command=app.destroy, fg_color="#27ae60",
                           hover_color="#2ecc71", width=120)
    ok_btn.pack(side="left", padx=5)

    # حركة صايعة: تقطيع النص بناءً على الأكواد اللي بلال مستخدمها
    for line in logs:
        parts = re.split(r'(\033\[\d+m)', line)
        current_tag = "bk"
        for part in parts:
            if part in tags:
                current_tag = tags[part][0]
            else:
                txt.insert("end", part, current_tag)
        txt.insert("end", "\n")

    # 4. شريط النسبة المئوية (Progress Bar) المتفاعل
    progress = ctk.CTkProgressBar(app, width=500, height=15)
    progress.set(success_percent / 100)

    # لون البار يتغير حسب النتيجة (أخضر للنجاح الكامل، برتقالي لو فيه فشل)
    bar_color = "#32CD32" if success_percent == 100 else "#FF4500"
    progress.configure(progress_color="#32CD32", fg_color="#FF4500")

    progress.pack(pady=15, padx=15, fill="x")

    # --- جوه دالة render وبعد تعريف الـ Progress Bar ---
    my_font = ctk.CTkFont(family="Consolas", size=22)
    # فريم (Container) شايل نصوص النسب المئوية عشان نتحكم في مكانها
    percent_frame = ctk.CTkFrame(app, fg_color="transparent")
    percent_frame.pack(pady=5, padx=20, fill="x")

    # تجهيز النسب
    fail_percent = round(100 - success_percent,1)

    # --- Logic توزيع النصوص (زي التيرمينال بالظبط) ---
    if success_percent == 100:
        # نص واحد أخضر في النص
        lbl = ctk.CTkLabel(percent_frame, text=f"{success_percent}%",
                           text_color="#32CD32", font=my_font)
        lbl.pack(expand=True)  # expand=True هي اللي بتخليه في النص

    elif fail_percent == 100:
        # نص واحد أحمر في النص
        lbl = ctk.CTkLabel(percent_frame, text=f"{fail_percent}%",
                           text_color="#FF4500", font=my_font)
        lbl.pack(expand=True)

    else:
        # نسبة النجاح على الشمال (الأخضر)
        left_lbl = ctk.CTkLabel(percent_frame, text=f"{success_percent}%",
                                text_color="#32CD32", font=my_font)
        left_lbl.pack(side="left")

        # نسبة الفشل على اليمين (الأحمر)
        right_lbl = ctk.CTkLabel(percent_frame, text=f"{fail_percent}%",
                                 text_color="#FF4500", font=my_font)
        right_lbl.pack(side="right")

        # 2. دالة الحساب "المنفصلة" عشان نستخدمها في أي وقت (Logic Only)
        def refresh_font_size():
            # بنجيب العرض الحقيقي من الويندوز دلوقتي
            app.update_idletasks()  # سطر سحري بيخلي الويندوز يحسب مقاساته فوراً قبل ما يكمل
            width = app.winfo_width()

            if width > 1200:
                new_size = 20
            elif width > 800:
                new_size = 16
            else:
                new_size = 14

            log_font.configure(size=new_size)
            txt.configure(font=log_font)

        # 3. معالجة الـ Initial State (قبل ما الـ Mainloop يبدأ)
        # بنناديها "يدوي" عشان أول ما الويندوز يظهر ياخد المقاس الصح فوراً
        refresh_font_size()

        # 4. الـ Event يشتغل عادي بعد كدة لأي تغيير مستقبلي
        def update_font_size(event):
            # بنحط الفلتر اللي يضمن إن التغيير من النافذة الأم فقط
            if event.widget == app:
                refresh_font_size()
    # ربط الويندوز بالدالة دي (تتنفذ مع كل تغيير حجم)
    app.bind("<Configure>", update_font_size)
    app.mainloop()