#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("please provide one argument \n");
    return 1;
  }

  intptr_t addr = atoi(argv[1]);
  char *ptr = (char *)addr;

  printf("%c\n", *ptr);
}
