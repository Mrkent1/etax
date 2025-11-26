## Agent Guide – eTax Mobile HTML (for Cursor Assistants)

This document tells any AI assistant (in Cursor) how to work on this project so that the UX/UI stays consistent with the original eTax Mobile app and with anh Nghĩa’s expectations.

---

### 1. Who is the Product Owner?

- Product Owner: **anh Nghĩa**.
- Assumptions:
  - He **does not code** and **does not manage servers**.
  - He cares about:
    - Screens looking **exactly like** the real eTax Mobile app (from screenshots).
    - User flows being **simple, consistent, and correct**.
    - Explanations in **simple Vietnamese**, minimal jargon.

**Communication rules:**
- Always call him **“anh Nghĩa”**.
- Explain:
  - **Mục tiêu** (goal) → **Cách làm** (steps) → **Tại sao** (reason) → **Ví dụ** (example).
- Avoid heavy technical terms; if you must use one, **immediately explain it** in plain language.
- Do **not** create long formal documentation unless he explicitly asks (this `agent.md` is an exception).

---

### 2. Project overview

- This is a **pure HTML/CSS/JS** clone of the eTax Mobile app UI.
- Main folders:
  - `assets/` – All icons and images (mostly `.webp`, some `.svg`).
  - `css/`, `home.css`, `login.css` – Global and page-level styles.
  - `js/` – Shared logic:
    - `auth.js` – simple localStorage-based auth (no real backend).
    - `utils.js` – helpers for navigation, viewport, service worker, `requireAuth`, etc.
  - `pages/` – all feature pages (register tax, declare tax, invoices, lookup, support, profile,…).
  - `Clone 2 -.../Clone 2` – **source screenshots** of the real app. Treat these as “design spec”.

**Key entry points:**
- `index.html` → redirects to `login.html`.
- `login.html` (+ `login.js`) – login screen using MST + password.
- `home.html` (+ `home.js`) – main dashboard with profile card, feature grid, sidebar.

---

### 3. UX/UI cloning principles

**3.1 Mapping screenshots to HTML files**
- One screenshot corresponds to **one main HTML file**:
  - Login screen → `login.html`.
  - Home (avatar, grid of services) → `home.html`.
  - “Đăng ký thuế” menu → `pages/dang-ky-thue.html`.
  - “Khai thuế” menu → `pages/khai-thue.html`.
  - “Hoá đơn điện tử” menu → `pages/hoa-don-dien-tu.html`.
  - “Thông tin tài khoản” (big avatar, red buttons, info list) → `pages/thong-tin-tai-khoan.html`.
  - Other menus (Hỗ trợ, Tiện ích, Hỗ trợ quyết toán, Nhóm nộp thuế, Tra cứu…) → files with same names in `pages/`.

Whenever you see a screenshot, your first task is to:
1. Identify **which HTML file** it should map to.
2. Use that file as the base for layout.

**3.2 Reuse icons from `assets/`**

- Icon groups:
  - `index*.webp` – grid of services on home + sidebar services.
  - `dk*.webp`, `hs*.webp`, `nt*.webp` – register tax, registration dossiers, dependent info.
  - `kt*.webp` – tax declaration.
  - `hddt*.webp` – e-invoices.
  - `ti*.webp`, `tienich.webp` – utilities.
  - `ht*.webp`, `htqt*.webp`, `hotro.webp` – support & support for finalization.
  - `avatar.webp`, `logo-192.webp`, `logo.webp` – avatars and logos.
  - `icon-*.webp/svg` – small icons (MST field, password, eye, QR, change password, delete, etc.).

If the screenshot shows an icon that does not exist:
- Create a new small `.webp` (approx 48–76px) with similar style.
- Name it consistently with the group (e.g. `kt5.webp`, `nt9.webp`).
- Place it under `assets/` and reference it from HTML.

**3.3 Layout rules**

