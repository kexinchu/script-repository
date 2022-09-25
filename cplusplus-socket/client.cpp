/*
 * ��������client.cpp���˳���������ʾsocket�Ŀͻ���
 * ���ߣ�C���Լ�����(www.freecplus.net) ���ڣ�20190525
*/
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
 
int main(int argc,char *argv[])
{
  if (argc!=3)
  {
    printf("Using:./client ip port\nExample:./client 127.0.0.1 5005\n\n"); return -1;
  }

  // ��1���������ͻ��˵�socket��
  int sockfd;
  if ( (sockfd = socket(AF_INET,SOCK_STREAM,0))==-1) { perror("socket"); return -1; }
 
  // ��2�����������������������
  struct hostent* h;
  if ( (h = gethostbyname(argv[1])) == 0 )   // ָ������˵�ip��ַ��
  { printf("gethostbyname failed.\n"); close(sockfd); return -1; }
  struct sockaddr_in servaddr;
  memset(&servaddr,0,sizeof(servaddr));
  servaddr.sin_family = AF_INET;
  servaddr.sin_port = htons(atoi(argv[2])); // ָ������˵�ͨ�Ŷ˿ڡ�
  memcpy(&servaddr.sin_addr,h->h_addr,h->h_length);
  if (connect(sockfd, (struct sockaddr *)&servaddr,sizeof(servaddr)) != 0)  // �����˷�����������
  { perror("connect"); close(sockfd); return -1; }

  char buffer[1024];
 
  // ��3����������ͨ�ţ�����һ�����ĺ�ȴ��ظ���Ȼ���ٷ���һ�����ġ�
  for (int ii=0;ii<3;ii++)
  {
    int iret;
    memset(buffer,0,sizeof(buffer));
    sprintf(buffer,"���ǵ�%d������Ů�������%03d��",ii+1,ii+1);
    if ( (iret=send(sockfd,buffer,strlen(buffer),0))<=0) // �����˷��������ġ�
    { perror("send"); break; }
    printf("���ͣ�%s\n",buffer);

    memset(buffer,0,sizeof(buffer));
    if ( (iret=recv(sockfd,buffer,sizeof(buffer),0))<=0) // ���շ���˵Ļ�Ӧ���ġ�
    {
       printf("iret=%d\n",iret); break;
    }
    printf("���գ�%s\n",buffer);
  }
 
  // ��4�����ر�socket���ͷ���Դ��
  close(sockfd);
}

