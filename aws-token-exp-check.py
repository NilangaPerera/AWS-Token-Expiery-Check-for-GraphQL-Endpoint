import time
import requests
import json

def check_graphql_token_validity():
    """
    Checks the expiration of x-aws-waf-token for a GraphQL endpoint by sending test queries.
    """
    print("""
\033[1;31m  0x7gen  
 \033[1;32m  0000      x        7777777   ggggggg    eeeeeee    n     n
\033[1;33m  0    0    x x          7      g           e          nn    n
\033[1;34m  0    0    x x          7      g  gg       eeee       n n   n
\033[1;35m  0    0    x x          7      g   g       e          n  n  n
\033[1;36m   0000    x   x      77777     ggggggg    eeeeeee    n   nn

 	  === GraphQL - AWS Token Validity Checker ===

""")

    # User inputs for URL and token
    url = input("Enter the GraphQL endpoint URL: ").strip()
    token = input("Enter the x-aws-waf-token: ").strip()
    check_interval = int(input("Enter the check interval (in seconds): ").strip())

    # Define headers with the provided token
    headers = {
        "Content-Type": "application/json",
        "x-aws-waf-token": token,
        "User-Agent": "GraphQL-Token-Checker/1.0"
    }

    # Basic GraphQL Query to test token validity
    graphql_query = {
        "query": "{ __typename }"  # This minimal query checks if the endpoint responds successfully
    }

    print("\nStarting token validity test...\n")
    start_time = time.time()

    while True:
        try:
            # Send POST request to the GraphQL endpoint
            response = requests.post(url, headers=headers, data=json.dumps(graphql_query))

            # Check if the response indicates success
            if response.status_code == 200:
                print(f"[{time.strftime('%H:%M:%S')}] Token is still valid. Response: {response.status_code}")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Token expired or invalid. "
                      f"Response Code: {response.status_code} - {response.text}")
                break

        except requests.RequestException as e:
            print(f"Error during request: {e}")
            break

        # Wait for the next check
        time.sleep(check_interval)

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nToken validity duration: {duration // 60:.0f} minutes {duration % 60:.0f} seconds.")

if __name__ == "__main__":
    check_graphql_token_validity()
