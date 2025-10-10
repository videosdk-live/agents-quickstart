//
//  MeetingViewController.swift
//  videosdk-agents-quickstart-ios
//
//  Created by Deep Bhupatkar on 10/10/25.
//


import Foundation
import VideoSDKRTC

class MeetingViewController: ObservableObject {
    
    var token = "YOUR_VIDEOSDK_AUTH_TOKEN" // Add Your token here
    var meetingId: String = ""
    var name: String = ""
    
    @Published var meeting: Meeting? = nil
    @Published var participants: [Participant] = []
    @Published var meetingID: String = ""
    
    func initializeMeeting(meetingId: String, userName: String) {
        meeting = VideoSDK.initMeeting(
            meetingId: meetingId,
            participantName: userName,
            micEnabled: true,
            webcamEnabled: false
        )
        
        meeting?.addEventListener(self)
        meeting?.join()
    }
}

extension MeetingViewController: MeetingEventListener {
    
    func onMeetingJoined() {
        guard let localParticipant = self.meeting?.localParticipant else { return }
        
        // add to list
        participants.append(localParticipant)
        
        localParticipant.addEventListener(self)
        
    }
    
    func onParticipantJoined(_ participant: Participant) {
        participants.append(participant)
        
        // add listener
        participant.addEventListener(self)
        
    }
    
    func onParticipantLeft(_ participant: Participant) {
        participants = participants.filter({ $0.id != participant.id })
    }
    
    func onMeetingLeft() {
        meeting?.localParticipant.removeEventListener(self)
        meeting?.removeEventListener(self)
    }
    
    func onMeetingStateChanged(meetingState: MeetingState) {
        switch meetingState {
        case .DISCONNECTED:
            participants.removeAll()
        default:
            print("")
        }
    }
}

extension MeetingViewController: ParticipantEventListener {
    
}

extension MeetingViewController {
        
    func joinMeeting(meetingId: String, userName: String) {
        if !token.isEmpty {
            self.meetingID = meetingId
            self.initializeMeeting(meetingId: meetingId, userName: userName)
        }
        else {
            print("Auth token required")
        }
    }
}
