UAS R&D Hub (Enhanced Version) - 開發者與維護指南
UAS R&D Hub 是一個基於單一 HTML 檔案的輕量級、高效能無人機技術文件系統。它整合了戰略規劃、硬體拆解、MCU 架構分析、控制理論及軟體開發環境等核心知識，專為無人機系統工程師與研發人員設計。
本專案採用 SPA (Single Page Application) 概念，無需後端伺服器或繁雜的編譯流程，即可提供流暢的互動式閱讀體驗。
🚀 核心功能 (Key Features)
單檔運作 (Single File Architecture)：所有邏輯、樣式與內容封裝於單一 HTML，部署極其簡單。
互動式視覺化：
整合 Chart.js 繪製雷達圖與 PID 響應曲線。
動態 Pinout 定義互動介面。
MathJax 數學公式渲染 (FOC, PID)。
使用者體驗優化：
全文檢索：前端即時搜尋索引 (searchData)。
閱讀輔助：閱讀進度條、書籤功能 (Local Storage)、回到頂部按鈕。
主題切換：深色/淺色模式 (預設為深色工程風格)。
新手導覽：互動式功能導覽 (Tour)。
響應式設計：完整支援桌面端與行動端操作。
🛠️ 技術棧 (Tech Stack)
本專案不依賴任何 Build Tool (如 Webpack/Vite)，直接使用 CDN 引入資源：
Core Structure: Semantic HTML5
Styling: Tailwind CSS (CDN)
Charts: Chart.js
Math: MathJax
Icons: FontAwesome
Logic: Vanilla JavaScript (ES6+)
📂 快速開始 (Quick Start)
下載: 取得 UAS R&D Hub - Enhanced Version.html 檔案。
開啟: 直接使用現代瀏覽器 (Chrome, Edge, Firefox, Safari) 開啟該檔案。
注意：由於使用 CDN 資源，開啟時請確保電腦已連接網際網路。
🤝 無損整合標準作業程序 (Integration SOP)
若您需要新增技術章節，為確保搜尋索引與導航功能的完整性，請務必遵循以下四個步驟：
1. 判斷資料類別 (Categorize)
首先，將新資料歸類於以下四大領域之一，這決定了它在側邊欄的位置：
Strategic (戰略規劃): 技術路線圖、硬體拆解報告、市場分析。
Hardware (硬體工程): MCU 架構、電路設計參考、馬達與動力系統。
Logic (控制與邏輯): 控制理論 (PID)、通訊協議 (DShot/MavLink)、演算法。
Soft/Ops (軟體與營運): 開發環境建置、軟體棧 (Software Stack)、故障診斷。
2. 建立內容區塊 (Create Section)
在 HTML 的 <main> 標籤區域內（通常放在現有 <section> 之後），複製以下 HTML 模板並進行修改。
⚠️ 注意： 請務必保留 hidden animate-section relative 這些 CSS Class，以維持轉場動畫效果。
<!-- ==================== [編號]. 新章節名稱 ==================== -->
<section id="section-new-topic" class="mb-16 hidden animate-section relative">
    <!-- 書籤功能掛鉤 (data-bookmark 必須與 id 一致) -->
    <i class="fa-regular fa-bookmark bookmark-badge" data-bookmark="section-new-topic"></i>
    
    <header class="mb-8 border-b border-slate-800 pb-4">
        <h2 class="text-3xl font-bold text-slate-100 mb-2">新章節標題 (Title)</h2>
        <div class="flex items-center gap-2 text-slate-400 text-sm">
            <!-- source-badge 樣式請參考樣式指南 -->
            <span class="source-badge badge-standard">資料來源類型</span>
            <span>詳細來源說明</span>
        </div>
    </header>

    <!-- 內容容器 -->
    <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h3 class="text-xl font-bold text-sky-400 mb-4">
            <i class="fa-solid fa-code mr-2"></i>子標題
        </h3>
        <p class="text-sm text-slate-300">這裡放置內容...</p>
    </div>
</section>


3. 更新導覽列 (Update Sidebar)
在 HTML 的 <nav id="sidebar"> 區塊內，找到對應的類別標題，並在其下方新增導航連結：
<a href="#" data-section="section-new-topic" class="nav-item block px-6 py-3 text-sm font-medium text-slate-400 hover:bg-slate-800 hover:text-slate-200 border-l-4 border-transparent transition-colors">
    <!-- 請更換適合的 FontAwesome 圖示 -->
    <i class="fa-solid fa-file-lines mr-2 w-4"></i>新章節選單名稱
</a>


4. 註冊搜尋索引 (Register Index)
這是最關鍵的一步！ 為了讓「全文搜尋」與「書籤功能」生效，您必須在檔案底部的 <script> 區塊中，找到 searchData 陣列並新增物件。
const searchData = [
    // ... (保留原有資料) ...
    { 
        title: '新章節標題', 
        section: 'section-new-topic', // 必須與 HTML id 一致
        keywords: ['keyword1', 'keyword2', '關鍵字', '搜尋詞'] 
    }
];


🎨 樣式指南 (Style Guide)
為了保持視覺體驗的一致性，請嚴格使用以下 Tailwind CSS 組合：
背景與結構
主背景: bg-slate-900 (卡片、區塊背景)
次背景/強調: bg-slate-950 (表格、程式碼區塊、深層背景)
文字顏色
一般文字: text-slate-300 (主要內容) 或 text-slate-400 (次要資訊)
標題高亮: text-slate-100
功能色系 (Functional Colors)
請根據內容屬性選擇對應的顏色組合（文字 + 邊框）：
Emerald (綠色系): text-emerald-400, border-emerald-800
用途: 硬體規格、Datasheet、實機拆解、成功狀態。
Sky (藍色系): text-sky-400, border-sky-800
用途: 軟體架構、通訊協議、資訊說明。
Amber (橘黃色系): text-amber-400, border-amber-800
用途: 電源系統、警告、Debug 資訊、物理特性。
Rose (紅色系): text-rose-400, border-rose-800
用途: 核心處理器、安全開關 (Safety)、Failsafe 保護機制。
📄 License & Credits
Status: Internal Use / Engineering Reference
Strategy By: Marlon (Integration Strategy Agent)
