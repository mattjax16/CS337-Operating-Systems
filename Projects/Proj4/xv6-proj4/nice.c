 /* 
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 4
nice.c
Matthew Bass
03/07/2022

A function used to change the priority of a given process.
*/

#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"


int main(int argc, char *argv[]) {
  int pid, priority;

  if(argc < 3){
        printf(1, "usage: nice pid priority\n");
        exit();
  }

  pid = atoi(argv[1]);
  priority = atoi(argv[2]);

  if (priority < 0 || priority > 20){
  	printf(2, "invalid priority (0-20)!\n");
  	exit();
  }
  chpr(pid, priority);

  // ps();
  exit();
}