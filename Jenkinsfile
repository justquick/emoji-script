node {
    docker.build('${env.BUILD_TAG}'.tokenize('/')).inside {
        stage('Test') {
            sh 'env'
            echo '$PATH'
            sh 'pwd'
            sh 'ls'
            sh 'tox -e 2.7'
        }
    }
}
