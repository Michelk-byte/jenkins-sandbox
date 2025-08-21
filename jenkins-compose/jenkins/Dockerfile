FROM jenkins/jenkins:lts-jdk17

USER root

# Install Git + Docker CLI
RUN apt-get update \
 && apt-get install -y --no-install-recommends git docker.io \
 && rm -rf /var/lib/apt/lists/*

# (Optional) add Jenkins user to docker group if you ever drop back to USER jenkins
# RUN groupadd -f docker && usermod -aG docker jenkins

# Run as root so Jenkins jobs can access /var/run/docker.sock easily
USER root