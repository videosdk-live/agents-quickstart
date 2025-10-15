if(NOT TARGET hermes-engine::libhermes)
add_library(hermes-engine::libhermes SHARED IMPORTED)
set_target_properties(hermes-engine::libhermes PROPERTIES
    IMPORTED_LOCATION "/Users/pavanfaldu/.gradle/caches/8.13/transforms/fe598eff553706dec655b21cae0de175/transformed/hermes-android-0.79.3-debug/prefab/modules/libhermes/libs/android.x86_64/libhermes.so"
    INTERFACE_INCLUDE_DIRECTORIES "/Users/pavanfaldu/.gradle/caches/8.13/transforms/fe598eff553706dec655b21cae0de175/transformed/hermes-android-0.79.3-debug/prefab/modules/libhermes/include"
    INTERFACE_LINK_LIBRARIES ""
)
endif()

