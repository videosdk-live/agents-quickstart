# n8n Workflow — Appointment Follow-Up with VideoSDK AI Telephony

This example shows how to automate outbound appointment confirmation calls using **VideoSDK AI Telephony** and **n8n**. An AI agent calls customers from a Google Sheet, confirms their appointments, and updates the booking status automatically — sequentially, one customer at a time.

---

## What This Example Does

1. n8n reads your Google Sheet and finds all rows where **Status = `call left`**
2. It initiates an outbound call to the first customer via VideoSDK
3. The AI agent speaks with the customer and confirms whether they will attend their appointment
4. Based on the customer's response:
   - **Attending** → `Booking Status` is updated to `Booked`
   - **Not attending** → `Booking Status` is updated to `Cancelled`
5. The customer's **Status** is updated to `call done`
6. Once the call ends, the workflow moves to the next customer with `call left` status
7. This continues sequentially until all pending customers have been contacted

---

## Prerequisites

- A [VideoSDK](https://videosdk.live) account with AI Telephony enabled
- An [n8n](https://n8n.io) account (free trial available)
- A Google Sheet set up with your appointment data
- Google account authenticated in n8n (for Google Sheets node)
- Your VideoSDK Auth Token, API keys, `Gateway ID`, and `Agent ID`
- The webhook URL from the n8n Webhook node pasted into VideoSDK telephony webhooks

Refer to the VideoSDK docs for configuration details:
- [AI Phone Agent Quick Start](https://docs.videosdk.live/ai_agents/ai-phone-agent-quick-start#making-an-outbound-call)
- [Making Outbound Calls](https://docs.videosdk.live/telephony/managing-calls/making-outbound-calls)
- [SIP Webhooks Reference](https://docs.videosdk.live/telephony/managing-calls/sip-webhooks)

---

## Step 1 — Set Up Your Google Sheet

Structure your sheet with the following key columns:

- **Booking Status** — Tracks appointment confirmation. Starts as `Pending`, updated to `Booked` or `Cancelled` after the call.
- **Status** — Tracks whether the customer has been contacted:
  - `call left` — Customer has not been called yet
  - `calling` — Call is currently in progress
  - `call done` — Call has been completed

The AI agent will only call customers whose Status is `call left`, ensuring no one gets called twice.

---

## Step 2 — Import the n8n Workflow

1. Log in to your n8n account and open the canvas
2. Click the three-dot menu in the top right
3. Select **"Import from file"**
4. Upload `customer_followup_agent.json` from this directory
5. Your workflow will appear on the canvas, fully assembled

### The Three Core Nodes

**MCP Server Trigger** — Allows your AI Agent to perform specific operations (fetch data, update records, etc.)

**HTTP POST Request (Calling Customer Node)** — Initiates the outbound call to each customer via the VideoSDK telephony API

**Webhook Trigger (Capturing Call Events)** — Listens for real-time call events (`call-answered`, `call-hangup`, etc.) from VideoSDK so the workflow can react when a call ends

---

## Step 3 — Connect Your AI Agent via MCP

1. Click on the **MCP Server** node in n8n
2. Copy the **Production URL** shown
3. Paste it into `appointment_telephony.py`:

```python
mcp_servers=[
    MCPServerHTTP(
        endpoint_url="[Your Production URL Here]",
    )
]
```

Use the **Test URL** during development and switch to the **Production URL** when going live.

---

## Step 4 — Configure Agent Instructions

Open `appointment_telephony.py`. This script contains the AI agent instructions that guide how the agent speaks to customers, handles responses, and triggers the appropriate n8n workflow actions.

---

## Step 5 — Run the Workflow

1. **Start the agent script**:

   ```bash
   uv run python "n8n Workflow/appointment_telephony.py"
   ```

2. **Publish your n8n workflow** — open the workflow and click **Publish**

3. **Execute the workflow** — click the dropdown arrow next to "Execute Workflow", select "When clicking 'Execute workflow'", then click **Execute Workflow**

---

## Files in This Directory

```
n8n Workflow/
├── appointment_telephony.py       # AI agent script
├── customer_followup_agent.json   # n8n workflow export (import this into n8n)
├── images/                        # Screenshots for documentation
└── README.md                      # This file
```
