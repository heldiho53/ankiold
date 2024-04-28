%bcond_without tests
Name:           anki
Version:        2.1.13
Release:        1%{?dist}
Summary:        Spaced-Repetition Memory Training Program
License:        AGPL-3.0-only
Group:          Productivity/Text/Utilities
URL:            https://apps.ankiweb.net/
Source0:        https://github.com/heldiho53/ankiold/releases/download/stable/anki-2.1.13-source.tgz
Source1:        https://raw.githubusercontent.com/heldiho53/ankiold/main/anki.appdata.xml
# PATCH-FIX-OPENSUSE - anki-aqt___init__.py.patch -- Load Qt4 translations from the right place
#Patch1:         %{name}-aqt___init__.py.patch
# PATCH-FIX-OPENSUSE - anki-anki_lang.py.patch -- Load Anki translations from the right place
#Patch2:         %{name}-anki_lang.py.patch
BuildRequires:  python3-markdown
BuildRequires:  python3-pyaudio
BuildRequires:  python3-send2trash
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-decorator
BuildRequires:  python3-jsonschema
BuildRequires:  python3-qt5-devel
BuildRequires:  python3-qt5-webengine
BuildRequires:  python3-requests
BuildRequires:  python3-pytest-mock
Requires:       python3-markdown
Requires:       python3-pyaudio
Requires:       python3-send2trash
Requires:       python3-beautifulsoup4
Requires:       python3-decorator
Requires:       python3-jsonschema
Requires:       python3-qt5
Requires:       python3-qt5-webengine
Requires:       python3-requests
Suggests:       lame
Suggests:       mpv
Suggests:       sox
BuildArch:      noarch
BuildRequires:  fdupes
BuildRequires:  desktop-file-utils
%if %{with tests}
BuildRequires:  python3-nose2
%endif

%description
Anki is a spaced repetition system (SRS). It helps the user remember things by
scheduling reviews, so that the user can learn a lot of information
with the minimum amount of effort.
Anki is content-agnostic and supports images, audio,
videos and scientific markup (via LaTeX).

Anki stores data in ~/.local/share/Anki2, or $XDG_DATA_HOME/Anki2
if the user has set a custom data path.

%prep
%setup -q
#%patch1 -p1
#%patch2 -p1

# SED-FIX-OPENSUSE -- Don't check for new updates.
sed -i -e 's|updates=True|updates=False|;
           s|suppressUpdate=False|suppressUpdate=True|' aqt/profiles.py

# Use dependencies instead of bundled stuff
rm -rf thirdparty

# Remove not needed files
rm -f anki/anki

%build
./tools/build_ui.sh
python3 -m compileall .
python3 -O -m compileall .

%install
%make_install

# install appdata
mkdir -p %{buildroot}%{_datadir}/appdata
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata

# install mime data
mkdir -p %{buildroot}%{_datadir}/mime/packages/
install -m 0644 %{name}.xml %{buildroot}%{_datadir}/mime/packages/

# Remove duplicate and unneeded doc files
rm %{buildroot}%{_datadir}/doc/anki/LICENSE
rm %{buildroot}%{_datadir}/doc/anki/LICENSE.logo
rm %{buildroot}%{_datadir}/doc/anki/README.contributing
rm %{buildroot}%{_datadir}/doc/anki/README.development
rm %{buildroot}%{_datadir}/doc/anki/README.md

%find_lang %{name} %{name}.lang

# Fix rpmlint issues
find %{buildroot}%{_datadir}/%{name}/web/ -name '*.js' -exec chmod a-x {} +
sed -i 's|/usr/bin/env python3|/usr/bin/python3|' %{buildroot}%{_bindir}/%{name}

%check
%if %{with tests}
# to prevent Exception("Anki requires a UTF-8 locale.")
export LC_ALL=en_US.UTF-8
./tools/tests.sh
%endif

%post
update-mime-database %{_datadir}/mime

%postun
update-mime-database %{_datadir}/mime

%files -f %{name}.lang
%doc README.md
%license LICENSE LICENSE.logo
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1%{?ext_man}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/%{name}

%changelog

