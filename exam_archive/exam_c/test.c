/* hello */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int main(void)
{
    char a = 'A';
    char b = 'a';

    printf("字符 a 的值为: %c\n", a);
    printf("字符 b 的值为: %c\n", b);

    if (a > b)
    {
        printf("字符 a 大于字符 b\n");
    }
    else if (a < b)
    {
        printf("字符 a 小于字符 b\n");
    }
    else
    {
        printf("字符 a 等于字符 b\n");
    }

    return 0;
}