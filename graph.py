from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from state import LeaveState
from nodes import employee_retrieval_agent, holiday_retrieval_agent, computation_agent, human_confirmation_node, persistence_agent


def route_after_computation(state: LeaveState) -> str:
    if state.get("status") == "REJECTED":
        return "end"
    return "human_confirmation"

# 1. Instantiate the Graph with our State schema
workflow = StateGraph(LeaveState)

# 2. Register all Agent Nodes
workflow.add_node("employee_retrieval", employee_retrieval_agent)
workflow.add_node("holiday_retrieval", holiday_retrieval_agent)
workflow.add_node("computation", computation_agent)
workflow.add_node("human_confirmation", human_confirmation_node)
workflow.add_node("persistence", persistence_agent)

# 3. Configure Parallel Execution:
# Branch directly from START into both retrieval agents concurrently
workflow.add_edge(START, "employee_retrieval")
workflow.add_edge(START, "holiday_retrieval")

# 4. Configure Sequential Merging:
# Computation agent waits until BOTH retrieval agents finish
workflow.add_edge("employee_retrieval", "computation")
workflow.add_edge("holiday_retrieval", "computation")

# 5. Connect Human Confirmation and Database Persistence sequentially
workflow.add_conditional_edges(
    "computation",
    route_after_computation,
    {
        "human_confirmation": "human_confirmation",
        "end": END
    }
)
workflow.add_edge("human_confirmation", "persistence")
workflow.add_edge("persistence", END)

# 6. Compile the Graph with Checkpointing & HITL Interruption
memory = MemorySaver()
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_confirmation"]  # Graph automatically pauses right before executing this node
)
