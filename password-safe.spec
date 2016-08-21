%define sname pwsafe

Summary:	A cross-platform password database utility
Name:		password-safe
Version:	0.99
Release:	1
License:	Artistic
Group:		File tools
URL:		https://pwsafe.org/
Source0:	%{sname}-%{version}BETA-src.tgz
#Source0:	https://github.com/pwsafe/%{sname}/releases/download/%{version}BETA/%{sname}-%{version}BETA-src.tgz
Source1:	%{sname}-%{version}BETA-src.tgz.sig
#Source1:	https://github.com/pwsafe/%{sname}/releases/download/%{version}BETA/%{sname}-%{version}BETA-src.tgz.sig
Patch0:		%{name}-0.99-static_libs.patch
Patch1:		%{name}-0.99-test_missing_link.patch

BuildRequires:	cmake
BuildRequires:	gtest-devel
BuildRequires:	imagemagick
BuildRequires:	libyubikey-devel
BuildRequires:	wxgtku3.0-devel
BuildRequires:	zip
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(xerces-c)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(ykpers-1)

%description
Password Safe is a password database utility. Like many other such
products, commercial and otherwise, it stores your passwords in an
encrypted file, allowing you to remember only one password (the "safe
combination"), instead of all the username/password combinations that
you use.

%files -f %{name}.lang
%{_bindir}/%{sname}
%{_datadir}/%{sname}/
%{_datadir}/applications/%{sname}.desktop
%{_datadir}/pixmaps/%{sname}.xpm
%{_iconsdir}/hicolor/*/apps/%{sname}.png
%{_mandir}/man1/%{sname}.1*
%docdir docs/help
%doc README.txt
%doc README.LINUX
%doc docs/pwsafe-state-machine.rtf
%doc docs/help.txt
%doc docs/config.txt
%doc docs/formatV1.txt
%doc docs/formatV2.txt
%doc docs/formatV3.txt
%doc docs/ChangeLog.txt
%doc docs/ReleaseNotes.txt
%doc docs/*.html
%doc docs/LICENSE.rtf

%prep
%setup -q -n %{sname}-%{version}BETA

# apply all patches
%patch0 -p1 -b .static
%patch1 -p1 -b .link

# fix help dir path
%__sed -i -e 's|/usr/share/doc/password-safe/help/|%{_docdir}/%{name}/help/|' src/os/unix/dir.cpp

%build
%cmake
%make

%install
%make_install -C build

# .desktop file
%__install -dm 755 %{buildroot}%{_datadir}/applications/
%__mv %{buildroot}%{_datadir}/%{sname}/%{sname}.desktop \
	%{buildroot}%{_datadir}/applications/%{sname}.desktop

# icons
for dim in 16x16 32x32 48x48 64x64 72x72 128x128
do
	%__install -dm 755 %{buildroot}%{_iconsdir}/hicolor/"$dim"/apps/
	convert -background none install/graphics/%{sname}.png \
		-scale "$dim" %{buildroot}%{_iconsdir}/hicolor/"$dim"/apps/%{sname}.png
done
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps/
convert -background none install/graphics/%{sname}.png \
	-scale 32x32 %{buildroot}%{_datadir}/pixmaps/%{sname}.xpm

# localizations
%find_lang %{name} --all-name

# help
%__install -dm 0755 %{buildroot}%{_docdir}/%{name}/help/
%__install -pm 0644 build/help/help*zip %{buildroot}%{_docdir}/%{name}/help/

# we are not Debian
%__rm -fr %{buildroot}%{_docdir}/passwordsafe

%check
# desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{sname}.desktop

