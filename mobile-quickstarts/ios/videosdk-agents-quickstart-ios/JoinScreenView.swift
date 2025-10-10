//
//  JoinScreenView.swift
//  videosdk-agents-quickstart-ios
//
//  Created by Deep Bhupatkar on 10/10/25.
//

import SwiftUI

struct JoinScreenView: View {
    
    // State variables for
    let meetingId: String = "YOUR_MEETING_ID"
    @State var name: String
    
    var body: some View {
        NavigationView {
            VStack {
                Text("VideoSDK")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                Text("AI Agent Quickstart")
                    .font(.largeTitle)
                    .fontWeight(.semibold)
                    .padding(.bottom)
                
                TextField("Enter Your Name", text: $name)
                    .foregroundColor(Color.black)
                    .autocorrectionDisabled()
                    .font(.headline)
                    .overlay(
                        Image(systemName: "xmark.circle.fill")
                            .padding()
                            .offset(x: 10)
                            .foregroundColor(Color.gray)
                            .opacity(name.isEmpty ? 0.0 : 1.0)
                            .onTapGesture {
                                UIApplication.shared.endEditing()
                                name = ""
                            }
                        , alignment: .trailing)
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 25)
                            .fill(Color.secondary.opacity(0.5))
                            .shadow(color: Color.gray.opacity(0.10), radius: 10))
                    .padding()
                
                NavigationLink(destination: MeetingView(meetingId: self.meetingId, userName: name ?? "Guest")
                    .navigationBarBackButtonHidden(true)) {
                        Text("Join Meeting")
                            .foregroundColor(Color.white)
                            .padding()
                            .background(
                                RoundedRectangle(cornerRadius: 25.0)
                                    .fill(Color.blue))
                    }
            }
        }
    }
}

extension UIApplication {
    
    func endEditing() {
        sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
}
