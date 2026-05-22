import AVFoundation
import UIKit

final class SoundManager {
    private var clickID: SystemSoundID = 0
    private var resetID: SystemSoundID = 0
    private var useHaptics = true

    init() {
        // Use system sounds for cute clicks
        clickID = 1104  // soft tap
        resetID = 1105  // gentle sweep
    }

    func playClick() {
        AudioServicesPlaySystemSound(clickID)
        if useHaptics {
            UIImpactFeedbackGenerator(style: .light).impactOccurred()
        }
    }

    func playReset() {
        AudioServicesPlaySystemSound(resetID)
        if useHaptics {
            UINotificationFeedbackGenerator().notificationOccurred(.success)
        }
    }
}
