import os
import autogen
import time
from dotenv import load_dotenv
import memgpt
from memgpt import create_client
from memgpt.client.client import LocalClient
import json

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Configure MemGPT with Gemini
def setup_memgpt_client():
    """Setup MemGPT client with Gemini backend"""
    try:
        # Initialize MemGPT client
        client = create_client()
        
        # Create a MemGPT agent with custom persona
        agent_config = {
            "name": "MemGPT_Coder",
            "persona": "I'm a 10x engineer at a FAANG tech company with perfect memory of our conversations. I remember all context, previous code discussions, and can build upon our past work seamlessly.",
            "human": "You are a team manager at a FAANG tech company who values thorough documentation and iterative development.",
            "model": "gemini-2.0-flash",  # Use Gemini as backend
        }
        
        # Create agent
        agent = client.create_agent(**agent_config)
        return client, agent
    except Exception as e:
        print(f"MemGPT setup failed: {e}")
        print("Falling back to standard AutoGen agents...")
        return None, None

# MemGPT-AutoGen Bridge Class
class MemGPTAgent(autogen.ConversableAgent):
    """Bridge between MemGPT and AutoGen"""
    
    def __init__(self, name, memgpt_client, memgpt_agent, **kwargs):
        super().__init__(name=name, **kwargs)
        self.memgpt_client = memgpt_client
        self.memgpt_agent = memgpt_agent
        self.conversation_history = []
    
    def generate_reply(self, messages=None, sender=None, **kwargs):
        """Generate reply using MemGPT agent"""
        if not self.memgpt_client or not self.memgpt_agent:
            return "MemGPT agent not available"
        
        try:
            # Get the last message
            last_message = messages[-1]['content'] if messages else ""
            
            # Send message to MemGPT
            response = self.memgpt_client.user_message(
                agent_id=self.memgpt_agent.id,
                message=last_message
            )
            
            # Extract the assistant's response
            if response and response.messages:
                # Get the last assistant message
                for msg in reversed(response.messages):
                    if msg.role == 'assistant' and msg.text:
                        return msg.text
            
            return "I received your message and it's stored in my memory."
            
        except Exception as e:
            print(f"MemGPT error: {e}")
            return f"I encountered an issue accessing my memory, but I'm still here to help."

# Standard AutoGen config for fallback
config_list = [
    {
        'model': 'gemini-1.5-flash',
        'api_key': gemini_api_key,
        'api_type': 'google'
    }
]

llm_config = {
    "config_list": config_list, 
    "seed": 42,
    "temperature": 0.7,
    "timeout": 60
}

# Setup MemGPT
print("Setting up MemGPT...")
memgpt_client, memgpt_agent = setup_memgpt_client()

# User proxy agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin managing a development team.",
    code_execution_config={
        "last_n_messages": 2, 
        "work_dir": "groupchat",
        "use_docker": False
    },
    human_input_mode="NEVER"
)

# Create MemGPT-powered coder or fallback to standard agent
if memgpt_client and memgpt_agent:
    print("✅ MemGPT agent created successfully!")
    coder = MemGPTAgent(
        name="MemGPT_Coder",
        memgpt_client=memgpt_client,
        memgpt_agent=memgpt_agent,
        system_message="I'm a MemGPT-powered coder with persistent memory. I remember all our conversations and can build upon previous work.",
        llm_config=False  # Disable standard LLM as we use MemGPT
    )
else:
    print("⚠️ Using fallback standard AutoGen agent")
    coder = autogen.AssistantAgent(
        name="Standard_Coder",
        system_message="I'm a 10x engineer at a FAANG tech company, but I don't have persistent memory between conversations.",
        llm_config=llm_config,
    )

# Product Manager agent (standard AutoGen)
pm = autogen.AssistantAgent(
    name="Product_Manager", 
    system_message="I'm a creative product manager at a FAANG tech company. I generate innovative software product ideas and define requirements.",
    llm_config=llm_config,
)

# Create group chat with reduced rounds to avoid rate limits
groupchat = autogen.GroupChat(
    agents=[user_proxy, coder, pm], 
    messages=[], 
    max_round=6
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, 
    llm_config=llm_config
)

# Demonstration function
def demonstrate_memgpt_features():
    """Demonstrate MemGPT's memory capabilities"""
    if not memgpt_client or not memgpt_agent:
        print("MemGPT not available for demonstration")
        return
    
    print("\n🧠 MemGPT Memory Demonstration:")
    print("=" * 50)
    
    # Store some context
    context_messages = [
        "Remember that we're working on a social media app called 'DevConnect' for developers.",
        "The main features include code sharing, tech discussions, and project collaboration.",
        "We decided to use React for frontend and Node.js for backend.",
        "The target audience is software engineers and computer science students."
    ]
    
    for msg in context_messages:
        print(f"📝 Storing: {msg}")
        response = memgpt_client.user_message(
            agent_id=memgpt_agent.id,
            message=msg
        )
        time.sleep(1)  # Rate limiting
    
    print("\n🔍 Testing Memory Recall:")
    test_questions = [
        "What's the name of our app?",
        "What technology stack did we choose?",
        "Who is our target audience?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        response = memgpt_client.user_message(
            agent_id=memgpt_agent.id,
            message=question
        )
        
        if response and response.messages:
            for msg in response.messages:
                if msg.role == 'assistant' and msg.text:
                    print(f"🤖 MemGPT: {msg.text}")
                    break
        time.sleep(2)  # Rate limiting

# Start the conversation with MemGPT integration
if __name__ == "__main__":
    print("🚀 Starting MemGPT + AutoGen Demo")
    print("=" * 40)
    
    # Demonstrate MemGPT's memory capabilities
    demonstrate_memgpt_features()
    
    print("\n💬 Starting Multi-Agent Conversation:")
    print("=" * 40)
    
    try:
        user_proxy.initiate_chat(
            manager, 
            message="""Let's go Mario! 
            
            I want to discuss building a new developer collaboration platform. 
            MemGPT_Coder should remember our previous discussions about DevConnect if we had any.
            
            Please:
            1. MemGPT_Coder: Share what you remember about our project
            2. Product_Manager: Suggest 3 innovative features
            3. MemGPT_Coder: Provide technical implementation details
            
            Keep responses concise due to API rate limits."""
        )
        
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("⚠️ Rate limit exceeded. Gemini free tier allows 10 requests/minute.")
            print("💡 MemGPT stores this conversation in memory for future reference!")
            print("🕒 Wait 60 seconds and try again, or upgrade your API plan.")
        else:
            print(f"❌ Error occurred: {e}")
            
    # Show MemGPT's memory after conversation
    if memgpt_client and memgpt_agent:
        print("\n🧠 MemGPT Memory Status:")
        try:
            # Get agent's memory summary
            response = memgpt_client.user_message(
                agent_id=memgpt_agent.id,
                message="Summarize what we discussed today and what you remember about our project."
            )
            
            if response and response.messages:
                for msg in response.messages:
                    if msg.role == 'assistant' and msg.text:
                        print(f"📋 Memory Summary: {msg.text}")
                        break
        except Exception as e:
            print(f"Could not retrieve memory summary: {e}")
    print("\n✅ Demo completed! MemGPT has persistent memory of this conversation.")