# Central configuration for the Study Planner app
import os

# --- Paths & Directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "study_planner.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

# --- Authentication Settings ---
# PBKDF2 hashing parameters
HASH_NAME = 'sha256'
ITERATIONS = 100_000
SALT_SIZE = 16  # bytes

# --- Revision Planner Settings ---
# Days before exam to schedule review sessions
REVISION_OFFSETS = [7, 5, 3, 1]

# --- Streamlit Configuration ---
PAGE_TITLE = "Study Planner"
PAGE_ICON = "📚"
LAYOUT = "centered"
INITIAL_SIDEBAR_STATE = "collapsed"