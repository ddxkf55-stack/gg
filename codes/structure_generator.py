import os
import sys
import re
import json
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# إعدادات المظهر الأساسية
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- القوالب الجاهزة (1. Preset Templates) ---
TEMPLATES = {
    "مخصص (Custom)": "",
    "Express Node.js": """game-hub/
├── package.json
├── server.js
├── .env
├── .gitignore
├── public/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── README.md""",
    "React SPA": """my-react-app/
├── package.json
├── README.md
├── .gitignore
├── public/
│   ├── index.html
│   └── favicon.ico
└── src/
    ├── App.js
    ├── index.js
    └── components/
        └── Header.js""",
    "Django Web": """my_django_project/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── my_django_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main_app/
    ├── __init__.py
    ├── views.py
    └── models.py""",
    "Flutter App": """flutter_app/
├── pubspec.yaml
├── README.md
├── .gitignore
├── lib/
│   ├── main.dart
│   └── screens/
│       └── home_screen.dart
└── assets/
    └── images/"""
}

# --- المحتوى الابتدائي التلقائي (2. File Boilerplates) ---
BOILERPLATES = {
    "package.json": '{\n  "name": "my-app",\n  "version": "1.0.0",\n  "main": "index.js",\n  "scripts": {\n    "start": "node index.js"\n  }\n}',
    ".gitignore": "node_modules/\n.env\n*.log\n.DS_Store\ndist/\nbuild/\n",
    "README.md": "# Project Title\n\nGenerated automatically using Smart Directory Structure Generator.\n",
    "index.html": '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <title>App</title>\n</head>\n<body>\n  <h1>Hello World</h1>\n</body>\n</html>',
    "server.js": 'const express = require("express");\nconst app = express();\nconst PORT = process.env.PORT || 3000;\n\napp.listen(PORT, () => console.log(`Server running on port ${PORT}`));',
    ".env": "PORT=3000\nNODE_ENV=development\n"
}

class UltimateTreeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("المولد الذكي لهيكلية المشاريع | Ultimate Tree Generator")
        self.geometry("900x750")
        self.minsize(800, 600)

        # التخزين الداخلي والميزات (5. Undo History & 10. Saved Presets)
        self.last_created_paths = []
        self.history = []

        self.create_widgets()

    def create_widgets(self):
        # 9. Theme Switcher + Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=15, pady=(15, 5))

        self.title_label = ctk.CTkLabel(self.header_frame, text="⚡ Ultimate Structure Generator", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(side="left", padx=15, pady=10)

        self.theme_switch = ctk.CTkSwitch(self.header_frame, text="المظهر الداكن", command=self.toggle_theme)
        self.theme_switch.pack(side="right", padx=15)
        self.theme_switch.select()

        # Tabview Control
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=5)

        self.tab_generator = self.tabview.add("🛠️ إنشاء هيكلة")
        self.tab_reverse = self.tabview.add("🔄 تحويل مجلد إلى نص")
        self.tab_settings = self.tabview.add("⚙️ الإعدادات والاستثناءات")

        # --- TAB 1: GENERATOR ---
        self.setup_generator_tab()

        # --- TAB 2: REVERSE PARSER (8. Folder-to-Text) ---
        self.setup_reverse_tab()

        # --- TAB 3: SETTINGS & IGNORE (12. Ignore Rules) ---
        self.setup_settings_tab()

    def setup_generator_tab(self):
        # Top Path Selection & Presets
        controls_frame = ctk.CTkFrame(self.tab_generator)
        controls_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(controls_frame, text="مسار العمل:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.target_dir_entry = ctk.CTkEntry(controls_frame, placeholder_text="اختر المجلد Target Directory")
        self.target_dir_entry.insert(0, os.getcwd())
        self.target_dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        btn_browse = ctk.CTkButton(controls_frame, text="استعراض", width=80, command=self.browse_target)
        btn_browse.grid(row=0, column=2, padx=5, pady=5)

        # 1. Preset Templates Dropdown
        ctk.CTkLabel(controls_frame, text="القوالب الجاهزة:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.preset_option = ctk.CTkOptionMenu(controls_frame, values=list(TEMPLATES.keys()), command=self.apply_preset)
        self.preset_option.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        controls_frame.grid_columnconfigure(1, weight=1)

        # Main Text Editor (7. Drag & Drop Notice included)
        editor_frame = ctk.CTkFrame(self.tab_generator)
        editor_frame.pack(fill="both", expand=True, padx=10, pady=5)

        lbl_edit = ctk.CTkLabel(editor_frame, text="شجرة الملفات (قم باللصق هنا أو استورد ملف .txt):", font=ctk.CTkFont(size=12))
        lbl_edit.pack(anchor="w", padx=10, pady=(5, 0))

        self.editor = ctk.CTkTextbox(editor_frame, font=ctk.CTkFont(family="Consolas", size=13), wrap="none")
        self.editor.pack(fill="both", expand=True, padx=10, pady=5)
        self.editor.insert("1.0", TEMPLATES["Express Node.js"])

        # Options & Checkboxes
        opts_frame = ctk.CTkFrame(self.tab_generator, fg_color="transparent")
        opts_frame.pack(fill="x", padx=10, pady=5)

        # 3. Dry-Run Mode
        self.dry_run_var = ctk.BooleanVar(value=False)
        self.chk_dry_run = ctk.CTkCheckBox(opts_frame, text="اختبار فرضي بدون إنشاء (Dry-Run)", variable=self.dry_run_var)
        self.chk_dry_run.pack(side="left", padx=10)

        # 2. Boilerplates Auto-fill
        self.boilerplate_var = ctk.BooleanVar(value=True)
        self.chk_boilerplate = ctk.CTkCheckBox(opts_frame, text="تعبئة الملفات بكود افتراضي", variable=self.boilerplate_var)
        self.chk_boilerplate.pack(side="left", padx=10)

        # Import Text Button
        btn_import = ctk.CTkButton(opts_frame, text="📄 استيراد TXT", width=100, fg_color="#4A5568", command=self.import_file)
        btn_import.pack(side="right", padx=5)

        # Action Buttons Bottom
        actions_frame = ctk.CTkFrame(self.tab_generator, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=10)

        btn_run = ctk.CTkButton(actions_frame, text="🚀 إنشاء الهيكلة", font=ctk.CTkFont(size=14, weight="bold"), height=40, command=self.generate_tree)
        btn_run.pack(side="left", fill="x", expand=True, padx=5)

        # 5. Undo Creation Button
        self.btn_undo = ctk.CTkButton(actions_frame, text="↩️ تراجع عن الأخير", fg_color="#E53E3E", hover_color="#C53030", height=40, command=self.undo_last_creation)
        self.btn_undo.pack(side="left", padx=5)

        # 6. Open in VS Code & Explorer
        btn_vscode = ctk.CTkButton(actions_frame, text="💙 فتح في VS Code", fg_color="#2B6CB0", height=40, command=self.open_in_vscode)
        btn_vscode.pack(side="right", padx=5)

        btn_explorer = ctk.CTkButton(actions_frame, text="📁 فتح المجلد", fg_color="#2D3748", height=40, command=self.open_in_explorer)
        btn_explorer.pack(side="right", padx=5)

    def setup_reverse_tab(self):
        # 8. Folder-to-Text Reverse Parser
        frame = ctk.CTkFrame(self.tab_reverse)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        lbl = ctk.CTkLabel(frame, text="اختر مجلداً من جهازك لتحويله إلى نص شجري قابل للنخ والتحرير:")
        lbl.pack(anchor="w", padx=10, pady=10)

        top_rev = ctk.CTkFrame(frame, fg_color="transparent")
        top_rev.pack(fill="x", padx=10, pady=5)

        self.rev_path_entry = ctk.CTkEntry(top_rev, placeholder_text="مسار المجلد لتحليله...")
        self.rev_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_rev_browse = ctk.CTkButton(top_rev, text="استعراض", command=self.browse_reverse_target)
        btn_rev_browse.pack(side="left", padx=5)

        btn_parse = ctk.CTkButton(top_rev, text="🔍 تحليل وتوليد النص", fg_color="#38A169", command=self.parse_folder_to_text)
        btn_parse.pack(side="left", padx=5)

        self.rev_output = ctk.CTkTextbox(frame, font=ctk.CTkFont(family="Consolas", size=13), wrap="none")
        self.rev_output.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_settings_tab(self):
        # 12. Ignore Rules
        frame = ctk.CTkFrame(self.tab_settings)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_ignore = ctk.CTkLabel(frame, text="قائمة التخطي والاستثناء (فصل بينها بفارزة ,):", font=ctk.CTkFont(size=13, weight="bold"))
        lbl_ignore.pack(anchor="w", padx=10, pady=(10, 2))

        self.ignore_entry = ctk.CTkEntry(frame, placeholder_text="مثال: .git, node_modules, .DS_Store, __pycache__")
        self.ignore_entry.insert(0, ".git, node_modules, .DS_Store, __pycache__, .venv")
        self.ignore_entry.pack(fill="x", padx=10, pady=5)

        lbl_info = ctk.CTkLabel(frame, text="* الميزات المفعلة تلعقائياً:\n 11. Path Sanitization: تنظيف أسماء الملفات من الرموز الممنوعة في الويندوز والأنظمة تلقائياً.\n 4. Smart Hierarchy: التعرف الذكي على الرموز و العمق.\n 5. Full Undo Log: حفظ سجل للإنشاء لإمكانية التراجع الفوري.", justify="left")
        lbl_info.pack(anchor="w", padx=10, pady=20)

    # --- FUNCTIONS & LOGIC ---

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def browse_target(self):
        d = filedialog.askdirectory()
        if d:
            self.target_dir_entry.delete(0, "end")
            self.target_dir_entry.insert(0, d)

    def browse_reverse_target(self):
        d = filedialog.askdirectory()
        if d:
            self.rev_path_entry.delete(0, "end")
            self.rev_path_entry.insert(0, d)

    def apply_preset(self, choice):
        if choice in TEMPLATES and TEMPLATES[choice]:
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", TEMPLATES[choice])

    def import_file(self):
        f = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if f:
            with open(f, "r", encoding="utf-8") as file:
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", file.read())

    # 11. Path Sanitization
    def sanitize_name(self, name):
        # حذف الأشكال غير المسموحة في أسماء الملفات
        clean = re.sub(r'[\\/:*?"<>|]', '', name).strip()
        return clean if clean else "unnamed_item"

    def parse_depth(self, line):
        match = re.search(r'[^\s│├└─\-]', line)
        if not match:
            return None, None

        start_idx = match.start()
        clean_name = line[start_idx:].strip()
        prefix = line[:start_idx]

        depth = prefix.count('│') + prefix.count('├') + prefix.count('└')
        if depth == 0:
            leading_spaces = len(prefix.replace('\t', '    '))
            depth = leading_spaces // 4

        return depth, clean_name

    # Core Generator Function
    def generate_tree(self):
        raw_text = self.editor.get("1.0", "end").strip()
        base_path = self.target_dir_entry.get().strip()

        if not raw_text or not base_path:
            messagebox.showwarning("تنبيه", "تأكد من اختيار المجلد وإدخال نص الهيكلة!")
            return

        ignore_list = [x.strip() for x in self.ignore_entry.get().split(',') if x.strip()]
        lines = raw_text.splitlines()

        parsed_items = []
        for line in lines:
            if not line.strip():
                continue
            depth, name = self.parse_depth(line)
            if name:
                # Check ignore list
                if any(ign in name for ign in ignore_list):
                    continue
                parsed_items.append({'depth': depth, 'name': name})

        if not parsed_items:
            messagebox.showwarning("تنبيه", "لم يتم العثور على أسطر صالحة!")
            return

        is_dry_run = self.dry_run_var.get()
        add_boilerplate = self.boilerplate_var.get()

        created_files = []
        created_dirs = []
        stack = [(-1, base_path)]

        for idx, item in enumerate(parsed_items):
            depth = item['depth']
            raw_name = item['name']

            is_dir = raw_name.endswith('/')
            if not is_dir and idx < len(parsed_items) - 1:
                if parsed_items[idx + 1]['depth'] > depth:
                    is_dir = True

            clean_name = self.sanitize_name(raw_name.rstrip('/'))

            while stack and stack[-1][0] >= depth:
                stack.pop()

            parent_path = stack[-1][1]
            target_path = os.path.join(parent_path, clean_name)

            if is_dir:
                if not is_dry_run:
                    os.makedirs(target_path, exist_ok=True)
                created_dirs.append(target_path)
                stack.append((depth, target_path))
            else:
                if not is_dry_run:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'w', encoding='utf-8') as f:
                        # 2. Add Boilerplate if enabled
                        if add_boilerplate and clean_name in BOILERPLATES:
                            f.write(BOILERPLATES[clean_name])
                created_files.append(target_path)

        # 5. Log for Undo
        if not is_dry_run:
            self.last_created_paths = created_files + created_dirs

        # Dry Run vs Actual Report
        msg_title = "💡 نتيجة الاختبار الفرضي (Dry Run)" if is_dry_run else "🎉 تمت العملية بنجاح"
        msg_body = f"📁 المجلدات: {len(created_dirs)}\n📄 الملفات: {len(created_files)}\n📍 المسار: {base_path}"
        if is_dry_run:
            msg_body += "\n\n(لم يتم إنشاء أي ملفات حقيقية على القرص)"

        messagebox.showinfo(msg_title, msg_body)

    # 5. Undo Logic
    def undo_last_creation(self):
        if not self.last_created_paths:
            messagebox.showinfo("تنبيه", "لا توجد عمليات إنشاء سابقة للتراجع عنها.")
            return

        deleted_count = 0
        for path in reversed(self.last_created_paths):
            if os.path.isfile(path):
                os.remove(path)
                deleted_count += 1
            elif os.path.isdir(path):
                try:
                    os.rmdir(path)
                    deleted_count += 1
                except OSError:
                    pass  # المجلد ليس فارغاً

        self.last_created_paths = []
        messagebox.showinfo("تم التراجع", f"تم مسح {deleted_count} عنصر بنجاح!")

    # 6. Open in VS Code
    def open_in_vscode(self):
        target = self.target_dir_entry.get().strip()
        if os.path.exists(target):
            try:
                subprocess.run(["code", target], shell=True)
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر فتح VS Code:\n{str(e)}")
        else:
            messagebox.showwarning("خطأ", "المجلد غير موجود!")

    # 6. Open File Explorer
    def open_in_explorer(self):
        target = self.target_dir_entry.get().strip()
        if os.path.exists(target):
            if sys.platform == "win32":
                os.startfile(target)
            elif sys.platform == "darwin":
                subprocess.run(["open", target])
            else:
                subprocess.run(["xdg-open", target])
        else:
            messagebox.showwarning("خطأ", "المجلد غير موجود!")

    # 8. Folder to Text Parser Implementation
    def parse_folder_to_text(self):
        path = self.rev_path_entry.get().strip()
        if not os.path.exists(path):
            messagebox.showerror("خطأ", "المجلد المحدد غير موجود!")
            return

        ignore_list = [x.strip() for x in self.ignore_entry.get().split(',') if x.strip()]
        lines = [os.path.basename(path) + "/"]

        def build_tree(dir_path, prefix=""):
            try:
                entries = sorted(os.listdir(dir_path))
            except PermissionError:
                return

            entries = [e for e in entries if e not in ignore_list]
            count = len(entries)

            for i, entry in enumerate(entries):
                full_path = os.path.join(dir_path, entry)
                is_last = (i == count - 1)
                connector = "└── " if is_last else "├── "

                if os.path.isdir(full_path):
                    lines.append(f"{prefix}{connector}{entry}/")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    build_tree(full_path, new_prefix)
                else:
                    lines.append(f"{prefix}{connector}{entry}")

        build_tree(path)
        self.rev_output.delete("1.0", "end")
        self.rev_output.insert("1.0", "\n".join(lines))


if __name__ == "__main__":
    app = UltimateTreeApp()
    app.mainloop()