const XLSX = require('xlsx');
const wb = XLSX.readFile('c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/08.메뉴얼 및 평면도/최종/02_메뉴얼 공종프로섹스(집행단계)/매뉴얼BODY(집행단계-첨부폴더)v8/매뉴얼 BODY (집행단계)v8.xlsx');

function classifyDepartment(deptRaw, taskTitleRaw) {
  const deptText = (deptRaw || '').toLowerCase().replace(/\s+/g, '');
  const titleText = (taskTitleRaw || '').toLowerCase();
  const fullText = deptText + ' ' + titleText;

  // 1. 공무 / 계약 / 인허가
  if (
    deptText.includes('공무') ||
    deptText.includes('소장') ||
    deptText.includes('계약') ||
    deptText.includes('인허가') ||
    deptText.includes('기획') ||
    deptText.includes('발주')
  ) {
    return { subDept: '공무', rowIndex: 0 };
  }

  // 2. 품질
  if (deptText.includes('품질') || deptText.includes('시험') || deptText.includes('검측') || deptText.includes('검수')) {
    return { subDept: '품질', rowIndex: 2 };
  }

  // 3. 안전 / 보건 / 환경
  if (deptText.includes('안전') || deptText.includes('보건') || deptText.includes('환경')) {
    return { subDept: '안전', rowIndex: 3 };
  }

  // 4. 관리 / 용지 / 총무
  if (deptText.includes('관리') || deptText.includes('총무') || deptText.includes('용지') || deptText.includes('회계')) {
    return { subDept: '관리', rowIndex: 4 };
  }

  // 5. 본사 / 외주 / 기술
  if (
    deptText.includes('본사') ||
    deptText.includes('외주') ||
    deptText.includes('컴플라이언스') ||
    deptText.includes('스마트엔지니어링') ||
    deptText.includes('견적')
  ) {
    return { subDept: '본사', rowIndex: 5 };
  }

  // 6. 공사 / 현장 시공 / 시스템
  if (
    deptText.includes('공사') ||
    deptText.includes('시공') ||
    deptText.includes('토목') ||
    deptText.includes('궤도') ||
    deptText.includes('건축') ||
    deptText.includes('기계') ||
    deptText.includes('전기') ||
    deptText.includes('통신') ||
    deptText.includes('신호') ||
    deptText.includes('소방') ||
    deptText.includes('운영') ||
    deptText.includes('시스템') ||
    deptText.includes('협력업체') ||
    deptText.includes('업체')
  ) {
    return { subDept: '공사', rowIndex: 1 };
  }

  // 7. 작업명 키워드
  if (fullText.includes('인허가') || fullText.includes('계약') || fullText.includes('발주')) {
    return { subDept: '공무', rowIndex: 0 };
  }
  if (fullText.includes('품질') || fullText.includes('시험') || fullText.includes('검측')) {
    return { subDept: '품질', rowIndex: 2 };
  }
  if (fullText.includes('안전') || fullText.includes('보건') || fullText.includes('위험')) {
    return { subDept: '안전', rowIndex: 3 };
  }
  if (fullText.includes('용지') || fullText.includes('보상') || fullText.includes('관리')) {
    return { subDept: '관리', rowIndex: 4 };
  }

  return { subDept: '공사', rowIndex: 1 };
}

for (const sname of ['지반조사', '사전토공사', '지장물이설', '상부강화노반', '건축']) {
  const ws = wb.Sheets[sname];
  const json = XLSX.utils.sheet_to_json(ws, { defval: '' });
  console.log('=== Sheet: ' + sname + ' ===');
  json.slice(0, 10).forEach((r, idx) => {
    const dStr = r['주관'] || '';
    const tStr = r['작업단위 (Level 4 Task/Activity)'] || '';
    const cls = classifyDepartment(dStr, tStr);
    console.log('  [' + (idx+1) + '] 주관: "' + dStr + '" -> Row ' + cls.rowIndex + ' (' + cls.subDept + ') | Task: "' + tStr.slice(0, 25) + '"');
  });
}
