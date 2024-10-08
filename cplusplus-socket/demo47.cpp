/*
 *  程序名：demo47.cpp，此程序演示采用freecplus框架的CTcpClient类实现socket通信的客户端。
 *  作者：C语言技术网(www.freecplus.net) 日期：20190525
*/
#include "_freecplus.h"
 
int main(int argc,char *argv[])
{
  if (argc!=3)
  {
    printf("Using:./demo47 ip port\nExample:./demo47 172.21.0.3 5005\n\n"); return -1;
  }

  CTcpClient TcpClient;   // 创建客户端的对象。
 
  if (TcpClient.ConnectToServer(argv[1],atoi(argv[2]))==false) // 向服务端发起连接请求。
  {
    printf("TcpClient.ConnectToServer(\"%s\",%s) failed.\n",argv[1],argv[2]); return -1;
  }
  
  char strbuffer[1024];    // 存放数据的缓冲区。
 
  for (int ii=0;ii<30;ii++)   // 利用循环，与服务端进行5次交互。
  {
    memset(strbuffer,0,sizeof(strbuffer));
    snprintf(strbuffer,50,"%d:这是第%d个超级女生，编号%03d。",getpid(),ii+1,ii+1);
    printf("发送：%s\n",strbuffer);
    if (TcpClient.Write(strbuffer)==false) break;    // 向服务端发送请求报文。
 
    memset(strbuffer,0,sizeof(strbuffer));
    if (TcpClient.Read(strbuffer,20)==false) break;  // 接收服务端的回应报文。
    printf("接收：%s\n",strbuffer);
 
    sleep(1);
  }
 
  // 程序直接退出，析构函数会释放资源。
}
