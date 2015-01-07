#! perl -w
package Lingua::Rhyme;
our $VERSION = 0.092;

use strict;
use warnings;
use DBI();

=head1 NAME

Lingua::Rhyme - MySQL-based rhyme-lookups.

=head1 SYNOPSIS

First time, to install the dictionary:

	use Lingua::Rhyme;
	$Lingua::Rhyme::chat=1;
	$Lingua::Rhyme::DATABASE = "rhymedict";
	$Lingua::Rhyme::USER	 = "MyUserName";
	$Lingua::Rhyme::PASSWORD = "password";

	Lingua::Rhyme::build('C:/lang/win2k/perl/site/lib/lingua');

Thereafter:

	use Lingua::Rhyme;
	$Lingua::Rhyme::DATABASE = "rhymedict";
	$Lingua::Rhyme::USER	 = "MyUserName";
	$Lingua::Rhyme::PASSWORD = "password";

	my @rhymes_for_house = @{ Lingua::Rhyme::simplefind('house') };

	my @rhymes_for_tomAto = @{ Lingua::Rhyme::simplefind('tomato') };

	warn "Test if 'house' rhymes with 'mouse'....\n";
	if (simplematch("house","mouse")){
		warn "They rhyme.\n";
	} else {
		warn "They don't rhyme!";
	}

	warn syllable("contrary");


	__END__


=head1 DESCRIPTION

This module uses an SQL database of rhyming words to find words that rhyme. See L<the &build function|"&build"> for further information.

This is actually Text::Rhyme version 0.04, but rhyming is now considered a linguist, rather than a textual, operation.

=head1 INSTALLATION

See the enclosed file, C<INSTALL>.

=head1 PREREQUISITES

L<DBI.pm|<DBI.pm>,
L<DBD::mysql.pm|<DBD::mysql>,

=head1 CLASS VARIABLES

=over 4

=item $chat

You can set this for real-time chat on what's up, leave as C<undef> for silent operation.

=item $DATABASE

The name of the rhyming dictionary database that will be created. Defaults to C<rhymedict>.

=item $DRIVER

The DBI::* driver, defaults to C<mysql>.

=item $HOSTNAME, $PORT, $USER. $PASSWORD

The following variables must be set by the user to access the database.

=back

=cut

our $chat;

our $DATABASE = "rhymedict";
our $HOSTNAME = "localhost";
our $PORT     = "3306";
our $USER     = 'NotAdministrator';
our $PASSWORD = 'password';
our $DRIVER   = "mysql";

our $_connected;


=head1 FUNCTIONS

Functions begining with the word C<simple> will not take into account multiple pronunciations, for which use functions ending with the word C<all>.

=head2 &build

Running this function will fill the database C<> with three tables
from the supplied textfiles, C<words.txt>, C<rhymes.txt>, and C<multiple.txt>,
which should be in the C<Rhyme/dict/EN/> sub-directory of this module's location..
If these tables exist, they will be dropped.

If one paramter is supplied, it should be the directory in which this module is installed in.

If no paramter is supplied, the script will use the first value it finds in
C<@INC> that contains the string C<site>, because we assume this module is
installed in a standard location. To avoid this, call with the paramter C<undef>.

NB> the process will be as slow as your system: YMMV.

=cut

