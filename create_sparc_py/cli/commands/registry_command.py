import argparse
import json
import sys
from create_sparc_py.core.registry_client import RegistryClient


def registry_command(args):
    parser = argparse.ArgumentParser(
        prog="create-sparc-py registry",
        description="Registry client commands (list, get, post, auth)",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # list
    parser_list = subparsers.add_parser("list", help="List resources from the registry (e.g., templates, components)")
    parser_list.add_argument("resource", help="Resource type to list (e.g., templates, components)")

    # get
    parser_get = subparsers.add_parser("get", help="Get a resource from the registry by path")
    parser_get.add_argument("path", help="Path to the resource")

    # post
    parser_post = subparsers.add_parser("post", help="Post JSON data to the registry at path")
    parser_post.add_argument("path", help="Path to post to")
    parser_post.add_argument("data_json", help="JSON data to post")

    # auth
    parser_auth = subparsers.add_parser("auth", help="Authenticate with the registry using an API key")
    parser_auth.add_argument("api_key", help="API key for authentication")

    # Parse the registry_args from the main CLI
    parsed = parser.parse_args(getattr(args, "registry_args", []))
    client = RegistryClient()

    if parsed.subcommand == "list":
        result = client.get(f"{parsed.resource}")
        print(json.dumps(result, indent=2))
        return 0
    elif parsed.subcommand == "get":
        result = client.get(parsed.path)
        print(json.dumps(result, indent=2))
        return 0
    elif parsed.subcommand == "post":
        try:
            data = json.loads(parsed.data_json)
        except Exception as e:
            print(f"Invalid JSON: {e}", file=sys.stderr)
            return 1
        result = client.post(parsed.path, data)
        print(json.dumps(result, indent=2))
        return 0
    elif parsed.subcommand == "auth":
        ok = client.authenticate({"api_key": parsed.api_key})
        if ok:
            print("Authenticated successfully.")
            return 0
        else:
            print("Authentication failed.")
            return 0
    else:
        parser.print_help()
        return 1
