// Script to inject debugging tools into any eTax Mobile PWA page
// This script will be used to automatically add debugging functionality to all pages

function injectDebugTools() {
  // Check if debug tools are already injected
  if (document.getElementById('debug-overlay')) {
    console.log('Debug tools already injected');
    return;
  }

  // Load debug styles
  loadDebugStyles();
  
  // Load debug script
  loadDebugScript();
  
  // Initialize debug tools after a short delay to ensure DOM is ready
  setTimeout(() => {
    if (window.universalDebugOverlay) {
      console.log('Debug tools successfully injected and initialized');
    } else {
      console.log('Debug tools injected but not yet initialized');
    }
  }, 1000);
}

function loadDebugStyles() {
  // Create link element for debug styles
  const styleLink = document.createElement('link');
  styleLink.id = 'debug-styles';
  styleLink.rel = 'stylesheet';
  styleLink.type = 'text/css';
  styleLink.href = '/debug_styles.css';
  
  // Add to head
  document.head.appendChild(styleLink);
}

function loadDebugScript() {
  // Create script element for debug functionality
  const script = document.createElement('script');
  script.id = 'debug-script';
  script.src = '/universal_debug_overlay.js';
  script.async = false; // Ensure it loads in order
  
  // Add to head
  document.head.appendChild(script);
}

// Run the injection when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectDebugTools);
} else {
  // DOM is already loaded
  injectDebugTools();
}

// Additionally, provide a function to manually trigger injection
window.injectDebugTools = injectDebugTools;