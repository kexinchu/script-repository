/*
 *  ��������demo47_biz.cpp���˳�����ʾ����freecplus��ܵ�CTcpClient��ʵ��socketͨ�ŵĿͻ��ˡ�
 *  ������ҵ��ʾ����
 *  ���ߣ�C���Լ�����(www.freecplus.net) ���ڣ�20190525
*/
#include "_freecplus.h"
 
CTcpClient TcpClient;   // �����ͻ��˵Ķ���

bool biz000();  // �����������ġ�
bool biz001();  // �����֤
bool biz002();  // ����ѯ

int main(int argc,char *argv[])
{
  if (argc!=3)
  {
    printf("Using:./demo47_biz ip port\nExample:./demo47_biz 172.21.0.3 5005\n\n"); return -1;
  }

  if (TcpClient.ConnectToServer(argv[1],atoi(argv[2]))==false) // �����˷�����������
  {
    printf("TcpClient.ConnectToServer(\"%s\",%s) failed.\n",argv[1],argv[2]); return -1;
  }

  /*
  // �����֤
  if (biz001()==false)
  {
    printf("biz001() failed.\n"); return -1;
  }

  sleep(10);

  biz002(); // ����ѯ

  sleep(5);

  biz002(); // ����ѯ
  */

  for (int ii=0;ii<10;ii++)
  {
    if (biz000()==false) break;

    sleep(10);
  }

  // ����ֱ���˳��������������ͷ���Դ��
}

// �����֤��
bool biz001()
{
  char strbuffer[1024];    // ������ݵĻ�������
 
  memset(strbuffer,0,sizeof(strbuffer));
  snprintf(strbuffer,1000,"<bizcode>1</bizcode><username>wucz</username><password>p@ssw0rd</password>");
  printf("���ͣ�%s\n",strbuffer);
  if (TcpClient.Write(strbuffer)==false) return false;    // �����˷��������ġ�
 
  memset(strbuffer,0,sizeof(strbuffer));
  if (TcpClient.Read(strbuffer,20)==false) return false;  // ���շ���˵Ļ�Ӧ���ġ�
  printf("���գ�%s\n",strbuffer);

  int iretcode=-1;
  GetXMLBuffer(strbuffer,"retcode",&iretcode);

  if (iretcode==0) { printf("�����֤�ɹ���\n"); return true; }
 
  printf("�����֤ʧ�ܡ�\n"); 

  return false;
}
 
// ����ѯ
bool biz002()
{
  char strbuffer[1024];    // ������ݵĻ�������
 
  memset(strbuffer,0,sizeof(strbuffer));
  snprintf(strbuffer,1000,"<bizcode>2</bizcode><cardid>62620000000001</cardid>");
  printf("���ͣ�%s\n",strbuffer);
  if (TcpClient.Write(strbuffer)==false) return false;    // �����˷��������ġ�
 
  memset(strbuffer,0,sizeof(strbuffer));
  if (TcpClient.Read(strbuffer,20)==false) return false;  // ���շ���˵Ļ�Ӧ���ġ�
  printf("���գ�%s\n",strbuffer);

  int iretcode=-1;
  GetXMLBuffer(strbuffer,"retcode",&iretcode);

  if (iretcode==0) { printf("��ѯ���ɹ���\n"); return true; }
 
  printf("��ѯ���ʧ�ܡ�\n"); 

  return false;
}
 
bool biz000()  // �����������ġ�
{
  char strbuffer[1024];    // ������ݵĻ�������
 
  memset(strbuffer,0,sizeof(strbuffer));
  snprintf(strbuffer,1000,"<bizcode>0</bizcode>");
  //printf("���ͣ�%s\n",strbuffer);
  if (TcpClient.Write(strbuffer)==false) return false;    // �����˷��������ġ�
 
  memset(strbuffer,0,sizeof(strbuffer));
  if (TcpClient.Read(strbuffer,20)==false) return false;  // ���շ���˵Ļ�Ӧ���ġ�
  //printf("���գ�%s\n",strbuffer);

  return true;
}
 
