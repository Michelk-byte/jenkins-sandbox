# Jenkins + Python CI/CD Example (with Datadog)

This repository shows how to set up a **local Jenkins server** using Docker Compose, run a **sample Python project**, configure a **Declarative Pipeline** for testing with `pytest`, and send build/test metrics to **Datadog**.

---

## Prerequisites

- macOS (or Linux)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Git](https://git-scm.com/downloads)
- [Datadog account](https://app.datadoghq.com/) with an API key

---

## Running Jenkins with Docker Compose

1. Move into the Jenkins compose folder:

```bash
cd jenkins-compose
```

2.	Start Jenkins:

```bash
docker compose up -d --build
```

3.	Grab the admin password:

```bash
docker exec -it jenkins bash -lc 'cat /var/jenkins_home/secrets/initialAdminPassword'
```

4.	Open Jenkins at http://localhost:8080 and finish the setup wizard:
- Install Suggested Plugins
- Create your admin user

---

## Jenkins Configuration

### Install required plugins

In Manage Jenkins → Plugins, ensure these are installed:
-	Pipeline
-	Git
-	Git client
-	Docker Pipeline
-	JUnit
- Stage View
- Datadog
-	(Optional) Workspace Cleanup

### Create a Pipeline Job
1.	New Item → Pipeline → hello-jenkins-py
2.	Definition: Pipeline script from SCM
3.	SCM: Git
   - Repository URL: https://github.com/<your-username>/jenkins-sandbox.git
   - Credentials: None (for public repo)
   - Branches to build: */main (or */master)
   - Script Path: Jenkinsfile
4.	Save → Build Now

---

## The Jenkinsfile Explained

<pre markdown="1">
```groovy
pipeline {
  agent { docker { image 'python:3.13-slim' } }

  options {
    skipDefaultCheckout()
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        deleteDir()
        checkout scm
      }
    }
    stage('Install deps') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'pytest -q --junitxml=reports/junit.xml'
      }
      post {
        always {
          junit 'reports/junit.xml'
        }
      }
    }
  }
}
```
</pre>

- Agent: runs every stage in a fresh python:3.13-slim container
- Checkout: cleans the workspace and clones the repo
- Install deps: installs Python requirements
- Test: runs pytest and publishes test results in Jenkins UI

---

## Python Project

Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

---

## Datadog Integration (Agentless)

### Install and enable the Datadog Jenkins plugin v3.1.0 or later:

In your Jenkins instance web interface, go to Manage Jenkins > Manage Plugins.
In the Update Center on the Available tab, search for Datadog Plugin.
Select the checkbox next to the plugin, and install using one of the two install buttons at the bottom of the screen.
To verify that the plugin is installed, search for Datadog Plugin on the Installed tab.

### Configure the Datadog Jenkins plugin

Use this option to make the Jenkins plugin report directly to Datadog without using the Datadog Agent. It requires an API Key.

1. In your Jenkins instance web interface, go to Manage Jenkins > Configure System.
2. Go to the Datadog Plugin section, scrolling down the configuration screen.
3. Select the mode Use Datadog site and API key to report to Datadog.
4. Select your Datadog site in the Pick a site dropdown.
5. Enter a valid Datadog API Key (or use Select from credentials option).
6. Click the Test Key button to verify that your API key is valid.
7. Configure CI Visibility:
   - a. Enable the Enable CI Visibility checkbox.
   - b. (Optional) Configure your CI Instance name.
8. (Optional) Configure logs collection:
   - a. Enable the Enable Log Collection checkbox.
9. (Optional) Enter the name of the host that you use to access Datadog UI (for example, app.datadoghq.com) in the Datadog App hostname field.
10. Save your configuration.

![Datadog jenkins plugin configuration](https://datadog-docs.imgix.net/images/ci/ci-jenkins-plugin-config-agentless-app-hostname.91c692b697d9bdffeb04493e2d1a2e17.png?fit=max&auto=format)

### Visualize pipeline data in Datadog

Once the integration is successfully configured, both the CI Pipeline List and Executions pages populate with data after pipelines finish.

The CI Pipeline List page shows data for only the default branch of each repository. For more information, see Search and Manage CI Pipelines.

---

Notes
- Jenkins exposes:
- 8080 → Web UI
- 50000 → JNLP agent port (not needed locally, useful for remote agents)
- Jenkins container runs as root to allow access to the Docker socket (/var/run/docker.sock)
- Default branch is master (check your repo and adjust Jenkins config accordingly)

---

Common Issues
	•	fatal: not in a git directory
Caused by stale workspaces. Fixed by:
	•	Using deleteDir() before checkout scm (as in Jenkinsfile)
	•	Or enabling “Clean before checkout” in job config
	•	permission denied /var/run/docker.sock
Caused when Jenkins can’t talk to Docker. Fixed by running Jenkins container as root.

