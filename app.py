import streamlit as st
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
from orchestrator import GeminiOrchestrator

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner - Agentic System",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'ai_recommendations' not in st.session_state:
    st.session_state.ai_recommendations = {}

# Initialize AI Orchestrator
def init_orchestrator():
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key and not st.session_state.orchestrator:
        try:
            st.session_state.orchestrator = GeminiOrchestrator(api_key)
            st.session_state.orchestrator.start_session()
            return True
        except Exception as e:
            st.error(f"Failed to initialize AI: {str(e)}")
            return False
    return st.session_state.orchestrator is not None

# Main title
st.title("🤖 AI Travel Planner - Agentic System")
st.markdown("**Powered by Multi-Agent AI & Google Gemini** - Your intelligent travel companion")

# API Key setup in sidebar
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key_input = st.text_input("Google Gemini API Key", type="password", 
                                   value=os.getenv('GEMINI_API_KEY', ''),
                                   help="Enter your Gemini API key to enable AI features")
    
    if api_key_input:
        os.environ['GEMINI_API_KEY'] = api_key_input
        if st.button("Initialize AI System"):
            if init_orchestrator():
                st.success("✅ AI System Initialized!")
            else:
                st.error("❌ Failed to initialize AI")
    
    st.divider()
    
    # Show agent status
    if st.session_state.orchestrator:
        st.success("🟢 AI Agents Active")
        with st.expander("Active Agents"):
            st.write("🧠 Planning Agent")
            st.write("✈️ Travel Agent")
            st.write("💰 Finance Agent")
            st.write("🔍 Search Agent")
    else:
        st.warning("🔴 AI Agents Offline")
        st.info("Enter API key to activate AI features")

st.markdown("Plan your perfect trip with ease!")

# Sidebar for trip details
with st.sidebar:
    st.header("📋 Trip Details")
    
    # Destination
    destination = st.text_input("Destination", placeholder="e.g., Paris, France")
    
    # Date selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now())
    with col2:
        end_date = st.date_input("End Date", datetime.now() + timedelta(days=7))
    
    # Calculate trip duration
    if end_date >= start_date:
        duration = (end_date - start_date).days + 1
        st.info(f"Trip Duration: {duration} days")
    else:
        st.error("End date must be after start date!")
        duration = 0
    
    # Number of travelers
    travelers = st.number_input("Number of Travelers", min_value=1, max_value=20, value=1)
    
    # Budget
    st.subheader("💰 Budget Planning")
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"])
    total_budget = st.number_input(f"Total Budget ({currency})", min_value=0.0, value=1000.0, step=100.0)
    
    if duration > 0:
        daily_budget = total_budget / duration
        st.metric("Daily Budget", f"{currency} {daily_budget:.2f}")

# Main content area
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🤖 AI Assistant", "📍 Itinerary", "💵 Budget", "✈️ Travel Search", "📦 Packing", "📝 Notes"])

# Tab 1: AI Assistant Chat
with tab1:
    st.header("AI Travel Assistant")
    st.markdown("Chat with AI agents to plan your trip. Ask about destinations, flights, hotels, budgets, and more!")
    
    if not st.session_state.orchestrator:
        st.warning("⚠️ Please initialize the AI system with your Gemini API key in the sidebar to use this feature.")
        st.info("""
        **What you can ask:**
        - "What are the top attractions in Paris?"
        - "Find me flights to Tokyo"
        - "Create a 5-day itinerary for Rome"
        - "What's my budget breakdown?"
        - "Suggest hotels in New York under $200/night"
        """)
    else:
        # Get current trip context
        trip_context = {
            'destination': destination if destination else '',
            'start_date': start_date.isoformat() if 'start_date' in locals() else '',
            'end_date': end_date.isoformat() if 'end_date' in locals() else '',
            'duration': duration if 'duration' in locals() else 0,
            'travelers': travelers if 'travelers' in locals() else 1,
            'budget': total_budget if 'total_budget' in locals() else 0,
            'currency': currency if 'currency' in locals() else 'USD'
        }
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(msg['user'])
            with st.chat_message("assistant"):
                st.write(msg['assistant'])
        
        # Chat input
        user_question = st.chat_input("Ask me anything about your trip...")
        
        if user_question:
            # Display user message
            with st.chat_message("user"):
                st.write(user_question)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("🤔 AI agents are working..."):
                    response = st.session_state.orchestrator.chat_with_user(user_question, trip_context)
                    st.write(response)
            
            # Save to history
            st.session_state.chat_history.append({
                'user': user_question,
                'assistant': response
            })
            st.rerun()
        
        # Quick action buttons
        st.divider()
        st.subheader("Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗺️ Generate Complete Itinerary", use_container_width=True):
                if destination:
                    with st.spinner("Creating your complete travel plan..."):
                        complete_plan = st.session_state.orchestrator.create_complete_itinerary(trip_context)
                        st.session_state.ai_recommendations['complete_plan'] = complete_plan
                        st.success("✅ Complete plan generated! Check the recommendations below.")
                        st.rerun()
                else:
                    st.warning("Please set a destination first!")
        
        with col2:
            if st.button("💡 Get Destination Tips", use_container_width=True):
                if destination:
                    with st.spinner("Gathering travel tips..."):
                        tips = st.session_state.orchestrator.get_recommendations('planning', trip_context)
                        st.session_state.ai_recommendations['tips'] = tips
                        st.rerun()
                else:
                    st.warning("Please set a destination first!")
        
        with col3:
            if st.button("💰 Budget Analysis", use_container_width=True):
                if total_budget > 0:
                    with st.spinner("Analyzing budget..."):
                        budget_advice = st.session_state.orchestrator.get_recommendations('finance', trip_context)
                        st.session_state.ai_recommendations['budget'] = budget_advice
                        st.rerun()
                else:
                    st.warning("Please set a budget first!")
        
        # Display AI recommendations
        if st.session_state.ai_recommendations:
            st.divider()
            st.subheader("📋 AI Recommendations")
            
            for key, value in st.session_state.ai_recommendations.items():
                if key == 'complete_plan':
                    with st.expander("🗺️ Complete Travel Plan", expanded=True):
                        if isinstance(value, dict):
                            st.markdown(f"**Itinerary:**\n{value.get('itinerary', '')}")
                            st.divider()
                            st.markdown(f"**Travel Options:**\n{value.get('travel_options', '')}")
                            st.divider()
                            st.markdown(f"**Accommodation:**\n{value.get('accommodation', '')}")
                            st.divider()
                            st.markdown(f"**Budget Plan:**\n{value.get('budget_plan', '')}")
                elif key == 'tips':
                    with st.expander("💡 Destination Tips & Recommendations"):
                        st.markdown(value)
                elif key == 'budget':
                    with st.expander("💰 Budget Analysis & Tips"):
                        st.markdown(value)

