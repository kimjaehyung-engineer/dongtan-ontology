const { app, BrowserWindow } = require('electron');
const path = require('path');

// 윈도우 GPU 디스크 캐시 락 및 권한 에러(0x5) 회피 스위치
app.commandLine.appendSwitch('disable-gpu-shader-disk-cache');
app.commandLine.appendSwitch('disable-gpu');
app.commandLine.appendSwitch('no-sandbox');

app.whenReady().then(() => {
  // 전용 UserData 경로 지정으로 캐시 락 해결
  try {
    app.setPath('userData', path.join(app.getPath('appData'), 'DongtanTramProcessMapV2'));
  } catch (e) {
    console.error('Failed to set userData path:', e);
  }

  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1600,
    height: 950,
    title: '동탄도시철도(트램) 사전토공사 프로세스 맵',
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false, // 로컬 HTML 파일 뷰어 및 CORS 호환용
    },
  });

  const iconPath = path.join(__dirname, 'dist', 'favicon.ico');
  if (require('fs').existsSync(iconPath)) {
    mainWindow.setIcon(iconPath);
  }

  mainWindow.maximize();
  mainWindow.setMenuBarVisibility(false);

  // 렌더러 프로세스 콘솔 로그 가로채기
  mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
    console.log(`[RENDERER CONSOLE] level:${level} | ${message} (at ${sourceId}:${line})`);
  });

  mainWindow.webContents.on('render-process-gone', (event, details) => {
    console.error('[RENDERER GONE]', details);
  });

  // Vite 빌드 디렉토리의 index.html 로드
  const indexPath = path.join(__dirname, 'dist', 'index.html');
  mainWindow.loadFile(indexPath).catch((err) => {
    console.error('Failed to load index.html:', err);
  });

  // F12 또는 Ctrl+Shift+I 키 입력 시 개발자 도구 토글 기능
  mainWindow.webContents.on('before-input-event', (event, input) => {
    if (input.key === 'F12' || (input.control && input.shift && input.key.toLowerCase() === 'i')) {
      mainWindow.webContents.toggleDevTools();
      event.preventDefault();
    }
  });
}

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
