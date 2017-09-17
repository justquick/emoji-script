node {
    docker.image('python:tox').inside {
        stage('Test') {
            sh 'tox -e 2.7'
        }
    }
}
