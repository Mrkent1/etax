// Universal Debug Overlay for eTax Mobile PWA
// Provides pixel-perfect debugging tools for all pages

class UniversalDebugOverlay {
  constructor() {
    this.isActive = false;
    this.gridSize = 8; // Standard grid size for mobile UI
    this.overlay = null;
    this.gridOverlay = null;
    this.measurements = [];
    this.currentElement = null;
    this.colorPickerActive = false;
    this.colorPickerElement = null;
    
    this.init();
  }

  init() {
    // Create the main overlay container
    this.createOverlay();
    
    // Add event listeners
    this.addEventListeners();
  }

  createOverlay() {
    // Create main overlay container
    this.overlay = document.createElement('div');
    this.overlay.id = 'debug-overlay';
    this.overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 9999;
      font-family: monospace;
      font-size: 12px;
      color: #ff00ff;
      display: none;
    `;
    
    // Create grid overlay
    this.gridOverlay = document.createElement('div');
    this.gridOverlay.id = 'debug-grid';
    this.gridOverlay.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: 
        linear-gradient(to right, rgba(255, 0, 255, 0.2) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 0, 255, 0.2) 1px, transparent 1px);
      background-size: ${this.gridSize}px ${this.gridSize}px;
      pointer-events: none;
      display: none;
    `;
    
    // Create color picker element
    this.colorPickerElement = document.createElement('div');
    this.colorPickerElement.id = 'debug-color-picker';
    this.colorPickerElement.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      width: 200px;
      background: rgba(0, 0, 0, 0.8);
      border: 1px solid #ff00ff;
      border-radius: 4px;
      padding: 10px;
      color: white;
      font-family: monospace;
      font-size: 12px;
      z-index: 10000;
      display: none;
    `;
    
    // Create color picker content
    this.colorPickerElement.innerHTML = `
      <div style="margin-bottom: 10px; font-weight: bold;">Color Picker</div>
      <div id="current-color" style="width: 100%; height: 30px; margin-bottom: 5px; border: 1px solid white;"></div>
      <div id="color-info">Click anywhere to pick color</div>
      <div id="element-info" style="margin-top: 10px;"></div>
    `;
    
    // Create toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.id = 'debug-toggle';
    toggleBtn.textContent = 'DEBUG';
    toggleBtn.style.cssText = `
      position: fixed;
      top: 10px;
      left: 10px;
      background: #ff00ff;
      color: white;
      border: none;
      padding: 8px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
      z-index: 10001;
      pointer-events: auto;
    `;
    
    toggleBtn.addEventListener('click', () => this.toggleOverlay());
    
    // Create grid toggle button
    const gridToggleBtn = document.createElement('button');
    gridToggleBtn.id = 'debug-grid-toggle';
    gridToggleBtn.textContent = 'GRID';
    gridToggleBtn.style.cssText = `
      position: fixed;
      top: 10px;
      left: 80px;
      background: #00ffff;
      color: black;
      border: none;
      padding: 8px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
      z-index: 10001;
      pointer-events: auto;
    `;
    
    gridToggleBtn.addEventListener('click', () => this.toggleGrid());
    
    // Create color picker toggle button
    const colorToggleBtn = document.createElement('button');
    colorToggleBtn.id = 'debug-color-toggle';
    colorToggleBtn.textContent = 'COLOR';
    colorToggleBtn.style.cssText = `
      position: fixed;
      top: 10px;
      left: 150px;
      background: #ffff00;
      color: black;
      border: none;
      padding: 8px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
      z-index: 10001;
      pointer-events: auto;
    `;
    
    colorToggleBtn.addEventListener('click', () => this.toggleColorPicker());
    
    // Add elements to document
    document.body.appendChild(this.overlay);
    document.body.appendChild(this.gridOverlay);
    document.body.appendChild(this.colorPickerElement);
    document.body.appendChild(toggleBtn);
    document.body.appendChild(gridToggleBtn);
    document.body.appendChild(colorToggleBtn);
  }

  addEventListeners() {
    // Mouse move for element highlighting and measurements
    document.addEventListener('mousemove', (e) => {
      if (this.isActive && this.currentElement !== e.target) {
        this.currentElement = e.target;
        this.highlightElement(e.target);
      }
    });
    
    // Click for color picking
    document.addEventListener('click', (e) => {
      if (this.colorPickerActive) {
        e.preventDefault();
        e.stopPropagation();
        this.pickColor(e.clientX, e.clientY);
      }
    }, true); // Use capture phase to intercept before other handlers
    
    // Touch events for mobile
    document.addEventListener('touchstart', (e) => {
      if (this.colorPickerActive) {
        e.preventDefault();
        e.stopPropagation();
        this.pickColor(e.touches[0].clientX, e.touches[0].clientY);
      }
    }, true);
  }

  toggleOverlay() {
    this.isActive = !this.isActive;
    this.overlay.style.display = this.isActive ? 'block' : 'none';
    
    if (!this.isActive) {
      this.clearHighlight();
      this.gridOverlay.style.display = 'none';
      this.colorPickerElement.style.display = 'none';
      this.colorPickerActive = false;
    }
  }

  toggleGrid() {
    if (!this.isActive) {
      alert('Please activate debug mode first');
      return;
    }
    
    const isCurrentlyVisible = this.gridOverlay.style.display === 'block';
    this.gridOverlay.style.display = isCurrentlyVisible ? 'none' : 'block';
  }

  toggleColorPicker() {
    if (!this.isActive) {
      alert('Please activate debug mode first');
      return;
    }
    
    this.colorPickerActive = !this.colorPickerActive;
    this.colorPickerElement.style.display = this.colorPickerActive ? 'block' : 'none';
    
    if (this.colorPickerActive) {
      document.body.style.cursor = 'crosshair';
    } else {
      document.body.style.cursor = 'default';
    }
  }

  highlightElement(element) {
    // Remove previous highlights
    this.clearHighlight();
    
    // Get element position and dimensions
    const rect = element.getBoundingClientRect();
    
    // Create highlight overlay
    const highlight = document.createElement('div');
    highlight.className = 'debug-highlight';
    highlight.style.cssText = `
      position: fixed;
      top: ${rect.top}px;
      left: ${rect.left}px;
      width: ${rect.width}px;
      height: ${rect.height}px;
      border: 2px solid #ff00ff;
      background: rgba(255, 0, 255, 0.1);
      pointer-events: none;
      z-index: 9998;
      box-sizing: border-box;
    `;
    
    // Add measurements
    const measurements = document.createElement('div');
    measurements.className = 'debug-measurements';
    measurements.style.cssText = `
      position: fixed;
      top: ${rect.top - 20}px;
      left: ${rect.left}px;
      background: rgba(255, 0, 255, 0.8);
      color: white;
      padding: 2px 4px;
      font-size: 10px;
      z-index: 9999;
      pointer-events: none;
    `;
    
    // Get computed styles
    const computedStyle = window.getComputedStyle(element);
    const fontSize = computedStyle.fontSize;
    const fontFamily = computedStyle.fontFamily;
    const color = computedStyle.color;
    const backgroundColor = computedStyle.backgroundColor;
    const margin = `${computedStyle.marginTop} ${computedStyle.marginRight} ${computedStyle.marginBottom} ${computedStyle.marginLeft}`;
    const padding = `${computedStyle.paddingTop} ${computedStyle.paddingRight} ${computedStyle.paddingBottom} ${computedStyle.paddingLeft}`;
    
    measurements.innerHTML = `
      ${Math.round(rect.width)}×${Math.round(rect.height)}<br>
      <small>Font: ${Math.round(parseFloat(fontSize))}px ${fontFamily.split(',')[0]}</small><br>
      <small>Color: ${color}</small>
    `;
    
    // Add to overlay
    this.overlay.appendChild(highlight);
    this.overlay.appendChild(measurements);
    
    // Show element info in color picker panel
    if (this.colorPickerActive) {
      const elementInfo = document.getElementById('element-info');
      elementInfo.innerHTML = `
        <div><strong>Element Info:</strong></div>
        <div>Tag: ${element.tagName.toLowerCase()}</div>
        <div>Class: ${element.className || 'none'}</div>
        <div>ID: ${element.id || 'none'}</div>
        <div>Dimensions: ${Math.round(rect.width)}×${Math.round(rect.height)}</div>
        <div>Font: ${Math.round(parseFloat(fontSize))}px ${fontFamily.split(',')[0]}</div>
        <div>Color: ${color}</div>
        <div>BG: ${backgroundColor}</div>
        <div>Margin: ${margin}</div>
        <div>Padding: ${padding}</div>
      `;
    }
  }

  clearHighlight() {
    // Remove all highlight elements
    const highlights = this.overlay.querySelectorAll('.debug-highlight, .debug-measurements');
    highlights.forEach(el => el.remove());
  }

  pickColor(x, y) {
    // Get pixel color at coordinates
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 1;
    const ctx = canvas.getContext('2d');
    
    // Draw a 1x1 pixel at the specified location
    // Note: This is a simplified approach - in a real implementation, 
    // we would need to handle the case where we can't directly read pixel data
    // due to cross-origin restrictions
    
    // For now, we'll get the element at that position and show its background color
    const element = document.elementFromPoint(x, y);
    if (element) {
      const style = window.getComputedStyle(element);
      const bgColor = style.backgroundColor;
      const textColor = style.color;
      
      // Update color picker display
      const currentColor = document.getElementById('current-color');
      const colorInfo = document.getElementById('color-info');
      
      if (currentColor && colorInfo) {
        currentColor.style.backgroundColor = bgColor;
        colorInfo.textContent = `BG: ${bgColor}, Text: ${textColor}`;
      }
      
      // Also highlight the element
      this.highlightElement(element);
    }
  }

  // Method to capture viewport screenshot
  captureScreenshot() {
    return new Promise((resolve) => {
      // This would use HTML2Canvas or similar library in a real implementation
      // For now, we'll just return a placeholder
      console.log('Screenshot capture would happen here');
      resolve('screenshot_data');
    });
  }

  // Method to measure distances between elements
  measureDistance(element1, element2) {
    const rect1 = element1.getBoundingClientRect();
    const rect2 = element2.getBoundingClientRect();
    
    // Calculate distances
    const horizontalDistance = Math.abs(rect1.right - rect2.left);
    const verticalDistance = Math.abs(rect1.bottom - rect2.top);
    
    return {
      horizontal: Math.round(horizontalDistance),
      vertical: Math.round(verticalDistance)
    };
  }

  // Method to generate pixel diff report
  generatePixelDiffReport() {
    // This would compare current page with reference screenshot
    // For now, we'll return a placeholder report
    return {
      overallAccuracy: "Calculating...",
      fontIssues: [],
      colorIssues: [],
      spacingIssues: [],
      recommendations: []
    };
  }
}

// Initialize the debug overlay when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.universalDebugOverlay = new UniversalDebugOverlay();
});

// Also initialize if DOM is already loaded
if (document.readyState === 'loading') {
  // Loading hasn't finished yet
} else {
  // DOM is already loaded
  window.universalDebugOverlay = new UniversalDebugOverlay();
}