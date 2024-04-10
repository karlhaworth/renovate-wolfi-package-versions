# Chainguard package query

This python script fetches the `APKINDEX` from https://packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz allowing us to parse the file and query it.

We can use the outputs of this file to populate necessary package versions for renovate.

## Use in Renovate

```json
{
    "enabledManagers": ["regex"],
    "versioning": "loose",
    "customManagers": [
      {
        "customType": "regex",
        "fileMatch": ["^Dockerfile$"],
        "matchStrings": ["ENV NODE_VERSION=(?<currentValue>.*?)\\n"],
        "depNameTemplate": "node-lts",
        "datasourceTemplate": "custom.local_generic"
      },
      {
        "customType": "regex",
        "fileMatch": ["^Dockerfile$"],
        "matchStrings": ["ENV PYTHON_VERSION=(?<currentValue>.*?)\\n"],
        "depNameTemplate": "python-3",
        "datasourceTemplate": "custom.local_generic"
      }
    ],
    "customDatasources": {
        "local_generic": {
          "defaultRegistryUrlTemplate": "https://karlhaworth.github.io/renovate-wolfi-package-versions/packages/{{packageName}}/versions.json",
          "transformTemplates": [
            "{ \"releases\": $map($, function($v) { { \"version\": $v.version } }) }"
          ]
        }
    }
  }
```