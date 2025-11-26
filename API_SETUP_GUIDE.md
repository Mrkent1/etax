# GitHub Personal Access Token Setup

## Tạo GitHub Token (5 phút)

### Bước 1: Vào GitHub Settings
1. Vào: https://github.com/settings/tokens
2. Click "**Generate new token (classic)**"
3. Click "**Generate new token (classic)**"

### Bước 2: Configure Token
- **Note**: "Vercel Deployment Token"
- **Expiration**: "No expiration" hoặc 30 days
- **Scopes**: ✅ chọn các checkbox sau:
  - ✅ repo (Full control of private repositories)
  - ✅ workflow (Update GitHub Action workflows)
  - ✅ admin:repo_hook (Full control of repository hooks)
  - ✅ write:packages (Upload packages)

### Bước 3: Generate & Copy
1. Click "**Generate token**"
2. **Copy token** (dạng: ghp_xxxxxxxxxxxxxxxxxxxx)

⚠️ **IMPORTANT**: Copy token ngay lập tức, sẽ không hiển thị lại!

### Bước 4: Vercel Setup
1. Vào Vercel: https://vercel.com/dashboard
2. Click "**New Project**"  
3. Import GitHub repo: **Mrkent1/etax**
4. Vào "**Environment Variables**"
5. Add:
   - **Name**: `GITHUB_TOKEN`
   - **Value**: [paste token của bạn]
6. Click "**Deploy**" ✅

## ✅ Kết quả
- URL: `https://etax-xxx.vercel.app`
- HTTPS: Automatic
- PWA: Optimized
- Auto-deploy: Mỗi push code

**Tổng thời gian: 5-7 phút**