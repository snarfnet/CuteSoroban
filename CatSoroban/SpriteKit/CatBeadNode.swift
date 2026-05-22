import SpriteKit

class CatBeadNode: SKNode {
    var isHeaven: Bool = false
    var rodIndex: Int = 0
    var beadIndex: Int = 0
    var stableHitSize: CGSize = .zero

    var stableHitFrame: CGRect {
        CGRect(
            x: position.x - stableHitSize.width / 2,
            y: position.y - stableHitSize.height / 2,
            width: stableHitSize.width,
            height: stableHitSize.height
        )
    }

    static func create(width: CGFloat, height: CGFloat, isHeaven: Bool, rodIndex: Int, beadIndex: Int) -> CatBeadNode {
        let node = CatBeadNode()
        node.isHeaven = isHeaven
        node.rodIndex = rodIndex
        node.beadIndex = beadIndex
        node.isUserInteractionEnabled = false
        node.stableHitSize = CGSize(width: width * 1.14, height: height * 1.72)

        let shadow = SKShapeNode(ellipseOf: CGSize(width: width * 0.95, height: height * 0.30))
        shadow.position = CGPoint(x: 0, y: -height * 0.52)
        shadow.fillColor = SKColor(red: 0.55, green: 0.32, blue: 0.40, alpha: 0.18)
        shadow.strokeColor = .clear
        shadow.zPosition = -2
        node.addChild(shadow)

        let bead = SKSpriteNode(imageNamed: catBeadImageName(rodIndex: rodIndex, beadIndex: beadIndex, isHeaven: isHeaven))
        bead.size = CGSize(width: width * 1.22, height: height * 1.78)
        bead.position = CGPoint(x: 0, y: height * 0.10)
        bead.zPosition = 1
        node.addChild(bead)

        let pawDot = SKShapeNode(circleOfRadius: max(1.8, width * 0.045))
        pawDot.fillColor = SKColor(white: 1, alpha: 0.62)
        pawDot.strokeColor = SKColor(red: 1, green: 0.64, blue: 0.74, alpha: 0.55)
        pawDot.lineWidth = 0.6
        pawDot.position = CGPoint(x: width * 0.34, y: -height * 0.34)
        pawDot.zPosition = 2
        node.addChild(pawDot)

        return node
    }

    private static func catBeadImageName(rodIndex: Int, beadIndex: Int, isHeaven: Bool) -> String {
        let names = ["CatBeadOrange", "CatBeadLavender", "CatBeadCalico"]
        let offset = isHeaven ? 1 : beadIndex
        return names[(rodIndex + offset) % names.count]
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
