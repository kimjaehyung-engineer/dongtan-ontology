# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

print("=== Starting 1:1 Step Visual SVG Diagram Upgrade for v8 & Web App ===")

# Define Light-Theme 2D SVG Diagrams for STEP 01 - STEP 04

SVG_STEP_01 = '''<div class="clickable-diagram cursor-pointer transition transform hover:scale-[1.02] hover:shadow-lg bg-slate-50 border border-slate-200 rounded-xl p-3 mb-3" onclick="openDiagramZoom(this.outerHTML, 'STEP 01: 토사 30cm 층포설 시공 2D 도식')">
    <div class="text-[11px] font-bold text-slate-500 mb-1 flex items-center justify-between">
        <span>🔍 클릭 시 대형 팝업 확대</span>
        <span class="text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200 font-extrabold">2D 시공 도식</span>
    </div>
    <svg viewBox="0 0 480 180" class="w-full h-auto rounded bg-white border border-slate-200">
        <rect width="480" height="180" fill="#F8FAFC"/>
        <!-- Sky & Grid -->
        <line x1="0" y1="130" x2="480" y2="130" stroke="#94A3B8" stroke-width="2"/>
        <!-- Base Subgrade -->
        <rect x="0" y="130" width="480" height="50" fill="#CBD5E1"/>
        <text x="20" y="155" font-size="12" font-weight="bold" fill="#475569">원지반 (Existing Ground)</text>
        
        # Spreading Layer 30cm
        <rect x="120" y="100" width="340" height="30" fill="#FDE68A" stroke="#D97706" stroke-width="1.5" stroke-dasharray="4,2"/>
        <text x="220" y="120" font-size="13" font-weight="900" fill="#92400E">성토 토사 층포설 (H = 30cm)</text>
        
        # Height Gauge Marker
        <line x1="440" y1="100" x2="440" y2="130" stroke="#DC2626" stroke-width="2.5"/>
        <line x1="435" y1="100" x2="445" y2="100" stroke="#DC2626" stroke-width="2.5"/>
        <line x1="435" y1="130" x2="445" y2="130" stroke="#DC2626" stroke-width="2.5"/>
        <text x="400" y="118" font-size="12" font-weight="900" fill="#DC2626">30cm</text>
        
        # 2D Dump Truck Body
        <rect x="20" y="75" width="75" height="40" rx="4" fill="#EAB308" stroke="#CA8A04" stroke-width="2"/>
        <polygon points="10,115 20,85 45,85 45,115" fill="#3B82F6" opacity="0.8"/>
        <circle cx="35" cy="125" r="10" fill="#1E293B"/>
        <circle cx="75" cy="125" r="10" fill="#1E293B"/>
        <text x="22" y="100" font-size="11" font-weight="bold" fill="#0F172A">덤프트럭</text>
    </svg>
</div>'''

SVG_STEP_02 = '''<div class="clickable-diagram cursor-pointer transition transform hover:scale-[1.02] hover:shadow-lg bg-sky-50 border border-sky-200 rounded-xl p-3 mb-3" onclick="openDiagramZoom(this.outerHTML, 'STEP 02: 살수차 최적함수비 살수 2D 도식')">
    <div class="text-[11px] font-bold text-sky-700 mb-1 flex items-center justify-between">
        <span>🔍 클릭 시 대형 팝업 확대</span>
        <span class="text-sky-700 bg-sky-100 px-2 py-0.5 rounded border border-sky-300 font-extrabold">2D 살수 도식</span>
    </div>
    <svg viewBox="0 0 480 180" class="w-full h-auto rounded bg-white border border-sky-200">
        <rect width="480" height="180" fill="#F0F9FF"/>
        <line x1="0" y1="130" x2="480" y2="130" stroke="#0284C7" stroke-width="2"/>
        <rect x="0" y="130" width="480" height="50" fill="#BAE6FD"/>
        
        # Moisture Layer
        <rect x="60" y="110" width="400" height="20" fill="#7DD3FC" opacity="0.6"/>
        <text x="210" y="125" font-size="13" font-weight="900" fill="#0369A1">최적함수비 (OMC ±1.5%) 침투층</text>
        
        # Water Tank Truck 2D
        <rect x="40" y="70" width="100" height="45" rx="10" fill="#0284C7" stroke="#0369A1" stroke-width="2"/>
        <rect x="140" y="85" width="30" height="30" rx="3" fill="#38BDF8"/>
        <circle cx="65" cy="125" r="10" fill="#0F172A"/>
        <circle cx="125" cy="125" r="10" fill="#0F172A"/>
        <text x="60" y="98" font-size="12" font-weight="bold" fill="#FFFFFF">살수차 (Water Tank)</text>
        
        # Water Droplets
        <path d="M 140 115 L 170 130 M 150 115 L 180 130 M 160 115 L 190 130" stroke="#0284C7" stroke-width="3" stroke-dasharray="3,3"/>
    </svg>
</div>'''

