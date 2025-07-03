# 🤖 A2A Implementation Guide

This guide explains how to build a complete Agent to Agent (A2A) system. We'll create a banking customer service system with a main customer service agent and a loan specialist.

![A2A Sequence Diagram](https://cdn.videosdk.live/website-resources/docs-resources/a2a_sequence_diagram.png)

## 🔄 Understanding the Sequence Diagram

The diagram above shows the complete flow of A2A communication:

### **Initialization Phase**
- **CustomerAgent** and **LoanAgent** register themselves with the A2A system
- Each agent declares their domain expertise and capabilities
- The A2A system maintains a registry of available agents

### **Loan Query Flow**
1. **Customer Query**: User asks about personal loans
2. **Agent Discovery**: CustomerAgent uses `find_agents_by_domain("loan")` to locate specialists
3. **Query Forwarding**: CustomerAgent sends the query to LoanAgent via A2A messaging
4. **Processing**: LoanAgent processes the query using its specialized knowledge
5. **Response Chain**: LoanAgent sends the response back to CustomerAgent
6. **User Relay**: CustomerAgent delivers the specialist response to the user

### **Follow-up Query Flow**
- The system maintains context for follow-up questions
- Subsequent loan-related queries automatically route to the same specialist
- No re-discovery needed for continuous conversation flow

## 📋 What We're Building

- **Customer Service Agent**: Voice-enabled interface agent that users interact with
- **Loan Specialist Agent**: Text-based domain expert for loan-related queries
- **Intelligent Routing**: Automatic detection and forwarding of loan queries
- **Seamless Communication**: Users get expert responses without knowing about the routing

## 📁 Project Structure

```js
A2A/
├── agents/
│   ├── customer_agent.py     # CustomerServiceAgent definition
│   ├── loan_agent.py         # LoanAgent definition
├── session_manager.py        # Session and pipeline management
└── main.py                   # Entry point: runs main() and starts agents
```

## Step 1: Customer Service Agent Design

**Purpose**: Main user-facing agent with voice capabilities

**Key Components**:
- **Agent Registration**: Registers with domain "customer_service" and coordination capabilities
- **Function Tool**: Implements `forward_to_specialist()` that uses A2A discovery to find domain experts
- **Response Handling**: Automatically receives and relays specialist responses back to users
- **Voice Interaction**: Configured for real-time audio communication with users

**Intelligence Flow**:
- Handles general banking queries directly
- Detects loan-related questions and triggers specialist routing
- Maintains conversation context while coordinating with specialists

## Step 2: Loan Specialist Agent Design

**Purpose**: Domain expert with specialized loan knowledge

**Key Components**:
- **Domain Registration**: Registers with domain "loan" for discoverability
- **Query Processing**: Handles incoming specialist queries from other agents
- **Response Generation**: Processes queries using specialized loan knowledge
- **A2A Communication**: Sends responses back to requesting agents

**Specialization**:
- Text-based processing for efficient response generation
- Background operation (doesn't join meetings)
- Focuses on loan products, rates, terms, and requirements

## Step 3: Session Management Configuration

**Purpose**: Configure different agent modalities and capabilities

**Pipeline Configuration**:
- **Customer Agent**: **RealTimePipeline** with Gemini Realtime model (`gemini-2.0-flash-live-001`) for low-latency voice interaction
- **Specialist Agent**: **CascadingPipeline** with OpenAI LLM for efficient text processing
- **Voice Configuration**: Customer agent uses "Leda" voice with audio response modality
- **Modality Separation**: Audio pipeline for user interaction, text pipeline for specialist processing

**Session Strategy**:
- Customer agent joins VideoSDK meetings for user interaction
- Specialist agents run in background for processing only

## Step 4: System Deployment

**Purpose**: Orchestrate the complete A2A system

**System Initialization**:
- Both agents are created and configured with their respective pipelines
- Customer agent joins VideoSDK meeting for user interaction
- Specialist agent runs in background mode
- Environment requires `VIDEOSDK_AUTH_TOKEN`, `GOOGLE_API_KEY`, and `OPENAI_API_KEY`

**Resource Management**:
- Proper startup sequence ensures agents register before queries arrive
- Clean shutdown includes A2A unregistration
- Session isolation maintains independent agent operations

## 🚀 Running the Application

```bash
cd A2A
python main.py
```

## 🔧 Agent Specifications

| Agent | ID | Domain | Pipeline | Modality | Meeting Join | Function |
|-------|-----|---------|----------|----------|--------------|----------|
| **Customer Service** | `customer_service_1` | `customer_service` | RealTimePipeline | Audio | ✅ Yes | User interface and query routing |
| **Loan Specialist** | `specialist_1` | `loan` | CascadingPipeline | Text | ❌ No | Loan expertise and information |

## 🌟 Key Features

- **Multi-Modal Communication**: Audio agents for users, text agents for processing
- **Intelligent Routing**: Automatic query detection and specialist forwarding
- **Real-Time Collaboration**: Seamless agent-to-agent communication
- **Domain Specialization**: Easily extensible to new domains (tech support, finance, etc.)

## 🔍 How A2A Discovery Works

**Agent Registration**:
- Each agent registers with an `AgentCard` containing their capabilities
- The A2A system maintains a global registry of available agents
- Agents can be discovered by domain or specific capabilities

**Query Routing Process**:
- Customer agent detects domain-specific queries
- Uses `find_agents_by_domain()` to locate appropriate specialists
- Forwards queries using standardized `A2AMessage` format
- Specialists process and respond back through the same system

**Response Coordination**:
- Specialists send responses back to the requesting agent
- Customer agent automatically relays responses to users
- Context is maintained across multiple exchanges

## 📚 Learn More

- **[A2A Overview](https://docs.videosdk.live/ai_agents/a2a/overview)** - Core concepts and components
- **[A2A Implementation](https://docs.videosdk.live/ai_agents/a2a/implementation)** - Complete implementation guide
- **[VideoSDK AI Agents](https://docs.videosdk.live/ai_agents/introduction)** - Framework documentation

