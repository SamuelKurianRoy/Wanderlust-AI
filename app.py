import streamlit as st
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Travel Planner Helper",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []

# Main title
st.title("✈️ Travel Planner Helper")
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
tab1, tab2, tab3, tab4 = st.tabs(["📍 Itinerary", "💵 Budget Breakdown", "📦 Packing List", "📝 Notes"])

# Tab 1: Itinerary Builder
with tab1:
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

# Tab 2: Budget Breakdown
with tab2:
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

# Tab 3: Packing List
with tab3:
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

# Tab 4: Notes
with tab4:
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
