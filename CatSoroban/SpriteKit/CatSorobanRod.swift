import SpriteKit

class CatSorobanRod {
    let index: Int
    let x: CGFloat
    let beamY: CGFloat
    let topY: CGFloat
    let bottomY: CGFloat
    let beadWidth: CGFloat
    let beadHeight: CGFloat
    let beadSpacing: CGFloat

    var heavenBeads: [CatBeadNode] = []
    var earthBeads: [CatBeadNode] = []
    var heavenActive: [Bool] = [false]
    var earthActive: [Bool] = [false, false, false, false]

    private let beamGap: CGFloat = 4

    init(index: Int, x: CGFloat, beamY: CGFloat, topY: CGFloat, bottomY: CGFloat,
         beadWidth: CGFloat, beadHeight: CGFloat, beadSpacing: CGFloat) {
        self.index = index
        self.x = x
        self.beamY = beamY
        self.topY = topY
        self.bottomY = bottomY
        self.beadWidth = beadWidth
        self.beadHeight = beadHeight
        self.beadSpacing = beadSpacing
    }

    func heavenRestPosition(active: Bool) -> CGPoint {
        if active {
            return CGPoint(x: x, y: beamY + beamGap + beadHeight / 2 + 4)
        } else {
            return CGPoint(x: x, y: topY - beadHeight / 2)
        }
    }

    func earthRestPosition(index: Int, active: Bool) -> CGPoint {
        let reversedIndex = 3 - index
        if active {
            let baseY = beamY - beamGap - beadHeight / 2 - 4
            return CGPoint(x: x, y: baseY - CGFloat(reversedIndex) * (beadHeight + beadSpacing))
        } else {
            let baseY = bottomY + beadHeight / 2
            return CGPoint(x: x, y: baseY + CGFloat(index) * (beadHeight + beadSpacing))
        }
    }

    var value: Int {
        var v = 0
        if heavenActive[0] { v += 5 }
        for active in earthActive where active { v += 1 }
        return v
    }
}
