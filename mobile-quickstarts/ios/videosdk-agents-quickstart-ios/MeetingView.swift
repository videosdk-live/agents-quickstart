//
//  MeetingView.swift
//  videosdk-agents-quickstart-ios
//
//  Created by Deep Bhupatkar on 10/10/25.
//

import SwiftUI
import VideoSDKRTC

struct MeetingView: View{

@Environment(\.presentationMode) var presentationMode

@ObservedObject var meetingViewController = MeetingViewController()
@State var meetingId: String?
@State var userName: String?
@State var isUnMute: Bool = true

var body: some View {
    VStack {
        if meetingViewController.participants.count == 0 {
            Text("Meeting Initializing")
        } else {
            VStack {
                VStack(spacing: 20) {
                    Text("Meeting ID: \(meetingViewController.meetingID)")
                        .padding(.vertical)
                    
                    List {
                        ForEach(meetingViewController.participants.indices, id: \.self) { index in
                            Text("Participant Name: \(meetingViewController.participants[index].displayName)")
                        }
                    }
                }
                
                VStack {
                    HStack(spacing: 15) {
                        // mic button
                        Button {
                            if isUnMute {
                                isUnMute = false
                                meetingViewController.meeting?.muteMic()
                            }
                            else {
                                isUnMute = true
                                meetingViewController.meeting?.unmuteMic()
                            }
                        } label: {
                            Text("Toggle Mic")
                                .foregroundStyle(Color.white)
                                .font(.caption)
                                .padding()
                                .background(
                                    RoundedRectangle(cornerRadius: 25)
                                        .fill(Color.blue))
                        }
                        // end meeting button
                        Button {
                            meetingViewController.meeting?.end()
                            presentationMode.wrappedValue.dismiss()
                        } label: {
                            Text("End Call")
                                .foregroundStyle(Color.white)
                                .font(.caption)
                                .padding()
                                .background(
                                    RoundedRectangle(cornerRadius: 25)
                                        .fill(Color.red))
                        }
                    }
                    .padding(.bottom)
                }
            }
        }
    }
    .onAppear() {
        /// MARK :- configuring the videoSDK
        VideoSDK.config(token: meetingViewController.token)
        print(meetingId)
        if meetingId?.isEmpty == false {
            print("i ff meeting isd is emty \(meetingId)")
            // join an existing meeting with provided meeting Id
            meetingViewController.joinMeeting(meetingId: meetingId!, userName: userName!)
        }
    }
}
}
