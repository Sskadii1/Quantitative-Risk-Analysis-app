import sqlite3

# Kết nối với cơ sở dữ liệu SQLite (hoặc tạo mới nếu không tồn tại)
conn = sqlite3.connect("risk_management_congty.db")
cursor = conn.cursor()

# Tạo bảng nếu chưa tồn tại
cursor.execute('''
    CREATE TABLE IF NOT EXISTS risk_assessment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset TEXT,
        risk TEXT,
        asset_value REAL,
        EF REAL,
        SLE REAL,
        ARO REAL,
        loss_value REAL,
        safeguard TEXT,
        cost_of_safeguard REAL,
        EF_after_safeguard REAL,
        ALE_before REAL,
        ALE_after REAL,
        net_benefit REAL
    )
''')
conn.commit()

def tinh_ale(asset_value, EF, ARO, EF_after_safeguard):
    """Tính toán SLE, ALE Trước và ALE Sau Khi Áp Dụng Biện Pháp"""
    SLE = asset_value * EF
    ALE_before = SLE * ARO
    SLE_after = asset_value * EF_after_safeguard
    ALE_after = SLE_after * ARO
    return SLE, ALE_before, SLE_after, ALE_after

def nhap_du_lieu_rui_ro():
    """Nhập dữ liệu và lưu vào cơ sở dữ liệu"""
    asset = input("\nNhập tên tài sản: ")
    risk = input("Nhập rủi ro: ")
    asset_value = float(input("Nhập giá trị tài sản ($): "))
    EF = float(input("Nhập yếu tố phơi nhiễm (dưới dạng thập phân, ví dụ 0.85 cho 85%): "))
    ARO = float(input("Nhập tỷ lệ xảy ra hàng năm (dưới dạng thập phân, ví dụ 0.10 cho 10%): "))
    loss_value = float(input("Nhập giá trị thiệt hại ($): "))
    safeguard = input("Nhập biện pháp bảo vệ: ")
    cost_of_safeguard = float(input("Nhập chi phí bảo vệ ($): "))
    EF_after_safeguard = float(input("Nhập yếu tố phơi nhiễm sau khi áp dụng biện pháp bảo vệ (dưới dạng thập phân, ví dụ 0.05 cho 5%): "))

    # Tính toán các giá trị
    SLE, ALE_before, SLE_after, ALE_after = tinh_ale(asset_value, EF, ARO, EF_after_safeguard)
    net_benefit = (ALE_before - ALE_after) - cost_of_safeguard

    # Lưu vào cơ sở dữ liệu
    cursor.execute('''
        INSERT INTO risk_assessment (asset, risk, asset_value, EF, SLE, ARO, loss_value, safeguard, 
                                     cost_of_safeguard, EF_after_safeguard, ALE_before, ALE_after, net_benefit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (asset, risk, asset_value, EF, SLE, ARO, loss_value, safeguard, cost_of_safeguard, EF_after_safeguard, ALE_before, ALE_after, net_benefit))

    conn.commit()
    print(f"\nĐánh giá rủi ro cho {asset} đã được lưu thành công!\n")

def hien_thi_du_lieu_rui_ro():
    """Lấy và hiển thị tất cả các đánh giá rủi ro đã lưu"""
    cursor.execute("SELECT * FROM risk_assessment")
    records = cursor.fetchall()

    if not records:
        print("\nKhông có đánh giá rủi ro nào. Vui lòng nhập dữ liệu trước.\n")
        return

    print("\nDanh sách các đánh giá rủi ro:")
    print("-" * 120)
    print(f"{'ID':<5} {'Tài sản':<15} {'Rủi ro':<20} {'ALE Trước ($)':<15} {'ALE Sau ($)':<15} {'Lợi ích ròng ($)':<15}")
    print("-" * 120)

    for row in records:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<20} {row[11]:<15.2f} {row[12]:<15.2f} {row[13]:<15.2f}")

    print("-" * 120)

def cap_nhat_rui_ro():
    """Cập nhật thông tin rủi ro đã lưu"""
    # Hiển thị các bản ghi và cho người dùng chọn bản ghi cần cập nhật
    hien_thi_du_lieu_rui_ro()

    id_rui_ro = int(input("\nNhập ID của bản ghi cần cập nhật: "))

    cursor.execute("SELECT * FROM risk_assessment WHERE id = ?", (id_rui_ro,))
    record = cursor.fetchone()

    if not record:
        print("Không tìm thấy bản ghi với ID này.")
        return

    print(f"\nCập nhật rủi ro cho bản ghi ID {id_rui_ro}:")
    
    # Cập nhật thông tin cho các trường
    asset = input(f"Tài sản (hiện tại: {record[1]}): ") or record[1]
    risk = input(f"Rủi ro (hiện tại: {record[2]}): ") or record[2]
    asset_value = float(input(f"Giá trị tài sản ($) (hiện tại: {record[3]}): ") or record[3])
    EF = float(input(f"Yếu tố phơi nhiễm (hiện tại: {record[4]}): ") or record[4])
    ARO = float(input(f"Tỷ lệ xảy ra hàng năm (hiện tại: {record[6]}): ") or record[6])
    loss_value = float(input(f"Giá trị thiệt hại ($) (hiện tại: {record[7]}): ") or record[7])
    safeguard = input(f"Biện pháp bảo vệ (hiện tại: {record[8]}): ") or record[8]
    cost_of_safeguard = float(input(f"Chi phí bảo vệ ($) (hiện tại: {record[9]}): ") or record[9])
    EF_after_safeguard = float(input(f"Yếu tố phơi nhiễm sau bảo vệ (hiện tại: {record[10]}): ") or record[10])

    # Tính toán lại các giá trị sau khi cập nhật
    SLE, ALE_before, SLE_after, ALE_after = tinh_ale(asset_value, EF, ARO, EF_after_safeguard)
    net_benefit = (ALE_before - ALE_after) - cost_of_safeguard

    # Cập nhật vào cơ sở dữ liệu
    cursor.execute('''
        UPDATE risk_assessment SET 
            asset = ?, risk = ?, asset_value = ?, EF = ?, SLE = ?, ARO = ?, loss_value = ?, 
            safeguard = ?, cost_of_safeguard = ?, EF_after_safeguard = ?, ALE_before = ?, ALE_after = ?, net_benefit = ?
        WHERE id = ?
    ''', (asset, risk, asset_value, EF, SLE, ARO, loss_value, safeguard, cost_of_safeguard, EF_after_safeguard, ALE_before, ALE_after, net_benefit, id_rui_ro))

    conn.commit()
    print(f"\nCập nhật thành công cho bản ghi ID {id_rui_ro}!")

# Vòng lặp menu chính
while True:
    print("\nHỆ THỐNG QUẢN LÝ RỦI RO")
    print("1. Nhập Dữ Liệu Rủi Ro Mới")
    print("2. Tính Toán & Hiển Thị Các Rủi Ro Đã Lưu")
    print("3. Cập Nhật Rủi Ro Đã Nhập")
    print("4. Hiển Thị Tất Cả Dữ Liệu")
    print("5. Thoát")

    choice = input("Chọn một tùy chọn (1/2/3/4/5): ")
    
    if choice == "1":
        nhap_du_lieu_rui_ro()
    elif choice == "2":
        hien_thi_du_lieu_rui_ro()
    elif choice == "3":
        cap_nhat_rui_ro()
    elif choice == "4":
        hien_thi_tat_ca_du_lieu()
    elif choice == "5":
        print("\nThoát... Đóng kết nối cơ sở dữ liệu.")
        conn.close()
        break
    else:
        print("\nTùy chọn không hợp lệ. Vui lòng thử lại.")
