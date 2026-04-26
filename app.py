import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd


def bind_mousewheel(widget):
    widget.bind_all("<MouseWheel>", lambda e: widget.yview_scroll(int(-1*(e.delta/120)), "units"))
    widget.bind_all("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))
    widget.bind_all("<Button-5>", lambda e: widget.yview_scroll(1, "units"))

def unbind_mousewheel(widget):
    widget.unbind_all("<MouseWheel>")
    widget.unbind_all("<Button-4>")
    widget.unbind_all("<Button-5>")

root = tk.Tk()
root.title("Revenue Dashboard")
root.geometry("1350x900")
root.configure(bg="#f4f6fb")

canvas = tk.Canvas(root, bg="#f4f6fb", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas, bg="#f4f6fb")
window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(window_id, width=canvas.winfo_width())

scrollable_frame.bind("<Configure>", on_configure)
bind_mousewheel(canvas)  

countries = ["USA", "Germany", "Australia", "Japan", "Brazil"]
revenue = [4000, 5000, 450, 1200, 600]

def rgb_to_hex(rgb):
    r, g, b = rgb[:3]
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

colors = [rgb_to_hex(c) for c in plt.cm.Set2.colors]

monthly_data = []

FONT_BIG = ("Segoe UI", 20, "bold")
FONT_TITLE = ("Segoe UI", 13, "bold")
FONT = ("Segoe UI", 11)
CARD_BG = "#ffffff"

def total_revenue():
    return sum(revenue)

def top_market():
    return countries[revenue.index(max(revenue))] if countries else "-"

def market_share(i):
    return (revenue[i] / total_revenue() * 100) if total_revenue() else 0

def load_from_excel():
    global countries, revenue, colors
    path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not path:
        return
    try:
        df = pd.read_excel(path)
        if not {"Country", "Revenue"}.issubset(df.columns):
            messagebox.showerror("Error", "Excel mora imati kolone: Country i Revenue")
            return

        monthly_data.append(df.copy())
        grouped = df.groupby("Country", as_index=False)["Revenue"].sum()

        countries[:] = grouped["Country"].astype(str).tolist()
        revenue[:] = grouped["Revenue"].astype(float).tolist()
        colors[:] = [colors[i % len(colors)] for i in range(len(countries))]

        update_all()
        messagebox.showinfo("Success", "Excel podaci uspješno učitani!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_card(parent, title):
    f = tk.Frame(parent, bg=CARD_BG, width=300, height=90)
    f.pack_propagate(False)
    tk.Label(f, text=title, bg=CARD_BG, fg="#777",
             font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(12, 0))
    lbl = tk.Label(f, bg=CARD_BG, font=FONT_BIG)
    lbl.pack(anchor="w", padx=20)
    return f, lbl

top = tk.Frame(scrollable_frame, bg="#f4f6fb")
top.pack(pady=20)

cards = tk.Frame(top, bg="#f4f6fb")
cards.pack()

c1, lbl_total = create_card(cards, "TOTAL REVENUE")
c2, lbl_top = create_card(cards, "TOP MARKET")
c3, lbl_count = create_card(cards, "ACTIVE MARKETS")

c1.grid(row=0, column=0, padx=15)
c2.grid(row=0, column=1, padx=15)
c3.grid(row=0, column=2, padx=15)

mid = tk.Frame(scrollable_frame, bg="#f4f6fb")
mid.pack(fill="x", padx=40, pady=10)

mid.columnconfigure(0, weight=1)
mid.columnconfigure(1, weight=1)

left = tk.Frame(mid, bg=CARD_BG)
right = tk.Frame(mid, bg=CARD_BG)

left.grid(row=0, column=0, sticky="nsew", padx=15)
right.grid(row=0, column=1, sticky="nsew", padx=15)

def draw_donut():
    for w in left.winfo_children():
        w.destroy()

    tk.Label(
        left,
        text="Sales Distribution",
        bg=CARD_BG,
        font=FONT_TITLE
    ).pack(anchor="w", padx=20, pady=10)

    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.15)

    ax.pie(
        revenue,
        colors=colors[:len(revenue)],
        startangle=90,
        wedgeprops=dict(width=0.35)
    )
    ax.axis("equal")

    canvas_fig = FigureCanvasTkAgg(fig, left)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack(anchor="center")

    plt.close(fig)

    legend_frame = tk.Frame(left, bg=CARD_BG)
    legend_frame.pack(pady=8)

    cols = 4
    for i, country in enumerate(countries):
        item = tk.Frame(legend_frame, bg=CARD_BG)
        item.grid(row=i // cols, column=i % cols, padx=8, pady=4, sticky="w")

        tk.Canvas(
            item,
            width=10,
            height=10,
            bg=colors[i],
            highlightthickness=0
        ).pack(side="left", padx=(0, 5))

        tk.Label(
            item,
            text=country,
            bg=CARD_BG,
            font=("Segoe UI", 9)
        ).pack(side="left")

def draw_bar():
    for w in right.winfo_children():
        w.destroy()

    tk.Label(right, text="Revenue by Country",
             bg=CARD_BG, font=FONT_TITLE).pack(anchor="w", padx=20, pady=10)

    fig, ax = plt.subplots(figsize=(5.2, 4))
    bars = ax.bar(range(len(countries)), revenue, color=colors[:len(revenue)])
    ax.set_xticks([])
    ax.grid(axis="y", alpha=0.15)

    cursor = mplcursors.cursor(bars, hover=True)
    cursor.connect("add", lambda sel:
        sel.annotation.set_text(f"{countries[sel.index]}\n${revenue[sel.index]:,}")
    )

    FigureCanvasTkAgg(fig, right).get_tk_widget().pack()
    plt.close(fig)

def open_trend_reports():
    if not monthly_data:
        messagebox.showinfo("Info", "Nema spašenih mjesečnih podataka.")
        return

    all_data = pd.concat(monthly_data)
    months = len(monthly_data)

    top3 = (
        all_data.groupby("Country")["Revenue"]
        .sum().sort_values(ascending=False).head(3).index.tolist()
    )

    
    unbind_mousewheel(canvas)

    win = tk.Toplevel(root)
    win.title("Trend Reports")
    win.geometry("1450x950")
    win.configure(bg="#f4f6fb")

    canvas_win = tk.Canvas(win, bg="#f4f6fb", highlightthickness=0)
    canvas_win.pack(side="left", fill="both", expand=True)

    scroll_y = tk.Scrollbar(win, orient="vertical", command=canvas_win.yview)
    scroll_y.pack(side="right", fill="y")

    canvas_win.configure(yscrollcommand=scroll_y.set)

    scrollable_frame_win = tk.Frame(canvas_win, bg="#f4f6fb")
    window_id_win = canvas_win.create_window((0,0), window=scrollable_frame_win, anchor="nw")

    def on_configure(event):
        canvas_win.configure(scrollregion=canvas_win.bbox("all"))
        canvas_win.itemconfig(window_id_win, width=canvas_win.winfo_width())

    scrollable_frame_win.bind("<Configure>", on_configure)
    bind_mousewheel(canvas_win)

    
    def on_close():
        bind_mousewheel(canvas)
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    
    tk.Label(scrollable_frame_win, text=f"Trends in {months} months!",
             font=("Segoe UI", 28, "bold"),
             bg="#f4f6fb", fg="#333").pack(pady=(20, 20))

    content = tk.Frame(scrollable_frame_win, bg="#f4f6fb")
    content.pack(expand=True, fill="both", padx=20)
    content.columnconfigure((0,1,2), weight=1)

    for i, country in enumerate(top3):
        card = tk.Frame(content, bg=CARD_BG, padx=30, pady=30, relief="raised", bd=2)
        card.grid(row=0, column=i, padx=15, sticky="nsew")

        tk.Label(card, text=country,
                 font=("Segoe UI", 20, "bold"),
                 bg=CARD_BG).pack(pady=(0, 15))

        country_revenue = all_data[all_data["Country"] == country]["Revenue"].sum()
        tk.Label(card, text=f"Total Revenue: ${country_revenue:,}",
                 font=("Segoe UI", 14, "bold"),
                 bg=CARD_BG, fg="#4CAF50").pack(pady=(0, 15))

        fig, ax = plt.subplots(figsize=(6, 3.5))
        trend = [m[m["Country"] == country]["Revenue"].sum() for m in monthly_data]
        ax.plot(range(1, months + 1), trend, linewidth=2.5, marker="o", color="#3f51b5")
        ax.set_xticks(range(1, months + 1))
        ax.set_title("Revenue Trend", fontsize=14, fontweight="bold")
        ax.grid(alpha=0.25)
        FigureCanvasTkAgg(fig, card).get_tk_widget().pack(pady=(0,20))
        plt.close(fig)

        tk.Label(card, text="Top 3 Products",
                 font=("Segoe UI", 14, "bold"),
                 bg=CARD_BG).pack(pady=(0, 5))

        prod_data = all_data[all_data["Country"] == country]
        top_product_name = None
        if "Product" in prod_data.columns:
            top_products = (
                prod_data.groupby("Product")["Revenue"]
                .sum().sort_values(ascending=False).head(3)
            )
            for j, (prod, rev) in enumerate(top_products.items(), start=1):
                tk.Label(card, text=f"{j}. {prod}: ${rev:,}",
                         font=("Segoe UI", 12),
                         bg=CARD_BG, anchor="w").pack(fill="x", padx=5)
                if j == 1:
                    top_product_name = prod
        else:
            tk.Label(card, text="No product data available",
                     font=("Segoe UI", 12),
                     bg=CARD_BG).pack()

        tk.Label(card, text=" Recommendation",
                 font=("Segoe UI", 16, "bold italic"),
                 bg=CARD_BG, fg="#ff9800").pack(pady=(15,5))

        if top_product_name:
            tk.Label(card,
                     text=f"Focus on '{top_product_name}' in {country} to maximize revenue.",
                     font=("Segoe UI", 13),
                     bg=CARD_BG, wraplength=320, justify="left").pack(pady=(0,10))
        else:
            tk.Label(card, text="No recommendation available.",
                     font=("Segoe UI", 13),
                     bg=CARD_BG).pack()

    
    report_frame = tk.Frame(scrollable_frame_win, bg=CARD_BG, padx=20, pady=20, relief="groove", bd=2)
    report_frame.pack(fill="x", padx=25, pady=(20, 20))

    tk.Label(report_frame, text=" Market Changes Report",
             font=("Segoe UI", 18, "bold"),
             bg=CARD_BG, fg="#3f51b5").pack(anchor="w", pady=(0,10))

    changes_text = ""
    for month_idx, df in enumerate(monthly_data, start=1):
        current_countries = set(df["Country"].astype(str).tolist())
        previous_countries = set(monthly_data[month_idx-2]["Country"].astype(str).tolist()) if month_idx > 1 else set()
        added = current_countries - previous_countries
        removed = previous_countries - current_countries

        month_name = df["Date"].dt.strftime("%B").iloc[0] if "Date" in df.columns else f"Month {month_idx}"

        for c in added:
            changes_text += f"In {month_name}, we expanded market to {c}.\n"
        for c in removed:
            changes_text += f"In {month_name}, we stopped selling in {c}.\n"

    if not changes_text:
        changes_text = "No market changes detected."

    tk.Label(report_frame, text=changes_text,
             font=("Segoe UI", 13),
             bg=CARD_BG, justify="left", anchor="w").pack(fill="x")


table_frame = tk.Frame(scrollable_frame, bg=CARD_BG)
table_frame.pack(fill="both", padx=25, pady=15)

tk.Label(table_frame, text="Market Overview",
         bg=CARD_BG, font=FONT_TITLE).pack(anchor="w", padx=15, pady=10)

tree = ttk.Treeview(
    table_frame,
    columns=("Country", "Revenue", "Share"),
    show="headings",
    height=7
)

for col in ("Country", "Revenue", "Share"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True)

def refresh_table():
    tree.delete(*tree.get_children())
    for i, c in enumerate(countries):
        tree.insert("", "end",
                    values=(c, f"${revenue[i]:,}", f"{market_share(i):.1f}%"))

def update_all():
    draw_donut()
    draw_bar()
    refresh_table()
    lbl_total.config(text=f"${total_revenue():,}")
    lbl_top.config(text=top_market())
    lbl_count.config(text=len(countries))

btn_frame = tk.Frame(scrollable_frame, bg="#f4f6fb")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text=" Load Excel",
          font=("Segoe UI", 11, "bold"),
          bg="#4CAF50", fg="white",
          relief="flat", padx=15,
          command=load_from_excel).pack(side="left", padx=5)

tk.Button(btn_frame, text=" Trend Reports",
          font=("Segoe UI", 11, "bold"),
          bg="#3f51b5", fg="white",
          relief="flat", padx=15,
          command=open_trend_reports).pack(side="left")

update_all()
root.mainloop()
