/*
 *  程序名：demo48.cpp，此程序演示采用freecplus框架的CTcpServer类实现socket通信的服务端。
 *  作者：C语言技术网(www.freecplus.net) 日期：20190525
*/
#include "_freecplus.h"
 
int main(int argc,char *argv[])
{
  if (argc!=2)
  {
    printf("Using:./demo48 port\nExample:./demo48 5005\n\n"); return -1;
  }

  CTcpServer TcpServer;   // 创建服务端对象。
 
  if (TcpServer.InitServer(atoi(argv[1]))==false) // 初始化TcpServer的通信端口。
  {
    printf("TcpServer.InitServer(%s) failed.\n",argv[1]); return -1;
  }
 
  if (TcpServer.Accept()==false)   // 等待客户端连接。
  {
    printf("TcpServer.Accept() failed.\n"); return -1;
  }
 
  printf("客户端(%s)已连接。\n",TcpServer.GetIP());
 
  char strbuffer[1024];  // 存放数据的缓冲区。
 
  while (true)
  {
    memset(strbuffer,0,sizeof(strbuffer));
    //if (TcpServer.Read(strbuffer,300)==false) break; // 接收客户端发过来的请求报文。
    if (TcpServer.Read(strbuffer,10)==false) break; // 接收客户端发过来的请求报文。
    printf("接收：%s\n",strbuffer);
 
    strcat(strbuffer,"ok");      // 在客户端的报文后加上"ok"。
    printf("发送：%s\n",strbuffer);
    if (TcpServer.Write(strbuffer)==false) break;     // 向客户端回应报文。
  }
 
  printf("客户端已断开。\n");    // 程序直接退出，析构函数会释放资源。
}
