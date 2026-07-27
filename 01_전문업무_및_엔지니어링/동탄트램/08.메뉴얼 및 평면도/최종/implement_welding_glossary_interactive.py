import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

# Javascript / HTML Component to inject for Glossary & Scene Modal
common_style = """
    /* Glossary & Scene Popup CSS */
    .term-highlight {
        color: #0284c7 !important;
        font-weight: 700 !important;
        border-bottom: 2px dashed #0284c7 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        padding: 0 2px !important;
    }
    .term-highlight:hover {
        background: #e0f2fe !important;
        color: #0369a1 !important;
        border-radius: 4px !important;
    }
    .scene-link {
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        color: #059669 !important;
        font-weight: 700 !important;
        background: #ecfdf5 !important;
        border: 1px solid #10b981 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
        font-size: 0.8rem !important;
        cursor: pointer !important;
        margin-left: 8px !important;
        transition: all 0.2s ease !important;
        text-decoration: none !important;
    }
    .scene-link:hover {
        background: #d1fae5 !important;
        color: #065f46 !important;
    }
    /* Modal Window Styling */
    .glossary-modal {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(4px);
        align-items: center;
        justify-content: center;
    }
    .glossary-modal.active {
        display: flex;
    }
    .glossary-modal-content {
        background-color: #ffffff;
        margin: auto;
        padding: 24px;
        border: 1px solid #e2e8f0;
        width: 90%;
        max-width: 520px;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        position: relative;
        animation: modalFadeIn 0.3s ease;
        text-align: left;
    }
    @keyframes modalFadeIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .glossary-close {
        color: #94a3b8;
        position: absolute;
        right: 20px;
        top: 16px;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.2s;
    }
    .glossary-close:hover {
        color: #334155;
    }
"""

common_modal_html = """
<!-- Glossary & Scene Popup Modal Layer -->
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 시공장면 해설</h3>
        <div class="modal-body">
            <img id="modalImage" src="" style="width:100%; border-radius:10px; display:none; margin-bottom:15px; border: 1px solid #cbd5e1;" />
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<script>
const glossaryData = {
    'standard_rail': {
        title: '👷 정척레일 (Standard Rail)',
        desc: '제철소에서 압연 생산하여 반입되는 표준 길이의 단일 레일입니다. 한국도시철도 표준은 보통 25m 규격을 적용하며, 열차 주행 충격과 진동 소음의 원인이 되는 이음매를 줄이기 위해 용접장에서 여러 개를 이어 붙여 장대레일로 사전 가공합니다.'
    },
    'cwr': {
        title: '🛤️ 장대레일 (Continuous Welded Rail, CWR)',
        desc: '25m 정척레일의 끝단을 용접 접속하여 길이 200m 이상(트램의 경우 곡선 반경에 맞춰 수십 미터 단위도 포함)으로 연속시킨 궤도 레일입니다. 신축 이음매가 존재하지 않아 진동·소음이 획기적으로 차감되고 승차감이 우수하며, 레일 자체 신축 거동은 강력한 체결 장치와 도상 저항력으로 구속하여 흡수합니다.'
    },
    'thermit': {
        title: '🔥 테르밋 용접 (Thermit Welding)',
        desc: '알루미늄 분말과 산화철 분말의 발열 화학반응(2,000℃ 이상의 초고온)으로 생성되는 용융 철을 금형(몰드) 내부에 주입하여 레일 단면을 상호 융착 접합하는 현장 주조 용접 공법입니다. 전원 설비가 부족한 노선 현장에서 레일 조립 후 정밀 접속 시 주로 사용됩니다.',
        img: '../rail_welding_closeup.jpg'
    },
    'flash_butt': {
        title: '⚡ 플래시버트 용접 (Flash Butt Welding)',
        desc: '용접할 두 레일 단면 사이에 강한 전류를 흘려 불꽃(Flash) 아크 열로 강재 단면을 순간 융용시킨 후, 대용량 유압 잭으로 강한 압력을 주어 순간 접합하는 고성능 자동 기계식 용접법입니다. 인장 강도가 우수하고 품질 균질성이 매우 뛰어나 장대레일 기지 제작에 필수적으로 적용됩니다.',
        img: '../rail_welding_closeup.jpg'
    },
    'gas_pressure': {
        title: '💨 가스압접 (Gas Pressure Welding)',
        desc: '산소-아세틸렌 불꽃으로 레일 맞대기 단면을 고온(약 1,200℃, 용융점 이하)으로 균일 가열하여 연화시킨 후, 축방향 압축력을 주어 고체 상태에서 접촉면의 원자를 융합 접합하는 공법입니다. 용착 금속이나 전극 봉을 사용하지 않아 강재 조직 변형이 적은 특징이 있습니다.'
    },
    'ndt': {
        title: '🔍 비파괴검사 (Non-Destructive Testing, NDT)',
        desc: '용접부를 파괴하지 않고 내부 결함(미세 균열, 슬래그 혼입, 기포 등)을 검출하는 정밀 비파괴 검사입니다. 주로 초음파 탐상검사(UT) 및 자분 탐상검사(MT)를 적용하여 결함 지시가 없는 100% 합격 판정을 획득한 용접부만 현장 본선 부설로 공급할 수 있습니다.'
    },
    'yard': {
        title: '📐 레일 용접장 (Welding Yard)',
        desc: '반입된 25m 정척레일을 대용량 고정식 플래시버트/가스압접 장비 및 정밀 롤러대를 구축하여 장대레일(CWR)로 사전 대량 조립·제작하기 위해 궤도기지 내에 임시 마련하는 시공 전문 인프라 시설입니다.',
        img: '../rail_welding_yard_view.jpg'
    },
    'launching': {
        title: '🚚 장대레일 인양 및 인입 (Rail Launching)',
        desc: '사전 제작 완료된 200m 이상의 기다란 장대레일을 본선 궤도 현장 내부나 지하 터널 구간까지 롤러 베드 가이드를 따라 미끄러지듯 밀어 넣거나(Launching), 레일 전용 잭 크레인과 운반용 플랫카 열차 조합으로 수송 및 안치하는 정밀 기계화 시공 공정입니다.',
        img: '../rail_welding_yard_view.jpg'
    }
};

function openGlossary(termKey) {
    const data = glossaryData[termKey];
    if (!data) return;
    
    document.getElementById('modalTitle').innerText = data.title;
    document.getElementById('modalDescription').innerText = data.desc;
    
    const imgEl = document.getElementById('modalImage');
    if (data.img) {
        imgEl.src = data.img;
        imgEl.style.display = 'block';
    } else {
        imgEl.src = '';
        imgEl.style.display = 'none';
    }
    
    document.getElementById('glossaryModal').classList.add('active');
}

function openScene(sceneKey) {
    openGlossary(sceneKey);
}

function closeGlossaryModal() {
    document.getElementById('glossaryModal').classList.remove('active');
}

// Esc close key handler
window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeGlossaryModal();
    }
});
</script>
"""

