using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using live.videosdk;
using UnityEngine.Android;
using TMPro;
using EasyUI.Toast;
public class GameManager : MonoBehaviour
{
    private bool micToggle;
    private bool camToggle;

    [SerializeField] GameObject _videoSurfacePrefab;
    [SerializeField] Transform _parent;
    [SerializeField] GameObject _meetControlls;
    [SerializeField] GameObject _meetCreateActivity;
    [SerializeField] GameObject _meetJoinActivity;

    private VideoSurface _localParticipant;
    private Meeting videosdk;
    private readonly string _token = "YOUR_TOKEN";
    
    [SerializeField] TMP_Text _meetIdTxt;
    [SerializeField] TMP_InputField _meetIdInputField;

    private List<VideoSurface> _participantList = new List<VideoSurface>();

    private void Awake()
    {
        _meetControlls.SetActive(false);
        _meetCreateActivity.SetActive(false);
        _meetJoinActivity.SetActive(false);
        RequestForPermission(Permission.Camera);
    }
    void Start()
    {
        videosdk = Meeting.GetMeetingObject();

        videosdk.OnCreateMeetingIdCallback += OnCreateMeet;
        videosdk.OnParticipantJoinedCallback += OnParticipantJoined;
        videosdk.OnParticipantLeftCallback += OnParticipantLeft;
        videosdk.OnCreateMeetingIdFailedCallback += OnCreateMeetFailed;
        videosdk.OnMeetingStateChangedCallback += OnMeetingStateChanged;
        videosdk.OnErrorCallback += OnError;
        _meetCreateActivity.SetActive(true);
        _meetJoinActivity.SetActive(true);
    }

    private void OnError(Error error)
    {
        Debug.LogError($"Error-Code: {error.Code} Message: {error.Message} Type: {error.Type}");
        Toast.Show($"OnError: Error-Code: {error.Code} Message: {error.Message}", 3f, Color.red, ToastPosition.MiddleCenter);
    }

    private void OnParticipantJoined(IParticipant obj)
    {   
        Debug.Log($"On Pariticpant Joined: " + obj.ToString());
        Toast.Show($"<color=green>PariticpantJoined: </color> {obj.ToString()}", 1f, ToastPosition.TopCenter);
        VideoSurface participant = Instantiate(_videoSurfacePrefab, _parent.transform).GetComponentInChildren<VideoSurface>();
        participant.SetVideoSurfaceType(VideoSurfaceType.RawImage);//For raw Image
        participant.SetParticipant(obj);
        participant.SetEnable(true);
        _participantList.Add(participant);
        if (obj.IsLocal)
        {
            _localParticipant = participant;
             _localParticipant.OnStreamEnableCallback += OnStreamEnable;
             _localParticipant.OnStreamDisableCallback += OnStreamDisable;
            _meetIdTxt.text = videosdk.MeetingID;
            _meetIdInputField.text = string.Empty;
            _meetCreateActivity.SetActive(false);
            _meetJoinActivity.SetActive(false);
            _meetControlls.SetActive(true);

        }
    }

    private void OnStreamDisable(StreamKind kind)
    {
        Debug.Log($"OnStreamDisable {kind}");
        camToggle = _localParticipant.CamEnabled;
        micToggle = _localParticipant.MicEnabled;
    }

    private void OnStreamEnable(StreamKind kind)
    {
        Debug.Log($"OnStreamEnable {kind}");
        camToggle = _localParticipant.CamEnabled;
        micToggle = _localParticipant.MicEnabled;
    }

    private void OnParticipantLeft(IParticipant obj)
    {
        Debug.Log($"On Pariticpant Left: " + obj.ToString());
        Toast.Show($"<color=yellow>PariticpantLeft: </color> {obj.ToString()}", 2f, ToastPosition.TopCenter);
        if (obj.IsLocal)
        {
            OnLeave();
        }
        else
        {
            VideoSurface participant = null;
            for (int i = 0; i < _participantList.Count; i++)
            {
                if(obj.Id== _participantList[i].ParticipantId)
                {
                    participant = _participantList[i];
                    _participantList.RemoveAt(i);
                    break;
                }
                
            }
            if(participant!=null)
            {
                Destroy(participant.transform.parent.gameObject);
            }
        }
    }

