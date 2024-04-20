@REM these are the commands that I have needed to run to setup the environment

@REM http://lua-users.org/wiki/SimpleLuaApiExample
curl -L -R -O https://www.lua.org/ftp/lua-5.4.6.tar.gz
tar zxf lua-5.4.6.tar.gz
cd lua-5.4.6
make all test