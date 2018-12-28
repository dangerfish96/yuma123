#include <sys/types.h>
#include <stdio.h>
#include "Socket.h"

#include <net/ethernet.h>
#include <netinet/in.h>


#define ZEBRA_INTERFACE_ADD                1
#define ZEBRA_INTERFACE_DELETE             2
#define ZEBRA_INTERFACE_ADDRESS_ADD        3
#define ZEBRA_INTERFACE_ADDRESS_DELETE     4
#define ZEBRA_INTERFACE_UP                 5
#define ZEBRA_INTERFACE_DOWN               6
#define ZEBRA_IPV4_ROUTE_ADD               7
#define ZEBRA_IPV4_ROUTE_DELETE            8
#define ZEBRA_IPV6_ROUTE_ADD               9
#define ZEBRA_IPV6_ROUTE_DELETE           10
#define ZEBRA_REDISTRIBUTE_ADD            11
#define ZEBRA_REDISTRIBUTE_DELETE         12
#define ZEBRA_REDISTRIBUTE_DEFAULT_ADD    13
#define ZEBRA_REDISTRIBUTE_DEFAULT_DELETE 14
#define ZEBRA_IPV4_NEXTHOP_LOOKUP         15
#define ZEBRA_IPV6_NEXTHOP_LOOKUP         16
#define ZEBRA_IPV4_IMPORT_LOOKUP          17
#define ZEBRA_IPV6_IMPORT_LOOKUP          18
#define ZEBRA_INTERFACE_RENAME            19
#define ZEBRA_ROUTER_ID_ADD               20
#define ZEBRA_ROUTER_ID_DELETE            21
#define ZEBRA_ROUTER_ID_UPDATE            22
#define ZEBRA_HELLO                       23
#define ZEBRA_IPV4_NEXTHOP_LOOKUP_MRIB    24
#define ZEBRA_VRF_UNREGISTER              25
#define ZEBRA_INTERFACE_LINK_PARAMS       26

#define ZEBRA_NEXTHOP_REGISTER            27
#define ZEBRA_NEXTHOP_UNREGISTER          28
#define ZEBRA_NEXTHOP_UPDATE              29
#define ZEBRA_MESSAGE_MAX                 30

#define ZAPI_MESSAGE_NEXTHOP  0x01
#define ZAPI_MESSAGE_IFINDEX  0x02
#define ZAPI_MESSAGE_DISTANCE 0x04
#define ZAPI_MESSAGE_METRIC   0x08
#define ZAPI_MESSAGE_MTU      0x10
#define ZAPI_MESSAGE_TAG      0x20

#define ZEBRA_ROUTE_SYSTEM               0
#define ZEBRA_ROUTE_KERNEL               1
#define ZEBRA_ROUTE_CONNECT              2
#define ZEBRA_ROUTE_STATIC               3
#define ZEBRA_ROUTE_RIP                  4
#define ZEBRA_ROUTE_RIPNG                5
#define ZEBRA_ROUTE_OSPF                 6
#define ZEBRA_ROUTE_OSPF6                7
#define ZEBRA_ROUTE_ISIS                 8
#define ZEBRA_ROUTE_BGP                  9
#define ZEBRA_ROUTE_PIM                  10
#define ZEBRA_ROUTE_HSLS                 11
#define ZEBRA_ROUTE_OLSR                 12
#define ZEBRA_ROUTE_BABEL                13
#define ZEBRA_ROUTE_NHRP                 14
#define ZEBRA_ROUTE_MAX                  15

#define SAFI_UNICAST              1
#define SAFI_MULTICAST            2
#define SAFI_RESERVED_3           3
#define SAFI_MPLS_VPN             4
#define SAFI_ENCAP                7 /* per IANA */
#define SAFI_MAX                  8

#define SET_FLAG(V,F)        (V) |= (F)

void makeCommand(int message_type, char *prefix, int prefixlen, char *nexthop,u_int32_t metric  );

struct prefix_ipv4
  {
    unsigned char family;
    unsigned char prefixlen;
    struct in_addr prefix __attribute__ ((aligned (8)));
  }__attribute__((__packed__));


struct socket_command{
   struct in_addr nexthop __attribute__((__packed__));
   char mtype;
   unsigned char type;
   int metric;
   struct prefix_ipv4 p __attribute__((__packed__));
} __attribute__((__packed__)) ;


