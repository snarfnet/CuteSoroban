import SpriteKit

class CuteSorobanScene: SKScene {

    private let rodCount = 13
    private let earthBeadsPerRod = 4

    weak var sorobanState: SorobanState?
    private var rods: [CuteSorobanRod] = []
    private var soundManager = SoundManager()
    private var draggedBead: CuteBeadNode?
    private var dragStartY: CGFloat = 0

    private var frameRect = CGRect.zero
    private var beamY: CGFloat = 0
    private var rodSpacing: CGFloat = 0
    private var rodStartX: CGFloat = 0
    private var beadWidth: CGFloat = 0
    private var beadHeight: CGFloat = 0
    private var topFrameY: CGFloat = 0
    private var bottomFrameY: CGFloat = 0
    private var heavenTopY: CGFloat = 0
    private var earthBottomY: CGFloat = 0
    private var beadSpacing: CGFloat = 2

    // MARK: - Lifecycle

    override func didMove(to view: SKView) {
        backgroundColor = SKColor(red: 1.0, green: 0.96, blue: 0.97, alpha: 1) // soft pink-white
        calculateLayout()
        buildBackground()
        buildFrame()
        buildRods()
        observeNotifications()
    }

    override func willMove(from view: SKView) {
        NotificationCenter.default.removeObserver(self)
    }

    // MARK: - Layout

    private func calculateLayout() {
        let margin: CGFloat = 16
        let sorobanWidth = size.width - margin * 2
        let sorobanHeight = size.height * 0.88

        let sorobanY = (size.height - sorobanHeight) / 2

        frameRect = CGRect(x: margin, y: sorobanY, width: sorobanWidth, height: sorobanHeight)

        let beamRatio: CGFloat = 0.30
        beamY = frameRect.minY + sorobanHeight * (1 - beamRatio)
        topFrameY = frameRect.maxY
        bottomFrameY = frameRect.minY

        rodSpacing = sorobanWidth / CGFloat(rodCount + 1)
        rodStartX = frameRect.minX + rodSpacing

        beadWidth = rodSpacing * 0.82
        beadHeight = min(sorobanHeight * 0.065, beadWidth * 0.6)
        beadSpacing = beadHeight * 0.15

        heavenTopY = topFrameY - beadHeight * 0.8
        earthBottomY = bottomFrameY + beadHeight * 0.8
    }

    // MARK: - Cute Background

    private func buildBackground() {
        // Scattered tiny hearts / stars
        let decorations = ["heart.fill", "star.fill", "sparkle"]
        for i in 0..<18 {
            let seed = Double(i)
            let x = pseudo(seed, 127.1, 311.7) * size.width
            let y = pseudo(seed, 269.5, 183.3) * size.height
            let sz = pseudo(seed, 78.23, 91.4) * 8 + 4
            let alpha = pseudo(seed, 42.17, 17.9) * 0.12 + 0.04

            let circle = SKShapeNode(circleOfRadius: sz)
            circle.position = CGPoint(x: x, y: y)
            circle.fillColor = SKColor(
                red: CGFloat(0.9 + pseudo(seed, 13.0, 7.0) * 0.1),
                green: CGFloat(0.7 + pseudo(seed, 23.0, 11.0) * 0.2),
                blue: CGFloat(0.8 + pseudo(seed, 31.0, 17.0) * 0.2),
                alpha: CGFloat(alpha)
            )
            circle.strokeColor = .clear
            circle.zPosition = -5
            addChild(circle)
        }
    }

    private func pseudo(_ seed: Double, _ a: Double, _ b: Double) -> Double {
        (sin(seed * a + b) * 43758.5453).truncatingRemainder(dividingBy: 1.0).magnitude
    }

    // MARK: - Cute Frame

