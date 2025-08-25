import streamlit as st
import random
import time

# Configure page
st.set_page_config(
    page_title="Epic Quest RPG",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 50%, #2d1b69 100%);
        color: white;
    }
    
    /* Title styling */
    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #c9c9c9;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Card styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Character stats */
    .stat-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-label {
        font-weight: 500;
        color: #e0e0e0;
        font-size: 1rem;
    }
    
    .stat-value {
        font-weight: 600;
        color: #ffd700;
        font-size: 1.2rem;
    }
    
    /* Quest styling */
    .quest-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .quest-completed {
        border-color: #4caf50 !important;
        background: rgba(76, 175, 80, 0.1) !important;
    }
    
    .quest-name {
        font-weight: 600;
        font-size: 1.1rem;
        color: #fff;
        margin-bottom: 8px;
    }
    
    .quest-progress {
        color: #c9c9c9;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    .quest-reward {
        color: #ffd700;
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Activity log */
    .activity-log {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-height: 300px;
        overflow-y: auto;
    }
    
    .log-entry {
        padding: 10px 15px;
        margin-bottom: 8px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #ffd700;
    }
    
    .log-level-up {
        border-left-color: #4caf50 !important;
        background: rgba(76, 175, 80, 0.1) !important;
    }
    
    .log-quest-complete {
        border-left-color: #2196f3 !important;
        background: rgba(33, 150, 243, 0.1) !important;
    }
    
    /* Progress bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 20px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Metric styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #ffd700;
    }
</style>
""", unsafe_allow_html=True)

# Quest class
class Quest:
    def __init__(self, name, qtype, target, reward):
        self.name = name
        self.qtype = qtype
        self.target = target
        self.progress = 0
        self.reward = reward
        self.done = False
    
    def update(self):
        if not self.done:
            self.progress += 1
            if self.progress >= self.target:
                self.done = True
                return True
        return False
    
    def get_status(self):
        return f"{self.name} ({self.qtype}): {self.progress}/{self.target} - {'Done' if self.done else 'In Progress'}"

# Character class
class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.items = 0
        self.kills = 0
    
    def gain_exp(self, amount):
        self.exp += amount
        exp_needed = self.level * 10
        if self.exp >= exp_needed:
            self.level += 1
            self.exp = 0
            return True  # Level up occurred
        return False

# Generate random quest
def generate_random_quest(player_level):
    qtype = random.choice(["kill", "collect"])
    target = random.randint(1, player_level + 2)
    
    if qtype == "kill":
        return Quest(f"Defeat {target} Enemies", "kill", target, 5 * player_level)
    else:
        return Quest(f"Collect {target} Items", "collect", target, 4 * player_level)

# Initialize session state
def init_session_state():
    if 'player' not in st.session_state:
        st.session_state.player = None
    if 'quests' not in st.session_state:
        st.session_state.quests = []
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = []
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

# Add log entry
def add_log(message, log_type="normal"):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.activity_log.insert(0, {
        'message': message,
        'type': log_type,
        'time': timestamp
    })
    # Keep only last 50 entries
    if len(st.session_state.activity_log) > 50:
        st.session_state.activity_log = st.session_state.activity_log[:50]

# Main app
def main():
    init_session_state()
    
    # Title
    st.markdown('<h1 class="main-title">⚔️ Epic Quest RPG ⚔️</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Master of Adventures and Legendary Quests</p>', unsafe_allow_html=True)
    
    # Character creation or game interface
    if not st.session_state.game_started:
        show_character_creation()
    else:
        show_game_interface()

def show_character_creation():
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 🌟 Create Your Character")
        
        character_name = st.text_input(
            "Enter your character name:",
            placeholder="Enter your epic hero name...",
            max_chars=20
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Begin Your Quest", use_container_width=True):
            if character_name.strip():
                st.session_state.player = Character(character_name.strip())
                st.session_state.quests = [generate_random_quest(1)]
                st.session_state.game_started = True
                add_log(f"Welcome to the adventure, {character_name}!")
                add_log(f"New Quest Added: {st.session_state.quests[0].name}")
                st.rerun()
            else:
                st.error("Please enter a character name!")

def show_game_interface():
    player = st.session_state.player
    
    # Sidebar with character info
    with st.sidebar:
        st.markdown("### ⚔️ Character Status")
        
        # Character stats in attractive format
        st.markdown(f"""
        <div class="metric-container">
            <div class="stat-label">Hero Name</div>
            <div class="stat-value">{player.name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="stat-label">Level</div>
            <div class="stat-value">{player.level}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Experience with progress bar
        exp_needed = player.level * 10
        exp_progress = (player.exp / exp_needed) * 100
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="stat-label">Experience</div>
            <div class="stat-value">{player.exp} / {exp_needed}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(exp_progress / 100)
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="stat-label">Items Collected</div>
            <div class="stat-value">{player.items}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="stat-label">Enemies Defeated</div>
            <div class="stat-value">{player.kills}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # New character button
        if st.button("🔄 New Character"):
            st.session_state.clear()
            st.rerun()
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Action buttons
        st.markdown("### 🎮 Actions")
        
        button_col1, button_col2, button_col3, button_col4 = st.columns(4)
        
        with button_col1:
            if st.button("⚔️ Fight Enemy", use_container_width=True):
                fight_action()
        
        with button_col2:
            if st.button("💎 Collect Item", use_container_width=True):
                collect_action()
        
        with button_col3:
            if st.button("📜 New Quest", use_container_width=True):
                generate_new_quest()
        
        with button_col4:
            if st.button("📋 View All Quests", use_container_width=True):
                show_all_quests()
        
        # Active quests
        st.markdown("### 📜 Active Quests")
        show_quests()
    
    with col2:
        # Activity log
        st.markdown("### 📖 Activity Log")
        show_activity_log()

def fight_action():
    player = st.session_state.player
    player.kills += 1
    
    # Gain experience
    level_up = player.gain_exp(2)
    
    add_log("⚔️ You fought an enemy!")
    add_log(f"💫 {player.name} gained 2 XP! Total XP: {player.exp}")
    
    if level_up:
        add_log(f"🎉 LEVEL UP! {player.name} is now Level {player.level}", "level_up")
    
    # Update kill quests
    for quest in st.session_state.quests:
        if quest.qtype == "kill" and not quest.done:
            if quest.update():
                quest_level_up = player.gain_exp(quest.reward)
                add_log(f"✅ Quest Completed: {quest.name}", "quest_complete")
                add_log(f"💫 Gained {quest.reward} bonus XP!")
                if quest_level_up:
                    add_log(f"🎉 LEVEL UP! {player.name} is now Level {player.level}", "level_up")
    
    st.rerun()

def collect_action():
    player = st.session_state.player
    player.items += 1
    
    # Gain experience
    level_up = player.gain_exp(1)
    
    add_log("💎 You found an item!")
    add_log(f"💫 {player.name} gained 1 XP! Total XP: {player.exp}")
    
    if level_up:
        add_log(f"🎉 LEVEL UP! {player.name} is now Level {player.level}", "level_up")
    
    # Update collect quests
    for quest in st.session_state.quests:
        if quest.qtype == "collect" and not quest.done:
            if quest.update():
                quest_level_up = player.gain_exp(quest.reward)
                add_log(f"✅ Quest Completed: {quest.name}", "quest_complete")
                add_log(f"💫 Gained {quest.reward} bonus XP!")
                if quest_level_up:
                    add_log(f"🎉 LEVEL UP! {player.name} is now Level {player.level}", "level_up")
    
    st.rerun()

def generate_new_quest():
    player = st.session_state.player
    new_quest = generate_random_quest(player.level)
    st.session_state.quests.append(new_quest)
    add_log(f"📜 New Quest Added: {new_quest.name}")
    st.rerun()

def show_all_quests():
    if not st.session_state.quests:
        add_log("📋 No active quests. Generate a new quest to continue!")
    else:
        add_log("📋 === Current Quests ===")
        for quest in st.session_state.quests:
            status = "✅" if quest.done else "🔄"
            add_log(f"{status} {quest.get_status()}")

def show_quests():
    if not st.session_state.quests:
        st.info("🎯 No active quests. Generate a new quest to start your adventure!")
        return
    
    for i, quest in enumerate(st.session_state.quests):
        quest_class = "quest-completed" if quest.done else ""
        progress_percent = (quest.progress / quest.target) * 100
        
        st.markdown(f"""
        <div class="quest-card {quest_class}">
            <div class="quest-name">{'✅' if quest.done else '🔄'} {quest.name}</div>
            <div class="quest-progress">Progress: {quest.progress}/{quest.target} ({progress_percent:.0f}%)</div>
            <div class="quest-reward">💰 Reward: {quest.reward} XP</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar for active quests
        if not quest.done:
            st.progress(progress_percent / 100)

def show_activity_log():
    if not st.session_state.activity_log:
        st.info("🔍 Activity log is empty. Start your adventure!")
        return
    
    # Create scrollable container
    log_html = '<div class="activity-log">'
    
    for entry in st.session_state.activity_log[:10]:  # Show last 10 entries
        log_class = ""
        if entry['type'] == "level_up":
            log_class = "log-level-up"
        elif entry['type'] == "quest_complete":
            log_class = "log-quest-complete"
        
        log_html += f'''
        <div class="log-entry {log_class}">
            <small>[{entry['time']}]</small><br>
            {entry['message']}
        </div>
        '''
    
    log_html += '</div>'
    st.markdown(log_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
