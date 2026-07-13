import os
import shutil

def apply_optimization(file_path):
    print(f"Applying performance optimization to: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_opt"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    # 1. Inject content-visibility CSS
    css_to_inject = """
        /* 웹 성능 최적화: 화면 밖 DOM 렌더링 연산 생략 */
        article.answer-sheet {
            content-visibility: auto;
            contain-intrinsic-size: 1px 1200px;
        }
    """
    
    if "article.answer-sheet {" not in content or "content-visibility" not in content:
        # Style tag closing replacement
        content = content.replace("</style>", css_to_inject + "\n</style>", 1)
        print("Successfully injected content-visibility CSS.")
    else:
        print("content-visibility CSS already exists or overlapping class found.")
        
    # 2. Update MathJax config to prevent initial full-page typesetting
    old_mathjax_config_pattern = """            options: {
                ignoreHtmlClass: 'tex2jax_ignore',
                processHtmlClass: 'tex2jax_process'
            }"""
            
    new_mathjax_config = """            options: {
                ignoreHtmlClass: 'tex2jax_ignore',
                processHtmlClass: 'tex2jax_process'
            },
            startup: {
                typeset: false
            }"""
            
    if old_mathjax_config_pattern in content:
        content = content.replace(old_mathjax_config_pattern, new_mathjax_config, 1)
        print("Successfully updated MathJax config to typeset: false (initial block prevented).")
    else:
        # Fallback loose replacement if spacing differs
        loose_target = "options: {"
        loose_replacement = "options: {\n                ignoreHtmlClass: 'tex2jax_ignore',\n                processHtmlClass: 'tex2jax_process'\n            },\n            startup: {\n                typeset: false\n            }"
        
        # Check if typeset: false already in content
        if "typeset: false" not in content:
            # We can replace options part
            content = content.replace("options: {", loose_replacement, 1)
            print("Successfully updated MathJax config via fallback loose pattern.")
        else:
            print("MathJax startup options already optimized.")
            
    # 3. Inject JS Lazy Typesetting Script before </body>
    js_lazy_script = """
    <script id="mathjax-lazy-loader">
    document.addEventListener('DOMContentLoaded', () => {
        // 1. 초기 화면에 보이는 첫 3개 문항만 빠르게 수식 렌더링
        setTimeout(() => {
            if (window.MathJax && MathJax.typesetPromise) {
                const firstArticles = Array.from(document.querySelectorAll('article.answer-sheet')).slice(0, 3);
                MathJax.typesetPromise(firstArticles).catch(err => console.log(err));
            }
        }, 400);

        // 2. IntersectionObserver를 통해 화면 스크롤 시 해당 문항만 수식 렌더링
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                     const target = entry.target;
                     if (!target.classList.contains('math-rendered')) {
                         target.classList.add('math-rendered');
                         if (window.MathJax && MathJax.typesetPromise) {
                             MathJax.typesetPromise([target]).catch(err => console.error(err));
                         }
                     }
                }
            });
        }, {
            root: null,
            rootMargin: '100px 0px 400px 0px', // 스크롤이 도달하기 전 아래쪽 400px 영역에서 미리 렌더링 시작
            threshold: 0
        });

        document.querySelectorAll('article.answer-sheet').forEach(art => {
            observer.observe(art);
        });

        // 3. 사이드바 링크 클릭 시 해당 문항 강제 수식 렌더링 (즉각 시각화)
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href && href.startsWith('#')) {
                    const targetArt = document.querySelector(href);
                    if (targetArt && !targetArt.classList.contains('math-rendered')) {
                        targetArt.classList.add('math-rendered');
                        if (window.MathJax && MathJax.typesetPromise) {
                            MathJax.typesetPromise([targetArt]).catch(err => {});
                        }
                    }
                }
            });
        });
    });
    </script>
    """
    
    if "mathjax-lazy-loader" not in content:
        content = content.replace("</body>", js_lazy_script + "\n</body>", 1)
        print("Successfully injected MathJax Lazy Loading JS Script.")
    else:
        print("MathJax Lazy Loading JS Script already exists.")
        
    with open(file_path, "w", encoding="utf-8") as f_out:
        f_out.write(content)
    print(f"Optimizations applied and saved to: {file_path}")

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        apply_optimization(v2_path)
        
        # Sync to public/index.html
        if os.path.exists(public_path):
            print(f"\nSyncing optimized HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied optimized HTML to public/index.html.")
        else:
            print(f"Warning: public/index.html does not exist at {public_path}")
    else:
        print(f"Error: {v2_path} does not exist!")
