"""
CareerPath AI - Database Seeding Script
Populates:
1. Canonical career benchmarks and roadmap milestones
2. 27 High-quality assessment MCQs across 9 assessment categories
3. Admin credentials: admin@careerpath.ai / Admin@12345
4. Demo student credentials: demo@student.edu / Student@12345 with realistic sample assessment
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models import init_db, get_db_connection, User, StudentProfile
from app.ml.career_data import CAREER_DETAILS, CAREERS
from app.ml.engine import get_engine

ASSESSMENT_QUESTIONS = [
    # 1. Logical Reasoning
    {
        "category": "logical_reasoning",
        "question": "If all Developers understand Algorithms, and some Designers understand Algorithms, which statement is logically guaranteed?",
        "option_a": "All Designers are Developers",
        "option_b": "Some individuals who understand Algorithms are Designers",
        "option_c": "All individuals who understand Algorithms are Developers",
        "option_d": "No Designers are Developers",
        "correct": "B",
        "explanation": "Since some designers understand algorithms, those individuals are both designers and algorithm-literate."
    },
    {
        "category": "logical_reasoning",
        "question": "Look at this sequence: 4, 9, 25, 49, 121, ?. What number should come next?",
        "option_a": "144",
        "option_b": "169",
        "option_c": "196",
        "option_d": "225",
        "correct": "B",
        "explanation": "These are squares of prime numbers: 2^2=4, 3^2=9, 5^2=25, 7^2=49, 11^2=121. The next prime is 13, so 13^2 = 169."
    },
    {
        "category": "logical_reasoning",
        "question": "Statement: 'A is taller than B. C is shorter than A but taller than D.' Who is definitively the tallest?",
        "option_a": "B",
        "option_b": "C",
        "option_c": "A",
        "option_d": "Cannot be determined",
        "correct": "C",
        "explanation": "A is taller than B, and A is taller than C (which is taller than D). Therefore, A is the tallest."
    },

    # 2. Analytical Thinking
    {
        "category": "analytical_thinking",
        "question": "An e-commerce website experiences a 30% drop in checkout conversions while traffic remains steady. What is the best initial analytical step?",
        "option_a": "Immediately redesign the home page banner",
        "option_b": "Check user drop-off funnel logs and payment gateway error rates",
        "option_c": "Increase marketing budget to acquire more traffic",
        "option_d": "Fire the customer support manager",
        "correct": "B",
        "explanation": "Funnel analysis and error logs identify the exact technical or UX failure point in the transaction pipeline."
    },
    {
        "category": "analytical_thinking",
        "question": "When interpreting two variables with a high correlation coefficient (r = 0.92), what conclusion is scientifically valid?",
        "option_a": "Variable A causes Variable B directly",
        "option_b": "A strong statistical association exists, but causality requires further controlled experimentation",
        "option_c": "There is definitely a lurking third variable",
        "option_d": "The correlation is purely coincidental",
        "correct": "B",
        "explanation": "Correlation does not imply causation without controlled intervention and causal inference testing."
    },
    {
        "category": "analytical_thinking",
        "question": "You have a dataset where 99% of transactions are legitimate and 1% are fraud. What metric best measures a fraud detection model?",
        "option_a": "Accuracy",
        "option_b": "Precision-Recall AUC / F1-Score on the fraud class",
        "option_c": "Mean Squared Error",
        "option_d": "R-squared value",
        "correct": "B",
        "explanation": "In severe class imbalance, high accuracy can be trivially achieved by predicting everything as legitimate. PR-AUC and F1 measure true fraud capture."
    },

    # 3. Problem Solving
    {
        "category": "problem_solving",
        "question": "You have 8 balls that look identical, but one is slightly heavier. Using a two-pan balance scale, what is the minimum weighings needed to find the heavy ball?",
        "option_a": "1",
        "option_b": "2",
        "option_c": "3",
        "option_d": "4",
        "correct": "B",
        "explanation": "Divide into 3-3-2. First weighing: weigh 3 vs 3. If balanced, heavy ball is in the remaining 2 (weigh 1 vs 1). If unbalanced, take the 3 and weigh 1 vs 1. 2 weighings guaranteed."
    },
    {
        "category": "problem_solving",
        "question": "A web service experiences sudden memory exhaustion and crashes every 4 hours under peak load. How would you systematically diagnose this?",
        "option_a": "Restart the server automatically every 3 hours with a cron job",
        "option_b": "Capture heap memory snapshots over time to isolate object retention and unclosed connection leaks",
        "option_c": "Double the RAM without investigating",
        "option_d": "Switch programming languages immediately",
        "correct": "B",
        "explanation": "Heap profiling pinpoints memory leaks, uncollected references, or buffer pooling bugs."
    },
    {
        "category": "problem_solving",
        "question": "To efficiently find whether a cycle exists in a directed graph of dependencies, which algorithmic technique is optimal?",
        "option_a": "Linear search across all node pairs",
        "option_b": "Depth-First Search (DFS) with recursion stack state tracking / Kahn's Topological Sort",
        "option_c": "Binary Search",
        "option_d": "Bubble Sort",
        "correct": "B",
        "explanation": "DFS cycle detection with 3-color states or Kahn's algorithm detects cycles in O(V + E) linear time."
    },

    # 4. Mathematics
    {
        "category": "mathematics",
        "question": "What is the derivative of f(x) = 3x^3 - 5x + 7 with respect to x?",
        "option_a": "9x^2 - 5",
        "option_b": "6x^2 - 5",
        "option_c": "9x^3 - 5",
        "option_d": "3x^2 + 7",
        "correct": "A",
        "explanation": "d/dx(3x^3) = 9x^2; d/dx(-5x) = -5; d/dx(7) = 0. Result: 9x^2 - 5."
    },
    {
        "category": "mathematics",
        "question": "In linear algebra, if the determinant of a square matrix A is 0, what does this indicate?",
        "option_a": "The matrix is symmetric",
        "option_b": "The matrix is non-invertible (singular) and its columns are linearly dependent",
        "option_c": "The matrix is an identity matrix",
        "option_d": "All eigenvalues are equal to 1",
        "correct": "B",
        "explanation": "A determinant of zero means volume scaling is 0, the matrix has no inverse, and vectors collapse onto a lower dimensional subspace."
    },
    {
        "category": "mathematics",
        "question": "If you roll two fair standard 6-sided dice, what is the probability that their sum is equal to 7?",
        "option_a": "1/12",
        "option_b": "1/6",
        "option_c": "7/36",
        "option_d": "5/36",
        "correct": "B",
        "explanation": "Combinations summing to 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 outcomes out of 36 total. 6/36 = 1/6."
    },

    # 5. Technical Aptitude
    {
        "category": "technical_aptitude",
        "question": "What is the primary operational difference between a Process and a Thread in operating systems?",
        "option_a": "Processes cannot execute code",
        "option_b": "Threads within the same process share memory address space, whereas processes have isolated memory spaces",
        "option_c": "Threads cannot run concurrently",
        "option_d": "Processes do not have PIDs",
        "correct": "B",
        "explanation": "Threads share text, data, and heap within a process, while processes have private virtual address spaces protected by the MMU."
    },
    {
        "category": "technical_aptitude",
        "question": "In networking, which protocol provides reliable, connection-oriented byte stream transmission with congestion control?",
        "option_a": "UDP",
        "option_b": "TCP",
        "option_c": "ICMP",
        "option_d": "ARP",
        "correct": "B",
        "explanation": "TCP incorporates a 3-way handshake, sequence numbers, checksums, retransmission timers, and windowing congestion control."
    },
    {
        "category": "technical_aptitude",
        "question": "What is the primary purpose of an index on a database table column?",
        "option_a": "To encrypt sensitive data on disk",
        "option_b": "To accelerate SELECT query lookups at the trade-off of slight overhead on write operations",
        "option_c": "To enforce foreign key relationships only",
        "option_d": "To compress table storage size",
        "correct": "B",
        "explanation": "B-Tree/Hash indexes reduce search time from O(N) full table scans to O(log N) tree traversals."
    },

    # 6. Creativity
    {
        "category": "creativity",
        "question": "When designing an innovative mobile onboarding flow for a complex fintech app, which approach promotes the highest user engagement?",
        "option_a": "Displaying a 15-page PDF terms and conditions prompt upfront",
        "option_b": "Progressive disclosure with micro-interactions, contextual gamified guidance, and minimal initial inputs",
        "option_c": "Requiring all financial documents before allowing the user to see the dashboard",
        "option_d": "A static monochrome text page with zero visual feedback",
        "correct": "B",
        "explanation": "Progressive disclosure lowers cognitive friction, letting users experience immediate product value."
    },
    {
        "category": "creativity",
        "question": "In human-computer interaction, what is the role of visual hierarchy and whitespace?",
        "option_a": "Filling up every pixel to maximize content density",
        "option_b": "Directing the viewer's eye rhythmically to key actions and reducing cognitive overload",
        "option_c": "Slowing down rendering speed deliberately",
        "option_d": "Preventing mobile users from scrolling",
        "correct": "B",
        "explanation": "Whitespace and typographic weight create contrast, focus attention, and enhance intuitive readability."
    },
    {
        "category": "creativity",
        "question": "You are asked to generate novel ideas for an AI product feature. Which brainstorming technique is most divergent and exploratory?",
        "option_a": "Copying the exact layout of your top competitor",
        "option_b": "SCAMPER (Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse) methodology",
        "option_c": "Only allowing the senior manager to speak",
        "option_d": "Accepting the very first solution without exploration",
        "correct": "B",
        "explanation": "SCAMPER systematically forces lateral thinking and re-evaluates assumptions from multiple angles."
    },

    # 7. Communication Skills
    {
        "category": "communication_skills",
        "question": "How should a technical lead explain a database deadlock incident to non-technical executive stakeholders?",
        "option_a": "Using obscure low-level assembly dumps and mutex address pointers",
        "option_b": "Using an intuitive analogy (e.g. two cars blocking a narrow single-lane bridge), outlining business impact and preventative safeguards",
        "option_c": "Refusing to explain because executives wouldn't understand",
        "option_d": "Blaming external cloud vendors without providing data",
        "correct": "B",
        "explanation": "Effective communication translates complex engineering mechanics into business-relevant clarity and actionable remediations."
    },
    {
        "category": "communication_skills",
        "question": "During a contentious code review discussion where two engineers disagree on an architecture design, what is the best communicative response?",
        "option_a": "Rejecting the pull request with a sarcastic comment",
        "option_b": "Scheduling a synchronous discussion to walk through objective trade-offs, benchmarks, and team conventions empathetically",
        "option_c": "Escalating directly to the CEO",
        "option_d": "Merging the code secretly without consensus",
        "correct": "B",
        "explanation": "Collaborative, criteria-driven communication preserves psychological safety while reaching technical excellence."
    },
    {
        "category": "communication_skills",
        "question": "What is the core principle of active listening in client requirements gathering?",
        "option_a": "Formulating your rebuttal while the client is still talking",
        "option_b": "Paraphrasing and summarizing the client's problem statement to validate shared understanding before proposing solutions",
        "option_c": "Nodding continuously without taking notes",
        "option_d": "Interrupting to show how much you know",
        "correct": "B",
        "explanation": "Reflective playback confirms alignment, clarifies ambiguity, and builds stakeholder trust."
    },

    # 8. Leadership
    {
        "category": "leadership",
        "question": "A critical production sprint deadline is approaching, and an unexpected blocker threatens delivery. What is the most effective leadership action?",
        "option_a": "Assigning blame publicly to create urgency",
        "option_b": "Reranking priorities with stakeholders, deselecting non-essential scope, and unblocking the team collaboratively",
        "option_c": "Hiding the delay until the release date arrives",
        "option_d": "Demanding everyone work 24 hours straight without guidance",
        "correct": "B",
        "explanation": "Decisive leadership involves transparent communication, scope negotiation, and removing operational friction."
    },
    {
        "category": "leadership",
        "question": "When mentoring a junior developer who lacks confidence in system design, what leadership approach fosters the greatest long-term growth?",
        "option_a": "Writing all their architectural diagrams for them",
        "option_b": "Guiding them through pair-design sessions, asking Socratic questions, and providing constructive feedback in small iterations",
        "option_c": "Telling them they are not ready for engineering",
        "option_d": "Assigning them only documentation tasks indefinitely",
        "correct": "B",
        "explanation": "Empowering mentorship develops autonomous problem-solving capabilities through safe guided practice."
    },
    {
        "category": "leadership",
        "question": "What is the defining characteristic of servant leadership in agile software engineering?",
        "option_a": "Enforcing top-down micromanagement of daily hours",
        "option_b": "Focusing on enabling the team's success, removing systemic roadblocks, and cultivating team autonomy",
        "option_c": "Avoiding all accountability during product failures",
        "option_d": "Refusing to make tough strategic decisions",
        "correct": "B",
        "explanation": "Servant leadership prioritizes team enablement, psychological safety, and collective ownership."
    },

    # 9. Programming Knowledge
    {
        "category": "programming_knowledge",
        "question": "What is the time complexity of searching for an element in an unsorted array of size N versus a balanced Binary Search Tree (BST)?",
        "option_a": "O(1) vs O(N)",
        "option_b": "O(N) for unsorted array vs O(log N) for balanced BST",
        "option_c": "O(log N) for both",
        "option_d": "O(N^2) vs O(1)",
        "correct": "B",
        "explanation": "An unsorted array requires scanning up to N elements (O(N)), while a balanced BST cuts the search space in half at each step (O(log N))."
    },
    {
        "category": "programming_knowledge",
        "question": "In Python, what is the key difference between a List and a Tuple?",
        "option_a": "Lists are immutable; Tuples are mutable",
        "option_b": "Lists are mutable and can be modified after creation; Tuples are immutable and cannot be altered",
        "option_c": "Tuples cannot hold heterogeneous data types",
        "option_d": "Lists are always faster for hash table keys",
        "correct": "B",
        "explanation": "Tuples cannot be changed once allocated, making them memory-efficient, hashable, and thread-safe."
    },
    {
        "category": "programming_knowledge",
        "question": "In REST API design, which HTTP method is idempotent and conventionally used to replace an entire resource representation?",
        "option_a": "POST",
        "option_b": "PUT",
        "option_c": "PATCH",
        "option_d": "CONNECT",
        "correct": "B",
        "explanation": "PUT is defined as idempotent (multiple identical requests yield identical server state) for full resource replacement."
    }
]

def seed_database():
    """Initializes the database and seeds default data."""
    print("Initializing database tables...")
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Seed Careers & Roadmaps
    print("Seeding canonical careers & learning roadmaps...")
    for career_name in CAREERS:
        meta = CAREER_DETAILS[career_name]
        cursor.execute("""
            INSERT OR REPLACE INTO career_dataset 
            (career_name, category, description, difficulty, salary_range, growth_outlook, benchmark_scores_json, required_skills_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            career_name,
            meta["category"],
            meta["description"],
            meta["difficulty"],
            meta["salary_range"],
            meta["growth_outlook"],
            json.dumps(meta["benchmark_scores"]),
            json.dumps(meta["required_skills"])
        ))

        # Clear existing roadmaps for this career and insert updated steps
        cursor.execute("DELETE FROM learning_roadmaps WHERE career_name = ?", (career_name,))
        for step in meta["roadmap"]:
            cursor.execute("""
                INSERT INTO learning_roadmaps (career_name, step_number, title, duration, level, topics, resources)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                career_name,
                step["step"],
                step["title"],
                step["duration"],
                step["level"],
                step["topics"],
                step["resources"]
            ))

    # 2. Seed Assessment Questions
    print(f"Seeding {len(ASSESSMENT_QUESTIONS)} assessment questions...")
    cursor.execute("DELETE FROM assessment_questions")
    for q in ASSESSMENT_QUESTIONS:
        cursor.execute("""
            INSERT INTO assessment_questions (question_text, category, option_a, option_b, option_c, option_d, correct_option, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q["question"],
            q["category"],
            q["option_a"],
            q["option_b"],
            q["option_c"],
            q["option_d"],
            q["correct"],
            q["explanation"]
        ))

    conn.commit()
    conn.close()

    # 3. Create Admin User
    admin = User.get_by_email("admin@careerpath.ai")
    if not admin:
        print("Creating default administrator account (admin@careerpath.ai)...")
        User.create(
            name="System Administrator",
            email="admin@careerpath.ai",
            password="Admin@12345",
            education_level="Postgraduate",
            role="admin"
        )
    else:
        print("Administrator account already exists.")

    # 4. Create Demo Student User
    demo = User.get_by_email("demo@student.edu")
    if not demo:
        print("Creating sample demo student account (demo@student.edu)...")
        user_id = User.create(
            name="Aarav Sharma",
            email="demo@student.edu",
            password="Student@12345",
            education_level="Undergraduate",
            role="student"
        )
        # Populate student profile
        StudentProfile.update(user_id, {
            "age": 21,
            "gender": "Male",
            "education_qualification": "Undergraduate",
            "college_name": "National Institute of Technology",
            "degree": "B.Tech",
            "branch": "Computer Science & Engineering",
            "current_semester": 7,
            "cgpa": 8.75,
            "programming_skills": "Python, C++, JavaScript, SQL",
            "technical_skills": "Machine Learning, Pandas, Scikit-learn, Git, Flask",
            "soft_skills": "Analytical Thinking, Problem Solving, Team Leadership",
            "interests": "Predictive Modeling, AI Systems, Data Visualization",
            "preferred_career_domain": "Data & AI"
        }, skill_ratings={
            "programming_python": 88,
            "programming_java_cpp": 75,
            "web_technologies": 60,
            "data_structures_algorithms": 82,
            "databases_sql": 80,
            "machine_learning_ai": 85,
            "cloud_computing": 65,
            "networking_security": 50,
            "ui_ux_design": 45,
            "business_analytics": 78
        })

        # Add sample assessment result
        cat_scores = {
            "logical_reasoning": 90,
            "analytical_thinking": 95,
            "problem_solving": 88,
            "mathematics": 92,
            "technical_aptitude": 85,
            "creativity": 72,
            "communication_skills": 80,
            "leadership": 75,
            "programming_knowledge": 92
        }
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO assessment_results (user_id, total_score, max_score, percentage, category_scores_json)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, 24, 27, 88.89, json.dumps(cat_scores)))
        conn.commit()

        # Generate and save demo recommendation using ML engine
        eng = get_engine()
        recs = eng.predict(
            StudentProfile.get_by_user_id(user_id)["skill_ratings"],
            cat_scores,
            top_k=5
        )
        conn.execute("""
            INSERT INTO career_recommendations (user_id, primary_career, match_score, top_careers_json)
            VALUES (?, ?, ?, ?)
        """, (user_id, recs[0]["career"], recs[0]["match_score"], json.dumps(recs)))
        
        # Mark first 2 steps of roadmap completed for demonstration
        conn.execute("""
            INSERT OR REPLACE INTO roadmap_progress (user_id, career_name, step_number, completed, completed_at)
            VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP), (?, ?, ?, 1, CURRENT_TIMESTAMP)
        """, (user_id, recs[0]["career"], 1, user_id, recs[0]["career"], 2))
        
        conn.commit()
        conn.close()
        print("Demo student Aarav Sharma created with realistic profile, assessment, and recommendations!")
    else:
        print("Demo student account already exists.")

    print("\nDatabase seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
