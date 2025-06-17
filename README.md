# MemGPT + AutoGen Multi-Agent System

A powerful multi-agent conversational system that combines MemGPT's persistent memory capabilities with AutoGen's collaborative agent framework, powered by Google's Gemini AI.

## 🌟 Features

- **Persistent Memory**: MemGPT-powered agents remember conversation history across sessions
- **Multi-Agent Collaboration**: Product Manager, Coder, and User Proxy agents work together
- **Gemini AI Integration**: Leverages Google's Gemini models for intelligent responses
- **Fallback System**: Gracefully falls back to standard AutoGen agents if MemGPT fails
- **Rate Limit Handling**: Built-in error handling for API rate limits
- **Memory Demonstration**: Interactive demo showcasing persistent memory capabilities

## 🏗️ Architecture

The system consists of three main components:

1. **MemGPT_Coder**: A memory-enabled coding agent that retains context across conversations
2. **Product_Manager**: Standard AutoGen agent for generating product ideas and requirements
3. **User_Proxy**: Human-like agent that manages the conversation flow

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- MemGPT installation requirements

### Installation

1. Clone the repository:
```bash
git clone https://github.com/naakaarafr/MemGPT-AutoGen-Multi-Agent-System.git
cd MemGPT-AutoGen-Multi-Agent-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Run the system:
```bash
python mem.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Agent Configuration

The system automatically configures agents with the following personas:

- **MemGPT_Coder**: "10x engineer at a FAANG tech company with perfect memory"
- **Product_Manager**: "Creative product manager generating innovative software ideas"
- **User_Proxy**: "Team manager who values thorough documentation"

## 🧠 MemGPT Integration

### Memory Features

- **Persistent Context**: Conversations are stored and recalled across sessions
- **Contextual Awareness**: Agents can reference previous discussions
- **Memory Demonstration**: Built-in demo showing memory capabilities

### Bridge Architecture

The `MemGPTAgent` class bridges MemGPT with AutoGen:

```python
class MemGPTAgent(autogen.ConversableAgent):
    def __init__(self, name, memgpt_client, memgpt_agent, **kwargs):
        # Bridges MemGPT persistent memory with AutoGen conversations
```

## 🎯 Usage Examples

### Basic Conversation

```python
user_proxy.initiate_chat(
    manager,
    message="Let's discuss building a new developer platform."
)
```

### Memory Testing

The system includes a built-in memory demonstration:

```python
demonstrate_memgpt_features()
```

This function:
1. Stores context about a fictional project "DevConnect"
2. Tests memory recall with specific questions
3. Demonstrates persistent memory capabilities

## 🔧 Customization

### Adding New Agents

```python
new_agent = autogen.AssistantAgent(
    name="Custom_Agent",
    system_message="Your custom system message",
    llm_config=llm_config
)

# Add to group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, coder, pm, new_agent],
    messages=[],
    max_round=8
)
```

### Modifying Agent Personas

Edit the `agent_config` dictionary in `setup_memgpt_client()`:

```python
agent_config = {
    "name": "Your_Agent_Name",
    "persona": "Your custom persona description",
    "human": "Your human description",
    "model": "gemini-2.0-flash"
}
```

## ⚠️ Rate Limits & Error Handling

### Gemini API Limits

- **Free Tier**: 10 requests per minute
- **Paid Tier**: Higher limits available

### Error Handling

The system includes comprehensive error handling:

- **Rate Limit Errors**: Graceful handling with user-friendly messages
- **MemGPT Failures**: Automatic fallback to standard AutoGen agents
- **API Timeouts**: 60-second timeout with retry logic

## 🐛 Troubleshooting

### Common Issues

1. **MemGPT Setup Failed**
   - Check MemGPT installation: `pip install memgpt`
   - Verify API key configuration
   - System falls back to standard AutoGen

2. **Rate Limit Exceeded**
   - Wait 60 seconds between conversations
   - Consider upgrading to paid Gemini API tier
   - Reduce `max_round` in group chat

3. **Docker Errors**
   - Code execution disabled by default (`use_docker: False`)
   - Enable Docker if needed for code execution

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Considerations

- **Memory Usage**: MemGPT stores conversation history locally
- **API Calls**: Each agent response counts toward rate limits
- **Conversation Length**: Limited by `max_round` parameter (default: 6)

## 🔮 Future Enhancements

- [ ] Support for additional LLM backends
- [ ] Web interface for easier interaction
- [ ] Enhanced memory management tools
- [ ] Multi-project memory separation
- [ ] Advanced agent role customization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [AutoGen](https://github.com/microsoft/autogen) - Multi-agent conversation framework
- [MemGPT](https://github.com/cpacker/MemGPT) - Persistent memory for LLMs
- [Google Gemini](https://ai.google.dev/) - Generative AI platform

## 📞 Support

For issues and questions:
- Open a GitHub issue
- Check the troubleshooting section
- Review AutoGen and MemGPT documentation

---

**Note**: This system is designed for development and research purposes. Monitor API usage and costs when using paid services.
