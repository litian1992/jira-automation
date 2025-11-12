# jira-automation
A repo for all Jira automation related scripts and tools

## Create CTC1 Tickets Usage
First replace `MY_PERSONAL_TOKEN` with your own Jira personal access token.
Then execute
```
python create-ctc1-tickets.py <RHELMISC-XXX>
``` 
## What it does
This will create an Epic which is a clone of RHELMISC ticket.
Then link the Epic to RHELMISC as 'caused by' relation.
Finally it creates Tasks for each sub-team/platform under above Epic.
