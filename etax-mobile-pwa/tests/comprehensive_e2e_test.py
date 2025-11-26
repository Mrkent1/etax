#!/usr/bin/env python3
"""
Comprehensive E2E Testing Suite for eTax Mobile PWA
Tests all 22 HTML pages for functionality, PWA compliance, and potential issues
"""

import os
import json
import re
import time
import requests
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime

class ComprehensiveE2ETester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.base_path = "/workspace/etax_code/etax-html-version-main"
        self.results = {}
        self.bugs_found = []
        self.fixes_applied = []
        
    def find_all_html_pages(self):
        """Tìm tất cả HTML files"""
        html_files = []
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.base_path)
                    html_files.append(relative_path)
        return sorted(html_files)
    
    def test_html_structure(self, html_file):
        """Test HTML structure và validate"""
        results = {
            'file': html_file,
            'status': 'PASS',
            'issues': [],
            'warnings': [],
            'suggestions': []
        }
        
        try:
            with open(os.path.join(self.base_path, html_file), 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Test 1: Validate HTML structure
            if not soup.find('html'):
                results['issues'].append("Missing <html> tag")
                results['status'] = 'FAIL'
            
            # Test 2: Check viewport meta tag
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                results['issues'].append("Missing viewport meta tag")
                results['status'] = 'FAIL'
            elif 'width=device-width, initial-scale=1.0' not in viewport.get('content', ''):
                results['issues'].append(f"Incorrect viewport: {viewport.get('content')}")
                results['warnings'].append("Viewport should be: width=device-width, initial-scale=1.0")
            
            # Test 3: Check charset
            charset = soup.find('meta', attrs={'charset': True})
            if not charset:
                results['warnings'].append("Missing charset declaration")
            
            # Test 4: Check title
            title = soup.find('title')
            if not title or not title.get_text().strip():
                results['warnings'].append("Missing or empty title tag")
            
            # Test 5: Check for basic HTML structure
            if not soup.find('head'):
                results['issues'].append("Missing <head> section")
                results['status'] = 'FAIL'
            
            if not soup.find('body'):
                results['issues'].append("Missing <body> section")
                results['status'] = 'FAIL'
            
            # Test 6: Check for common PWA issues
            if 'login' in html_file.lower() or 'index' in html_file.lower():
                # Check for manifest link
                manifest_link = soup.find('link', attrs={'rel': 'manifest'})
                if not manifest_link:
                    results['warnings'].append("Missing manifest link for PWA")
                
                # Check for theme-color meta
                theme_color = soup.find('meta', attrs={'name': 'theme-color'})
                if not theme_color:
                    results['warnings'].append("Missing theme-color meta tag")
            
            # Test 7: Check for JavaScript errors (basic)
            scripts = soup.find_all('script')
            for script in scripts:
                src = script.get('src')
                if src and src.startswith('/'):
                    # Check if local JS files exist
                    js_path = os.path.join(self.base_path, src.lstrip('/'))
                    if not os.path.exists(js_path):
                        results['issues'].append(f"Missing JavaScript file: {src}")
            
            # Test 8: Check for CSS files
            links = soup.find_all('link', attrs={'rel': 'stylesheet'})
            for link in links:
                href = link.get('href')
                if href and href.startswith('/'):
                    css_path = os.path.join(self.base_path, href.lstrip('/'))
                    if not os.path.exists(css_path):
                        results['issues'].append(f"Missing CSS file: {href}")
            
        except Exception as e:
            results['status'] = 'FAIL'
            results['issues'].append(f"Error parsing HTML: {str(e)}")
        
        return results
    
    def test_pwa_compliance(self, html_file):
        """Test PWA compliance chi tiết"""
        results = {
            'file': html_file,
            'score': 0,
            'max_score': 100,
            'tests': {},
            'pass_count': 0,
            'total_tests': 10
        }
        
        try:
            with open(os.path.join(self.base_path, html_file), 'r', encoding='utf-8') as f:
                content = f.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # PWA Test 1: Viewport meta tag (10 points)
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if viewport and 'width=device-width, initial-scale=1.0' == viewport.get('content'):
                results['tests']['viewport'] = {'score': 10, 'status': 'PASS', 'details': 'Correct viewport meta tag'}
                results['pass_count'] += 1
            else:
                results['tests']['viewport'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing or incorrect viewport'}
            
            # PWA Test 2: Manifest link (15 points)
            manifest_link = soup.find('link', attrs={'rel': 'manifest'})
            if manifest_link:
                results['tests']['manifest'] = {'score': 15, 'status': 'PASS', 'details': 'Manifest link found'}
                results['pass_count'] += 1
            else:
                results['tests']['manifest'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing manifest link'}
            
            # PWA Test 3: Theme color (10 points)
            theme_color = soup.find('meta', attrs={'name': 'theme-color'})
            if theme_color:
                results['tests']['theme_color'] = {'score': 10, 'status': 'PASS', 'details': 'Theme color meta tag found'}
                results['pass_count'] += 1
            else:
                results['tests']['theme_color'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing theme color meta tag'}
            
            # PWA Test 4: Service worker registration (20 points)
            if 'login' in html_file.lower() or 'index' in html_file.lower():
                service_worker_reg = re.search(r'navigator\.serviceWorker\.register\(', content)
                if service_worker_reg:
                    results['tests']['service_worker'] = {'score': 20, 'status': 'PASS', 'details': 'Service worker registration found'}
                    results['pass_count'] += 1
                else:
                    results['tests']['service_worker'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing service worker registration'}
            
            # PWA Test 5: Mobile optimization meta tags (10 points)
            apple_mobile = soup.find('meta', attrs={'name': 'apple-mobile-web-app-capable'})
            if apple_mobile:
                results['tests']['apple_mobile'] = {'score': 10, 'status': 'PASS', 'details': 'Apple mobile web app capable tag found'}
                results['pass_count'] += 1
            else:
                results['tests']['apple_mobile'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing apple mobile web app meta tag'}
            
            # PWA Test 6: Icons (10 points)
            icons = soup.find_all('link', attrs={'rel': re.compile(r'icon|apple.*icon')})
            if icons:
                results['tests']['icons'] = {'score': 10, 'status': 'PASS', 'details': f'Found {len(icons)} icon links'}
                results['pass_count'] += 1
            else:
                results['tests']['icons'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing icon links'}
            
            # PWA Test 7: Start URL (5 points)
            if 'index.html' in html_file or 'login.html' in html_file:
                results['tests']['start_url'] = {'score': 5, 'status': 'PASS', 'details': 'Entry point page'}
                results['pass_count'] += 1
            
            # PWA Test 8: Offline readiness (15 points)
            # Check if service worker file exists
            sw_file = os.path.join(self.base_path, 'service-worker.js')
            if os.path.exists(sw_file):
                results['tests']['offline_ready'] = {'score': 15, 'status': 'PASS', 'details': 'Service worker file exists'}
                results['pass_count'] += 1
            else:
                results['tests']['offline_ready'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing service worker file'}
            
            # PWA Test 9: Manifest validation (10 points)
            manifest_file = os.path.join(self.base_path, 'manifest.json')
            if os.path.exists(manifest_file):
                try:
                    with open(manifest_file, 'r') as f:
                        manifest = json.load(f)
                    if manifest.get('name') and manifest.get('start_url'):
                        results['tests']['manifest_valid'] = {'score': 10, 'status': 'PASS', 'details': 'Manifest has required fields'}
                        results['pass_count'] += 1
                    else:
                        results['tests']['manifest_valid'] = {'score': 5, 'status': 'PARTIAL', 'details': 'Manifest missing required fields'}
                except:
                    results['tests']['manifest_valid'] = {'score': 0, 'status': 'FAIL', 'details': 'Invalid manifest.json'}
            else:
                results['tests']['manifest_valid'] = {'score': 0, 'status': 'FAIL', 'details': 'Missing manifest.json'}
            
            # PWA Test 10: Performance hints (5 points)
            preload_links = soup.find_all('link', attrs={'rel': 'preload'})
            if preload_links:
                results['tests']['performance'] = {'score': 5, 'status': 'PASS', 'details': 'Resource preloading found'}
                results['pass_count'] += 1
            else:
                results['tests']['performance'] = {'score': 0, 'status': 'FAIL', 'details': 'No resource preloading'}
            
            # Calculate total score
            for test, result in results['tests'].items():
                results['score'] += result['score']
            
            results['percentage'] = (results['score'] / results['max_score']) * 100
            
        except Exception as e:
            results['error'] = str(e)
            results['score'] = 0
            results['percentage'] = 0
        
        return results
    
    def test_javascript_functionality(self, html_file):
        """Test JavaScript functionality"""
        results = {
            'file': html_file,
            'functional_tests': {},
            'js_files': [],
            'errors': []
        }
        
        try:
            with open(os.path.join(self.base_path, html_file), 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find JavaScript files
            scripts = soup.find_all('script')
            for script in scripts:
                src = script.get('src')
                if src:
                    if src.startswith('/'):
                        full_path = os.path.join(self.base_path, src.lstrip('/'))
                    else:
                        full_path = os.path.join(self.base_path, src)
                    
                    if os.path.exists(full_path):
                        results['js_files'].append(src)
                        
                        # Test specific JS files
                        if 'auth.js' in src:
                            results['functional_tests']['auth'] = self.test_auth_js(full_path)
                        elif 'home.js' in src:
                            results['functional_tests']['home'] = self.test_home_js(full_path)
            
            # Check for common JavaScript patterns
            inline_scripts = soup.find_all('script', src=False)
            for script in inline_scripts:
                script_content = script.get_text()
                if 'function' in script_content or 'const ' in script_content or 'var ' in script_content:
                    results['functional_tests']['inline_js'] = True
            
        except Exception as e:
            results['errors'].append(f"Error testing JavaScript: {str(e)}")
        
        return results
    
    def test_auth_js(self, js_file_path):
        """Test auth.js specific functionality"""
        results = {'status': 'UNKNOWN', 'issues': []}
        
        try:
            with open(js_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for authentication logic
            if 'isAuthenticated' in content:
                results['has_auth'] = True
            else:
                results['issues'].append("Missing isAuthenticated function")
            
            if 'login' in content.lower():
                results['has_login'] = True
            else:
                results['issues'].append("Missing login functionality")
            
            if 'logout' in content.lower():
                results['has_logout'] = True
            
            if results['has_auth'] and results['issues']:
                results['status'] = 'PARTIAL'
            elif results['has_auth'] and not results['issues']:
                results['status'] = 'PASS'
            else:
                results['status'] = 'FAIL'
                
        except Exception as e:
            results['status'] = 'ERROR'
            results['error'] = str(e)
        
        return results
    
    def test_home_js(self, js_file_path):
        """Test home.js specific functionality"""
        results = {'status': 'UNKNOWN', 'issues': []}
        
        try:
            with open(js_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for navigation
            if 'navigateTo' in content:
                results['has_navigation'] = True
            else:
                results['issues'].append("Missing navigation function")
            
            # Check for authentication check
            if 'isAuthenticated' in content:
                results['has_auth_check'] = True
            else:
                results['issues'].append("Missing authentication check")
            
            # Check if auth check is commented out (security issue)
            if 'isAuthenticated' in content and content.count('/*') > content.count('isAuthenticated'):
                results['security_issue'] = "Authentication check may be commented out"
            
            if results['has_navigation'] and results['has_auth_check'] and 'security_issue' not in results:
                results['status'] = 'PASS'
            elif results['has_navigation'] and results['has_auth_check']:
                results['status'] = 'PARTIAL'
            else:
                results['status'] = 'FAIL'
                
        except Exception as e:
            results['status'] = 'ERROR'
            results['error'] = str(e)
        
        return results
    
    def test_network_requirements(self):
        """Test network requirements for PWA"""
        results = {
            'manifest_test': False,
            'service_worker_test': False,
            'cors_test': False,
            'errors': []
        }
        
        # Test manifest.json
        try:
            manifest_url = f"{self.base_url}/manifest.json"
            response = requests.get(manifest_url, timeout=10)
            if response.status_code == 200:
                manifest_data = response.json()
                if manifest_data.get('name') and manifest_data.get('start_url'):
                    results['manifest_test'] = True
        except Exception as e:
            results['errors'].append(f"Manifest test failed: {str(e)}")
        
        # Test service worker
        try:
            sw_url = f"{self.base_url}/service-worker.js"
            response = requests.get(sw_url, timeout=10)
            if response.status_code == 200:
                results['service_worker_test'] = True
        except Exception as e:
            results['errors'].append(f"Service worker test failed: {str(e)}")
        
        return results
    
    def auto_fix_viewport(self, html_file):
        """Auto fix viewport meta tag"""
        try:
            file_path = os.path.join(self.base_path, html_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace viewport meta tag
            pattern = r'<meta\s+name=["\']viewport["\'][^>]*>'
            replacement = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, f"Fixed viewport in {html_file}"
            
            return False, f"No viewport tag found in {html_file}"
            
        except Exception as e:
            return False, f"Error fixing {html_file}: {str(e)}"
    
    def add_service_worker_registration(self, html_file):
        """Add service worker registration script"""
        try:
            file_path = os.path.join(self.base_path, html_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already has service worker registration
            if 'navigator.serviceWorker.register(' in content:
                return False, f"Service worker registration already exists in {html_file}"
            
            # Find closing body tag and add script before it
            if '</body>' in content:
                sw_script = '''
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(function(registration) {
                        console.log('SW registered: ', registration);
                    })
                    .catch(function(registrationError) {
                        console.log('SW registration failed: ', registrationError);
                    });
            });
        }
    </script>'''
                
                content = content.replace('</body>', sw_script + '\n</body>')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True, f"Added service worker registration to {html_file}"
            
            return False, f"Could not find </body> tag in {html_file}"
            
        except Exception as e:
            return False, f"Error adding service worker registration to {html_file}: {str(e)}"
    
    def add_pwa_meta_tags(self, html_file):
        """Add missing PWA meta tags to index.html"""
        try:
            if 'index.html' not in html_file:
                return False, f"Not index.html, skipping {html_file}"
            
            file_path = os.path.join(self.base_path, html_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if meta tags already exist
            if 'theme-color' in content and 'apple-mobile-web-app-capable' in content:
                return False, f"PWA meta tags already exist in {html_file}"
            
            # Find head tag
            head_pattern = r'(<head[^>]*>)'
            head_match = re.search(head_pattern, content, re.IGNORECASE)
            
            if head_match:
                pwa_meta_tags = '''
    <meta name="theme-color" content="#cc0000">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'''
                
                new_content = content.replace(head_match.group(1), head_match.group(1) + pwa_meta_tags)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, f"Added PWA meta tags to {html_file}"
            
            return False, f"Could not find <head> tag in {html_file}"
            
        except Exception as e:
            return False, f"Error adding PWA meta tags to {html_file}: {str(e)}"
    
    def run_comprehensive_test(self):
        """Chạy comprehensive testing cho tất cả files"""
        print("🚀 Starting Comprehensive E2E Testing...")
        print(f"📁 Testing files in: {self.base_path}")
        
        # Find all HTML files
        html_files = self.find_all_html_pages()
        print(f"📄 Found {len(html_files)} HTML files")
        
        all_results = {
            'test_timestamp': datetime.now().isoformat(),
            'total_files': len(html_files),
            'html_structure_tests': {},
            'pwa_compliance_tests': {},
            'javascript_tests': {},
            'network_tests': {},
            'summary': {
                'total_bugs': 0,
                'auto_fixes_applied': 0,
                'pwa_scores': []
            }
        }
        
        # Test từng file
        for i, html_file in enumerate(html_files, 1):
            print(f"🔍 Testing {i}/{len(html_files)}: {html_file}")
            
            # HTML Structure Test
            html_results = self.test_html_structure(html_file)
            all_results['html_structure_tests'][html_file] = html_results
            
            # PWA Compliance Test
            pwa_results = self.test_pwa_compliance(html_file)
            all_results['pwa_compliance_tests'][html_file] = pwa_results
            all_results['summary']['pwa_scores'].append(pwa_results.get('percentage', 0))
            
            # JavaScript Functionality Test
            js_results = self.test_javascript_functionality(html_file)
            all_results['javascript_tests'][html_file] = js_results
            
            # Count bugs
            bug_count = len(html_results.get('issues', [])) + len(pwa_results.get('tests', {}).get('status', 'FAIL'))
            all_results['summary']['total_bugs'] += bug_count
        
        # Network tests
        print("🌐 Running network tests...")
        network_results = self.test_network_requirements()
        all_results['network_tests'] = network_results
        
        # Auto-fix issues
        print("🔧 Applying auto-fixes...")
        auto_fix_count = 0
        
        for html_file in html_files:
            # Fix viewport issues
            fixed, message = self.auto_fix_viewport(html_file)
            if fixed:
                auto_fix_count += 1
                self.fixes_applied.append(message)
                print(f"✅ {message}")
            
            # Add service worker registration for main pages
            if html_file in ['index.html', 'login.html', 'home.html']:
                added, message = self.add_service_worker_registration(html_file)
                if added:
                    auto_fix_count += 1
                    self.fixes_applied.append(message)
                    print(f"✅ {message}")
            
            # Add PWA meta tags to index.html
            if html_file == 'index.html':
                added, message = self.add_pwa_meta_tags(html_file)
                if added:
                    auto_fix_count += 1
                    self.fixes_applied.append(message)
                    print(f"✅ {message}")
        
        all_results['summary']['auto_fixes_applied'] = auto_fix_count
        
        # Calculate average PWA score
        if all_results['summary']['pwa_scores']:
            all_results['summary']['average_pwa_score'] = sum(all_results['summary']['pwa_scores']) / len(all_results['summary']['pwa_scores'])
        
        return all_results

if __name__ == "__main__":
    tester = ComprehensiveE2ETester()
    results = tester.run_comprehensive_test()
    
    # Save results
    with open('/workspace/comprehensive_e2e_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎯 Testing completed!")
    print(f"📊 Total files tested: {results['total_files']}")
    print(f"🐛 Total bugs found: {results['summary']['total_bugs']}")
    print(f"🔧 Auto-fixes applied: {results['summary']['auto_fixes_applied']}")
    print(f"⭐ Average PWA score: {results['summary'].get('average_pwa_score', 0):.1f}%")
    
    if tester.fixes_applied:
        print(f"\n✅ Fixes applied:")
        for fix in tester.fixes_applied:
            print(f"   - {fix}")
    
    print(f"\n💾 Detailed results saved to: comprehensive_e2e_results.json")