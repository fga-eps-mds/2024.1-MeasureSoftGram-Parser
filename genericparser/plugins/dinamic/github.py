import os
from genericparser.plugins.domain.generic_class import GenericStaticABC
import requests
from datetime import datetime


class ParserGithub(GenericStaticABC):
    token = None

    def __init__(self, token=None):
        self.token = token

    def _make_request(self, url, token=None):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print("error making request to github api in url: ", url, e)
        return response.json() if response.status_code == 200 else {}

    def _get_ci_feedback_times(self, base_url, token=None):
        ci_feedback_times = []
        url = f"{base_url}/actions/runs"
        response = self._make_request(url, token)

        if response is not None:
            workflow_runs = response.get("workflow_runs", [])

            for run in workflow_runs:
                started_at = datetime.fromisoformat(
                    run["created_at"].replace("Z", "+00:00")
                )
                completed_at = datetime.fromisoformat(
                    run["updated_at"].replace("Z", "+00:00")
                )
                feedback_time = completed_at - started_at
                ci_feedback_times.append(int(feedback_time.total_seconds()))

            result = {
                "metrics": ["sum_ci_feedback_times", "total_builds"],
                "values": [sum(ci_feedback_times), len(ci_feedback_times)],
            }

            return result
        else:
            return False

    def _get_pull_metrics_by_threshold(self, base_url, token=None):
        values = []
        url = f"{base_url}/pulls?state=all"
        response = self._make_request(url, token)
        pull_requests = response if isinstance(response, list) else []
        total_issues = len(pull_requests)
        resolved_issues = sum(1 for pr in pull_requests if pr["state"] == "closed")

        values.extend(
            [
                total_issues,
                resolved_issues,
                resolved_issues / total_issues if total_issues > 0 else 0,
            ]
        )

        return {
            "metrics": ["total_issues", "resolved_issues", "resolved_ratio"],
            "values": values,
        }

    def extract(self, input_file):
        token_from_github = (
            input_file.get("token", None)
            if type(input_file) is dict
            else None or os.environ.get("GITHUB_TOKEN", None) or self.token
        )
        repository = (
            input_file.get("repository", None)
            if (type(input_file) is dict)
            else input_file
        )
        metrics = []
        keys = repository
        values = []
        owner, repository_name = repository.split("/")
        url = f"https://api.github.com/repos/{owner}/{repository_name}"

        return_of_get_pull_metrics_by_threshold = self._get_pull_metrics_by_threshold(
            url, token_from_github
        )
        metrics.extend(return_of_get_pull_metrics_by_threshold["metrics"])
        values.extend(return_of_get_pull_metrics_by_threshold["values"])

        return_of_get_ci_feedback_times = self._get_ci_feedback_times(
            url, token_from_github
        )

        if return_of_get_ci_feedback_times:
            metrics.extend(return_of_get_ci_feedback_times["metrics"])
            values.extend(return_of_get_ci_feedback_times["values"])

        return {"metrics": metrics, "values": values, "file_paths": keys}


def main():
    return ParserGithub()