# Modify Standard HTML
def modify_standard(fp):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Inject CSS
    if "</style>" in html:
        html = html.replace("</style>", common_style + "\n    </style>")
        
    # Inject highlights inside body
    # Standard rail
    html = html.replace("정척레일 15본", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span> 15본')
    html = html.replace("정척레일(25m)", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일(25m)</span>')
    # CWR
    html = html.replace("장대레일 제작하는", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 제작하는')
    html = html.replace("장대로 용접하는", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 용접하는')
    # Welding methods
    html = html.replace("테르밋 및", '<span class="term-highlight" onclick="openGlossary(\'thermit\')">테르밋</span> 및')
    html = html.replace("가스압접 용접을", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접 용접</span>을')
    # NDT
    html = html.replace("NDT 작업 공간", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT(비파괴검사)</span> 작업 공간')
    
    # Inject scene view button inside body
    html = html.replace("레일 용접장 선정 정량적", '레일 용접장 선정 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span> 정량적')
    
    # Inject Modal Div & JS right before </body>
    if "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Updated Standard file: {os.path.basename(fp)}")

# Modify Guideline HTML
def modify_guideline(fp):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Inject CSS
    if "</style>" in html:
        html = html.replace("</style>", common_style + "\n    </style>")
        
    # Inject highlights inside body
    html = html.replace("정척 레일을", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span>을')
    html = html.replace("장대레일로 1차", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 1차')
    html = html.replace("장대레일 반출", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 반출')
    html = html.replace("가스압접/플래시버트 용접하기", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>하기')
    html = html.replace("가스압접/플래시버트 용접용", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>용')
    html = html.replace("가스압접/플래시버트 용접 및", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span> 및')
    
    html = html.replace("비파괴 검사장", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 검사(NDT)장</span>')
    html = html.replace("비파괴검사(초음파/자분)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴검사(NDT)</span>')
    html = html.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>')
    
    # Inject scene view buttons
    html = html.replace("용접장 입지 검토", '용접장 입지 검토 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span>')
    html = html.replace("버(Burr) 전단", '버(Burr) 전단 <span class="scene-link" onclick="openScene(\'flash_butt\')">📸 용접 과정 보기</span>')
    html = html.replace("장대레일 반출", '장대레일 반출 <span class="scene-link" onclick="openScene(\'launching\')">📸 인입(Launching) 보기</span>')
    
    # Inject Modal Div & JS right before </body>
    if "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Updated Guideline file: {os.path.basename(fp)}")

# Modify Checklist HTML
def modify_checklist(fp):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Inject CSS
    if "</style>" in html:
        html = html.replace("</style>", common_style + "\n    </style>")
        
    # Inject highlights inside body
    html = html.replace("장대레일 제작 시", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 제작 시')
    html = html.replace("장대레일 영구", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 영구')
    html = html.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>')
    html = html.replace("NDT 용접부", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT 용접부</span>')
    
    # Inject scene link inside risk checkbox list
    html = html.replace("수평 오차 초과로", '수평 오차 초과로 <span class="scene-link" onclick="openScene(\'yard\')">📸 롤러 가이드 베드 보기</span>')
    
    # Inject Modal Div & JS right before </body>
    if "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Updated Checklist file: {os.path.basename(fp)}")

# Target files
std_files = [
    os.path.join(base_dir, "표준서", "레일 용접장 선정_표준서.html"),
    os.path.join(base_dir, "표준서", "3_레일 용접장 선정_표준서.html")
]
gui_files = [
    os.path.join(base_dir, "수행지침", "레일 용접장 선정_수행지침.html")
]
chk_files = [
    os.path.join(base_dir, "체크리스트", "레일 용접장 선정_체크리스트.html"),
    os.path.join(base_dir, "체크리스트", "3_레일 용접장 선정_체크리스트.html")
]

# Run
for sf in std_files: modify_standard(sf)
for gf in gui_files: modify_guideline(gf)
for cf in chk_files: modify_checklist(cf)

# Create 3_ prefixed guideline if not exists for link robustness
prefixed_gui = os.path.join(base_dir, "수행지침", "3_레일 용접장 선정_수행지침.html")
if not os.path.exists(prefixed_gui) and os.path.exists(gui_files[0]):
    import shutil
    shutil.copy2(gui_files[0], prefixed_gui)
    print(f"🎉 Successfully created prefixed guideline copy for links: {prefixed_gui}")

print("\n🎉 Completed implementing glossary popup module with images successfully!")
