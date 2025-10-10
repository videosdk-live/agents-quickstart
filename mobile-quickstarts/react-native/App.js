import React from 'react';
import {
  SafeAreaView,
  TouchableOpacity,
  Text,
  View,
  FlatList,
} from 'react-native';
import {
  MeetingProvider,
  useMeeting,
} from '@videosdk.live/react-native-sdk';
import { meetingId, token, name } from './constants';

const Button = ({ onPress, buttonText, backgroundColor }) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={{
        backgroundColor: backgroundColor,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 12,
        borderRadius: 4,
      }}>
      <Text style={{ color: 'white', fontSize: 12 }}>{buttonText}</Text>
    </TouchableOpacity>
  );
};

function ControlsContainer({ join, leave, toggleMic }) {
  return (
    <View
      style={{
        padding: 24,
        flexDirection: 'row',
        justifyContent: 'space-between',
      }}>
      <Button
        onPress={() => {
          join();
        }}
        buttonText={'Join'}
        backgroundColor={'#1178F8'}
      />
      <Button
        onPress={() => {
          toggleMic();
        }}
        buttonText={'Toggle Mic'}
        backgroundColor={'#1178F8'}
      />
      <Button
        onPress={() => {
          leave();
        }}
        buttonText={'Leave'}
        backgroundColor={'#FF0000'}
      />
    </View>
  );
}

function ParticipantView({ participantDisplayName }) {
  return (
    <View
      style={{
        backgroundColor: 'grey',
        height: 300,
        justifyContent: 'center',
        alignItems: 'center',
        marginVertical: 8,
        marginHorizontal: 8,
      }}>
      <Text style={{ fontSize: 16 }}>Participant: {participantDisplayName}</Text>
    </View>
  );
}

function ParticipantList({ participants }) {
  return participants.length > 0 ? (
    <FlatList
      data={participants}
      renderItem={({ item }) => {
        return <ParticipantView participantDisplayName={item.displayName} />;
      }}
    />
  ) : (
    <View
      style={{
        flex: 1,
        backgroundColor: '#F6F6FF',
        justifyContent: 'center',
        alignItems: 'center',
      }}>
      <Text style={{ fontSize: 20 }}>Press Join button to enter meeting.</Text>
    </View>
  );
}

function MeetingView() {
  const { join, leave, toggleMic, participants, meetingId } = useMeeting({});

  const participantsList = [...participants.values()].map(participant => ({
    displayName: participant.displayName,
  }));

  return (
    <View style={{ flex: 1 }}>
      {meetingId ? (
        <Text style={{ fontSize: 18, padding: 12 }}>Meeting Id : {meetingId}</Text>
      ) : null}
      <ParticipantList participants={participantsList} />
      <ControlsContainer
        join={join}
        leave={leave}
        toggleMic={toggleMic}
      />
    </View>
  );
}

export default function App() {
  if (!meetingId || !token) {
    return (
      <SafeAreaView style={{ flex: 1, backgroundColor: '#F6F6FF' }}>
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <Text style={{ fontSize: 20, textAlign: 'center' }}>
            Please add a valid Meeting ID and Token in the `constants.js` file.
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#F6F6FF' }}>
      <MeetingProvider
        config={{
          meetingId,
          micEnabled: true,
          webcamEnabled: false,
          name,
        }}
        token={token}>
        <MeetingView />
      </MeetingProvider>
    </SafeAreaView>
  );
}
