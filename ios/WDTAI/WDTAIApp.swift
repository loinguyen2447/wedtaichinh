import SwiftUI

@main
struct WDTAIApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .preferredColorScheme(nil) /* để trang web tự chọn dark/light theo thiết bị */
        }
    }
}
