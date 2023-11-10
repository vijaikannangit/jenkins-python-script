import requests

# to check minimum number of PR approval is 2 and PR is approved or not 

def is_pr_approved_min_approvals(owner, repo, pr_number, github_token, min_approvals=2):
    # Construct the API URL for the PR

    print ("Step0")
    print (owner, repo, pr_number, github_token, min_approvals)

    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'

    # Set up the headers with the GitHub token
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    print ("Step1")

    # Make the API request to get the PR reviews
    response = requests.get(url, headers=headers)

    print ("Step2")
    print (response)

    # Check if the request was successful (status code 200)
    print (url)
    if response.status_code == 200:
        # Check if there are enough approvals
        reviews = response.json()
        approved_count = sum(1 for review in reviews if review['state'] == 'APPROVED')

        if approved_count >= min_approvals:
            return True
        else:
            return False
    else:
        # Print an error message if the request was not successful
        print(f'Error: Unable to fetch PR reviews. Status code: {response.status_code}')
        return False



def automerge_pr(owner, repo, pr_number, github_token):
    # Construct the API URL for merging the PR
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge'

    # Set up the headers with the GitHub token
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Set up the data for the merge request
    data = {
        'commit_title': 'Automerge PR',  # You can customize the commit title
        'commit_message': 'Automatically merged by script'  # You can customize the commit message
    }

    # Make the API request to merge the PR
    response = requests.put(url, headers=headers, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f'PR #{pr_number} successfully merged!')
        return True
    else:
        # Print an error message if the request was not successful
        print(f'Error: Unable to merge PR. Status code: {response.status_code}, Message: {response.json()["message"]}')
        return False

#parameters
owner = 'vijaikannangit'
repo = 'jenkins-python-script'
pr_number = 1 
github_token = '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'

if is_pr_approved_min_approvals(owner, repo, pr_number, github_token, min_approvals=2):
    print(f'PR #{pr_number} has at least 2 approvals!')
else:
    print(f'PR #{pr_number} does not have enough approvals or an error occurred.')

"""
if automerge_pr(owner, repo, pr_number, github_token):
    print(f'Automerging of PR #{pr_number} successful!')
else:
    print(f'Automerging of PR #{pr_number} failed.')
"""