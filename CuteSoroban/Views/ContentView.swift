import SwiftUI
import SpriteKit

struct ContentView: View {
    @StateObject private var sorobanState = SorobanState()

    var body: some View {
        GeometryReader { geo in
            ZStack {
                // Cute gradient background
                LinearGradient(
                    colors: [
                        Color(red: 1.0, green: 0.95, blue: 0.97),
                        Color(red: 0.96, green: 0.94, blue: 1.0),
                        Color(red: 1.0, green: 0.97, blue: 0.95)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()

                VStack(spacing: 0) {
                    // Display
                    displayBar
                        .frame(height: 52)

                    // Soroban
                    SpriteView(scene: makeScene(size: CGSize(
                        width: geo.size.width,
                        height: geo.size.height - 52 - 60
                    )), options: [.allowsTransparency])
                    .ignoresSafeArea(edges: .horizontal)

                    // Bottom bar
                    bottomBar
                        .frame(height: 60)
                }
            }
        }
    }

    private var displayBar: some View {
        HStack {
            Spacer()
            Text(sorobanState.displayValue)
                .font(.system(size: 30, weight: .medium, design: .rounded))
                .foregroundStyle(
                    LinearGradient(
                        colors: [
                            Color(red: 0.82, green: 0.55, blue: 0.72),
                            Color(red: 0.62, green: 0.52, blue: 0.82)
                        ],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .lineLimit(1)
                .minimumScaleFactor(0.5)
                .padding(.horizontal, 20)
            Spacer()
        }
        .frame(maxWidth: .infinity)
        .background(
            Color.white.opacity(0.82)
                .shadow(.inner(color: Color(red: 1.0, green: 0.8, blue: 0.85).opacity(0.4), radius: 8, y: 2))
        )
    }

    private var bottomBar: some View {
        HStack {
            Button {
                NotificationCenter.default.post(name: .cutesorobanReset, object: nil)
                sorobanState.displayValue = "0"
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: "arrow.counterclockwise")
                        .font(.system(size: 16, weight: .semibold))
                    Text("Reset")
                        .font(.system(size: 14, weight: .bold, design: .rounded))
                }
                .foregroundStyle(Color(red: 0.75, green: 0.55, blue: 0.72))
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(
                    Capsule()
                        .fill(Color.white.opacity(0.85))
                        .shadow(color: Color(red: 1.0, green: 0.75, blue: 0.82).opacity(0.4), radius: 6, y: 2)
                )
            }

            Spacer()

            // Ad banner
            BannerAdView(adUnitID: AdConfig.bannerAdUnitID)
                .frame(width: 320, height: 50)

            Spacer()

            Color.clear.frame(width: 80, height: 38)
        }
        .padding(.horizontal, 12)
        .background(Color.white.opacity(0.62))
    }

    private func makeScene(size: CGSize) -> CuteSorobanScene {
        let scene = CuteSorobanScene(size: size)
        scene.scaleMode = .resizeFill
        scene.sorobanState = sorobanState
        return scene
    }
}

class SorobanState: ObservableObject {
    @Published var displayValue: String = "0"
}

extension Notification.Name {
    static let cutesorobanReset = Notification.Name("cutesorobanReset")
}
