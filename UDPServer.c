#include <stdio.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 
#include <netdb.h>

#define SERVER_PORT 5432 
#define MAX_PENDING 5 
#define MAX_LINE 256 

int main() 
{ 
  struct sockaddr_in sin, clientAddr; 
  char buf[MAX_LINE]; 
  int len, clientAddrLen; 
  int s; 

  /* build address data structure */ 
  bzero((char *)&sin, sizeof(sin)); 
  sin.sin_family = AF_INET; 
  sin.sin_addr.s_addr = INADDR_ANY; 
  sin.sin_port = htons(SERVER_PORT); 

  /* create new socket */
  if ((s = socket(PF_INET, SOCK_DGRAM, 0)) < 0) { 
    perror("simplex-talk: socket"); 
    exit(1); 
  } 

  printf("**Socket created\n");

  /* setup for passive open */ 
  if ((bind(s, (struct sockaddr *)&sin, sizeof(sin))) < 0) { 
    perror("simplex-talk: bind"); 
    exit(1); 
  } 

  printf("**Socket bound to local address\n");

  listen(s, MAX_PENDING); 

  /* wait for connection, then receive and print text */ 
  while(1) { 

    while (len = recvfrom(s, buf, sizeof(buf), 0,
			  (struct sockaddr *) &clientAddr, &clientAddrLen))
      fputs(buf, stdout);

    printf("**End of data\n");
  } 
}