# Tab 2: Itinerary Builder (keeping original functionality)
with tab2:
    st.header("Daily Itinerary")
    
    if destination:
        # Add activity form
        with st.expander("➕ Add New Activity", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                activity_day = st.selectbox("Day", range(1, duration + 1) if duration > 0 else [1])
                activity_name = st.text_input("Activity Name", placeholder="e.g., Visit Eiffel Tower")
            with col2:
                activity_time = st.time_input("Time")
                activity_cost = st.number_input(f"Cost ({currency})", min_value=0.0, step=10.0)
            
            activity_notes = st.text_area("Notes", placeholder="Additional details...")
            
            if st.button("Add Activity", type="primary"):
                if activity_name:
                    st.session_state.itinerary.append({
                        'day': activity_day,
                        'time': activity_time.strftime("%H:%M"),
                        'name': activity_name,
                        'cost': activity_cost,
                        'notes': activity_notes
                    })
                    st.success(f"Added: {activity_name}")
                    st.rerun()
                else:
                    st.warning("Please enter an activity name!")
        
        # Display itinerary
        if st.session_state.itinerary:
            st.divider()
            
            # Sort by day and time
            sorted_itinerary = sorted(st.session_state.itinerary, key=lambda x: (x['day'], x['time']))
            
            current_day = None
            for idx, activity in enumerate(sorted_itinerary):
                if activity['day'] != current_day:
                    current_day = activity['day']
                    st.subheader(f"Day {current_day}")
                
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{activity['time']}** - {activity['name']}")
                    if activity['notes']:
                        st.caption(activity['notes'])
                with col2:
                    st.markdown(f"💰 {currency} {activity['cost']:.2f}")
                with col3:
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.itinerary.pop(idx)
                        st.rerun()
            
            # Clear all button
            st.divider()
            if st.button("Clear All Activities", type="secondary"):
                st.session_state.itinerary = []
                st.rerun()
        else:
            st.info("No activities added yet. Add your first activity above!")
    else:
        st.warning("Please enter a destination in the sidebar to start planning!")

# Tab 3: Budget Breakdown
with tab3:
    st.header("Budget Analysis")
    
    if destination and total_budget > 0:
        # Calculate spent amount
        total_spent = sum(activity['cost'] for activity in st.session_state.itinerary)
        remaining = total_budget - total_spent
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budget", f"{currency} {total_budget:.2f}")
        with col2:
            st.metric("Spent", f"{currency} {total_spent:.2f}", 
                     delta=f"-{(total_spent/total_budget*100):.1f}%" if total_budget > 0 else "0%")
        with col3:
            st.metric("Remaining", f"{currency} {remaining:.2f}",
                     delta=f"{(remaining/total_budget*100):.1f}%" if total_budget > 0 else "0%")
        
        # Progress bar
        if total_budget > 0:
            progress = min(total_spent / total_budget, 1.0)
            st.progress(progress)
            
            if remaining < 0:
                st.error(f"⚠️ Over budget by {currency} {abs(remaining):.2f}!")
            elif remaining < total_budget * 0.1:
                st.warning(f"⚠️ Less than 10% of budget remaining!")
        
        # Expense categories
        st.subheader("Expense Breakdown by Day")
        if st.session_state.itinerary:
            day_expenses = {}
            for activity in st.session_state.itinerary:
                day = activity['day']
                if day not in day_expenses:
                    day_expenses[day] = 0
                day_expenses[day] += activity['cost']
            
            for day in sorted(day_expenses.keys()):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"Day {day}")
                with col2:
                    st.write(f"{currency} {day_expenses[day]:.2f}")
        
        # Suggested categories
        st.divider()
        st.subheader("💡 Budget Allocation Suggestions")
        st.markdown(f"""
        - **Accommodation**: {currency} {total_budget * 0.35:.2f} (35%)
        - **Food**: {currency} {total_budget * 0.25:.2f} (25%)
        - **Activities**: {currency} {total_budget * 0.20:.2f} (20%)
        - **Transportation**: {currency} {total_budget * 0.15:.2f} (15%)
        - **Emergency Fund**: {currency} {total_budget * 0.05:.2f} (5%)
        """)
    else:
        st.info("Set your budget in the sidebar to see the breakdown!")

