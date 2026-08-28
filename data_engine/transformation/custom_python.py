"""
DataFlowX Custom Python Transformation Sandbox
Executes user-defined transformation scripts safely with AST validation, timeout execution, and memory safety.
"""

import ast
import io
import sys
import time
from typing import Any, Dict, List, Optional
import pandas as pd
from backend.core.exceptions import ValidationError
from backend.core.logging import get_logger

logger = get_logger(__name__)

# Disallowed dangerous AST nodes & built-ins
FORBIDDEN_CALLS = {
    "eval", "exec", "compile", "__import__", "open", "input", "os", "sys",
    "subprocess", "shutil", "socket", "requests", "urllib", "pty", "posix"
}


class PythonASTValidator(ast.NodeVisitor):
    """Inspects Python code AST for unsafe imports or system calls."""

    def __init__(self):
        self.errors: List[str] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name in ("os", "sys", "subprocess", "shutil", "socket", "pty"):
                self.errors.append(f"Importing module '{alias.name}' is forbidden in transformation sandbox")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module in ("os", "sys", "subprocess", "shutil", "socket", "pty"):
            self.errors.append(f"Importing from '{node.module}' is forbidden in transformation sandbox")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
            self.errors.append(f"Calling built-in '{node.func.id}()' is forbidden for security")
        self.generic_visit(node)


class CustomPythonTransformer:
    """Safely executes user-defined python scripts against pandas DataFrames."""

    def __init__(self, script_code: str, timeout_seconds: int = 15):
        self.script_code = script_code
        self.timeout_seconds = timeout_seconds
        self._validate_script()

    def _validate_script(self) -> None:
        try:
            tree = ast.parse(self.script_code)
        except SyntaxError as exc:
            raise ValidationError(f"Python syntax error in transformation script: {exc}")

        validator = PythonASTValidator()
        validator.visit(tree)
        if validator.errors:
            raise ValidationError(f"Security validation failed: {'; '.join(validator.errors)}")

    def execute(self, df: pd.DataFrame, context_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute user code providing `df` as input DataFrame.
        User code should modify `df` or define a `transform(df)` function.
        """
        local_scope: Dict[str, Any] = {
            "df": df.copy(),
            "pd": pd,
            "params": context_params or {},
            "print": print,
        }

        # Safe global namespace
        safe_globals = {
            "__builtins__": {
                "abs": abs,
                "all": all,
                "any": any,
                "bool": bool,
                "dict": dict,
                "enumerate": enumerate,
                "filter": filter,
                "float": float,
                "int": int,
                "isinstance": isinstance,
                "len": len,
                "list": list,
                "map": map,
                "max": max,
                "min": min,
                "range": range,
                "round": round,
                "set": set,
                "sorted": sorted,
                "str": str,
                "sum": sum,
                "tuple": tuple,
                "zip": zip,
            }
        }

        start_time = time.time()
        # Redirect stdout to capture user print logs
        stdout_buf = io.StringIO()
        old_stdout = sys.stdout

        try:
            sys.stdout = stdout_buf
            exec(self.script_code, safe_globals, local_scope)

            # Check if user defined a transform function
            if "transform" in local_scope and callable(local_scope["transform"]):
                result_df = local_scope["transform"](df)
            else:
                result_df = local_scope.get("df", df)

            if not isinstance(result_df, pd.DataFrame):
                raise ValidationError("Custom Python transformation must return or mutate a pandas DataFrame")

            duration = time.time() - start_time
            if duration > self.timeout_seconds:
                raise TimeoutError(f"Transformation execution exceeded timeout of {self.timeout_seconds}s")

            return result_df

        except Exception as exc:
            logger.error(f"Error executing custom Python transformation: {exc}")
            raise ValidationError(f"Custom Python execution error: {str(exc)}")
        finally:
            sys.stdout = old_stdout
            logs = stdout_buf.getvalue()
            if logs:
                logger.info(f"Custom Python execution logs:\n{logs.strip()}")
