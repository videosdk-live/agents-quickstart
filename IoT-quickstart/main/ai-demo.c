#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/param.h>
#include <sys/time.h>
#include "esp_event.h"
#include "esp_log.h"
#include "esp_mac.h"
#include "esp_netif.h"
#include "esp_partition.h"
#include "esp_system.h"
#include "freertos/FreeRTOS.h"
#include "nvs_flash.h"
#include "protocol_examples_common.h"
#include "videosdk.h"

static const char *TAG = "Videosdk";

const char *token = "YOUR_VIDEOSDK_AUTH_TOKEN"; // Replace with your VideoSDK auth token
static void meeting_task(void *pvParameters)
{

    create_meeting_result_t result = create_meeting(token);
    if (result.room_id)
    {
        ESP_LOGI(TAG, "Created meeting roomId = %s", result.room_id);
        free(result.room_id);
    }
    else
    {
        ESP_LOGE(TAG, "Failed to create meeting");
    }

    ESP_LOGI(TAG, "meeting_task finished, deleting self");
    vTaskDelete(NULL);
}

void app_main(void)
{
    static char deviceid[32] = {0};
    uint8_t mac[8] = {0};

    esp_log_level_set("*", ESP_LOG_INFO);
    esp_log_level_set("esp-tls", ESP_LOG_VERBOSE);
    esp_log_level_set("MQTT_CLIENT", ESP_LOG_VERBOSE);
    esp_log_level_set("MQTT_EXAMPLE", ESP_LOG_VERBOSE);
    esp_log_level_set("TRANSPORT_BASE", ESP_LOG_VERBOSE);
    esp_log_level_set("TRANSPORT", ESP_LOG_VERBOSE);
    esp_log_level_set("OUTBOX", ESP_LOG_VERBOSE);

    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    ESP_ERROR_CHECK(example_connect());

    BaseType_t ok = xTaskCreate(meeting_task, "meeting_task", 16384, (void *)token, 5, NULL);
    if (ok != pdPASS)
    {
        ESP_LOGE(TAG, "Failed to create meeting_task");
    }
    init_config_t init_cfg = {
        .meetingID = "YOUR_MEETING_ID", // Replace with your meeting ID
        .token = token,
        .displayName = "ESP32-Device",
        .audioCodec = AUDIO_CODEC_OPUS,
    };

    result_t init_result = init(&init_cfg);
    printf("Result: %d\n", init_result);
    result_t result_publish = startPublishAudio("");
    result_t result_susbcribe = startSubscribeAudio("", NULL);
    printf("Result:%d\n", result_publish);

    while (1)
    {
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

