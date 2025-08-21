# Jenkins + Python CI/CD Example

This repository shows how to set up a **local Jenkins server** using Docker Compose, run a **sample Python project**, and configure a **Declarative Pipeline** for testing with `pytest`.

---

## Prerequisites

- macOS (or Linux)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Git](https://git-scm.com/downloads)

---

## Repository Layout

.
├── Jenkinsfile           # Declarative Pipeline definition
├── app.py                # Simple Python app
├── test_app.py           # Pytest test cases
├── requirements.txt      # Python dependencies
├── jenkins-compose/      # Jenkins environment
│   ├── docker-compose.yml
│   └── jenkins/
│       └── Dockerfile

---

## Running Jenkins with Docker Compose

1. Move into the Jenkins compose folder:

   ```bash
   cd jenkins-compose

	2.	Start Jenkins:

docker compose up -d --build


	3.	Grab the admin password:

docker exec -it jenkins bash -lc 'cat /var/jenkins_home/secrets/initialAdminPassword'


	4.	Open Jenkins at http://localhost:8080 and finish the setup wizard:
	•	Install Suggested Plugins
	•	Create your admin user

⸻

Jenkins Configuration

Install required plugins

In Manage Jenkins → Plugins, ensure these are installed:
	•	Pipeline
	•	Git
	•	Git client
	•	Docker Pipeline
	•	JUnit
	•	(Optional) Workspace Cleanup

Create a Pipeline Job
	1.	New Item → Pipeline → hello-jenkins-py
	2.	Definition: Pipeline script from SCM
	3.	SCM: Git
	•	Repository URL: https://github.com/<your-username>/jenkins-sandbox.git
	•	Credentials: None (for public repo)
	•	Branches to build: */main (or */master)
	•	Script Path: Jenkinsfile
	4.	Save → Build Now

⸻

The Jenkinsfile Explained

pipeline {
  agent { docker { image 'python:3.13-slim' } }

  options {
    skipDefaultCheckout()  // disable implicit checkout
    timestamps()           // add timestamps to logs
  }

  stages {
    stage('Checkout') {
      steps {
        deleteDir()        // clean workspace
        checkout scm       // full clone of repo
      }
    }

    stage('Install deps') {
      steps {
        sh 'python --version'
        sh 'pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Test') {
      steps {
        sh 'pytest -q --junitxml=reports/junit.xml'
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        }
      }
    }
  }
}

	•	Agent: runs every stage in a fresh python:3.13-slim container
	•	Checkout: cleans the workspace and clones the repo
	•	Install deps: installs Python requirements
	•	Test: runs pytest and publishes test results in Jenkins UI

⸻

Python Project

Run locally

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q


⸻

Notes
	•	Jenkins exposes:
	•	8080 → Web UI
	•	50000 → JNLP agent port (not needed locally, useful for remote agents)
	•	Jenkins container runs as root to allow access to the Docker socket (/var/run/docker.sock)
	•	Default branch is master (check your repo and adjust Jenkins config accordingly)

⸻

Common Issues
	•	fatal: not in a git directory
Caused by stale workspaces. Fixed by:
	•	Using deleteDir() before checkout scm (as in Jenkinsfile)
	•	Or enabling “Clean before checkout” in job config
	•	permission denied /var/run/docker.sock
Caused when Jenkins can’t talk to Docker. Fixed by running Jenkins container as root.

⸻

Next Steps
	•	Add linting (flake8) and coverage (pytest-cov)
	•	Configure GitHub webhook → trigger Jenkins on pushes
	•	Optionally move repo into a GitHub Organization for branch protection rules

⸻


---

Do you want me to also include in this README the **docker-compose.yml** and **jenkins/Dockerfile** snippets, so anyone can just copy-paste without hunting inside the repo?