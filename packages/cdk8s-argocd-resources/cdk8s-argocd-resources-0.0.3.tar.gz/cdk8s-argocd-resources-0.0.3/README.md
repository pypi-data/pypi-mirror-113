# cdk8s-argocd-resources

Has the ability to synth ArgoCD Application, and AppProject manifests. See example.

## Overview

### example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from constructs import Construct
from cdk8s import App, Chart, ChartProps
import opencdk8s.cdk8s_argocd_resources as argo

class MyChart(Chart):
    def __init__(self, scope, id, *, namespace=None, labels=None):
        super().__init__(scope, id, namespace=namespace, labels=labels)

        argo.ArgoCdApplication(self, "DemoApp",
            metadata={
                "name": "demo",
                "namespace": "argocd"
            },
            spec={
                "project": "default",
                "source": {
                    "repo_uRL": "example-git-repo",
                    "path": "examplepath",
                    "target_revision": "HEAD"
                },
                "destination": {
                    "server": "https://kubernetes.default.svc"
                },
                "sync_policy": {
                    "sync_options": ["ApplyOutOfSyncOnly=true"
                    ]
                }
            }
        )

        argo.ArgoCdProject(self, "DemoProject",
            metadata={
                "name": "demo",
                "namespace": "argocd"
            },
            spec={
                "description": "demo project",
                "source_repos": ["*"
                ],
                "destination": [{
                    "namespace": "default",
                    "server": "https://kubernetes.default.svc"
                }]
            }
        )

app = App()
MyChart(app, "asd")
app.synth()
```

<details>
<summary>demo.k8s.yaml</summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo
  namespace: argocd
spec:
  destination:
    server: https://kubernetes.default.svc
  project: default
  source:
    path: examplepath
    repoURL: example-git-repo
    targetRevision: HEAD
  syncPolicy:
    syncOptions:
      - ApplyOutOfSyncOnly=true
---
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: demo
  namespace: argocd
spec:
  description: demo project
  destination:
    - namespace: default
      server: https://kubernetes.default.svc
  sourceRepos:
    - "*"
```

</details>

## Installation

### TypeScript

Use `yarn` or `npm` to install.

```sh
$ npm install @opencdk8s/cdk8s-argocd-resources
```

```sh
$ yarn add @opencdk8s/cdk8s-argocd-resources
```

### Python

```sh
$ pip install cdk8s-argocd-resources
```

## Contribution

1. Fork ([link](https://github.com/opencdk8s/cdk8s-argocd-resources/fork))
2. Bootstrap the repo:

   ```bash
   npx projen   # generates package.json
   yarn install # installs dependencies
   ```
3. Development scripts:
   |Command|Description
   |-|-
   |`yarn compile`|Compiles typescript => javascript
   |`yarn watch`|Watch & compile
   |`yarn test`|Run unit test & linter through jest
   |`yarn test -u`|Update jest snapshots
   |`yarn run package`|Creates a `dist` with packages for all languages.
   |`yarn build`|Compile + test + package
   |`yarn bump`|Bump version (with changelog) based on [conventional commits]
   |`yarn release`|Bump + push to `master`
4. Create a feature branch
5. Commit your changes
6. Rebase your local changes against the master branch
7. Create a new Pull Request (use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for the title please)

## Licence

[Apache License, Version 2.0](./LICENSE)

## Author

[Hunter-Thompson](https://github.com/Hunter-Thompson)
