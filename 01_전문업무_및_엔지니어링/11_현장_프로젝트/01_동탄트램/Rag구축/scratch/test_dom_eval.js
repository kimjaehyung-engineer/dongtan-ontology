const fs = require('fs');

// Read script
const js = fs.readFileSync('scratch/script_0.js', 'utf-8');

// Mock DOM
class MockElement {
  constructor(tag, id = '') {
    this.tag = tag;
    this.id = id;
    this.children = [];
    this.style = {};
    this.classList = {
      add: (c) => this.classes.push(c),
      remove: (c) => this.classes = this.classes.filter(x => x !== c),
      toggle: (c, v) => {}
    };
    this.classes = [];
    this.innerHTML = '';
    this.innerText = '';
  }
  appendChild(child) {
    this.children.push(child);
  }
  querySelector(sel) {
    return new MockElement('div');
  }
  querySelectorAll(sel) {
    return [];
  }
}

const docElements = {
  'rootFolderPathDisplay': new MockElement('div', 'rootFolderPathDisplay'),
  'docCountBadge': new MockElement('span', 'docCountBadge'),
  'docList': new MockElement('div', 'docList')
};

global.document = {
  getElementById: (id) => docElements[id] || new MockElement('div', id),
  createElement: (tag) => new MockElement(tag)
};
global.window = {};

// Evaluate the script functions
try {
  eval(js);
  console.log('Eval successful!');
} catch (e) {
  console.error('Eval error:', e);
}
