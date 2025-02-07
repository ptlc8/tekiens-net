FROM mariadb:lts

# dummy creds
ENV MYSQL_ROOT_PASSWORD=passwd \
    MYSQL_DATABASE=tekiens_net \
    MYSQL_USER=tekiens_net \
    MYSQL_PASSWORD=passwd

# Copy database configuration
COPY mariadb.cnf /etc/mysql/conf.d/mariadb.cnf

# Copy database schema
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# Maybe copy database sample data (work only because i<s)
#COPY sample.sql /docker-entrypoint-initdb.d/sample.sql
