// SPDX-FileCopyrightText: The LineageOS Project
// SPDX-License-Identifier: Apache-2.0

// Host-only ION contract fixture. Link wrapping prevents real device access.
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <ion/ion.h>
#include <linux/ion_4.19.h>

_Static_assert(sizeof(struct ion_new_allocation_data) == 24, "BLA modern ION ABI");

static int open_calls, probe_calls, alloc_calls, close_calls;
static int fail_open, fail_alloc, fail_close;

#define CHECK(expr) do { \
    if (!(expr)) { \
        fprintf(stderr, "contract failed at line %d: %s\n", __LINE__, #expr); \
        exit(1); \
    } \
} while (0)

int __wrap_open(const char* path, int flags, ...) {
    CHECK(strcmp(path, "/dev/ion") == 0);
    CHECK(flags == (O_RDONLY | O_CLOEXEC));
    open_calls++;
    if (fail_open) {
        errno = EACCES;
        return -1;
    }
    return 17;
}

int __wrap_close(int fd) {
    CHECK(fd == 17);
    close_calls++;
    if (fail_close) {
        errno = EBADF;
        return -1;
    }
    return 0;
}

int __wrap_ioctl(int fd, unsigned long request, ...) {
    CHECK(fd == 17);
    va_list ap;
    va_start(ap, request);
    void* arg = va_arg(ap, void*);
    va_end(ap);
    // The kernel command is unsigned int; libc may receive sign-extended int.
    switch ((uint32_t)request) {
        case 0xc0044901U: // Old handle FREE probe: absent on the measured modern ABI.
            CHECK(arg != NULL);
            probe_calls++;
            errno = ENOTTY;
            return -1;
        case 0xc0184900U: { // 24-byte allocation request, independently measured.
            struct ion_new_allocation_data* data = arg;
            CHECK(data != NULL);
            CHECK(data->len == 8192);
            CHECK(data->heap_id_mask == 0x10);
            CHECK(data->flags == 3);
            CHECK(data->unused == 0);
            alloc_calls++;
            if (fail_alloc) {
                errno = ENOMEM;
                return -1;
            }
            data->fd = 25;
            return 0;
        }
        default:
            fprintf(stderr, "unexpected ioctl: 0x%x\n", (uint32_t)request);
            exit(1);
    }
}

// No platform log backend or /dev/log access is needed for host error cases.
int __android_log_print(int priority, const char* tag, const char* format, ...) {
    (void)priority;
    (void)tag;
    (void)format;
    return 0;
}

int main(int argc, char** argv) {
    CHECK(argc == 2);
    if (strcmp(argv[1], "null_output") == 0) {
        CHECK(ion_alloc_fd(17, 8192, 4096, 0x10, 3, NULL) == -EINVAL);
        CHECK(open_calls == 0 && probe_calls == 0 && alloc_calls == 0);
        return 0;
    }
    if (strcmp(argv[1], "open_error") == 0) {
        fail_open = 1;
        CHECK(ion_open() == -1);
        CHECK(errno == EACCES && open_calls == 1);
        CHECK(probe_calls == 0 && alloc_calls == 0);
        return 0;
    }

    int fd = ion_open();
    CHECK(fd == 17 && open_calls == 1);
    if (strcmp(argv[1], "close_error") == 0) {
        fail_close = 1;
        CHECK(ion_close(fd) == -EBADF);
        CHECK(close_calls == 1);
        return 0;
    }
    CHECK(strcmp(argv[1], "allocation") == 0 || strcmp(argv[1], "allocation_error") == 0);
    fail_alloc = strcmp(argv[1], "allocation_error") == 0;
    int buffer_fd = -1;
    int result = ion_alloc_fd(fd, 8192, 4096, 0x10, 3, &buffer_fd);
    CHECK(result == (fail_alloc ? -ENOMEM : 0));
    CHECK(buffer_fd == (fail_alloc ? -1 : 25));
    CHECK(probe_calls == 1 && alloc_calls == 1);
    CHECK(ion_close(fd) == 0 && close_calls == 1);
    return 0;
}
