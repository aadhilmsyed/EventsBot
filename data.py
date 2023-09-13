# Dictionary of Ban/Kick/Timeout Reasons
ban_reasons     = {}
kick_reasons    = {}
timeout_reasons = {}

# List of restricted announcement channels
restricted_channels = []

# Log Channels
member_logs_channel  = None
message_logs_channel = None
mod_logs_channel     = None
server_logs_channel  = None
voice_logs_channel   = None
event_logs_channel   = None

# API Request Parameters
MAX_REQUESTS = 10
TIME_WINDOW = 3600  # 1 hour in seconds
request_timestamps = []
