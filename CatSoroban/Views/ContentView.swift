import SwiftUI
import SpriteKit

struct ContentView: View {
    @StateObject private var sorobanState = SorobanState()
    @State private var scene = CatSorobanScene(size: CGSize(width: 800, height: 400))

    var body: some View {
        GeometryReader { geo in
            ZStack {
                Image("CatBackground")
                    .resizable()
                    .scaledToFill()
                    .ignoresSafeArea()
                    .overlay(Color.white.opacity(0.10).ignoresSafeArea())

                LinearGradient(
                    colors: [
                        Color.white.opacity(0.10),
                        Color(red: 1.0, green: 0.74, blue: 0.84).opacity(0.18),
                        Color(red: 1.0, green: 0.88, blue: 0.70).opacity(0.12)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()

                VStack(spacing: 0) {
                    displayBar
                        .frame(height: 62)

                    SpriteView(scene: configuredScene(size: CGSize(
                        width: geo.size.width,
                        height: max(240, geo.size.height - 62 - 64)
                    )), options: [.allowsTransparency])
                    .ignoresSafeArea(edges: .horizontal)

                    bottomBar
                        .frame(height: 64)
                }
            }
        }
    }

    private var displayBar: some View {
        HStack {
            Spacer()
            Text(sorobanState.displayValue)
                .font(.system(size: 34, weight: .heavy, design: .rounded))
                .foregroundStyle(
                    LinearGradient(
                        colors: [
                            Color(red: 0.95, green: 0.35, blue: 0.62),
                            Color(red: 0.92, green: 0.55, blue: 0.26)
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
            ZStack {
                Color.white.opacity(0.70)
                LinearGradient(
                    colors: [
                        Color(red: 1.0, green: 0.70, blue: 0.84).opacity(0.22),
                        Color(red: 0.72, green: 0.90, blue: 1.0).opacity(0.16)
                    ],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            }
            .shadow(color: Color.white.opacity(0.55), radius: 8, y: 2)
        )
    }

    private var bottomBar: some View {
        HStack {
            Button {
                NotificationCenter.default.post(name: .catSorobanReset, object: nil)
                sorobanState.displayValue = "0"
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: "arrow.counterclockwise")
                        .font(.system(size: 16, weight: .semibold))
                    Text("Reset")
                        .font(.system(size: 14, weight: .bold, design: .rounded))
                }
                .foregroundStyle(Color(red: 0.88, green: 0.34, blue: 0.58))
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(
                    Capsule()
                        .fill(Color.white.opacity(0.86))
                        .overlay(
                            Capsule()
                                .stroke(Color.white.opacity(0.85), lineWidth: 1)
                        )
                        .shadow(color: Color(red: 1.0, green: 0.48, blue: 0.70).opacity(0.28), radius: 8, y: 3)
                )
            }

            Spacer()

            Text("Cute Soroban")
                .font(.system(size: 15, weight: .bold, design: .rounded))
                .foregroundStyle(Color(red: 0.88, green: 0.34, blue: 0.58))
                .lineLimit(1)

            Spacer()

            Color.clear.frame(width: 80, height: 38)
        }
        .padding(.horizontal, 12)
        .background(Color.white.opacity(0.58))
    }

    private func configuredScene(size: CGSize) -> CatSorobanScene {
        if scene.size != size {
            scene.size = size
        }
        scene.scaleMode = .resizeFill
        scene.sorobanState = sorobanState
        return scene
    }
}

class SorobanState: ObservableObject {
    @Published var displayValue: String = "0"
}

extension Notification.Name {
    static let catSorobanReset = Notification.Name("catSorobanReset")
}