    private func buildFrame() {
        let frameThickness: CGFloat = 10
        let beamThickness: CGFloat = 8

        // Soft shadow
        let shadow = SKShapeNode(rect: frameRect.offsetBy(dx: 0, dy: -3), cornerRadius: 16)
        shadow.fillColor = SKColor(red: 0.8, green: 0.7, blue: 0.85, alpha: 0.18)
        shadow.strokeColor = .clear
        shadow.zPosition = -2
        addChild(shadow)

        // Frame background - soft cream
        let bg = SKShapeNode(rect: frameRect.insetBy(dx: frameThickness / 2, dy: frameThickness / 2), cornerRadius: 14)
        bg.fillColor = SKColor(red: 1.0, green: 0.98, blue: 0.95, alpha: 1)
        bg.strokeColor = .clear
        bg.zPosition = 0
        addChild(bg)

        // Frame border - pastel pink
        let border = SKShapeNode(rect: frameRect, cornerRadius: 16)
        border.strokeColor = SKColor(red: 1.0, green: 0.75, blue: 0.80, alpha: 1)
        border.lineWidth = frameThickness
        border.fillColor = .clear
        border.zPosition = 5
        addChild(border)

        // Inner glow line
        let inner = SKShapeNode(rect: frameRect.insetBy(dx: frameThickness * 0.6, dy: frameThickness * 0.6), cornerRadius: 12)
        inner.strokeColor = SKColor(white: 1.0, alpha: 0.55)
        inner.lineWidth = 1.5
        inner.fillColor = .clear
        inner.zPosition = 6
        addChild(inner)

        // Beam - pastel lavender
        let beamRect = CGRect(x: frameRect.minX, y: beamY - beamThickness / 2, width: frameRect.width, height: beamThickness)
        let beam = SKShapeNode(rect: beamRect, cornerRadius: 4)
        beam.fillColor = SKColor(red: 0.85, green: 0.78, blue: 0.95, alpha: 1)
        beam.strokeColor = SKColor(red: 0.75, green: 0.65, blue: 0.88, alpha: 1)
        beam.lineWidth = 1
        beam.zPosition = 10
        addChild(beam)

        // Beam highlight
        let beamHL = SKShapeNode(rect: CGRect(x: beamRect.minX + 4, y: beamRect.maxY - 1.5, width: beamRect.width - 8, height: 1))
        beamHL.fillColor = SKColor(white: 1.0, alpha: 0.55)
        beamHL.strokeColor = .clear
        beamHL.zPosition = 11
        addChild(beamHL)

        // Dot markers - cute pink dots
        let dotPositions = [3, 6, 9]
        for pos in dotPositions where pos < rodCount {
            let dotX = rodStartX + CGFloat(pos) * rodSpacing
            let dot = SKShapeNode(circleOfRadius: 3.2)
            dot.position = CGPoint(x: dotX, y: beamY)
            dot.fillColor = SKColor(red: 1.0, green: 0.65, blue: 0.72, alpha: 1)
            dot.strokeColor = SKColor(red: 0.88, green: 0.50, blue: 0.58, alpha: 0.5)
            dot.lineWidth = 0.8
            dot.zPosition = 12
            addChild(dot)
        }

        // Rods - thin pastel lines
        for i in 0..<rodCount {
            let x = rodStartX + CGFloat(i) * rodSpacing

            let rod = SKShapeNode()
            let path = CGMutablePath()
            path.move(to: CGPoint(x: x, y: bottomFrameY + 6))
            path.addLine(to: CGPoint(x: x, y: topFrameY - 6))
            rod.path = path
            rod.strokeColor = SKColor(red: 0.82, green: 0.78, blue: 0.88, alpha: 0.72)
            rod.lineWidth = 1.8
            rod.zPosition = 1
            addChild(rod)

            // Subtle glint
            let glint = SKShapeNode()
            let gp = CGMutablePath()
            gp.move(to: CGPoint(x: x - 0.5, y: bottomFrameY + 10))
            gp.addLine(to: CGPoint(x: x - 0.5, y: topFrameY - 10))
            glint.path = gp
            glint.strokeColor = SKColor(white: 1.0, alpha: 0.32)
            glint.lineWidth = 0.6
            glint.zPosition = 2
            addChild(glint)
        }
    }

    // MARK: - Build Beads

    private func buildRods() {
        rods = []
        for i in 0..<rodCount {
            let x = rodStartX + CGFloat(i) * rodSpacing
            let rod = CuteSorobanRod(
                index: i, x: x, beamY: beamY, topY: heavenTopY, bottomY: earthBottomY,
                beadWidth: beadWidth, beadHeight: beadHeight, beadSpacing: beadSpacing
            )
            rods.append(rod)

            let heavenBead = CuteBeadNode.create(
                width: beadWidth, height: beadHeight, isHeaven: true, rodIndex: i, beadIndex: 0
            )
            heavenBead.position = rod.heavenRestPosition(active: false)
            heavenBead.zPosition = 20
            addChild(heavenBead)
            rod.heavenBeads.append(heavenBead)

            for j in 0..<earthBeadsPerRod {
                let earthBead = CuteBeadNode.create(
                    width: beadWidth, height: beadHeight, isHeaven: false, rodIndex: i, beadIndex: j
                )
                earthBead.position = rod.earthRestPosition(index: j, active: false)
                earthBead.zPosition = 20
                addChild(earthBead)
                rod.earthBeads.append(earthBead)
            }
        }
    }

    // MARK: - Touch Handling

    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let touch = touches.first else { return }
        let location = touch.location(in: self)

