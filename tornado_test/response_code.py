#! /usr/bin/env python3
"""
响应码定义
"""
# 认证错误CODE
AuthenticationHeaderError = 1000
UserError = 1001
TokenError = 1002
LoginExpired = 1003
PleaseLogin = 1004
UserOrPasswordError = 1005
UserDisabled = 1006
VerificationCodeError = 1007
PermissionAllowed = 1008

SecondaryAuthentication = 2001

# 提示类
OldTaskNotSupportOperations = 3000
PasswordStrengthLow = 3001
UserNameEmailExist = 3002
GroupNotExist = 3003
GroupExist = 3004
EmptyResult = 3010
AddProjectError = 3020
# --- node Error ----
NodeExist = 3050
NodeOffline = 3051


ParameterError = 5000
ImageFormatError = 5001
# --- celery Error ------
FMT_ERROR = 5090
TARGET_ERROR = 5091

# 网络问题
TimeExpired = 6000
SSLError = 6001
NetError = 6002
# api问题
GoogleConnectError = 6080
WarrantConnectError = 6081
