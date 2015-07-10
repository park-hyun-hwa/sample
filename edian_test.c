#include<stdio.h>

int main(){
	int i = 0x00000001;
	char *ch = (char *)&i;
	if(ch[0]==1)printf("little"); 
	else printf("big"); 
}
 
