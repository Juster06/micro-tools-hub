"""Small reusable native Tk controls with batched table rendering."""
import tkinter as tk
from tkinter import ttk

BG, PANEL, BORDER = "#020617", "#0f172a", "#334155"
FG, MUTED, ACCENT = "#e2e8f0", "#94a3b8", "#a5b4fc"


def configure_style(window):
    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure(".", background=BG, foreground=FG, font=("Segoe UI", 10))
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=PANEL)
    style.configure("TLabel", background=BG, foreground=FG)
    style.configure("Muted.TLabel", foreground=MUTED)
    style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
    style.configure("Heading.TLabel", font=("Segoe UI", 14, "bold"), foreground=ACCENT)
    style.configure("TButton", padding=(10, 7), background="#1e293b", foreground=FG, bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, focuscolor=ACCENT)
    style.map("TButton", background=[("active", BORDER)], foreground=[("disabled", MUTED)])
    style.configure("Primary.TButton", background="#4338ca")
    style.configure("Nav.TButton", anchor="w", padding=(12, 11))
    style.configure("Active.Nav.TButton", background="#312e81", foreground="#c7d2fe")
    style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=FG, rowheight=29, bordercolor=BORDER)
    style.configure("Treeview.Heading", background="#1e293b", foreground=FG, padding=7)
    style.map("Treeview", background=[("selected", "#3730a3")], foreground=[("selected", "#ffffff")])
    style.configure("TEntry", fieldbackground=PANEL, foreground=FG, insertcolor=FG, padding=6)
    style.configure("TCombobox", fieldbackground=PANEL, foreground=FG, arrowcolor=FG, padding=5)
    style.map("TCombobox", fieldbackground=[("readonly", PANEL)], foreground=[("readonly", FG)])
    style.configure("TProgressbar", background="#6366f1", troughcolor="#1e293b", bordercolor=BG)
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(12, 7), background="#1e293b")
    style.map("TNotebook.Tab", background=[("selected", "#312e81")])
    window.option_add("*TCombobox*Listbox.background", PANEL)
    window.option_add("*TCombobox*Listbox.foreground", FG)


class ScrollableBody(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        canvas = tk.Canvas(self, background=BG, highlightthickness=0, width=1, height=1)
        scroll = ttk.Scrollbar(self, command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self.body = ttk.Frame(canvas)
        item = canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(item, width=event.width))
        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-event.delta / 120), "units"))


class ReadOnlyText(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.text = tk.Text(self, wrap="word", bg=PANEL, fg=FG, selectbackground="#4338ca", insertbackground=FG, relief="flat", padx=12, pady=10, font=("Segoe UI", 10), state="disabled", **kwargs)
        scroll = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

    def set(self, value):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", value)
        self.text.configure(state="disabled")

    def append(self, value):
        self.text.configure(state="normal")
        self.text.insert("end", value)
        self.text.see("end")
        self.text.configure(state="disabled")


class Table(ttk.Frame):
    def __init__(self, parent, columns, select=None, sort=None):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(self, columns=[c[0] for c in columns], show="headings", selectmode="browse", height=6)
        self.tree.grid(row=0, column=0, sticky="nsew")
        for key, label, width in columns:
            self.tree.heading(key, text=label, command=(lambda k=key: sort(k)) if sort else "")
            self.tree.column(key, width=width, minwidth=70, stretch=False)
        vertical = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        self.tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.tree.tag_configure("next", foreground="#c7d2fe", background="#1e1b4b")
        self.tree.tag_configure("blocked", foreground="#fda4af")
        if select:
            self.tree.bind("<<TreeviewSelect>>", lambda _: select(self.tree.selection()[0]) if self.tree.selection() else None)
        self.version = 0

    def render(self, rows):
        self.version += 1
        version = self.version
        old = self.tree.get_children()
        if old:
            self.tree.delete(*old)
        iterator = iter(rows)
        def batch():
            if version != self.version or not self.winfo_exists():
                return
            for _ in range(80):
                row = next(iterator, None)
                if row is None:
                    return
                key, values, tags = row
                self.tree.insert("", "end", iid=key, values=values, tags=tags)
            self.after(1, batch)
        batch()
