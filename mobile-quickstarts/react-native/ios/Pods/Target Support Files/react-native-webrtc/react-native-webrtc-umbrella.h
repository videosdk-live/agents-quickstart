#ifdef __OBJC__
#import <UIKit/UIKit.h>
#else
#ifndef FOUNDATION_EXPORT
#if defined(__cplusplus)
#define FOUNDATION_EXPORT extern "C"
#else
#define FOUNDATION_EXPORT extern
#endif
#endif
#endif

#import "AVCaptureSession+DevicePosition.h"
#import "CaptureController.h"
#import "CapturerEventsDelegate.h"
#import "DataChannelWrapper.h"
#import "RCTConvert+WebRTC.h"
#import "RemoteTrackRegistry.h"
#import "RTCCameraVideoCapturerImp.h"
#import "RTCDispatcher+Private.h"
#import "RTCMediaStreamTrack+React.h"
#import "RTCVideoViewManager.h"
#import "ScreenCaptureController.h"
#import "ScreenCapturePickerViewManager.h"
#import "ScreenCapturer.h"
#import "SerializeUtils.h"
#import "SocketConnection.h"
#import "TrackCapturerEventsEmitter.h"
#import "VideoCaptureController.h"
#import "ProcessorProvider.h"
#import "VideoEffectProcessor.h"
#import "VideoFrameProcessor.h"
#import "WebRTCModule+RTCDataChannel.h"
#import "WebRTCModule+RTCMediaStream.h"
#import "WebRTCModule+RTCPeerConnection.h"
#import "WebRTCModule+VideoTrackAdapter.h"
#import "WebRTCModule.h"
#import "WebRTCModuleOptions.h"

FOUNDATION_EXPORT double react_native_webrtcVersionNumber;
FOUNDATION_EXPORT const unsigned char react_native_webrtcVersionString[];

