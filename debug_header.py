#!/usr/bin/env python3
"""
Debug script for pixel-perfect comparison of mobile PWA header
"""

import os
import sys
import time
import json
from PIL import Image, ImageChops, ImageDraw, ImageFont
import requests
from playwright.sync_api import sync_playwright


def capture_screenshots_and_analyze():
    """Main function to analyze the header of the mobile PWA"""
    
    # Setup
    base_url = "http://localhost:8000"
    reference_img_path = "/workspace/user_input_files/image.png"
    current_screenshot_path = "/workspace/current_screenshot.png"
    header_screenshot_path = "/workspace/header_screenshot.png"
    diff_output_path = "/workspace/diff_output.png"
    
    print("Starting header analysis...")
    
    # Check if reference image exists
    if not os.path.exists(reference_img_path):
        print(f"Reference image not found: {reference_img_path}")
        return
    
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
            
            # Capture full page screenshot
            print("Capturing current page screenshot...")
            page.screenshot(path=current_screenshot_path, full_page=True)
            
            # Capture header section screenshot
            print("Capturing header screenshot...")
            logo_element = page.locator(".logo")
            if logo_element.count() > 0:
                logo_element.screenshot(path=header_screenshot_path)
                
                # Extract header styles
                print("Extracting header styles...")
                header_styles = {
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
                
                # Extract logo styles
                logo_img = page.locator(".logo img")
                logo_styles = {
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
                }
            else:
                print("Logo element not found, using full page screenshot as reference")
                header_styles = {}
                logo_styles = {}
                title_styles = {}
            
            # Compare with reference image
            print("Comparing with reference image...")
            similarity, diff_img = compare_images(reference_img_path, current_screenshot_path, diff_output_path)
            
            # Generate report
            report = {
                "reference_image": reference_img_path,
                "current_screenshot": current_screenshot_path,
                "header_screenshot": header_screenshot_path,
                "diff_output": diff_output_path,
                "similarity_percentage": round(similarity, 2),
                "header_styles": header_styles,
                "logo_styles": logo_styles,
                "title_styles": title_styles,
                "viewport_info": {
                    "width": page.viewport_size["width"],
                    "height": page.viewport_size["height"],
                    "device_scale_factor": context.devices["iPhone X"].get("device_scale_factor", 1) if "iPhone X" in [d for d in dir(p) if not d.startswith('_')] else 2
                },
                "issues": [],
                "fixes": []
            }
            
            # Analyze potential issues
            if similarity < 99.5:
                report["issues"].append({
                    "type": "overall_similarity_low",
                    "description": f"Overall similarity is {similarity:.2f}%, below the required 99.5%",
                    "severity": "high"
                })
            
            # Check for specific style issues
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
            report_path = "/workspace/debug_report.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"Analysis complete. Report saved to {report_path}")
            print(f"Similarity: {similarity:.2f}%")
            print(f"Current screenshot: {current_screenshot_path}")
            print(f"Difference visualization: {diff_output_path}")
            
            return report
            
        finally:
            browser.close()


def compare_images(img1_path, img2_path, output_diff_path):
    """Compare two images pixel by pixel and highlight differences"""
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')
    
    # Ensure both images are the same size
    if img1.size != img2.size:
        # Resize the smaller image to match the larger one
        max_size = (max(img1.size[0], img2.size[0]), max(img1.size[1], img2.size[1]))
        img1 = img1.resize(max_size)
        img2 = img2.resize(max_size)
    
    # Calculate difference
    diff = ImageChops.difference(img1, img2)
    
    # Create a mask where differences exist (non-black pixels)
    diff_mask = diff.convert('L').point(lambda x: 255 if x > 30 else 0)
    
    # Create red overlay for differences
    red_overlay = Image.new('RGB', img1.size, (255, 0, 0))
    diff_img = Image.new('RGBA', img1.size, (0, 0, 0, 0))
    diff_img.paste(red_overlay, (0, 0), diff_mask)
    
    # Blend the original image with the red overlay
    result = Image.blend(img1.convert('RGBA'), diff_img, 0.3)
    
    # Save the result
    result.save(output_diff_path)
    
    # Calculate similarity percentage
    total_pixels = img1.size[0] * img1.size[1]
    different_pixels = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0))
    similarity = (total_pixels - different_pixels) / total_pixels * 100
    
    return similarity, diff_img


if __name__ == "__main__":
    capture_screenshots_and_analyze()