from __future__ import annotations

from typing import Any

from arp_standard_model import (
    Candidate,
    CandidateSet,
    NodeKind,
    NodeRun,
    NodeRunEvaluationReportRequest,
    NodeRunState,
    NodeRunsCreateRequest,
    NodeRunsCreateResponse,
    NodeType,
    NodeTypeRef,
)


def make_node_type(*, node_type_id: str, version: str, input_schema: dict[str, Any]) -> NodeType:
    return NodeType(
        node_type_id=node_type_id,
        version=version,
        kind=NodeKind.atomic,
        description="Test node type",
        input_schema=input_schema,
    )


def make_candidate_set(*, candidate: NodeTypeRef) -> CandidateSet:
    return CandidateSet(
        candidate_set_id="candidate_set_1",
        subtask_id="subtask_1",
        candidates=[Candidate(node_type_ref=candidate, score=1.0, rationale="first")],
        top_k=1,
    )


class FakeSelection:
    def __init__(self, candidate_set: CandidateSet) -> None:
        self._candidate_set = candidate_set
        self.requests: list[object] = []

    async def generate_candidate_set(self, body) -> CandidateSet:
        self.requests.append(body)
        return self._candidate_set


class FakeNodeRegistry:
    def __init__(self, node_type: NodeType) -> None:
        self._node_type = node_type
        self.requests: list[tuple[str, str | None]] = []

    async def get_node_type(self, node_type_id: str, version: str | None = None) -> NodeType:
        self.requests.append((node_type_id, version))
        return self._node_type


class FakeRunCoordinator:
    def __init__(self) -> None:
        self.created: list[NodeRunsCreateRequest] = []
        self.completed: list[tuple[str, object]] = []
        self.evaluations: list[tuple[str, NodeRunEvaluationReportRequest]] = []
        self._node_runs: dict[str, NodeRun] = {}

    async def create_node_runs(self, body: NodeRunsCreateRequest) -> NodeRunsCreateResponse:
        self.created.append(body)
        node_run_id = f"child-{len(self._node_runs)}"
        node_run = NodeRun(
            node_run_id=node_run_id,
            node_type_ref=body.node_runs[0].node_type_ref,
            state=NodeRunState.succeeded,
            run_id=body.run_id,
            outputs={"ok": True},
        )
        self._node_runs[node_run_id] = node_run
        return NodeRunsCreateResponse(node_runs=[node_run])

    async def get_node_run(self, node_run_id: str) -> NodeRun:
        return self._node_runs[node_run_id]

    async def report_node_run_evaluation(self, node_run_id: str, body: NodeRunEvaluationReportRequest) -> None:
        self.evaluations.append((node_run_id, body))

    async def complete_node_run(self, node_run_id: str, body) -> None:
        self.completed.append((node_run_id, body))