sub build {
	local (*WORDS,*RHYMES);
	my ($base, $chat)=('',1);
	if (defined $_[0]){
		$base = shift;
	} else {
		foreach (@INC){
			$base = $_ if /site/;
			last;
		}
	}
	die "Please read the POD and edit the source code to set the database-access variables."
		if (not defined $USER and not defined $PASSWORD);
	die "Could not find words.txt from which to build db!\nDir: $base"
		if not -e "$base/Rhyme/dict/EN/words.txt";
	die "Could not find rhymes.txt from which to build db!\nDir: $base"
		if not -e "$base/Rhyme/dict/EN/rhymes.txt";
	die "Could not find multiple.txt from which to build db!\nDir: $base"
		if not -e "$base/Rhyme/dict/EN/multiple.txt";

	warn "Setting up db connection...\n" if $chat;
	our $dsn = "DBI:$DRIVER:database=$DATABASE;host=$HOSTNAME;port=$PORT";
	our $dbh = DBI->connect($dsn, $USER, $PASSWORD);
	DBI->install_driver("mysql");

	#
	# Create a new tables: **words**
	#
	warn "Building table words...\n" if $chat;
	$dbh->do("DROP TABLE IF EXISTS words");
	$dbh->do("CREATE TABLE words "
			."("
				. "word	char(255) NOT NULL, "
				. "idx	char(10) NOT NULL, "
				. "syllables int NOT NULL, "
				. "PRIMARY KEY(word) "
			. ")"
	);

	open WORDS,"$base/Rhyme/dict/EN/words.txt" or die "Couldn't find words.txt from which to build db table!";
	while (<WORDS>){
		my ($word, $idx, $syllables) = split /\s/,$_;
		$dbh->do("INSERT INTO words (word,idx,syllables) VALUES ( " .$dbh->quote($word).",".$dbh->quote($idx).",$syllables)");
	}
	close WORDS;

	#
	# Create a new tables: **rhymes**
	#
	warn "Building table rhymes...\n" if $chat;
	$dbh->do("DROP TABLE IF EXISTS rhymes");
	$dbh->do("CREATE TABLE rhymes "
			."("
				. "idx	char(10) NOT NULL, "
				. "rhymes text NOT NULL, "
				. "PRIMARY KEY(idx) "
			. ")"
	);

	open RHYMES,"$base/Rhyme/dict/EN/rhymes.txt" or die "Couldn't find rhymes.txt from which to build db table!";
	while (<RHYMES>){
		my ($idx, $rhymes) = split /\s/,$_,2;
		$dbh->do("INSERT INTO rhymes (idx,rhymes) VALUES ( " .$dbh->quote($idx).",".$dbh->quote($rhymes).")");
	}
	close WORDS;


	#
	# Create a new tables: **multiple**
	#
	warn "Building table multiple...\n" if $chat;
	$dbh->do("DROP TABLE IF EXISTS multiple");
	$dbh->do("CREATE TABLE multiple "
			."("
				. "word	char(255) NOT NULL, "
				. "multiples text NOT NULL, "
				. "PRIMARY KEY(word) "
			. ")"
	);

	open MULTIPLE,"$base/Rhyme/dict/EN/multiple.txt" or die "Couldn't find multiple.txt from which to build db table!";
	while (<MULTIPLE>){
		my ($word, $multiples) = split /\s/,$_,2;
		$dbh->do("INSERT INTO multiple (word,multiples) VALUES ( " .$dbh->quote($word).",".$dbh->quote($multiples).")");
	}
	close WORDS;

	warn "All built without problems, disconnecting...\n" if $chat;
	$dbh->disconnect();
	warn "...disconnected from db.\n" if $chat;
} # End sub build




#
# Private subroutine _connect just sets up the dbh is not already done so
# stores in global $_connected
#
sub _connect {
	if (defined $_connected) {
		#warn "Already connected to db.\n" if $chat; return $_connected
	}
	die "Please read the POD and edit the source code to set the database-access variables."
		if (not defined $USER and not defined $PASSWORD);
	warn "Connecting to db...\n" if $chat;
	my $dsn = "DBI:$DRIVER:database=$DATABASE;host=$HOSTNAME;port=$PORT";
	my $dbh = DBI->connect($dsn, $USER, $PASSWORD);
	DBI->install_driver("mysql");
	$_connected = $dbh;
	return $dbh;
}

#
# Private subroutine _disconnect disconnects the global connection if it exists, otherwise
# can disconnect a specific dbh if passed.
#
sub _disconnect {
	warn "Disconnecting from db.\n" if $chat;
	if (defined $_connected) { $_connected->disconnect() }
	else { $_[0]->disconnect() }
}




=head2 &simplefind ($word_to_match)

Accepts B<a scalar> of one word to lookup, and returns a B<reference to an array> of rhyming words, or C<undef> if the word isn't in the dictionary.

=cut

sub simplefind { my ($lookup) = (uc shift);
	unless (defined $lookup) {
		warn "&simplefind requires a scalar to lookup as its sole argument.";
		return undef;
	}
	$_ = _simplefind(_connect,$lookup);
	_disconnect;
	return $_;
}


