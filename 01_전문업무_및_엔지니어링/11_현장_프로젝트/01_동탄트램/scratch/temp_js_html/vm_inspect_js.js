import fs from 'fs';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
const jsCode = scriptMatch[1];

console.log("=== Pure Node Mock DOM Runtime Inspection ===");

function createMockElement(id) {
  return {
    id: id,
    innerHTML: '',
    innerText: '',
    style: {},
    classList: {
      add: () => {},
      remove: () => {}
    },
    appendChild: function(child) {
      this.innerHTML += (child.outerHTML || child.innerHTML || '');
    },
    querySelectorAll: () => [],
    addEventListener: () => {},
    setAttribute: () => {},
    getBoundingClientRect: () => ({ width: 1200, height: 600 })
  };
}

const mockDoc = {
  getElementById: (id) => createMockElement(id),
  querySelectorAll: () => [],
  createElement: (tag) => ({
    tagName: tag,
    className: '',
    innerHTML: '',
    style: {},
    appendChild: function(c) {},
    addEventListener: () => {}
  })
};

try {
  const sandbox = {
    document: mockDoc,
    window: {
      addEventListener: () => {},
      innerWidth: 1400,
      innerHeight: 800
    },
    console: console,
    setTimeout: (fn) => fn(),
    setInterval: () => {}
  };

  const evalFunc = new Function('document', 'window', 'console', 'setTimeout', jsCode);
  evalFunc(mockDoc, sandbox.window, console, sandbox.setTimeout);
  
  console.log("✓ Evaluated script without crashing!");

} catch (err) {
  console.error("❌ CRASH ERROR DURING SCRIPT EVALUATION:", err);
}
