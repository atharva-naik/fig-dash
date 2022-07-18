def add_slave(i_type, psz_uri, b_select):
    """Add a slave to the current media player.
    @note: If the player is playing, the slave will be added directly. This call
    will also update the slave list of the attached L{Media}.
    @param i_type: subtitle or audio.
    @param psz_uri: Uri of the slave (should contain a valid scheme).
    @param b_select: True if this slave should be selected when it's loaded.
    @return: 0 on success, -1 on error.
    @version: LibVLC 3.0.0 and later. See L{media_slaves_add}.
    """

def audio_get_channel():
    """Get current audio channel.
    @return: the audio channel See L{AudioOutputChannel}.
    """

def audio_get_delay():
    """Get current audio delay.
    @return: the audio delay (microseconds).
    @version: LibVLC 1.1.1 or later.
    """

def audio_get_mute():
    """Get current mute status.
    @return: the mute status (boolean) if defined, -1 if undefined/unapplicable.
    """

def audio_get_track():
    """Get current audio track.
    @return: the audio track ID or -1 if no active input.
    """

def audio_get_track_count():
    """Get number of available audio tracks.
    @return: the number of available audio tracks (int), or -1 if unavailable.
    """

def audio_get_track_description():
    """Get the description of available audio tracks."""

def audio_get_volume():
    """Get current software audio volume.
    @return: the software volume in percents (0 = mute, 100 = nominal / 0dB).
    """

def audio_output_device_enum():
    """Gets a list of potential audio output devices,
    See L{audio_output_device_set}().
    @note: Not all audio outputs support enumerating devices.
    The audio output may be functional even if the list is empty (None).
    @note: The list may not be exhaustive.
    @warning: Some audio output devices in the list might not actually work in
    some circumstances. By default, it is recommended to not specify any
    explicit audio device.
    @return: A None-terminated linked list of potential audio output devices. It must be freed with L{audio_output_device_list_release}().
    @version: LibVLC 2.2.0 or later.
    """

def audio_output_device_get():
    """Get the current audio output device identifier.
    This complements L{audio_output_device_set}().
    @warning: The initial value for the current audio output device identifier
    may not be set or may be some unknown value. A LibVLC application should
    compare this value against the known device identifiers (e.g. those that
    were previously retrieved by a call to L{audio_output_device_enum} or
    L{audio_output_device_list_get}) to find the current audio output device.
    It is possible that the selected audio output device changes (an external
    change) without a call to L{audio_output_device_set}. That may make this
    method unsuitable to use if a LibVLC application is attempting to track
    dynamic audio device changes as they happen.
    @return: the current audio output device identifier None if no device is selected or in case of error (the result must be released with free() or L{free}()).
    @version: LibVLC 3.0.0 or later.
    """

def audio_output_device_set(module, device_id):
    """Configures an explicit audio output device.
    If the module paramater is None, audio output will be moved to the device
    specified by the device identifier string immediately. This is the
    recommended usage.
    A list of adequate potential device strings can be obtained with
    L{audio_output_device_enum}().
    However passing None is supported in LibVLC version 2.2.0 and later only;
    in earlier versions, this function would have no effects when the module
    parameter was None.
    If the module parameter is not None, the device parameter of the
    corresponding audio output, if it exists, will be set to the specified
    string. Note that some audio output modules do not have such a parameter
    (notably MMDevice and PulseAudio).
    A list of adequate potential device strings can be obtained with
    L{audio_output_device_list_get}().
    @note: This function does not select the specified audio output plugin.
    L{audio_output_set}() is used for that purpose.
    @warning: The syntax for the device parameter depends on the audio output.
    Some audio output modules require further parameters (e.g. a channels map
    in the case of ALSA).
    @param module: If None, current audio output module. if non-None, name of audio output module.
    @param device_id: device identifier string.
    @return: Nothing. Errors are ignored (this is a design bug).
    """

