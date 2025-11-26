// Comprehensive Debug Report Generator for eTax Mobile PWA
// Analyzes all pages and generates detailed reports

class DebugReportGenerator {
  constructor() {
    this.reports = {};
    this.currentPage = '';
    this.debugConfig = null;
    this.loadConfig();
  }

  async loadConfig() {
    try {
      const response = await fetch('/debug_config.json');
      this.debugConfig = await response.json();
    } catch (error) {
      console.error('Failed to load debug config:', error);
      // Use default config
      this.debugConfig = {
        debugConfig: {
          gridSize: 8,
          tolerance: {
            pixelDiff: 2,
            colorDiff: 5,
            fontSizeDiff: 1,
            spacingDiff: 2
          },
          uiElements: {
            header: {
              selectors: ['.header', '.navbar', '.nav-bar', '.top-bar', '.toolbar', '.action-bar', '[id*="header"]', '[class*="header"]'],
              properties: ['height', 'backgroundColor', 'color', 'fontSize', 'fontFamily', 'fontWeight', 'padding', 'margin']
            },
            button: {
              selectors: ['.button', '.btn', '.action-button', 'button', '[type="button"]', '[type="submit"]'],
              properties: ['width', 'height', 'backgroundColor', 'color', 'fontSize', 'fontFamily', 'border', 'borderRadius', 'padding', 'margin']
            },
            input: {
              selectors: ['.input', '.form-control', 'input', 'textarea', 'select'],
              properties: ['width', 'height', 'backgroundColor', 'color', 'fontSize', 'fontFamily', 'border', 'borderRadius', 'padding', 'margin']
            },
            card: {
              selectors: ['.card', '.panel', '.container', '.box', '.section'],
              properties: ['width', 'height', 'backgroundColor', 'color', 'border', 'borderRadius', 'padding', 'margin']
            }
          }
        }
      };
    }
  }

  async analyzePage(pageName) {
    this.currentPage = pageName;
    console.log(`Analyzing page: ${pageName}`);
    
    const report = {
      page: pageName,
      timestamp: new Date().toISOString(),
      viewport: this.getViewportInfo(),
      elements: {},
      issues: [],
      recommendations: []
    };

    // Analyze different UI elements
    await this.analyzeUIElements(report);
    
    // Check for common issues
    this.checkCommonIssues(report);
    
    // Generate recommendations
    this.generateRecommendations(report);
    
    this.reports[pageName] = report;
    
    return report;
  }

  getViewportInfo() {
    return {
      width: window.innerWidth,
      height: window.innerHeight,
      deviceWidth: screen.width,
      deviceHeight: screen.height,
      pixelRatio: window.devicePixelRatio,
      isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
      orientation: window.innerWidth > window.innerHeight ? 'landscape' : 'portrait'
    };
  }

  async analyzeUIElements(report) {
    const uiElements = this.debugConfig.debugConfig.uiElements;
    
    for (const [elementType, config] of Object.entries(uiElements)) {
      const elements = this.findElements(config.selectors);
      if (elements.length > 0) {
        report.elements[elementType] = [];
        
        for (const element of elements) {
          const elementData = this.getElementData(element, config.properties);
          report.elements[elementType].push(elementData);
          
          // Check for issues with this element
          this.checkElementIssues(elementType, elementData, report);
        }
      }
    }
  }

  findElements(selectors) {
    const elements = [];
    for (const selector of selectors) {
      try {
        const found = document.querySelectorAll(selector);
        elements.push(...Array.from(found));
      } catch (e) {
        // Ignore invalid selectors
      }
    }
    // Remove duplicates
    return [...new Set(elements)];
  }

  getElementData(element, properties) {
    const rect = element.getBoundingClientRect();
    const computedStyle = window.getComputedStyle(element);
    
    const data = {
      tagName: element.tagName.toLowerCase(),
      className: element.className,
      id: element.id,
      position: {
        x: rect.left,
        y: rect.top,
        width: rect.width,
        height: rect.height
      },
      styles: {}
    };
    
    for (const prop of properties) {
      data.styles[prop] = computedStyle[prop];
    }
    
    return data;
  }