SVG_STEP_03 = '''<div class="clickable-diagram cursor-pointer transition transform hover:scale-[1.02] hover:shadow-lg bg-amber-50 border border-amber-200 rounded-xl p-3 mb-3" onclick="openDiagramZoom(this.outerHTML, 'STEP 03: 10t 진동롤러 다짐 2D 도식')">
    <div class="text-[11px] font-bold text-amber-800 mb-1 flex items-center justify-between">
        <span>🔍 클릭 시 대형 팝업 확대</span>
        <span class="text-amber-800 bg-amber-100 px-2 py-0.5 rounded border border-amber-300 font-extrabold">2D 다짐 도식</span>
    </div>
    <svg viewBox="0 0 480 180" class="w-full h-auto rounded bg-white border border-amber-200">
        <rect width="480" height="180" fill="#FEF3C7"/>
        <line x1="0" y1="130" x2="480" y2="130" stroke="#D97706" stroke-width="2"/>
        <rect x="0" y="130" width="480" height="50" fill="#FDE68A"/>
        
        # Roller Machine 2D
        <circle cx="100" cy="115" r="25" fill="#94A3B8" stroke="#475569" stroke-width="4"/>
        <circle cx="180" cy="120" r="20" fill="#64748B" stroke="#334155" stroke-width="3"/>
        <rect x="100" y="70" width="80" height="40" rx="5" fill="#F59E0B" stroke="#D97706" stroke-width="2"/>
        <text x="108" y="93" font-size="11" font-weight="black" fill="#78350F">10t 진동롤러</text>
        
        # Compaction Gauge Dial
        <circle cx="360" cy="85" r="35" fill="#FFFFFF" stroke="#D97706" stroke-width="3"/>
        <path d="M 360 85 L 380 65" stroke="#DC2626" stroke-width="3"/>
        <text x="330" y="138" font-size="12" font-weight="900" fill="#B45309">다짐도 ≥ 90% (KDS 기준)</text>
        <text x="333" y="153" font-size="11" font-weight="bold" fill="#0369A1">Ev2 ≥ 120 MPa</text>
    </svg>
</div>'''

SVG_STEP_04 = '''<div class="clickable-diagram cursor-pointer transition transform hover:scale-[1.02] hover:shadow-lg bg-emerald-50 border border-emerald-200 rounded-xl p-3 mb-3" onclick="openDiagramZoom(this.outerHTML, 'STEP 04: 성토 다짐 성과표 감리 승인 2D 도식')">
    <div class="text-[11px] font-bold text-emerald-800 mb-1 flex items-center justify-between">
        <span>🔍 클릭 시 대형 팝업 확대</span>
        <span class="text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-300 font-extrabold">2D 승인 도식</span>
    </div>
    <svg viewBox="0 0 480 180" class="w-full h-auto rounded bg-white border border-emerald-200">
        <rect width="480" height="180" fill="#ECFDF5"/>
        
        # Surveying Instrument 2D
        <polygon points="60,140 40,170 80,170" fill="#64748B"/>
        <rect x="50" y="110" width="20" height="30" fill="#F59E0B"/>
        <circle cx="60" cy="100" r="12" fill="#0284C7"/>
        <text x="30" y="90" font-size="11" font-weight="bold" fill="#0F172A">광학/토탈스테이션 실측</text>
        
        # Inspection Document Paper
        <rect x="220" y="25" width="180" height="135" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="2"/>
        <line x1="240" y1="45" x2="380" y2="45" stroke="#059669" stroke-width="2"/>
        <line x1="240" y1="65" x2="360" y2="65" stroke="#94A3B8" stroke-width="1.5"/>
        <line x1="240" y1="85" x2="370" y2="85" stroke="#94A3B8" stroke-width="1.5"/>
        <line x1="240" y1="105" x2="340" y2="105" stroke="#94A3B8" stroke-width="1.5"/>
        <text x="245" y="40" font-size="12" font-weight="900" fill="#047857">성토 다짐 검측 성과표</text>
        
        # Approval Seal Stamp
        <circle cx="350" cy="120" r="22" fill="#FEF2F2" stroke="#DC2626" stroke-width="2.5"/>
        <text x="333" y="125" font-size="12" font-weight="900" fill="#DC2626">감리 승인</text>
    </svg>
</div>'''

