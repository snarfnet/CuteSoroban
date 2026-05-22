import SpriteKit

class CatSorobanScene: SKScene {

    private let rodCount = 13
    private let earthBeadsPerRod = 4

    weak var sorobanState: SorobanState?
    private var rods: [CatSorobanRod] = []
    private var soundManager = SoundManager()
    private var draggedBead: CatBeadNode?
    private var activeTouch: UITouch?
    private var dragStartY: CGFloat = 0
    private var didRegisterNotifications = false

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
        backgroundColor = .clear
        view.backgroundColor = .clear
        view.allowsTransparency = true
        view.isMultipleTouchEnabled = false
        rebuildSoroban()
        observeNotifications()
    }

    override func didChangeSize(_ oldSize: CGSize) {
        guard oldSize != size, view != nil else { return }
        let snapshot = rods.map { ($0.heavenActive, $0.earthActive) }
        rebuildSoroban(restoring: snapshot)
    }

    private func rebuildSoroban(restoring snapshot: [([Bool], [Bool])] = []) {
        removeAllChildren()
        calculateLayout()
        buildBackground()
        buildFrame()
        buildRods()
        restore(snapshot)
        updateValue()
    }

    override func willMove(from view: SKView) {
        NotificationCenter.default.removeObserver(self)
        didRegisterNotifications = false
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
        let bg = SKSpriteNode(imageNamed: "CatBackground")
        let scale = max(size.width / max(bg.size.width, 1), size.height / max(bg.size.height, 1))
        bg.size = CGSize(width: bg.size.width * scale, height: bg.size.height * scale)
        bg.position = CGPoint(x: size.width / 2, y: size.height / 2)
        bg.alpha = 0.82
        bg.zPosition = -20
        addChild(bg)

        let wash = SKShapeNode(rect: CGRect(origin: .zero, size: size))
        wash.fillColor = SKColor(white: 1, alpha: 0.10)
        wash.strokeColor = .clear
        wash.zPosition = -19
        addChild(wash)

        for i in 0..<30 {
            let seed = Double(i)
            let x = pseudo(seed, 127.1, 311.7) * size.width
            let y = pseudo(seed, 269.5, 183.3) * size.height
            let sz = pseudo(seed, 78.23, 91.4) * 5 + 2
            let alpha = pseudo(seed, 42.17, 17.9) * 0.22 + 0.08

            let circle = SKShapeNode(circleOfRadius: sz)
            circle.position = CGPoint(x: x, y: y)
            circle.fillColor = SKColor(
                red: CGFloat(0.92 + pseudo(seed, 13.0, 7.0) * 0.08),
                green: CGFloat(0.82 + pseudo(seed, 23.0, 11.0) * 0.16),
                blue: CGFloat(0.92 + pseudo(seed, 31.0, 17.0) * 0.08),
                alpha: CGFloat(alpha)
            )
            circle.strokeColor = .clear
            circle.zPosition = -10
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

        let shadow = SKShapeNode(rect: frameRect.offsetBy(dx: 0, dy: -3), cornerRadius: 16)
        shadow.fillColor = SKColor(red: 0.78, green: 0.42, blue: 0.50, alpha: 0.16)
        shadow.strokeColor = .clear
        shadow.zPosition = -2
        addChild(shadow)

        let bg = SKShapeNode(rect: frameRect.insetBy(dx: frameThickness / 2, dy: frameThickness / 2), cornerRadius: 14)
        bg.fillColor = SKColor(red: 1.0, green: 0.95, blue: 0.965, alpha: 0.70)
        bg.strokeColor = SKColor(white: 1.0, alpha: 0.5)
        bg.lineWidth = 1
        bg.zPosition = 0
        addChild(bg)

        let border = SKShapeNode(rect: frameRect, cornerRadius: 16)
        border.strokeColor = SKColor(red: 1.0, green: 0.62, blue: 0.76, alpha: 1)
        border.lineWidth = frameThickness
        border.fillColor = .clear
        border.zPosition = 5
        addChild(border)

        let inner = SKShapeNode(rect: frameRect.insetBy(dx: frameThickness * 0.6, dy: frameThickness * 0.6), cornerRadius: 12)
        inner.strokeColor = SKColor(white: 1.0, alpha: 0.75)
        inner.lineWidth = 1.5
        inner.fillColor = .clear
        inner.zPosition = 6
        addChild(inner)

        let beamRect = CGRect(x: frameRect.minX, y: beamY - beamThickness / 2, width: frameRect.width, height: beamThickness)
        let beam = SKShapeNode(rect: beamRect, cornerRadius: 4)
        beam.fillColor = SKColor(red: 1.0, green: 0.75, blue: 0.84, alpha: 1)
        beam.strokeColor = SKColor(red: 0.98, green: 0.52, blue: 0.70, alpha: 0.78)
        beam.lineWidth = 1
        beam.zPosition = 10
        addChild(beam)

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
            rod.strokeColor = SKColor(red: 0.96, green: 0.58, blue: 0.16, alpha: 0.95)
            rod.lineWidth = 2.4
            rod.zPosition = 1
            addChild(rod)

            let glint = SKShapeNode()
            let gp = CGMutablePath()
            gp.move(to: CGPoint(x: x - 0.5, y: bottomFrameY + 10))
            gp.addLine(to: CGPoint(x: x - 0.5, y: topFrameY - 10))
            glint.path = gp
            glint.strokeColor = SKColor(red: 1.0, green: 0.92, blue: 0.55, alpha: 0.45)
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
            let rod = CatSorobanRod(
                index: i, x: x, beamY: beamY, topY: heavenTopY, bottomY: earthBottomY,
                beadWidth: beadWidth, beadHeight: beadHeight, beadSpacing: beadSpacing
            )
            rods.append(rod)

            let heavenBead = CatBeadNode.create(
                width: beadWidth, height: beadHeight, isHeaven: true, rodIndex: i, beadIndex: 0
            )
            heavenBead.position = rod.heavenRestPosition(active: false)
            heavenBead.zPosition = 20
            addChild(heavenBead)
            rod.heavenBeads.append(heavenBead)

            for j in 0..<earthBeadsPerRod {
                let earthBead = CatBeadNode.create(
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
        guard activeTouch == nil, let touch = touches.first else { return }
        let location = touch.location(in: self)

        if let bead = bead(at: location) {
            activeTouch = touch
            draggedBead = bead
            dragStartY = location.y
        }
    }

    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let touch = activeTouch, touches.contains(touch), let bead = draggedBead else { return }
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
            if targetActive {
                moveEarthBeads(rod: rod, touchedIndex: beadIdx, active: true)
                dragStartY = location.y
            } else if targetInactive {
                moveEarthBeads(rod: rod, touchedIndex: beadIdx, active: false)
                dragStartY = location.y
            }
        }
    }

    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let touch = activeTouch, touches.contains(touch) else { return }
        if let bead = draggedBead {
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
                    moveEarthBeads(rod: rod, touchedIndex: beadIdx, active: !rod.earthActive[beadIdx])
                }
            }
        }
        activeTouch = nil
        draggedBead = nil
    }

    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        if let touch = activeTouch, touches.contains(touch) {
            activeTouch = nil
            draggedBead = nil
        }
    }

    // MARK: - Bead Movement

    private func moveHeavenBead(rod: CatSorobanRod, active: Bool) {
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

    private func moveEarthBead(rod: CatSorobanRod, index: Int, active: Bool) {
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

    private func moveEarthBeads(rod: CatSorobanRod, touchedIndex: Int, active: Bool) {
        var changed = false
        let indices: [Int] = active
            ? Array(touchedIndex..<earthBeadsPerRod)
            : Array(0...touchedIndex)
        for index in indices {
            if rod.earthActive[index] != active {
                moveEarthBeadSilently(rod: rod, index: index, active: active)
                changed = true
            }
        }
        if changed {
            soundManager.playClick()
            updateValue()
        }
    }

    private func moveEarthBeadSilently(rod: CatSorobanRod, index: Int, active: Bool) {
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
        guard !didRegisterNotifications else { return }
        didRegisterNotifications = true
        NotificationCenter.default.addObserver(
            forName: .catSorobanReset, object: nil, queue: .main
        ) { [weak self] _ in
            self?.resetSoroban()
        }
    }

    private func bead(at location: CGPoint) -> CatBeadNode? {
        let allBeads = rods.flatMap { $0.heavenBeads + $0.earthBeads }
        var nearest: CatBeadNode?
        var nearestDistance = CGFloat.greatestFiniteMagnitude

        for bead in allBeads {
            guard bead.stableHitFrame.contains(location) else { continue }
            let dx = bead.position.x - location.x
            let dy = bead.position.y - location.y
            let distance = dx * dx + dy * dy
            if distance < nearestDistance {
                nearest = bead
                nearestDistance = distance
            }
        }
        return nearest
    }

    private func restore(_ snapshot: [([Bool], [Bool])]) {
        guard snapshot.count == rods.count else { return }
        for (rodIndex, state) in snapshot.enumerated() {
            let rod = rods[rodIndex]
            rod.heavenActive = state.0
            rod.earthActive = state.1
            rod.heavenBeads[0].position = rod.heavenRestPosition(active: rod.heavenActive[0])
            for index in 0..<earthBeadsPerRod {
                rod.earthBeads[index].position = rod.earthRestPosition(index: index, active: rod.earthActive[index])
            }
        }
    }
}
