# Credential Sanitization Note

This file documents a local patch applied to the yt-dlp submodule to remove hard-coded AWS credentials that were inadvertently committed in the vendored source.

## What was changed

In the file `YouTube/Clipping/yt-dlp/yt_dlp/extractor/shahid.py`, the following fields were originally set to non-empty values that appeared to be genuine AWS credentials:

- `_AWS_API_KEY`
- `access_key` (within the `_call_api` method)
- `secret_key` (within the `_call_api` method)

These values have been replaced with empty strings (`''`) to prevent accidental exposure of credentials.

## Why this change was necessary

The original values appeared to be genuine AWS access key ID and secret access key. Committing such credentials to a public repository poses a security risk, as they could be used to make unauthorized requests to AWS services on behalf of the account owner.

This change restores the file to its intended upstream state, where these fields are empty strings, allowing users to configure their own AWS credentials through the standard yt-dlp mechanisms (e.g., environment variables, netrc file, etc.) without risking exposure of sensitive information.

## Impact on functionality

The extractor will still function correctly for users who provide their own AWS credentials through the proper channels. When no credentials are provided, the AWS requests will fail with appropriate authentication errors, which is the expected behavior.

This change does not alter the extractor's logic or behavior beyond removing the hard-coded credentials.

## Original upstream source

The values were restored to match the upstream yt-dlp revision:
897341241f2bfb2439fe0367f4c7e9ccd29a3828

Where the fields are defined as empty strings.
