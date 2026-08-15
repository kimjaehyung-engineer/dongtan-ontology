import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

// Electron file:// 로컬 로딩 시 CORS 차단 방지를 위해 crossorigin 속성 제거 플러그인
const removeCrossorigin = () => ({
  name: 'remove-crossorigin',
  transformIndexHtml(html: string) {
    return html.replace(/ crossorigin/g, '');
  },
});

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [react(), viteSingleFile(), removeCrossorigin()],
  server: {
    port: 8082,
  },
})