def audio_output_set(psz_name):
    """Selects an audio output module.
    @note: Any change will take be effect only after playback is stopped and
    restarted. Audio output cannot be changed while playing.
    @param psz_name: name of audio output, use psz_name of See L{AudioOutput}.
    @return: 0 if function succeeded, -1 on error.
    """

def audio_set_callbacks(play, pause, resume, flush, drain, opaque):
    """Sets callbacks and private data for decoded audio.
    Use L{audio_set_format}() or L{audio_set_format_callbacks}()
    to configure the decoded audio format.
    @note: The audio callbacks override any other audio output mechanism.
    If the callbacks are set, LibVLC will B{not} output audio in any way.
    @param play: callback to play audio samples (must not be None).
    @param pause: callback to pause playback (or None to ignore).
    @param resume: callback to resume playback (or None to ignore).
    @param flush: callback to flush audio buffers (or None to ignore).
    @param drain: callback to drain audio buffers (or None to ignore).
    @param opaque: private pointer for the audio callbacks (as first parameter).
    @version: LibVLC 2.0.0 or later.
    """

def audio_set_channel(channel):
    """Set current audio channel.
    @param channel: the audio channel, See L{AudioOutputChannel}.
    @return: 0 on success, -1 on error.
    """

def audio_set_delay(i_delay):
    """Set current audio delay. The audio delay will be reset to zero each time the media changes.
    @param i_delay: the audio delay (microseconds).
    @return: 0 on success, -1 on error.
    @version: LibVLC 1.1.1 or later.
    """

def audio_set_format(format, rate, channels):
    """Sets a fixed decoded audio format.
    This only works in combination with L{audio_set_callbacks}(),
    and is mutually exclusive with L{audio_set_format_callbacks}().
    @param format: a four-characters string identifying the sample format (e.g. "S16N" or "f32l").
    @param rate: sample rate (expressed in Hz).
    @param channels: channels count.
    @version: LibVLC 2.0.0 or later.
    """

def audio_set_format_callbacks(setup, cleanup):
    """Sets decoded audio format via callbacks.
    This only works in combination with L{audio_set_callbacks}().
    @param setup: callback to select the audio format (cannot be None).
    @param cleanup: callback to release any allocated resources (or None).
    @version: LibVLC 2.0.0 or later.
    """

def audio_set_mute(status):
    """Set mute status.
    @param status: If status is true then mute, otherwise unmute @warning This function does not always work. If there are no active audio playback stream, the mute status might not be available. If digital pass-through (S/PDIF, HDMI...) is in use, muting may be unapplicable. Also some audio output plugins do not support muting at all. @note To force silent playback, disable all audio tracks. This is more efficient and reliable than mute.
    """

def audio_set_track(i_track):
    """Set current audio track.
    @param i_track: the track ID (i_id field from track description).
    @return: 0 on success, -1 on error.
    """

def audio_set_volume(i_volume):
    """Set current software audio volume.
    @param i_volume: the volume in percents (0 = mute, 100 = 0dB).
    @return: 0 if the volume was set, -1 if it was out of range.
    """

def audio_set_volume_callback(set_volume):
    """Set callbacks and private data for decoded audio. This only works in
    combination with L{audio_set_callbacks}().
    Use L{audio_set_format}() or L{audio_set_format_callbacks}()
    to configure the decoded audio format.
    @param set_volume: callback to apply audio volume, or None to apply volume in software.
    @version: LibVLC 2.0.0 or later.
    """

def audio_toggle_mute():
    """Toggle mute status.
    """

def can_pause():
    """Can this media player be paused?
    @return: true if the media player can pause \libvlc_return_bool.
    """

def from_param(this):
    """(INTERNAL) ctypes parameter conversion method.
    """

def get_agl():
    """\deprecated Use L{get_nsobject}() instead.
    """

def get_chapter():
    """Get movie chapter.
    @return: chapter number currently playing, or -1 if there is no media.
    """

def get_chapter_count():
    """Get movie chapter count.
    @return: number of chapters in movie, or -1.
    """

