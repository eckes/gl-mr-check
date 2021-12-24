import os
import sys
import gitlab
from git import Repo

GITLAB_SERVER=os.getenv('CI_SERVER_URL', 'https://gitlab.com')
GITLAB_PROJECT_ID=os.getenv('CI_PROJECT_ID', 278964)
MR_ID=os.getenv('CI_MERGE_REQUEST_ID', '77311')

def get_fixes_since(a_repo, a_target_branch):
    fixes = []
    for c in a_repo.iter_commits(f"{a_target_branch}.."):
        if c.message.startswith('FIX'):
            fixes.append( c )
    return(fixes)

#   fixes = get_fixes_since(Repo('F:/src/mr-stuff'), os.getenv('CI_MERGE_REQUEST_TARGET_BRANCH_NAME', 'master'))
#   for f in fixes:
#       # fixes.append( { 'title': title.split('\n')[0].rstrip('\r'), 'hash': c.hexsha } )
#       print(f.message.split('\n')[0].rstrip('\r'))

fixes = []
gl = gitlab.Gitlab(GITLAB_SERVER)
project = gl.projects.get(GITLAB_PROJECT_ID)
mr = project.mergerequests.get(MR_ID)
for c in mr.commits():
    if c.message.startswith('FIX'):
        fixes.append(c)

if len(fixes) == 0:
    print("no fixes, no CVSS ratings needed")
    sys.exit(0)

closing = mr.closes_issues()
for d in mr.discussions.list():
    print(d)