- Headers on subpages:
  - Reuse structure:
    - `header.page-header` with `.header-back`, `.header-title`, and optionally `.header-home` or `.header-spacer`.
  - Colors, padding, font-size are set mainly via:
    - `css/common.css` and each page’s `*.css`.

- Cards (feature tiles):
  - Always use:
    - `.section-card` → the button container.
    - `.section-card-icon` → holds image (icon).
    - `.section-card-text` → label, often with `<br>` for line breaks.
  - Adjust text and `<br>` positions to match screenshot line breaks.

- Do **not** redesign the markup from scratch:
  - Prefer adjusting CSS in `*.css` rather than changing HTML structure.
  - Only modify HTML structure if absolutely necessary to match the design.

**3.4 Real data fields**

- Login:
  - MST input → `#mst-input`.
  - Password input → `#password-input`.
  - Error fields → `#mst-error` and `#error-message`.
  - Logic in `login.js` and `js/auth.js`.

- Profile / account info:
  - Page: `pages/thong-tin-tai-khoan.html`.
  - IDs:
    - `#account-mst`, `#account-fullname`, `#account-address`,
    - `#account-tax-office`, `#account-phone`, `#account-email`.
  - Filled via `thong-tin-tai-khoan.js` using `getUserSession()` and `getProfile()`.

Many other pages are currently **placeholders** (“Chức năng đang được phát triển”). When screenshots show real forms for these screens, they should be implemented inside `<main class="page-content">` using existing styles from `common.css`.

---

### 4. Navigation and auth rules

- Redirects:
  - `index.html` → immediately navigates to `login.html`.

- Login flow:
  - If session exists → `login.js` redirects to `home.html`.
  - If MST + password are correct → store session (localStorage) → `home.html`.
  - If invalid → display error message under the form, no redirect.

- Home:
  - `home.js` uses `isAuthenticated()`:
    - If not authenticated → `navigateTo('login.html')`.
  - Feature tiles and sidebar links are normal `<a href="pages/...">` links to `pages/*.html`.

- Protected pages:
  - Every page in `pages/` should call:
    - `requireAuth('../login.html')` from `js/utils.js`.
  - If no valid session → redirect back to login.

- Logout:
  - Sidebar “Đăng xuất” button:
    - Calls `logoutUser()` from `auth.js`.
    - Then redirects to `login.html`.

Do not change these flow rules unless anh Nghĩa explicitly asks.

---

### 5. Tool usage (Cursor + Browser tools)

**5.1 File/code tools**
- Use:
  - `read_file`, `list_dir`, `grep` to explore the repo.
  - `apply_patch` to edit files (HTML, CSS, JS, or add assets by name).
- Do not create:
  - Huge binaries.
  - Obfuscated code or meaningless content.

**5.2 Browser tools (very important for UX/UI)**

Whenever you modify HTML or CSS that affects layout:
- Use browser tools to **visually validate**:
  - `mcp_cursor-ide-browser_browser_navigate` to open the relevant page.
  - `mcp_cursor-ide-browser_browser_snapshot` to inspect structure.
  - `mcp_cursor-ide-browser_browser_take_screenshot` to compare with the original screenshot.
  - Interact:
    - Click cards and menu items.
    - Scroll.
    - Test login, logout, and protected-page redirects.

Goal: ensure that what the user sees in the browser **matches the screenshot** as closely as possible (spacing, icons, text, and flows).

---

### 6. How to explain changes to anh Nghĩa

When you finish a batch of changes:
- Summarize in **plain Vietnamese**:
  - “Em vừa chỉnh lại màn X để icon, chữ, màu giống hình chụp. Bây giờ bấm vào nút Y sẽ nhảy sang trang Z đúng như app gốc.”
- Avoid dumping large code blocks in explanations.
- Focus on:
  - What changed in terms of **màn hình** (screen).
  - **Hành vi** (what happens when you tap/click).
  - How this brings it **closer to the original screenshot**.