# Upgrade realManualHtmlMap.ts
map_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\03_process-map-web-v2(집행단계)\src\data\realManualHtmlMap.ts'
if os.path.exists(map_path):
    with open(map_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject Lightbox Zoom Modal handler into HTML template strings if missing
    if 'openDiagramZoom' not in content:
        zoom_script = '''<div id="zoomModal" class="fixed inset-0 z-[9999] hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4" onclick="this.classList.add(\\'hidden\\')">
    <div class="bg-white rounded-3xl p-6 max-w-4xl w-full max-h-[90vh] overflow-auto border-4 border-indigo-500 shadow-2xl relative" onclick="event.stopPropagation()">
        <button onclick="document.getElementById(\\'zoomModal\\').classList.add(\\'hidden\\')" class="absolute top-4 right-4 bg-slate-900 text-white font-black px-4 py-2 rounded-full text-sm hover:bg-slate-700">✕ 닫기</button>
        <h3 id="zoomTitle" class="text-xl font-black text-slate-900 mb-4 pb-2 border-b border-slate-200">고해상도 2D 시공 도식 확대보기</h3>
        <div id="zoomContent" class="flex justify-center items-center"></div>
    </div>
</div>
<script>
function openDiagramZoom(htmlContent, title) {
    var modal = document.getElementById('zoomModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'zoomModal';
        modal.className = 'fixed inset-0 z-[9999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4';
        modal.onclick = function() { modal.classList.add('hidden'); };
        modal.innerHTML = '<div class="bg-white rounded-3xl p-6 max-w-4xl w-full max-h-[90vh] overflow-auto border-4 border-indigo-500 shadow-2xl relative" onclick="event.stopPropagation()"><button onclick="document.getElementById(\\'zoomModal\\').classList.add(\\'hidden\\')" class="absolute top-4 right-4 bg-slate-900 text-white font-black px-4 py-2 rounded-full text-sm">✕ 닫기</button><h3 id="zoomTitle" class="text-xl font-black text-slate-900 mb-4 pb-2 border-b border-slate-200">고해상도 2D 시공 도식 확대보기</h3><div id="zoomContent" class="flex justify-center items-center"></div></div>';
        document.body.appendChild(modal);
    }
    document.getElementById('zoomTitle').innerText = title || '2D 시공 도식 확대보기';
    document.getElementById('zoomContent').innerHTML = htmlContent;
    modal.classList.remove('hidden');
}
</script>'''
        content = content.replace('</body>', zoom_script + '\n</body>')
    
    # Replace plain text step cards with SVG_STEP_01 .. SVG_STEP_04
    content = re.sub(
        r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 01</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
        SVG_STEP_01 + r'<div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 01</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
        content
    )
    content = re.sub(
        r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 02</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
        SVG_STEP_02 + r'<div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 02</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
        content
    )
    content = re.sub(
        r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 03</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
        SVG_STEP_03 + r'<div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 03</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
        content
    )
    content = re.sub(
        r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 04</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
        SVG_STEP_04 + r'<div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 04</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
        content
    )
    
    with open(map_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated realManualHtmlMap.ts with Light-Theme 2D SVG Diagrams & Lightbox Zoom Handlers.")

# Upgrade v8 HTML files
v8_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8'
upgraded_v8_count = 0

zoom_modal_html = '''
<div id="zoomModal" class="fixed inset-0 z-[9999] hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4" onclick="this.classList.add('hidden')">
    <div class="bg-white rounded-3xl p-6 max-w-4xl w-full max-h-[90vh] overflow-auto border-4 border-indigo-500 shadow-2xl relative" onclick="event.stopPropagation()">
        <button onclick="document.getElementById('zoomModal').classList.add('hidden')" class="absolute top-4 right-4 bg-slate-900 text-white font-black px-4 py-2 rounded-full text-sm hover:bg-slate-700">✕ 닫기</button>
        <h3 id="zoomTitle" class="text-xl font-black text-slate-900 mb-4 pb-2 border-b border-slate-200">고해상도 2D 시공 도식 확대보기</h3>
        <div id="zoomContent" class="flex justify-center items-center"></div>
    </div>
</div>
<script>
function openDiagramZoom(htmlContent, title) {
    var modal = document.getElementById('zoomModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'zoomModal';
        modal.className = 'fixed inset-0 z-[9999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4';
        modal.onclick = function() { modal.classList.add('hidden'); };
        modal.innerHTML = '<div class="bg-white rounded-3xl p-6 max-w-4xl w-full max-h-[90vh] overflow-auto border-4 border-indigo-500 shadow-2xl relative" onclick="event.stopPropagation()"><button onclick="document.getElementById(\\'zoomModal\\').classList.add(\\'hidden\\')" class="absolute top-4 right-4 bg-slate-900 text-white font-black px-4 py-2 rounded-full text-sm">✕ 닫기</button><h3 id="zoomTitle" class="text-xl font-black text-slate-900 mb-4 pb-2 border-b border-slate-200">고해상도 2D 시공 도식 확대보기</h3><div id="zoomContent" class="flex justify-center items-center"></div></div>';
        document.body.appendChild(modal);
    }
    document.getElementById('zoomTitle').innerText = title || '2D 시공 도식 확대보기';
    document.getElementById('zoomContent').innerHTML = htmlContent;
    modal.classList.remove('hidden');
}
</script>
'''

for root, dirs, files in os.walk(v8_path):
    for f in files:
        if f.endswith('.html'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file_obj:
                c = file_obj.read()
            
            modified = False
            
            # Inject Tailwind CDN & Noto Sans Font if missing
            if 'tailwindcss' not in c and '</head>' in c:
                tailwind_hdr = '<script src="https://cdn.tailwindcss.com"></script>\n<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n'
                c = c.replace('</head>', tailwind_hdr + '</head>')
                modified = True
                
            # Inject Zoom Modal script if missing
            if 'openDiagramZoom' not in c and '</body>' in c:
                c = c.replace('</body>', zoom_modal_html + '\n</body>')
                modified = True
            
            # Upgrade step cards
            if 'STEP 01' in c or 'STEP 1' in c or '단계별 세부 업무 절차' in c:
                # Replace plain text step cards with SVG illustrations
                c = re.sub(
                    r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 01</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
                    SVG_STEP_01 + r'<div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 01</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
                    c
                )
                c = re.sub(
                    r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 02</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
                    SVG_STEP_02 + r'<div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 02</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
                    c
                )
                c = re.sub(
                    r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 03</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
                    SVG_STEP_03 + r'<div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 03</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
                    c
                )
                c = re.sub(
                    r'<div class="bg-slate-50 dark:bg-slate-800/60 border[^"]*">\s*<div class="flex items-center gap-3 mb-3">\s*<span[^>]*>STEP 04</span>\s*<h4[^>]*>([^<]*)</h4>\s*</div>\s*<p[^>]*>([^<]*)</p>\s*</div>',
                    SVG_STEP_04 + r'<div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 mb-4"><div class="flex items-center gap-3 mb-2"><span class="text-xs font-black text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full">STEP 04</span><h4 class="text-base font-bold text-slate-900">\1</h4></div><p class="text-slate-600 text-sm leading-relaxed">\2</p></div>',
                    c
                )
                modified = True
            
            if modified:
                with open(fp, 'w', encoding='utf-8') as file_obj:
                    file_obj.write(c)
                upgraded_v8_count += 1

print(f"Successfully upgraded {upgraded_v8_count} HTML files in v8 with Light-Theme 2D SVG Diagrams & Lightbox Zoom handlers.")