  checkElementIssues(elementType, elementData, report) {
    const tolerance = this.debugConfig.debugConfig.tolerance;
    
    // Check dimensions
    if (elementData.position.width < 10 && elementType === 'button') {
      report.issues.push({
        type: 'dimension',
        element: elementType,
        property: 'width',
        expected: '>= 10px',
        actual: elementData.position.width,
        severity: 'high',
        description: `Button is too narrow (${elementData.position.width}px)`
      });
    }
    
    if (elementData.position.height < 44 && elementType === 'button') {
      report.issues.push({
        type: 'dimension',
        element: elementType,
        property: 'height',
        expected: '>= 44px',
        actual: elementData.position.height,
        severity: 'high',
        description: `Button is too short (${elementData.position.height}px), may not be touch-friendly`
      });
    }
    
    // Check font size
    if (elementType === 'button' || elementType === 'header') {
      const fontSize = parseFloat(elementData.styles.fontSize);
      if (fontSize < 14) {
        report.issues.push({
          type: 'typography',
          element: elementType,
          property: 'fontSize',
          expected: '>= 14px',
          actual: fontSize,
          severity: 'medium',
          description: `Text is too small (${fontSize}px)`
        });
      }
    }
    
    // Check contrast for text elements
    if (elementType === 'header' || elementType === 'button') {
      const bgColor = this.hexToRgb(elementData.styles.backgroundColor);
      const textColor = this.hexToRgb(elementData.styles.color);
      
      if (bgColor && textColor) {
        const contrastRatio = this.calculateContrastRatio(bgColor, textColor);
        if (contrastRatio < 4.5) {
          report.issues.push({
            type: 'accessibility',
            element: elementType,
            property: 'colorContrast',
            expected: '>= 4.5:1',
            actual: `${contrastRatio.toFixed(2)}:1`,
            severity: 'high',
            description: `Low color contrast (${contrastRatio.toFixed(2)}:1), may be hard to read`
          });
        }
      }
    }
  }

