# 網站待提供與確認資料

本清單只處理隱私政策與支援網站。資料未補齊時，網站保留為本機草稿，發布檢查預期停止。請提供可公開的資料；不需要 GitHub 密碼、權杖、Apple 帳號密碼、私人錄音或研究資料。

2026-10-24：擁有者已確認採用目前四個中英文頁面的版面；獨立儲存庫名稱已定為 `violin-trainer-support`。接下來補齊公開資料，再確認正式網址。以下範例僅供填寫參考，沒有寫入網站設定。

## 需要提供

| 資料 | 用途／填入位置 | 目前狀態 | 填寫範例（示意） |
| --- | --- | --- | --- |
| GitHub 帳號名稱 | `deployment.json` → `githubOwner` | 空白；提供個人頁網址中的帳號名稱，不是顯示暱稱 | `violin-dev-demo` |
| 獨立網站儲存庫名稱 | `deployment.json` → `repositoryName` | 已確認，不需再提供；尚未建立遠端儲存庫 | `violin-trainer-support` |
| 公開開發者名稱 | `content.json` → `configuration.developerName`，並同步 App 設定 | 空白；會顯示在四個頁面，可中英文並列 | `王小明 / Ming Wang` |
| 支援 Email | `content.json` → `configuration.supportEmail`，並同步 App 設定 | 空白；提供你能收信且願意公開的信箱 | `support@example.com`（僅為範例） |

## 可直接回填

```text
GitHub 帳號：
公開開發者名稱：
支援 Email：
支援資料保存與刪除：同意依目前政策執行／需要修改（請說明）
額外後台或分析服務：沒有／有（請列出名稱與用途）
```

「目前政策」指支援信件與附件只用於處理問題及必要後續追蹤，不再需要時刪除；使用者可回覆原信件要求刪除，研究或模型訓練用途另行取得同意。若你的實際作法不同，先提供差異，再調整政策。

「額外後台或分析服務」指目前專案說明以外，由你另外使用的服務。若沒有，可直接填「沒有」。正式網址由 GitHub 帳號與已確認的儲存庫名稱產生，這次不需自行填寫。

## 可由帳號與儲存庫名稱產生，需確認

以下是格式，不是已存在的網站：

```text
https://<githubOwner>.github.io/violin-trainer-support/privacy.html
https://<githubOwner>.github.io/violin-trainer-support/privacy-en.html
https://<githubOwner>.github.io/violin-trainer-support/support.html
https://<githubOwner>.github.io/violin-trainer-support/support-en.html
```

這一輪採用專案型 GitHub Pages 與 GitHub 預設網域，網址保留 `/violin-trainer-support/` 路徑；不需要購買自有網域。

## 發布前需確認的內容與操作

- 確認現有政策如實描述你的作法，尤其支援信件與音訊附件的保存、使用與刪除，以及是否還有專案以外的後台／分析服務。網站已附 GitHub Pages 基於安全目的記錄 IP 的說明；網站沒有加入追蹤程式、外部字型或表單。
- 補齊公開開發者名稱與支援信箱後，核對實際顯示及正式網址；目前版面已確認採用。公開儲存庫會讓網站工具和設定也可讀，因此不放私人聯絡或審查專用資料。
- 日後由你登入 GitHub 建立獨立儲存庫，或明確授權協助建立／推送與公開；本次只準備檔案。按照 README 設定 Pages，手動啟動發布後，才能驗證正式網址與 HTTPS。
- 公開後，將確認過的網址與相同聯絡資料同步 App 共用設定及 App Store Connect；正式 App Privacy 仍沿用 build 78 的待確認流程。

不會因為取得上述文字資料就自動推送或公開。歷史網站、App 原始碼、判弦模型與私人研究資料都不屬於這個獨立網站儲存庫。
