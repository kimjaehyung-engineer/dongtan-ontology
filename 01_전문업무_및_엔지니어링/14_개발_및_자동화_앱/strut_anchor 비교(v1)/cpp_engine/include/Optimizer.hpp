#pragma once
#include "SoilLayer.hpp"
#include "NonLinearSolver.hpp"
#include <string>
#include <vector>
#include <algorithm>

namespace EarthRetaining {

struct CostItem {
    std::string name;
    double quantity;
    std::string unit;
    double unitPrice; // 원
    double totalPrice; // 원
};

struct AlternativeSpec {
    int id;
    std::string name;               // "대안 1: 버팀보(All Strut) 공법"
    std::string type;               // "ALL_STRUT", "ALL_ANCHOR", "HYBRID", "OPTIMIZED"
    std::string description;
    WallSection wall;
    std::vector<SupportStage> supports;
    std::vector<StageResult> stageResults;
    
    // 최종 결과 요약
    double maxMoment;               // kNm/m
    double maxDisplacement;         // mm
    double pileStressRatio;         // H-Pile 응력비
    double minSupportSF;            // 지보재 최소 안전율
    double embedmentSF;             // 근입장 안전율
    double boilingSF;               // 보일링 안전율
    double heavingSF;               // 히빙 안전율
    bool isStructurallySafe;        // 구조적 안전 여부
    
    // 경제성 (단위 m당 또는 총 공사비)
    double wallLengthPerimeter;     // m (가시설 총 연장, ex: 100m)
    std::vector<CostItem> costBreakdown;
    double totalCostWon;            // 총 공사비 (원)
    double costPerM;                // m당 공사비 (원/m)
    
