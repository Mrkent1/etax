# Comprehensive Debugging Plan for eTax Mobile PWA

## Project Overview
- Project: eTax Mobile PWA
- Total Pages: 26 functional pages + 3 main pages (index, login, home)
- Debugging Goal: Pixel-perfect implementation matching reference screenshots

## Pages to Debug

### Main Pages
1. **index.html** - Main landing page
2. **login.html** - Login page
3. **home.html** - Home dashboard

### Functional Pages
4. **bien-lai-dien-tu.html** - Electronic receipt page
5. **dang-ky-thue.html** - Tax registration page
6. **ho-so-dang-ky-thue.html** - Tax registration file page
7. **ho-so-quyet-toan-thue.html** - Tax settlement file page
8. **ho-tro-quyet-toan.html** - Tax settlement support page
9. **ho-tro.html** - Support page
10. **hoa-don-dien-tu.html** - Electronic invoice page
11. **khai-thue.html** - Tax declaration page
12. **nhom-chuc-nang-nop-thue.html** - Tax payment function group page
13. **nop-thue.html** - Tax payment page
14. **thay-doi-thong-tin-npt.html** - Change taxpayer information page
15. **thiet-lap-ca-nhan.html** - Personal settings page
16. **thong-bao.html** - Notifications page
17. **thong-tin-tai-khoan.html** - Account information page
18. **thong-tin-tong-quan.html** - General information page
19. **tien-ich.html** - Utilities page
20. **tra-cuu-chung-tu.html** - Document search page
21. **tra-cuu-nghia-vu-thue.html** - Tax obligation search page
22. **tra-cuu-thong-tin-nguoi-phu-thuoc.html** - Dependent information search page

## Debugging Process for Each Page

For each page, we will:
1. Compare viewport mobile screenshot with reference image
2. Extract UI text style attributes (font-size, family, color)
3. Measure pixel distances (margin, padding) for key UI elements
4. Check color accuracy (RGB values)
5. Verify full screen viewport and proper scaling
6. Generate pixel-to-pixel diff report
7. Create detailed JSON report with issues and fixes
8. Apply fixes and re-verify

## Priority Order for Debugging

### Phase 1: Critical Pages (High Priority)
1. index.html
2. login.html
3. home.html
4. thong-tin-tong-quan.html

### Phase 2: Core Functionality (Medium Priority)
5. dang-ky-thue.html
6. khai-thue.html
7. nop-thue.html
8. hoa-don-dien-tu.html

### Phase 3: Supporting Pages (Lower Priority)
9. ho-so-dang-ky-thue.html
10. ho-so-quyet-toan-thue.html
11. ho-tro-quyet-toan.html
12. ho-tro.html
13. bien-lai-dien-tu.html
14. nhom-chuc-nang-nop-thue.html
15. thay-doi-thong-tin-npt.html
16. thiet-lap-ca-nhan.html
17. thong-bao.html
18. thong-tin-tai-khoan.html
19. tien-ich.html
20. tra-cuu-chung-tu.html
21. tra-cuu-nghia-vu-thue.html
22. tra-cuu-thong-tin-nguoi-phu-thuoc.html

## Debugging Tools and Reports

### Tools to be Created
1. Universal debugging overlay script
2. Screenshot capture utility
3. Pixel comparison algorithm
4. CSS analysis tool
5. Color picker utility

### Reports to be Generated
1. Individual page analysis report (JSON format)
2. Overall project compliance report
3. Recommended fixes for each page
4. Before/after comparison screenshots

## Success Criteria
- 99.5% pixel accuracy compared to reference screenshots
- All fonts match exactly (family, size, weight, color)
- All spacing matches exactly (margins, padding, positioning)
- All colors match exactly (RGB values)
- Proper viewport scaling and full-screen display
- All interactive elements properly sized and positioned