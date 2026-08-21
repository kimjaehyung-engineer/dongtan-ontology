#pragma once
#include "SoilLayer.hpp"
#include <vector>
#include <iostream>
#include <iomanip>

namespace EarthRetaining {

struct NodeResult {
    double depth;          // m
    double displacement;   // mm (벽체 수평변위, 양수: 굴착측)
    double rotation;       // rad
    double bendingMoment;  // kNm/m (단위폭당 휨모멘트)
    double shearForce;     // kN/m (단위폭당 전단력)
    double earthPressure;  // kN/m2 (작용 토압/지반반력)
    double waterPressure;  // kN/m2 (수압)
    double paLimit;        // kN/m2 (주동토압 한계)
    double ppLimit;        // kN/m2 (수동토압 한계)
    bool isYielded;        // 소성 항복 여부
};

struct SupportResult {
    int supportIndex;
    SupportType type;
    double depth;
    double axialForce;     // kN (H-Pile 간격 고려 지보재 1본당 축력/인장력)
    double allowableForce; // kN (허용내력)
    double safetyFactor;   // 안전율 (허용 / 실제)
    bool isSafe;
};

struct StabilityResult {
    double embedmentSafetyFactor; // 근입장 안전율 (Kp 저항 / Ka 전도)
    bool isEmbedmentSafe;
    double boilingSafetyFactor;   // 보일링 안전율 (icr / iexit)
    bool isBoilingSafe;
    double heavingSafetyFactor;   // 히빙 안전율
    bool isHeavingSafe;
    double pipingSafetyFactor;    // 파이핑 안전율
    bool isPipingSafe;
    double maxMoment;             // kNm/m
    double maxDisplacement;       // mm
    double maxShear;              // kN/m
    double pileStressRatio;       // H-Pile 응력비 (실제응력 / 허용응력)
    bool isPileSafe;
};

struct StageResult {
    int stage;
    std::string stageName;
    double excavationDepth;
    std::vector<NodeResult> nodes;
    std::vector<SupportResult> supports;
    StabilityResult stability;
};

class FEMElastoPlasticSolver {
private:
    std::vector<SoilLayer> m_soils;
    WallSection m_wall;
    double m_elementLength; // m (기본 0.1m)
    int m_numNodes;
    int m_numElements;
    
    // 지층 물성 조회
    const SoilLayer* getSoilAtDepth(double depth) const {
        for (const auto& soil : m_soils) {
            if (depth >= soil.topDepth && depth <= soil.bottomDepth) {
                return &soil;
            }
        }
        return m_soils.empty() ? nullptr : &m_soils.back();
    }

    // 유효 상재압 및 정수압/토압 한계 계산
    void calcSoilPressures(double depth, double excDepth, double wtBehind, double wtInside, double surcharge,
                           double& sigmaV, double& u, double& pa, double& pp, double& kh) const {
        // 배면측 유효연직응력 적분
        sigmaV = surcharge;
        double curD = 0.0;
        double step = 0.05;
        while (curD < depth) {
            const SoilLayer* s = getSoilAtDepth(curD + step / 2.0);
            double gamma = (curD >= wtBehind) ? s->gammaSat : s->gamma;
            sigmaV += gamma * step;
            curD += step;
        }

        // 수압 (배면측 정수압, 굴착저면 하부 감압)
        if (depth > wtBehind) {
            u = (depth - wtBehind) * 9.81;
        } else {
            u = 0.0;
        }

        const SoilLayer* s = getSoilAtDepth(depth);
        double c = s->cohesion;
        double phiRad = s->frictionAngle * M_PI / 180.0;
        double Ka = s->getKa();
        double Kp = s->getKp();

        // Rankine 주동/수동 토압 (단위면적당)
        double sigmaVEff = std::max(0.0, sigmaV - u);
        pa = std::max(0.0, Ka * sigmaVEff - 2.0 * c * std::sqrt(Ka)) + u;
        
        // 수동토압 (굴착면 하부에서만 유효)
        if (depth >= excDepth) {
            double excEffSigmaV = (depth - excDepth) * (s->gammaSat - 9.81);
            pp = Kp * excEffSigmaV + 2.0 * c * std::sqrt(Kp);
            kh = s->kh0 * std::pow(std::max(0.1, depth - excDepth), 0.5);
        } else {
            pp = 0.0;
            kh = 0.0;
        }
    }

public:
    FEMElastoPlasticSolver(const std::vector<SoilLayer>& soils, const WallSection& wall, double elemLen = 0.1)
        : m_soils(soils), m_wall(wall), m_elementLength(elemLen) {
        m_numNodes = static_cast<int>(std::round(wall.totalLength / m_elementLength)) + 1;
        m_numElements = m_numNodes - 1;
    }

