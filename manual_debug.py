#!/usr/bin/env python3
"""
Manual debug script for analyzing mobile PWA header without browser automation
"""

import json
import re
from pathlib import Path


def analyze_header_styles():
    """Analyze header styles by examining CSS files directly"""
    
    print("Starting manual header analysis...")
    
    # Read CSS files
    css_files = [
        "/workspace/etax-mobile-pwa/source/css/common.css",
        "/workspace/etax-mobile-pwa/source/login.css"
    ]
    
    css_content = {}
    for css_file in css_files:
        if Path(css_file).exists():
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content[css_file] = f.read()
        else:
            print(f"CSS file not found: {css_file}")
    
    # Extract header-related styles
    header_styles = {}
    
    # Look for logo styles in login.css
    login_css = css_content.get("/workspace/etax-mobile-pwa/source/login.css", "")
    
    # Extract logo styles
    logo_match = re.search(r'/\* Logo \*/\s*\.(logo)\s*\{([^}]*(?:\}[^}])*)+\}', login_css, re.DOTALL)
    if logo_match:
        logo_styles = logo_match.group(0)
        header_styles['logo'] = extract_css_properties(logo_styles)
    
    # Extract logo img styles
    logo_img_match = re.search(r'\.logo img \{([^}]*(?:\}[^}])*)+\}', login_css, re.DOTALL)
    if logo_img_match:
        header_styles['logo_img'] = extract_css_properties(logo_img_match.group(0))
    
    # Extract logo h1 styles
    logo_h1_match = re.search(r'\.logo h1 \{([^}]*(?:\}[^}])*)+\}', login_css, re.DOTALL)
    if logo_h1_match:
        header_styles['logo_h1'] = extract_css_properties(logo_h1_match.group(0))
    
    # Look for design tokens
    design_tokens_match = re.search(r'/\* Design Tokens \*/\s*\.wrapper \{([^}]*(?:\}[^}])*)+\}', login_css, re.DOTALL)
    if design_tokens_match:
        header_styles['design_tokens'] = extract_css_properties(design_tokens_match.group(0))
    
    # Generate report
    report = {
        "header_styles": header_styles,
        "issues": [],
        "fixes": [],
        "viewport_info": {
            "device": "mobile (iPhone X equivalent)",
            "width": "375px",
            "height": "812px",
            "scale_factor": 2
        }
    }
    
    # Check for common issues
    logo_h1_styles = header_styles.get('logo_h1', {})
    
    # Check font size
    font_size = logo_h1_styles.get('font-size', '')
    if font_size != '28px':
        report["issues"].append({
            "type": "font_size",
            "element": "header title",
            "expected": "28px",
            "actual": font_size,
            "severity": "medium"
        })
        
        report["fixes"].append({
            "element": ".logo h1",
            "property": "font-size",
            "value": "28px",
            "reason": "Fix header title font size to match reference"
        })
    
    # Check color
    color = logo_h1_styles.get('color', '')
    if 'var(--login-text)' not in color and '#ffffff' not in color and '255, 255, 255' not in color:
        report["issues"].append({
            "type": "text_color",
            "element": "header title",
            "expected": "var(--login-text) or #ffffff",
            "actual": color,
            "severity": "high"
        })
        
        report["fixes"].append({
            "element": ".logo h1",
            "property": "color",
            "value": "var(--login-text)",
            "reason": "Fix header text color to match reference"
        })
    
    # Check text shadow
    text_shadow = logo_h1_styles.get('text-shadow', '')
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
    
    # Check margin
    margin = logo_h1_styles.get('margin', '')
    if '16px' not in margin and 'top' not in margin:
        report["issues"].append({
            "type": "margin",
            "element": "header title",
            "expected": "margin-top: 16px or similar",
            "actual": margin,
            "severity": "low"
        })
        
        report["fixes"].append({
            "element": ".logo h1",
            "property": "margin-top",
            "value": "16px",
            "reason": "Add proper margin to header title"
        })
    
    # Save report
    report_path = "/workspace/manual_debug_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Report saved to {report_path}")
    print(f"Found {len(report['issues'])} issues and {len(report['fixes'])} fixes")
    
    return report


def extract_css_properties(css_block):
    """Extract CSS properties from a CSS block"""
    properties = {}
    
    # Find all property: value; patterns
    pattern = r'([a-zA-Z\-]+)\s*:\s*([^;]+);'
    matches = re.findall(pattern, css_block)
    
    for prop, value in matches:
        properties[prop.strip()] = value.strip()
    
    return properties


def apply_fixes():
    """Apply the suggested fixes to the CSS files"""
    print("Applying fixes to CSS files...")
    
    css_file = "/workspace/etax-mobile-pwa/source/login.css"
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply fixes based on the analysis
    # Fix font size
    if '.logo h1 {' in content:
        # Check if font-size is already set to 28px
        if 'font-size: 28px' not in content:
            # Replace the font-size property or add it if it doesn't exist
            h1_block_match = re.search(r'(\.logo h1 \{[^}]*)\}', content, re.DOTALL)
            if h1_block_match:
                h1_block = h1_block_match.group(1)
                if 'font-size' in h1_block:
                    # Update existing font-size
                    content = re.sub(r'font-size: [^;]+;', 'font-size: 28px;', content)
                else:
                    # Add font-size property
                    content = re.sub(r'(\.logo h1 \{)', r'\1\n  font-size: 28px;', content)
    
    # Fix color if needed
    if '.logo h1 {' in content and 'color:' not in content:
        content = re.sub(r'(\.logo h1 \{)', r'\1\n  color: var(--login-text);', content)
    
    # Fix text-shadow if needed
    if '.logo h1 {' in content and 'text-shadow' not in content:
        content = re.sub(r'(\.logo h1 \{)', r'\1\n  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);', content)
    
    # Write the updated content back
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixes applied to {css_file}")


if __name__ == "__main__":
    report = analyze_header_styles()
    apply_fixes()