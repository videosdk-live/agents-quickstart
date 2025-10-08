import React, { useEffect, useRef, useState } from "react";
import { MeetingProvider, MeetingConsumer, useMeeting, useParticipant } from "@videosdk.live/react-sdk";
import { TOKEN, ROOM_ID } from "./config";

function ParticipantAudio({ participantId }) {
  const { micStream, micOn, isLocal, displayName } = useParticipant(participantId);
  const audioRef = useRef(null);

  useEffect(() => {
    if (!audioRef.current) return;
    if (micOn && micStream) {
      const mediaStream = new MediaStream();
      mediaStream.addTrack(micStream.track);
      audioRef.current.srcObject = mediaStream;
      audioRef.current.play().catch(() => {});
    } else {
      audioRef.current.srcObject = null;
    }
  }, [micStream, micOn]);

  return (
    <div>
      <p>Participant: {displayName} | Mic: {micOn ? "ON" : "OFF"}</p>
      <audio ref={audioRef} autoPlay muted={isLocal} />
    </div>
  );
}

function Controls() {
  const { leave, toggleMic } = useMeeting();
  return (
    <div>
      <button onClick={() => leave()}>Leave</button>
      <button onClick={() => toggleMic()}>Toggle Mic</button>
    </div>
  );
}

function MeetingView({ meetingId, onMeetingLeave }) {
  const [joined, setJoined] = useState(null);
  const { join, participants } = useMeeting({
    onMeetingJoined: () => setJoined("JOINED"),
    onMeetingLeft: onMeetingLeave,
  });

  const joinMeeting = () => {
    setJoined("JOINING");
    join();
  };

  return (
    <div>
      <h3>Meeting Id: {meetingId}</h3>
      {joined === "JOINED" ? (
        <div>
          <Controls />
          {[...participants.keys()].map((pid) => (
            <ParticipantAudio key={pid} participantId={pid} />
          ))}
        </div>
      ) : joined === "JOINING" ? (
        <p>Joining the meeting...</p>
      ) : (
        <button onClick={joinMeeting}>Join</button>
      )}
    </div>
  );
}

export default function App() {
  const [meetingId] = useState(ROOM_ID);

  const onMeetingLeave = () => {
    // no-op; simple sample
  };

  return (
    <MeetingProvider
      config={{
        meetingId,
        micEnabled: true,
        webcamEnabled: false,
        name: "Agent React User",
        multiStream: false,
      }}
      token={TOKEN}
    >
      <MeetingConsumer>
        {() => <MeetingView meetingId={meetingId} onMeetingLeave={onMeetingLeave} />}
      </MeetingConsumer>
    </MeetingProvider>
  );
}


