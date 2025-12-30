pipeline {
  agent any
  options { timestamps(); disableConcurrentBuilds() }

  environment {
    VENV_DIR = ".venv"
    DEPLOY_DIR = "/tmp/flask_deploy_target"
  }

  triggers {
    // Webhook is ideal; polling works in labs too
    pollSCM('H/5 * * * *')
  }

  stages {
    stage('Clone the Repository') {
      steps {
        checkout scm
        sh 'git rev-parse --short HEAD'
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          set -e
          python3 --version || python --version

          if command -v python3 >/dev/null 2>&1; then
            python3 -m venv ${VENV_DIR}
          else
            python -m venv ${VENV_DIR}
          fi

          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run Unit Tests') {
      steps {
        sh '''
          set -e
          . ${VENV_DIR}/bin/activate
          pytest -q
        '''
      }
    }

    stage('Build the Application') {
      steps {
        sh '''
          set -e
          mkdir -p build_artifact
          tar --exclude=${VENV_DIR} --exclude=build_artifact --exclude=.git -czf build_artifact/flask_app.tar.gz .
          ls -lah build_artifact
        '''
      }
      post {
        success {
          archiveArtifacts artifacts: 'build_artifact/flask_app.tar.gz', fingerprint: true
        }
      }
    }

    stage('Deploy the Application') {
      steps {
        sh '''
          set -e
          mkdir -p ${DEPLOY_DIR}
          rm -rf ${DEPLOY_DIR}/*
          tar -xzf build_artifact/flask_app.tar.gz -C ${DEPLOY_DIR}
          echo "Deployed to ${DEPLOY_DIR}"
          ls -lah ${DEPLOY_DIR}
          echo "Simulating service restart..."
          echo "Service restarted (simulated)."
        '''
      }
    }
  }

  post {
    failure { echo "Pipeline failed. Check console output." }
  }
}
