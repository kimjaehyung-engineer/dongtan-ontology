import { REAL_MANUAL_HTML_MAP } from '../data/realManualHtmlMap';

export const MANUAL_BASE_PATH = `C:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/08.메뉴얼 및 평면도/최종/02_메뉴얼 공종프로섹스(집행단계)/매뉴얼BODY(집행단계-첨부폴더)v8`;

export function getManualHtmlForActivity(actNum: number, actTitle: string, tab: 'standard' | 'directive' | 'checklist'): string {
  const realHtml = REAL_MANUAL_HTML_MAP[actNum]?.[tab];
  if (realHtml) {
    return realHtml;
  }

  const tabName = tab === 'standard' ? '표준서' : tab === 'directive' ? '수행지침' : '체크리스트';
  const tabTheme = tab === 'standard' ? { border: 'border-indigo-500/50', badge: 'bg-indigo-950/80 text-indigo-300 border-indigo-700/60', title: 'text-indigo-400', btn: 'bg-indigo-600' } :
                   tab === 'directive' ? { border: 'border-amber-500/50', badge: 'bg-amber-950/80 text-amber-300 border-amber-700/60', title: 'text-amber-400', btn: 'bg-amber-600' } :
                   { border: 'border-emerald-500/50', badge: 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60', title: 'text-emerald-400', btn: 'bg-emerald-600' };

  return `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄도시철도(트램) - [#${actNum}] ${actTitle} ${tabName}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style> body { font-family: 'Noto Sans KR', sans-serif; } </style>
</head>
<body class="bg-slate-900 text-slate-100 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-slate-900/95 rounded-3xl shadow-2xl border-2 ${tabTheme.border} p-6 sm:p-10 space-y-8">
    
    <!-- 🔵 헤더 영역 -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-800 gap-4">
        <div>
            <span class="text-xs font-black px-3.5 py-1.5 rounded-full mb-3 inline-block border ${tabTheme.badge}">
                Dongtan Tram Subgrade Playbook | WBS 9000-7-${actNum} ${tabName}
            </span>
            <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight flex items-center gap-2">
                <span>[#${actNum}]</span> ${actTitle} ${tabName}
            </h1>
        </div>
        <div class="shrink-0">
            <span class="inline-flex items-center justify-center gap-1.5 text-xs font-black text-white ${tabTheme.btn} px-4 py-2.5 rounded-xl shadow-md">
                <span>📑</span>
                <span>매뉴얼BODY v7 정식 문서</span>
            </span>
        </div>
    </div>

    <!-- 💡 1. 핵심 개요 및 지정 목적 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="md:col-span-2 bg-slate-950/80 border border-slate-800 rounded-2xl p-5 space-y-2">
            <h3 class="text-base font-black ${tabTheme.title} flex items-center gap-2">
                <span>📌</span> 현장 이행 및 방침 목적
            </h3>
            <p class="text-slate-300 text-xs leading-relaxed font-medium">
                본 과업은 동탄도시철도(트램) 건설공사 사전토공사 및 노반 공종의 <b>[#${actNum}] ${actTitle}</b>에 관한 관계 법령(KDS/KCS 시방서 및 건설기술 진흥법)을 준수하고, 시공 중 품질·안전 리스크를 사전 차단하기 위한 필수 ${tabName} 규정임.
            </p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-2xl p-5 space-y-2">
            <h3 class="text-base font-black text-slate-200 flex items-center gap-2">
                <span>📑</span> 필수 성과품 / 서류
            </h3>
            <p class="text-slate-300 font-extrabold text-xs leading-relaxed bg-slate-900 p-3 rounded-xl border border-slate-800">
                ${actTitle} 정밀 검측성과표 및 책임감리원 최종 서면 승인서
            </p>
        </div>
    </div>

    <!-- 🛠️ 2. 상세 수행지침 및 확인 절차 -->
    <div class="space-y-4 pt-2">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 class="text-lg font-black text-white flex items-center gap-2">
                <span>🛠️</span> 상세 ${tabName} 가이드라인 및 필수 체크항목
            </h3>
            <span class="text-xs font-bold ${tabTheme.title}">현장 감리·시공 공통 규격</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-slate-950/70 border border-slate-800 rounded-2xl p-4 space-y-2">
                <span class="text-[11px] font-black ${tabTheme.title} bg-slate-900 px-2.5 py-1 rounded-md inline-block">STEP 01</span>
                <h4 class="font-bold text-sm text-white">사전 준비 및 서류 검토</h4>
                <p class="text-slate-400 text-xs leading-relaxed">
                    도면, 시방 규격, 자재 승인원 및 안전관리계획서 사전 이행 여부를 확인하고 감리단 보고서 작성.
                </p>
            </div>

            <div class="bg-slate-950/70 border border-slate-800 rounded-2xl p-4 space-y-2">
                <span class="text-[11px] font-black ${tabTheme.title} bg-slate-900 px-2.5 py-1 rounded-md inline-block">STEP 02</span>
                <h4 class="font-bold text-sm text-white">현장 검측 및 실측 시험</h4>
                <p class="text-slate-400 text-xs leading-relaxed">
                    현장 측량, 평탄성 및 평판재하시험(KDS 기준) 3개소 이상 무작위 측정 및 품질 실측값 산출.
                </p>
            </div>

            <div class="bg-slate-950/70 border border-slate-800 rounded-2xl p-4 space-y-2">
                <span class="text-[11px] font-black ${tabTheme.title} bg-slate-900 px-2.5 py-1 rounded-md inline-block">STEP 03</span>
                <h4 class="font-bold text-sm text-white">리스크 저감 및 이행 점검</h4>
                <p class="text-slate-400 text-xs leading-relaxed">
                    지장물 간섭, 민원 저감 대책 및 임시 배수시설 가동 상태를 최종 점검 후 사후 조치 기록.
                </p>
            </div>

            <div class="bg-slate-950/70 border border-slate-800 rounded-2xl p-4 space-y-2">
                <span class="text-[11px] font-black ${tabTheme.title} bg-slate-900 px-2.5 py-1 rounded-md inline-block">STEP 04</span>
                <h4 class="font-bold text-sm text-white">최종 검측 결재 및 승인</h4>
                <p class="text-slate-400 text-xs leading-relaxed">
                    책임감리원 및 현장소장 최종 조율 후 서면 승인서 발행 및 다음 단계(Phase) 공종 이행 승인.
                </p>
            </div>
        </div>
    </div>

    <!-- 📌 푸터 안내 -->
    <div class="pt-6 border-t border-slate-800 flex items-center justify-between text-xs text-slate-500">
        <span>🏢 동탄도시철도(트램) 건설공사 시공 표준 플레이북</span>
        <span>매뉴얼BODY(집행단계-첨부폴더)v8 연동</span>
    </div>

</div>
</body>
</html>`;
}
