#!/usr/bin/env python3
"""
Simple debug script for mobile PWA header analysis
"""

import json
import time
from playwright.sync_api import sync_playwright


def simple_header_analysis():
    """Simple function to analyze the header of the mobile PWA"""
    
    base_url = "http://localhost:8000"
    
    print("Starting simple header analysis...")
    
    with sync_playwright() as p:
        # Launch browser with mobile emulation
        browser = p.chromium.launch(headless=True)
        
        # Define iPhone X mobile device settings
        iphone_x = p.devices["iPhone X"]
        context = browser.new_context(**iphone_x)
        
        page = context.new_page()
        
        try:
            # Navigate to the login page
            print("Navigating to login page...")
            page.goto(f"{base_url}/login.html")
            
            # Wait for page to load
            page.wait_for_load_state("networkidle")
            time.sleep(1)  # Additional wait for full render
            
            # Get viewport information
            viewport_info = {
                "width": page.viewport_size["width"],
                "height": page.viewport_size["height"],
                "device_scale_factor": iphone_x.get("device_scale_factor", 2)
            }
            
            # Extract header styles (logo section)
            logo_element = page.locator(".logo")
            if logo_element.count() > 0:
                print("Found logo element, extracting styles...")
                
                # Get bounding box for the logo
                logo_bbox = logo_element.bounding_box()
                
                # Extract styles for logo container
                logo_styles = {
                    'font-size': logo_element.evaluate("el => window.getComputedStyle(el).fontSize"),
                    'font-family': logo_element.evaluate("el => window.getComputedStyle(el).fontFamily"),
                    'color': logo_element.evaluate("el => window.getComputedStyle(el).color"),
                    'background-color': logo_element.evaluate("el => window.getComputedStyle(el).backgroundColor"),
                    'margin': logo_element.evaluate("el => window.getComputedStyle(el).margin"),
                    'padding': logo_element.evaluate("el => window.getComputedStyle(el).padding"),
                    'width': logo_element.evaluate("el => window.getComputedStyle(el).width"),
                    'height': logo_element.evaluate("el => window.getComputedStyle(el).height"),
                    'position': logo_element.evaluate("el => window.getComputedStyle(el).position"),
                    'top': logo_element.evaluate("el => window.getComputedStyle(el).top"),
                    'left': logo_element.evaluate("el => window.getComputedStyle(el).left"),
                }
                
                # Extract logo image styles
                logo_img = page.locator(".logo img")
                logo_img_styles = {
                    'width': logo_img.evaluate("el => window.getComputedStyle(el).width"),
                    'height': logo_img.evaluate("el => window.getComputedStyle(el).height"),
                    'margin': logo_img.evaluate("el => window.getComputedStyle(el).margin"),
                    'padding': logo_img.evaluate("el => window.getComputedStyle(el).padding"),
                }
                
                # Extract title styles
                title_element = page.locator(".logo h1")
                title_styles = {
                    'font-size': title_element.evaluate("el => window.getComputedStyle(el).fontSize"),
                    'font-family': title_element.evaluate("el => window.getComputedStyle(el).fontFamily"),
                    'color': title_element.evaluate("el => window.getComputedStyle(el).color"),
                    'margin': title_element.evaluate("el => window.getComputedStyle(el).margin"),
                    'padding': title_element.evaluate("el => window.getComputedStyle(el).padding"),
                    'text-shadow': title_element.evaluate("el => window.getComputedStyle(el).textShadow"),
                    'font-weight': title_element.evaluate("el => window.getComputedStyle(el).fontWeight"),
                }
                
                # Get element positions and dimensions
                title_bbox = title_element.bounding_box()
                
                # Generate report
                report = {
                    "viewport_info": viewport_info,
                    "logo_element": {
                        "styles": logo_styles,
                        "bbox": logo_bbox
                    },
                    "logo_img": {
                        "styles": logo_img_styles
                    },
                    "title_element": {
                        "styles": title_styles,
                        "bbox": title_bbox
                    },
                    "issues": [],
                    "fixes": []
                }
                
                # Analyze potential issues
                title_color = title_styles.get('color', '')
                if '255, 255, 255' not in title_color:  # Not white
                    report["issues"].append({
                        "type": "text_color",
                        "element": "header title",
                        "expected": "rgb(255, 255, 255) or similar white color",
                        "actual": title_color,
                        "severity": "high"
                    })
                    
                    report["fixes"].append({
                        "element": ".logo h1",
                        "property": "color",
                        "value": "#ffffff",
                        "reason": "Fix header text color to white to match reference"
                    })
                
                # Check font size of title
                title_font_size = title_styles.get('font-size', '')
                if title_font_size and '28px' not in title_font_size:
                    report["issues"].append({
                        "type": "font_size",
                        "element": "header title",
                        "expected": "28px",
                        "actual": title_font_size,
                        "severity": "medium"
                    })
                    
                    report["fixes"].append({
                        "element": ".logo h1",
                        "property": "font-size",
                        "value": "28px",
                        "reason": "Fix header title font size to match reference"
                    })
                
                # Check text shadow
                text_shadow = title_styles.get('text-shadow', '')
                if not text_shadow or '0 2px 6px' not in text_shadow:
                    report["issues"].append({
                        "type": "text_shadow",
                        "element": "header title",
                        "expected": "0 2px 6px rgba(0, 0, 0, 0.35) or similar",
                        "actual": text_shadow,
                        "severity": "medium"
                    })
                    
                    report["fixes"].append({
                        "element": ".logo h1",
                        "property": "text-shadow",
                        "value": "0 2px 6px rgba(0, 0, 0, 0.35)",
                        "reason": "Add text shadow to match reference"
                    })
                
                # Save report
                report_path = "/workspace/simple_debug_report.json"
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                
                print(f"Analysis complete. Report saved to {report_path}")
                print(f"Viewport: {viewport_info}")
                print(f"Title styles: {title_styles}")
                
                # Take a screenshot of the header area
                header_screenshot_path = "/workspace/header_simple.png"
                logo_element.screenshot(path=header_screenshot_path)
                print(f"Header screenshot saved to {header_screenshot_path}")
                
                return report
            else:
                print("Logo element not found")
                return None
                
        finally:
            browser.close()


if __name__ == "__main__":
    simple_header_analysis()