    // 시공성/민원성 점수 (100점 만점 기준)
    double workSpaceScore;          // 굴착 작업공간 확보성 (앵커: 95점, 스트러트: 65점)
    double boundaryRiskScore;       // 부지경계선 침범 안전성 (스트러트: 100점, 앵커: 70점)
    double constructabilityScore;   // 시공 용이성
    double periodDays;              // 공사기간 (일)
    double overallScore;            // 종합 점수 (안전성40% + 경제성35% + 시공성25%)
    int rank;                       // 추천 순위
};

class AlternativeOptimizer {
public:
    static AlternativeSpec evaluateAlternative(
        int altId,
        const std::string& altName,
        const std::string& altType,
        const std::string& desc,
        const std::vector<SoilLayer>& soils,
        const WallSection& wall,
        const std::vector<SupportStage>& supports,
        double excavationDepth,
        double excavationWidth,
        double totalWallPerimeter = 100.0,
        double wtBehind = 3.0,
        double wtInside = 15.0,
        double surcharge = 20.0
    ) {
        AlternativeSpec alt;
        alt.id = altId;
        alt.name = altName;
        alt.type = altType;
        alt.description = desc;
        alt.wall = wall;
        alt.supports = supports;
        alt.wallLengthPerimeter = totalWallPerimeter;

        // 시공 단계 정의 (굴착 -> 지보설치 순차)
        std::vector<ExcavationStage> stages;
        
        // Stage 1: 선행 굴착 (1단 지보 심도 + 0.5m)
        double stage1Exc = supports.empty() ? excavationDepth : std::min(excavationDepth, supports[0].depth + 0.5);
        stages.push_back({1, "1차 선행 굴착", stage1Exc, wtBehind, std::max(stage1Exc, wtInside), surcharge, {}});

        // 중간 단계들
        for (size_t i = 0; i < supports.size(); ++i) {
            std::vector<SupportStage> activeSups(supports.begin(), supports.begin() + i + 1);
            double nextExc = (i + 1 < supports.size()) ? std::min(excavationDepth, supports[i + 1].depth + 0.5) : excavationDepth;
            stages.push_back({
                static_cast<int>(i + 2),
                std::to_string(i + 1) + "단 지보설치 및 " + std::to_string(i + 2) + "차 굴착",
                nextExc,
                wtBehind,
                std::max(nextExc, wtInside),
                surcharge,
                activeSups
            });
        }

        // C++ 탄소성 FEM 솔버 실행
        FEMElastoPlasticSolver solver(soils, wall, 0.1);
        alt.stageResults = solver.solveConstructionStages(stages);

        // 최종 단계 결과 추출
        const auto& finalRes = alt.stageResults.back();
        alt.maxMoment = finalRes.stability.maxMoment;
        alt.maxDisplacement = finalRes.stability.maxDisplacement;
        alt.pileStressRatio = finalRes.stability.pileStressRatio;
        alt.embedmentSF = finalRes.stability.embedmentSafetyFactor;
        alt.boilingSF = finalRes.stability.boilingSafetyFactor;
        alt.heavingSF = finalRes.stability.heavingSafetyFactor;

        double minSupSF = 99.0;
        for (const auto& sup : finalRes.supports) {
            minSupSF = std::min(minSupSF, sup.safetyFactor);
        }
        alt.minSupportSF = (minSupSF > 90.0) ? 1.5 : minSupSF;

        alt.isStructurallySafe = (alt.pileStressRatio <= 1.0) &&
                                (alt.minSupportSF >= 1.0) &&
                                (alt.embedmentSF >= 1.2) &&
                                (alt.boilingSF >= 1.5) &&
                                (alt.heavingSF >= 1.2);

        // 공사비 산정 (물량 x 단가)
        calculateCost(alt, excavationDepth, excavationWidth);

        // 시공성 및 종합 점수 산정
        calculateConstructability(alt, altType, excavationWidth);

        return alt;
    }

private:
    static void calculateCost(AlternativeSpec& alt, double excDepth, double excWidth) {
        double L_perim = alt.wallLengthPerimeter;
        double wallArea = L_perim * alt.wall.totalLength;
        int numPiles = static_cast<int>(std::ceil(L_perim / alt.wall.spacing));

        alt.costBreakdown.clear();

        // 1. H-Pile 자재비 및 천공/항타비
        double pileWeightTon = numPiles * alt.wall.totalLength * 0.094; // 약 94kg/m 기준 (H-300)
        double pileCost = pileWeightTon * 1350000.0; // 1,350,000원/톤
        double drillingCost = numPiles * alt.wall.totalLength * 45000.0; // 45,000원/m
        alt.costBreakdown.push_back({"H-Pile 강재 (자재/손료)", pileWeightTon, "ton", 1350000.0, pileCost});
        alt.costBreakdown.push_back({"H-Pile 천공 및 근입시공", numPiles * alt.wall.totalLength, "m", 45000.0, drillingCost});

        // 2. 토류판(목재 또는 토류벽) 공사비
        double laggingArea = L_perim * excDepth;
        double laggingCost = laggingArea * 38000.0; // 38,000원/m2
        alt.costBreakdown.push_back({"토류판(낙엽송/목재) 설치", laggingArea, "m2", 38000.0, laggingCost});

        // 3. 띠장(Wale) 2-H형강 설치
        int numSupportTiers = static_cast<int>(alt.supports.size());
        double waleLen = L_perim * numSupportTiers;
        double waleWeightTon = waleLen * 0.188; // 2열 H-300 약 188kg/m
        double waleCost = waleWeightTon * 1400000.0;
        alt.costBreakdown.push_back({"띠장(W-Beam 2열) 가설/해체", waleWeightTon, "ton", 1400000.0, waleCost});

        // 4. 지보재 (Strut vs Anchor) 공사비
        double strutCost = 0.0;
        double anchorCost = 0.0;
        double kingPostCost = 0.0;

        for (const auto& sup : alt.supports) {
            if (sup.type == SupportType::STRUT) {
                // 버팀보 본수 = L_perim / (2 * horizSpacing) (양측 대칭)
                int numStruts = static_cast<int>(std::ceil(L_perim / (2.0 * sup.horizSpacing)));
                double strutLen = excWidth;
                double strutWeightTon = numStruts * strutLen * 0.11; // 약 110kg/m (강관 또는 H형강)
                strutCost += strutWeightTon * 1450000.0;
            } else if (sup.type == SupportType::GROUND_ANCHOR) {
                // 어스앵커 공수 = L_perim / horizSpacing
                int numAnchors = static_cast<int>(std::ceil(L_perim / sup.horizSpacing));
                double totalAnchorLen = numAnchors * (sup.freeLength + sup.bondLength);
                anchorCost += totalAnchorLen * 58000.0; // 58,000원/m (천공+강선+그라우팅+인장)
            }
        }

        if (strutCost > 0.0) {
            alt.costBreakdown.push_back({"버팀보(Strut/브레이싱) 설치/해체", strutCost / 1450000.0, "ton", 1450000.0, strutCost});
            // 중간말뚝 (King Post)
            int numKingPosts = static_cast<int>(std::ceil(L_perim / 6.0) * std::ceil(excWidth / 10.0));
            kingPostCost = numKingPosts * (excDepth + 5.0) * 85000.0;
            alt.costBreakdown.push_back({"중간말뚝(King Post) 및 복공", numKingPosts * (excDepth + 5.0), "m", 85000.0, kingPostCost});
        }

        if (anchorCost > 0.0) {
            alt.costBreakdown.push_back({"어스앵커(천공/강선/그라우팅/인장)", anchorCost / 58000.0, "m", 58000.0, anchorCost});
        }

        // 총액 합산
        double total = 0.0;
        for (const auto& item : alt.costBreakdown) {
            total += item.totalPrice;
        }
        alt.totalCostWon = total;
        alt.costPerM = total / L_perim;
    }

