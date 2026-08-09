"""Dynamic Synthesis & Parameterized Academic Sizing Engine.

Provides algorithmic Function Point analysis, Basic COCOMO effort/cost
derivation, and dynamic markdown report generation parameterized by custom
system inputs and grounded via multi-modal RAG context blocks.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Final

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_modal import (
    COCOMOModel,
    COCOMOResult,
    FPSizingResult,
    ProjectParameters,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger: Final[logging.Logger] = logging.getLogger("SynthesisEngine")


def compute_unadjusted_function_points(
    inputs: int,
    outputs: int,
    inquiries: int,
    internal_files: int,
    external_interfaces: int,
) -> int:
    """Computes Unadjusted Function Points using standard IFPUG average weights.

    Args:
        inputs: Count of external input transactions (weight: 4).
        outputs: Count of external output reports/responses (weight: 5).
        inquiries: Count of external inquiry queries (weight: 4).
        internal_files: Count of internal logical data stores (weight: 10).
        external_interfaces: Count of external shared interfaces (weight: 7).

    Returns:
        int: Total Unadjusted Function Points (UFP).
    """
    return (
        (inputs * 4)
        + (outputs * 5)
        + (inquiries * 4)
        + (internal_files * 10)
        + (external_interfaces * 7)
    )


def compute_value_adjustment_factor(degrees_of_influence_sum: int) -> float:
    """Computes the Value Adjustment Factor (VAF) from 14 General System
    Characteristics.

    Args:
        degrees_of_influence_sum: Total sum of ratings across all 14 GSCs (0 to 70).

    Returns:
        float: Computed VAF rounded to 4 decimal places.
    """
    vaf: float = 0.65 + (0.01 * degrees_of_influence_sum)
    return round(vaf, 4)


def compute_function_points(params: ProjectParameters) -> FPSizingResult:
    """Calculates complete Function Point sizing and derived KLOC from parameters.

    Args:
        params: Project configuration parameters.

    Returns:
        FPSizingResult: Calculated UFP, VAF, AFP, and derived KLOC.
    """
    ufp: int = compute_unadjusted_function_points(
        inputs=params.ufp_inputs,
        outputs=params.ufp_outputs,
        inquiries=params.ufp_inquiries,
        internal_files=params.ufp_internal_files,
        external_interfaces=params.ufp_external_interfaces,
    )
    vaf: float = compute_value_adjustment_factor(
        degrees_of_influence_sum=params.complexity_adjustment_factors_sum
    )
    afp: float = round(ufp * vaf, 2)
    kloc: float = round((afp * params.loc_per_function_point) / 1000.0, 2)

    logger.info(
        f"Computed FP Sizing for {params.system_name}: "
        f"UFP={ufp}, AFP={afp}, KLOC={kloc}"
    )
    return FPSizingResult(
        unadjusted_function_points=ufp,
        value_adjustment_factor=vaf,
        adjusted_function_points=afp,
        derived_kloc=kloc,
    )


def compute_cocomo_metrics(
    kloc: float,
    mode: COCOMOModel = COCOMOModel.SEMIDETACHED,
    labor_rate_usd: float = 8500.0,
) -> COCOMOResult:
    """Computes Basic COCOMO effort, nominal schedule, staffing, and total cost.

    Args:
        kloc: Thousands of source lines of code.
        mode: Organic, Semidetached, or Embedded project classification.
        labor_rate_usd: Monthly blended cost per engineer in USD.

    Returns:
        COCOMOResult: Full estimation breakdown.
    """
    coefficients: dict[COCOMOModel, tuple[float, float, float, float]] = {
        COCOMOModel.ORGANIC: (2.4, 1.05, 2.5, 0.38),
        COCOMOModel.SEMIDETACHED: (3.0, 1.12, 2.5, 0.35),
        COCOMOModel.EMBEDDED: (3.6, 1.20, 2.5, 0.32),
    }

    a, b, c, d = coefficients[mode]

    effort_pm: float = round(a * (kloc**b), 2)
    dev_time_months: float = round(c * (effort_pm**d), 2)
    staff_size: float = (
        round(effort_pm / dev_time_months, 2) if dev_time_months > 0 else 0.0
    )
    total_cost_usd: float = round(effort_pm * labor_rate_usd, 2)
    productivity_loc_pm: float = (
        round((kloc * 1000.0) / effort_pm, 2) if effort_pm > 0 else 0.0
    )

    logger.info(
        f"Computed COCOMO ({mode.value}): Effort={effort_pm} PM, "
        f"Schedule={dev_time_months} Mo, Staff={staff_size} Eng"
    )

    return COCOMOResult(
        effort_person_months=effort_pm,
        development_time_months=dev_time_months,
        average_staff_size=staff_size,
        estimated_total_cost_usd=total_cost_usd,
        productivity_loc_per_pm=productivity_loc_pm,
    )


def synthesize_dynamic_report_markdown(
    params: ProjectParameters,
    fp_result: FPSizingResult,
    cocomo_result: COCOMOResult,
    rag_citations: dict[str, str] | None = None,
) -> str:
    """Dynamically synthesizes the comprehensive 4-Task academic solution report.

    Args:
        params: Configured project parameters.
        fp_result: Calculated Function Point metrics.
        cocomo_result: Calculated COCOMO effort and schedule metrics.
        rag_citations: Optional dictionary of grounded courseware citations.

    Returns:
        str: Grounded master Markdown document ready for vector diagram injection.
    """
    sys_name: str = params.system_name
    citations: dict[str, str] = rag_citations or {}

    task1_citation: str = citations.get(
        "task1", "CS05_UnderstandingRequirements.pdf (Slide 25)"
    )
    task2_citation: str = citations.get(
        "task2", "CS06_AnalysisModel.pdf (Slides 12-18)"
    )
    task3_citation: str = citations.get(
        "task3", "CS-08__Architectural Design.pdf (Slides 45-52)"
    )
    task4_citation: str = citations.get(
        "task4", "CS12_SoftwareTestingProcess.pdf & Lecture 11"
    )

    return f"""# {sys_name} - Software Engineering Assignment Report

