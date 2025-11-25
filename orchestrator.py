"""
Gemini Orchestrator - Bridge between human and AI agents
Coordinates multiple agents and processes natural language requests
"""

import google.generativeai as genai
from typing import Dict, Any, List, Optional
import json
from agents import PlanningAgent, TravelAgent, FinanceAgent, SearchAgent


class GeminiOrchestrator:
    """
    Main orchestrator using Google Gemini to coordinate between agents
    Acts as the bridge between human language and agent actions
    """
    
    def __init__(self, api_key: str):
        """Initialize Gemini orchestrator"""
        genai.configure(api_key=api_key)
        
        # Use stable, reliable models from the available list
        # Prioritize stable versions over experimental/preview
        model_names_to_try = [
            'gemini-2.5-flash',           # Stable, fast, recommended for most use cases
            'gemini-2.0-flash-001',       # Stable Gemini 2.0 Flash
            'gemini-flash-latest',        # Latest Flash version
            'gemini-2.5-pro',             # More capable but slower
            'gemini-pro-latest',          # Latest Pro version
        ]
        
        self.model = None
        last_error = None
        
        for model_name in model_names_to_try:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"✅ Initialized with model: {model_name}")
                break
            except Exception as e:
                last_error = str(e)[:150]
                continue
        
        if not self.model:
            raise Exception(f"Could not initialize any Gemini model. Last error: {last_error}")
        
        self.chat = None
        
        # Initialize specialized agents
        self.planning_agent = PlanningAgent()
        self.travel_agent = TravelAgent()
        self.finance_agent = FinanceAgent()
        self.search_agent = SearchAgent()
        
        # Conversation history
        self.history = []
        
    def start_session(self):
        """Start a new chat session"""
        self.chat = self.model.start_chat(history=[])
        
    def parse_intent(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Gemini to understand user intent and determine which agents to invoke
        """
        system_prompt = f"""You are a travel planning coordinator that analyzes user requests and determines which specialized agents should handle the task.

Available agents:
1. PlanningAgent - Handles destination research, attractions, itinerary creation
2. TravelAgent - Handles flights, hotels, transportation booking
3. FinanceAgent - Handles budget planning, cost estimates, money-saving tips
4. SearchAgent - Handles web searches for specific information

Current trip context:
{json.dumps(context, indent=2)}

User request: "{user_message}"

Analyze the request and respond with a JSON object containing:
{{
    "intent": "brief description of what user wants",
    "agents_needed": ["list of agent names needed"],
    "tasks": {{
        "AgentName": "specific task for this agent"
    }},
    "search_queries": ["list of searches needed if any"]
}}

Only return valid JSON, no other text."""

        try:
            response = self.model.generate_content(system_prompt)
            intent_data = json.loads(response.text.strip())
            return intent_data
        except Exception as e:
            # Fallback if JSON parsing fails
            return {
                "intent": user_message,
                "agents_needed": ["PlanningAgent"],
                "tasks": {"PlanningAgent": user_message},
                "search_queries": []
            }
    
    def coordinate_agents(self, intent: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate multiple agents based on parsed intent
        """
        results = {
            'intent': intent.get('intent', ''),
            'agent_responses': {}
        }
        
        agents_map = {
            'PlanningAgent': self.planning_agent,
            'TravelAgent': self.travel_agent,
            'FinanceAgent': self.finance_agent,
            'SearchAgent': self.search_agent
        }
        
        # Execute tasks for each agent
        for agent_name in intent.get('agents_needed', []):
            if agent_name in agents_map:
                agent = agents_map[agent_name]
                task = intent['tasks'].get(agent_name, '')
                
                # Process task with agent
                agent_result = agent.process(task, context)
                results['agent_responses'][agent_name] = agent_result
        
        return results
    
    def generate_ai_content(self, prompt: str, context: Dict[str, Any]) -> str:
        """
        Use Gemini to generate travel content (itineraries, recommendations, etc.)
        """
        try:
            full_prompt = f"""Travel Planning Context:
{json.dumps(context, indent=2)}

{prompt}

Provide detailed, practical, and helpful information."""
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def chat_with_user(self, user_message: str, context: Dict[str, Any]) -> str:
        """
        Main method to process user messages using conversational AI
        """
        if not self.chat:
            self.start_session()
        
        # Enhance message with context
        enhanced_message = f"""Travel Context: {json.dumps(context, indent=2)}

User message: {user_message}

As a helpful travel planning assistant with access to specialized agents, provide a comprehensive response. Be specific, practical, and include actionable recommendations."""
        
        try:
            response = self.chat.send_message(enhanced_message)
            
            # Store in history
            self.history.append({
                'user': user_message,
                'assistant': response.text,
                'context': context
            })
            
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def get_recommendations(self, agent_type: str, context: Dict[str, Any]) -> str:
        """
        Get AI-generated recommendations from specific agent perspective
        """
        prompts = {
            'planning': self.planning_agent.create_itinerary_prompt(context),
            'travel': self.travel_agent.create_search_prompt(context, 'flights'),
            'finance': self.finance_agent.create_finance_prompt(context)
        }
        
        prompt = prompts.get(agent_type, '')
        if prompt:
            return self.generate_ai_content(prompt, context)
        return ""
    
    def search_and_summarize(self, query: str, context: Dict[str, Any]) -> str:
        """
        Perform search and use AI to summarize results
        """
        search_result = self.search_agent.process(query, context)
        
        summary_prompt = f"""Based on a search for "{query}", provide a comprehensive summary of what travelers should know.

Include:
1. Key information and highlights
2. Practical tips and recommendations
3. Important details to consider
4. Estimated costs if relevant

Be specific and helpful."""
        
        return self.generate_ai_content(summary_prompt, context)
    
    def create_complete_itinerary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate all agents to create a complete travel plan
        """
        destination = context.get('destination', '')
        duration = context.get('duration', 1)
        budget = context.get('budget', 0)
        
        # Step 1: Planning Agent - Create itinerary
        itinerary_prompt = self.planning_agent.create_itinerary_prompt(context)
        itinerary = self.generate_ai_content(itinerary_prompt, context)
        
        # Step 2: Travel Agent - Get travel options
        travel_prompt = self.travel_agent.create_search_prompt(context, 'flights')
        travel_info = self.generate_ai_content(travel_prompt, context)
        
        hotel_prompt = self.travel_agent.create_search_prompt(context, 'hotels')
        hotel_info = self.generate_ai_content(hotel_prompt, context)
        
        # Step 3: Finance Agent - Budget breakdown
        finance_prompt = self.finance_agent.create_finance_prompt(context)
        finance_info = self.generate_ai_content(finance_prompt, context)
        
        # Step 4: Compile everything
        complete_plan = {
            'destination': destination,
            'duration': duration,
            'budget': budget,
            'itinerary': itinerary,
            'travel_options': travel_info,
            'accommodation': hotel_info,
            'budget_plan': finance_info
        }
        
        return complete_plan
    
    def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """
        Answer specific questions about the trip
        """
        return self.chat_with_user(question, context)
