import tkinter as tk
import pandas as pd
from pathlib import Path

class CSVViewer(tk.Toplevel):
    def __init__(self, filepath):
        super().__init__()
        self.title("Data Viewer")
        self.geometry("1100x600")
        self.configure(bg="#2b2b2b")
        self.resizable(True, True)

        self.filepath = filepath
        self.df = pd.read_csv(filepath, dtype=str)  # load everything as string to avoid float width issues
        self.sort_state = {}
        self.filtered_df = self.df.copy()

        self._build_ui()

    def _build_ui(self):
        # ── Title bar ─────────────────────────────────────────
        topbar = tk.Frame(self, bg="#1a1a1a", pady=10)
        topbar.pack(fill="x")

        tk.Label(topbar, text="  DATA VIEWER", bg="#1a1a1a", fg="#8136B2",
                 font=("Courier New", 13, "bold")).pack(side="left")

        tk.Label(topbar, text=f"{Path(self.filepath).name}  ",
                 bg="#1a1a1a", fg="#666666",
                 font=("Courier New", 10)).pack(side="right")

        # ── Search bar ────────────────────────────────────────
        searchbar = tk.Frame(self, bg="#2b2b2b", pady=8)
        searchbar.pack(fill="x", padx=16)

        tk.Label(searchbar, text="SEARCH", bg="#2b2b2b", fg="#666666",
                 font=("Courier New", 9, "bold")).pack(side="left", padx=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)

        search_entry = tk.Entry(searchbar, textvariable=self.search_var,
                                bg="#1a1a1a", fg="#e2e8f0", insertbackground="#8136B2",
                                relief="flat", font=("Courier New", 11),
                                highlightthickness=1, highlightcolor="#8136B2",
                                highlightbackground="#444444", width=40)
        search_entry.pack(side="left", ipady=5, padx=(0, 16))

        self.row_count_label = tk.Label(searchbar, bg="#2b2b2b", fg="#666666",
                                        font=("Courier New", 9))
        self.row_count_label.pack(side="left")

        # ── Hint ──────────────────────────────────────────────
        tk.Label(self, text="  Click a cell to copy  •  Click a header to sort  •  ↕ cycles asc / desc / original",
                 bg="#2b2b2b", fg="#555555", font=("Courier New", 9)).pack(anchor="w", padx=16)

        # ── Table container ───────────────────────────────────
        container = tk.Frame(self, bg="#2b2b2b")
        container.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        self.canvas = tk.Canvas(container, bg="#2b2b2b", highlightthickness=0)
        vscroll = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        hscroll = tk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)

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

        # ── Toast ─────────────────────────────────────────────
        self.toast = tk.Label(self, text="✓ Copied!", bg="#8136B2", fg="white",
                              font=("Courier New", 10, "bold"), padx=12, pady=4)

        self._render_table()

    def _col_width(self, col, df):
        """Return a safe integer character-width for a column."""
        header_len = len(str(col))
        if len(df) > 0:
            max_data_len = df[col].fillna("").astype(str).str.len().max()
        else:
            max_data_len = 0
        # clamp between 8 and 30 characters, always an int
        return int(min(max(int(max(header_len, max_data_len)) + 2, 8), 30))

    def _render_table(self):
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
                font=("Courier New", 10, "bold"),
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
                    font=("Courier New", 10),
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
        """Return a numeric series for columns that contain numbers inside strings."""
        series = self.filtered_df[col].fillna("")
        # strip $, commas, ' mi.' etc and try converting to float
        stripped = series.str.replace(r"[^\d.]", "", regex=True)
        converted = pd.to_numeric(stripped, errors="coerce")
        # if more than half the non-null values converted, treat as numeric
        if converted.notna().sum() > len(converted) / 2:
            return converted
        return series  # fall back to plain string sort

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
            # numeric sort using the extracted key
            self.filtered_df = self.filtered_df.assign(_sort_key=key.values) \
                .sort_values("_sort_key", ascending=asc, na_position="last") \
                .drop(columns="_sort_key")
        else:
            # plain string sort
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
        self.toast.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        self.after(1500, self.toast.place_forget)

    def _update_row_count(self):
        total = len(self.df)
        showing = len(self.filtered_df)
        if showing == total:
            self.row_count_label.config(text=f"{total} rows")
        else:
            self.row_count_label.config(text=f"{showing} of {total} rows")