def get_chapter_count_for_title(i_title):
    """Get title chapter count.
    @param i_title: title.
    @return: number of chapters in title, or -1.
    """

def get_fps():
    """Get movie fps rate
    This function is provided for backward compatibility. It cannot deal with
    multiple video tracks. In LibVLC versions prior to 3.0, it would also fail
    if the file format did not convey the frame rate explicitly.
    \deprecated Consider using L{media_tracks_get}() instead.
    @return: frames per second (fps) for this playing movie, or 0 if unspecified.
    """

def get_full_chapter_descriptions(i_chapters_of_title):
    """Get the full description of available chapters.
    @param i_chapters_of_title: index of the title to query for chapters (uses current title if set to -1).
    @return: the chapters list
    @version: LibVLC 3.0.0 and later.
    """

def get_full_title_descriptions():
    """Get the full description of available titles.
    @return: the titles list
    @version: LibVLC 3.0.0 and later.
    """

def get_fullscreen():
    """Get current fullscreen status.
    @return: the fullscreen status (boolean) \libvlc_return_bool.
    """

def get_hwnd():
    """Get the Windows API window handle (HWND) previously set with
    L{set_hwnd}(). The handle will be returned even if LibVLC
    is not currently outputting any video to it.
    @return: a window handle or None if there are none.
    """

def get_instance():
    """Return the associated Instance.
    """

def get_length():
    """Get the current movie length (in ms).
    @return: the movie length (in ms), or -1 if there is no media.
    """

def get_media():
    """Get the media used by the media_player.
    @return: the media associated with p_mi, or None if no media is associated.
    """

def get_nsobject():
    """Get the NSView handler previously set with L{set_nsobject}().
    @return: the NSView handler or 0 if none where set.
    """

def get_position():
    """Get movie position as percentage between 0.0 and 1.0.
    @return: movie position, or -1. in case of error.
    """

def get_rate():
    """Get the requested movie play rate.
    @warning: Depending on the underlying media, the requested rate may be
    different from the real playback rate.
    @return: movie play rate.
    """

def get_role():
    """Gets the media role.
    @return: the media player role (
ef libvlc_media_player_role_t).
    @version: LibVLC 3.0.0 and later.
    """

def get_state():
    """Get current movie state.
    @return: the current state of the media player (playing, paused, ...) See L{State}.
    """

def get_time():
    """Get the current movie time (in ms).
    @return: the movie time (in ms), or -1 if there is no media.
    """

def get_title():
    """Get movie title.
    @return: title number currently playing, or -1.
    """

def get_title_count():
    """Get movie title count.
    @return: title number count, or -1.
    """

def get_xwindow():
    """Get the X Window System window identifier previously set with
    L{set_xwindow}(). Note that this will return the identifier
    even if VLC is not currently using it (for instance if it is playing an
    audio-only input).
    @return: an X window ID, or 0 if none where set.
    """

def has_vout():
    """How many video outputs does this media player have?
    @return: the number of video outputs.
    """

def is_playing():
    """is_playing.
    @return: 1 if the media player is playing, 0 otherwise \libvlc_return_bool.
    """

def is_seekable():
    """Is this media player seekable?
    @return: true if the media player can seek \libvlc_return_bool.
    """

def navigate(navigate):
    """Navigate through DVD Menu.
    @param navigate: the Navigation mode.
    @version: libVLC 2.0.0 or later.
    """

def next_chapter():
    """Set next chapter (if applicable).
    """

def next_frame():
    """Display the next frame (if supported).
    """

def pause():
    """Toggle pause (no effect if there is no media).
    """

def play():
    """Play.
    @return: 0 if playback started (and was already started), or -1 on error.
    """

def previous_chapter():
    """Set previous chapter (if applicable).
    """

def program_scrambled():
    """Check if the current program is scrambled.
    @return: true if the current program is scrambled \libvlc_return_bool.
    @version: LibVLC 2.2.0 or later.
    """

def release():
    """Release a media_player after use
    Decrement the reference count of a media player object. If the
    reference count is 0, then L{release}() will
    release the media player object. If the media player object
    has been released, then it should not be used again.
    """