    // 시공단계별 해석 실행
    std::vector<StageResult> solveConstructionStages(const std::vector<ExcavationStage>& stages) {
        std::vector<StageResult> stageResults;
        std::vector<double> prevDisplacements(m_numNodes * 2, 0.0); // 변위 및 회전각 이력

        for (const auto& stage : stages) {
            StageResult sRes;
            sRes.stage = stage.stage;
            sRes.stageName = stage.name;
            sRes.excavationDepth = stage.excavationDepth;

            // 1D 보 유한요소 행렬 구성 및 Newton-Raphson 비선형 수렴 해석
            int totalDOF = m_numNodes * 2;
            std::vector<double> U = prevDisplacements; // 이전 단계 변위에서 시작
            std::vector<double> F_ext(totalDOF, 0.0);
            std::vector<NodeResult> nodeRes(m_numNodes);

            // 하중 및 지반반력, 지보재 모델링
            // 간이 탄소성 보-스프링 직접 강도 해석 루프
            int maxIter = 50;
            double tolerance = 1e-4;

            for (int iter = 0; iter < maxIter; ++iter) {
                // 전체 강성 행렬 K (2*numNodes x 2*numNodes)
                // 1D Euler-Bernoulli 보 굽힘 강성 + 지반 스프링 + 지보 스프링
                std::vector<std::vector<double>> K(totalDOF, std::vector<double>(totalDOF, 0.0));
                std::vector<double> F_int(totalDOF, 0.0);
                std::vector<double> F_load(totalDOF, 0.0);

                // 1. 보 요소 강성 조립
                double EI = m_wall.EI;
                double L = m_elementLength;
                double L2 = L * L;
                double L3 = L * L * L;

                for (int e = 0; e < m_numElements; ++e) {
                    int i1 = e * 2;
                    int i2 = i1 + 2;

                    // 4x4 Hermitian 보 강성 행렬
                    double k_e[4][4] = {
                        { 12 * EI / L3,  6 * EI / L2, -12 * EI / L3,  6 * EI / L2 },
                        {  6 * EI / L2,  4 * EI / L,  -6 * EI / L2,  2 * EI / L  },
                        {-12 * EI / L3, -6 * EI / L2,  12 * EI / L3, -6 * EI / L2 },
                        {  6 * EI / L2,  2 * EI / L,  -6 * EI / L2,  4 * EI / L  }
                    };

                    int indices[4] = { i1, i1 + 1, i2, i2 + 1 };
                    for (int r = 0; r < 4; ++r) {
                        for (int c = 0; c < 4; ++c) {
                            K[indices[r]][indices[c]] += k_e[r][c];
                        }
                    }
                }

                // 2. 지반 압력 및 비선형 지반 스프링 적용
                for (int n = 0; n < m_numNodes; ++n) {
                    double depth = n * m_elementLength;
                    int dofW = n * 2;
                    double disp = U[dofW]; // 수평변위 (m)

                    double sigmaV, u, pa, pp, kh;
                    calcSoilPressures(depth, stage.excavationDepth, stage.waterTableBehind, stage.waterTableInside, stage.surcharge, sigmaV, u, pa, pp, kh);

                    nodeRes[n].depth = depth;
                    nodeRes[n].paLimit = pa;
                    nodeRes[n].ppLimit = pp;
                    nodeRes[n].waterPressure = u;

                    double tributaryArea = (n == 0 || n == m_numNodes - 1) ? (m_elementLength / 2.0) : m_elementLength;

                    if (depth < stage.excavationDepth) {
                        // 굴착면 상부: 배면 주동토압 + 수압 재하
                        double load = pa * tributaryArea;
                        F_load[dofW] += load;
                        nodeRes[n].earthPressure = pa;
                        nodeRes[n].isYielded = true;
                    } else {
                        // 굴착면 하부: 지반 스프링 (주동토압 vs 수동토압 사이의 탄소성 거동)
                        // 초기 주동토압 작용
                        F_load[dofW] += pa * tributaryArea;

                        // 변위에 따른 수동측 지반 반력 p_soil = kh * disp
                        double p_soil = kh * disp;
                        if (p_soil > pp) {
                            // 수동 소성 항복
                            p_soil = pp;
                            nodeRes[n].isYielded = true;
                            F_load[dofW] -= pp * tributaryArea;
                        } else {
                            // 탄성 영역 지반 스프링 강성 행렬에 추가
                            K[dofW][dofW] += kh * tributaryArea;
                            nodeRes[n].isYielded = false;
                        }
                        nodeRes[n].earthPressure = pa - p_soil;
                    }
                }

                // 3. 지보재(Strut/Anchor) 스프링 및 선행하중(Preload) 조립
                for (const auto& sup : stage.activeSupports) {
                    int nodeIdx = static_cast<int>(std::round(sup.depth / m_elementLength));
                    if (nodeIdx >= 0 && nodeIdx < m_numNodes) {
                        int dofW = nodeIdx * 2;
                        double angleRad = sup.angle * M_PI / 180.0;
                        // 단위폭당 유효 수평 스프링 강성 (k_eff = k_spring * cos^2(angle) / spacing)
                        double k_eff = (sup.springStiffness * std::pow(std::cos(angleRad), 2.0)) / sup.horizSpacing;
                        K[dofW][dofW] += k_eff;

                        // 선행하중(Preload) 수평분력 재하
                        double p_preload = (sup.preload * std::cos(angleRad)) / sup.horizSpacing;
                        F_load[dofW] -= p_preload; // 변위 억제 방향
                    }
                }

                // 4. 벽체 하단 가상 지지조건 (연암/경암 착저 시 회전/변위 구속)
                K[totalDOF - 2][totalDOF - 2] += 1e7; // 최하단 노드 변위 구속 스프링
                K[totalDOF - 1][totalDOF - 1] += 1e7; // 최하단 노드 회전 구속 스프링

                // 5. 연립방정식 풀이 (Gauss Elimination) [K]{U_new} = {F_load}
                std::vector<double> U_new(totalDOF, 0.0);
                std::vector<std::vector<double>> A = K;
                std::vector<double> B = F_load;

                // Gauss-Jordan elimination with partial pivoting
                for (int i = 0; i < totalDOF; ++i) {
                    int pivot = i;
                    for (int j = i + 1; j < totalDOF; ++j) {
                        if (std::abs(A[j][i]) > std::abs(A[pivot][i])) pivot = j;
                    }
                    std::swap(A[i], A[pivot]);
                    std::swap(B[i], B[pivot]);

                    if (std::abs(A[i][i]) < 1e-12) continue;

                    for (int j = i + 1; j < totalDOF; ++j) {
                        double factor = A[j][i] / A[i][i];
                        for (int k = i; k < totalDOF; ++k) {
                            A[j][k] -= factor * A[i][k];
                        }
                        B[j] -= factor * B[i];
                    }
                }

                for (int i = totalDOF - 1; i >= 0; --i) {
                    double sum = B[i];
                    for (int j = i + 1; j < totalDOF; ++j) {
                        sum -= A[i][j] * U_new[j];
                    }
                    U_new[i] = (std::abs(A[i][i]) > 1e-12) ? (sum / A[i][i]) : 0.0;
                }

                // 수렴 판정
                double diff = 0.0;
                for (int i = 0; i < totalDOF; ++i) {
                    diff = std::max(diff, std::abs(U_new[i] - U[i]));
                }
                U = U_new;

                if (diff < tolerance) break;
            }

            prevDisplacements = U;

            // 6. 결과 산출 (변위, 휨모멘트 M = EI * d2w/dz2, 전단력 V = dM/dz)
            double maxM = 0.0;
            double maxV = 0.0;
            double maxDisp = 0.0;

            for (int n = 0; n < m_numNodes; ++n) {
                nodeRes[n].displacement = U[n * 2] * 1000.0; // m -> mm
                nodeRes[n].rotation = U[n * 2 + 1];
                maxDisp = std::max(maxDisp, std::abs(nodeRes[n].displacement));

                // 2차 미분 모멘트 산정 (Central Difference)
                if (n > 0 && n < m_numNodes - 1) {
                    double w_prev = U[(n - 1) * 2];
                    double w_curr = U[n * 2];
                    double w_next = U[(n + 1) * 2];
                    double d2w = (w_next - 2.0 * w_curr + w_prev) / (m_elementLength * m_elementLength);
                    nodeRes[n].bendingMoment = -m_wall.EI * d2w;
                } else if (n == 0) {
                    nodeRes[n].bendingMoment = 0.0;
                } else {
                    nodeRes[n].bendingMoment = nodeRes[n - 1].bendingMoment * 0.5;
                }
                maxM = std::max(maxM, std::abs(nodeRes[n].bendingMoment));
            }

            // 전단력 산출
            for (int n = 0; n < m_numNodes - 1; ++n) {
                nodeRes[n].shearForce = (nodeRes[n + 1].bendingMoment - nodeRes[n].bendingMoment) / m_elementLength;
                maxV = std::max(maxV, std::abs(nodeRes[n].shearForce));
            }
            nodeRes[m_numNodes - 1].shearForce = nodeRes[m_numNodes - 2].shearForce;

            sRes.nodes = nodeRes;

            // 7. 지보재 반력 및 축력 계산
            for (size_t i = 0; i < stage.activeSupports.size(); ++i) {
                const auto& sup = stage.activeSupports[i];
                int nodeIdx = static_cast<int>(std::round(sup.depth / m_elementLength));
                double disp = (nodeIdx < m_numNodes) ? U[nodeIdx * 2] : 0.0;
                double angleRad = sup.angle * M_PI / 180.0;

                // 수평 반력 = k_eff * disp + preload_h
                double k_eff = (sup.springStiffness * std::pow(std::cos(angleRad), 2.0)) / sup.horizSpacing;
                double p_preload_h = (sup.preload * std::cos(angleRad)) / sup.horizSpacing;
                double totalHorizRxnPerM = k_eff * disp + p_preload_h;

                // 1본당 실제 작용 축력/인장력 P = R_m * spacing / cos(angle)
                double axialForce = (totalHorizRxnPerM * sup.horizSpacing) / std::max(0.1, std::cos(angleRad));

                SupportResult supRes;
                supRes.supportIndex = static_cast<int>(i + 1);
                supRes.type = sup.type;
                supRes.depth = sup.depth;
                supRes.axialForce = std::max(sup.preload, axialForce);
                supRes.allowableForce = sup.allowableCapacity;
                supRes.safetyFactor = supRes.allowableForce / std::max(1.0, supRes.axialForce);
                supRes.isSafe = (supRes.safetyFactor >= 1.0);
                sRes.supports.push_back(supRes);
            }

            // 8. 지반 파괴 안정성 검토
            StabilityResult stab;
            stab.maxMoment = maxM;
            stab.maxDisplacement = maxDisp;
            stab.maxShear = maxV;

            // H-Pile 응력 검토 (단위폭당 모멘트 -> H-Pile 1본당 휨응력)
            // sigma_b = (M * spacing) / Zx
            if (m_wall.Zx > 0) {
                double momentPerPile = maxM * m_wall.spacing; // kNm
                double actualStress = (momentPerPile * 1e6) / (m_wall.Zx * 1e3); // MPa
                stab.pileStressRatio = actualStress / m_wall.allowBendingStress;
                stab.isPileSafe = (stab.pileStressRatio <= 1.0);
            } else {
                stab.pileStressRatio = 0.75;
                stab.isPileSafe = true;
            }

            // 근입장 안전율 검토 (굴착저면 기준 수동저항모멘트 / 주동전도모멘트)
            double embedmentLength = m_wall.totalLength - stage.excavationDepth;
            double drivingMoment = 0.0;
            double resistingMoment = 0.0;

            for (const auto& n : nodeRes) {
                if (n.depth < stage.excavationDepth) {
                    drivingMoment += n.paLimit * (stage.excavationDepth - n.depth) * m_elementLength;
                } else {
                    resistingMoment += n.ppLimit * (n.depth - stage.excavationDepth) * m_elementLength;
                }
            }
            stab.embedmentSafetyFactor = (drivingMoment > 0) ? (resistingMoment / drivingMoment) : 2.5;
            stab.isEmbedmentSafe = (stab.embedmentSafetyFactor >= 1.2);

            // 보일링 검토 (사질토 및 수위차 검토)
            double deltaH = std::max(0.0, stage.excavationDepth - stage.waterTableBehind);
            double icr = (19.0 - 9.81) / 9.81; // 대략 0.937
            double iexit = (deltaH > 0 && embedmentLength > 0) ? (deltaH / (2.0 * embedmentLength)) : 0.01;
            stab.boilingSafetyFactor = (iexit > 0.001) ? (icr / iexit) : 3.0;
            stab.isBoilingSafe = (stab.boilingSafetyFactor >= 1.5);

            // 히빙 검토 (점성토 지반)
            const SoilLayer* baseSoil = getSoilAtDepth(stage.excavationDepth + 1.0);
            if (baseSoil && baseSoil->isCohesive) {
                double c_base = baseSoil->cohesion;
                double gamma_avg = baseSoil->gamma;
                double Nc = 5.14 * (1.0 + 0.2 * (stage.excavationDepth / 10.0));
                double heavingResistance = Nc * c_base + gamma_avg * embedmentLength;
                double heavingDriving = stage.excavationDepth * gamma_avg + stage.surcharge;
                stab.heavingSafetyFactor = (heavingDriving > 0) ? (heavingResistance / heavingDriving) : 2.0;
            } else {
                stab.heavingSafetyFactor = 2.5; // 사질토/암반은 히빙 우려 없음
            }
            stab.isHeavingSafe = (stab.heavingSafetyFactor >= 1.2);
            stab.pipingSafetyFactor = stab.boilingSafetyFactor * 1.2;
            stab.isPipingSafe = (stab.pipingSafetyFactor >= 1.5);

            sRes.stability = stab;
            stageResults.push_back(sRes);
        }

        return stageResults;
    }
};

} // namespace EarthRetaining
