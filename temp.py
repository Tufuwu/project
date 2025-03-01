from search_exe import get_history,file_operate
import re
'''
gh = get_history()
fo = file_operate()
workflow_file_path = '.github/workflows/'
api_token = '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'
commits = gh.get_workflow_file_history('areski/python-nvd3', workflow_file_path, api_token)

for c in commits:
    b = c['commit']['message']
    if (fo.re_match("Migrate",b) or fo.re_match('Move',b) or fo.re_match('Replace',b) ) and fo.re_match('Travis',b) :
        temp_file = gh.get_commit_diff(c['url'],api_token)
        print(temp_file)
'''
s = ' @@ -1,0 +1,36 @@ '
if re.search(r'@@ \-1,\d+ \+\d+,\d+ @@',s):
    print('ssss')