**Course**: SE ZG343 Software Engineering (BITS Pilani WILP)  
**Author**: Arabindaksha Mishra  
**Target Domain**: {params.domain}  
**Synthesis Mode**: Parameterized Dynamic Academic Engine  

---

## Executive Summary & System Scope

The **{sys_name}** is an industrial-grade, cloud-native software architecture designed
for {params.domain}. It orchestrates real-time 3D airspace deconfliction, dynamic
vertiport load balancing, and high-frequency telemetry processing under mission-critical
safety standards.

```mermaid
graph TD
    A[{sys_name} Central Cloud] --> B[Edge Gateways]
    A --> C[Campus Vertiports]
```

---

## Task 1: Software Requirements Specification (IEEE 830)

*Academic Grounding Source: {task1_citation}*

### 1.1 Core Functional Requirements (FR)

1. **FR-01: Real-Time Airspace Corridor Allocation**: The system shall dynamically
assign 3D safety bounding corridors with sub-second collision avoidance checks.
2. **FR-02: Vertiport Dynamic Load Balancing**: When pad utilization exceeds 85%, the
system shall reroute approaching UAVs to the nearest auxiliary vertiport.
3. **FR-03: Autonomous Mission Execution & Battery Gateways**: Validates payload weight
and battery state of charge (SoC) prior to flight path clearance.
4. **FR-04: Automated Billing & Smart Metering**: Generates per-second kilowatt-hour and
corridor transit invoices automatically upon landing.
5. **FR-05: Real-Time Radar SCADA Integration**: Continuously reconciles edge ADS-B
radar observations with planned flight paths.

### 1.2 Non-Functional Metrics (NFR)

* **NFR-01 (Latency)**: 99th percentile end-to-end command dispatch latency shall not
exceed **{params.nfr_latency_p99_ms} ms**.
* **NFR-02 (Availability)**: Central cloud control plane shall maintain
**{params.nfr_availability_pct}%** uptime across redundant availability zones.
* **NFR-03 (Throughput)**: Ingestion pipeline shall sustain telemetry streams at
**{params.nfr_telemetry_hz} Hz** across 5,000 concurrent UAV nodes.

```mermaid
graph LR
    User[Operator] --> Auth[OAuth2 Gate]
```

---

## Task 2: Behavioral & Activity Modeling

*Academic Grounding Source: {task2_citation}*

The dynamic load balancing and emergency landing activity workflow enforces safe drone
rerouting during severe vertiport congestion:

```mermaid
stateDiagram-v2
    [*] --> Standby
```

---

## Task 3: 4+1 View & Microservices Architecture

*Academic Grounding Source: {task3_citation}*

### 3.1 Logical View & Domain Class Model

```mermaid
classDiagram
    class FlightPlan {{
        +UUID planId
        +validate()
    }}
```

### 3.2 Component & Microservices Architecture

```mermaid
graph TB
    API[Envoy Gateway] --> Kafka[Apache Kafka]
```

---

## Task 4: Software Sizing & Effort Estimation

*Academic Grounding Source: {task4_citation}*

### 4.1 Function Point Analysis (FPA)

$$\\text{{UFP}} = (EI \\times 4) + (EO \\times 5) + (EQ \\times 4) + (ILF \\times 10) +
(EIF \\times 7) = {fp_result.unadjusted_function_points}$$

$$\\text{{VAF}} = 0.65 + (0.01 \\times \\sum TDI) = 0.65 + (0.01 \\times
{params.complexity_adjustment_factors_sum}) = {fp_result.value_adjustment_factor}$$

$$\\text{{AFP}} = \\text{{UFP}} \\times \\text{{VAF}} =
{fp_result.unadjusted_function_points} \\times {fp_result.value_adjustment_factor} =
{fp_result.adjusted_function_points}\\text{{ FP}}$$

$$\\text{{Derived KLOC}} = \\frac{{{fp_result.adjusted_function_points} \\times
{params.loc_per_function_point}}}{{1000}} = {fp_result.derived_kloc}\\text{{ KLOC}}$$

### 4.2 Basic COCOMO Estimation ({params.cocomo_category.value.title()} Mode)

$$\\text{{Effort (Person-Months)}} = {cocomo_result.effort_person_months}\\text{{ PM}}$$

$$\\text{{Nominal Schedule}} = {cocomo_result.development_time_months}\\text{{ Calendar
Months}}$$

$$\\text{{Average Staff Size}} = {cocomo_result.average_staff_size}\\text{{ Full-Time
Engineers}}$$

$$\\text{{Estimated Total Engineering Cost}} =
\\${cocomo_result.estimated_total_cost_usd:,.2f}\\text{{ USD}}$$

$$\\text{{Engineering Productivity}} = {cocomo_result.productivity_loc_per_pm}\\text{{
LOC / Person-Month}}$$

---
*Report generated dynamically by Academic RAG Synthesis Engine.*
"""
