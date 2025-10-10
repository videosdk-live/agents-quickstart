import 'package:flutter/material.dart';
import 'api_call.dart';
import 'meeting_screen.dart';

class JoinScreen extends StatelessWidget {
  final _meetingIdController = TextEditingController();

  JoinScreen({super.key});

  void onCreateButtonPressed(BuildContext context) async {
    // call api to create meeting and navigate to MeetingScreen with meetingId,token
    await createMeeting().then((meetingId) {
      if (!context.mounted) return;
      Navigator.of(context).push(
        MaterialPageRoute(
          builder:
              (context) => MeetingScreen(meetingId: meetingId, token: token),
        ),
      );
    });
  }

  void onJoinButtonPressed(BuildContext context) {
    // check meeting id is not null or invaild
    // if meeting id is vaild then navigate to MeetingScreen with meetingId,token
    Navigator.of(context).push(
      MaterialPageRoute(
        builder:
            (context) =>
                MeetingScreen(meetingId: "YOUR_MEETING_ID", token: token),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('VideoSDK QuickStart')),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Center(
          child: ElevatedButton(
            onPressed: () => onJoinButtonPressed(context),
            child: const Text('Join Meeting'),
          ),
        ),
      ),
    );
  }
}
