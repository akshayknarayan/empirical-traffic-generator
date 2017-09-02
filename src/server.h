#ifndef __server_h
#define __server_h

//#define DEBUG
#define READBUF_SIZE 1048576

/* prototypes */ 
void handle_connection(int sockfd, const struct sockaddr_in *cliaddr);
void print_usage();
void read_args(int argc, char*argv[]);

#endif

