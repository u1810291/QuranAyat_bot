# BismillahBot -- Explore the Holy Qur'an on Telegram
# May Allah reward Rahiel Kasim
# 
# Copyright (C) 1436-1438 AH  Rahiel Kasim

def message_to_dict(file):
  """Parse file data to store in redis db."""

  if isinstance(file, str):
    return { 'file': file }
  return {
    'audio': {
      'title': file.audio.title,
      'file_id': file.audio.file_id,
      'duration': file.audio.duration,
      'file_name': file.audio.file_name,
      'file_size': file.audio.file_size,
      'mime_type': file.audio.mime_type,
      'performer': file.audio.performer,
      'file_unique_id': file.audio.file_unique_id,
      },
    'channel_chat_created': file.channel_chat_created,
    'chat': {
      'id': file.chat.id,
      'type': file.chat.type,
      'username': file.chat.username,
      'first_name': file.chat.first_name,
      },
    'date': file.date.isoformat(),
    'delete_chat_photo': file.delete_chat_photo,
    'from_user': {
      'id': file.from_user.id,
      'is_bot': file.from_user.is_bot,
      'username': file.from_user.username,
      'first_name': file.from_user.first_name,
      },
    'message_id': file.message_id,
    'group_chat_created': file.group_chat_created,
    'supergroup_chat_created': file.supergroup_chat_created
  }

def save_user(chat_id: int, state: Tuple[int, int, str]):
  """State is a tuple: (surah, ayah, type)"""
  r.set(redis_namespace + str(chat_id),
        json.dumps(state), ex=60 * 60 * 24 * 2)  # keep state for two days for making it month add 31 instead of 2

def get_user(chat_id: int):
  v = r.get(redis_namespace + str(chat_id))
  if v is not None:
      return json.loads(v)

def save_file(filename: str, file_id: str):
  message = ''
  try:
    message = message_to_dict(file_id)
  except Exception as err:
    message = ''
    print("Error", err)
  r.set(redis_namespace + "file:" + filename,
        json.dumps(message), ex=60 * 60 * 24 * 2)  # keep for 2 days for making it month add 31 instead of 2