# Tab 4: Travel Search (New AI-powered search)
with tab4:
    st.header("✈️ AI-Powered Travel Search")
    
    if not st.session_state.orchestrator:
        st.warning("⚠️ Please initialize the AI system to use search features.")
    else:
        search_type = st.selectbox("What are you looking for?", 
                                   ["Flights", "Hotels", "Attractions", "Restaurants", "Activities"])
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search details", 
                                        placeholder=f"e.g., Cheap flights to Paris in December")
        with col2:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        
        if search_button and search_query:
            trip_context = {
                'destination': destination if destination else '',
                'start_date': start_date.isoformat() if 'start_date' in locals() else '',
                'end_date': end_date.isoformat() if 'end_date' in locals() else '',
                'duration': duration if 'duration' in locals() else 0,
                'travelers': travelers if 'travelers' in locals() else 1,
                'budget': total_budget if 'total_budget' in locals() else 0,
                'search_type': search_type.lower(),
                'query': search_query
            }
            
            with st.spinner(f"🔍 Searching for {search_type.lower()}..."):
                results = st.session_state.orchestrator.search_and_summarize(search_query, trip_context)
                
                st.subheader(f"Search Results: {search_type}")
                st.markdown(results)
        
        # Popular searches
        st.divider()
        st.subheader("💡 Popular Searches")
        
        if destination:
            quick_searches = [
                f"Best time to visit {destination}",
                f"Top 10 attractions in {destination}",
                f"Budget-friendly hotels in {destination}",
                f"Local food and restaurants in {destination}",
                f"Transportation options in {destination}"
            ]
            
            for search in quick_searches:
                if st.button(search, key=f"quick_{search}"):
                    trip_context = {
                        'destination': destination,
                        'query': search
                    }
                    with st.spinner("Searching..."):
                        results = st.session_state.orchestrator.search_and_summarize(search, trip_context)
                        st.markdown(results)

# Tab 5: Packing List
with tab5:
    st.header("Packing Checklist")
    
    if 'packing_list' not in st.session_state:
        st.session_state.packing_list = {
            'Essentials': ['Passport', 'Travel documents', 'Money/Credit cards', 'Phone & charger'],
            'Clothing': ['Shirts', 'Pants', 'Underwear', 'Socks', 'Shoes'],
            'Toiletries': ['Toothbrush', 'Toothpaste', 'Shampoo', 'Soap', 'Medications'],
            'Electronics': ['Camera', 'Laptop/Tablet', 'Adapters', 'Power bank']
        }
    
    for category, items in st.session_state.packing_list.items():
        with st.expander(f"📦 {category}", expanded=True):
            for item in items:
                st.checkbox(item, key=f"pack_{category}_{item}")

# Tab 6: Notes
with tab6:
    st.header("Trip Notes")
    
    if 'notes' not in st.session_state:
        st.session_state.notes = ""
    
    notes = st.text_area(
        "Write your notes here...",
        value=st.session_state.notes,
        height=300,
        placeholder="Important contacts, emergency numbers, special reminders, etc."
    )
    
    if st.button("Save Notes"):
        st.session_state.notes = notes
        st.success("Notes saved!")
    
    # Quick info section
    st.divider()
    st.subheader("📞 Important Reminders")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Before You Go:**
        - Check passport validity
        - Get travel insurance
        - Notify bank of travel
        - Check visa requirements
        """)
    with col2:
        st.markdown("""
        **During Trip:**
        - Keep copies of documents
        - Stay connected with family
        - Track your expenses
        - Take lots of photos!
        """)

# Footer
st.divider()
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    if destination:
        st.markdown(f"### Happy travels to **{destination}**! 🌍")
    else:
        st.markdown("### Start planning your adventure! ✨")
