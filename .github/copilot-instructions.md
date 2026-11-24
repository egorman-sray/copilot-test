# Pull Request Review Instructions

When reviewing a pull request, follow these steps systematically:

## 1. Locate and Fetch the Jira Ticket
- Extract the Jira issue key (e.g., `BLUE-123`) from the PR title, branch name, or PR description.
- Use the configured Jira MCP tool to retrieve the full ticket details, including the summary, description, acceptance criteria, and any relevant comments.
- If no Jira issue key is found or the ticket cannot be retrieved, explicitly note this in the review summary before continuing with a standard code review.

## 2. Evaluate Acceptance Criteria
- Compare the PR diff directly against every acceptance criterion listed in the Jira ticket.
- Verify that:
  - All functional requirements and edge cases described in the ticket are implemented.
  - Automated tests (unit/integration) exist and meaningfully cover each acceptance criterion.
  - No unintended scope creep or unrelated changes are introduced without explanation.

## 3. Code Quality & Standards Check
- Check the changes for security vulnerabilities, error handling gaps, performance regressions, and maintainability issues.
- Ensure changes adhere to existing repository patterns and conventions.

## 4. Review Output Format
- **Jira Summary:** State the ticket key, title, and a brief Pass/Fail checklist mapping each acceptance criterion to the code changes.
- **Inline Comments:** Leave targeted, actionable comments on specific lines for any unmet criteria, bugs, or missing test coverage.
