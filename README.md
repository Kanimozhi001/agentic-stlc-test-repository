# Agentic STLC test repository

This repository contains sample UI tests (pytest/Playwright), API tests
(Karate), and a demo application for exercising them. The demo is deliberately
not a production application; replace it with the application under test when
connecting this flow to a real product.

## Run locally

From the repository root, start the demo application in one terminal:

```powershell
python mock_app.py
```

In another terminal, install the UI test dependencies and Chromium, then run
the UI tests:

```powershell
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python -m pytest frontend -q
```

Run the API feature files with Java 17 and Maven installed:

```powershell
mvn test
```

The demo listens on `http://127.0.0.1:3000`. To use another API test URL,
pass `-DbaseUrl=http://host:port` to Maven.

## Jira-to-PR validation

The GitHub Actions workflow starts `mock_app.py`, runs the UI and Karate
tests on pull requests that change test files, and posts both results as a PR
comment. A failed suite fails the required status check. The workflow never
approves or merges a pull request.

To require human approval, configure branch protection for `main` in GitHub:
require at least one approving review and require the **Validate generated
tests / validate** status check before merging. For forked pull requests,
GitHub may restrict the token from posting comments; the workflow result and
logs remain available in the Checks tab.
