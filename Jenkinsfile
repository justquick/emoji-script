node {
    docker.build('emoji-script').inside {
        stage('Test') {
            sh 'env'
            echo '$PATH'
            sh 'pwd'
            sh 'ls'
            sh 'tox -e 2.7'
        }
    }
}
