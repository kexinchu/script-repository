/*
 *  ��������demo47.cpp���˳�����ʾ����freecplus��ܵ�CTcpClient��ʵ��socketͨ�ŵĿͻ��ˡ�
 *  ���ߣ�C���Լ�����(www.freecplus.net) ���ڣ�20190525
*/
#include "_freecplus.h"
 
int main(int argc,char *argv[])
{
  if (argc!=3)
  {
    printf("Using:./demo47 ip port\nExample:./demo47 172.21.0.3 5005\n\n"); return -1;
  }

  CTcpClient TcpClient;   // �����ͻ��˵Ķ���
 
  if (TcpClient.ConnectToServer(argv[1],atoi(argv[2]))==false) // �����˷�����������
  {
    printf("TcpClient.ConnectToServer(\"%s\",%s) failed.\n",argv[1],argv[2]); return -1;
  }
  
  char strbuffer[1024];    // ������ݵĻ�������
 
  for (int ii=0;ii<30;ii++)   // ����ѭ���������˽���5�ν�����
  {
    memset(strbuffer,0,sizeof(strbuffer));
    snprintf(strbuffer,50,"%d:���ǵ�%d������Ů�������%03d��",getpid(),ii+1,ii+1);
    printf("���ͣ�%s\n",strbuffer);
    if (TcpClient.Write(strbuffer)==false) break;    // �����˷��������ġ�
 
    memset(strbuffer,0,sizeof(strbuffer));
    if (TcpClient.Read(strbuffer,20)==false) break;  // ���շ���˵Ļ�Ӧ���ġ�
    printf("���գ�%s\n",strbuffer);
 
    sleep(1);
  }
 
  // ����ֱ���˳��������������ͷ���Դ��
}
