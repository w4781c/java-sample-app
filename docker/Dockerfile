FROM tomcat:8.0-alpine

ENV APP_HOME=/usr/local/tomcat/webapps/

ADD java-hello-world.war $APP_HOME

RUN adduser -u 2000 -G root -D web \
    && chown -R 2000:0  $APP_HOME
 
USER 2000

EXPOSE 8080

CMD ["/usr/local/tomcat/bin/catalina.sh", "run"]
