import SpriteKit

class CuteBeadNode: SKNode {
    var isHeaven: Bool = false
    var rodIndex: Int = 0
    var beadIndex: Int = 0

    static func create(width: CGFloat, height: CGFloat, isHeaven: Bool, rodIndex: Int, beadIndex: Int) -> CuteBeadNode {
        let node = CuteBeadNode()
        node.isHeaven = isHeaven
        node.rodIndex = rodIndex
        node.beadIndex = beadIndex
        node.isUserInteractionEnabled = false

        // Soft shadow
        let shadow = SKShapeNode(ellipseOf: CGSize(width: width * 0.8, height: height * 0.3))
        shadow.position = CGPoint(x: 1, y: -height * 0.12)
        shadow.fillColor = SKColor(red: 0.6, green: 0.5, blue: 0.7, alpha: 0.18)
        shadow.strokeColor = .clear
        shadow.zPosition = -2
        node.addChild(shadow)

        // Round cute bead (not bicone - round pill shape)
        let beadColor = isHeaven ? CutePalette.heavenBead(rodIndex: rodIndex) : CutePalette.earthBead(rodIndex: rodIndex)
        let borderColor = isHeaven ? CutePalette.heavenBorder(rodIndex: rodIndex) : CutePalette.earthBorder(rodIndex: rodIndex)

        let cornerRadius = min(width, height) * 0.42
        let rect = CGRect(x: -width / 2, y: -height / 2, width: width, height: height)
        let shape = SKShapeNode(rect: rect, cornerRadius: cornerRadius)
        shape.fillColor = beadColor
        shape.strokeColor = borderColor
        shape.lineWidth = 1.5
        shape.zPosition = 0
        node.addChild(shape)

        // Glossy highlight (top-left shine)
        let glossW = width * 0.35
        let glossH = height * 0.28
        let gloss = SKShapeNode(ellipseOf: CGSize(width: glossW, height: glossH))
        gloss.position = CGPoint(x: -width * 0.12, y: height * 0.14)
        gloss.fillColor = SKColor(white: 1.0, alpha: 0.42)
        gloss.strokeColor = .clear
        gloss.zPosition = 1
        node.addChild(gloss)

        // Tiny sparkle on heaven beads
        if isHeaven {
            let star = SKShapeNode(circleOfRadius: 2.2)
            star.position = CGPoint(x: width * 0.18, y: height * 0.08)
            star.fillColor = SKColor(white: 1.0, alpha: 0.72)
            star.strokeColor = .clear
            star.zPosition = 2
            node.addChild(star)
        }

        // Center hole (cute small dot)
        let hole = SKShapeNode(circleOfRadius: max(1.4, width * 0.035))
        hole.fillColor = SKColor(white: 0.0, alpha: 0.12)
        hole.strokeColor = SKColor(white: 1.0, alpha: 0.18)
        hole.lineWidth = 0.5
        hole.zPosition = 3
        node.addChild(hole)

        return node
    }
}

// Pastel color palette for beads
enum CutePalette {
    // Pastel rainbow cycle for earth beads
    private static let earthColors: [(fill: SKColor, border: SKColor)] = [
        (SKColor(red: 1.00, green: 0.72, blue: 0.77, alpha: 1), SKColor(red: 0.92, green: 0.55, blue: 0.62, alpha: 1)), // pink
        (SKColor(red: 1.00, green: 0.82, blue: 0.68, alpha: 1), SKColor(red: 0.92, green: 0.68, blue: 0.50, alpha: 1)), // peach
        (SKColor(red: 1.00, green: 0.95, blue: 0.70, alpha: 1), SKColor(red: 0.90, green: 0.82, blue: 0.50, alpha: 1)), // lemon
        (SKColor(red: 0.72, green: 0.95, blue: 0.78, alpha: 1), SKColor(red: 0.55, green: 0.82, blue: 0.62, alpha: 1)), // mint
        (SKColor(red: 0.72, green: 0.85, blue: 1.00, alpha: 1), SKColor(red: 0.55, green: 0.70, blue: 0.92, alpha: 1)), // sky
        (SKColor(red: 0.82, green: 0.75, blue: 1.00, alpha: 1), SKColor(red: 0.65, green: 0.58, blue: 0.92, alpha: 1)), // lavender
    ]

    // Heaven beads are slightly more saturated
    private static let heavenColors: [(fill: SKColor, border: SKColor)] = [
        (SKColor(red: 1.00, green: 0.58, blue: 0.65, alpha: 1), SKColor(red: 0.88, green: 0.40, blue: 0.48, alpha: 1)), // rose
        (SKColor(red: 1.00, green: 0.72, blue: 0.52, alpha: 1), SKColor(red: 0.88, green: 0.55, blue: 0.35, alpha: 1)), // coral
        (SKColor(red: 1.00, green: 0.88, blue: 0.52, alpha: 1), SKColor(red: 0.88, green: 0.75, blue: 0.35, alpha: 1)), // gold
        (SKColor(red: 0.55, green: 0.90, blue: 0.65, alpha: 1), SKColor(red: 0.38, green: 0.75, blue: 0.48, alpha: 1)), // green
        (SKColor(red: 0.55, green: 0.75, blue: 1.00, alpha: 1), SKColor(red: 0.38, green: 0.58, blue: 0.88, alpha: 1)), // blue
        (SKColor(red: 0.72, green: 0.60, blue: 1.00, alpha: 1), SKColor(red: 0.55, green: 0.42, blue: 0.88, alpha: 1)), // purple
    ]

    static func earthBead(rodIndex: Int) -> SKColor {
        earthColors[rodIndex % earthColors.count].fill
    }

    static func earthBorder(rodIndex: Int) -> SKColor {
        earthColors[rodIndex % earthColors.count].border
    }

    static func heavenBead(rodIndex: Int) -> SKColor {
        heavenColors[rodIndex % heavenColors.count].fill
    }

    static func heavenBorder(rodIndex: Int) -> SKColor {
        heavenColors[rodIndex % heavenColors.count].border
    }
}
