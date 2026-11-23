import os
import re
from typing import List
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from src.agent_state import AgentState
from src import prompts

def get_llm(temperature: float = 0.85) -> ChatGroq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Set it in your environment or .env file.")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=api_key,
    )

def parse_versions(raw_text: str, expected: int) -> List[str]:
    parts = re.split(r"---\s*VERSION\s*\d+\s*---", raw_text, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) >= expected:
        return parts[:expected]
    return parts if parts else [raw_text.strip()]

def route_request(state: AgentState) -> AgentState:
    if state.get("content_type"):
        return state
    llm = get_llm(temperature=0)
    prompt = prompts.ROUTER_SYSTEM_PROMPT.format(request=state["request"])
    label = llm.invoke(prompt).content.strip().lower()
    valid = {"readme", "linkedin_post", "linkedin_about", "linkedin_headline", "custom"}
    state["content_type"] = label if label in valid else "custom"
    if state["content_type"] == "custom":
        state["custom_label"] = state.get("request", "personal branding content")
    return state

def route_decision(state: AgentState) -> str:
    return state["content_type"]

def _run_generator(template: str, state: AgentState, **extra) -> AgentState:
    n = state.get("num_variations", 5)
    llm = get_llm(temperature=0.85)
    prompt = template.format(
        context=state.get("context", "").strip() or "(no extra context given)",
        humanize_rules=prompts.HUMANIZE_RULES,
        variation_instruction=prompts.build_variation_instruction(n),
        **extra,
    )
    result = llm.invoke(prompt)
    state["outputs"] = parse_versions(result.content, n)
    return state

def generate_readme(state): return _run_generator(prompts.README_TEMPLATE, state)
def generate_linkedin_post(state): return _run_generator(prompts.LINKEDIN_POST_TEMPLATE, state)
def generate_linkedin_about(state): return _run_generator(prompts.LINKEDIN_ABOUT_TEMPLATE, state)
def generate_linkedin_headline(state): return _run_generator(prompts.LINKEDIN_HEADLINE_TEMPLATE, state)
def generate_custom(state):
    label = state.get("custom_label") or "personal branding content"
    return _run_generator(prompts.CUSTOM_TEMPLATE, state, content_type=label)

def build_profile_graph():
    graph = StateGraph(AgentState)
    graph.add_node("router", route_request)
    graph.add_node("readme", generate_readme)
    graph.add_node("linkedin_post", generate_linkedin_post)
    graph.add_node("linkedin_about", generate_linkedin_about)
    graph.add_node("linkedin_headline", generate_linkedin_headline)
    graph.add_node("custom", generate_custom)

    graph.set_entry_point("router")
    graph.add_conditional_edges("router", route_decision, {
        "readme": "readme",
        "linkedin_post": "linkedin_post",
        "linkedin_about": "linkedin_about",
        "linkedin_headline": "linkedin_headline",
        "custom": "custom",
    })
    for node in ["readme", "linkedin_post", "linkedin_about", "linkedin_headline", "custom"]:
        graph.add_edge(node, END)
    return graph.compile()
