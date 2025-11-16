import os

if os.getenv("RAILWAY_ENVIRONMENT_NAME"):
  from .settings_prod import *
  print("🚀 Production settings loaded")
else:
  from .settings_dev import *
  print("🛠️ Development settings loaded")
