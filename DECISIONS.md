# SECTION G: 

**1. Why vector RAG (vs. a vectorless/long-context read) fits this SOP corpus — and what would change your answer if the plant's SOP set were fixed at 20 pages instead of continuously growing.**

Vector RAG is ideal for a continuously growing SOP corpus because it isolates the specific rules related to a query, minimizing prompt token costs, reducing latency, and mitigating hallucination risks caused by irrelevant policies. If the SOPs were rigidly fixed at 20 pages, a vectorless long-context read (coupled with prompt caching) would be vastly superior; modern LLMs can easily ingest a 20-page context window, completely eliminating the maintenance overhead, indexing latency, and retrieval-miss risks associated with managing a vector database.

**2. Why an agent loop (vs. a fixed pipeline) is justified for the tool-selection step here — and name the one part of this system you would NOT make agentic, and why.**

An agent loop is justified for tool selection because shop floor queries are highly variable (e.g., text-only questions vs. image-only defect checks vs. hybrid queries requiring sequential CV, OCR, and DB lookups); a fixed pipeline would rigidly execute unneeded steps, wasting latency, or fail on unanticipated inputs. I would absolutely NOT make the final escalation or ERP-write workflows agentic. Any action that alters physical machinery, scraps inventory, or writes to a database must remain a deterministic, hard-coded, and human-gated pipeline to prevent catastrophic financial or safety incidents caused by LLM hallucinations.



**3. Why you chose classical CV, a pretrained model, or both for the defect classifier — and what would push you to fine-tune a custom model instead.**


I chose a lightweight classical CV approach (OpenCV) because the defects in this scenario present clear, deterministic visual features (e.g., Hough lines for scratches, distinct color thresholding for dimensional markers) that operate with ultra-low latency and minimal compute footprint on edge devices. I would pivot to fine-tuning a custom model (like YOLOv8) if the defect variations became highly heterogeneous (e.g., subtle metallic oxidation, dynamic lighting conditions, varied backgrounds) where hand-coded pixel thresholds become brittle and impossible to maintain.



**4. If this pilot needed to scale from one plant to ten, which cost-optimization lever — prompt/response caching, model tiering, batching, a smaller fine-tuned model, or quantization — would you apply first, and why that one before the others.**

I would apply **prompt/response caching** (semantic caching) first. In a manufacturing environment, line workers encounter and query identical issues repeatedly across different shifts and plants (e.g., "what is the tolerance for a 3mm surface scratch"). Caching intercepts the majority of these redundant queries at the API edge, instantly reducing LLM compute costs and latency to near-zero with very low implementation effort, yielding the highest immediate ROI before investing into complex architectural changes like model quantization or fine-tuning.



**5. Name one governance risk specific to a shop floor (not a generic AI risk) that this design does not yet fully address, and how you'd close it in a real engagement.**

This design does not fully address the risk of **automation complacency (shadow adherence)**, where workers begin blindly trusting the AI's defect categorizations without verifying them, potentially allowing out-of-spec parts to pass QA due to a CV false negative. In a real engagement, I would close this by implementing a dynamic confidence threshold and random forced-audits: the UI would occasionally hide the AI's prediction and force the supervisor to manually categorize the defect first, tracking the delta between human and machine to continuously calibrate both the model's accuracy and the operator's vigilance. In photo we cann't capture the depth of the scratch fully it is also a limitation of this system.
