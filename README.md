# copilot-test

Demo repo

## status

doesn't work because it is blocked. from copilot review logs:

```
Get Jira issue
Input
{
  "cloudId": "esgbook.atlassian.net",
  "issueIdOrKey": "BLUE-2946",
  "view": "evidence"
}
MCP server 'atlassian': {"error":true,"message":"You don't have permission to connect via API token. Please ask your organization admin for access."}
```

## secrets

in https://github.com/egorman-sray/copilot-test/settings/secrets/agents

create `COPILOT_MCP_ATLASSIAN_AUTH`

with contents

```bash
JIRA_EMAIL='<your Atlassian email>'
printf 'Basic %s' "$(printf '%s:%s' "$JIRA_EMAIL" "$(tr -d '\r\n' < jira_token)" | base64 -w0)"
```
