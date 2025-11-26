# 🎯 DEVELOPER CONTEXT GUIDE
**For AI Agents - Project Understanding & Working Rules**

---

## 📋 PROJECT OVERVIEW

### **🎯 What This Is:**
- **Project Name:** eTax Mobile PWA
- **Type:** Progressive Web Application (PWA)
- **Purpose:** Vietnamese tax service mobile app
- **Status:** ✅ PRODUCTION READY (96.7/100 PWA Score)
- **Owner:** anh Nghĩa (non-technical stakeholder)

### **📱 What It Does:**
- **Mobile-first** web application for Vietnamese tax services
- **Authentication system** for MST (tax ID) based login
- **22 HTML pages** covering various tax functions:
  - Login/Authentication
  - Home dashboard  
  - Tax registration
  - Electronic invoices
  - Tax declarations
  - Payment processing
  - Account management
  - Support functions

### **🔧 Technical Stack:**
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **PWA Features:** Service Worker, Web App Manifest
- **Authentication:** Firebase integration
- **Offline:** Service worker caching
- **Mobile:** Responsive design, iPhone optimized
- **Vietnamese:** Full localization

---

## 🏗️ WORKSPACE ORGANIZATION

### **🎯 ACTIVE PROJECT LOCATION:**
```
/workspace/etax-mobile-pwa/
```
**THIS IS THE ONLY DIRECTORY FOR PROJECT WORK**

#### **📁 Subdirectories:**
- **`source/`** - Production code (HTML/CSS/JS)
- **`docs/`** - Documentation & reports
- **`tests/`** - Testing frameworks & tools
- **`configs/`** - Server configurations
- **`reports/`** - Generated reports (future)

### **🚫 FORBIDDEN LOCATIONS:**
```
/workspace/system/           # Browser tools (ignore)
/workspace/user_input_files/ # Original uploads (reference only)
/workspace/archives/         # Historical backups (read-only)
```
**NEVER WORK IN THESE DIRECTORIES FOR PROJECT TASKS**

---

## 🤖 AI AGENT WORKING RULES

### **✅ ALWAYS DO THIS:**

1. **Work from correct directory:**
   ```bash
   cd /workspace/etax-mobile-pwa/source/  # For development
   cd /workspace/etax-mobile-pwa/docs/    # For documentation
   cd /workspace/etax-mobile-pwa/tests/   # For testing
   ```

2. **Follow file type rules:**
   - **HTML/CSS/JS** → `/source/`
   - **Documentation** → `/docs/`
   - **Python tests** → `/tests/`
   - **Config files** → `/configs/`

3. **Maintain clean organization:**
   - Separate source code from documentation
   - Keep test files in tests directory
   - Use archives for historical reference only

### **❌ NEVER DO THIS:**

1. **Work in wrong directories:**
   ```bash
   # WRONG ❌
   /workspace/system/browser_extension/
   /workspace/user_input_files/tax1.zip
   /workspace/archives/error_viewport/
   
   # RIGHT ✅
   /workspace/etax-mobile-pwa/source/
   ```

2. **Mix file types:**
   ```bash
   # WRONG ❌
   source/
   ├── README.md              # Documentation in source
   ├── test.py               # Test file in source
   
   # RIGHT ✅
   source/
   ├── index.html            # Only web files
   docs/
   ├── README.md             # Documentation here
   tests/
   ├── test.py              # Tests here
   ```

3. **Modify archives:**
   ```bash
   # NEVER MODIFY
   /workspace/archives/*      # Read-only historical files
   ```

---

## 📝 KEY PROJECT FILES

### **🎯 Primary Files (Production Ready):**
```
etax-mobile-pwa/source/
├── index.html              # PWA entry point (96.7/100 score)
├── login.html              # Authentication page
├── home.html               # Main dashboard
├── manifest.json           # PWA manifest (100/100)
├── service-worker.js       # Offline functionality
├── css/common.css          # Global styles
├── js/auth.js              # Authentication logic
└── pages/                  # 19 tax function pages
```