def retain():
    """Retain a reference to a media player object. Use
    L{release}() to decrement reference count.
    """

def set_agl(drawable):
    """\deprecated Use L{set_nsobject}() instead.
    """

def set_android_context(p_awindow_handler):
    """Set the android context.
    @param p_awindow_handler: org.videolan.libvlc.AWindow jobject owned by the org.videolan.libvlc.MediaPlayer class from the libvlc-android project.
    @version: LibVLC 3.0.0 and later.
    """

def set_chapter(i_chapter):
    """Set movie chapter (if applicable).
    @param i_chapter: chapter number to play.
    """

def set_equalizer(p_equalizer):
    """Apply new equalizer settings to a media player.
    The equalizer is first created by invoking L{audio_equalizer_new}() or
    L{audio_equalizer_new_from_preset}().
    It is possible to apply new equalizer settings to a media player whether the media
    player is currently playing media or not.
    Invoking this method will immediately apply the new equalizer settings to the audio
    output of the currently playing media if there is any.
    If there is no currently playing media, the new equalizer settings will be applied
    later if and when new media is played.
    Equalizer settings will automatically be applied to subsequently played media.
    To disable the equalizer for a media player invoke this method passing None for the
    p_equalizer parameter.
    The media player does not keep a reference to the supplied equalizer so it is safe
    for an application to release the equalizer reference any time after this method
    returns.
    @param p_equalizer: opaque equalizer handle, or None to disable the equalizer for this media player.
    @return: zero on success, -1 on error.
    @version: LibVLC 2.2.0 or later.
    """

def set_evas_object(p_evas_object):
    """Set the EFL Evas Object.
    @param p_evas_object: a valid EFL Evas Object (Evas_Object).
    @return: -1 if an error was detected, 0 otherwise.
    @version: LibVLC 3.0.0 and later.
    """

def set_fullscreen(b_fullscreen):
    """Enable or disable fullscreen.
    @warning: With most window managers, only a top-level windows can be in
    full-screen mode. Hence, this function will not operate properly if
    L{set_xwindow}() was used to embed the video in a
    non-top-level window. In that case, the embedding window must be reparented
    to the root window B{before} fullscreen mode is enabled. You will want
    to reparent it back to its normal parent when disabling fullscreen.
    @param b_fullscreen: boolean for fullscreen status.
    """

def set_hwnd(drawable):
    """Set a Win32/Win64 API window handle (HWND).

    Specify where the media player should render its video
    output. If LibVLC was built without Win32/Win64 API output
    support, then this has no effects.

    @param drawable: windows handle of the drawable.
    """

def set_media(p_md):
    """Set the media that will be used by the media_player. If any,
    previous md will be released.
    @param p_md: the Media. Afterwards the p_md can be safely destroyed.
    """

def set_mrl(mrl, options):
    """Set the MRL to play.

    Warning: most audio and video options, such as text renderer,
    have no effects on an individual media. These options must be
    set at the vlc.Instance or vlc.MediaPlayer instanciation.

    @param mrl: The MRL
    @param options: optional media option=value strings
    @return: the Media object
    """

def set_nsobject(drawable):
    """Set the NSView handler where the media player should render its video output.
    Use the vout called "macosx".
    The drawable is an NSObject that follow the VLCOpenGLVideoViewEmbedding
    protocol:
    @code.m
    \@protocol VLCOpenGLVideoViewEmbedding <NSObject>
    - (void)addVoutSubview:(NSView *)view;
    - (void)removeVoutSubview:(NSView *)view;
    \@end
    @endcode
    Or it can be an NSView object.
    If you want to use it along with Qt see the QMacCocoaViewContainer. Then
    the following code should work:
    @code.mm
    
        NSView *video = [[NSView alloc] init];
        QMacCocoaViewContainer *container = new QMacCocoaViewContainer(video, parent);
        L{set_nsobject}(mp, video);
        [video release];
    
    @endcode
    You can find a live example in VLCVideoView in VLCKit.framework.
    @param drawable: the drawable that is either an NSView or an object following the VLCOpenGLVideoViewEmbedding protocol.
    """

