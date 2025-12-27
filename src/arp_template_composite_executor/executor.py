from __future__ import annotations

from arp_standard_model import (
    CompositeBeginRequest,
    CompositeBeginResponse,
    CompositeExecutorBeginCompositeNodeRunRequest,
    CompositeExecutorCancelCompositeNodeRunRequest,
    CompositeExecutorHealthRequest,
    CompositeExecutorVersionRequest,
    Health,
    Status,
    VersionInfo,
)
from arp_standard_server.composite_executor import BaseCompositeExecutorServer

from . import __version__
from .run_coordinator_client import RunCoordinatorGatewayClient
from .utils import now


class CompositeExecutor(BaseCompositeExecutorServer):
    """Composite execution surface; plug your composite engine here."""

    # Core method - API surface and main extension points
    def __init__(
        self,
        *,
        service_name: str = "arp-template-composite-executor",
        service_version: str = __version__,
        run_coordinator: RunCoordinatorGatewayClient | None = None,
    ) -> None:
        """
        Not part of ARP spec; required to construct the executor.

        Args:
          - service_name: Name exposed by /v1/version.
          - service_version: Version exposed by /v1/version.
          - run_coordinator: Optional wrapper for Run Coordinator calls.

        Potential modifications:
          - Inject your composite planner/executor implementation.
          - Add background task orchestration or queues.
        """
        self._service_name = service_name
        self._service_version = service_version
        self._run_coordinator = run_coordinator

    # Core methods - Composite Executor API implementations
    async def health(self, request: CompositeExecutorHealthRequest) -> Health:
        """
        Mandatory: Required by the ARP Composite Executor API.

        Args:
          - request: CompositeExecutorHealthRequest (unused).
        """
        _ = request
        return Health(status=Status.ok, time=now())

    async def version(self, request: CompositeExecutorVersionRequest) -> VersionInfo:
        """
        Mandatory: Required by the ARP Composite Executor API.

        Args:
          - request: CompositeExecutorVersionRequest (unused).
        """
        _ = request
        return VersionInfo(
            service_name=self._service_name,
            service_version=self._service_version,
            supported_api_versions=["v1"],
        )

    async def begin_composite_node_run(
        self, request: CompositeExecutorBeginCompositeNodeRunRequest
    ) -> CompositeBeginResponse:
        """
        Mandatory: Required by the ARP Composite Executor API.

        Args:
          - request: CompositeExecutorBeginCompositeNodeRunRequest with assignment info.

        Potential modifications:
          - Kick off background execution and return accepted=true.
          - Validate constraints before accepting.
        """
        return self._begin(request.body)

    async def cancel_composite_node_run(self, request: CompositeExecutorCancelCompositeNodeRunRequest) -> None:
        """
        Mandatory: Required by the ARP Composite Executor API.

        Args:
          - request: CompositeExecutorCancelCompositeNodeRunRequest with node_run_id.

        Potential modifications:
          - Add cooperative cancellation to your composite executor implementation.
        """
        _ = request
        return None

    # Helpers (internal): implementation detail for the template.
    def _begin(self, request: CompositeBeginRequest) -> CompositeBeginResponse:
        """Minimal composite begin handler (edit/extend this)."""
        return CompositeBeginResponse(
            accepted=True,
            message="Composite assignment accepted (template).",
        )
