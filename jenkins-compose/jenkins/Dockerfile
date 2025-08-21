FROM jenkins/jenkins:lts-jdk17

USER root
# Install Docker CLI (from Debian repos is fine for local use)
RUN apt-get update \
 && apt-get install -y --no-install-recommends docker.io \
 && rm -rf /var/lib/apt/lists/*

# Let 'jenkins' user talk to the docker socket
RUN groupadd -f docker && usermod -aG docker jenkins

USER jenkins