        let tappedNodes = nodes(at: location)
        for node in tappedNodes {
            if let bead = node as? CuteBeadNode ?? node.parent as? CuteBeadNode {
                draggedBead = bead
                dragStartY = location.y
                return
            }
        }
    }

    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let touch = touches.first, let bead = draggedBead else { return }
        let location = touch.location(in: self)
        let deltaY = location.y - dragStartY

        let rodIdx = bead.rodIndex
        guard rodIdx < rods.count else { return }
        let rod = rods[rodIdx]

        if bead.isHeaven {
            let targetActive = deltaY < -beadHeight * 0.3
            let targetInactive = deltaY > beadHeight * 0.3
            if targetActive && !rod.heavenActive[0] {
                moveHeavenBead(rod: rod, active: true)
            } else if targetInactive && rod.heavenActive[0] {
                moveHeavenBead(rod: rod, active: false)
            }
        } else {
            let beadIdx = bead.beadIndex
            let targetActive = deltaY > beadHeight * 0.3
            let targetInactive = deltaY < -beadHeight * 0.3
            if targetActive && !rod.earthActive[beadIdx] {
                moveEarthBead(rod: rod, index: beadIdx, active: true)
                dragStartY = location.y
            } else if targetInactive && rod.earthActive[beadIdx] {
                moveEarthBead(rod: rod, index: beadIdx, active: false)
                dragStartY = location.y
            }
        }
    }

    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        if let bead = draggedBead {
            guard let touch = touches.first else { draggedBead = nil; return }
            let location = touch.location(in: self)
            let deltaY = abs(location.y - dragStartY)

            if deltaY < beadHeight * 0.3 {
                let rodIdx = bead.rodIndex
                guard rodIdx < rods.count else { draggedBead = nil; return }
                let rod = rods[rodIdx]

                if bead.isHeaven {
                    moveHeavenBead(rod: rod, active: !rod.heavenActive[0])
                } else {
                    let beadIdx = bead.beadIndex
                    moveEarthBead(rod: rod, index: beadIdx, active: !rod.earthActive[beadIdx])
                }
            }
        }
        draggedBead = nil
    }

    // MARK: - Bead Movement

    private func moveHeavenBead(rod: CuteSorobanRod, active: Bool) {
        guard rod.heavenActive[0] != active else { return }
        rod.heavenActive[0] = active
        let bead = rod.heavenBeads[0]
        let target = rod.heavenRestPosition(active: active)

        let move = SKAction.move(to: target, duration: 0.10)
        move.timingMode = .easeOut
        let bounce = SKAction.sequence([
            SKAction.scale(to: 1.08, duration: 0.05),
            SKAction.scale(to: 1.0, duration: 0.06)
        ])
        bead.run(SKAction.group([move, bounce]))
        soundManager.playClick()
        updateValue()
    }

    private func moveEarthBead(rod: CuteSorobanRod, index: Int, active: Bool) {
        guard rod.earthActive[index] != active else { return }
        rod.earthActive[index] = active
        let bead = rod.earthBeads[index]
        let target = rod.earthRestPosition(index: index, active: active)

        let move = SKAction.move(to: target, duration: 0.08)
        move.timingMode = .easeOut
        let bounce = SKAction.sequence([
            SKAction.scale(to: 1.06, duration: 0.04),
            SKAction.scale(to: 1.0, duration: 0.05)
        ])
        bead.run(SKAction.group([move, bounce]))
        soundManager.playClick()
        updateValue()
    }

    // MARK: - Value

    private func updateValue() {
        var totalValue: Int64 = 0
        for (i, rod) in rods.enumerated() {
            let placeValue = pow(10.0, Double(rodCount - 1 - i))
            var rodValue = 0
            if rod.heavenActive[0] { rodValue += 5 }
            for j in 0..<earthBeadsPerRod {
                if rod.earthActive[j] { rodValue += 1 }
            }
            totalValue += Int64(Double(rodValue) * placeValue)
        }

        let formatted = formatNumber(totalValue)
        DispatchQueue.main.async { [weak self] in
            self?.sorobanState?.displayValue = formatted
        }
    }

    private func formatNumber(_ value: Int64) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.groupingSeparator = ","
        return formatter.string(from: NSNumber(value: value)) ?? "0"
    }

    // MARK: - Reset

    private func resetSoroban() {
        for rod in rods {
            if rod.heavenActive[0] { moveHeavenBead(rod: rod, active: false) }
            for j in 0..<earthBeadsPerRod {
                if rod.earthActive[j] { moveEarthBead(rod: rod, index: j, active: false) }
            }
        }
        soundManager.playReset()
    }

    private func observeNotifications() {
        NotificationCenter.default.addObserver(
            forName: .cutesorobanReset, object: nil, queue: .main
        ) { [weak self] _ in
            self?.resetSoroban()
        }
    }
}