### **📋 Documentation Files:**
```
etax-mobile-pwa/docs/reports/
├── FINAL_SUMMARY_REPORT.md         # Complete project overview
├── comprehensive_analysis_report.md # Technical analysis
└── *.json                          # Test results data
```

### **🧪 Testing Tools:**
```
etax-mobile-pwa/tests/
├── comprehensive_e2e_test.py       # Full testing framework
├── pwa_test_tool.py               # PWA specific tests
└── production_optimizer.py        # Optimization scripts
```

---

## 🎯 PROJECT STATUS SUMMARY

### **✅ COMPLETED ACHIEVEMENTS:**
- **96.7/100 PWA Score** - Excellent for production
- **iPhone viewport issues** - Fixed completely
- **22 HTML files** - All tested and optimized
- **Authentication system** - Working and secure
- **Service worker** - Offline functionality active
- **Performance optimization** - Resource preloading added
- **Security configuration** - Headers and HTTPS ready
- **Testing framework** - Comprehensive E2E coverage
- **Documentation** - Complete and organized

### **📋 CURRENT WORKSPACE:**
- **Clean organization** - No duplicate files
- **Professional structure** - Industry standards
- **Agent guidelines** - Clear rules established
- **Production ready** - Ready for deployment

---

## 🚀 DEPLOYMENT REQUIREMENTS

### **✅ Ready for Production:**
1. **Deploy to HTTPS server** (required for PWA)
2. **Configure SSL certificate** 
3. **Upload source files** from `/etax-mobile-pwa/source/`
4. **Apply security headers** using `/configs/.htaccess`
5. **Test PWA installation**

### **📱 What Users Will Get:**
- **Mobile-first experience** optimized for iPhone
- **PWA installation** - "Add to Home Screen" prompt
- **Offline functionality** - Works without internet
- **Fast loading** - Performance optimized
- **Vietnamese interface** - Full localization
- **Secure authentication** - MST-based login

---

## 🔍 QUALITY ASSURANCE

### **🧪 Testing Coverage:**
- **22 HTML files** - All validated
- **PWA compliance** - 96.7/100 score
- **Mobile responsiveness** - iPhone optimized
- **Authentication flow** - Security verified
- **Service worker** - Offline tested

### **📊 Performance Metrics:**
- **Loading speed** - Optimized with preloading
- **Mobile performance** - iPhone rendering fixed
- **PWA features** - Install prompt working
- **Security** - Headers configured, HTTPS ready

---

## 📞 SUPPORT INFORMATION

### **👥 Project Team:**
- **Stakeholder:** anh Nghĩa (non-technical)
- **AI Agent:** MiniMax Agent
- **Project Type:** PWA Development & Optimization

### **📚 Documentation Hierarchy:**
1. **README.md** - Project overview & quick start
2. **PROJECT_STRUCTURE.md** - Agent development rules
3. **PRODUCTION_READY.md** - Current status & deployment
4. **DEVELOPER_CONTEXT.md** - This guide (agent context)
5. **WORKSPACE_CLEANUP_SUMMARY.md** - Organization history

---

## 🎯 SUCCESS CRITERIA

### **✅ Project Success Indicators:**
- **Production deployment** - App live on HTTPS
- **PWA installation** - Users can "Add to Home Screen"
- **Mobile optimization** - iPhone display perfect
- **Authentication working** - MST login functional
- **Offline capability** - Service worker active

### **✅ Agent Success Indicators:**
- **Clean workspace** - Files organized properly
- **No confusion** - Working in correct directories
- **Follow rules** - Using PROJECT_STRUCTURE.md guidelines
- **Professional delivery** - Industry standard quality

---

**🎯 Remember:** This is a **production-ready Vietnamese tax PWA** with 96.7/100 score. All critical issues fixed, tested, and optimized. Ready for immediate deployment to HTTPS server.

**Last Updated:** 2025-11-26 19:54:15