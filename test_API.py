import edge_tts
import asyncio

async def generate_speech(text, output_file="/static/voices/v.mp3"):
    voice = "ru-RU-SvetlanaNeural"  # русский голос
    com = edge_tts.Communicate(text=text, voice=voice)
    await com.save(output_file)

if __name__ == "__main__":
    asyncio.run(generate_speech("яблоко"))


