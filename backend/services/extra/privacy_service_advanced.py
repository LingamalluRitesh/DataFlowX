"""
DataFlowX Advanced Privacy Service Layer
Executes K-Anonymity suppression, Laplace differential privacy noise injections, and T-Closeness audits.
"""

from typing import List, Optional
import pandas as pd
from data_engine.privacy.k_anonymity import KAnonymityEngine, KAnonymityReport
from data_engine.privacy.l_diversity import LDiversityEngine, LDiversityReport
from data_engine.privacy.laplace_mechanism import DifferentialPrivacyLaplace
from data_engine.privacy.t_closeness import TClosenessEngine, TClosenessReport


class AdvancedPrivacyService:
    """Service layer for mathematical privacy preservation."""

    @classmethod
    def audit_dataset_privacy(
        cls,
        df: pd.DataFrame,
        quasi_identifiers: List[str],
        sensitive_column: Optional[str] = None
    ) -> dict:
        k_rep = KAnonymityEngine.evaluate_k_anonymity(df, quasi_identifiers)
        l_rep = LDiversityEngine.evaluate_distinct_l_diversity(df, quasi_identifiers, sensitive_column) if sensitive_column else None
        t_rep = TClosenessEngine.evaluate_t_closeness(df, quasi_identifiers, sensitive_column) if sensitive_column else None

        return {
            "k_anonymity": k_rep,
            "l_diversity": l_rep,
            "t_closeness": t_rep,
        }
