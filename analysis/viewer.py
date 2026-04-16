# Car Listing Analysis CSV Viewer using Cars.com - Amair084 on GitHub

import customtkinter as ctk
from PIL import Image
import pandas as pd
from pathlib import Path
import sys, os

def resource_path(path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

class CSVViewer(ctk.CTkToplevel):
    def __init__(self, filepath):
        super().__init__()
        self.title("Cars.com Market Analysis | Data Viewer")
        self.geometry("1100x600")
        self.configure(fg_color="#2b2b2b")
        self.iconbitmap(resource_path("resources/icon.ico"))
        self.resizable(True, True)

        self.filepath = filepath
        self.df = pd.read_csv(filepath, dtype=str)
        self.sort_state = {}
        self.filtered_df = self.df.copy()

        self._build_ui()

    def _build_ui(self):
        # ── Title bar ─────────────────────────────────────────
        topbar = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=0)
        topbar.pack(fill="x")

        ctk.CTkLabel(topbar, text="  Data Viewer", fg_color="#1a1a1a",
                     text_color="#FFFFFF", font=("Arial", 13, "bold")).pack(side="left", pady=10)

        ctk.CTkLabel(topbar, text=f"{Path(self.filepath).name}  ",
                     fg_color="#1a1a1a", text_color="#666666",
                     font=("Courier New", 10)).pack(side="right", pady=10)

        # ── Search + Logo row ─────────────────────────────────
        searchbar = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=0)
        searchbar.pack(fill="x", padx=16, pady=(8, 0))

        ctk.CTkLabel(searchbar, text="SEARCH", fg_color="#2b2b2b",
                     text_color="#666666", font=("Courier New", 9, "bold")).pack(side="left", padx=(0, 8))

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._on_search)

        search_entry = ctk.CTkEntry(searchbar, textvariable=self.search_var,
                                    fg_color="#1a1a1a", text_color="#e2e8f0",
                                    border_color="#8136B2", border_width=1,
                                    font=("Courier New", 11), width=300)
        search_entry.pack(side="left", padx=(0, 16), pady=6)

        self.row_count_label = ctk.CTkLabel(searchbar, fg_color="#2b2b2b",
                                            text_color="#666666", font=("Arial", 9), text="")
        self.row_count_label.pack(side="left")

        # ── Logo ───────────────────
        logo_img = ctk.CTkImage(
            light_image=Image.open(resource_path("resources/icon.png")),
            dark_image=Image.open(resource_path("resources/icon.png")),
            size=(55, 62)
        )
        ctk.CTkLabel(searchbar, image=logo_img, text="",
                     fg_color="#2b2b2b").pack(side="right", padx=(0, 9))

        # ── Hint ──────────────────────────────────────────────
        ctk.CTkLabel(self, text="  Click a cell to copy  •  Click a header to sort  •  ↕ cycles asc / desc / original",
                     fg_color="#2b2b2b", text_color="#555555",
                     font=("Courier New", 9)).pack(anchor="w", padx=16)

        # ── Table container ───────────────────────────────────
        container = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=0)
        container.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        # CTk doesn't have a native scrollable canvas, so we use tk underneath
        import tkinter as tk
        self.canvas = tk.Canvas(container, bg="#2b2b2b", highlightthickness=0)
        vscroll = ctk.CTkScrollbar(container, orientation="vertical", command=self.canvas.yview)
        hscroll = ctk.CTkScrollbar(container, orientation="horizontal", command=self.canvas.xview)

        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)

        self.table_frame = tk.Frame(self.canvas, bg="#2b2b2b")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.table_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        # ── Copied toast ──────────────────────────────────────
        self.copied = ctk.CTkLabel(self, text="✓ Copied!", fg_color="#8136B2",
                                   text_color="white", font=("Courier New", 10, "bold"),
                                   corner_radius=6)

        self._render_table()

    def _col_width(self, col, df):
        header_len = len(str(col))
        if len(df) > 0:
            max_data_len = df[col].fillna("").astype(str).str.len().max()
        else:
            max_data_len = 0
        return int(min(max(int(max(header_len, max_data_len)) + 2, 8), 30))

    def _render_table(self):
        import tkinter as tk
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        df = self.filtered_df
        cols = list(df.columns)

        # ── Headers ───────────────────────────────────────────
        for ci, col in enumerate(cols):
            direction = self.sort_state.get(col, None)
            arrow = " ↑" if direction == "asc" else " ↓" if direction == "desc" else " ↕"
            w = self._col_width(col, df)

            btn = tk.Button(
                self.table_frame,
                text=str(col) + arrow,
                bg="#1a1a1a", fg="#AB74CF",
                font=("Arial", 10, "bold"),
                relief="flat", bd=0,
                anchor="w", padx=8,
                width=w,
                cursor="hand2",
                activebackground="#2d2d2d",
                activeforeground="#8136B2",
                command=lambda c=col: self._sort_by(c)
            )
            btn.grid(row=0, column=ci, sticky="nsew", padx=1, pady=1, ipady=8)

        # ── Rows ──────────────────────────────────────────────
        for ri, (_, row) in enumerate(df.iterrows()):
            row_bg = "#222222" if ri % 2 == 0 else "#2b2b2b"
            for ci, col in enumerate(cols):
                val = str(row[col]) if str(row[col]) != "nan" else ""
                w = self._col_width(col, df)

                cell = tk.Label(
                    self.table_frame,
                    text=val,
                    bg=row_bg, fg="#e2e8f0",
                    font=("Arial", 10),
                    relief="flat",
                    anchor="w", padx=8,
                    width=w,
                    cursor="hand2"
                )
                cell.grid(row=ri + 1, column=ci, sticky="nsew", padx=1, pady=0, ipady=6)
                cell.bind("<Button-1>", lambda e, v=val: self._copy(v))
                cell.bind("<Enter>", lambda e, w=cell: w.configure(bg="#3d1f5e"))
                cell.bind("<Leave>", lambda e, w=cell, bg=row_bg: w.configure(bg=bg))

        self._update_row_count()

    def _numeric_sort_key(self, col):
        series = self.filtered_df[col].fillna("")
        stripped = series.str.replace(r"[^\d.]", "", regex=True)
        converted = pd.to_numeric(stripped, errors="coerce")
        if converted.notna().sum() > len(converted) / 2:
            return converted
        return series

    def _sort_by(self, col):
        current = self.sort_state.get(col, None)

        if current is None:
            self.sort_state[col] = "asc"
            asc = True
        elif current == "asc":
            self.sort_state[col] = "desc"
            asc = False
        else:
            self.sort_state[col] = None
            self._apply_search(self.search_var.get())
            return

        key = self._numeric_sort_key(col)

        if isinstance(key, pd.Series) and pd.api.types.is_numeric_dtype(key):
            self.filtered_df = self.filtered_df.assign(_sort_key=key.values) \
                .sort_values("_sort_key", ascending=asc, na_position="last") \
                .drop(columns="_sort_key")
        else:
            self.filtered_df = self.filtered_df.sort_values(
                col, ascending=asc, na_position="last")

        self._render_table()

    def _on_search(self, *args):
        self._apply_search(self.search_var.get())

    def _apply_search(self, query):
        if not query.strip():
            self.filtered_df = self.df.copy()
        else:
            mask = self.df.astype(str).apply(
                lambda col: col.str.contains(query, case=False, na=False)
            ).any(axis=1)
            self.filtered_df = self.df[mask].copy()
        self.sort_state = {}
        self._render_table()

    def _copy(self, value):
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()
        self.copied.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        self.after(1500, self.copied.place_forget)

    def _update_row_count(self):
        total = len(self.df)
        showing = len(self.filtered_df)
        if showing == total:
            self.row_count_label.configure(text=f"{total} rows")
        else:
            self.row_count_label.configure(text=f"{showing} of {total} rows")