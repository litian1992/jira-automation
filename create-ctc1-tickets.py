###
# This script:
# 1. creates an Epic which is a clone of RHELMISC ticket
# 2. creates Tasks under above Epic for each platform/sub-team
###

import sys
from jira import JIRA

jira = JIRA(server="https://issues.redhat.com", token_auth=("MY_PERSONAL_TOKEN"))

def create_epic(src_ticket_id):
    # Clone the RHELMISC ticket
    src_ticket = jira.issue(src_ticket_id)
    fields = {
        'project': 'RHELOPC',
        'issuetype': 'Epic',
        'summary': f"[rhel-virt-cloud][{src_ticket.fields.fixVersions[0].name}] {src_ticket.fields.summary}",
        'priority': {'name': 'Major'},
        'versions': [{'name': src_ticket.fields.fixVersions[0].name}],
        'customfield_12311141': f"[rhel-virt-cloud][{src_ticket.fields.fixVersions[0].name}] {src_ticket.fields.summary}", # Epic name
        'customfield_12326540': {'value': 'rhel-virt-cloud'}, # AssignedTeam
        'security': {'name': 'Red Hat Employee'},
        'assignee': {'name': 'ldu@redhat.com'},
        'description': src_ticket.fields.description
    }
    epic = jira.create_issue(fields=fields)
    print(f"Info: Created Epic {jira._options['server']}/browse/{epic.key}")

    # Link Epic to RHELMISC ticket as 'caused by'
    jira.create_issue_link(type='causes', inwardIssue=src_ticket_id, outwardIssue=epic.key)
    create_subtasks(epic.key)

def create_subtasks(epic_id):
    # Platforms and assignees
    epic = jira.issue(epic_id)
    groups = {
        'Azure': 'yuxisun@redhat.com',
        'ESXi': 'boyang@redhat.com',
        'cloud-init': 'rhn-support-xiachen',
        'Hyper-V': 'xxiong@redhat.com',
        'AWS': 'rh-ee-libhe',
        'libguestfs': 'xchen@redhat.com',
        'Google Cloud': 'linl@redhat.com'
    }

    for platform, assignee in groups.items():
        if platform in ['AWS', 'libguestfs', 'Google Cloud']:
            project = 'VIRTCLOUD'
        else:
            project = 'RHELOPC'
        fields = {
            'project': project,
            'issuetype': 'Task',
            'summary': f"[{platform}]{epic.fields.summary}",
            'description': src_ticket.fields.description,
            'assignee': {'name': assignee},
            'customfield_12311140': epic_id, # Epic
            'customfield_12326540': {'value': 'rhel-virt-cloud'}, # AssignedTeam
            'versions': [{'name': epic.fields.versions[0].name}],
        }
        ticket = jira.create_issue(fields=fields)
        print(f"Info: Created Task {jira._options['server']}/browse/{ticket.key}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create-ctc1-tickets.py <origin_ticket>")
        sys.exit(1)
    src_ticket_id = sys.argv[1]
    create_epic(src_ticket_id)
