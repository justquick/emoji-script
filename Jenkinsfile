node {
    docker.image('snelis/tox').inside {
        stage('Test') {
            sh 'tox -e 2.7'
        }
    }
}
