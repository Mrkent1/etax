# 📁 PROJECT STRUCTURE GUIDELINES
**For AI Agents - Rules & Organization**

---

## 🎯 PURPOSE

This document defines the **STRICT ORGANIZATION RULES** for eTax Mobile PWA project. All AI agents MUST follow these guidelines when working with this project.

---

## 📋 CORE PRINCIPLES

### 1. **MAIN PROJECT LOCATION**
```
/workspace/etax-mobile-pwa/
```
**THIS IS THE ONLY ACTIVE PROJECT DIRECTORY** - All development work must be done here.

### 2. **ARCHIVES RULE**
```
/workspace/archives/
```
- **ONLY** historical/backup files go here
- **NEVER** modify files in archives
- **NEVER** work from archives directory

### 3. **TEMP RULE**
```
/workspace/temp/
```
- **ONLY** temporary/extraction files
- **CLEAN UP** after use
- **NEVER** commit temp files to source

---

## 🗂️ DIRECTORY SPECIFICATIONS

### 🔧 `/etax-mobile-pwa/source/`
**PRODUCTION SOURCE CODE**
- ✅ **ACTIVE DEVELOPMENT** happens here
- ✅ **ALL HTML/CSS/JS** files
- ✅ **PWA components** (manifest, service worker)
- ✅ **Assets** (images, icons, fonts)
- ❌ **NO** documentation files
- ❌ **NO** test files
- ❌ **NO** config files

**Typical files:**
```
source/
├── index.html              # PWA entry point
├── login.html              # Authentication
├── home.html               # Main dashboard
├── manifest.json           # PWA manifest
├── service-worker.js       # Offline functionality
├── css/                    # Stylesheets
├── js/                     # JavaScript modules
├── pages/                  # Sub-pages
└── assets/                 # Images & icons
```

### 📋 `/etax-mobile-pwa/docs/`
**DOCUMENTATION**
- ✅ **Markdown files** (.md)
- ✅ **Reports** (analysis, summaries)
- ✅ **API documentation**
- ✅ **User guides**
- ❌ **NO** source code
- ❌ **NO** test files

**Subdirectories allowed:**
```
docs/
├── reports/                # Test reports & analysis
├── api/                    # API documentation
├── user-guides/            # User manuals
└── development/            # Dev documentation
```

### 🧪 `/etax-mobile-pwa/tests/`
**TESTING FRAMEWORK**
- ✅ **Python test scripts**
- ✅ **Testing utilities**
- ✅ **Quality assurance tools**
- ❌ **NO** source code
- ❌ **NO** documentation

**Typical files:**
```
tests/
├── comprehensive_e2e_test.py    # E2E testing
├── pwa_test_tool.py            # PWA testing
├── production_optimizer.py     # Optimization
└── test_data/                  # Test datasets
```

### ⚙️ `/etax-mobile-pwa/configs/`
**CONFIGURATION FILES**
- ✅ **Server configs** (.htaccess, nginx.conf)
- ✅ **Build configs** (webpack, package.json)
- ✅ **Environment configs**
- ✅ **Security headers**
- ❌ **NO** source code
- ❌ **NO** documentation

**Typical files:**
```
configs/
├── .htaccess                # Apache security
├── nginx-config.conf        # Nginx security
├── production.env           # Environment vars
└── ssl/                     # SSL certificates
```

### 📊 `/etax-mobile-pwa/reports/`
**GENERATED REPORTS**
- ✅ **Auto-generated reports**
- ✅ **Performance metrics**
- ✅ **Test results**
- ❌ **NO** manual documentation
- ❌ **NO** source code

---

## 🚫 STRICT FORBIDDEN PRACTICES

### ❌ **NEVER DO THIS:**

1. **Create files in wrong directories:**
   ```bash
   # WRONG ❌
   /workspace/docs/test.py
   /workspace/source/README.md
   /workspace/tests/index.html
   
   # RIGHT ✅
   /workspace/etax-mobile-pwa/tests/test.py
   /workspace/etax-mobile-pwa/docs/README.md
   ```

