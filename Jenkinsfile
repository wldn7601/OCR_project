// http://wldn7601.store:8080/

pipeline {
  agent any
  environment {
    IMAGE = "wldn7601/receipt-ocr"
    COMPOSE = "/usr/bin/docker compose"   // jenkins 컨테이너에 설치된 compose 플러그인 경로
    PROJECT_DIR = "/workspace/OCR_Project"
  }
  stages {
    stage('Checkout') {
      steps {
        // Jenkins 컨테이너에 마운트된 폴더로 이동해서 빌드 (GitHub Webhook/SCM checkout을 쓰면 아래는 생략 가능)
        dir("${env.PROJECT_DIR}") {
          sh 'git rev-parse --is-inside-work-tree || true'
        }
      }
    }
    stage('Set Tags') {
      steps {
        script {
          env.SHORT_SHA = sh(script: 'git -C ${PROJECT_DIR} rev-parse --short=7 HEAD', returnStdout: true).trim()
          env.DATE_TAG = sh(script: 'date +%Y%m%d', returnStdout: true).trim()
          env.BUILD_TAG = "jenkins-${env.DATE_TAG}-${env.SHORT_SHA}"
        }
        echo "TAG = ${env.BUILD_TAG}"
      }
    }
    stage('Docker Login') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                          usernameVariable: 'DH_USER',
                                          passwordVariable: 'DH_PASS')]) {
          sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
        }
      }
    }
    stage('Build & Push') {
      steps {
        dir("${env.PROJECT_DIR}") {
          sh """
            docker build -t ${IMAGE}:${BUILD_TAG} -t ${IMAGE}:latest .
            docker push ${IMAGE}:${BUILD_TAG}
            docker push ${IMAGE}:latest
          """
        }
      }
    }
    stage('Deploy (web only)') {
      steps {
        sh """
          cd ${PROJECT_DIR}
          ${COMPOSE} pull web
          ${COMPOSE} up -d web
        """
      }
    }
  }
  post {
    always {
      sh 'docker logout || true'
    }
  }
}