def set_pause(do_pause):
    """Pause or resume (no effect if there is no media).
    @param do_pause: play/resume if zero, pause if non-zero.
    @version: LibVLC 1.1.1 or later.
    """

def set_position(f_pos):
    """Set movie position as percentage between 0.0 and 1.0.
    This has no effect if playback is not enabled.
    This might not work depending on the underlying input format and protocol.
    @param f_pos: the position.
    """

def set_rate(rate):
    """Set movie play rate.
    @param rate: movie play rate to set.
    @return: -1 if an error was detected, 0 otherwise (but even then, it might not actually work depending on the underlying media protocol).
    """

def set_renderer(p_item):
    """Set a renderer to the media player
    @note: must be called before the first call of L{play}() to
    take effect.
    See L{renderer_discoverer_new}.
    @param p_item: an item discovered by L{renderer_discoverer_start}().
    @return: 0 on success, -1 on error.
    @version: LibVLC 3.0.0 or later.
    """

def set_role(role):
    """Sets the media role.
    @param role: the media player role (
ef libvlc_media_player_role_t).
    @return: 0 on success, -1 on error.
    """

def set_time(i_time):
    """Set the movie time (in ms). This has no effect if no media is being played.
    Not all formats and protocols support this.
    @param i_time: the movie time (in ms).
    """

def set_title(i_title):
    """Set movie title.
    @param i_title: title number to play.
    """

def set_video_title_display(position, timeout):
    """Set if, and how, the video title will be shown when media is played.
    @param position: position at which to display the title, or libvlc_position_disable to prevent the title from being displayed.
    @param timeout: title display timeout in milliseconds (ignored if libvlc_position_disable).
    @version: libVLC 2.1.0 or later.
    """

def set_xwindow(drawable):
    """Set an X Window System drawable where the media player should render its
    video output. The call takes effect when the playback starts. If it is
    already started, it might need to be stopped before changes apply.
    If LibVLC was built without X11 output support, then this function has no
    effects.
    By default, LibVLC will capture input events on the video rendering area.
    Use L{video_set_mouse_input}() and L{video_set_key_input}() to
    disable that and deliver events to the parent window / to the application
    instead. By design, the X11 protocol delivers input events to only one
    recipient.
    @warning
    The application must call the XInitThreads() function from Xlib before
    L{new}(), and before any call to XOpenDisplay() directly or via any
    other library. Failure to call XInitThreads() will seriously impede LibVLC
    performance. Calling XOpenDisplay() before XInitThreads() will eventually
    crash the process. That is a limitation of Xlib.
    @param drawable: X11 window ID @note The specified identifier must correspond to an existing Input/Output class X11 window. Pixmaps are B{not} currently supported. The default X11 server is assumed, i.e. that specified in the DISPLAY environment variable. @warning LibVLC can deal with invalid X11 handle errors, however some display drivers (EGL, GLX, VA and/or VDPAU) can unfortunately not. Thus the window handle must remain valid until playback is stopped, otherwise the process may abort or crash.
    @bug No more than one window handle per media player instance can be specified. If the media has multiple simultaneously active video tracks, extra tracks will be rendered into external windows beyond the control of the application.
    """

def stop():
    """Stop (no effect if there is no media).
    """

def toggle_fullscreen():
    """Toggle fullscreen status on non-embedded video outputs.
    @warning: The same limitations applies to this function
    as to L{set_fullscreen}().
    """

def toggle_teletext():
    """Toggle teletext transparent status on video output.
    \deprecated use L{video_set_teletext}() instead.
    """

def video_get_adjust_float(option):
    """Get float adjust option.
    @param option: adjust option to get, values of L{VideoAdjustOption}.
    @version: LibVLC 1.1.1 and later.
    """

