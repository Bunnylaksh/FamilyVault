[app]

title = AABHAYA APP
package.name = myfamilyvault
package.domain = org.bharath

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db,json

version = 0.1

requirements = python3==3.12.3,hostpython3==3.12.3,kivy==2.3.1,kivymd==2.0.0

orientation = portrait
osx.kivy_version = 2.2.0
fullscreen = 0

android.permissions = READ_MEDIA_IMAGES

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.accept_sdk_license = True


# Python for Android

p4a.url = https://github.com/kivy/python-for-android.git
p4a.fork = kivy
p4a.branch = v2026.05.09
