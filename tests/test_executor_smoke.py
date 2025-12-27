import asyncio

from arp_standard_model import (
    CompositeBeginRequest,
    CompositeExecutorBeginCompositeNodeRunRequest,
    EndpointLocator,
    NodeTypeRef,
)
from arp_template_composite_executor.executor import CompositeExecutor


def test_begin_composite_node_run_accepts() -> None:
    executor = CompositeExecutor()
    request = CompositeExecutorBeginCompositeNodeRunRequest(
        body=CompositeBeginRequest(
            run_id="run_1",
            node_run_id="node_run_1",
            node_type_ref=NodeTypeRef(node_type_id="composite.echo", version="0.1.0"),
            inputs={"goal": "test"},
            coordinator_endpoint=EndpointLocator("http://127.0.0.1:8081"),
        )
    )

    result = asyncio.run(executor.begin_composite_node_run(request))

    assert result.accepted is True