def video_get_adjust_int(option):
    """Get integer adjust option.
    @param option: adjust option to get, values of L{VideoAdjustOption}.
    @version: LibVLC 1.1.1 and later.
    """

def video_get_aspect_ratio():
    """Get current video aspect ratio.
    @return: the video aspect ratio or None if unspecified (the result must be released with free() or L{free}()).
    """

def video_get_chapter_description(i_title):
    """Get the description of available chapters for specific title.
    @param i_title: selected title.
    @return: list containing description of available chapter for title i_title. It must be freed with L{track_description_list_release}().
    """

def video_get_crop_geometry():
    """Get current crop filter geometry.
    @return: the crop filter geometry or None if unset.
    """

def video_get_cursor(num=0):
    """Get the mouse pointer coordinates over a video as 2-tuple (x, y).

    Coordinates are expressed in terms of the decoded video resolution,
    B{not} in terms of pixels on the screen/viewport.  To get the
    latter, you must query your windowing system directly.

    Either coordinate may be negative or larger than the corresponding
    size of the video, if the cursor is outside the rendering area.

    @warning: The coordinates may be out-of-date if the pointer is not
    located on the video rendering area.  LibVLC does not track the
    mouse pointer if the latter is outside the video widget.

    @note: LibVLC does not support multiple mouse pointers (but does
    support multiple input devices sharing the same pointer).

    @param num: video number (default 0).
    """

def video_get_height(num=0):
    """Get the height of a video in pixels.

    @param num: video number (default 0).
    """

def video_get_logo_int(option):
    """Get integer logo option.
    @param option: logo option to get, values of L{VideoLogoOption}.
    """

def video_get_marquee_int(option):
    """Get an integer marquee option value.
    @param option: marq option to get See libvlc_video_marquee_int_option_t.
    """

def video_get_marquee_string(option):
    """Get a string marquee option value.
    @param option: marq option to get See libvlc_video_marquee_string_option_t.
    """

def video_get_scale():
    """Get the current video scaling factor.
    See also L{video_set_scale}().
    @return: the currently configured zoom factor, or 0. if the video is set to fit to the output window/drawable automatically.
    """

def video_get_size(num=0):
    """Get the video size in pixels as 2-tuple (width, height).

    @param num: video number (default 0).
    """

def video_get_spu():
    """Get current video subtitle.
    @return: the video subtitle selected, or -1 if none.
    """

def video_get_spu_count():
    """Get the number of available video subtitles.
    @return: the number of available video subtitles.
    """

def video_get_spu_delay():
    """Get the current subtitle delay. Positive values means subtitles are being
    displayed later, negative values earlier.
    @return: time (in microseconds) the display of subtitles is being delayed.
    @version: LibVLC 2.0.0 or later.
    """

def video_get_spu_description():
    """Get the description of available video subtitles."""

def video_get_teletext():
    """Get current teletext page requested or 0 if it's disabled.
    Teletext is disabled by default, call L{video_set_teletext}() to enable
    it.
    @return: the current teletext page requested.
    """

def video_get_title_description():
    """Get the description of available titles.
    @return: list containing description of available titles. It must be freed with L{track_description_list_release}().
    """

def video_get_track():
    """Get current video track.
    @return: the video track ID (int) or -1 if no active input.
    """

def video_get_track_count():
    """Get number of available video tracks.
    @return: the number of available video tracks (int).
    """

def video_get_track_description():
    """Get the description of available video tracks."""

def video_get_width(num=0):
    """Get the width of a video in pixels.

    @param num: video number (default 0).
    """

def video_set_adjust_float(option, value):
    """Set adjust option as float. Options that take a different type value are ignored.
    @param option: adust option to set, values of L{VideoAdjustOption}.
    @param value: adjust option value.
    @version: LibVLC 1.1.1 and later.
    """

def video_set_adjust_int(option, value):
    """Set adjust option as integer. Options that take a different type value are ignored.
    Passing libvlc_adjust_enable as option value has the side effect of
    starting (arg !0) or stopping (arg 0) the adjust filter.
    @param option: adust option to set, values of L{VideoAdjustOption}.
    @param value: adjust option value.
    @version: LibVLC 1.1.1 and later.
    """

