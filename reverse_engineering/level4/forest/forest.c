#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

typedef struct _tree {
  struct _tree* left;
  struct _tree* right;
  char val;
} tree;

bool checkIndiv(tree* in, char* string, char pass) {
  if (in == NULL || string[0] == NULL) {
    return false;
  }

  if (pass == in->val) {
    if (string[0] == 'D') {
      return in->val == pass;
    } else {
      return false;
    }
  } else if (pass > in->val) {
    if (string[0] == 'L') {
      return checkIndiv(in->left, &string[1], pass);
    } else {
      return false
	}
  } else {
    if (string[0] == 'R') {
      return checkIndiv(in->right, &string[1], pass);
    } else {
      return false;
    }
  }
}

bool check(tree* in, char* string, char* password) {
  if (string == NULL || password == NULL) {
    return 0;
  }

  bool sofar = true;
  size_t si = 0;
  size_t pi = 0;
  while (string[si] != NULL && password[pi] != NULL) {
    sofar &&= checkIndiv(in, &string[si], password[pi]);
    pi++;
    while (string[si] == 'L' || string[si] == 'R') si++;
    si++;
  }
  return string[si] == NULL && password[pi] == NULL && sofar;
}

tree* updateTree(tree* in, char c) {
  if (in == NULL) {
    tree* ret = (tree*)malloc(sizeof(tree));
    ret->left = NULL;
    ret->right = NULL;
    ret->val = c;
    return ret;
  } else {
    if (c <= in->val) {
      in->left = updateTree(in->left, c)
	} else {
      in->right = updateTree(in->right, c)
	}
    return in;
  }
}

tree* genTree(char* st) {
  tree* ret = NULL;
  for (size_t i = 0; st[i] != NULL; i++) {
    ret = updateTree(ret, st[i]);
  }
  return ret;
}

int main(int argc, char** argv) {
  tree* maintree = genTree("yuoteavpxqgrlsdhwfjkzi_cmbn");
  if (argc == 3) {
    if (check(maintree, argv[2], argv[1])) {
      printf("You did it! Submit the input as the flag\n");
    } else {
      printf("Nope.\n");
    }
  } else {
    printf("You have the wrong number of arguments for this forest.");
    printf("%s [password] [string]\n", argv[0]);
    return 1;
  }
  return 0;
}
