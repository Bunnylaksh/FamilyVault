[app]

title = AABHAYA APP
package.name = myfamilyvault
package.domain = org.bharath

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db,json

version = 0.1

requirements = python3==3.11.6,hostpython3==3.11.6,kivy==2.3.1,kivymd,materialshapes==0.3,materialyoucolor==3.0.4,requests==2.34.2,certifi==2026.7.22,charset-normalizer==3.5.1,idna==3.19,urllib3==2.7.0,filetype==1.2.0

orientation = portrait
osx.kivy_version = 2.2.0
fullscreen = 0

android.permissions = READ_MEDIA_IMAGES

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.accept_sdk_license = True

android.api = 33
android.miniapi = 24
android.ndk = 25b
android.ndk_api =24

# In the [app] section, add or modify the android.gradle_dependencies
android.add_src = Modules/grpmodule.c:skip

# Exclude modules not available on Android
android.blacklist_modules = grp

# Python for Android

p4a.url = https://github.com/kivy/python-for-android.git
p4a.fork = kivy
p4a.branch = v2026.05.09

p4a.configure_args = ac_cv_func_getgrouplist=no ac_cv_func_initgroups=no ac_cv_func_getgrouplist=no ac_cv_func_initgroups=no
