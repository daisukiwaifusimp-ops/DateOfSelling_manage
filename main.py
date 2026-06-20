import customtkinter as ctk
from customtkinter import CTkInputDialog
from tkinter import filedialog, messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import csv

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phân Tích Dữ Liệu Bán Hàng")
        self.root.geometry("1100x700")

        self.ngay = np.array([])
        self.sanpham = np.array([])
        self.soluong = np.array([])
        self.doanhthu = np.array([])

        self.create_gui()

    def create_gui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.left_frame = ctk.CTkFrame(self.root, width=230, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_rowconfigure(11, weight=1)

        ctk.CTkLabel(self.left_frame, text="💻 MENU CHỨC NĂNG", font=ctk.CTkFont(size=17, weight="bold")).grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=20,
                                                                                                              pady=(20,
                                                                                                                    15))

        btn_args = {"width": 190, "height": 35, "font": ctk.CTkFont(size=13), "corner_radius": 6, "anchor": "w"}

        ctk.CTkButton(self.left_frame, text="📂 1. Tải dữ liệu CSV", command=self.load_data, **btn_args).grid(row=1,
                                                                                                             column=0,
                                                                                                             padx=20,
                                                                                                             pady=5)
        ctk.CTkButton(self.left_frame, text="📊 2. Thống kê tổng quan", command=self.show_stats, **btn_args).grid(row=2,
                                                                                                                 column=0,
                                                                                                                 padx=20,
                                                                                                                 pady=5)
        ctk.CTkButton(self.left_frame, text="🔍 3. Lọc theo Doanh thu", command=self.filter_data, **btn_args).grid(row=3,
                                                                                                                  column=0,
                                                                                                                  padx=20,
                                                                                                                  pady=5)

        ctk.CTkButton(self.left_frame, text="🔮 4. Dự báo Xu hướng", command=self.predict_trend, **btn_args).grid(row=4,
                                                                                                                 column=0,
                                                                                                                 padx=20,
                                                                                                                 pady=5)

        ctk.CTkButton(self.left_frame, text="📊 5. Biểu đồ Cột", command=self.draw_bar_chart, **btn_args).grid(row=5,
                                                                                                              column=0,
                                                                                                              padx=20,
                                                                                                              pady=5)
        ctk.CTkButton(self.left_frame, text="📉 6. Biểu đồ Đường", command=self.draw_line_chart, **btn_args).grid(row=6,
                                                                                                                 column=0,
                                                                                                                 padx=20,
                                                                                                                 pady=5)
        ctk.CTkButton(self.left_frame, text="⭕ 7. Biểu đồ Tròn", command=self.draw_pie_chart, **btn_args).grid(row=7,
                                                                                                               column=0,
                                                                                                               padx=20,
                                                                                                               pady=5)

        ctk.CTkButton(self.left_frame, text="💾 8. Xuất Báo Cáo (.txt)", command=self.export_report, fg_color="#27ae60",
                      hover_color="#2ecc71", **btn_args).grid(row=8, column=0, padx=20, pady=(20, 5))
        ctk.CTkButton(self.left_frame, text="🔄 Làm mới", command=self.clear_screen, fg_color="transparent",
                      border_width=2, text_color=("gray10", "#DCE4EE"), **btn_args).grid(row=9, column=0, padx=20,
                                                                                         pady=5, sticky="s")

        self.right_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.text_result = ctk.CTkTextbox(self.right_frame, height=130, font=ctk.CTkFont(size=14), corner_radius=10)
        self.text_result.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        self.text_result.insert("0.0", "👋 Chào mừng bạn! Vui lòng tải dữ liệu CSV để bắt đầu.")

        self.chart_frame = ctk.CTkFrame(self.right_frame, corner_radius=10)
        self.chart_frame.grid(row=1, column=0, sticky="nsew")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", font=('Arial', 10, 'bold'),
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def load_data(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath: return

        try:
            n_list, sp_list, sl_list, dt_list = [], [], [], []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    n_list.append(row[0])
                    sp_list.append(row[1])
                    sl_list.append(int(row[2]))
                    dt_list.append(float(row[3]))

            self.ngay, self.sanpham, self.soluong, self.doanhthu = np.array(n_list), np.array(sp_list), np.array(
                sl_list), np.array(dt_list)
            self.print_to_screen(f"✅ Đã tải thành công {len(self.ngay)} dòng dữ liệu!")
            self.show_data_table()

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def show_data_table(self):
        self.clear_chart()
        columns = ("Ngay", "SanPham", "SoLuong", "DoanhThu")
        tree = ttk.Treeview(self.chart_frame, columns=columns, show="headings", style="Treeview")

        tree.heading("Ngay", text="Ngày Bán")
        tree.heading("SanPham", text="Tên Sản Phẩm")
        tree.heading("SoLuong", text="Số Lượng")
        tree.heading("DoanhThu", text="Doanh Thu (VNĐ)")

        tree.column("Ngay", width=120, anchor="center")
        tree.column("SanPham", width=250, anchor="w")
        tree.column("SoLuong", width=100, anchor="center")
        tree.column("DoanhThu", width=200, anchor="e")

        scrollbar = ttk.Scrollbar(self.chart_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        for i in range(len(self.ngay)):
            tree.insert("", "end", values=(self.ngay[i], self.sanpham[i], self.soluong[i], f"{self.doanhthu[i]:,.0f}"))

    def show_stats(self):
        if len(self.doanhthu) == 0: return self.print_to_screen("⚠️ Chưa có dữ liệu!")
        msg = (f"📊 THỐNG KÊ TỔNG QUAN\n"
               f"🔹 Tổng doanh thu: {np.sum(self.doanhthu):,.0f} VNĐ\n"
               f"🔹 Trung bình/ngày: {np.mean(self.doanhthu):,.0f} VNĐ\n"
               f"🔹 Đỉnh cao nhất: {np.max(self.doanhthu):,.0f} VNĐ (Ngày {self.ngay[np.argmax(self.doanhthu)]})")
        self.print_to_screen(msg)

    def filter_data(self):
        if len(self.doanhthu) == 0: return self.print_to_screen("⚠️ Chưa có dữ liệu!")

        dialog = CTkInputDialog(text="Nhập mức doanh thu mong muốn (VNĐ):", title="Lọc Dữ Liệu")
        muc_loc = dialog.get_input()

        if muc_loc is None or not muc_loc.isdigit(): return self.print_to_screen("⚠️ Vui lòng nhập một số hợp lệ.")

        muc_loc = int(muc_loc)
        cond = self.doanhthu >= muc_loc
        ngay_loc, sp_loc, dt_loc = self.ngay[cond], self.sanpham[cond], self.doanhthu[cond]

        if len(dt_loc) == 0: return self.print_to_screen(f"Không có ngày nào đạt mức {muc_loc:,.0f} VNĐ.")

        msg = f"🎯 CÓ {len(dt_loc)} ĐƠN HÀNG ĐẠT MỨC >= {muc_loc:,.0f} VNĐ\n"
        for n, sp, dt in zip(ngay_loc, sp_loc, dt_loc): msg += f"📍 {n} - {sp}: {dt:,.0f} VNĐ\n"
        self.print_to_screen(msg)

    # --- HÀM DỰ BÁO ---
    def predict_trend(self):
        if len(self.doanhthu) == 0: return self.print_to_screen("⚠️ Chưa có dữ liệu!")
        self.clear_chart()

        # 1. Vẽ biểu đồ nền mờ và đường xu hướng đứt nét
        x = np.arange(len(self.doanhthu))
        y = self.doanhthu
        he_so = np.polyfit(x, y, 1)
        duong_du_bao = np.poly1d(he_so)

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        ax.bar(self.ngay, y, color='#95a5a6', alpha=0.5, label="Dữ liệu thực tế")
        ax.plot(self.ngay, duong_du_bao(x), color='#e74c3c', linestyle='--', linewidth=3,
                label="Đường xu hướng (Hồi quy)")

        ax.set_title("DỰ BÁO XU HƯỚNG BÁN HÀNG", fontweight='bold')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f'{int(val):,}'))
        ax.tick_params(axis='x', rotation=45)
        for i, label in enumerate(ax.get_xticklabels()):
            if i % 3 != 0: label.set_visible(False)

        ax.legend()
        plt.tight_layout()
        self.embed_chart(fig)

        # 2. Xử lý logic Phân tích Tăng trưởng
        msg_tang_truong = ""
        if len(self.doanhthu) >= 2:
            mid = len(self.doanhthu) // 2
            doanhthu_nua_dau = np.sum(self.doanhthu[:mid])
            doanhthu_nua_sau = np.sum(self.doanhthu[mid:])
            chenh_lech = doanhthu_nua_sau - doanhthu_nua_dau
            # Tránh lỗi chia cho 0 nếu nửa đầu bằng 0
            ty_le = (chenh_lech / doanhthu_nua_dau) * 100 if doanhthu_nua_dau > 0 else 0
            trang_thai = "📈 TĂNG TRƯỞNG TỐT" if ty_le > 0 else "📉 SUY GIẢM"

            msg_tang_truong = (f"⚖️ PHÂN TÍCH TĂNG TRƯỞNG KỲ TRƯỚC\n"
                               f"🔹 Nửa đầu: {doanhthu_nua_dau:,.0f} đ  |  Nửa sau: {doanhthu_nua_sau:,.0f} đ\n"
                               f"👉 Trạng thái: {trang_thai} ({ty_le:+.2f}%)\n"
                               f"----------------------------------------\n")

        # 3. Kết luận từ thuật toán Dự báo Hồi quy (polyfit)
        loi_khuyen = "Đà bán hàng đang có xu hướng TĂNG LÊN." if he_so[
                                                                     0] > 0 else "Đà bán hàng đang GIẢM XUỐNG, cần tung khuyến mãi."
        msg_du_bao = f"🔮 DỰ BÁO XU HƯỚNG TƯƠNG LAI\n{loi_khuyen}"

        # 4. In gộp cả 2 thông báo ra Textbox
        self.print_to_screen(msg_tang_truong + msg_du_bao)
    def export_report(self):
        if len(self.doanhthu) == 0:
            return messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu! Vui lòng tải file CSV trước.")

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")],
                                                title="Lưu báo cáo tổng hợp")
        if not filepath: return

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("          BÁO CÁO KẾT QUẢ PHÂN TÍCH DOANH THU           \n")
                f.write("========================================================\n\n")

                f.write("[1]. THỐNG KÊ TỔNG QUAN\n")
                f.write(f"- Tổng số ngày phân tích: {len(self.ngay)} ngày\n")
                f.write(f"- Tổng doanh thu: {np.sum(self.doanhthu):,.0f} VNĐ\n")
                f.write(f"- Doanh thu trung bình/ngày: {np.mean(self.doanhthu):,.0f} VNĐ\n\n")

                idx_max = np.argmax(self.doanhthu)
                f.write("[2]. KỶ LỤC BÁN HÀNG\n")
                f.write(f"- Sản phẩm doanh thu cao nhất: {self.sanpham[idx_max]}\n")
                f.write(f"- Bán vào ngày: {self.ngay[idx_max]}\n")
                f.write(f"- Mức doanh thu đạt: {self.doanhthu[idx_max]:,.0f} VNĐ\n\n")

                x = np.arange(len(self.doanhthu))
                he_so = np.polyfit(x, self.doanhthu, 1)
                loi_khuyen = "Đang trên đà TĂNG TRƯỞNG. Tiếp tục duy trì phát huy!" if he_so[
                                                                                           0] > 0 else "Đang trên đà GIẢM. Cần có chiến lược Marketing, tung khuyến mãi để kích cầu!"

                f.write("[3]. DỰ BÁO XU HƯỚNG TƯƠNG LAI\n")
                f.write(f"-> Nhận định từ hệ thống: {loi_khuyen}\n")

                f.write("\n========================= HẾT ==========================\n")

            messagebox.showinfo("Thành công", f"Đã xuất báo cáo tổng hợp tại:\n{filepath}")
            self.print_to_screen("💾 Đã xuất báo cáo thành công! Hãy mở file txt vừa lưu để xem chi tiết.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

    def draw_bar_chart(self):
        if len(self.doanhthu) == 0: return self.print_to_screen("⚠️ Chưa có dữ liệu!")
        self.clear_chart()

        unique_sp = np.unique(self.sanpham)
        doanhthu_sp = [np.sum(self.doanhthu[self.sanpham == sp]) for sp in unique_sp]

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        ax.bar(unique_sp, doanhthu_sp,
               color=['#3498db', '#2ecc71', '#e67e22', '#9b59b6', '#f1c40f', '#e74c3c', '#1abc9c'])
        ax.set_title("DOANH THU THEO SẢN PHẨM", fontweight='bold')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f'{int(val):,}'))
        ax.tick_params(axis='x', rotation=15)
        plt.tight_layout()

        self.embed_chart(fig)
        self.print_to_screen("📈 Đã vẽ biểu đồ cột!")

    def draw_line_chart(self):
        if len(self.doanhthu) == 0: return self.print_to_screen("⚠️ Chưa có dữ liệu!")
        self.clear_chart()

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        ax.plot(self.ngay, self.doanhthu, marker='o', color='#e74c3c')
        ax.set_title("BIẾN ĐỘNG DOANH THU", fontweight='bold')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f'{int(val):,}'))
        ax.tick_params(axis='x', rotation=45)
        for i, label in enumerate(ax.get_xticklabels()):
            if i % 3 != 0: label.set_visible(False)

        plt.tight_layout()
        self.embed_chart(fig)
        self.print_to_screen("📉 Đã vẽ biểu đồ đường!")

    def draw_pie_chart(self):
        if len(self.doanhthu) == 0: return self.print_to_screen("⚠️ Chưa có dữ liệu!")
        self.clear_chart()

        unique_sp = np.unique(self.sanpham)
        doanhthu_sp = [np.sum(self.doanhthu[self.sanpham == sp]) for sp in unique_sp]

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        colors = ['#3498db', '#2ecc71', '#e67e22', '#9b59b6', '#f1c40f', '#e74c3c', '#1abc9c']
        ax.pie(doanhthu_sp, labels=unique_sp, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title("TỶ TRỌNG DOANH THU", fontweight='bold')
        plt.tight_layout()

        self.embed_chart(fig)
        self.print_to_screen("🎨 Đã vẽ biểu đồ tròn!")

    def clear_screen(self):
        self.text_result.delete("0.0", "end")
        self.clear_chart()
        self.text_result.insert("0.0", "Màn hình đã được làm mới.")

    def print_to_screen(self, text):
        self.text_result.delete("0.0", "end")
        self.text_result.insert("0.0", text)

    def clear_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def embed_chart(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")


if __name__ == "__main__":
    root = ctk.CTk()
    app = SalesApp(root)
    root.mainloop()