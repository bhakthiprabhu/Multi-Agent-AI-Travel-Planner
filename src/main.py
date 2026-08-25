import re

from typing_extensions import TypedDict

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


class TravelRequirements(BaseModel):
    destination: str | None = Field(default=None, description="Travel destination")
    number_of_days: int | None = Field(default=None, description="Number of travel days")
    number_of_travelers: int | None = Field(default=None, description="Number of travelers")
    budget: float | None = Field(default=None, description="Total trip budget")
    currency: str | None = Field(default=None, description="Budget currency")
    transportation_preference: str | None = Field(
        default=None, description="Transportation preference"
    )


class TripState(TypedDict, total=False):
    user_message: str
    expected_field: str | None
    destination: str | None
    number_of_days: int | None
    number_of_travelers: int | None
    budget: float | None
    currency: str | None
    transportation_preference: str | None


REQUIRED_FIELDS = [
    "destination",
    "number_of_days",
    "number_of_travelers",
    "budget",
    "transportation_preference",
]

INITIAL_TRIP_PROMPT = """
Where would you like to travel?
Please provide a city and country when possible.

Example:
Bengaluru, India
"""

QUESTIONS = {
    "destination": (
        "Where would you like to travel?\n"
        "Please provide a city and country when possible.\n"
        "Example: Bengaluru, India"
    ),
    "number_of_days": "How many days would you like the trip to be?\nExample: 3 days",
    "number_of_travelers": "How many people are travelling?\nExample: 2 people",
    "budget": "What is your approximate total trip budget?\nExample: ₹12,000 total for the trip",
    "transportation_preference": (
        "How would you prefer to travel locally?\n"
        "Examples: cab, public transport, self-drive, rental vehicle, or a combination"
    ),
}


llm = ChatOllama(
    model="qwen3:4b",
    temperature=0,
    reasoning=False,
    num_predict=100,
    num_ctx=1024,
    keep_alive="30m",
)
structured_llm = llm.with_structured_output(TravelRequirements)


def requirements_node(state: TripState) -> dict:
    expected_field = state.get("expected_field")
    prompt = f"""
You are a travel requirements extraction assistant.

The user is currently answering the {expected_field} question.
Extract only information explicitly provided by the user. Do not invent missing
information. Convert obvious number words to numbers. Extract budget as a numeric
value and identify currency when provided. Do not create an itinerary or recommend places.

User message:
{state["user_message"]}
"""
    requirements = structured_llm.invoke(prompt)
    extracted = {
        "destination": requirements.destination,
        "number_of_days": requirements.number_of_days,
        "number_of_travelers": requirements.number_of_travelers,
        "budget": requirements.budget,
        "currency": requirements.currency,
        "transportation_preference": requirements.transportation_preference,
    }
    return {field: value for field, value in extracted.items() if value is not None}


def next_missing_field(state: TripState) -> str | None:
    for field in REQUIRED_FIELDS:
        if state.get(field) is None:
            return field
    return None


def parse_expected_answer(field: str, user_message: str) -> dict:
    answer = user_message.strip()
    normalized_answer = answer.lower()

    if field in {"destination", "initial_trip_description"}:
        looks_like_location = (
            answer
            and len(answer) <= 80
            and not re.search(r"\d|\bbudget\b|\bpeople\b|\bdays?\b", normalized_answer)
        )
        if looks_like_location:
            return {"destination": answer}

    if field == "number_of_days":
        match = re.fullmatch(r"(\d+)\s*(?:day|days)?", normalized_answer)
        if match and int(match.group(1)) > 0:
            return {"number_of_days": int(match.group(1))}

    if field == "number_of_travelers":
        match = re.fullmatch(r"(\d+)\s*(?:person|people|traveler|travelers)?", normalized_answer)
        if match and int(match.group(1)) > 0:
            return {"number_of_travelers": int(match.group(1))}

    if field == "budget":
        match = re.fullmatch(
            r"(?:₹|rs\.?\s*|inr\s*)?([\d,]+(?:\.\d+)?)\s*(?:rupees?|inr)?",
            normalized_answer,
        )
        if match:
            budget = float(match.group(1).replace(",", ""))
            if budget > 0:
                parsed = {"budget": budget}
                if re.search(r"₹|\brs\.?\b|\binr\b|\brupees?\b", normalized_answer):
                    parsed["currency"] = "INR"
                return parsed

    return {}


def merge_requirements(state: TripState, extracted: dict, expected_field: str, parsed_answer: dict) -> None:
    for field, value in extracted.items():
        if state.get(field) is None or field == expected_field or field == "currency":
            state[field] = value
    state.update(parsed_answer)


def print_trip_summary(state: TripState) -> None:
    print("\nTrip requirements collected:")
    print(f"Destination: {state.get('destination')}")
    print(f"Days: {state.get('number_of_days')}")
    print(f"Travelers: {state.get('number_of_travelers')}")
    print(f"Budget: {state.get('budget')} {state.get('currency') or ''}".rstrip())
    print(f"Transportation: {state.get('transportation_preference')}")


builder = StateGraph(TripState)
builder.add_node("requirements", requirements_node)
builder.add_edge(START, "requirements")
builder.add_edge("requirements", END)
graph = builder.compile()


state: TripState = {}

while True:
    has_requirements = any(state.get(field) is not None for field in REQUIRED_FIELDS)
    if not has_requirements:
        expected_field = "initial_trip_description"
        user_message = input(f"\n{INITIAL_TRIP_PROMPT}\nYou: ")
    else:
        missing = next_missing_field(state)
        if missing is None:
            print_trip_summary(state)
            break
        expected_field = missing
        user_message = input(f"\n{QUESTIONS[missing]}\nYou: ")

    if user_message.strip().lower() == "start over":
        state = {}
        print("Trip requirements cleared. Let's start again.")
        continue

    parsed_answer = parse_expected_answer(expected_field, user_message)
    if parsed_answer:
        merge_requirements(state, {}, expected_field, parsed_answer)
        continue

    result = graph.invoke({
        **state,
        "expected_field": expected_field,
        "user_message": user_message,
    })
    extracted = {
        field: result[field]
        for field in result
        if field in REQUIRED_FIELDS or field == "currency"
    }
    merge_requirements(state, extracted, expected_field, {})
