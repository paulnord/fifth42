#include <gmp.h>
#include <cstdint>
#include <cgbn/cgbn.h>
int main(){mpz_t a;mpz_init_set_ui(a,42);int ok=mpz_cmp_ui(a,42)==0;mpz_clear(a);return ok?0:1;}
