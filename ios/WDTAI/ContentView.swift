import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        WebView()
            .ignoresSafeArea(.all, edges: .top) /* header web ăn theo phần tai thỏ */
            .statusBarHidden(false)
    }
}

struct WebView: UIViewRepresentable {
    /* Bật cả 2: bundle chạy offline, URL dùng khi bạn cập nhật web trên GitHub Pages */
    static let remoteURL = URL(string: "https://loinguyen2447.github.io/wedtaichinh/")!
    static let useRemote = false /* true = load từ GitHub Pages; false = chạy offline */

    func makeUIView(context: Context) -> WKWebView {
        let cfg = WKWebViewConfiguration()

        if Self.useRemote {
            let req = URLRequest(url: Self.remoteURL, cachePolicy: .reloadIgnoringLocalCacheData)
            let web = WKWebView(frame: .zero, configuration: cfg)
            web.load(req)
            return configure(web)
        }

        /* Load từ bundle: file index.html được kéo vào project Xcode (xem README bước 2) */
        if let url = Bundle.main.url(forResource: "index", withExtension: "html") {
            let web = WKWebView(frame: .zero, configuration: cfg)
            web.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
            return configure(web)
        }

        /* Không tìm thấy index.html trong bundle -> hiện cảnh báo */
        let web = WKWebView(frame: .zero, configuration: cfg)
        web.loadHTMLString("""
        <html><body style="font-family:-apple-system;display:grid;place-items:center;height:100vh;background:#07090d;color:#eaeef4;text-align:center;padding:24px">
        <div><h2>⚠️ Chưa thêm index.html</h2>
        <p style="color:#b7c1d1">Mở Xcode → kéo file <b>index.html</b> (nằm ở thư mục gốc repo)<br>
        vào mục <b>WDTAI → Copy items if needed</b> → Build lại.</p>
        <p style="color:#7d8899">Hoặc đổi <code>useRemote = true</code> trong ContentView.swift<br>
        để load trực tiếp từ GitHub Pages.</p></div>
        </body></html>
        """, baseURL: nil)
        return web
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    private func configure(_ web: WKWebView) -> WKWebView {
        web.isOpaque = false
        web.backgroundColor = UIColor(red: 0.027, green: 0.035, blue: 0.051, alpha: 1) /* #07090d */
        web.scrollView.bounces = false /* chống overshoot kéo giật kiểu web */
        web.scrollView.contentInsetAdjustmentBehavior = .never /* thông số dùng với ignoresSafeArea */
        web.allowsBackForwardGestures = false
        return web
    }
}