#
# Privaet sub _simplefind same as public simplefind but doesn't connect/disconnect
# Accepts: dbh ref, scalar for word to lookup
# Returns: ref to array
#
sub _simplefind { my ($dbh,$lookup) = (shift,shift);
	my $sth;
	my $rhymes_ref;
	die "_simplefind requires 2 args " unless defined $dbh and defined $lookup;
	warn "Looking up '$lookup' ... \n" if $chat;
	$sth = $dbh->prepare("SELECT idx FROM words WHERE word = ".$dbh->quote($lookup) );
	$sth->execute();
	my $idx_ref = $sth->fetchrow_arrayref();
	warn "... and got @$idx_ref\n" if defined $idx_ref and $chat;
	$sth->finish();
	if (defined $idx_ref){
		warn "Looking up index '@$idx_ref' ...\n"  if $chat;
		$sth = $dbh->prepare("SELECT rhymes FROM rhymes WHERE idx = ".$dbh->quote(@$idx_ref) );
		$sth->execute();
		if  ($rhymes_ref = $sth->fetchrow_arrayref() ) {
			chomp @$rhymes_ref;
			warn "... and got '@$rhymes_ref'\n"  if $chat;
		} else {
			warn "... and got nothing!\n"  if $chat;
		}
		$sth->finish();
		@$rhymes_ref[0] =~ s/\(\d+\)//g;	# Remove number refs
		@_ = split' ',@$rhymes_ref[0];
	} else {
		@_ = ();
		warn "Got nothing from db for '$lookup'.\n" if $chat
	}
	return \@_;
}



=head2 &findall ($word_to_lookup)

Accepts a scalar as a word to look up, and returns a reference to an array containing all the matches for all pronunciations of the word.

=cut

sub findall { my ($lookup) = (uc shift);
	unless (defined $lookup) {
		warn "&findall requires a scalar to lookup as its sole argument.";
		return undef;
	}
	my @found = ();
	my $sth;
	my $dbh = _connect;

	warn "Looking up '$lookup' in multiple db  ... \n" if $chat;
	$sth = $dbh->prepare("SELECT multiples FROM multiple WHERE word = ".$dbh->quote($lookup) );
	$sth->execute();
	my $lookup_ref = $sth->fetchrow_arrayref();
	warn "... and got @$lookup_ref\n" if $chat and defined $lookup_ref;
	$sth->finish();

	# Not in mulitple table, try words table by setting the value explicitly
	$lookup_ref = [$lookup] if (not defined $lookup_ref);

	foreach my $lookup (split' ',@$lookup_ref[0]){
		push @found, @{_simplefind($dbh, $lookup)};
	}

	_disconnect();

	# Remove duplicates
	my %dropdupes = map { $_ => 1 } @found;
	@found = sort keys %dropdupes;

	return \@found;
}



=head2 &simplematch ($word1,$word2)

Accepts two words as scalars and returns C<1> if C<$word1> rhymes with C<$word2>, otherwise returns C<undef>.

=cut

sub simplematch { my ($lookup,$against) = (uc shift, uc shift);
	unless (defined $lookup or not defined $against) {
		warn "&lookup requires a scalar to lookup, and a scalar to match against as its two arguments.";
		return undef;
	}
	my $found;
	my $dbh = _connect;
	foreach (@{_simplefind($dbh,$lookup)}) {
		if ($_ eq $against){
			$found = 1;
			last;
		}
	}
	_disconnect($dbh);
	return $found;
}





=head2 &matchall ($word_to_compare, $word2_to_compare);

See if two words rhyme. Accepts two scalars to compare, and returns C<1> on success, otherwise C<undef>.

=cut

sub matchall {
	my @words;
	($words[0],$words[1]) = (uc $_[0], uc $_[1]);
	unless (defined $words[0]and defined $words[1]) {
		warn "&findall requires two scalars to lookup as its two arguments.";
		return undef;
	}
	my $success;	# undef
	my @found = {};
	my $sth;
	my $dbh = _connect;

	CHECKBOTH:
	for my $i (0..1){
		warn "Looking up word $i ('$words[$i]') in multiple db  ... \n" if $chat;
		$sth = $dbh->prepare("SELECT multiples FROM multiple WHERE word = ".$dbh->quote($words[$i]) );
		$sth->execute();
		my $lookup_ref = $sth->fetchrow_arrayref();
		warn "... and got @$lookup_ref\n" if $chat and defined $lookup_ref;
		$sth->finish();

		# Not in mulitple table, try words table by setting the value explicitly
		$lookup_ref = [$words[$i]] if (not defined $lookup_ref);

		foreach my $lookup (split' ',@$lookup_ref[0]){
			foreach ( @{_simplefind($dbh, $lookup)} ){
				$found[$i]{$_} = 1;
				if (exists $found[$i]{$words[0]} and exists $found[$i]{$words[1]}){
					$success = 1;
					last CHECKBOTH;
				}
			}
		}
	}
	_disconnect();
	return $success;
}



=head2 &syllable ($word_to_lookup)

Accepts a word to look up, and returns the number of syllables in the word supplied, or C<undef> if the word isn't in the dictionary.

=cut

sub syllable { my ($lookup) = (uc shift);
	my $s = _syllable(_connect,$lookup);
	_disconnect;
	return $s;
}



