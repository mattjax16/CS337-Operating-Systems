 /* 
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 4
password.c
Matthew Bass
03/09/2022

A function to help the user set the password
*/

#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"
#define MAXLEN 30

/**
 * @brief This is the main running function for changing the password of the user
 * 
 * @param username the username the password goes with
 * @param npass the new password
 * @return int 
 */
int makeTempFile(char * username, char * npass){
  char buf[1024], buftemp [1024], newuser[1024];
  int i;
  
  //Open the users info file
  int fd = open("/shadow", O_RDONLY);

  //Create a user file to chage the password
  int tempFile = open("/shadow_temp", O_CREATE | O_RDWR);
  read(fd, buf, sizeof(buf));

  int pos = 0;
  int postemp = 0;
  int found = 0;
  char uname[MAXLEN];
  while(buf[pos]!=0 && !found){
    uname[postemp] = buf[pos];
    buftemp[postemp] = buf[pos];
    if(buf[pos] == ':'){
      uname[postemp] = 0;
      
      if(!strcmp(username, uname)){
        printf(1,"Changing %s's password\n", username);
        
        // the user has been found
        found=1;
      }
      
      // If the user has been found
      if(found){
        pos++;
        
        //Copy over the username and password
        strcpy(newuser,buftemp);
        strcpy(newuser+strlen(newuser),npass);
        postemp=strlen(newuser);
        while(buf[pos]!=':'){
          pos++;
        }
        buftemp[0]=0;
        postemp=0;
        while(buf[pos]!='\n'){
          buftemp[postemp++] = buf[pos++];
        }
        buftemp[postemp] = '\n';
        strcpy(newuser+strlen(newuser),buftemp);
   
        write(tempFile, newuser, strlen(newuser));
        buftemp[0]=0;
        postemp=0;
      }
      else{
        while(buf[pos]!='\n'){
          buftemp[postemp++] = buf[pos++];
        }
        buftemp[postemp] = '\n';
        write(tempFile, buftemp,strlen(buftemp));
      }
      postemp = -1;
      //printf(1,"%s", buftemp);
      for (i = 0; i < sizeof(buftemp); i++){
        buftemp[i] = 0;
      }
      for (i = 0; i < sizeof(uname); i++){
        uname[i] = 0;
      }
    }
    postemp++;
    pos++;
  }
  
  // if the user is not found
  if(!found){
    printf(1,"User %s not found\n", username);
    exit();
  }
  postemp=0;
  while(buf[pos]!=0){
    while(buf[pos]!='\n'){
      buftemp[postemp++] = buf[pos++];
    }
    buftemp[postemp] = '\n';
    write(tempFile, buftemp,strlen(buftemp));
    postemp = 0;
    
    for (i = 0; i < sizeof(buftemp); i++){
        buftemp[i] = 0;
    }
    pos++;
  }
  
  // if the user is found
  if(found){    
    close(fd);
    close(tempFile);
    unlink("/shadow");
    fd = open("/shadow", O_CREATE | O_RDWR);
    tempFile = open("/shadow_temp", O_CREATE | O_RDWR);
    read(tempFile, buftemp, sizeof(buftemp));    
    write(fd, buftemp, strlen(buftemp));
  }
  close(tempFile);
  unlink("/shadow_temp");
  exit();
  return 0;
}

int main(int argc, char *argv[]){
  if (argc <= 2){
    printf(1,"Usage: passwd username new_password\n");
    exit();
  }
  else{
    makeTempFile(argv[1], argv[2]);
    exit();
  }
  return 0;
}