from sqlalchemy import Column, String, Float, Integer, JSON
from app.core.database.session import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True)
    timestamp = Column(String, nullable=False)
    query = Column(String, nullable=False)
    work_order_id = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    defect_category = Column(String, nullable=True)
    ocr_text = Column(String, nullable=True)
    configuration_json = Column(JSON, nullable=False)
    decision_trace_json = Column(JSON, nullable=False)
    final_answer = Column(String, nullable=False)
    latency_ms = Column(Float, nullable=False)
    proposed_action_json = Column(JSON, nullable=True)
    feedback_score = Column(Integer, nullable=True)
    reward = Column(Float, nullable=True)

    @property
    def configuration(self):
        return self.configuration_json

    @property
    def decision_trace(self):
        return self.decision_trace_json

    @property
    def proposed_action(self):
        return self.proposed_action_json

