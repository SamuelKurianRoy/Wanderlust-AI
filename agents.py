"""
Multi-Agent System for Travel Planning
Defines base agent class and specialized agents for different tasks
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory = []
    
    @abstractmethod
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    def add_to_memory(self, interaction: Dict[str, Any]):
        """Store interaction in agent memory"""
        self.memory.append({
            'timestamp': datetime.now().isoformat(),
            'interaction': interaction
        })
    
    def get_memory(self) -> List[Dict[str, Any]]:
        """Retrieve agent memory"""
        return self.memory


class PlanningAgent(BaseAgent):
    """Agent responsible for destination planning and recommendations"""
    
    def __init__(self):
        super().__init__(
            name="Planning Agent",
            role="Destination research and itinerary planning"
        )
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process planning requests:
        - Find popular places in destination
        - Suggest activities and attractions
        - Create day-by-day itineraries
        """
        destination = context.get('destination', '')
        duration = context.get('duration', 1)
        interests = context.get('interests', [])
        
        result = {
            'agent': self.name,
            'task': task,
            'destination': destination,
            'duration': duration,
            'recommendations': [],
            'itinerary': {}
        }
        
        # This will be populated by search and AI
        self.add_to_memory({'task': task, 'context': context})
        
        return result
    
    def create_itinerary_prompt(self, context: Dict[str, Any]) -> str:
        """Generate prompt for AI to create itinerary"""
        destination = context.get('destination', '')
        duration = context.get('duration', 1)
        interests = context.get('interests', [])
        budget_level = context.get('budget_level', 'moderate')
        
        prompt = f"""As a travel planning expert, create a detailed {duration}-day itinerary for {destination}.

Traveler preferences:
- Duration: {duration} days
- Interests: {', '.join(interests) if interests else 'general sightseeing'}
- Budget level: {budget_level}

Please provide:
1. Top attractions and must-visit places
2. Day-by-day itinerary with activities
3. Estimated time for each activity
4. Best time to visit each location
5. Local tips and recommendations

Format the response as a structured itinerary."""
        
        return prompt


class TravelAgent(BaseAgent):
    """Agent responsible for transportation and accommodation"""
    
    def __init__(self):
        super().__init__(
            name="Travel Agent",
            role="Flights, hotels, and transportation management"
        )
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process travel logistics:
        - Find flights
        - Search hotels
        - Local transportation options
        """
        origin = context.get('origin', '')
        destination = context.get('destination', '')
        start_date = context.get('start_date', '')
        end_date = context.get('end_date', '')
        travelers = context.get('travelers', 1)
        
        result = {
            'agent': self.name,
            'task': task,
            'flights': [],
            'hotels': [],
            'transportation': []
        }
        
        self.add_to_memory({'task': task, 'context': context})
        
        return result
    
    def create_search_prompt(self, context: Dict[str, Any], search_type: str) -> str:
        """Generate prompt for travel search"""
        destination = context.get('destination', '')
        start_date = context.get('start_date', '')
        end_date = context.get('end_date', '')
        travelers = context.get('travelers', 1)
        budget = context.get('budget', 0)
        
        if search_type == 'flights':
            prompt = f"""Find flight options to {destination}:
- Departure date: {start_date}
- Return date: {end_date}
- Number of travelers: {travelers}
- Budget consideration: ${budget}

Provide flight recommendations with:
1. Airlines and routes
2. Approximate prices
3. Duration and connections
4. Best booking tips"""
            
        elif search_type == 'hotels':
            prompt = f"""Find accommodation options in {destination}:
- Check-in: {start_date}
- Check-out: {end_date}
- Guests: {travelers}
- Budget: ${budget}

Provide hotel recommendations with:
1. Hotel names and types
2. Location and proximity to attractions
3. Approximate prices per night
4. Amenities and ratings"""
            
        else:  # transportation
            prompt = f"""Provide local transportation options in {destination}:
- Duration: {start_date} to {end_date}

Include:
1. Public transportation (metro, bus, trains)
2. Taxi/rideshare options
3. Car rental recommendations
4. Walking/cycling options
5. Transportation passes and costs"""
        
        return prompt


class FinanceAgent(BaseAgent):
    """Agent responsible for budget management and cost optimization"""
    
    def __init__(self):
        super().__init__(
            name="Finance Agent",
            role="Budget planning and expense tracking"
        )
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process financial tasks:
        - Budget allocation
        - Cost estimates
        - Money-saving tips
        """
        budget = context.get('budget', 0)
        destination = context.get('destination', '')
        duration = context.get('duration', 1)
        travelers = context.get('travelers', 1)
        
        result = {
            'agent': self.name,
            'task': task,
            'budget_breakdown': self.calculate_budget_breakdown(budget),
            'daily_budget': budget / duration if duration > 0 else 0,
            'tips': []
        }
        
        self.add_to_memory({'task': task, 'context': context})
        
        return result
    
    def calculate_budget_breakdown(self, total_budget: float) -> Dict[str, float]:
        """Calculate recommended budget allocation"""
        return {
            'accommodation': total_budget * 0.35,
            'food': total_budget * 0.25,
            'activities': total_budget * 0.20,
            'transportation': total_budget * 0.15,
            'emergency': total_budget * 0.05
        }
    
    def create_finance_prompt(self, context: Dict[str, Any]) -> str:
        """Generate prompt for financial advice"""
        destination = context.get('destination', '')
        budget = context.get('budget', 0)
        duration = context.get('duration', 1)
        travelers = context.get('travelers', 1)
        
        prompt = f"""As a travel finance expert, provide budget guidance for a trip to {destination}:

Trip details:
- Total budget: ${budget}
- Duration: {duration} days
- Number of travelers: {travelers}
- Daily budget: ${budget/duration if duration > 0 else 0}

Please provide:
1. Detailed budget breakdown by category
2. Cost-saving tips specific to {destination}
3. Hidden costs to watch out for
4. Best ways to save money on this trip
5. Recommended emergency fund
6. Currency exchange tips
7. Payment methods and cards to use

Be specific and practical."""
        
        return prompt


class SearchAgent(BaseAgent):
    """Agent responsible for web searches and information gathering"""
    
    def __init__(self):
        super().__init__(
            name="Search Agent",
            role="Web search and information retrieval"
        )
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process search requests:
        - Web search for places
        - Flight information
        - Hotel searches
        - Activity recommendations
        """
        query = context.get('query', task)
        search_type = context.get('search_type', 'general')
        
        result = {
            'agent': self.name,
            'task': task,
            'query': query,
            'search_type': search_type,
            'results': []
        }
        
        self.add_to_memory({'task': task, 'context': context})
        
        return result
    
    def create_search_query(self, context: Dict[str, Any]) -> str:
        """Generate optimized search query"""
        destination = context.get('destination', '')
        search_type = context.get('search_type', 'general')
        
        if search_type == 'attractions':
            return f"top attractions and things to do in {destination}"
        elif search_type == 'flights':
            return f"flights to {destination} prices and airlines"
        elif search_type == 'hotels':
            return f"best hotels in {destination} reviews and prices"
        elif search_type == 'restaurants':
            return f"best restaurants and food in {destination}"
        elif search_type == 'activities':
            return f"popular activities and experiences in {destination}"
        else:
            return f"travel guide {destination}"
