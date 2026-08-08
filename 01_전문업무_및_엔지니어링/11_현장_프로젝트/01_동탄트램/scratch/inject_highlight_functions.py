# -*- coding: utf-8 -*-
manual_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼v1.html"

with open(manual_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Injection target: after line 4923 (closeModalOnBackdrop closing brace)
# and before line 4925 (</script>)
# We insert before the </script> at line 4925 (index 4924)

inject_code = """
// ============================================================
// SVG Highlight Simulation Functions (highlightSegment / resetHighlight / showInfo)
// ============================================================
function highlightSegment(className) {
    var allElements = document.querySelectorAll('.interactive-element');
    var highlightStyle = '';
    if (className === 'track-1') highlightStyle = 'highlight-track-1';
    if (className === 'track-2') highlightStyle = 'highlight-track-2';
    if (className === 'slab-a')  highlightStyle = 'highlight-slab-a';
    if (className === 'slab-b')  highlightStyle = 'highlight-slab-b';
    allElements.forEach(function(el) {
        if (el.classList.contains('segment-' + className)) {
            el.classList.add(highlightStyle);
            el.style.opacity = '1';
        } else {
            el.style.opacity = '0.35';
        }
    });
}

function resetHighlight() {
    var allElements = document.querySelectorAll('.interactive-element');
    var highlightClasses = ['highlight-track-1', 'highlight-track-2', 'highlight-slab-a', 'highlight-slab-b'];
    allElements.forEach(function(el) {
        highlightClasses.forEach(function(cls) { el.classList.remove(cls); });
        el.style.opacity = '1';
    });
}

function showInfo(title, desc) {
    var titleBox = document.getElementById('info-title');
    var descBox  = document.getElementById('info-desc');
    var panel    = document.getElementById('info-panel');
    if (!titleBox || !descBox || !panel) return;
    titleBox.innerHTML = '<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#3b82f6;margin-right:6px;"></span>' + title;
    descBox.textContent = desc;
    panel.style.background = '#eff6ff';
    panel.style.borderColor = '#93c5fd';
    setTimeout(function() {
        panel.style.background = '';
        panel.style.borderColor = '';
    }, 600);
}

"""

# Find line index 4924 (0-indexed = 4924-1 = 4923 before </script>)
target_line_index = 4924  # 0-indexed for line 4925
lines.insert(target_line_index, inject_code)

with open(manual_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Injection complete. Total lines:", len(lines))
# Verify
with open(manual_path, "r", encoding="utf-8") as f:
    content = f.read()
print("highlightSegment defined:", "function highlightSegment" in content)
print("resetHighlight defined:", "function resetHighlight" in content)
print("showInfo defined:", "function showInfo" in content)
