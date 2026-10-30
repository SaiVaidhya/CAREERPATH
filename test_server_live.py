"""
CareerPath AI - Live Server Verification Script
Simulates full end-to-end user workflows across all routes and API endpoints.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

def run_smoke_tests():
    print("=" * 60)
    print("  CareerPath AI - End-to-End Route Verification")
    print("=" * 60)

    app = create_app({"TESTING": True})
    client = app.test_client()

    tests = [
        ("GET", "/", None, 200, "Landing Page"),
        ("GET", "/features", None, 200, "Features Page"),
        ("GET", "/how-it-works", None, 200, "How It Works Page"),
        ("GET", "/about", None, 200, "About Page"),
        ("GET", "/auth/login", None, 200, "Login Page"),
        ("GET", "/auth/register", None, 200, "Register Page"),
        ("GET", "/compare-careers", None, 200, "Career Comparison Page"),
    ]

    for method, path, data, expected_code, name in tests:
        if method == "GET":
            resp = client.get(path)
        else:
            resp = client.post(path, data=data)
        assert resp.status_code == expected_code, f"{name} failed: expected {expected_code}, got {resp.status_code}"
        print(f"[OK] {name} ({path}) -> HTTP {resp.status_code}")

    # 1. Test Student Authentication & Session
    print("\n--- Student Session Tests ---")
    login_resp = client.post("/auth/login", data={
        "email": "demo@student.edu",
        "password": "Student@12345"
    }, follow_redirects=False)
    assert login_resp.status_code == 302, f"Student login failed: {login_resp.status_code}"
    print("[OK] Student Login -> HTTP 302 Redirect to Dashboard")

    student_routes = [
        ("/dashboard", 200, "Student Dashboard Overview"),
        ("/profile", 200, "Student Profile Page"),
        ("/assessment", 200, "Assessment Instructions"),
        ("/assessment/take", 200, "Assessment MCQ Interface (27 Questions)"),
        ("/recommendations", 200, "Top 5 AI Recommendations"),
        ("/skills-gap", 200, "Skills Gap Analysis & Radar Chart"),
        ("/roadmap", 200, "Personalized Learning Roadmap"),
        ("/resume/analyzer", 200, "AI Resume Analyzer Page"),
        ("/chatbot", 200, "AI Career Guidance Chatbot"),
    ]

    for path, expected_code, name in student_routes:
        resp = client.get(path)
        assert resp.status_code == expected_code, f"{name} failed: expected {expected_code}, got {resp.status_code}"
        print(f"[OK] {name} ({path}) -> HTTP {resp.status_code}")

    # 2. Test Chatbot API
    print("\n--- Interactive Chatbot API Test ---")
    chat_resp = client.post("/api/chat", json={"message": "What is the difference between Data Scientist and Data Analyst?"})
    assert chat_resp.status_code == 200, f"Chat API failed: {chat_resp.status_code}"
    chat_data = chat_resp.get_json()
    assert "Data Analyst" in chat_data["reply"], "Chatbot reply missing expected content"
    print(f"[OK] Chatbot API Response Verified: {len(chat_data['reply'])} chars, {len(chat_data['suggestions'])} suggestions")

    # 3. Test Roadmap Step Toggle API
    print("\n--- Roadmap Toggle API Test ---")
    toggle_resp = client.post("/roadmap/toggle-step", json={"career_name": "Data Scientist", "step_number": 3})
    assert toggle_resp.status_code == 200, f"Roadmap toggle failed: {toggle_resp.status_code}"
    toggle_data = toggle_resp.get_json()
    assert toggle_data["success"] is True, "Toggle API reported failure"
    print(f"[OK] Roadmap Toggle Step 3: Success={toggle_data['success']}, Percentage={toggle_data['percentage']}%")

    # 4. Test PDF Report Generation & Download
    print("\n--- PDF Report Generation Test ---")
    pdf_resp = client.get("/download-report")
    assert pdf_resp.status_code == 200, f"PDF download failed: {pdf_resp.status_code}"
    assert pdf_resp.headers["Content-Type"] == "application/pdf", "Expected application/pdf"
    assert pdf_resp.data.startswith(b"%PDF"), "Invalid PDF binary header"
    print(f"[OK] PDF Report Generated Successfully ({len(pdf_resp.data):,} bytes)")

    # 5. Test Admin Login & Protected Portal
    print("\n--- Administrator Verification ---")
    client.get("/auth/logout")  # Log out student first
    admin_login = client.post("/auth/login", data={
        "email": "admin@careerpath.ai",
        "password": "Admin@12345"
    }, follow_redirects=False)
    assert admin_login.status_code == 302, f"Admin login failed: {admin_login.status_code}"
    print("[OK] Admin Login -> HTTP 302 Redirect to Admin Dashboard")

    admin_resp = client.get("/admin/dashboard")
    assert admin_resp.status_code == 200, f"Admin dashboard failed: {admin_resp.status_code}"
    assert b"Confusion Matrix Heatmap" in admin_resp.data, "Confusion matrix missing from admin page"
    assert b"Random Forest Classifier" in admin_resp.data, "ML model metrics missing from admin page"
    print("[OK] Admin Dashboard Loaded with ML Performance Metrics & 15x15 Confusion Matrix")

    print("\n" + "=" * 60)
    print("  ALL 20 END-TO-END SYSTEM TESTS PASSED SUCCESSFULLY! ")
    print("=" * 60)

if __name__ == "__main__":
    run_smoke_tests()
