
#define _DEFAULT_SOURCE


#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <arpa/inet.h>

#include "Socket.h"
#include "com.h"
 


void makeCommand(int message_type, char *prefix, int prefixlen, char *nexthop,u_int32_t metric){
    int sock_fd;
    sock_fd = connect_tcp("127.0.0.1",8888);
    if(sock_fd <= 0){
        printf("Some error occured while connecting...");
        return;
    }
    struct socket_command * cmd = (struct socket_command*)malloc(sizeof(struct socket_command));
    struct prefix_ipv4 * p = (struct prefix_ipv4 *) malloc(sizeof(struct prefix_ipv4));
    p->family = AF_INET;
    p->prefixlen = prefixlen;
    inet_aton(prefix,&(p->prefix));

    memcpy(&(cmd->p),p, sizeof(struct prefix_ipv4));

    cmd->type = ZEBRA_ROUTE_STATIC;
    inet_aton(nexthop,&(cmd->nexthop));
    cmd->metric = metric;
    cmd->mtype = message_type;
    write(sock_fd, cmd, sizeof(cmd) + sizeof(struct prefix_ipv4) + sizeof(struct in_addr));
    free(cmd);
    close(sock_fd);
}

