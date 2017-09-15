#ifndef __common_h
#define __common_h

#include <stdlib.h>
#include <stdbool.h>
#include <sys/time.h>
#include <unistd.h>
#include <math.h>
#include <stdint.h>

/* prototypes */
unsigned int read_exact(int fd, char *buf, size_t count, 
		size_t max_per_read, bool dummy_buf);
unsigned int write_exact(int fd, const char *buf, size_t count, 
		 size_t max_per_write, bool dummy_buf);
unsigned int write_forever(int fd, const char *dummy_buf, size_t max_per_write,
                           const char* log);
uint64_t interval_us(struct timeval start, struct timeval end);

void error(const char *msg);

#endif
