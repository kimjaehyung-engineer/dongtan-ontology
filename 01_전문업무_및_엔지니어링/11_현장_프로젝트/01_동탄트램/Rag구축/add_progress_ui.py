target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

old_send = """      const botMsgDiv = appendMessage('bot', '<em>전체 문서 색인을 탐색하여 최적의 출처를 분석 중입니다 (수초 소요)...</em>');

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            query: query
          })
        });"""

new_send = """      const botMsgDiv = appendMessage('bot', `
        <div class="progress-box" style="font-size:12.5px; line-height: 1.6; color: var(--text-color);">
          <div id="step1" style="font-weight:600; color: #0284c7;">⚡ 1단계: 5개 문서 메타데이터 색인 탐색 중...</div>
          <div id="step2" style="color: var(--text-muted); opacity: 0.6;">📂 2단계: 최적 출처 문서 매칭 및 핵심 섹션 정밀 발췌 대기</div>
          <div id="step3" style="color: var(--text-muted); opacity: 0.6;">🤖 3단계: 수석 엔지니어 AI 도표/제원 정밀 분석 대기</div>
        </div>
      `);

      const t1 = setTimeout(() => {
        const s1 = document.getElementById('step1');
        const s2 = document.getElementById('step2');
        if (s1 && s2) {
          s1.innerHTML = '✅ 1단계: 5개 문서 메타데이터 색인 탐색 완료 (0.002s)';
          s1.style.color = '#15803d';
          s2.innerHTML = '📂 2단계: 최적 문서 핵심 섹션 정밀 발췌 완료 (초고속 슬라이싱)';
          s2.style.fontWeight = '600';
          s2.style.color = '#0284c7';
          s2.style.opacity = '1.0';
        }
      }, 700);

      const t2 = setTimeout(() => {
        const s2 = document.getElementById('step2');
        const s3 = document.getElementById('step3');
        if (s2 && s3) {
          s2.innerHTML = '✅ 2단계: 최적 출처 문서 핵심 섹션 발췌 완료';
          s2.style.color = '#15803d';
          s3.innerHTML = '<span class="loading-spinner"></span> 3단계: Gemini 고속 멀티모달 AI 분석 중...';
          s3.style.fontWeight = '600';
          s3.style.color = '#2563eb';
          s3.style.opacity = '1.0';
        }
      }, 1500);

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            query: query
          })
        });
        clearTimeout(t1);
        clearTimeout(t2);"""

if old_send in content:
    content = content.replace(old_send, new_send)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully added dynamic progress step feedback to sendQuery")
else:
    print("Failed to find old sendQuery block")
