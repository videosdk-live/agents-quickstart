idf_component_register(SRCS
  "ai-demo.c"
  INCLUDE_DIRS "."
  REQUIRES mbedtls REQUIRES json  REQUIRES esp_netif  REQUIRES fatfs  REQUIRES vfs REQUIRES  esp_common REQUIRES esp_timer  REQUIRES esp_lcd  REQUIRES nvs_flash REQUIRES bt
)

target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")
