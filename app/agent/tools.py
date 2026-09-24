class WorkOrderTool:
    def check(self, work_order_id: str) -> str:
        # Mock tool.
        if work_order_id.startswith("WO-"):
            return f"Work order {work_order_id} is active and pending inspection."
        return f"Work order {work_order_id} status is unknown; human verification required."
