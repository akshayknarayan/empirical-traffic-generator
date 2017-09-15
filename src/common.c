#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include "common.h"

/*
 * This function attemps to read exactly count bytes from file descriptor fd
 * into buffer starting at buf. It repeatedly calls read() until either: 
 * 1. count bytes have been read
 * 2. end of file is reached, or for a network socket, the connection is closed
 * 3. read() produces an error
 * Each internal call to read() is for at most max_per_read bytes. The return 
 * value gives the number of bytes successfully read.  
 * The dummy_buf flag can be set by the caller to indicate that the contents
 * of buf are irrelevant. In this case, all read() calls put their data at 
 * location starting at buf, overwriting previous reads.
 * To avoid buffer overflow, the length of buf should be at least count when
 * dummy_buf = false, and at least min{count, max_per_read} when 
 * dummy_buf = true. 
 */
unsigned int read_exact(int fd, char *buf, size_t count,
		size_t max_per_read, bool dummy_buf)
{
  unsigned int bytes_read = 0;
  do {
    unsigned int bytes_to_read = (count > max_per_read) ? max_per_read : count; 
    char *cur_buf = (dummy_buf) ? buf : (buf + bytes_read);
    int n = read(fd, cur_buf, bytes_to_read);
    if (n <= 0) {
      if (n < 0) 
	perror("read_exact(): ERROR in read");
      break;
    }
    bytes_read += n;
    count -= n;
  } while (count > 0);

  return bytes_read;
}


/*
 * This function attemps to write exactly count bytes from the buffer starting
 * at buf to file referred to by file descriptor fd. It repeatedly calls 
 * write() until either: 
 * 1. count bytes have been written
 * 2. write() produces an error
 * Each internal call to write() is for at most max_per_write bytes. The return 
 * value gives the number of bytes successfully written.  
 * The dummy_buf flag can be set by the caller to indicate that the contents
 * of buf are irrelevant. In this case, all write() calls get their data from 
 * starting location buf.
 * To avoid buffer overflow, the length of buf should be at least count when
 * dummy_buf = false, and at least min{count, max_per_write} when 
 * dummy_buf = true. 
 */
unsigned int write_exact(int fd, const char *buf, size_t count, 
		 size_t max_per_write, bool dummy_buf)
{
  unsigned int bytes_written = 0;
  do {
    unsigned int bytes_to_write = (count > max_per_write) ? max_per_write : count; 
    const char *cur_buf = (dummy_buf) ? buf : (buf + bytes_written);
    int n = write(fd, cur_buf, bytes_to_write);
    if (n < 0) { 
      perror("write_exact(): ERROR in write");
      break;
    }
    bytes_written += n;
    count -= n;
  } while (count > 0);

  return bytes_written;
}

uint64_t interval_us(struct timeval start, struct timeval end) {
  if ((end.tv_sec < start.tv_sec) ||
      ((end.tv_sec == start.tv_sec) && end.tv_usec < start.tv_usec)) {
    printf("Interval finding: Bad timestamps!!");
  }
  uint64_t diff_s  = end.tv_sec  - start.tv_sec;
  int diff_us = end.tv_usec - start.tv_usec;
  uint64_t diff_result_us = (diff_s * 1000000) + diff_us;
  return diff_result_us;
}

unsigned int write_forever(int fd, const char *dummy_buf,
                           size_t max_per_write, const char* log) {
  FILE* fd_log = fopen(log, "w");
  if (fd_log < 0) {
    printf("Cannot open server-side log!\n");
    fd_log = stdout;
  }
  struct timeval expt_start_time;
  struct timeval write_start_time;
  struct timeval write_interval_time;
  int n;
  uint64_t cumulative_bytes = 0;
  uint64_t diff_us;
  gettimeofday(&expt_start_time, NULL);
  do {
    gettimeofday(&write_start_time, NULL);
    n = write(fd, dummy_buf, max_per_write);
    if (n < 0) {
      perror("write_forever(): ERROR in write");
      return -1;
    }
    cumulative_bytes += n;
    gettimeofday(&write_interval_time, NULL);
    diff_us = interval_us(write_start_time, write_interval_time);
    fprintf(fd_log,
            "time %llu cumulative_bytes %llu bytes %d throughput %fMbps\n",
            diff_us, cumulative_bytes, n, 8.0*n/diff_us);
  } while (n > 0);
  close(fd);
  return 0;
}

/* 
 * Output error message and exit.
 */
void error(const char *msg)
{
  perror(msg);
  exit(EXIT_FAILURE);
}
