import requests

# to check minimum number of PR approval is 2 and PR is approved or not 

def is_pr_approved(owner, repo, pr_number, github_token, min_approvals=2):
    # Construct the API URL for the PR
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'

    # Set up the headers with the GitHub token
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the API request to get the PR reviews
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
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

#parameters
owner = 'vijaikannangit' #your_username'
repo = 'jenkins-python-script'
pr_number = 1  # Replace with your PR number
github_token = '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'

if is_pr_approved(owner, repo, pr_number, github_token, min_approvals=2):
    print(f'PR #{pr_number} has at least 2 approvals!')
else:
    print(f'PR #{pr_number} does not have enough approvals or an error occurred.')
