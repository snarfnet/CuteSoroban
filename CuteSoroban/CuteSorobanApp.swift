import SwiftUI
import GoogleMobileAds

@main
struct CuteSorobanApp: App {
    init() {
        GADMobileAds.sharedInstance().start { _ in }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .preferredColorScheme(.light)
        }
    }
}
