import AVFoundation
import UIKit

final class SoundManager {
    private var resetID: SystemSoundID = 0
    private let engine = AVAudioEngine()
    private let player = AVAudioPlayerNode()
    private let format = AVAudioFormat(standardFormatWithSampleRate: 44_100, channels: 1)
    private var useHaptics = true

    init() {
        resetID = 1105
        setupAudioEngine()
    }

    func playClick() {
        playMeow()
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

    private func setupAudioEngine() {
        guard let format else { return }
        engine.attach(player)
        engine.connect(player, to: engine.mainMixerNode, format: format)
        try? AVAudioSession.sharedInstance().setCategory(.ambient, mode: .default, options: [.mixWithOthers])
        try? AVAudioSession.sharedInstance().setActive(true)
        try? engine.start()
    }

    private func playMeow() {
        guard let format else { return }
        if !engine.isRunning {
            try? engine.start()
        }

        let sampleRate = format.sampleRate
        let duration = 0.28
        let frameCount = AVAudioFrameCount(sampleRate * duration)
        guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frameCount),
              let channel = buffer.floatChannelData?[0] else {
            return
        }

        buffer.frameLength = frameCount
        for frame in 0..<Int(frameCount) {
            let t = Double(frame) / sampleRate
            let progress = t / duration
            let envelope = sin(progress * .pi)
            let glide = 560.0 - 220.0 * progress + 35.0 * sin(progress * .pi * 2.0)
            let vibrato = 1.0 + 0.018 * sin(2.0 * .pi * 18.0 * t)
            let frequency = glide * vibrato
            let voice = sin(2.0 * .pi * frequency * t)
            let softHarmonic = 0.34 * sin(2.0 * .pi * frequency * 2.02 * t)
            let purr = 0.10 * sin(2.0 * .pi * 82.0 * t) * (1.0 - progress)
            channel[frame] = Float((voice + softHarmonic + purr) * envelope * 0.22)
        }

        player.stop()
        player.scheduleBuffer(buffer, at: nil, options: .interrupts, completionHandler: nil)
        player.play()
    }
}
