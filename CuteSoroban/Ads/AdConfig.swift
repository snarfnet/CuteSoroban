import Foundation

enum AdConfig {
    #if DEBUG
    static let bannerAdUnitID = "ca-app-pub-3940256099942544/2934735716"
    #else
    static let bannerAdUnitID = "ca-app-pub-9404799280370656/PLACEHOLDER"
    #endif

    static let appID = "ca-app-pub-9404799280370656~PLACEHOLDER"
}
