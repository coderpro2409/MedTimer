import streamlit as st
from datetime import datetime, time
import random
import pandas as pd
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="MedTimer - Daily Medicine Companion",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for amazing elderly-friendly interface
st.markdown("""
    <style>
    /* Animated gradient background */
    .main {
        background: linear-gradient(-45deg, #e3f2fd, #e8f5e9, #f3e5f5, #fff9c4);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Button styling */
    .stButton>button {
        font-size: 26px !important;
        padding: 22px 45px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        width: 100%;
        border: none !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%) !important;
        color: white !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.3) !important;
    }
    
    /* Typography */
    h1 {
        font-size: 58px !important;
        color: #1565c0;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px !important;
    }
    
    h2 {
        font-size: 42px !important;
        color: #1976d2;
        font-weight: 700 !important;
        margin-top: 20px !important;
    }
    
    h3 {
        font-size: 32px !important;
        color: #1e88e5;
        font-weight: 600 !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stTimeInput>div>div>input {
        font-size: 24px !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 3px solid #90caf9 !important;
        background-color: white !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Medicine cards */
    .medicine-card {
        background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: 20px 0;
        border-left: 8px solid #42a5f5;
        transition: all 0.3s ease;
    }
    
    .medicine-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    /* Status badges */
    .taken-badge {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 15px;
        font-size: 24px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    
    .upcoming-badge {
        background: linear-gradient(135deg, #ffb74d 0%, #ffa726 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 15px;
        font-size: 24px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    .missed-badge {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 15px;
        font-size: 24px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        animation: blink 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Congratulations styling */
    .congrats-container {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        padding: 50px;
        border-radius: 30px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(255,215,0,0.4);
        animation: celebrate 1s ease-in-out;
    }
    
    @keyframes celebrate {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .congrats-text {
        font-size: 52px;
        color: #f57c00;
        font-weight: 900;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        animation: bounce 1s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Motivational quote box */
    .motivation-box {
        background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
        padding: 25px;
        border-radius: 20px;
        border-left: 8px solid #66bb6a;
        margin: 20px 0;
        font-size: 24px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #42a5f5 0%, #1e88e5 100%);
        height: 35px !important;
        border-radius: 15px;
    }
    
    /* Big text */
    .big-text {
        font-size: 26px;
        line-height: 1.8;
        color: #424242;
    }
    
    /* Header box */
    .header-box {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        padding: 35px;
        border-radius: 25px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Adherence score box */
    .adherence-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin: 20px 0;
    }
    
    .adherence-score {
        font-size: 72px;
        font-weight: 900;
        color: #1565c0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'setup'
if 'medicines' not in st.session_state:
    st.session_state.medicines = []
if 'medicine_log' not in st.session_state:
    st.session_state.medicine_log = []

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "💪 Every dose you take is a step toward better health!",
    "🌟 You're doing great! Keep taking care of yourself!",
    "❤️ Your health is your wealth. Stay consistent!",
    "🎯 Small steps every day lead to big health wins!",
    "🌈 Taking your medicine shows you care about yourself!",
    "✨ You're building a healthy habit, one day at a time!",
    "🌺 Your dedication to health is inspiring!",
    "🎊 Celebrate every dose - you're doing amazing!"
]

# Setup Page
def setup_page():
    st.markdown('<div class="header-box"><h1 style="color: white; margin: 0;">💊 MedTimer - Daily Medicine Companion</h1><p style="font-size: 26px; margin: 10px 0 0 0;">Setup your personalized medicine schedule</p></div>', unsafe_allow_html=True)
    
    # Motivational quote
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.markdown(f'<div class="motivation-box">{quote}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 💊 Add Your Medicine")
        med_name = st.text_input("Medicine Name", placeholder="e.g., Aspirin 100mg", key="med_name")
        med_time = st.time_input("Time to Take", value=time(9, 0), key="med_time")
        
        st.markdown("### 📝 Additional Details (Optional)")
        med_dosage = st.text_input("Dosage", placeholder="e.g., 1 tablet", key="med_dosage")
        med_notes = st.text_area("Special Instructions", 
                                 placeholder="e.g., Take with food, After breakfast", 
                                 key="med_notes", height=100)
    
    with col2:
        st.markdown("### 📋 Your Medicine List")
        
        if st.session_state.medicines:
            for idx, med in enumerate(st.session_state.medicines):
                st.markdown(f"""
                <div class="medicine-card">
                    <h3>💊 {med['name']}</h3>
                    <p class="big-text"><strong>⏰ Time:</strong> {med['time'].strftime('%I:%M %p')}</p>
                    {f"<p class='big-text'><strong>💊 Dosage:</strong> {med['dosage']}</p>" if med.get('dosage') else ""}
                    {f"<p class='big-text'><strong>📝 Notes:</strong> {med['notes']}</p>" if med.get('notes') else ""}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑️ Remove {med['name']}", key=f"remove_{idx}"):
                    st.session_state.medicines.pop(idx)
                    st.rerun()
        else:
            st.info("👆 No medicines added yet. Add your first medicine!")
    
    st.markdown("---")
    
    col_add, col_continue = st.columns([1, 1])
    
    with col_add:
        if st.button("➕ Add Medicine", use_container_width=True):
            if med_name:
                medicine = {
                    'name': med_name,
                    'time': med_time,
                    'dosage': med_dosage if med_dosage else "",
                    'notes': med_notes if med_notes else ""
                }
                st.session_state.medicines.append(medicine)
                st.success(f"✓ Added {med_name}!")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Please enter medicine name")
    
    with col_continue:
        if st.session_state.medicines:
            if st.button("➡️ Continue to Tracker", use_container_width=True):
                st.session_state.page = 'main'
                st.rerun()
        else:
            st.button("➡️ Continue to Tracker", use_container_width=True, disabled=True)

# Function to get medicine status
def get_medicine_status(med_time, taken_today):
    current_time = datetime.now().time()
    
    if taken_today:
        return "taken", "✅ Taken"
    
    # Calculate time difference
    med_datetime = datetime.combine(datetime.today(), med_time)
    current_datetime = datetime.now()
    
    time_diff = (med_datetime - current_datetime).total_seconds() / 60  # in minutes
    
    if time_diff < -30:  # More than 30 minutes past scheduled time
        return "missed", "❌ Missed"
    elif time_diff > 0:  # Upcoming
        return "upcoming", "⏰ Upcoming"
    else:  # Within 30 minutes window
        return "upcoming", "⏰ Time to Take"

# Function to calculate adherence score based on timely taken medicines (per session)
def calculate_adherence():
    if not st.session_state.medicines:
        return 0
    
    if not st.session_state.medicine_log:
        return 0
    
    timely_taken = 0
    total_logged = len(st.session_state.medicines)
    
    # Check each logged medicine
    for log in st.session_state.medicine_log:
        # Find the corresponding medicine schedule
        scheduled_med = next((med for med in st.session_state.medicines 
                            if med['name'] == log['medicine']), None)
        
        if scheduled_med:
            # Calculate time difference
            scheduled_datetime = datetime.combine(log['date'], scheduled_med['time'])
            taken_datetime = datetime.combine(log['date'], log['time'])
            time_diff_minutes = (taken_datetime - scheduled_datetime).total_seconds() / 60
            
            # Count as timely if:
            # - Taken anytime BEFORE scheduled time (negative difference)
            # - Within 30 minutes AFTER scheduled time (0 to +30 minutes)
            if time_diff_minutes <= 30:
                timely_taken += 1
    
    # Adherence = (timely taken / total logged) * 100
    return int((timely_taken / total_logged * 100)) if total_logged > 0 else 0

# Congratulations Page
def congratulations_page():
    st.markdown('<div class="congrats-container">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 100px;">🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="congrats-text">Excellent Work!</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #f57c00; margin: 20px 0;">You\'ve taken all your medicines today!</h2>', unsafe_allow_html=True)
    
    # Show adherence score
    adherence = calculate_adherence()
    st.markdown(f'''
    <div class="adherence-box">
        <h3 style="color: #1565c0; margin: 0;">Session Adherence Score</h3>
        <div class="adherence-score">{adherence}%</div>
        <p style="font-size: 20px; color: #424242; margin: 10px 0 0 0;">Timely / Total medicines taken</p>
        <p style="font-size: 18px; color: #666; margin: 5px 0 0 0;">✅ Before or within 30 min after scheduled time</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Motivational message based on adherence
    if adherence >= 90:
        message = "🏆 Outstanding! You're a health champion!"
    elif adherence >= 75:
        message = "💪 Great job! You're doing really well!"
    elif adherence >= 60:
        message = "👍 Good effort! Keep improving!"
    else:
        message = "🌟 Every step counts! Keep trying!"
    
    st.markdown(f'<div class="motivation-box" style="text-align: center; font-size: 28px;">{message}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    # with col2:
    #     if st.button("🏠 Return to Tracker", use_container_width=True):
    #         st.session_state.page = 'main'
    #         st.rerun()
    if st.session_state.medicine_log:
        df = pd.DataFrame(st.session_state.medicine_log)
        df['Date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df['Time'] = df['time'].apply(lambda x: x.strftime('%I:%M %p'))
        
        # Create Excel file in memory
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Medicine Report')
        buffer.seek(0)
        
        st.download_button(
            label="📄 Download Excel Report",
            data=buffer,
            file_name=f"medtimer_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No data to download yet!")
    # Show today's completed schedule
    st.markdown("---")
    st.markdown("### ✅ Today's Completed Schedule")
    
    current_time = datetime.now()
    today_logs = [log for log in st.session_state.medicine_log 
                  if log['date'] == current_time.date()]
    
    for log in sorted(today_logs, key=lambda x: x['time']):
        st.markdown(f"""
        <div class="medicine-card">
            <h3>💊 {log['medicine']}</h3>
            <p class="big-text">✅ Taken at: {log['time'].strftime('%I:%M %p')}</p>
        </div>
        """, unsafe_allow_html=True)

# Main Page
def main_page():
    current_time = datetime.now()
    
    # Check if all medicines are taken
    # Check if all medicines are taken (must match both name and scheduled time)
    taken_today = [(log['medicine'], log.get('scheduled_time')) for log in st.session_state.medicine_log 
                if log['date'] == current_time.date()]
    all_taken = all((med['name'], med['time']) in taken_today for med in st.session_state.medicines)

    
    if all_taken and st.session_state.medicines:
        st.session_state.page = 'congrats'
        st.rerun()
    
    # Header
    st.markdown(f'''
    <div class="header-box">
        <h1 style="color: white; margin: 0;">💊 MedTimer - Today's Schedule</h1>
        <p style="font-size: 28px; margin: 10px 0 0 0;">📅 {current_time.strftime('%A, %B %d, %Y')} | ⏰ {current_time.strftime('%I:%M %p')}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Motivational quote
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.markdown(f'<div class="motivation-box">{quote}</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📊 Session Progress")
        
        # Calculate adherence
        adherence = calculate_adherence()
        
        st.markdown(f'''
        <div class="adherence-box">
            <h3 style="color: #1565c0; margin: 0;">Adherence Score</h3>
            <div class="adherence-score">{adherence}%</div>
            <p style="font-size: 18px; color: #666; margin: 5px 0 0 0;">Timely taken medicines</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.progress(adherence / 100)
        
        # Session statistics
        st.markdown("---")
        st.markdown("### 📈 Session Statistics")
        
        # Count timely and late doses
        timely_count = 0
        late_count = 0
        
        for log in st.session_state.medicine_log:
            scheduled_med = next((med for med in st.session_state.medicines 
                                if med['name'] == log['medicine']), None)
            if scheduled_med:
                scheduled_time = datetime.combine(log['date'], scheduled_med['time'])
                taken_time = datetime.combine(log['date'], log['time'])
                time_diff = (taken_time - scheduled_time).total_seconds() / 60
                
                if time_diff <= 30:
                    timely_count += 1
                else:
                    late_count += 1
        
        total_logged = timely_count + late_count
        
        if total_logged > 0:
            st.markdown(f"<h3 style='color: #1565c0;'>Total: {total_logged}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p class='big-text'>✅ Timely: {timely_count}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='big-text'>⏰ Late: {late_count}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='big-text'>No doses logged yet</p>", unsafe_allow_html=True)
        
        # Today's progress
        st.markdown("---")
        st.markdown("### 📅 Today's Progress")
        taken_count = len(taken_today)
        total_count = len(st.session_state.medicines)
        st.markdown(f"<h2 style='color: #1565c0;'>{taken_count} / {total_count}</h2>", unsafe_allow_html=True)
        st.progress(taken_count / total_count if total_count > 0 else 0)
        
        if taken_count == total_count and total_count > 0:
            st.markdown("### 🎉 All Done Today!")
        elif taken_count > 0:
            st.markdown(f"### 💪 {total_count - taken_count} remaining")
        
        st.markdown("---")
        st.markdown("## 🔧 Menu")
        if st.button("⚙️ Edit Medicines", use_container_width=True):
            st.session_state.page = 'setup'
            st.rerun()
        
        # if st.button("📥 Download Report", use_container_width=True):
            # Generate report
        if st.session_state.medicine_log:
            df = pd.DataFrame(st.session_state.medicine_log)
            df['Date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df['Time'] = df['time'].apply(lambda x: x.strftime('%I:%M %p'))
            
            # Create Excel file in memory
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Medicine Report')
            buffer.seek(0)
            
            st.download_button(
                label="📄 Download Excel Report",
                data=buffer,
                file_name=f"medtimer_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No data to download yet!")
    
    # Medicine Schedule
    st.markdown("## 💊 Today's Medicine Checklist")
    
    for idx, med in enumerate(sorted(st.session_state.medicines, key=lambda x: x['time'])):
        col1, col2 = st.columns([3, 1])
        
        # Check if medicine was taken
        taken_today_med = any(
            log['medicine'] == med['name'] and 
            log['date'] == current_time.date() and
            log['scheduled_time'] == med['time']
            for log in st.session_state.medicine_log
        )
        
        status, status_text = get_medicine_status(med['time'], taken_today_med)
        
        with col1:
            # Color coding based on status
            if status == "taken":
                border_color = "#66bb6a"
                bg_gradient = "linear-gradient(135deg, #ffffff 0%, #c8e6c9 100%)"
            elif status == "missed":
                border_color = "#ef5350"
                bg_gradient = "linear-gradient(135deg, #ffffff 0%, #ffcdd2 100%)"
            else:
                border_color = "#ffb74d"
                bg_gradient = "linear-gradient(135deg, #ffffff 0%, #fff9c4 100%)"
            
            st.markdown(f"""
            <div class="medicine-card" style="border-left: 8px solid {border_color}; background: {bg_gradient};">
                <h2 style="margin: 0;">💊 {med['name']}</h2>
                <p class="big-text" style="margin: 10px 0;"><strong>⏰ Scheduled Time:</strong> {med['time'].strftime('%I:%M %p')}</p>
                {f"<p class='big-text' style='margin: 5px 0;'><strong>💊 Dosage:</strong> {med['dosage']}</p>" if med.get('dosage') else ""}
                {f"<p class='big-text' style='margin: 5px 0;'><strong>📝 Notes:</strong> {med['notes']}</p>" if med.get('notes') else ""}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            if status == "taken":
                st.markdown('<div class="taken-badge">✅ Taken</div>', unsafe_allow_html=True)
                for log in st.session_state.medicine_log:
                    if (log['medicine'] == med['name'] and 
                        log['date'] == current_time.date() and
                        log['scheduled_time'] == med['time']):  # ADD scheduled_time check
                        st.markdown(f"<p class='big-text' style='text-align: center; margin-top: 10px;'>at {log['time'].strftime('%I:%M %p')}</p>", 
                                unsafe_allow_html=True)
                        break
            elif status == "missed":
                st.markdown('<div class="missed-badge">❌ Missed</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"✓ Mark as Taken", key=f"mark_{idx}", use_container_width=True):
                    st.session_state.medicine_log.append({
                        'medicine': med['name'],
                        'date': current_time.date(),
                        'time': current_time.time(),
                        'scheduled_time': med['time'],
                        'timestamp': current_time
                    })
                    st.success(f"✓ Marked {med['name']} as taken!")
                    st.balloons()
                    st.rerun()
            else:
                st.markdown('<div class="upcoming-badge">⏰ Upcoming</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"✓ Mark as Taken", key=f"mark_{idx}", use_container_width=True):
                    st.session_state.medicine_log.append({
                        'medicine': med['name'],
                        'date': current_time.date(),
                        'time': current_time.time(),
                        'scheduled_time': med['time'],
                        'timestamp': current_time
                    })
                    st.success(f"✓ Marked {med['name']} as taken!")
                    st.balloons()
                    st.rerun()
    
    st.markdown("---")
    
    # Medicine Log History
    if st.session_state.medicine_log:
        st.markdown("## 📜 Medicine History (Current Session)")
        
        if st.session_state.medicine_log:
            df = pd.DataFrame(st.session_state.medicine_log)
            df['Date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df['Time'] = df['time'].apply(lambda x: x.strftime('%I:%M %p'))
            
            # Add status column
            statuses = []
            for idx, row in df.iterrows():
                log = st.session_state.medicine_log[idx]
                scheduled_med = next((med for med in st.session_state.medicines 
                                    if med['name'] == log['medicine']), None)
                if scheduled_med:
                    scheduled_time = datetime.combine(log['date'], scheduled_med['time'])
                    taken_time = datetime.combine(log['date'], log['time'])
                    time_diff = (taken_time - scheduled_time).total_seconds() / 60
                    
                    if time_diff < 0:
                        statuses.append("✅ Early")
                    elif time_diff <= 30:
                        statuses.append("✅ On Time")
                    else:
                        statuses.append("⏰ Late")
                else:
                    statuses.append("N/A")
            
            df['Status'] = statuses
            df = df[['Date', 'Time', 'medicine', 'Status']].rename(columns={'medicine': 'Medicine'})
            
            st.dataframe(df, use_container_width=True, height=300)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Clear History", use_container_width=True):
                    st.session_state.medicine_log = []
                    st.rerun()
        else:
            st.info("📝 No medicine history in current session")

# Main app logic
if st.session_state.page == 'setup':
    setup_page()
elif st.session_state.page == 'congrats':
    congratulations_page()
else:
    main_page()