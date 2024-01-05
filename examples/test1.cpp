#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
  char buf[32];

  if (argc != 2) {
    printf("please provide one argument \n");
    return 1;
  }

  strcpy(buf, argv[1]); // buffer overflow
  printf("%s\n", buf);
  return 0;
}
