#include <stdio.h>

int main(int argc, char* argv[]) {
   
  if (argc < 2) {
    printf("please provide one argument \n");
    return 1;
  }
 
  FILE *file = fopen(argv[1], "r");
  char buffer[100];

  fread(buffer, sizeof(char), sizeof(buffer), file); // null pointer reference
  fclose(file);

  return 0;
}