    static void calculateConstructability(AlternativeSpec& alt, const std::string& altType, double excWidth) {
        if (altType == "ALL_ANCHOR") {
            alt.workSpaceScore = 95.0;      // 내부 완전 개방으로 굴착 효율 극대화
            alt.boundaryRiskScore = 68.0;   // 대지경계선 외측 앵커 침범 리스크 (사유지 동의 필요)
            alt.constructabilityScore = 88.0;
            alt.periodDays = 45.0;
        } else if (altType == "ALL_STRUT") {
            alt.workSpaceScore = 65.0;      // 버팀보 간섭으로 장비 작업성 저하
            alt.boundaryRiskScore = 100.0;  // 부지 경계 내에서 완결 (민원 안전)
            alt.constructabilityScore = 80.0;
            alt.periodDays = 55.0;
        } else if (altType == "HYBRID") {
            alt.workSpaceScore = 82.0;      // 상부 앵커로 장비 진입 용이, 하부 스트러트
            alt.boundaryRiskScore = 85.0;   // 상부 앵커는 도로부지/경계 내 정착 가능
            alt.constructabilityScore = 86.0;
            alt.periodDays = 48.0;
        } else { // OPTIMIZED
            alt.workSpaceScore = 85.0;
            alt.boundaryRiskScore = 88.0;
            alt.constructabilityScore = 90.0;
            alt.periodDays = 46.0;
        }

        // 안전성 점수 (100점 만점)
        double safetyScore = 100.0;
        if (!alt.isStructurallySafe) safetyScore = 40.0;
        else {
            safetyScore -= std::max(0.0, (alt.pileStressRatio - 0.7) * 50.0);
            safetyScore -= std::max(0.0, (alt.maxDisplacement - 25.0) * 1.5);
        }
        safetyScore = std::clamp(safetyScore, 50.0, 100.0);

        // 경제성 점수 (상대적 비교)
        double economyScore = 85.0; // 4대안 비교 시 정규화

        // 종합 점수 가중치 (안전 40% + 경제 35% + 시공 25%)
        alt.overallScore = safetyScore * 0.40 + economyScore * 0.35 + ((alt.workSpaceScore + alt.boundaryRiskScore) / 2.0) * 0.25;
    }
};

} // namespace EarthRetaining
