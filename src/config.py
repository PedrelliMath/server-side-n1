from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="server_side_", env_file=".env", env_file_encoding="utf-8")
    server_host: str = "0.0.0.0"
    server_port: int = 9999
    database_file: str
    init_sql_file: str

settings = Settings(database_file="../database.db", init_sql_file='../init.sql')