def video_set_aspect_ratio(psz_aspect):
    """Set new video aspect ratio.
    @param psz_aspect: new video aspect-ratio or None to reset to default @note Invalid aspect ratios are ignored.
    """

def video_set_callbacks(lock, unlock, display, opaque):
    """Set callbacks and private data to render decoded video to a custom area in memory.
    Use L{video_set_format}() or L{video_set_format_callbacks}()
    to configure the decoded format.
    @warning: Rendering video into custom memory buffers is considerably less
    efficient than rendering in a custom window as normal.
    For optimal perfomances, VLC media player renders into a custom window, and
    does not use this function and associated callbacks. It is B{highly
    recommended} that other LibVLC-based application do likewise.
    To embed video in a window, use libvlc_media_player_set_xid() or equivalent
    depending on the operating system.
    If window embedding does not fit the application use case, then a custom
    LibVLC video output display plugin is required to maintain optimal video
    rendering performances.
    The following limitations affect performance:
    - Hardware video decoding acceleration will either be disabled completely,
    or require (relatively slow) copy from video/DSP memory to main memory.
    - Sub-pictures (subtitles, on-screen display, etc.) must be blent into the
    main picture by the CPU instead of the GPU.
    - Depending on the video format, pixel format conversion, picture scaling,
    cropping and/or picture re-orientation, must be performed by the CPU
    instead of the GPU.
    - Memory copying is required between LibVLC reference picture buffers and
    application buffers (between lock and unlock callbacks).
    @param lock: callback to lock video memory (must not be None).
    @param unlock: callback to unlock video memory (or None if not needed).
    @param display: callback to display video (or None if not needed).
    @param opaque: private pointer for the three callbacks (as first parameter).
    @version: LibVLC 1.1.1 or later.
    """

def video_set_crop_geometry(psz_geometry):
    """Set new crop filter geometry.
    @param psz_geometry: new crop filter geometry (None to unset).
    """

def video_set_deinterlace(psz_mode):
    """Enable or disable deinterlace filter.
    @param psz_mode: type of deinterlace filter, None to disable.
    """

def video_set_format(chroma, width, height, pitch):
    """Set decoded video chroma and dimensions.
    This only works in combination with L{video_set_callbacks}(),
    and is mutually exclusive with L{video_set_format_callbacks}().
    @param chroma: a four-characters string identifying the chroma (e.g. "RV32" or "YUYV").
    @param width: pixel width.
    @param height: pixel height.
    @param pitch: line pitch (in bytes).
    @version: LibVLC 1.1.1 or later.
    @bug: All pixel planes are expected to have the same pitch. To use the YCbCr color space with chrominance subsampling, consider using L{video_set_format_callbacks}() instead.
    """

def video_set_format_callbacks(setup, cleanup):
    """Set decoded video chroma and dimensions. This only works in combination with
    L{video_set_callbacks}().
    @param setup: callback to select the video format (cannot be None).
    @param cleanup: callback to release any allocated resources (or None).
    @version: LibVLC 2.0.0 or later.
    """

def video_set_key_input(on):
    """Enable or disable key press events handling, according to the LibVLC hotkeys
    configuration. By default and for historical reasons, keyboard events are
    handled by the LibVLC video widget.
    @note: On X11, there can be only one subscriber for key press and mouse
    click events per window. If your application has subscribed to those events
    for the X window ID of the video widget, then LibVLC will not be able to
    handle key presses and mouse clicks in any case.
    @warning: This function is only implemented for X11 and Win32 at the moment.
    @param on: true to handle key press events, false to ignore them.
    """

def video_set_logo_int(option, value):
    """Set logo option as integer. Options that take a different type value
    are ignored.
    Passing libvlc_logo_enable as option value has the side effect of
    starting (arg !0) or stopping (arg 0) the logo filter.
    @param option: logo option to set, values of L{VideoLogoOption}.
    @param value: logo option value.
    """

