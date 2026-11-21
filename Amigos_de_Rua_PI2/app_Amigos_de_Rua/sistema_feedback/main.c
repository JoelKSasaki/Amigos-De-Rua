#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>

#define SUPABASE_URL "https://brnwhhxzekizjkxuobri.supabase.co/rest/v1/avaliacao"
#define SUPABASE_KEY "sb_publishable_Nxf5kNQo1ts9dUhT3bakNg_Upr14QON"

int ler_notas(char pergunta[]) {
    int nota;

    do {
        printf("%s", pergunta);
        scanf("%i", &nota);

        if (nota < 1 || nota > 5) {
            printf("Informe um número válido!\n");
        }
    }
    while (nota < 1 || nota > 5);

    return nota;
}

int ler_respostas(char pergunta[]) {
    char resposta;

    do {
        printf("%s", pergunta);
        scanf(" %c", &resposta);

        if (resposta != 's' && resposta != 'S' &&
            resposta != 'n' && resposta != 'N') {
            printf("Informe [s] ou [n].\n");
        }

    } while (resposta != 's' && resposta != 'S' &&
             resposta != 'n' && resposta != 'N');

    if (resposta == 's' || resposta == 'S')
        return 1;

    if (resposta == 'n' || resposta == 'N')
        return 0;
}

int main() {

    int nota_atendimento;
    int nota_qualidade;
    int nota_bem_estar;
    char comentario[500];
    int pos;
    int recomendaria;
    int voltaria;
    char pergunta[500];

    // Criar um objeto JSON
    cJSON *json;
    char *dados_json;
    long status_servidor;

    // Criar uma conexão via HTTP
    CURL *curl;
    CURLcode resultado;
    struct curl_slist *headers = NULL;

    printf("=========SISTEMA DE FEEDBACK=========\n\n");

    strcpy(pergunta, "Informe a nota de avaliacao do atendimento: ");
    nota_atendimento = ler_notas(pergunta);

    strcpy(pergunta, "Informe a nota de avaliacao da qualidade do procedimento: ");
    nota_qualidade = ler_notas(pergunta);

    strcpy(pergunta, "Informe o quanto voce se sentiu aliviado apos o procedimento realizado: ");
    nota_bem_estar = ler_notas(pergunta);

    strcpy(pergunta, "Voce voltaria a utilizar o servico? [s]/[n] ");
    voltaria = ler_respostas(pergunta);

    strcpy(pergunta, "Voce recomendaria o servico? [s]/[n] ");
    recomendaria = ler_respostas(pergunta);

    getchar();

    printf("Comentario (opcional): ");
    fgets(comentario, sizeof(comentario), stdin);

    // Criação do objeto JSON
    json = cJSON_CreateObject();

    cJSON_AddNumberToObject(json, "nota_atendimento", nota_atendimento);
    cJSON_AddNumberToObject(json, "nota_qualidade", nota_qualidade);
    cJSON_AddNumberToObject(json, "nota_bem_estar", nota_bem_estar);
    cJSON_AddBoolToObject(json, "retornaria", voltaria);
    cJSON_AddBoolToObject(json, "recomendaria", recomendaria);

    int quantidade = strlen(comentario);

    if (quantidade > 1) {
        pos = strcspn(comentario, "\n");
        comentario[pos] = '\0';
        cJSON_AddStringToObject(json, "comentario", comentario);
    }

    dados_json = cJSON_PrintUnformatted(json);

    // Inicializar cURL
    curl_global_init(CURL_GLOBAL_DEFAULT);

    curl = curl_easy_init();

    if (curl) {

        headers = curl_slist_append(
            headers, "Content-Type: application/json"
        );

        headers = curl_slist_append(
            headers, "Prefer: return=minimal"
        );

        headers = curl_slist_append(
            headers, "apikey: " SUPABASE_KEY
        );

        curl_easy_setopt(curl, CURLOPT_URL, SUPABASE_URL);
        curl_easy_setopt(curl, CURLOPT_CAINFO, "cacert.pem");
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, dados_json);

        resultado = curl_easy_perform(curl);

        if (resultado == CURLE_OK) {

            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_servidor);

            if (status_servidor >= 200 && status_servidor < 300) {
                printf("\nFeedback enviado com sucesso!\n");
            } else {
                printf("\nErro ao enviar. Codigo HTTP: %ld\n", status_servidor);
            }

        } else {
            printf("\nErro na conexao: %s\n",
                   curl_easy_strerror(resultado));
        }

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);

    } else {
        printf("\nErro ao inicializar cURL.\n");
    }

    // Liberar memória
    free(dados_json);
    cJSON_Delete(json);
    curl_global_cleanup();

    return 0;
}