    private void OnLeave()
    {
        _meetCreateActivity.SetActive(true);
        _meetJoinActivity.SetActive(true);
        _meetControlls.SetActive(false);
        camToggle = true;
        micToggle = true;
        for (int i = 0; i < _participantList.Count; i++)
        {
            Destroy(_participantList[i].transform.parent.gameObject);
        }
        _participantList.Clear();
        _meetIdTxt.text = "VideoSDK Unity Demo";
    }

    private void OnCreateMeet(string meetId)
    {
        _meetIdTxt.text = meetId;
        videosdk.Join(_token, meetId, "User", true, true);
    }

    public void CreateMeeting()
    {
        Debug.Log("User Request for Create meet-ID");
        _meetCreateActivity.SetActive(false);
        _meetJoinActivity.SetActive(false);
        videosdk.CreateMeetingId(_token);
    }

    private void OnCreateMeetFailed(string obj)
    {
        _meetCreateActivity.SetActive(true);
        _meetJoinActivity.SetActive(true);
        Debug.LogError(obj);
        Toast.Show($"OnCreateMeetFailed: {obj}", 1f, Color.red, ToastPosition.TopCenter);
    }

    private void OnMeetingStateChanged(MeetingState obj)
    {
        Toast.Show($"<color=yellow>MeetingStateChanged: </color> {obj}", 2f, ToastPosition.TopCenter);
        Debug.Log($"MeetingStateChanged: {obj}");
    }

    public void JoinMeet()
    {
        if (string.IsNullOrEmpty(_meetIdInputField.text)) return;

        try
        {
            videosdk.Join(_token, _meetIdInputField.text, "User", true, false);
        }
        catch (Exception ex)
        {
            Debug.LogError("Join Meet Failed: " + ex.Message);
        }
    }

    public void CamToggle()
    {
        camToggle = !camToggle;
        Debug.Log("Cam Toggle " + camToggle);
        _localParticipant?.SetVideo(camToggle);
    }
    public void AudioToggle()
    {
        micToggle = !micToggle;
        Debug.Log("Mic Toggle " + micToggle);
        _localParticipant?.SetAudio(micToggle);
    }

    public void LeaveMeeting()
    {
        videosdk?.Leave();
    }

    private void OnApplicationPause(bool pause)
    {
        if (_participantList.Count > 1)
        {
            AudioStream(pause);
            VideoStream(pause);

        }

    }

    private void AudioStream(bool status)
    {
        foreach (var participant in _participantList)
        {
            if (!participant.IsLocal)
            {
                switch (status)
                {
                    case true:
                        {
                            participant.PauseStream(StreamKind.AUDIO);
                            break;
                        }
                    case false:
                        {
                            participant.ResumeStream(StreamKind.AUDIO);
                            break;
                        }
                }
            }

        }
        _localParticipant?.SetAudio(!status);
    }

    private void VideoStream(bool status)
    {
        foreach (var participant in _participantList)
        {
            if (!participant.IsLocal)
            {
                switch (status)
                {
                    case true:
                        {
                            participant.PauseStream(StreamKind.VIDEO);
                            break;
                        }
                    case false:
                        {
                            participant.ResumeStream(StreamKind.VIDEO);
                            break;
                        }
                }
            }

        }
    }



    private void OnPermissionGranted(string permissionName)
    {
        if (Permission.HasUserAuthorizedPermission(Permission.Microphone) && Permission.HasUserAuthorizedPermission(Permission.Camera))
        {
            return;
        }
        RequestForPermission(Permission.Microphone);

    }

    private void OnPermissionDenied(string permissionName)
    {
       // Debug.LogError($"VideoSDK can't Initialize {permissionName} Denied");

    }

    private void OnPermissionDeniedAndDontAskAgain(string permissionName)
    {
       // Debug.LogError($"VideoSDK can't Initialize {permissionName} Denied And DontAskAgain");
    }


    private void RequestForPermission(string permission)
    {
        if (Application.platform == RuntimePlatform.Android)
        {
            if (Permission.HasUserAuthorizedPermission(Permission.Microphone) && Permission.HasUserAuthorizedPermission(Permission.Camera))
            {
                // The user authorized use of the microphone.
                OnPermissionGranted("");
            }
            else
            {
                var callbacks = new PermissionCallbacks();
                callbacks.PermissionDenied += OnPermissionDenied;
                callbacks.PermissionGranted += OnPermissionGranted;
                callbacks.PermissionDeniedAndDontAskAgain += OnPermissionDeniedAndDontAskAgain;
                Permission.RequestUserPermission(permission, callbacks);
            }
        }

    }


}
