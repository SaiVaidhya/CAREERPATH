"""
CareerPath AI - Application Server Entrypoint
Starts the Flask server for CareerPath AI.
"""

import os
import sys

# Ensure current directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.models import init_db, get_db_connection
from app.ml.engine import get_engine

app = create_app()

def bootstrap_application():
    """Ensure database is initialized and models are ready before running."""
    db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "careerpath.db"))
    if not os.path.exists(db_file):
        print("Database not found. Seeding initial database...")
        from seed_data import seed_database
        seed_database()

    # Preload ML Engine to verify serialization
    print("Verifying ML Recommendation Engine...")
    eng = get_engine()
    print("ML Engine loaded successfully.")

if __name__ == "__main__":
    bootstrap_application()
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "=" * 65)
    print("   CareerPath AI – Intelligent Career Recommendation System")
    print(f"   💻 Laptop / Local Browser : http://localhost:{port}")
    print(f"   📱 Mobile / Same Wi-Fi    : http://192.168.1.7:{port}")
    print("   Demo Student: demo@student.edu / Student@12345")
    print("   Administrator: admin@careerpath.ai / Admin@12345")
    print("=" * 65 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)
