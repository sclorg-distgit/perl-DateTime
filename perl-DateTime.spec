%{?scl:%scl_package perl-DateTime}

Name:           %{?scl_prefix}perl-DateTime
Epoch:          2
Version:        1.34
Release:        2%{?dist}
Summary:        Date and time object for Perl
License:        Artistic 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DateTime/
Source0:        http://www.cpan.org/authors/id/D/DR/DROLSKY/DateTime-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-devel
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.76
%if %{defined perl_small}
BuildRequires:  sed
%endif
# Run-time:
BuildRequires:  %{?scl_prefix}perl(base)
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(constant)
BuildRequires:  %{?scl_prefix}perl(DateTime::Locale) >= 1.05
BuildRequires:  %{?scl_prefix}perl(DateTime::TimeZone) >= 2.00
BuildRequires:  %{?scl_prefix}perl(Dist::CheckConflicts) >= 0.02
BuildRequires:  %{?scl_prefix}perl(integer)
BuildRequires:  %{?scl_prefix}perl(overload)
BuildRequires:  %{?scl_prefix}perl(Params::Validate) >= 1.03
BuildRequires:  %{?scl_prefix}perl(POSIX)
BuildRequires:  %{?scl_prefix}perl(Scalar::Util)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(Try::Tiny)
BuildRequires:  %{?scl_prefix}perl(vars)
BuildRequires:  %{?scl_prefix}perl(warnings)
BuildRequires:  %{?scl_prefix}perl(warnings::register)
# Optional Run-time:
BuildRequires:  %{?scl_prefix}perl(XSLoader)
# Tests:
%if !%{defined perl_small}
BuildRequires:  %{?scl_prefix}perl(CPAN::Meta::Check) >= 0.011
%endif
BuildRequires:  %{?scl_prefix}perl(CPAN::Meta::Requirements)
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(Test::Fatal)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.96
BuildRequires:  %{?scl_prefix}perl(Test::Warnings) >= 0.005
BuildRequires:  %{?scl_prefix}perl(utf8)
# Optional Tests:
BuildRequires:  %{?scl_prefix}perl(CPAN::Meta) >= 2.120900
BuildRequires:  %{?scl_prefix}perl(Storable)
%if !%{defined perl_small}
BuildRequires:  %{?scl_prefix}perl(Test::Warn)
%endif
# Dependencies:
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(XSLoader)

%if 0%{?rhel} < 7
# RPM 4.8 style
# Avoid provides from DateTime.so
# Filter under-specified dependencies
%{?filter_setup:
%filter_from_requires /^%{?scl_prefix}perl(DateTime::Locale)$/d
%filter_from_requires /^%{?scl_prefix}perl(DateTime::TimeZone)$/d
%filter_from_requires /^%{?scl_prefix}perl(Params::Validate)$/d
%?perl_default_filter
}
%else
# RPM 4.9 style
# Avoid provides from DateTime.so
%{?perl_default_filter}
# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\((DateTime::Locale|DateTime::TimeZone|Params::Validate)\\)$
%endif

%description
DateTime is a class for the representation of date/time combinations.  It
represents the Gregorian calendar, extended backwards in time before its
creation (in 1582). This is sometimes known as the "proleptic Gregorian
calendar". In this calendar, the first day of the calendar (the epoch), is the
first day of year 1, which corresponds to the date which was (incorrectly)
believed to be the birth of Jesus Christ.

%prep
%setup -q -n DateTime-%{version}
%if %{defined perl_small}
rm t/zzz-check-breaks.t
sed -i -e '/^t\/zzz-check-breaks\.t/d' MANIFEST
%endif

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc LICENSE
%doc Changes CONTRIBUTING.md CREDITS README.md TODO
%{perl_vendorarch}/auto/DateTime/
%{perl_vendorarch}/DateTime/
%{perl_vendorarch}/DateTime.pm
%{_mandir}/man3/DateTime.3*
%{_mandir}/man3/DateTime::Duration.3*
%{_mandir}/man3/DateTime::Infinite.3*
%{_mandir}/man3/DateTime::LeapSecond.3*

%changelog
* Mon Jul 11 2016 Petr Pisar <ppisar@redhat.com> - 2:1.34-2
- SCL

* Wed Jul  6 2016 Paul Howarth <paul@city-fan.org> - 2:1.34-1
- Update to 1.34
  - Added the leap second coming on December 31, 2016

