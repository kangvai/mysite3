node {
	echo "开始拉取代码"
	stage("Checkout") {
		checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'b888ba74-a43b-4133-9ae8-d0d737d04655', url: 'git@github.com:kangvai/mysite3.git']]])
	}
	
	stage("Build") {
		echo "开始构建docker镜像"
		sh '''
			docker build -f Dockerfile . -t django_mysite3:$BUILD_NUMBER
			docker build -f compose/nginx/Dockerfile . -t mynginx:$BUILD_NUMBER
		'''
	}
	
	stage("Upload") {
		echo "上传docker镜像到制品仓库"
		sh '''
			docker login -u kangvai -p kv@2016014351
			docker tag django_mysite3:$BUILD_NUMBER kangvai/django_mysite3:$BUILD_NUMBER
			docker tag mynginx:$BUILD_NUMBER kangvai/mynginx:$BUILD_NUMBER
			docker push kangvai/django_mysite3:$BUILD_NUMBER
			docker push kangvai/mynginx:$BUILD_NUMBER
		'''
	}
	
	stage("Deploy") {
		echo "开始部署dev环境"
		sh '''
			echo "docker login -u kangvai -p kv@2016014351" > /tmp/start.sh
			echo "docker pull kangvai/django_mysite3:$BUILD_NUMBER" >> /tmp/start.sh
			echo "docker pull kangvai/mynginx:$BUILD_NUMBER" >> /tmp/start.sh
			echo 'CONTAINER_EXIST11=`docker container ls -a|grep mysite3 | cut -d " " -f1`' >> /tmp/start.sh
			echo 'CONTAINER_EXIST12=`docker container ls -a|grep mysite3-nginx | cut -d " " -f1`' >> /tmp/start.sh
			echo '[ -n CONTAINER_EXIST1 ] && docker container stop mysite3' >> /tmp/start.sh
			echo '[ -n CONTAINER_EXIST2 ] && docker container stop mysite3-nginx' >> /tmp/start.sh
            echo '[ -n CONTAINER_EXIST1 ] && docker container rm mysite3' >> /tmp/start.sh
			echo '[ -n CONTAINER_EXIST2 ] && docker container rm mysite3-nginx' >> /tmp/start.sh
			echo "docker container run -it --name mysite3 -p 8000:8000 -v /home/enka/mysite3:/var/www/html/mysite3 -d kangvai/django_mysite3:$BUILD_NUMBER" >> /tmp/start.sh
			echo "docker container run -it --name mysite3-nginx -p 80:80 -v /home/enka/mysite3/static:/usr/share/nginx/html/static -v /home/enka/mysite3/media:/usr/share/nginx/html/media -v /home/enka/mysite3/compose/nginx/log:/var/log/nginx -d kangvai/mynginx:$BUILD_NUMBER" >> /tmp/start.sh
			echo "docker exec -it mysite3 /bin/bash start.sh" >> /tmp/start.sh
			sed -i 's/CONTAINER_EXIST1/"$CONTAINER_EXIST11"/g' /tmp/start.sh
			sed -i 's/CONTAINER_EXIST2/"$CONTAINER_EXIST12"/g' /tmp/start.sh
			scp /tmp/start.sh chenwei@172.16.91.122:/tmp/start.sh
			ssh chenwei@172.16.91.122 "chmod +x /tmp/start.sh"
            ssh chenwei@172.16.91.122 "/tmp/start.sh"
		'''
	}
}