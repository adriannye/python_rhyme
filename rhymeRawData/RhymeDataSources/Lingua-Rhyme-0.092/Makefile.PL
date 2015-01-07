use ExtUtils::MakeMaker;

WriteMakefile(
    'NAME'		=> 'Lingua::Rhyme',
    'VERSION_FROM'	=> 'Rhyme.pm',
    'PREREQ_PM'		=> {DBI=>0.01},
);