* Wed Jun 29 2016 Paul Howarth <paul@city-fan.org> - 2:1.33-1
- Update to 1.33
  - When you pass a locale to $dt->set you will now get a warning suggesting
    you should use $dt->set_locale instead (CPAN RT#115420)
  - Added support for $dt->truncate( to => 'quarter' ) (GH#17)
  - Fixed the $dt->set docs to say that you cannot pass a locale (even though
    you can but you'll get a warning) and added more docs for $dt->set_locale
  - Require DateTime::Locale 1.05
  - Require DateTime::TimeZone 2.00
- Take advantage of NO_PACKLIST option in recent EU:MM

* Sun May 22 2016 Paul Howarth <paul@city-fan.org> - 2:1.28-1
- Update to 1.28
  - Fixed handling of some floating point epochs; since DateTime treated the
    epoch like a string instead of a number, certain epochs with a non-integer
    value ended up treated like integers (Perl is weird) (GH#15, fixes GH#6)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.27-2
- Perl 5.24 rebuild

* Sat May 14 2016 Paul Howarth <paul@city-fan.org> - 2:1.27-1
- Update to 1.27
  - Added an environment variable PERL_DATETIME_DEFAULT_TZ to globally set the
    default time zone (GH#14); using this is very dangerous - be careful!
- BR: perl-generators

* Tue Mar 22 2016 Paul Howarth <paul@city-fan.org> - 2:1.26-1
- Update to 1.26
  - Switched from Module::Build to ExtUtils::MakeMaker (GH#13)

* Mon Mar  7 2016 Paul Howarth <paul@city-fan.org> - 2:1.25-1
- Update to 1.25
  - DateTime->from_object would die if given a DateTime::Infinite object; now
    it returns another DateTime::Infinite object (CPAN RT#112712)
- Simplify find command using -empty and -delete

* Tue Mar  1 2016 Paul Howarth <paul@city-fan.org> - 2:1.24-1
- Update to 1.24
  - The last release partially broke $dt->time; if you passed a value to use
    as unit separator, it was ignored (CPAN RT#112585)

* Mon Feb 29 2016 Paul Howarth <paul@city-fan.org> - 2:1.23-1
- Update to 1.23
  - Fixed several issues with the handling of non-integer values passed to
    from_epoch() (GH#11)
    - This method was simply broken for negative values, which would end up
      being incremented by a full second, so for example -0.5 became 0.5
    - The method did not accept all valid float values; specifically, it did
      not accept values in scientific notation
    - Finally, this method now rounds all non-integer values to the nearest
      millisecond, which matches the precision we can expect from Perl itself
      (53 bits) in most cases
  - Make all DateTime::Infinite objects return the system's representation of
    positive or negative infinity for any method that returns a number or
    string representation (year(), month(), ymd(), iso8601(), etc.); previously
    some of these methods could return "Nan", "-Inf--Inf--Inf", and other
    confusing outputs (CPAN RT#110341)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Paul Howarth <paul@city-fan.org> - 2:1.21-1
- Update to 1.21
  - Make all tests pass with the current DateTime::Locale
- Explicitly BR: perl-devel, needed for EXTERN.h

* Fri Jul 24 2015 Petr Pisar <ppisar@redhat.com> - 2:1.20-1
- 1.20 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.18-2
- Perl 5.22 rebuild

* Tue Jan  6 2015 Paul Howarth <paul@city-fan.org> - 2:1.18-1
- 1.18 bump

* Mon Jan  5 2015 Paul Howarth <paul@city-fan.org> - 2:1.17-1
- 1.17 bump
- Use %%license
- Make %%files list more explicit

* Mon Jan  5 2015 Paul Howarth <paul@city-fan.org> - 2:1.14-1
- 1.14 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.12-2
- Perl 5.20 rebuild

* Tue Sep 02 2014 Petr Pisar <ppisar@redhat.com> - 2:1.12-1
- 1.12 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.10-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Petr Pisar <ppisar@redhat.com> - 2:1.10-1
- 1.10 bump

* Fri Mar 14 2014 Paul Howarth <paul@city-fan.org> - 2:1.08-1
- 1.08 bump

* Mon Feb 10 2014 Paul Howarth <paul@city-fan.org> - 2:1.07-1
- 1.07 bump

* Fri Jan 03 2014 Petr Pisar <ppisar@redhat.com> - 2:1.06-1
- 1.06 bump

* Tue Dec 10 2013 Petr Pisar <ppisar@redhat.com> - 2:1.04-1
- 1.04 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 2:1.03-2
- Perl 5.18 rebuild

* Tue Jun 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.03-1
- 1.03 bump

* Tue Apr 02 2013 Petr Šabata <contyk@redhat.com> - 2:1.01-1
- 1.01 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Petr Pisar <ppisar@redhat.com> - 2:0.78-1
- 0.78 bump

* Thu Oct 18 2012 Petr Pisar <ppisar@redhat.com> - 2:0.77-1
- 0.77 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 2:0.70-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Iain Arnell <iarnell@gmail.com> 2:0.70-2
- Additional (Build)Requires from unofficial review

* Mon Aug 15 2011 Iain Arnell <iarnell@gmail.com> 2:0.70-1
- Unbundle DateTime::TimeZone and DateTime::Locale
- Bump epoch and revert to upstream versioning
- Specfile regenerated by cpanspec 1.78.
- Update description

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1:0.7000-3
- Perl mass rebuild

* Mon Jul 04 2011 Iain Arnell <iarnell@gmail.com> 1:0.7000-2
- update DateTime::TimeZone to 1.35 (Olson 2011h)
- add rpm 4.9 filtering macros

* Fri May 13 2011 Iain Arnell <iarnell@gmail.com> 1:0.7000-1
- update DateTime to 0.70

* Wed May 04 2011 Iain Arnell <iarnell@gmail.com> 1:0.6900-1
- update DateTime to 0.69
- update DateTime::TimeZone to 1.34 (Olson 2011g)

* Sun Apr 24 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-6
- fix the testing for loop

* Sun Apr 24 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-5
- update DateTime::TimeZone to 1.33 (Olson 2011f)

* Wed Apr 06 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-4
- update DateTime::TimeZone to 1.32 (Olson 2011e)

* Sat Mar 26 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-3
- update DateTime::TimeZone to 1.31
- DateTime::TimeZone no longer has Build.PL; use Makefile.PL
- whitespace cleanup
- clean up .packlist

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.6600-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Steven Pritchard <steve@kspei.com> 1:0.6600-1
- Update DateTime to 0.66.
- Update DateTime::TimeZone to 1.26.
- Update URL for FAQ in description.
- BR Class::Load and parent.

* Sat Oct 09 2010 Iain Arnell <iarnell@gmail.com> 1:0.6300-1
- Update DateTime to 0.63
- Update DateTime::TimeZone to 1.22
- DateTime license changed from "GPL+ or Artistic" to "Artistic 2.0"
- Fix DTLocale/Changelog encoding

* Mon Jun 14 2010 Petr Sabata <psabata@redhat.com> - 1:0.5300-4
- perl-DateTime-Locale-0.45 update

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.5300-3
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 1:0.5300-2
- new upstream version of DateTime-TimeZone

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 1:0.5300-1
- new upstream version
- use Build.PL as Makefile.PL no longer exists
- use iconv to recode to utf-8, not a patch
- update BuildRequires
- drop Provides: %{?scl_prefix}perl(DateTime::TimeZoneCatalog), it is no longer there
- use filtering macros

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:0.4501-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4501-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4501-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 09 2008 Steven Pritchard <steve@kspei.com> 1:0.4501-1
- Update to DateTime 0.4501.

* Mon Nov 10 2008 Steven Pritchard <steve@kspei.com> 1:0.4401-1
- Update to DateTime 0.4401.
- Update to DateTime::Locale 0.42.
- Update to DateTime::TimeZone 0.8301.

* Mon Sep 08 2008 Steven Pritchard <steve@kspei.com> 1:0.4304-2
- Update to DateTime::TimeZone 0.7904.

* Tue Jul 15 2008 Steven Pritchard <steve@kspei.com> 1:0.4304-1
- Update to DateTime 0.4304.
- Update to DateTime::TimeZone 0.78.
- Update to DateTime::Locale 0.41.

* Tue Jul 08 2008 Steven Pritchard <steve@kspei.com> 1:0.4302-2
- Update to DateTime::TimeZone 0.7701.

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 1:0.4302-1
- Update to DateTime 0.4302.
- Update to DateTime::TimeZone 0.77.
- Update to DateTime::Locale 0.4001.
- BR List::MoreUtils.
- Define IS_MAINTAINER so we run the pod tests.

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 1:0.42-1
- Update to DateTime 0.42.
- Update to DateTime::TimeZone 0.75.
- Update FAQ URL in description.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.41-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.41-4
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.41-3
- rebuild for new perl

* Tue Dec 11 2007 Steven Pritchard <steve@kspei.com> 1:0.41-2
- Update License tag.
- Update to DateTime::TimeZone 0.70.

* Mon Sep 17 2007 Steven Pritchard <steve@kspei.com> 1:0.41-1
- Update to DateTime 0.41.
- Update to DateTime::Locale 0.35.
- Update to DateTime::TimeZone 0.67.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1:0.39-2
- Rebuild for selinux ppc32 issue.

* Sun Jul 22 2007 Steven Pritchard <steve@kspei.com> 1:0.39-1
- Update to DateTime 0.39.
- Update to DateTime::TimeZone 0.6603.

* Thu Jul 05 2007 Steven Pritchard <steve@kspei.com> 1:0.38-2
- BR Test::Output.

* Mon Jul 02 2007 Steven Pritchard <steve@kspei.com> 1:0.38-1
- Update to DateTime 0.38.
- Update to DateTime::TimeZone 0.6602.
- BR Test::Pod::Coverage.

* Mon Apr 02 2007 Steven Pritchard <steve@kspei.com> 1:0.37-3
- Drop BR DateTime::Format::* to avoid circular build deps.

* Mon Apr 02 2007 Steven Pritchard <steve@kspei.com> 1:0.37-2
- Filter Win32::TieRegistry dependency.
- Do the provides filter like we do in cpanspec.
- Drop some macro usage.

* Sat Mar 31 2007 Steven Pritchard <steve@kspei.com> 1:0.37-1
- Update to DateTime 0.37.
- Update to DateTime::TimeZone 0.63.

* Tue Mar 13 2007 Steven Pritchard <steve@kspei.com> 1:0.36-2
- Update to DateTime::Locale 0.34.
- Update to DateTime::TimeZone 0.62.

* Mon Jan 22 2007 Steven Pritchard <steve@kspei.com> 1:0.36-1
- Update to Date::Time 0.36.
- Update to DateTime::Locale 0.33.
- Update to DateTime::TimeZone 0.59.

* Fri Nov 03 2006 Steven Pritchard <steve@kspei.com> 1:0.35-1
- Update to DateTime 0.35.
- Update to DateTime::Locale 0.3101.
- LICENSE.icu seems to have been renamed LICENSE.cldr.
- Update to DateTime::TimeZone 0.54.
- Use fixperms macro instead of our own chmod incantation.
- Convert DateTime::LeapSecond to UTF-8 to avoid a rpmlint warning.

* Tue Aug 29 2006 Steven Pritchard <steve@kspei.com> 1:0.34-3
- Update to DateTime::TimeZone 0.48.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 1:0.34-2
- Update to DateTime::TimeZone 0.47.

* Mon Aug 14 2006 Steven Pritchard <steve@kspei.com> 1:0.34-1
- Update to DateTime 0.34.

* Fri Jul 28 2006 Steven Pritchard <steve@kspei.com> 1:0.32-1
- Update to DateTime 0.32.
- Improve Summary, description, and source URLs.
- Fix find option order.

* Thu Jul 13 2006 Steven Pritchard <steve@kspei.com> 1:0.31-2
- BR DateTime::Format::ICal and DateTime::Format::Strptime for better
  test coverage.

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1:0.31-1
- Update DateTime to 0.31.
- Update DateTime::TimeZone to 0.46.

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 1:0.30-3
- Bump Epoch (argh, 0.2901 > 0.30 to rpm)
- Update DateTime::TimeZone to 0.42

* Sat Feb 18 2006 Steven Pritchard <steve@kspei.com> 0.30-2
- Update DateTime::TimeZone to 0.41

* Tue Jan 10 2006 Steven Pritchard <steve@kspei.com> 0.30-1
- Update DateTime to 0.30
- Update DateTime::TimeZone to 0.40

* Fri Sep 16 2005 Paul Howarth <paul@city-fan.org> 0.2901-2
- Unpack each tarball only once
- Use Module::Build's build script where available
- Help each module find the others when needed
- Clean up files list
- Include additional documentation from DT::Locale & DT::TimeZone
- Add BR: perl(File::Find::Rule) & perl(Test::Pod) to improve test coverage
- Remove unversioned provides of perl(DateTime) & perl(DateTime::TimeZone)

* Wed Aug 31 2005 Steven Pritchard <steve@kspei.com> 0.2901-1
- Specfile autogenerated.
