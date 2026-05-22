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

        let hitArea = SKShapeNode(ellipseOf: CGSize(width: width * 1.06, height: height * 1.65))
        hitArea.fillColor = .clear
        hitArea.strokeColor = .clear
        hitArea.zPosition = -10
        node.addChild(hitArea)

        let shadow = SKShapeNode(ellipseOf: CGSize(width: width * 0.8, height: height * 0.3))
        shadow.position = CGPoint(x: 1, y: -height * 0.12)
        shadow.fillColor = SKColor(red: 0.6, green: 0.5, blue: 0.7, alpha: 0.18)
        shadow.strokeColor = .clear
        shadow.zPosition = -2
        node.addChild(shadow)

        let beadColor = isHeaven ? CutePalette.heavenBead(rodIndex: rodIndex) : CutePalette.earthBead(rodIndex: rodIndex)
        let borderColor = isHeaven ? CutePalette.heavenBorder(rodIndex: rodIndex) : CutePalette.earthBorder(rodIndex: rodIndex)

        let shape = SKShapeNode(path: crystalPath(width: width, height: height))
        shape.fillColor = beadColor
        shape.strokeColor = borderColor
        shape.lineWidth = 1.35
        shape.zPosition = 0
        node.addChild(shape)

        let facet = SKShapeNode(path: facetPath(width: width, height: height))
        facet.strokeColor = SKColor(white: 1.0, alpha: 0.44)
        facet.lineWidth = 0.7
        facet.fillColor = .clear
        facet.zPosition = 1
        node.addChild(facet)

        let gloss = SKShapeNode(ellipseOf: CGSize(width: width * 0.28, height: height * 0.22))
        gloss.position = CGPoint(x: -width * 0.18, y: height * 0.18)
        gloss.fillColor = SKColor(white: 1.0, alpha: 0.58)
        gloss.strokeColor = .clear
        gloss.zPosition = 2
        node.addChild(gloss)

        let sparkle = SKShapeNode(path: sparklePath(radius: isHeaven ? 3.1 : 2.2))
        sparkle.position = CGPoint(x: width * 0.22, y: height * 0.10)
        sparkle.fillColor = SKColor(white: 1.0, alpha: isHeaven ? 0.86 : 0.58)
        sparkle.strokeColor = .clear
        sparkle.zPosition = 3
        node.addChild(sparkle)

        let hole = SKShapeNode(circleOfRadius: max(1.5, width * 0.036))
        hole.fillColor = SKColor(red: 0.65, green: 0.36, blue: 0.50, alpha: 0.16)
        hole.strokeColor = SKColor(white: 1.0, alpha: 0.26)
        hole.lineWidth = 0.5
        hole.zPosition = 4
        node.addChild(hole)

        return node
    }

    private static func crystalPath(width: CGFloat, height: CGFloat) -> CGPath {
        let w = width / 2
        let h = height / 2
        let path = CGMutablePath()
        path.move(to: CGPoint(x: -w * 0.72, y: 0))
        path.addLine(to: CGPoint(x: -w * 0.42, y: h * 0.76))
        path.addLine(to: CGPoint(x: 0, y: h))
        path.addLine(to: CGPoint(x: w * 0.42, y: h * 0.76))
        path.addLine(to: CGPoint(x: w * 0.72, y: 0))
        path.addLine(to: CGPoint(x: w * 0.42, y: -h * 0.76))
        path.addLine(to: CGPoint(x: 0, y: -h))
        path.addLine(to: CGPoint(x: -w * 0.42, y: -h * 0.76))
        path.closeSubpath()
        return path
    }

    private static func facetPath(width: CGFloat, height: CGFloat) -> CGPath {
        let w = width / 2
        let h = height / 2
        let path = CGMutablePath()
        path.move(to: CGPoint(x: -w * 0.42, y: h * 0.76))
        path.addLine(to: CGPoint(x: 0, y: 0))
        path.addLine(to: CGPoint(x: w * 0.42, y: h * 0.76))
        path.move(to: CGPoint(x: -w * 0.42, y: -h * 0.76))
        path.addLine(to: CGPoint(x: 0, y: 0))
        path.addLine(to: CGPoint(x: w * 0.42, y: -h * 0.76))
        path.move(to: CGPoint(x: -w * 0.72, y: 0))
        path.addLine(to: CGPoint(x: w * 0.72, y: 0))
        return path
    }

    private static func sparklePath(radius: CGFloat) -> CGPath {
        let path = CGMutablePath()
        path.move(to: CGPoint(x: 0, y: radius))
        path.addLine(to: CGPoint(x: radius * 0.28, y: radius * 0.28))
        path.addLine(to: CGPoint(x: radius, y: 0))
        path.addLine(to: CGPoint(x: radius * 0.28, y: -radius * 0.28))
        path.addLine(to: CGPoint(x: 0, y: -radius))
        path.addLine(to: CGPoint(x: -radius * 0.28, y: -radius * 0.28))
        path.addLine(to: CGPoint(x: -radius, y: 0))
        path.addLine(to: CGPoint(x: -radius * 0.28, y: radius * 0.28))
        path.closeSubpath()
        return path
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
