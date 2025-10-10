import 'package:flutter/material.dart';
import 'package:videosdk/videosdk.dart';

class ParticipantTile extends StatefulWidget {
  final Participant participant;
  const ParticipantTile({super.key, required this.participant});

  @override
  State<ParticipantTile> createState() => _ParticipantTileState();
}

class _ParticipantTileState extends State<ParticipantTile> {
  var pariticpantName;
  @override
  void initState() {
    pariticpantName = widget.participant.displayName;

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Container(
        color: Colors.grey.shade800,
        child: Center(
          child: Text(
            '$pariticpantName',
            style: TextStyle(color: Colors.white),
          ),
        ),
      ),
    );
  }
}
