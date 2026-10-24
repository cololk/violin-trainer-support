# Violin Trainer 隱私政策與支援網站

這個資料夾可獨立成為 GitHub Pages 儲存庫。公開內容只有繁體中文與英文的隱私政策、使用說明與支援頁。網站使用靜態 HTML 和本機 CSS，不需要 App 專案、模型、錄音、官網素材、JavaScript、外部字型或套件安裝。

目前是 build 78 的本機草稿。儲存庫名稱已確認為 `violin-trainer-support`；開發者名稱、支援 Email 與 GitHub 帳號待提供，網址待確認。沒有建立遠端儲存庫、設定遠端、推送或發布；缺少資料時發布檢查會停止。待提供資料集中在 [OWNER-INPUTS.md](OWNER-INPUTS.md)。

## 檔案與公開範圍

| 位置 | 用途 |
| --- | --- |
| `public/privacy.html`、`public/privacy-en.html` | 中英文隱私政策 |
| `public/support.html`、`public/support-en.html` | 中英文使用說明與支援 |
| `public/index.html` | 導向繁中隱私政策，保留英文入口 |
| `public/styles.css` | 共用樣式，支援桌面及手機 |
| `content.json` | App 核准文案的網站副本與四項公開聯絡設定 |
| `deployment.json` | GitHub 帳號與儲存庫名稱 |
| `tools/site.py`、`tools/test_site.py` | 產生頁面與發布前檢查 |
| `.github/workflows/pages.yml` | 手動發布流程，只上傳 `public/` |

`public/` 必須恰好包含上述六個檔案，額外檔案、連結檔、外部載入資源、過期頁面或失效內部連結都會使檢查失敗。README、設定檔與工具不會進入 Pages 網站，但如果日後使用公開儲存庫，這些儲存庫檔案也能被閱讀，因此其中只能放可公開資訊。

## 本機檢查與預覽

以下命令在這個資料夾執行，使用 Python 3.9 或更新版本；macOS 可用 `/usr/bin/python3` 替換 `python3`。

```sh
python3 tools/site.py --check
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 -m http.server 8000 --bind 127.0.0.1 --directory public
```

瀏覽 `http://127.0.0.1:8000/privacy.html`。HTTP 伺服器只綁定本機，按 Control-C 結束。草稿標籤與 `noindex` 會在四項有效公開聯絡資料補齊後移除；`noindex` 不提供存取權限保護。

## 更新文案與公開資料

App 專案仍是文案來源。在 App 專案根目錄執行：

```sh
/usr/bin/python3 Tools/PrivacySupport/prepare_github_pages.py
/usr/bin/python3 Tools/PrivacySupport/prepare_github_pages.py --check
```

這只讀取 App 的公開隱私／支援 JSON，再更新本資料夾；不會改動 App 或原有 `Website/`。同步會覆寫 `content.json`，因此同一輪的姓名、Email 與正式網址應先更新到 App 共用設定，再同步，避免兩邊分歧。網站僅額外說明 GitHub Pages 的 IP 安全記錄，來源為 [GitHub 官方資料收集說明](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)。

獨立儲存庫也可直接編輯 `content.json` 後執行 `python3 tools/site.py --write`，但發布前需把相同內容同步回 App 並重新核對。既有政策內容與支援信件處理方式仍需擁有者確認，請見待提供資料。

## 日後發布步驟

以下是準備好的操作說明，本次未執行。當你決定公開時：

1. 確定 GitHub 帳號與獨立網站儲存庫名稱。免費 GitHub Pages 使用公開儲存庫；只把本資料夾的內容（含 `.github` 與 `.gitignore`）放到新儲存庫根目錄，保留完整工具與內容檔。不複製 App 儲存庫的 `.git`、提交歷史或任何其他資料夾。
2. 填寫 `deployment.json` 的 `githubOwner`、`repositoryName`，以及 `content.json` 的公開開發者名稱、支援 Email、隱私政策與支援網址。專案型網址為 `https://帳號.github.io/儲存庫/privacy.html` 與 `support.html`；帳號型儲存庫 `帳號.github.io` 則沒有儲存庫路徑。這份設定暫不使用自有網域或 `CNAME`。
3. 重新產生頁面，執行 `python3 tools/site.py --check --require-public-details`。補齊前預期回傳 exit 2；完成後必須成功。
4. 在獨立儲存庫提交並推送，於 **Settings → Pages → Build and deployment → Source** 選擇 **GitHub Actions**。檢查 `github-pages` environment 的部署分支符合準備使用的預設分支，並在可設定時啟用 **Enforce HTTPS**。
5. 到 **Actions → Publish privacy and support pages → Run workflow** 手動啟動。流程先測試及檢查，確認帳號／儲存庫與網址相符，再上傳六個公開檔案並部署。一般 push 或 pull request 都不觸發發布。
6. 用未登入瀏覽器確認四個正式頁面可讀、語言切換與 Email 正確，再把正式中英文 URL 填入 App 與 App Store Connect 對應語系欄位。網站公開完成不等同 App 已上架或隱私申報已定案。

工作流程放在本資料夾內；目前在 App 儲存庫中並不是根目錄的 `.github/workflows`，不會被當作 App 的 Actions 執行。只有移到獨立儲存庫根目錄後才成為工作流程。

## 發布設定依據

- [GitHub Pages 自訂工作流程](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)：artifact、權限與 `github-pages` environment。
- [GitHub Pages HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)。
- [GitHub Pages 方案與網址](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)。

Actions 已依 2026-10-24 查得的官方版本固定 commit SHA：checkout v6、configure-pages v5、upload-pages-artifact v4、deploy-pages v4。更新版本時應重新核對官方來源與工作流程。
