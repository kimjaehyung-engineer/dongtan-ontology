#include "include/SoilLayer.hpp"
#include "include/NonLinearSolver.hpp"
#include "include/Optimizer.hpp"
#include <iostream>
#include <iomanip>

using namespace EarthRetaining;

int main() {
    std::cout << "========================================================\n";
    std::cout << "  가시설 Strut & Ground Anchor C++ 고정밀 탄소성 해석 엔진 \n";
    std::cout << "========================================================\n\n";

    // 1. 전형적 도심지 복합 지층 정의 (매립토 -> 풍화토 -> 풍화암 -> 연암)
    std::vector<SoilLayer> soils = {
        {"매립층 (Fill)", 0.0, 3.0, 18.0, 19.0, 5.0, 26.0, 15000.0, 12000.0, 8.0, false},
        {"풍화토 (Weathered Soil)", 3.0, 8.0, 19.0, 20.0, 12.0, 30.0, 35000.0, 25000.0, 25.0, false},
        {"풍화암 (Weathered Rock)", 8.0, 14.0, 21.0, 22.0, 30.0, 35.0, 80000.0, 60000.0, 50.0, false},
        {"연암 (Soft Rock)", 14.0, 25.0, 24.0, 25.0, 100.0, 40.0, 250000.0, 150000.0, 50.0, false}
    };

    // 2. 가시설 벽체 조건 (H-300x300x10x15 @ 1.8m)
    WallSection wall;
    wall.name = "H-300x300x10x15 @ 1.8m";
    wall.type = "H_PILE";
    wall.spacing = 1.8;
    // 단위폭당 EI (E = 2.05e8 kN/m2, Ix = 20400 cm4 -> EI_unit = E * Ix / 1.8)
    wall.EI = (2.05e8 * 20400.0 * 1e-8) / 1.8; // kNm2/m (~23,233 kNm2/m)
    wall.EA = (2.05e8 * 119.8 * 1e-4) / 1.8;  // kN/m
    wall.Zx = 1360.0; // cm3
    wall.totalLength = 17.0; // m
    wall.yieldStrength = 235.0; // MPa
    wall.allowBendingStress = 140.0; // MPa

    double excavationDepth = 12.0; // m
    double excavationWidth = 18.0; // m

    std::cout << "[1] 기본 입력 조건:\n";
    std::cout << " - 굴착 깊이: " << excavationDepth << " m, 굴착 폭: " << excavationWidth << " m\n";
    std::cout << " - 벽체 형식: " << wall.name << " (총 연장: " << wall.totalLength << " m)\n";
    std::cout << " - 지층: 4개층 (매립 3m / 풍화토 5m / 풍화암 6m / 연암)\n\n";

    // 3. 4대안 생성 및 C++ 탄소성 FEM 해석 실행
    // 대안 1: All-Strut (4단 버팀보)
    std::vector<SupportStage> strutSups = {
        {1, SupportType::STRUT, 1.5, 0.0, 3.5, 50.0, 45000.0, 0.0, 0.0, 650.0, "강관 Φ508x9t"},
        {2, SupportType::STRUT, 4.5, 0.0, 3.5, 80.0, 45000.0, 0.0, 0.0, 650.0, "강관 Φ508x9t"},
        {3, SupportType::STRUT, 7.5, 0.0, 3.5, 100.0, 45000.0, 0.0, 0.0, 650.0, "강관 Φ508x9t"},
        {4, SupportType::STRUT, 10.0, 0.0, 3.5, 100.0, 45000.0, 0.0, 0.0, 650.0, "강관 Φ508x9t"}
    };
    auto alt1 = AlternativeOptimizer::evaluateAlternative(1, "대안 1: 버팀보(All-Strut) 공법", "ALL_STRUT", "내부 4단 버팀보 지지 구조", soils, wall, strutSups, excavationDepth, excavationWidth);

    // 대안 2: All-Anchor (4단 어스앵커)
    std::vector<SupportStage> anchorSups = {
        {1, SupportType::GROUND_ANCHOR, 1.5, 15.0, 2.0, 150.0, 35000.0, 8.0, 6.0, 350.0, "SWPC 12.7mm 4가닥"},
        {2, SupportType::GROUND_ANCHOR, 4.5, 15.0, 2.0, 200.0, 35000.0, 8.0, 6.5, 450.0, "SWPC 12.7mm 5가닥"},
        {3, SupportType::GROUND_ANCHOR, 7.5, 15.0, 2.0, 250.0, 35000.0, 7.0, 7.0, 450.0, "SWPC 12.7mm 5가닥"},
        {4, SupportType::GROUND_ANCHOR, 10.0, 15.0, 2.0, 250.0, 35000.0, 6.0, 7.0, 450.0, "SWPC 12.7mm 5가닥"}
    };
    auto alt2 = AlternativeOptimizer::evaluateAlternative(2, "대안 2: 어스앵커(All-Anchor) 공법", "ALL_ANCHOR", "전단 그라운드 앵커 지지 구조", soils, wall, anchorSups, excavationDepth, excavationWidth);

    // 대안 3: Hybrid (상부 1,2단 앵커 + 하부 3,4단 스트러트)
    std::vector<SupportStage> hybridSups = {
        {1, SupportType::GROUND_ANCHOR, 1.5, 15.0, 2.0, 150.0, 35000.0, 8.0, 6.0, 350.0, "SWPC 12.7mm 4가닥"},
        {2, SupportType::GROUND_ANCHOR, 4.5, 15.0, 2.0, 200.0, 35000.0, 8.0, 6.5, 450.0, "SWPC 12.7mm 5가닥"},
        {3, SupportType::STRUT, 7.5, 0.0, 3.5, 100.0, 45000.0, 0.0, 0.0, 650.0, "강관 Φ508x9t"},
        {4, SupportType::STRUT, 10.0, 0.0, 3.5, 100.0, 45000.0, 0.0, 0.0, 650.0, "강관 Φ508x9t"}
    };
    auto alt3 = AlternativeOptimizer::evaluateAlternative(3, "대안 3: 복합공법 (상부 앵커 + 하부 스트러트)", "HYBRID", "상부 작업공간 확보 + 하부 암반층 버팀보", soils, wall, hybridSups, excavationDepth, excavationWidth);

    // 대안 4: 최적화 단면 (H-300 @ 2.0m + 3단 고내력 복합)
    WallSection wallOpt = wall;
    wallOpt.name = "H-300x300x10x15 @ 2.0m (자재절감형)";
    wallOpt.spacing = 2.0;
    wallOpt.EI = (2.05e8 * 20400.0 * 1e-8) / 2.0;
    wallOpt.totalLength = 16.0;
    std::vector<SupportStage> optSups = {
        {1, SupportType::GROUND_ANCHOR, 1.8, 15.0, 2.0, 180.0, 38000.0, 8.0, 6.0, 450.0, "SWPC 12.7mm 5가닥"},
        {2, SupportType::GROUND_ANCHOR, 5.5, 15.0, 2.0, 240.0, 38000.0, 8.0, 7.0, 520.0, "SWPC 12.7mm 6가닥"},
        {3, SupportType::STRUT, 9.0, 0.0, 4.0, 120.0, 50000.0, 0.0, 0.0, 750.0, "강관 Φ609x12t"}
    };
    auto alt4 = AlternativeOptimizer::evaluateAlternative(4, "대안 4: 자재 최적화 복합안 (3단 복합+벽체절감)", "OPTIMIZED", "단수 축소 및 지보 배치 최적화", soils, wallOpt, optSups, excavationDepth, excavationWidth);

    std::vector<AlternativeSpec> alts = {alt1, alt2, alt3, alt4};

    std::cout << "\n[2] C++ 탄소성 유한요소(FEM) 해석 및 4대안 비교 결과:\n";
    std::cout << "--------------------------------------------------------------------------------------------------------------------\n";
    std::cout << std::left << std::setw(30) << "대안명"
              << std::setw(12) << "최대변위(mm)"
              << std::setw(14) << "최대모멘트(kNm)"
              << std::setw(12) << "H-Pile응력비"
              << std::setw(12) << "근입장 F.S"
              << std::setw(12) << "보일링 F.S"
              << std::setw(16) << "총공사비(백만원)"
              << std::setw(10) << "종합점수" << "\n";
    std::cout << "--------------------------------------------------------------------------------------------------------------------\n";

    for (const auto& a : alts) {
        std::cout << std::left << std::setw(30) << a.name
                  << std::fixed << std::setprecision(2)
                  << std::setw(12) << a.maxDisplacement
                  << std::setw(14) << a.maxMoment
                  << std::setw(12) << a.pileStressRatio
                  << std::setw(12) << a.embedmentSF
                  << std::setw(12) << a.boilingSF
                  << std::setw(16) << (a.totalCostWon / 1e6)
                  << std::setw(10) << a.overallScore << "\n";
    }
    std::cout << "--------------------------------------------------------------------------------------------------------------------\n";
    std::cout << "=> C++ FEM 탄소성 해석 완료.\n";

    return 0;
}
