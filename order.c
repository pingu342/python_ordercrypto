#include <stdlib.h>
int main(void) {
	int status = system("./order.sh");
	int ret = WEXITSTATUS(status);
	return ret;
}
