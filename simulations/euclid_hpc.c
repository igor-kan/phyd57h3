#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

/* Standard Remainder Euclidean Algorithm */
uint64_t gcd_remainder(uint64_t a, uint64_t b) {
    while (b != 0) {
        uint64_t r = a % b;
        a = b;
        b = r;
    }
    return a;
}

/* Branch-free Stein Binary GCD using hardware CTZ intrinsic */
uint64_t gcd_binary_hpc(uint64_t u, uint64_t v) {
    if (u == 0) return v;
    if (v == 0) return u;

    int shift = __builtin_ctzll(u | v);
    u >>= __builtin_ctzll(u);

    do {
        v >>= __builtin_ctzll(v);
        if (u > v) {
            uint64_t t = v;
            v = u;
            u = t;
        }
        v = v - u;
    } while (v != 0);

    return u << shift;
}

int main(void) {
    uint64_t a = 12345678901234ULL;
    uint64_t b = 987654321ULL;

    printf("=== PHYD57 HPC Number Theory Primitives ===\n");
    printf("Inputs: a = %llu, b = %llu\n", (unsigned long long)a, (unsigned long long)b);
    printf("Standard Modulo GCD: %llu\n", (unsigned long long)gcd_remainder(a, b));
    printf("Hardware Binary GCD: %llu\n", (unsigned long long)gcd_binary_hpc(a, b));

    return 0;
}
