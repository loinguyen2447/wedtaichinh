# WĐT AI — App iOS (Xcode + WKWebView)

App iOS gói sẵn trang web bảng giá trong thư mục này. **File `index.html` ở thư mục gốc repo chính là toàn bộ giao diện app.**

## Cấu trúc

```
ios/
├── WDTAI.xcodeproj/     ← Mở file này bằng Xcode
├── WDTAI/
│   ├── WDTAIApp.swift   ← Entry point SwiftUI
│   ├── ContentView.swift ← WKWebView load index.html
│   ├── Info.plist       ← Tên app "WĐT AI", launch screen
│   └── Assets.xcassets/ ← Icon app + logo launch screen
└── make_icons.py        ← Script sinh lại icon (nếu muốn đổi logo)
```

## Cài lên iPhone của bạn (sideload, miễn phí)

### Bước 0 — Chuẩn bị (làm 1 lần)
1. **Mac có Xcode 15+** (tải miễn phí trên App Store, dung lượng ~12 GB).
2. **Cáp Lightning/USB-C** kết nối iPhone với Mac.
3. Trên iPhone: **Cài đặt → Quyền riêng tư & Bảo mật → Chế độ nhà phát triển** → bật ON (chỉ hiện trên iOS 16+; nếu không thấy thì bỏ qua, Xcode sẽ tự hỏi lúc kết nối).
4. Trên iPhone màn hình đầu tiên: bấm **Tin cậy** khi được hỏi "Tin cậy máy tính này?".

### Bước 1 — Mở project
Mở file `ios/WDTAI.xcodeproj` bằng Xcode (nhấp đúp).

### Bước 2 — Kéo `index.html` vào project
1. Trong Xcode, nhìn panel trái (Project Navigator) → chọn mục **WDTAI** (cùng cấp với `WDTAIApp.swift`).
2. Kéo file **`index.html`** từ thư mục repo vào đó.
3. Hộp thoại hiện ra → tích:
   - ✅ **Copy items if needed**
   - ✅ **Add to targets: WDTAI**
4. Bấm **Finish**.

> Nếu bỏ qua bước này, app sẽ chạy và hiện màn hình hướng dẫn nhắc bạn thêm file (không bị crash).

### Bước 3 — Chọn Team (để ký app)
1. Chọn project **WDTAI** (dòng đầu tiên trong Project Navigator) → tab **Signing & Capabilities**.
2. Tick ✅ **Automatically manage signing**.
3. Mục **Team** → chọn **Your Name (Personal Team)** — dùng Apple ID cá nhân là được, KHÔNG cần trả $99.
   - Nếu chưa có: Xcode → Settings (⌘,) → Accounts → bấm **+** → đăng nhập Apple ID thường.

### Bước 4 — Chọn thiết bị & Run
1. Trên thanh công cụ Xcode (góc trên trái), bấm vào tên thiết bị (mặc định là Simulator) → chọn **iPhone của bạn** (mục "iOS Device").
2. Bấm ▶️ (⌘R) để build và cài.
3. Nếu báo lỗi signing:
   - `Failed to register bundle identifier` → Bundle ID `com.wdtai.app` đã có người dùng Team khác dùng → đổi ở **Signing & Capabilities → Bundle Identifier** thành `com.wdtai.app2` (hoặc bất kỳ, chỉ cần duy nhất).
   - `Untrusted Developer` trên iPhone → vào **Cài đặt → Cài đặt chung → VPN & Quản lý thiết bị** → chọn Apple ID của bạn → bấm **Tin cậy**.

### Bước 5 — App đã trên máy!
- App tên **WĐT AI**, chạy offline (file HTML nằm trong app).
- Muốn đổi sang load từ GitHub Pages (bản web luôn mới): mở `ContentView.swift`, đổi dòng
  `static let useRemote = false` thành `true`.

## Câu hỏi thường gặp

**Q: Chưa có Mac?**
Dùng máy ảo macOS trên Windows (macOS Sonoma + Xcode) hoặc dịch vụ CI đám mây như **Codemagic** (miễn phí 500 phút/tháng), **GitHub Actions với runner macOS** (miễn phí cho repo public) — nhưng phải cài chứng chỉ ký lên dịch vụ nên hơi phức tạp.

**Q: App tự tắt sau 7 ngày?**
Đúng, Apple giới hạn app ký bằng tài khoản miễn phí chỉ sống **7 ngày**. Cách xử lý:
- Chạy lại `⌘R` trong Xcode (1 phút, làm mỗi tuần).
- Trả $99/năm để ký tài khoản Developer → app sống 365 ngày.

**Q: Muốn đẩy lên App Store?**
Cần tài khoản Apple Developer ($99/năm), rồi trong Xcode chọn **Product → Archive** → **Distribute App**. Lưu ý app chỉ là WebView có thể bị Apple từ chối theo guideline 4.2 — nên thêm tính năng native (thông báo giá, Face ID, widget) trước khi nộp.

**Q: Icon muốn đổi?**
Sửa `ios/make_icons.py` (biến `GOLD`, `GREEN`, `BG` + hình 3 nến) rồi chạy:
```bash
python3 ios/make_icons.py
```
Icon sẽ tự cập nhật vào `Assets.xcassets` — mở lại Xcode là thấy.

## Lưu ý dữ liệu

- Giá coin/vàng: **thật** từ Binance API.
- Giá dầu: **mô phỏng** (đã gắn nhãn MÔ PHỎNG trên UI) — chỉ tham khảo, không phải giá giao ngay thực tế.
- Fear & Greed Index: **thật** từ alternative.me.