2. **Mix file types:**
   ```bash
   # WRONG ❌
   source/
   ├── report.md           # Documentation in source
   ├── test.py            # Test file in source
   └── config.json        # Config in source
   
   # RIGHT ✅
   source/
   ├── index.html         # Only HTML/CSS/JS
   └── manifest.json      # Only PWA files
   ```

3. **Work from archives:**
   ```bash
   # WRONG ❌
   /workspace/archives/error_viewport/index.html  # Modify archive
   
   # RIGHT ✅
   # Reference only, work from /etax-mobile-pwa/source/
   ```

4. **Leave temp files:**
   ```bash
   # WRONG ❌
   /workspace/temp/           # Messy temp directory
   
   # RIGHT ✅
   # Clean up temp files after use
   ```

---

## ✅ MANDATORY ORGANIZATION RULES

### **FOR AGENTS:**

1. **ALWAYS work from:** `/workspace/etax-mobile-pwa/source/`
2. **ALWAYS organize files** by their type (docs/docs/, tests/tests/, configs/configs/)
3. **NEVER modify archives/** directory
4. **CLEAN UP temp/** after operations
5. **KEEP documentation** in docs/ subdirectories
6. **SEPARATE concerns:** Source ≠ Tests ≠ Docs ≠ Configs

### **FILE PLACEMENT MATRIX:**

| File Type | Directory | Example |
|-----------|-----------|---------|
| HTML/CSS/JS | `/source/` | `source/index.html` |
| Python Scripts | `/tests/` | `tests/test.py` |
| Markdown Docs | `/docs/` | `docs/readme.md` |
| Config Files | `/configs/` | `configs/.htaccess` |
| Test Data | `/tests/` | `tests/data.json` |
| Reports | `/docs/reports/` | `docs/reports/summary.md` |
| Images/Assets | `/source/assets/` | `source/assets/logo.webp` |
| PWA Files | `/source/` | `source/manifest.json` |

---

## 🔄 WORKFLOW FOR AGENTS

### **Task Execution Pattern:**

1. **Understand task scope**
2. **Identify correct directory** using matrix above
3. **Organize files** according to rules
4. **Keep archives untouched**
5. **Clean up temp files**
6. **Update relevant documentation**

### **Example Workflow - Add New Feature:**

```bash
# 1. Work in source directory
cd /workspace/etax-mobile-pwa/source/

# 2. Create new HTML file
new-feature.html

# 3. Add related CSS to css/
css/new-feature.css

# 4. Add JS to js/
js/new-feature.js

# 5. If creating tests
cd /workspace/etax-mobile-pwa/tests/
test_new_feature.py

# 6. If creating docs
cd /workspace/etax-mobile-pwa/docs/
guides/new-feature-guide.md

# 7. Clean up
rm -rf /workspace/temp/*
```

---

## 🎯 QUALITY CHECKLIST

### **Before completing ANY task:**

- [ ] ✅ Files placed in correct directories
- [ ] ✅ No files in wrong locations
- [ ] ✅ Archives directory untouched
- [ ] ✅ Temp directory cleaned
- [ ] ✅ Documentation updated if needed
- [ ] ✅ Source code organized properly

### **Common Mistakes to Avoid:**

1. **Mixed directories** - Don't put docs in source/
2. **Ignored archives** - Never modify /archives/
3. **Messy temp** - Always clean up temp files
4. **Wrong file types** - Use matrix above
5. **No organization** - Follow directory structure strictly

---

## 📞 ENFORCEMENT

**VIOLATION = TASK FAILURE**

If you violate these rules:
- ❌ **Poor organization = Poor quality**
- ❌ **Mixed files = Maintenance nightmare**
- ❌ **Dirty workspace = Unprofessional**

**SUCCESS = STRICT ADHERENCE**

If you follow these rules:
- ✅ **Clean codebase = Easy maintenance**
- ✅ **Organized structure = Professional delivery**
- ✅ **Proper separation = Scalable architecture**

---

**REMEMBER:** Good organization = Good development practices = Happy stakeholders

**Last Updated:** 2025-11-26 19:45:42