#
# Private sub _syllable
# Accepts dbh and word to lookup
# Returns number of syllables id'ed in db for word to lookup, or undef
#
sub _syllable { my ($dbh,$lookup) = (shift,shift);
	my $sth;
	my $rhymes_ref;
	warn "Looking up '$lookup' ... \n" if $chat;
	$sth = $dbh->prepare("SELECT syllables FROM words WHERE word = ".$dbh->quote($lookup) );
	$sth->execute();
	my $syl_ref = $sth->fetchrow_arrayref();
	warn "... and got @$syl_ref[0] syllable\n" if defined $syl_ref and $chat;
	return defined $syl_ref? @$syl_ref[0]  : undef;
}














1;
__END__




=head1 CAVEATS

There appear to be duplicate entires in the DB:

	DBD::mysql::db do failed: Duplicate entry '#?2,M+?*.+' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 13570.
	DBD::mysql::db do failed: Duplicate entry '7*?7\.?/.N' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 16070.
	DBD::mysql::db do failed: Duplicate entry 'E,[' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 20111.
	DBD::mysql::db do failed: Duplicate entry 'E1=' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 20397.
	DBD::mysql::db do failed: Duplicate entry '02)?#D/.?2' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 20623.
	DBD::mysql::db do failed: Duplicate entry 'e,:' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 25587.
	DBD::mysql::db do failed: Duplicate entry 'E)@' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 25605.
	DBD::mysql::db do failed: Duplicate entry 'e):' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 30844.
	DBD::mysql::db do failed: Duplicate entry 'e2:' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 30983.
	DBD::mysql::db do failed: Duplicate entry 'e"[' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 34284.
	DBD::mysql::db do failed: Duplicate entry 'E#,U' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 34545.
	DBD::mysql::db do failed: Duplicate entry 'e4:' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 34637.
	DBD::mysql::db do failed: Duplicate entry '-T2,M+?*.+' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 36221.
	DBD::mysql::db do failed: Duplicate entry '/B+,=' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 41578.
	DBD::mysql::db do failed: Duplicate entry '4T2)A#?/.N' for key 1 at E:\Src\Pl\Text\Rhyme\build.pl line 53, <WORDS> line 41821.

=head1 TODO

=item Tidy

Tidy the db accessing, error messaging and catching,  maybe?

=item Languages

If I can find dictionaries for German and Yiddish (or others), I'll add those too.

=head1 SEE ALSO

L<Lingua::Rhyme::FindScheme>;
L<DBI>;
L<MySQL|http://www.mysql.com>;
L<The Rhyming Dictionary|http://rhyme.sourceforge.net/index.html>;
L<Carnegie Mellon University Pronouncing Dictionary|http://www.speech.cs.cmu.edu/cgi-bin/cmudict>;
perl(1).

=head1 ACKNOWLEDGMENTS

A thousand thanks to Brian "tuffy" Langenberger for the database files used in his L<Rhyming Dictionary|http://rhyme.sourceforge.net/index.html>.  Brain writes that his 'work is based wholly on the work of the L<Carnegie Mellon University Pronouncing Dictionary|http://www.speech.cs.cmu.edu/cgi-bin/cmudict>'.

=head1 AUTHOR

Lee Goddard <lgoddard@cpan.org>

=head1 CHANGES

Revision history for Perl extension Text::Rhyme.

	0.081 Mon Apr 08 19:32 2002
		- fixed buy in syllable

	0.08  Mon Apr 08 19:22 2002
		- tidied up POD and modified param of C<build()>.

	0.07  Fri Jun 01 12:12:00 2001
		- added matchall routine

	0.06  Thu May 31 14:35:00 2001
		- corrected connection bug

	0.05  Thu May 31 13:13:00 2001
		- added multiple.txt db
		- added new functions and renamed old functions

	0.04  Wed May 30 19:01:25 2001
		- completely rewritten - now uses a MySQL DB.
		- moved namespace, as rhyming is now a linguist, not textual, operation (if it ever was).

	0.03  Tue May 29 13:35:12 2001
		- ACTUALLY text-rhyme-0.03
		- added parsing of final consenants. Still I can't spell.

	0.02  Tue May 29 12:32:00 2001
		- ACTUALLY text-rhyme-0.02
		- damn, got the module name wrong!

	0.01  Tue May 29 12:18:12 2001
		- ACTUALLY text-rhyme-0.01
		- original version; created by h2xs 1.20 with options

			-Xcfn Text::Rhyme




=head1 COPYRIGHT

Copyright (C) Lee Goddard, 30/05/2001 ff.

This is free software, and can be used/modified under the same terms as Perl itself.

=cut
