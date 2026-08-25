# AI Travel Planner

An open-source, multi-agent AI travel planning application that helps users plan a complete trip through an interactive, human-in-the-loop workflow.

The project is designed not only to build a useful travel planner, but also to learn how to build **multi-agent AI applications** using open-source technologies.

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Problem Statement](#2-problem-statement)
- [3. Project Goals](#3-project-goals)
- [4. Core User Journey](#4-core-user-journey)
- [5. Example User Journey](#5-example-user-journey)
- [6. Multi-Agent Architecture](#6-multi-agent-architecture)
- [7. Agents](#7-agents)
- [8. Tools](#8-tools)
- [9. Human-in-the-Loop Workflow](#9-human-in-the-loop-workflow)
- [10. Technology Stack](#10-technology-stack)
- [11. Why These Technologies](#11-why-these-technologies)
- [12. Project Structure](#12-project-structure)
- [13. Shared Trip State](#13-shared-trip-state)
- [14. Data Flow](#14-data-flow)
- [15. Important Design Principles](#15-important-design-principles)
- [16. Open-Source Data and Services](#16-open-source-data-and-services)
- [17. MVP Scope](#17-mvp-scope)
- [18. Future Enhancements](#18-future-enhancements)
- [19. Development Roadmap](#19-development-roadmap)
- [20. Local Development](#20-local-development)
- [21. Environment Variables](#21-environment-variables)
- [22. Testing Strategy](#22-testing-strategy)
- [23. Error Handling](#23-error-handling)
- [24. Reliability and Hallucination Prevention](#24-reliability-and-hallucination-prevention)
- [25. Cost Calculation](#25-cost-calculation)
- [26. Booking Disclaimer](#26-booking-disclaimer)
- [27. Learning Objectives](#27-learning-objectives)
- [28. Production Evolution](#28-production-evolution)
- [29. Contributing](#29-contributing)
- [30. License](#30-license)

---

# 1. Project Overview

**AI Travel Planner** is a conversational travel-planning application powered by open-source AI and a multi-agent architecture.

A user can enter a destination such as:

> Bengaluru, Karnataka, India

The application progressively asks for the information it needs instead of making assumptions.

It can then:

1. Discover famous and relevant places to visit.
2. Show distance and estimated travel time between places.
3. Allow the user to choose the places they want to visit.
4. Generate a detailed day-by-day itinerary.
5. Ask the user to approve or modify the itinerary.
6. Search for accommodation based on the user's preferences.
7. Allow the user to select a stay.
8. Generate a final complete itinerary.
9. Provide accommodation and external booking information when available.
10. Estimate the overall trip cost.

The application is intentionally designed as a **human-in-the-loop multi-agent system**.

---

# 2. Problem Statement

Planning a trip often requires information from multiple sources:

- Tourist attractions
- Locations
- Distances
- Travel times
- Opening hours
- Accommodation
- Budget
- Transportation
- User preferences

A traditional application may expose all of these as separate search screens.

This project aims to provide a conversational experience where an AI system coordinates these tasks while keeping the user in control.

The system should not simply generate an itinerary from an LLM's knowledge.

Instead:

```text
User
  |
  v
AI Agent
  |
  +----> External/Open Data Tools
  |
  +----> Routing Tools
  |
  +----> Accommodation Search
  |
  v
AI-generated plan
  |
  v
User approval
```

The LLM is responsible for reasoning and orchestration, while tools provide factual information.

---

# 3. Project Goals

## Primary Goal

Build a practical multi-agent AI application while learning:

- LLMs
- Agents
- Tools
- Tool calling
- Structured outputs
- LangGraph
- Shared state
- Conditional workflows
- Human-in-the-loop
- Multi-agent orchestration
- External APIs
- Open-source models

## Secondary Goal

Build a useful travel planner that can eventually support:

- Multiple destinations
- Accommodation
- Transportation
- Weather
- Restaurants
- Budget optimization
- Booking links
- Personalized recommendations

---

# 4. Core User Journey

The application follows this workflow:

```text
                    User
                     |
                     v
          Collect Trip Requirements
                     |
                     v
            Destination Agent
                     |
                     v
              Places Search
                     |
                     v
              Routing Tools
                     |
                     v
             Itinerary Agent
                     |
                     v
              User Approval
                /        \
             Modify      Accept
               |            |
               |            v
               |       Stay Agent
               |            |
               |            v
               |       User Selects
               |            |
               └------------+
                            |
                            v
                     Final Planner
                            |
                            v
                    Complete Itinerary
```

---

# 5. Example User Journey

## Step 1 — Destination

AI:

> Where would you like to travel?

User:

> Bengaluru

---

## Step 2 — Duration

AI:

> How many days would you like to stay?

User:

> 3 days

---

## Step 3 — Travelers

AI:

> How many people are travelling?

User:

> 2

---

## Step 4 — Budget

AI:

> What is your approximate budget?

User:

> ₹5,000 per person per day

---

## Step 5 — Transportation

AI:

> How would you like to travel?

Possible options:

- Public transport
- Cab
- Rental vehicle
- Self-drive
- Combination

User:

> Cab and public transport

---

## Step 6 — Discover Places

The Destination Agent searches for suitable attractions.

Example:

```text
1. Lalbagh Botanical Garden
2. Cubbon Park
3. Bangalore Palace
4. Vidhana Soudha
5. ISKCON Temple
6. Nandi Hills
7. Commercial Street
```

The application can display:

```text
Lalbagh Botanical Garden

Category: Nature
Location: Bengaluru

Distance from current/previous location:
5.2 km

Estimated travel time:
20 minutes

[ Select ]
```

---

## Step 9 — User Selects Places

User selects:

```text
Lalbagh
Cubbon Park
Bangalore Palace
Vidhana Soudha
Nandi Hills
```

---

## Step 10 — Itinerary Generation

The Itinerary Agent creates a plan based on:

- Number of days
- Selected attractions
- Distance
- Travel time
- Opening hours
- Budget

Example:

```text
DAY 1

09:00
Leave hotel

09:30 - 12:00
Lalbagh Botanical Garden

12:00 - 12:25
Travel to Cubbon Park

Distance: 5.2 km
Estimated travel time: 25 minutes

12:30 - 14:00
Cubbon Park

14:00 - 15:00
Lunch

15:30 - 17:30
Bangalore Palace

18:00
Return to hotel
```

---

## Step 11 — User Approval

The application stops and asks:

```text
Do you approve this itinerary?

1. Accept
2. Modify
3. Start over
```

The accommodation workflow should not start until the user chooses **Accept**.

---

## Step 12 — Accommodation

The Stay Agent asks:

```text
What type of accommodation do you prefer?

1. Hotel
2. Villa
3. Apartment
4. Hostel
5. No preference
```

Then:

```text
What is your nightly budget?
```

Then:

```text
Where would you prefer to stay?

1. Near attractions
2. Near public transport
3. City center
4. Quiet area
5. No preference
```

---

## Step 13 — Stay Selection

The application shows suitable options.

The user selects one.

---

## Step 14 — Final Itinerary

The Final Planner combines all approved information:

```text
BENGALURU
3 Days / 2 Nights
2 Travelers

Accommodation:
Hotel XYZ

DAY 1
...

DAY 2
...

DAY 3
...

Estimated Cost:

Accommodation: ₹8,000
Transport: ₹3,000
Food: ₹3,000
Activities: ₹2,000

Estimated Total: ₹16,000

Booking:
External booking provider
```

---

# 6. Multi-Agent Architecture

The initial architecture uses four primary agents.

```text
                    +----------------+
                    |      User      |
                    +-------+--------+
                            |
                            v
                 +---------------------+
                 | Requirements Agent  |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Destination Agent   |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Places / Geo Tools  |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Itinerary Agent     |
                 +----------+----------+
                            |
                            v
                    +---------------+
                    | User Approval |
                    +-------+-------+
                            |
                  +---------+---------+
                  |                   |
                MODIFY              ACCEPT
                  |                   |
                  |                   v
                  |          +----------------+
                  |          |   Stay Agent   |
                  |          +-------+--------+
                  |                  |
                  |                  v
                  |          +----------------+
                  |          | User Selection |
                  |          +-------+--------+
                  |                  |
                  +------------------+
                                     |
                                     v
                           +------------------+
                           | Final Planner    |
                           +--------+---------+
                                    |
                                    v
                           Complete Itinerary
```

---

# 7. Agents

## 7.1 Requirements Agent

### Responsibility

Collect the information required to plan the trip.

### Information

```text
destination
number_of_days
number_of_travelers
budget
transportation_preference
```

### Important rule

If information is missing, ask the user.

Do not guess.

---

## 7.2 Destination Agent

### Responsibility

Find relevant places in the selected destination.

### Inputs

```text
destination
number_of_days
```

### Outputs

```text
place name
description
category
latitude
longitude
location
```

The agent should use real data sources wherever possible.

---

## 7.3 Itinerary Agent

### Responsibility

Generate the day-by-day travel plan.

It should consider:

- Selected places
- Distance
- Travel time
- Opening hours
- Number of days
- Budget
- Meal breaks
- Rest time

The agent should group geographically close attractions where practical.

---

## 7.4 Stay Agent

### Responsibility

Find accommodation after the itinerary is approved.

It should consider:

- Accommodation type
- Budget
- Preferred location
- Number of travelers
- Number of nights
- Relationship to planned attractions

The Stay Agent must not claim real-time availability unless availability has actually been verified.

---

## 7.5 Final Planner

### Responsibility

Combine all approved trip information.

Inputs:

```text
trip requirements
selected places
routes
approved itinerary
selected accommodation
cost information
```

Output:

```text
complete final itinerary
```

---

# 8. Tools

Agents should use tools for deterministic and external operations.

Recommended tools:

```text
tools/
├── places.py
├── geocoding.py
├── routing.py
├── opening_hours.py
├── accommodation.py
└── cost_calculator.py
```

---

## Places Tool

Responsible for finding places.

Example:

```python
search_places(destination)
```

---

## Geocoding Tool

Converts an address/place name into coordinates.

Example:

```python
geocode_location(place_name)
```

---

## Routing Tool

Calculates:

- Distance
- Travel time
- Route

Example:

```python
calculate_route(origin, destination)
```

---

## Opening Hours Tool

Retrieves opening/closing information where available.

This helps avoid generating impossible itineraries.

---

## Accommodation Tool

Searches for suitable stays.

---

## Cost Calculator

Performs deterministic calculations.

For example:

```text
Accommodation
+ Transportation
+ Food
+ Activities
+ Miscellaneous
= Estimated Total
```

The LLM should not be responsible for arithmetic that Python can perform reliably.

---

# 9. Human-in-the-Loop Workflow

Human approval is a core feature.

The user must approve:

1. Selected places
2. Itinerary
3. Accommodation

The application should never silently make these decisions.

Example:

```text
AI:
Here is your proposed itinerary.

[ Accept ]
[ Modify ]
[ Start Over ]
```

If the user chooses:

```text
Modify
```

The workflow returns to the itinerary generation step.

---

# 10. Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Agent orchestration | LangGraph |
| Local LLM runtime | Ollama |
| LLM | Qwen / Llama / Mistral |
| Structured data | Pydantic |
| Database | SQLite initially |
| Maps | OpenStreetMap |
| Geocoding | Nominatim |
| Places | Overpass API / OSM |
| Routing | OSRM |
| Frontend | React / Next.js |
| Maps UI | Leaflet |
| Version control | Git |

---

# 11. Why These Technologies

## Python

Python has a mature ecosystem for:

- AI
- LLMs
- APIs
- data processing
- agent frameworks

It is also beginner-friendly.

---

## LangGraph

LangGraph is used to model the travel planner as a stateful graph.

It provides concepts such as:

- Nodes
- Edges
- Conditional routing
- State
- Interruptions
- Checkpoints
- Human-in-the-loop workflows

This makes it a good fit for this project.

---

## Ollama

Ollama allows open-source LLMs to run locally.

This makes it useful for learning without depending on a paid proprietary LLM API.

---

## OpenStreetMap

OpenStreetMap provides open geographic data.

---

## Nominatim

Used for geocoding and reverse geocoding.

---

## OSRM

Used for routing and obtaining:

- Distance
- Travel duration

---

## SQLite

SQLite is sufficient for the first version.

A production system can later migrate to PostgreSQL.

---

# 12. Project Structure

Recommended initial structure:

```text
ai-travel-planner/
│
├── .venv/
│
├── src/
│   ├── main.py
│   │
│   ├── agents/
│   │   ├── requirements_agent.py
│   │   ├── destination_agent.py
│   │   ├── itinerary_agent.py
│   │   ├── stay_agent.py
│   │   └── final_planner.py
│   │
│   ├── tools/
│   │   ├── places.py
│   │   ├── geocoding.py
│   │   ├── routing.py
│   │   ├── opening_hours.py
│   │   ├── accommodation.py
│   │   └── cost_calculator.py
│   │
│   ├── graph/
│   │   └── travel_graph.py
│   │
│   ├── models/
│   │   └── trip.py
│   │
│   ├── database/
│   │   └── db.py
│   │
│   └── config.py
│
├── tests/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_graph.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

The structure can be simplified during the first learning stages.

Do not create all files immediately.

Create files only when their functionality is introduced.

---

# 13. Shared Trip State

The agents should communicate through a shared state instead of passing arbitrary strings between agents.

Example:

```python
class TripState(TypedDict, total=False):
    destination: str
    number_of_days: int
    number_of_travelers: int

    budget: float
    currency: str

    transportation_preference: str

    available_places: list
    selected_places: list

    routes: list

    itinerary: dict
    itinerary_approved: bool

    accommodation_preferences: dict
    accommodation_options: list
    selected_accommodation: dict

    estimated_cost: dict

    final_itinerary: dict
```

The exact state model may evolve as the application grows.

---

# 14. Data Flow

A simplified data flow:

```text
User Input
    |
    v
Requirements State
    |
    v
Destination Agent
    |
    +------> Places Tool
    |
    +------> Geocoding Tool
    |
    v
Available Places
    |
    v
User Selects Places
    |
    v
Routing Tool
    |
    v
Distance / Duration
    |
    v
Itinerary Agent
    |
    v
Proposed Itinerary
    |
    v
User Approval
    |
    +---- Modify
    |
    +---- Accept
            |
            v
       Stay Agent
            |
            v
      Accommodation
            |
            v
      User Selection
            |
            v
      Final Planner
            |
            v
     Complete Itinerary
```

---

# 15. Important Design Principles

## 15.1 LLM for reasoning

Use the LLM for:

- Understanding user intent
- Asking questions
- Planning
- Ranking
- Reasoning
- Generating natural language

---

## 15.2 Tools for facts

Use tools for:

- Places
- Coordinates
- Distances
- Travel time
- Opening hours
- Accommodation data
- External information

---

## 15.3 Python for calculations

Use Python for:

- Cost calculation
- Date calculations
- Duration calculations
- Validation
- Filtering
- Sorting

---

## 15.4 User for important decisions

The user decides:

- Where to go
- Which places to visit
- Whether the itinerary is acceptable
- Where to stay
- Whether to modify the plan

---

# 16. Open-Source Data and Services

The project should prefer open-source and open-data services.

Potential services include:

### OpenStreetMap

Geographic and map data.

### Nominatim

Geocoding.

### Overpass API

Query OpenStreetMap data.

### OSRM

Routing.

### Leaflet

Interactive map rendering.

Always check the current usage policy, rate limits, attribution requirements, and terms of each public service before production deployment.

For production workloads, consider self-hosting or using an appropriate provider instead of depending on public endpoints.

---

# 17. MVP Scope

The first MVP should support only:

```text
Destination
    ↓
Trip requirements
    ↓
Place discovery
    ↓
User place selection
    ↓
Distance / travel time
    ↓
Itinerary
    ↓
User approval
    ↓
Accommodation preferences
    ↓
Accommodation options
    ↓
User selection
    ↓
Final itinerary
```

The MVP should NOT initially include:

- Flight booking
- Train booking
- Payment
- User authentication
- Advanced recommendation models
- Vector database
- RAG
- Kubernetes
- Complex microservices
- Multiple databases
- Real-time traffic
- Voice assistant

---

# 18. Future Enhancements

Once the MVP works, additional agents can be introduced.

## Weather Agent

```text
Weather Agent
      |
      v
Weather API
      |
      v
Itinerary Agent
```

It could suggest itinerary changes based on weather.

---

## Restaurant Agent

Find restaurants near itinerary locations.

---

## Transportation Agent

Compare:

- Public transport
- Taxi
- Rental car
- Self-drive

---

## Budget Agent

Optimize the itinerary based on a fixed budget.

---

## Supervisor Agent

Eventually a supervisor can coordinate specialized agents:

```text
                 Supervisor
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
 Destination      Stay        Transport
    Agent         Agent          Agent
       |             |             |
       +-------------+-------------+
                     |
                     v
              Itinerary Agent
                     |
                     v
               Final Planner
```

Do not implement this complexity until the basic workflow is working.

---

# 19. Development Roadmap

## Phase 1 — Python and Environment

Learn:

- Virtual environments
- Python project structure
- Dependencies
- Environment variables

Build the smallest runnable application.

---

## Phase 2 — LLM

Learn:

- Prompt
- System message
- User message
- Model
- Structured output

Create:

```text
User
 ↓
LLM
 ↓
Response
```

---

## Phase 3 — First LangGraph

Learn:

- State
- Node
- Edge
- Graph

Create:

```text
User
 ↓
Agent
 ↓
Response
```

---

## Phase 4 — Requirements Agent

Implement conversational requirements gathering.

---

## Phase 5 — Destination Agent

Search for attractions.

---

## Phase 6 — Geographic Tools

Add:

- Nominatim
- OpenStreetMap
- OSRM

---

## Phase 7 — Itinerary Agent

Generate multi-day plans.

---

## Phase 8 — Human Approval

Add approval and modification loops.

---

## Phase 9 — Stay Agent

Add accommodation workflow.

---

## Phase 10 — Final Planner

Generate the complete trip.

---

## Phase 11 — Frontend

Create the user interface.

---

## Phase 12 — Persistence

Add SQLite persistence.

---

## Phase 13 — Production Improvements

Consider:

- PostgreSQL
- Authentication
- Caching
- Observability
- Better API providers
- Self-hosted geographic services
- Deployment

---

# 20. Local Development

## Prerequisites

Install:

- Python 3.12+
- Git
- Ollama
- Node.js if using React/Next.js

Verify Python:

```bash
python --version
```

Verify Git:

```bash
git --version
```

Verify Ollama:

```bash
ollama --version
```

---

## Create Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Install an Ollama Model

Example:

```bash
ollama pull qwen3
```

The exact model should depend on the available hardware.

For local development, choose a model that your computer can run comfortably.

---

## Run the Application

Example:

```bash
python src/main.py
```

If the project exposes a FastAPI application:

```bash
uvicorn src.main:app --reload
```

The exact command may change as the project evolves.

---

# 21. Environment Variables

Use `.env` for configuration that should not be committed.

Example `.env.example`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3

DATABASE_URL=sqlite:///./travel_planner.db

NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org
OSRM_BASE_URL=https://router.project-osrm.org
```

Do not commit secrets.

Use:

```text
.env
```

in `.gitignore`.

---

# 22. Testing Strategy

Testing should happen at multiple levels.

## Unit Tests

Test individual tools.

Example:

```text
calculate_route()
calculate_trip_cost()
geocode_location()
```

---

## Agent Tests

Test whether an agent produces the expected structured output.

---

## Graph Tests

Test workflow transitions:

```text
Requirements
    ↓
Destination
    ↓
Itinerary
    ↓
Approval
```

---

## Human Approval Tests

Verify:

```text
Accept → Stay Agent
Modify → Itinerary Agent
```

---

## End-to-End Tests

Test the complete user journey.

Example:

```text
Bengaluru
3 days
2 travelers
₹15,000
```

Then verify that the application reaches the final itinerary.

---

# 23. Error Handling

The application must handle failures gracefully.

## Unknown Destination

```text
I couldn't confidently identify that destination.

Please provide the city and country.
```

---

## No Places Found

```text
I couldn't find suitable places in that destination.
```

---

## Routing Failure

```text
I couldn't retrieve route information right now.

Would you like to continue without travel-time estimates?
```

---

## No Accommodation

```text
I couldn't find accommodation matching all your preferences.

Would you like to:

1. Increase your budget
2. Expand the search area
3. Change accommodation type
```

---

# 24. Reliability and Hallucination Prevention

The application must prioritize factual accuracy.

## Never allow the LLM to invent:

- Tourist attractions
- Hotels
- Prices
- Distances
- Travel times
- Availability
- Booking confirmations

---

## Example

Bad:

```text
LLM:
The hotel costs ₹4,500 and has rooms available.
```

If no real source was consulted, this is unacceptable.

Better:

```text
Hotel:
ABC Hotel

Price:
₹4,500/night

Source:
External provider

Availability:
Not verified
```

---

# 25. Cost Calculation

The cost calculation should be performed by deterministic application code.

Example:

```text
Accommodation
= ₹4,500 × 2 nights
= ₹9,000

Transportation
= ₹3,000

Food
= ₹3,000

Activities
= ₹2,000

Miscellaneous
= ₹1,000

-------------------------
Estimated Total
= ₹18,000
```

Python should perform these calculations.

The LLM should explain the result to the user.

---

# 26. Booking Disclaimer

The initial version should not process payments or claim that bookings were completed.

The application should provide external booking information when available.

Example:

```text
Accommodation:

Hotel ABC

Estimated price:
₹4,500/night

Booking:
Visit external booking provider

Note:
Price and availability should be verified before booking.
```

---

# 27. Learning Objectives

This project is primarily a learning project for multi-agent AI.

By completing it, the developer should understand:

## LLM

A language model that generates and understands text.

---

## Agent

A system that uses an LLM to reason and decide what action to take.

---

## Tool

A function that an agent can call to perform a specific task.

---

## Tool Calling

The mechanism through which an LLM requests a tool execution.

---

## Structured Output

Returning predictable data instead of free-form text.

---

## State

The information maintained throughout the workflow.

---

## Node

A step in the LangGraph workflow.

---

## Edge

A connection between workflow steps.

---

## Conditional Edge

A decision that determines where the workflow should go next.

---

## Human-in-the-Loop

A workflow where a human can approve, reject, or modify an AI-generated result.

---

## Multi-Agent System

Multiple specialized agents working together.

---

## Supervisor

An agent that coordinates other agents.

---

## Subgraph

A reusable graph representing a specialized workflow.

---

## Memory

Information maintained across interactions or sessions.

---

## RAG

Retrieval-Augmented Generation.

RAG should only be introduced when the project has a genuine need for retrieving a knowledge base.

---

# 28. Production Evolution

The initial application can eventually evolve into:

```text
                         Frontend
                            |
                            v
                         FastAPI
                            |
                            v
                       Supervisor
                            |
          +-----------------+----------------+
          |                 |                |
          v                 v                v
   Destination Agent   Stay Agent     Transport Agent
          |                 |                |
          v                 v                v
      Places API        Hotel Data       Transport Data
          |                 |                |
          +-----------------+----------------+
                            |
                            v
                    Itinerary Agent
                            |
                            v
                       Cost Agent
                            |
                            v
                     Final Planner
                            |
                            v
                       Final Trip
```

Production infrastructure may eventually include:

- PostgreSQL
- Redis
- Background jobs
- API caching
- Authentication
- Monitoring
- Tracing
- Rate limiting
- Better routing providers
- Production accommodation providers
- Self-hosted geographic services

These should only be introduced when required.

---

# 29. Contributing

Contributions are welcome.

When contributing:

1. Keep changes focused.
2. Follow the existing project structure.
3. Add tests for new functionality.
4. Avoid unnecessary dependencies.
5. Prefer open-source solutions.
6. Document new agents and tools.
7. Do not introduce an agent where a normal function/tool is sufficient.

---

# 30. License

Choose an open-source license before publishing the project.

A permissive license such as MIT may be appropriate for this type of project, but the final license should be selected based on the project's intended use and dependencies.

Also review the licenses and usage policies of:

- LLM models
- OpenStreetMap data
- Nominatim
- OSRM
- Other external services

before distribution or commercial deployment.

---

# Project Philosophy

The most important principle of this project is:

> **Use AI for reasoning, tools for facts, code for deterministic operations, and humans for important decisions.**

The project should not try to make everything autonomous.

Instead, the goal is to build a reliable system where specialized AI agents and deterministic tools work together while keeping the user in control.

---

# Current MVP Goal

The first working version should achieve:

```text
User
  |
  | destination
  v
Requirements Agent
  |
  | preferences
  v
Destination Agent
  |
  | real places
  v
Places + Routing Tools
  |
  | distance / travel time
  v
Itinerary Agent
  |
  | proposed plan
  v
User Approval
  |
  | accepted
  v
Stay Agent
  |
  | accommodation
  v
User Selection
  |
  v
Final Planner
  |
  v
Complete Travel Itinerary
```

Start small.

Make every stage work.

Understand each component before adding the next one.

The objective is not just to build a travel application.

The objective is to **learn how to design, implement, debug, and evolve a real multi-agent AI system using open-source technologies.**
