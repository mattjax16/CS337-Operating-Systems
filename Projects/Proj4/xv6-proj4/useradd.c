 /* 
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 4 (Extension)
useradd.c
Matthew Bass
03/09/2022

A function used to login before using the operating system.
*/
#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"
#define MAXLEN 30


/**
 * @brief Function toadd users to the operating system
 * 
 * @param argc 
 * @param argv 
 * @return int 
 */
int main(int argc, char *argv[]){
  int i, n, c,l;
  char iuser[MAXLEN];
  char buf[1024];
  char userFileBufer[2];
  int userIn;

  l = c = 0;

  // Open the users info
  
  userIn = open("/usersInfo", O_RDWR);
  int usersCount = 0;
  char * newUsername = argv[1];
  char * tempPassword = argv[2];
  char * newHomeDirectory = "/home/";
  if(argc <= 2){
    printf(1,"Usage: Specify user and password, Ex.: userAdd user password\n");
    exit();
  }
  
  // Look through the userInfo to see if the user name already exists
  while((n = read(userIn, buf, sizeof(buf))) > 0){
    for(i=0; i<n; i++) {
      if(l == 0){ 
        if(i != 0){
          i--;  
        }
        while(i < n && buf[i] != ':' ){
          iuser[c++] = buf[i++];
        }
        if(i == n){
          break; 
        } 
        iuser[c] = '\0';
      }
      if(!strcmp(argv[1],iuser)){
        printf(1, "Username already exists\n");
        exit();
      }
      c = 0;
      while(i < n && buf[i++] != '\n');
    }
    
    usersCount++;
  }
  
  // Setting up the home directory for the user
  strcpy(newHomeDirectory + strlen(newHomeDirectory), newUsername);
  mkdir(newHomeDirectory);
  read(userIn, buf, sizeof(buf));
  write(userIn, newUsername,strlen(newUsername));
  write(userIn, ":",1);
  write(userIn, tempPassword, strlen(tempPassword));
  write(userIn, ":",1);
  
  // increment the number of users
  int userNumber = open("/numUsers", O_RDWR);
  read(userNumber, userFileBufer, sizeof(userFileBufer));
  write(userIn, userFileBufer, sizeof(userFileBufer)-1);
  close(userNumber);
  
  // Write the new home directory to usersInfo
  write(userIn, ":",1);
  write(userIn, newHomeDirectory, strlen(newHomeDirectory));
  write(userIn, "\n", 1);
  userFileBufer[0]= userFileBufer[0]+1;
  
  //Re write the numUsers with the file buffer
  userNumber = open("/numUsers", O_RDWR);
  write(userNumber, userFileBufer, sizeof(userFileBufer));

  close(userIn);
  close(userNumber);
  
  exit();
}