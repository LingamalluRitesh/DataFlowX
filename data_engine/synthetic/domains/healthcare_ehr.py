"""
DataFlowX Healthcare EHR & Clinical Encounters Benchmark Generator
Generates synthetic HIPAA-compliant Electronic Health Record (EHR) data: clinical encounters, ICD-10 diagnosis codes, CPT procedure codes, and vitals.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class HealthcareEHRGenerator:
    """Generates synthetic patient encounters and ICD-10 clinical records."""

    ICD10_CODES = [
        ("I10", "Essential (primary) hypertension"),
        ("E11.9", "Type 2 diabetes mellitus without complications"),
        ("J45.909", "Unspecified asthma, uncomplicated"),
        ("M54.5", "Low back pain"),
        ("F41.1", "Generalized anxiety disorder"),
        ("K21.9", "Gastro-esophageal reflux disease without esophagitis"),
    ]

    DEPARTMENTS = ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Oncology"]

    @classmethod
    def generate_encounters(cls, num_encounters: int = 20000) -> pd.DataFrame:
        encounter_ids = np.arange(500000, 500000 + num_encounters)
        patient_ids = np.random.randint(10000, 99999, size=num_encounters)
        departments = np.random.choice(cls.DEPARTMENTS, size=num_encounters)

        icd_indices = np.random.randint(0, len(cls.ICD10_CODES), size=num_encounters)
        icd_codes = [cls.ICD10_CODES[i][0] for i in icd_indices]
        icd_descs = [cls.ICD10_CODES[i][1] for i in icd_indices]

        systolic = np.random.randint(100, 160, size=num_encounters)
        diastolic = np.random.randint(60, 100, size=num_encounters)

        now = datetime.now(timezone.utc)
        timestamps = [now - timedelta(hours=int(i % 720)) for i in range(num_encounters)]

        return pd.DataFrame({
            "encounter_id": [f"ENC-{eid}" for eid in encounter_ids],
            "patient_id": [f"PAT-{pid}" for pid in patient_ids],
            "department": departments,
            "icd10_code": icd_codes,
            "diagnosis_description": icd_descs,
            "systolic_bp": systolic,
            "diastolic_bp": diastolic,
            "admitted_at": [ts.isoformat() for ts in timestamps]
        })
