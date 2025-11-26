#!/usr/bin/env python3
"""
PWA Testing Tool cho eTax Mobile
Kiểm tra tất cả các yếu tố PWA cần thiết
"""

import requests
import json
import os
from urllib.parse import urljoin

class PWATester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "manifest": {},
            "service_worker": {},
            "html_pwa_tags": {},
            "icons": {},
            "security": {},
            "performance": {}
        }
    
    def test_manifest(self):
        """Kiểm tra PWA Manifest"""
        print("🔍 Testing PWA Manifest...")
        
        manifest_url = urljoin(self.base_url, "manifest.json")
        try:
            response = requests.get(manifest_url, timeout=10)
            if response.status_code == 200:
                manifest = response.json()
                
                required_fields = [
                    "name", "short_name", "icons", "start_url", 
                    "display", "theme_color", "background_color"
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in manifest:
                        missing_fields.append(field)
                
                if not missing_fields:
                    print("✅ Manifest có đầy đủ các field cần thiết")
                    self.results["manifest"]["status"] = "PASS"
                    self.results["manifest"]["score"] = 100
                else:
                    print(f"❌ Thiếu các field: {', '.join(missing_fields)}")
                    self.results["manifest"]["status"] = "FAIL"
                    self.results["manifest"]["missing_fields"] = missing_fields
                    self.results["manifest"]["score"] = 70 - len(missing_fields) * 10
                
                # Kiểm tra icons
                if "icons" in manifest:
                    icons_ok = True
                    for icon in manifest["icons"]:
                        icon_url = urljoin(self.base_url, icon["src"])
                        try:
                            icon_resp = requests.head(icon_url, timeout=5)
                            if icon_resp.status_code != 200:
                                icons_ok = False
                                print(f"⚠️ Icon không tồn tại: {icon['src']}")
                        except:
                            icons_ok = False
                            print(f"⚠️ Không thể truy cập icon: {icon['src']}")
                    
                    if icons_ok:
                        print("✅ Tất cả icons đều accessible")
                        self.results["icons"]["status"] = "PASS"
                    else:
                        self.results["icons"]["status"] = "FAIL"
                        print("❌ Một số icons không accessible")
                
                self.results["manifest"]["details"] = manifest
                
            else:
                print(f"❌ Không thể truy cập manifest.json (Status: {response.status_code})")
                self.results["manifest"]["status"] = "FAIL"
                self.results["manifest"]["score"] = 0
                
        except Exception as e:
            print(f"❌ Lỗi khi test manifest: {str(e)}")
            self.results["manifest"]["status"] = "ERROR"
    
    def test_service_worker(self):
        """Kiểm tra Service Worker"""
        print("\n🔍 Testing Service Worker...")
        
        sw_url = urljoin(self.base_url, "service-worker.js")
        try:
            response = requests.get(sw_url, timeout=10)
            if response.status_code == 200:
                sw_content = response.text
                
                # Kiểm tra các event handlers quan trọng
                events = ["install", "activate", "fetch"]
                found_events = []
                
                for event in events:
                    if f'"{event}"' in sw_content or f"'{event}'" in sw_content:
                        found_events.append(event)
                
                if len(found_events) >= 3:
                    print("✅ Service Worker có đầy đủ event handlers")
                    self.results["service_worker"]["status"] = "PASS"
                    self.results["service_worker"]["score"] = 90
                else:
                    print(f"⚠️ Service Worker thiếu một số event handlers: {found_events}")
                    self.results["service_worker"]["status"] = "PARTIAL"
                    self.results["service_worker"]["score"] = 70
                
                self.results["service_worker"]["events_found"] = found_events
                self.results["service_worker"]["file_size"] = len(sw_content)
                
            else:
                print(f"❌ Không thể truy cập service-worker.js (Status: {response.status_code})")
                self.results["service_worker"]["status"] = "FAIL"
                self.results["service_worker"]["score"] = 0
                
        except Exception as e:
            print(f"❌ Lỗi khi test service worker: {str(e)}")
            self.results["service_worker"]["status"] = "ERROR"
    
    def test_html_pwa_tags(self):
        """Kiểm tra PWA tags trong HTML"""
        print("\n🔍 Testing HTML PWA Tags...")
        
        pages = ["index.html", "login.html", "home.html"]
        tags_found = {}
        
        for page in pages:
            try:
                response = requests.get(urljoin(self.base_url, page), timeout=10)
                if response.status_code == 200:
                    html = response.text
                    
                    # PWA tags cần tìm
                    pwa_tags = [
                        ('viewport', 'viewport'),
                        ('theme-color', 'theme-color'),
                        ('apple-mobile-web-app-capable', 'apple-mobile-web-app-capable'),
                        ('apple-mobile-web-app-status-bar-style', 'apple-mobile-web-app-status-bar-style'),
                        ('manifest', 'link rel="manifest"'),
                        ('service-worker', 'link rel="serviceworker"')
                    ]
                    
                    page_tags = {}
                    for tag_name, search_text in pwa_tags:
                        if tag_name.lower() in html.lower() or search_text.lower() in html.lower():
                            page_tags[tag_name] = True
                        else:
                            page_tags[tag_name] = False
                    
                    tags_found[page] = page_tags
                    
                    print(f"📄 {page}:")
                    for tag, found in page_tags.items():
                        status = "✅" if found else "❌"
                        print(f"  {status} {tag}: {found}")
                
            except Exception as e:
                print(f"❌ Lỗi khi test {page}: {str(e)}")
                tags_found[page] = {"error": str(e)}
        
        # Tính điểm tổng
        total_score = 0
        pages_count = len(pages)
        
        for page, tags in tags_found.items():
            if "error" not in tags:
                page_score = sum(tags.values()) / len(tags) * 100
                total_score += page_score
        
        avg_score = total_score / pages_count if pages_count > 0 else 0
        
        self.results["html_pwa_tags"] = {
            "status": "PASS" if avg_score >= 80 else "PARTIAL" if avg_score >= 60 else "FAIL",
            "score": int(avg_score),
            "pages": tags_found
        }
        
        if avg_score >= 80:
            print("✅ HTML có đầy đủ PWA tags")
        elif avg_score >= 60:
            print("⚠️ HTML có một số PWA tags")
        else:
            print("❌ HTML thiếu nhiều PWA tags")
    
    def test_security(self):
        """Kiểm tra các tính năng bảo mật"""
        print("\n🔍 Testing Security Features...")
        
        # Kiểm tra HTTPS trong production (mock test)
        print("📋 Security Checklist:")
        security_items = [
            ("HTTPS", "Cần HTTPS cho PWA trong production"),
            ("CSP Headers", "Content Security Policy"),
            ("Service Worker Scope", "Service worker được đăng ký đúng scope"),
            ("Cache Strategy", "Cache strategy phù hợp")
        ]
        
        for item, desc in security_items:
            print(f"  📌 {item}: {desc}")
        
        self.results["security"] = {
            "status": "NEEDS_REVIEW",
            "items": security_items,
            "note": "Cần review thêm trong production environment"
        }
    
    def generate_report(self):
        """Tạo báo cáo tổng hợp"""
        print("\n" + "="*50)
        print("🎯 PWA TESTING REPORT - eTax Mobile")
        print("="*50)
        
        # Tính điểm tổng
        scores = []
        if "manifest" in self.results and "score" in self.results["manifest"]:
            scores.append(self.results["manifest"]["score"])
        
        if "service_worker" in self.results and "score" in self.results["service_worker"]:
            scores.append(self.results["service_worker"]["score"])
        
        if "html_pwa_tags" in self.results and "score" in self.results["html_pwa_tags"]:
            scores.append(self.results["html_pwa_tags"]["score"])
        
        overall_score = sum(scores) / len(scores) if scores else 0
        
        print(f"\n📊 OVERALL PWA SCORE: {overall_score:.1f}/100")
        
        if overall_score >= 90:
            print("🏆 EXCELLENT - PWA hoàn toàn sẵn sàng!")
        elif overall_score >= 80:
            print("✅ GOOD - PWA chạy tốt, cần một số cải thiện nhỏ")
        elif overall_score >= 60:
            print("⚠️ PARTIAL - PWA cần cải thiện đáng kể")
        else:
            print("❌ NEEDS WORK - PWA cần phát triển thêm")
        
        print(f"\n📋 Chi tiết từng component:")
        for component, result in self.results.items():
            if isinstance(result, dict) and "status" in result:
                print(f"  • {component}: {result['status']}")
        
        return self.results
    
    def run_all_tests(self):
        """Chạy tất cả tests"""
        print("🚀 Bắt đầu PWA Testing cho eTax Mobile...")
        print(f"🌐 Testing against: {self.base_url}")
        
        self.test_manifest()
        self.test_service_worker() 
        self.test_html_pwa_tags()
        self.test_security()
        
        return self.generate_report()

if __name__ == "__main__":
    tester = PWATester()
    results = tester.run_all_tests()
    
    # Lưu kết quả vào file
    with open("/workspace/pwa_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Kết quả chi tiết đã lưu vào: pwa_test_results.json")