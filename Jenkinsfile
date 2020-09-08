node ("gtst_tushu122") {
	echo "开始拉取代码"
	stage("Checkout") {
		checkout([$class: 'GitSCM', branches: [[name: 'master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '093e6cdb-fb3a-4631-99b8-7d7bafcf5dad', url: 'https://github.com/kangvai/mysite3.git']]])
	}
	
	stage("Build") {
		echo "开始构建docker镜像"
		sh '''
			sudo docker build -f Dockerfile . -t django_mysite3:v1
			sudo docker build -f compose/nginx/Dockerfile . -t mynginx:v1
		'''
	}
	
	stage("Deploy") {
		echo "开始部署dev环境"
		sh '''
			echo "sudo docker run -it --name mysite3 -p 8000:8000 -v /home/enka/mysite3:/var/www/html/mysite3 -d django_mysite3:v1" >> /tmp/start.sh
			echo "sudo docker run -it --name mysite3-nginx -p 80:80 -v /home/enka/mysite3/static:/usr/share/nginx/html/static -v /home/enka/mysite3/media:/usr/share/nginx/html/media -v /home/enka/mysite3/compose/nginx/log:/var/log/nginx -d mynginx:v1" >> /tmp/start.sh
			echo "sudo docker exec -it mysite3 /bin/bash start.sh" >> /tmp/start.sh
			sudo chmod +x /tmp/start.sh
            		/tmp/start.sh
		'''
	}
}