  hexToRgb(hex) {
    // Handle shorthand hex
    if (hex.length === 4) {
      hex = hex[0] + hex[1] + hex[1] + hex[2] + hex[2] + hex[3] + hex[3];
    }
    
    // Handle rgb/rgba values
    if (hex.startsWith('rgb')) {
      const match = hex.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)/);
      if (match) {
        return {
          r: parseInt(match[1]),
          g: parseInt(match[2]),
          b: parseInt(match[3])
        };
      }
    }
    
    // Handle hex values
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  }

  calculateContrastRatio(color1, color2) {
    const luminance1 = this.relativeLuminance(color1);
    const luminance2 = this.relativeLuminance(color2);
    
    const brightest = Math.max(luminance1, luminance2);
    const darkest = Math.min(luminance1, luminance2);
    
    return (brightest + 0.05) / (darkest + 0.05);
  }

  relativeLuminance(color) {
    const r = color.r / 255;
    const g = color.g / 255;
    const b = color.b / 255;
    
    const sRGB = (c) => {
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    };
    
    return 0.2126 * sRGB(r) + 0.7152 * sRGB(g) + 0.0722 * sRGB(b);
  }

  checkCommonIssues(report) {
    // Check for viewport meta tag
    const viewportMeta = document.querySelector('meta[name="viewport"]');
    if (!viewportMeta) {
      report.issues.push({
        type: 'meta',
        element: 'viewport',
        property: 'tag',
        expected: 'exists with proper settings',
        actual: 'missing',
        severity: 'high',
        description: 'Viewport meta tag is missing, which affects mobile rendering'
      });
    } else {
      const content = viewportMeta.getAttribute('content');
      if (!content.includes('width=device-width') || !content.includes('initial-scale=1')) {
        report.issues.push({
          type: 'meta',
          element: 'viewport',
          property: 'content',
          expected: 'width=device-width, initial-scale=1',
          actual: content,
          severity: 'high',
          description: 'Viewport meta tag does not have proper settings for mobile'
        });
      }
    }
    
    // Check for proper font loading
    const fonts = document.styleSheets;
    let hasWebFont = false;
    for (const sheet of Array.from(fonts)) {
      try {
        if (sheet.cssRules) {
          for (const rule of Array.from(sheet.cssRules)) {
            if (rule.type === CSSRule.FONT_FACE_RULE) {
              hasWebFont = true;
              break;
            }
          }
        }
      } catch (e) {
        // Skip if we can't access the stylesheet due to CORS
      }
    }
    
    if (!hasWebFont) {
      report.issues.push({
        type: 'typography',
        element: 'font',
        property: 'loading',
        expected: 'web font loaded',
        actual: 'using system fonts',
        severity: 'medium',
        description: 'No web fonts detected, using system fonts instead'
      });
    }
  }

  generateRecommendations(report) {
    // Group issues by severity
    const highSeverity = report.issues.filter(issue => issue.severity === 'high');
    const mediumSeverity = report.issues.filter(issue => issue.severity === 'medium');
    const lowSeverity = report.issues.filter(issue => issue.severity === 'low');
    
    // Generate recommendations based on issues
    if (highSeverity.length > 0) {
      report.recommendations.push({
        priority: 'high',
        description: 'Address high severity issues first as they affect functionality or accessibility',
        issuesCount: highSeverity.length
      });
    }
    
    if (mediumSeverity.length > 0) {
      report.recommendations.push({
        priority: 'medium',
        description: 'Fix medium severity issues to improve user experience',
        issuesCount: mediumSeverity.length
      });
    }
    
    // Check if page needs responsive improvements
    if (report.viewport.width > 768) {
      report.recommendations.push({
        priority: 'medium',
        description: 'Test on actual mobile device as viewport width is large',
        issuesCount: 1
      });
    }
  }

  generateOverallReport() {
    const summary = {
      totalPages: Object.keys(this.reports).length,
      timestamp: new Date().toISOString(),
      totalPagesAnalyzed: Object.keys(this.reports).length,
      totalIssues: 0,
      issuesBySeverity: {
        high: 0,
        medium: 0,
        low: 0
      },
      pagesWithIssues: 0,
      averageIssuesPerPage: 0,
      compliancePercentage: 0
    };
    
    // Calculate statistics
    for (const [pageName, report] of Object.entries(this.reports)) {
      const issuesCount = report.issues.length;
      summary.totalIssues += issuesCount;
      
      for (const issue of report.issues) {
        summary.issuesBySeverity[issue.severity]++;
      }
      
      if (issuesCount > 0) {
        summary.pagesWithIssues++;
      }
    }
    
    if (summary.totalPages > 0) {
      summary.averageIssuesPerPage = summary.totalIssues / summary.totalPages;
      // Calculate compliance percentage (inverse of issue density)
      summary.compliancePercentage = Math.max(0, 100 - (summary.totalIssues * 2)); // Simplified calculation
    }
    
    return {
      summary: summary,
      detailedReports: this.reports
    };
  }

  exportReport(filename = 'debug_report.json') {
    const report = this.generateOverallReport();
    const dataStr = JSON.stringify(report, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = filename;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  }
}

// Initialize the debug report generator
window.debugReportGenerator = new DebugReportGenerator();

// Function to analyze the current page
window.analyzeCurrentPage = async function(pageName = window.location.pathname.split('/').pop() || 'index') {
  if (!window.debugReportGenerator) {
    window.debugReportGenerator = new DebugReportGenerator();
  }
  
  return await window.debugReportGenerator.analyzePage(pageName);
};

// Function to generate and download the full report
window.generateFullDebugReport = function() {
  if (window.debugReportGenerator) {
    window.debugReportGenerator.exportReport();
  }
};