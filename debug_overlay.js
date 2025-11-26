/**
 * Debug overlay for pixel-perfect comparison of mobile PWA header
 * This script adds visual guides and measurements to help with debugging
 */

(function() {
    'use strict';
    
    // Create debug overlay container
    function createDebugOverlay() {
        // Check if overlay already exists
        if (document.getElementById('debug-overlay')) {
            return;
        }
        
        const overlay = document.createElement('div');
        overlay.id = 'debug-overlay';
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.pointerEvents = 'none';
        overlay.style.zIndex = '9999';
        overlay.style.overflow = 'hidden';
        
        // Grid lines
        const grid = document.createElement('div');
        grid.style.position = 'absolute';
        grid.style.top = '0';
        grid.style.left = '0';
        grid.style.width = '100%';
        grid.style.height = '100%';
        grid.style.backgroundImage = `
            linear-gradient(to right, rgba(255, 0, 0, 0.1) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 0, 0, 0.1) 1px, transparent 1px)
        `;
        grid.style.backgroundSize = '20px 20px';
        grid.style.pointerEvents = 'none';
        
        // Header highlight
        const headerHighlight = document.createElement('div');
        headerHighlight.id = 'header-highlight';
        headerHighlight.style.position = 'absolute';
        headerHighlight.style.border = '2px solid #00ff00';
        headerHighlight.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
        headerHighlight.style.pointerEvents = 'none';
        headerHighlight.style.display = 'none';
        
        // Measurements display
        const measurements = document.createElement('div');
        measurements.id = 'measurements-display';
        measurements.style.position = 'fixed';
        measurements.style.top = '10px';
        measurements.style.right = '10px';
        measurements.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        measurements.style.color = 'white';
        measurements.style.padding = '10px';
        measurements.style.borderRadius = '5px';
        measurements.style.fontFamily = 'monospace';
        measurements.style.fontSize = '12px';
        measurements.style.zIndex = '10000';
        measurements.style.pointerEvents = 'none';
        measurements.innerHTML = '<strong>Header Debug Info:</strong><br>';
        
        // Add elements to overlay
        overlay.appendChild(grid);
        overlay.appendChild(headerHighlight);
        overlay.appendChild(measurements);
        
        document.body.appendChild(overlay);
        
        // Update header highlight position
        function updateHeaderHighlight() {
            const logoElement = document.querySelector('.logo');
            if (logoElement) {
                const rect = logoElement.getBoundingClientRect();
                headerHighlight.style.display = 'block';
                headerHighlight.style.left = (rect.left + window.scrollX) + 'px';
                headerHighlight.style.top = (rect.top + window.scrollY) + 'px';
                headerHighlight.style.width = rect.width + 'px';
                headerHighlight.style.height = rect.height + 'px';
                
                // Update measurements display
                const measurementsDisplay = document.getElementById('measurements-display');
                if (measurementsDisplay) {
                    measurementsDisplay.innerHTML = `
                        <strong>Header Debug Info:</strong><br>
                        Position: ${Math.round(rect.left)}, ${Math.round(rect.top)}<br>
                        Size: ${Math.round(rect.width)} × ${Math.round(rect.height)}<br>
                        Font-size: ${window.getComputedStyle(logoElement.querySelector('h1')).fontSize}<br>
                        Color: ${window.getComputedStyle(logoElement.querySelector('h1')).color}<br>
                        Text-shadow: ${window.getComputedStyle(logoElement.querySelector('h1')).textShadow}
                    `;
                }
            }
        }
        
        // Initial update
        updateHeaderHighlight();
        
        // Update on resize
        window.addEventListener('resize', updateHeaderHighlight);
        
        // Periodic update for dynamic content
        setInterval(updateHeaderHighlight, 500);
    }
    
    // Create toggle button
    function createToggleButton() {
        if (document.getElementById('debug-toggle')) {
            return;
        }
        
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'debug-toggle';
        toggleBtn.textContent = 'Debug';
        toggleBtn.style.position = 'fixed';
        toggleBtn.style.bottom = '20px';
        toggleBtn.style.right = '20px';
        toggleBtn.style.zIndex = '10001';
        toggleBtn.style.padding = '10px 15px';
        toggleBtn.style.backgroundColor = '#C60000';
        toggleBtn.style.color = 'white';
        toggleBtn.style.border = 'none';
        toggleBtn.style.borderRadius = '5px';
        toggleBtn.style.cursor = 'pointer';
        toggleBtn.style.fontSize = '14px';
        
        toggleBtn.onclick = function() {
            const overlay = document.getElementById('debug-overlay');
            if (overlay) {
                overlay.style.display = overlay.style.display === 'none' ? 'block' : 'none';
                this.textContent = overlay.style.display === 'none' ? 'Debug' : 'Hide';
            } else {
                createDebugOverlay();
                this.textContent = 'Hide';
            }
        };
        
        document.body.appendChild(toggleBtn);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            createToggleButton();
        });
    } else {
        createToggleButton();
    }
    
    // Add CSS for better visual debugging
    const debugCSS = document.createElement('style');
    debugCSS.textContent = `
        .debug-info {
            position: absolute;
            background: rgba(255, 255, 0, 0.8);
            color: black;
            font-size: 10px;
            padding: 2px 4px;
            border-radius: 2px;
            z-index: 10000;
            pointer-events: none;
        }
    `;
    document.head.appendChild(debugCSS);
    
})();