def video_set_logo_string(option, psz_value):
    """Set logo option as string. Options that take a different type value
    are ignored.
    @param option: logo option to set, values of L{VideoLogoOption}.
    @param psz_value: logo option value.
    """

def video_set_marquee_int(option, i_val):
    """Enable, disable or set an integer marquee option
    Setting libvlc_marquee_Enable has the side effect of enabling (arg !0)
    or disabling (arg 0) the marq filter.
    @param option: marq option to set See libvlc_video_marquee_int_option_t.
    @param i_val: marq option value.
    """

def video_set_marquee_string(option, psz_text):
    """Set a marquee string option.
    @param option: marq option to set See libvlc_video_marquee_string_option_t.
    @param psz_text: marq option value.
    """

def video_set_mouse_input(on):
    """Enable or disable mouse click events handling. By default, those events are
    handled. This is needed for DVD menus to work, as well as a few video
    filters such as "puzzle".
    See L{video_set_key_input}().
    @warning: This function is only implemented for X11 and Win32 at the moment.
    @param on: true to handle mouse click events, false to ignore them.
    """

def video_set_scale(f_factor):
    """Set the video scaling factor. That is the ratio of the number of pixels on
    screen to the number of pixels in the original decoded video in each
    dimension. Zero is a special value; it will adjust the video to the output
    window/drawable (in windowed mode) or the entire screen.
    Note that not all video outputs support scaling.
    @param f_factor: the scaling factor, or zero.
    """

def video_set_spu(i_spu):
    """Set new video subtitle.
    @param i_spu: video subtitle track to select (i_id from track description).
    @return: 0 on success, -1 if out of range.
    """

def video_set_spu_delay(i_delay):
    """Set the subtitle delay. This affects the timing of when the subtitle will
    be displayed. Positive values result in subtitles being displayed later,
    while negative values will result in subtitles being displayed earlier.
    The subtitle delay will be reset to zero each time the media changes.
    @param i_delay: time (in microseconds) the display of subtitles should be delayed.
    @return: 0 on success, -1 on error.
    @version: LibVLC 2.0.0 or later.
    """

def video_set_subtitle_file(psz_subtitle):
    """Set new video subtitle file.
    \deprecated Use L{add_slave}() instead.
    @param psz_subtitle: new video subtitle file.
    @return: the success status (boolean).
    """

def video_set_teletext(i_page):
    """Set new teletext page to retrieve.
    This function can also be used to send a teletext key.
    @param i_page: teletex page number requested. This value can be 0 to disable teletext, a number in the range ]0;1000[ to show the requested page, or a 
ef L{TeletextKey}. 100 is the default teletext page.
    """

def video_set_track(i_track):
    """Set video track.
    @param i_track: the track ID (i_id field from track description).
    @return: 0 on success, -1 if out of range.
    """

def video_take_snapshot(num, psz_filepath, i_width, i_height):
    """Take a snapshot of the current video window.
    If i_width AND i_height is 0, original size is used.
    If i_width XOR i_height is 0, original aspect-ratio is preserved.
    @param num: number of video output (typically 0 for the first/only one).
    @param psz_filepath: the path of a file or a folder to save the screenshot into.
    @param i_width: the snapshot's width.
    @param i_height: the snapshot's height.
    @return: 0 on success, -1 if the video was not found.
    """

def video_update_viewpoint(p_viewpoint, b_absolute):
    """Update the video viewpoint information.
    @note: It is safe to call this function before the media player is started.
    @param p_viewpoint: video viewpoint allocated via L{video_new_viewpoint}().
    @param b_absolute: if true replace the old viewpoint with the new one. If false, increase/decrease it.
    @return: -1 in case of error, 0 otherwise @note the values are set asynchronously, it will be used by the next frame displayed.
    @version: LibVLC 3.0.0 and later.
    """

def will_play():
    """Is the player able to play.
    @return: boolean \libvlc_return_bool.
    """

