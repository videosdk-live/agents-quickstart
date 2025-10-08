// getting Elements from Dom
const leaveButton = document.getElementById("leaveBtn");
const toggleMicButton = document.getElementById("toggleMicBtn");
const createButton = document.getElementById("createMeetingBtn");
const audioContainer = document.getElementById("audioContainer");
const textDiv = document.getElementById("textDiv");

// declare Variables
let meeting = null;
let meetingId = "";
let isMicOn = false;

// Join Agent Meeting Button Event Listener
createButton.addEventListener("click", async () => {
  document.getElementById("join-screen").style.display = "none";
  textDiv.textContent = "Please wait, we are joining the meeting";

  // For dynamic meeting ID
//   const url = `https://api.videosdk.live/v2/rooms`;
//   const options = {
//     method: "POST",
//     headers: { Authorization: TOKEN, "Content-Type": "application/json" },
//   };

//   const { roomId } = await fetch(url, options)
//     .then((response) => response.json())
//     .catch((error) => alert("error", error));
//   meetingId = roomId;
  // Use static meeting ID from config instead of creating new room
  meetingId = ROOM_ID;

  initializeMeeting();
});

// Initialize meeting
function initializeMeeting() {
  window.VideoSDK.config(TOKEN);

  meeting = window.VideoSDK.initMeeting({
    meetingId: meetingId, // required
    name: "C.V.Raman", // required
    micEnabled: true, // optional, default: true
    webcamEnabled: false, // disabled - audio only
  });

  meeting.join();

  // setting local participant stream (audio only)
  meeting.localParticipant.on("stream-enabled", (stream) => {
    if (stream.kind === "audio") {
      setAudioTrack(stream, meeting.localParticipant, true);
    }
  });

  meeting.on("meeting-joined", () => {
    textDiv.textContent = null;

    document.getElementById("grid-screen").style.display = "block";
    document.getElementById(
      "meetingIdHeading"
    ).textContent = `Meeting Id: ${meetingId}`;
  });

  meeting.on("meeting-left", () => {
    audioContainer.innerHTML = "";
  });

  //  participant joined (audio only)
  meeting.on("participant-joined", (participant) => {
    let audioElement = createAudioElement(participant.id);

    participant.on("stream-enabled", (stream) => {
      if (stream.kind === "audio") {
        setAudioTrack(stream, participant, false);
        audioContainer.appendChild(audioElement);
      }
    });
  });

  // participants left
  meeting.on("participant-left", (participant) => {
    let aElement = document.getElementById(`a-${participant.id}`);
    if (aElement) {
      aElement.remove();
    }
  });
}

// Audio-only mode - no video elements needed

// creating audio element
function createAudioElement(pId) {
  let audioElement = document.createElement("audio");
  audioElement.setAttribute("autoPlay", "false");
  audioElement.setAttribute("playsInline", "true");
  audioElement.setAttribute("controls", "false");
  audioElement.setAttribute("id", `a-${pId}`);
  audioElement.style.display = "none";
  return audioElement;
}

// Audio-only mode - no local participant video needed

// setting audio track only
function setAudioTrack(stream, participant, isLocal) {
  if (stream.kind === "audio") {
    if (isLocal) {
      isMicOn = true;
    } else {
      const audioElement = document.getElementById(`a-${participant.id}`);
      if (audioElement) {
        const mediaStream = new MediaStream();
        mediaStream.addTrack(stream.track);
        audioElement.srcObject = mediaStream;
        audioElement
          .play()
          .catch((error) => console.error("audioElem.play() failed", error));
      }
    }
  }
}

// leave Meeting Button Event Listener
leaveButton.addEventListener("click", async () => {
  meeting?.leave();
  document.getElementById("grid-screen").style.display = "none";
  document.getElementById("join-screen").style.display = "block";
});

// Toggle Mic Button Event Listener
toggleMicButton.addEventListener("click", async () => {
  if (isMicOn) {
    // Disable Mic in Meeting
    meeting?.muteMic();
  } else {
    // Enable Mic in Meeting
    meeting?.unmuteMic();
  }
  isMicOn = !isMicOn;
});

// Audio-only mode - no webcam toggle needed