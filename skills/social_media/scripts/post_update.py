#!/usr/bin/env python3
import argparse
import json

from automation_hub.services.social.client import SocialService


def main():
    parser = argparse.ArgumentParser(
        description="Post updates to social media platforms."
    )
    parser.add_argument("--platform", required=True, help="Platform: X, LinkedIn.")
    parser.add_argument("--message", required=True, help="Message to post.")

    args = parser.parse_args()

    try:
        client = SocialService()
        if client.connect():
            result = client.post_update(args.platform, args.message)
            print(json.dumps(result))
            client.disconnect()
        else:
            print(json.dumps({"status": "error", "message": "Connection failed"}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))


if __name__ == "__main__":
    main()
