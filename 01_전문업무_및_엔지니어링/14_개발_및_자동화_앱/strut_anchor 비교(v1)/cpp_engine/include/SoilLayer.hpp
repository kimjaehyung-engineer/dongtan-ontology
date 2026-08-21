#pragma once
#include <string>
#include <vector>
#include <cmath>

namespace EarthRetaining {

struct SoilLayer {
    std::string name;
    double topDepth;       // m (상부 심도)
    double bottomDepth;    // m (하부 심도)
    double gamma;          // kN/m3 (습윤 단위중량)
    double gammaSat;       // kN/m3 (포화 단위중량)
    double cohesion;       // kN/m2 (점착력 c)
    double frictionAngle;  // deg (내부마찰각 phi)
    double Es;             // kN/m2 (지반 변형계수)
    double kh0;            // kN/m3 (기본 수평지반반력계수)
    double NValue;         // SPT N치
    bool isCohesive;       // 점성토 여부

    // 주동토압계수 Ka (Rankine)
    double getKa() const {
        double rad = frictionAngle * M_PI / 180.0;
        return std::pow(std::tan(M_PI / 4.0 - rad / 2.0), 2.0);
    }

    // 수동토압계수 Kp (Rankine)
    double getKp() const {
        double rad = frictionAngle * M_PI / 180.0;
        return std::pow(std::tan(M_PI / 4.0 + rad / 2.0), 2.0);
    }

    // 정지토압계수 K0 (Jaky)
    double getK0() const {
        double rad = frictionAngle * M_PI / 180.0;
        return 1.0 - std::sin(rad);
    }
};

struct WallSection {
    std::string name;      // ex: "H-300x300x10x15" or "CIP D400@500"
    std::string type;      // "H_PILE", "CIP", "SCW", "SHEET_PILE"
    double spacing;        // m (H-Pile 등 수평간격, ex: 1.8m)
    double EI;             // kNm2/m (단위폭당 휨강성)
    double EA;             // kN/m (단위폭당 축강성)
    double Zx;             // cm3 (H형강 1본당 단면계수)
    double totalLength;    // m (벽체 총 연장 = 굴착고 + 근입장)
    double yieldStrength;  // MPa (강재 항복강도, ex: 235 or 355)
    double allowBendingStress; // MPa (허용휨응력)
};

enum class SupportType {
    STRUT,
    GROUND_ANCHOR,
    RAKER
};

struct SupportStage {
    int stageIndex;
    SupportType type;
    double depth;          // m (지표면 기준 설치 심도)
    double angle;          // deg (수평선 기준 설치각도, Strut=0, Anchor=15~20)
    double horizSpacing;   // m (수평 설치 간격, ex: 3.0m)
    double preload;        // kN (선행재하 하중 / 초기 인장력)
    double springStiffness;// kN/m (지보재 축강성 k = EA/L)
    double freeLength;     // m (앵커 자유장)
    double bondLength;     // m (앵커 정착장)
    double allowableCapacity; // kN (허용 지지력/인장력)
    std::string specName;  // ex: "강관 Φ508x9t", "SWPC 12.7mm 4가닥"
};

struct ExcavationStage {
    int stage;
    std::string name;
    double excavationDepth; // m (해당 단계 굴착 심도)
    double waterTableBehind;// m (배면 지하수위 심도)
    double waterTableInside;// m (굴착측 지하수위 심도)
    double surcharge;       // kN/m2 (상재하중)
    std::vector<SupportStage> activeSupports; // 해당 단계까지 설치된 지보공
};

} // namespace EarthRetaining
