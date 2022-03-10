 /* 
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 4
login.c
Matthew Bass
03/09/2022

A function used to login before using the operating system.
*/

#include "types.h"
#include "user.h"
#include "stat.h"
#include "fcntl.h"
#define MAXLEN 30
char *argv[] = { "sh",  0};

/**
 * @brief This is a function to check the password input
 * 
 * @param userInfo the file descriptor
 * @param user The user string
 * @param passwd The password string
 * @return int 
 */
int checkpasswd(int userInfo, char *user, char *passwd){
  int i, n, c,l;
  char ipasswd[MAXLEN];
  char iuser[MAXLEN];
  char buf[1024];
  l = c = 0;
  //chop the \n
  if(user[strlen(user)-1]  == '\n'){
  	user[strlen(user)-1]  = 0;	
  }
  if(passwd[strlen(passwd)-1]  == '\n'){
  	passwd[strlen(passwd)-1]  = 0;	
  }

  while((n = read(userInfo, buf, sizeof(buf))) > 0){
    for(i=0; i<n;) {
      if(l == 0){	
      	while(i < n && buf[i] != ':' )iuser[c++] = buf[i++];
      	if(i == n) break; 
      	iuser[c] = '\0';
      	i++;
      }
      while(i <n && buf[i] != ':')ipasswd[l++] = buf[i++];
      if(i == n) break;
      ipasswd[l] = '\0';
      c = 0;
      l = 0;

      if(!strcmp(user,iuser) && !strcmp(passwd,ipasswd)){
      	char * dirToCreate = "/home/";
      	strcpy(dirToCreate + strlen(dirToCreate), user);
     
      	mkdir(dirToCreate);
      	return 1;
      }
      while(i <n && buf[i++] != '\n');

    }
  }
  return 0; 
}

/**
 * @brief The main function to log a user in before they can use the shell
 * 
 * @return int 
 */
int main(void){
	int pid, wpid, userInfo;
	int loggedIn = 1;
	mkdir("/home/");
	while(loggedIn){
		printf(1,"Username: ");
		char * username = gets("username", MAXLEN);
		printf(1,"Password: ");
		char * password = gets("password", MAXLEN);
		//printf(1,"%s, %s\n",username, password);
		dup(0);  // stdout
		dup(0);  // stderr
		//printf(1, "init: starting sh\n");
		if((userInfo = open("/usersInfo", O_RDONLY)) < 0){
		printf(1, "login: cannot open %s\n", argv[1]);
			exit();
		}
		if(checkpasswd(userInfo,username,password)){
			loggedIn = 0;
			printf(1,"Welcome back %s\n", username);
			pid = fork();
			if(pid < 0){
			  printf(1, "login: fork failed\n");
			  exit();
			}
			if(pid == 0){
				char * uname[] = {username};
			  exec("sh", uname);
			  printf(1, "login: exec sh failed\n");
			  exit();
			}
		}
		else{
			printf(1,"wrong username or password\n");
		}
		close(userInfo);
		while((wpid=wait()) >= 0 && wpid != pid)
		  printf(1, "zombie!\n"); 
			
	}
	
	wait();
	exit();
	
	return 0;
}