import pyaudio
import wave
from typing import Optional


class AudioDeviceController:
    def __init__(self) -> None:
        self.audio: pyaudio.PyAudio = pyaudio.PyAudio()
        self.frames: list[bytes] = []
        self.stream: Optional[pyaudio.Stream] = None

    def _recording_callback(
        self, in_data: bytes | None, frame_count: int, time_info, status
    ) -> tuple[Optional[bytes], int]:
        if in_data is None:
            return None, pyaudio.paContinue

        self.frames.append(in_data)

        return in_data, pyaudio.paContinue

    def start_recording(self) -> None:
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
            stream_callback=self._recording_callback,
        )
        self.frames = []  # Clear previous frames

    def stop_recording(self) -> None:
        print("Recording stopped...")
        self.stream.stop_stream()
        self.stream.close()

    def get_audio(self) -> bytes:
        return b"".join(self.frames)

    def set_audio(self, audio_data: bytes) -> None:
        # the opposite of get_audio
        self.frames = [audio_data]

    def play_audio(self, audio_data: Optional[bytes] = None) -> None:
        if not audio_data:
            audio_data = b"".join(self.frames)
        stream = self.audio.open(
            format=self.audio.get_format_from_width(2),
            channels=1,
            rate=44100,
            output=True,
        )
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()

    def save_audio(self, filename: str) -> None:
        wf = wave.open(filename, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        print(f"Audio saved as '{filename}'")

    def close(self) -> None:
        self.audio.terminate()

    def reset(self) -> None:
        self.close()
        self.__init__()
